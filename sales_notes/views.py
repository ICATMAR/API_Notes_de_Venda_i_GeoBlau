import json
import logging
import os
from datetime import datetime

from django.db import transaction
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from django_ratelimit.decorators import ratelimit
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Envio, RawSalesNote
from .permissions import DARPCanCreateInvestigadorCanRead
from .serializers import EnvioStagingSerializer

logger = logging.getLogger(__name__)


class EnvioViewSet(
    mixins.CreateModelMixin,  # POST
    mixins.RetrieveModelMixin,  # GET /envios/{id}/
    mixins.ListModelMixin,  # GET /envios/
    viewsets.GenericViewSet,
):
    """
    ViewSet per gestionar enviaments de notes de venda

    Permisos per rol:
    - DARP: Crear (POST) i consultar els seus enviaments (GET)
    - Investigadors: Només consultar TOTS els enviaments (GET) - lectura
    - Admin: Control total (GET, POST, PUT, DELETE)

    Endpoints:
    - POST   /api/sales-notes/envios/          - Crear enviament (DARP)
    - GET    /api/sales-notes/envios/          - Llistar enviaments (paginat)
    - GET    /api/sales-notes/envios/{id}/     - Detall enviament
    - GET    /api/sales-notes/envios/{id}/status/ - Estat processament
    """

    queryset = Envio.objects.all().select_related("usuario_envio")
    serializer_class = EnvioStagingSerializer
    permission_classes = [IsAuthenticated, DARPCanCreateInvestigadorCanRead]

    # Filtres, cerca i ordenació
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["procesado_en_db", "usuario_envio"]
    search_fields = ["num_envio"]
    ordering_fields = ["fecha_recepcion", "num_envio"]
    ordering = ["-fecha_recepcion"]  # Per defecte: més recents primer

    pagination_class = None

    def get_queryset(self):
        """
        Filtrar queryset segons el tipus d'usuari

        - DARP: Només veu els seus propis enviaments
        - Investigadors: Veuen TOTS els enviaments
        - Admin: Veu TOTS els enviaments
        """
        user = self.request.user

        # Admin veu tot
        if user.is_staff or user.is_superuser:
            return self.queryset

        # Investigadors veuen tot (només lectura)
        if user.groups.filter(name="Investigadors").exists():
            return self.queryset

        # Els usuaris amb permís per afegir només veuen els seus enviaments
        if user.has_perm("sales_notes.add_envio"):
            return self.queryset.filter(usuario_envio=user)

        # Per defecte, no veure res
        return Envio.objects.none()

    @method_decorator(ratelimit(key="user", rate="100/h", method="POST"), name="dispatch")
    def create(self, request, *args, **kwargs):
        """
        Crear nou enviament amb rate limiting
        """
        logger.info(f"User {request.user} creating envio from IP {request.META.get('REMOTE_ADDR')}")

        # Validar que només DARP o Admin puguin crear
        # La classe de permís ja gestiona això, però una doble comprovació no fa mal
        if not request.user.has_perm("sales_notes.add_envio"):
            return Response({"detail": "No tens permís per crear enviaments."}, status=status.HTTP_403_FORBIDDEN)

        # Utilitzem una transacció atòmica per assegurar "Tot o Res"
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                envio = serializer.save(usuario_envio=request.user)

                # Guardem el JSON cru complet associat a l'enviament per traçabilitat
                # Això assegura que tenim el JSON original encara que no tingui vendes individuals
                RawSalesNote.objects.create(envio=envio, raw_data=request.data)

                # --- NOU: Guardar còpia JSON en disc ---
                try:
                    backup_dir = "/app/data_backups/envios_json"
                    os.makedirs(backup_dir, exist_ok=True)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"envio_{envio.num_envio}_{timestamp}.json"
                    filepath = os.path.join(backup_dir, filename)

                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(request.data, f, ensure_ascii=False, indent=4)

                    logger.info(f"Backup JSON d'enviament guardat a: {filepath}")
                except Exception as e:
                    # No volem que falli la petició si falla el backup en disc, només loguejar-ho
                    logger.error(f"❌ Error guardant backup JSON en disc: {e}")

                logger.info(f"Envio {envio.num_envio} created successfully by {request.user}")
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            logger.error(f"Error creant enviament: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        Llistar enviaments (paginat)

        DARP: Només veu els seus enviaments
        Investigadors: Veuen TOTS els enviaments
        Admin: Veu tot

        Filtres disponibles:
        - ?tipo_respuesta=1
        - ?procesado=true
        - ?search=ENV2025
        - ?ordering=-fecha_recepcion
        """
        logger.info(f"User {request.user} listing envios")

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Obtenir detall d'un enviament específic

        DARP: Només els seus enviaments
        Investigadors: Qualsevol enviament
        Admin: Qualsevol enviament
        """
        instance = self.get_object()

        logger.info(f"User {request.user} retrieving envio {instance.num_envio}")

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="status")
    def status(self, request, pk=None):
        """
        Consultar l'estat de processament d'un enviament específic

        URL: /api/sales-notes/envios/{id}/status/

        Retorna:
        - procesado: bool
        - errores_validacion: JSON amb errors si n'hi ha
        - fecha_recepcion: timestamp
        """
        envio = self.get_object()

        logger.info(f"User {request.user} checking status of envio {envio.num_envio}")

        serializer = self.get_serializer(envio)
        return Response(serializer.data)
        return Response(serializer.data)
