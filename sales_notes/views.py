# sales_notes/views.py - Implementar ViewSets complets
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

class EnvioViewSet(viewsets.ModelViewSet):
    """ViewSet per gestionar enviaments de notes de venda"""
    queryset = Envio.objects.all()
    serializer_class = EnvioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EnvioListSerializer
        elif self.action == 'status':
            return EnvioStatusSerializer
        return EnvioSerializer
    
    @method_decorator(ratelimit(key='user', rate='100/h', method='POST'))
    def create(self, request, *args, **kwargs):
        """Crear nou enviament amb rate limiting"""
        # Logging d'auditoria
        logger.info(f"User {request.user} creating envio from IP {request.META.get('REMOTE_ADDR')}")
        return super().create(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """Consultar l'estat d'un enviament"""
        envio = self.get_object()
        serializer = self.get_serializer(envio)
        return Response(serializer.data)