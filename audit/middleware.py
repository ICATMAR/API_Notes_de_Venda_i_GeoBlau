"""
Middleware per auditoria automàtica de peticions
"""

import hashlib
import logging
import time

from django.http.request import RawPostDataException
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from audit.models import SecurityEvent
from authentication.models import APIAccessLog

logger = logging.getLogger("audit")


class AuditMiddleware(MiddlewareMixin):
    """
    Middleware que registra totes les peticions a l'API per auditoria
    """

    def process_request(self, request):
        """Capturar temps d'inici de la petició"""
        request._start_time = time.time()
        return None

    def process_response(self, request, response):
        """Registrar la petició completada"""

        # Calcular temps de resposta
        if hasattr(request, "_start_time"):
            response_time = int((time.time() - request._start_time) * 1000)
        else:
            response_time = 0

        # Obtenir informació de la petició
        user = request.user if request.user.is_authenticated else None
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
        request_id = request.META.get("HTTP_X_REQUEST_ID", "")

        # Hash del body per privacitat (no guardem dades sensibles)
        request_body_hash = ""

        # Només calcular hash per mètodes que poden tenir body
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            try:
                body = request.body
                request_body_hash = hashlib.sha256(body).hexdigest()
            except RawPostDataException:
                request_body_hash = hashlib.sha256(b"").hexdigest()
        else:
            request_body_hash = hashlib.sha256(b"").hexdigest()

        # Només registrar si és una petició a l'API
        if request.path.startswith("/api/"):
            try:
                # Crear log d'accés
                APIAccessLog.objects.create(
                    user=user,
                    path=request.path,
                    method=request.method,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    request_id=request_id,
                    status_code=response.status_code,
                    response_time_ms=response_time,
                    request_body_hash=request_body_hash,
                    error_message=self.get_error_message(response),
                )

                # Detectar possibles problemes de seguretat
                self.detect_security_issues(request, response, user, ip_address)

            except Exception as e:
                logger.error(f"Error registrant log d'accés: {str(e)}", exc_info=True)

        return response

    def process_exception(self, request, exception):
        """Registrar excepcions"""
        user = request.user if request.user.is_authenticated else None
        ip_address = self.get_client_ip(request)

        try:
            APIAccessLog.objects.create(
                user=user,
                path=request.path,
                method=request.method,
                ip_address=ip_address,
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
                request_id=request.META.get("HTTP_X_REQUEST_ID", ""),
                status_code=500,
                response_time_ms=0,
                error_message=str(exception)[:1000],
            )
        except Exception as e:
            logger.error(f"Error registrant excepció: {str(e)}", exc_info=True)

        return None

    def get_client_ip(self, request):
        """Obtenir la IP real del client (considerant proxies)"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def get_error_message(self, response):
        """Extreure missatge d'error de la resposta"""
        if response.status_code >= 400:
            try:
                if hasattr(response, "data"):
                    return str(response.data)[:1000]
            except (AttributeError, TypeError, ValueError) as e:
                logger.debug(f"No s'ha pogut extreure missatge d'error: {e}")
        return ""

    def detect_security_issues(self, request, response, user, ip_address):
        """
        Detectar possibles problemes de seguretat basats en patrons
        """
        # Intent d'accés no autoritzat
        if response.status_code == 401 or response.status_code == 403:
            self.log_security_event(
                event_type="UNAUTHORIZED_ACCESS",
                description=f"Intent d'accés no autoritzat a {request.path}",
                request=request,
                user=user,
                ip_address=ip_address,
                severity="MEDIUM",
            )

        # Petició mal formada (possible intent d'atac)
        if response.status_code == 400:
            if self.looks_suspicious(request):
                self.log_security_event(
                    event_type="MALFORMED_REQUEST",
                    description=f"Petició mal formada sospitosa a {request.path}",
                    request=request,
                    user=user,
                    ip_address=ip_address,
                    severity="LOW",
                )

        # Massa peticions des de la mateixa IP
        if self.check_rate_limit_exceeded(ip_address):
            self.log_security_event(
                event_type="RATE_LIMIT_EXCEEDED",
                description=f"Límit de peticions excedit des de {ip_address}",
                request=request,
                user=user,
                ip_address=ip_address,
                severity="MEDIUM",
                blocked=True,
            )

    def looks_suspicious(self, request):
        """
        Detectar patrons sospitosos en la petició
        """
        suspicious_patterns = [
            "script",
            "<script>",
            "javascript:",
            "SELECT",
            "UNION",
            "DROP",
            "INSERT",
            "../",
            "..\\",
            "eval(",
            "exec(",
        ]

        # Comprovar URL
        path = request.path.lower()
        for pattern in suspicious_patterns:
            if pattern.lower() in path:
                return True

        # Comprovar query params
        query = request.GET.urlencode().lower()
        for pattern in suspicious_patterns:
            if pattern.lower() in query:
                return True

        return False

    def check_rate_limit_exceeded(self, ip_address):
        """
        Comprovar si una IP ha excedit els límits de peticions
        """
        from datetime import timedelta

        # Últimes 5 minuts
        time_threshold = timezone.now() - timedelta(minutes=5)
        recent_requests = APIAccessLog.objects.filter(ip_address=ip_address, timestamp__gte=time_threshold).count()

        # Màxim 100 peticions en 5 minuts per IP
        return recent_requests > 100

    def log_security_event(self, event_type, description, request, user, ip_address, severity="MEDIUM", blocked=False):
        """
        Registrar un event de seguretat
        """
        try:
            SecurityEvent.objects.create(
                event_type=event_type,
                user=user,
                ip_address=ip_address,
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
                description=description,
                request_path=request.path,
                request_method=request.method,
                request_data_hash=hashlib.sha256(str(request.body).encode()).hexdigest() if request.body else "",
                severity=severity,
                blocked=blocked,
                action_taken="Blocked" if blocked else "Logged",
            )

            logger.warning(f"Event de seguretat: {event_type} - {description} " f"(IP: {ip_address}, User: {user})")

        except Exception as e:
            logger.error(f"Error registrant event de seguretat: {str(e)}", exc_info=True)
