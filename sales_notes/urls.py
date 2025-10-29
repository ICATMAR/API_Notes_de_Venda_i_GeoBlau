"""
URLs de l'app sales_notes

Endpoints disponibles:
- POST /envios/           → Crear nou enviament
- GET  /envios/{id}/status/ → Consultar estat d'enviament
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'sales_notes'

# Router buit de moment (després afegirem ViewSets)
router = DefaultRouter()

# Registrar ViewSet (només permet POST gràcies als mixins)
router.register(r'envios', views.EnvioViewSet, basename='envio')

# URLs buides temporalment fins que creem les views
urlpatterns = [
     path('', include(router.urls)),
]