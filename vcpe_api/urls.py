# ============================================
# vcpe_api/urls.py - URLs principals
# ============================================
"""
URLs principals del projecte VCPE API
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def health_check(request):
    """Endpoint de salut per healthchecks"""
    return JsonResponse({"status": "healthy", "service": "vcpe-api"})


@require_http_methods(["GET"])
def root_view(request):
    """Vista arrel amb informació de l'API"""
    return JsonResponse({
        "service": "VCPE API - Notes de Venda",
        "version": "1.0.0",
        "institution": "ICATMAR",
        "documentation": "/api/docs/",
        "endpoints": {
            "auth": "/api/auth/",
            "sales_notes": "/api/sales-notes/",
            "admin": "/admin/",
        }
    })


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health check
    path('health/', health_check, name='health-check'),
    
    # Root
    path('', root_view, name='root'),
    
    # API endpoints
    path('api/auth/', include('authentication.urls')),
    path('api/sales-notes/', include('sales_notes.urls')),
    
    # Documentació API (OpenAPI/Swagger)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Personalitzar admin
admin.site.site_header = "VCPE API - Administració"
admin.site.site_title = "VCPE API Admin"
admin.site.index_title = "Gestió del Sistema"


# ============================================
# sales_notes/urls.py
# ============================================
"""
URLs de l'app sales_notes
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'sales_notes'

# Router per ViewSets
router = DefaultRouter()
router.register(r'envios', views.EnvioViewSet, basename='envio')

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoints addicionals si són necessaris
    path('estadistiques/', views.EstadistiquesView.as_view(), name='estadistiques'),
]


# ============================================
# authentication/urls.py
# ============================================
"""
URLs de l'app authentication
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import views

app_name = 'authentication'

urlpatterns = [
    # JWT Token endpoints
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User management
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]