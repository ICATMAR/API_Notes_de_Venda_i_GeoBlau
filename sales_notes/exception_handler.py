import logging

from django.utils import timezone
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Handler personalitzat per gestionar excepcions de l'API

    - Estandarditza format de respostes d'error
    - Registra errors a logs d'auditoria
    - Oculta detalls sensibles en producció
    """
    # Cridar handler per defecte de DRF primer
    response = exception_handler(exc, context)

    if response is not None:
        # Obtenir informació del request
        request = context.get("request")

        # Estructura estandarditzada d'error
        custom_response = {
            "status": "error",
            "status_code": response.status_code,
            "message": response.data.get("detail", str(exc)),
            "timestamp": timezone.now().isoformat(),
            "path": request.path if request else None,
        }

        # Afegir request_id si està disponible (del middleware)
        if hasattr(request, "id"):
            custom_response["request_id"] = str(request.id)

        # Logging segons severitat
        if response.status_code >= 500:
            logger.error(
                f"Server error: {exc}",
                extra={
                    "status_code": response.status_code,
                    "path": request.path if request else None,
                    "user": request.user if request and request.user.is_authenticated else "Anonymous",
                },
            )
        elif response.status_code >= 400:
            logger.warning(
                f"Client error: {exc}",
                extra={
                    "status_code": response.status_code,
                    "path": request.path if request else None,
                },
            )

        # En producció, ocultar detalls interns dels errors 500
        if response.status_code >= 500 and not context.get("request").DEBUG:
            custom_response["message"] = "Internal server error. Please contact support."

        response.data = custom_response

    return response
