import logging

from django.conf import settings
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)


class IPRestrictionMiddleware:
    """
    Middleware per restringir l'accés a l'API només a IPs autoritzades en producció.
    Llegeix la llista d'IPs permeses de settings.ALLOWED_API_IPS.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Només apliquem restricció si estem en producció (DEBUG=False) i és una ruta d'API
        if not settings.DEBUG and request.path.startswith("/api/"):
            # Obtenir llista d'IPs permeses (per defecte buida si no està definida)
            allowed_ips = getattr(settings, "ALLOWED_API_IPS", [])

            client_ip = self.get_client_ip(request)

            if client_ip not in allowed_ips:
                logger.warning(f"Accés denegat IP: {client_ip} a {request.path}")
                return HttpResponseForbidden("Access denied: IP not allowed")

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
