"""
URLs principals del projecte VCPE API
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from . import views

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Health check
    path("health/", views.health_check, name="health-check"),
    # Root
    path("", views.root_view, name="root"),
    # API endpoints
    path("api/auth/", include("authentication.urls", namespace="authentication")),
    path("api/sales-notes/", include("sales_notes.urls")),
    # Documentació API (OpenAPI/Swagger)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Personalitzar admin
admin.site.site_header = "VCPE API - Administració"
admin.site.site_title = "VCPE API Admin"
admin.site.index_title = "Gestió del Sistema"
