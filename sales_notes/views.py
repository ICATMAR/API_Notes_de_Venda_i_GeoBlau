from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .models import Envio
from .serializers import EnvioSerializer, EnvioListSerializer, EnvioStatusSerializer
import logging

logger = logging.getLogger(__name__)


class EnvioViewSet(mixins.CreateModelMixin,  # Només CREATE (POST)
                    viewsets.GenericViewSet):  # Base sense operacions
    """
    ViewSet per gestionar enviaments de notes de venda
    
    NOMÉS permet crear nous enviaments (POST)
    No permet llistar, actualitzar ni esborrar
    """
    queryset = Envio.objects.all()
    serializer_class = EnvioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Retorna el serialitzador adequat segons l'acció"""
        if self.action == 'status':
            return EnvioStatusSerializer
        return EnvioSerializer
    
    @method_decorator(ratelimit(key='user', rate='100/h', method='POST'))
    def create(self, request, *args, **kwargs):
        """
        Crear nou enviament amb rate limiting
        
        Rate limit: 100 peticions per hora per usuari
        """
        # Logging d'auditoria
        logger.info(
            f"User {request.user} creating envio from IP {request.META.get('REMOTE_ADDR')}"
        )
        
        # Afegir usuari i IP automàticament
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Guardar amb informació d'auditoria
        envio = serializer.save(
            usuario_envio=request.user,
            ip_origen=request.META.get('REMOTE_ADDR')
        )
        
        logger.info(f"Envio {envio.num_envio} created successfully")
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=True, methods=['get'], url_path='status')
    def status(self, request, pk=None):
        """
        Consultar l'estat d'un enviament específic
        URL: /api/sales-notes/envios/{id}/status/
        """
        envio = self.get_object()
        serializer = self.get_serializer(envio)
        return Response(serializer.data)