from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import Envio
from .serializers import EnvioSerializer, EnvioListSerializer, EnvioStatusSerializer
from .permissions import DARPCanCreateInvestigadorCanRead
import logging

logger = logging.getLogger(__name__)


class EnvioViewSet(mixins.CreateModelMixin,     # POST
                   mixins.RetrieveModelMixin,   # GET /envios/{id}/
                   mixins.ListModelMixin,       # GET /envios/
                   viewsets.GenericViewSet):
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
    
    queryset = Envio.objects.all().select_related('usuario_envio').prefetch_related(
        'establecimientos',
        'establecimientos__unidades_productivas',
        'establecimientos__unidades_productivas__especies'
    )
    serializer_class = EnvioSerializer
    permission_classes = [IsAuthenticated, DARPCanCreateInvestigadorCanRead]
    
    # Filtres, cerca i ordenació
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo_respuesta', 'procesado', 'usuario_envio']
    search_fields = ['num_envio']
    ordering_fields = ['fecha_recepcion', 'num_envio', 'tipo_respuesta']
    ordering = ['-fecha_recepcion']  # Per defecte: més recents primer
    
    # Paginació
    pagination_class = None  # Usar la default del settings o definir-ne una
    
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
        if user.groups.filter(name='Investigadors').exists():
            return self.queryset
        
        # DARP només veu els seus enviaments
        if hasattr(user, 'organization') and 'DARP' in user.organization.upper():
            return self.queryset.filter(usuario_envio=user)
        
        # Per defecte, no veure res
        return Envio.objects.none()
    
    def get_serializer_class(self):
        """Retorna el serialitzador adequat segons l'acció"""
        if self.action == 'list':
            return EnvioListSerializer  # Versió resumida per llistat
        elif self.action == 'status':
            return EnvioStatusSerializer
        return EnvioSerializer
    
    @method_decorator(ratelimit(key='user', rate='100/h', method='POST'), name='dispatch')
    def create(self, request, *args, **kwargs):
        """
        Crear nou enviament amb rate limiting
        """
        logger.info(
            f"User {request.user} creating envio from IP {request.META.get('REMOTE_ADDR')}"
        )
        
        # Validar que només DARP o Admin puguin crear
        if not (request.user.is_staff or request.user.is_superuser):
            if not (hasattr(request.user, 'organization') and 'DARP' in request.user.organization.upper()):
                return Response(
                    {"detail": "Només els usuaris DARP poden crear enviaments."},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        # PRIMER: Convertir de PascalCase a snake_case
        input_serializer = EnvioInputSerializer()
        converted_data = input_serializer.to_internal_value(request.data)
        
        # SEGON: Validar amb el serializer principal
        serializer = EnvioSerializer(data=converted_data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Guardar
        envio = serializer.save()
        
        logger.info(f"Envio {envio.num_envio} created successfully by {request.user}")
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
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
        
        logger.info(
            f"User {request.user} retrieving envio {instance.num_envio}"
        )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='status')
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
        
        logger.info(
            f"User {request.user} checking status of envio {envio.num_envio}"
        )
        
        serializer = self.get_serializer(envio)
        return Response(serializer.data)