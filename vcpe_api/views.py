"""
Views generals de l'API
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def health_check(request):
    """Endpoint de salut per healthchecks"""
    return JsonResponse({"status": "healthy", "service": "vcpe-api"})


@require_http_methods(["GET"])
def root_view(request):
    """Vista arrel amb informació de l'API"""
    return JsonResponse(
        {
            "service": "VCPE API - Notes de Venda",
            "version": "1.0.0",
            "institution": "ICATMAR",
            "documentation": "/api/docs/",
            "endpoints": {
                "auth": "/api/auth/",
                "sales_notes": "/api/sales-notes/",
                "admin": "/admin/",
            },
        }
    )
