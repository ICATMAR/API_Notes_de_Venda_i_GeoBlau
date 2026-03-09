import logging

from django.conf import settings
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)


class IPWhitelistMiddleware:
    """
    Middleware unificat per restringir l'accés.
    Combina IPs fixes i configuració de settings.ALLOWED_API_IPS.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Llista d'IPs permeses (White List)
        self.allowed_ips = [
            "127.0.0.1",  # Localhost
            "::1",  # Localhost IPv6
            "77.227.4.18",  # IP Externa sol·licitada
            "172.26.86.205",  # La teva IP local (wlp0s20f3)
            "172.28.136.24",  # La teva IP de VPN/PPP (per si de cas)
        ]

        # Afegim les IPs definides a les variables d'entorn (settings.py)
        settings_ips = getattr(settings, "ALLOWED_API_IPS", [])
        if settings_ips:
            self.allowed_ips.extend(settings_ips)

        # Eliminar duplicats
        self.allowed_ips = list(set(self.allowed_ips))

    def __call__(self, request):
        # Obtenir la IP del client
        ip = self.get_client_ip(request)

        # Si la IP no està a la llista, retornem 403 Forbidden
        if ip not in self.allowed_ips:
            logger.warning(f"⛔ Accés denegat per IP no autoritzada: {ip} a {request.path}")
            return HttpResponseForbidden(f"Access Denied for IP: {ip}")

        return self.get_response(request)

    def get_client_ip(self, request):
        # Gestió de proxies (Nginx/Gunicorn)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
