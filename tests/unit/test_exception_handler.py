"""
Tests per al custom exception handler
"""
import logging
from unittest.mock import Mock, patch

import pytest
from django.test import RequestFactory
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotFound,
    PermissionDenied,
    ValidationError,
)

from sales_notes.exception_handler import custom_exception_handler


@pytest.fixture
def request_factory():
    """Fixture que retorna una RequestFactory"""
    return RequestFactory()


@pytest.fixture
def mock_request(request_factory):
    """Fixture que crea un mock request amb atributs bàsics"""
    request = request_factory.get("/api/test/")
    request.user = Mock()
    request.user.is_authenticated = True
    request.user.username = "test_user"
    return request


class TestCustomExceptionHandler:
    """Tests per al custom exception handler"""

    def test_exception_handler_with_none_response(self, mock_request):
        """Test que verifica que retorna None quan el handler de DRF retorna None"""
        # Simular una excepció que no genera resposta de DRF
        exc = Exception("Test error")
        context = {"request": mock_request}

        with patch("sales_notes.exception_handler.exception_handler", return_value=None):
            response = custom_exception_handler(exc, context)

        assert response is None

    def test_exception_handler_with_400_error(self, mock_request):
        """Test per errors 4xx (client error)"""
        exc = ValidationError("Invalid data")
        context = {"request": mock_request}

        with patch("sales_notes.exception_handler.exception_handler") as mock_handler:
            mock_response = Mock()
            mock_response.status_code = status.HTTP_400_BAD_REQUEST
            mock_response.data = {"detail": "Invalid data"}
            mock_handler.return_value = mock_response

            with patch("sales_notes.exception_handler.logger") as mock_logger:
                response = custom_exception_handler(exc, context)

                # Verificar que es crida warning per errors 4xx
                mock_logger.warning.assert_called_once()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "error"
        assert response.data["status_code"] == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Invalid data"
        assert response.data["path"] == "/api/test/"
        assert "timestamp" in response.data

    def test_exception_handler_with_401_error(self, mock_request):
        """Test per errors d'autenticació (401)"""
        exc = AuthenticationFailed("Invalid token")
        context = {"request": mock_request}

        with patch("sales_notes.exception_handler.exception_handler") as mock_handler:
            mock_response = Mock()
            mock_response.status_code = status.HTTP_401_UNAUTHORIZED
            mock_response.data = {"detail": "Invalid token"}
            mock_handler.return_value = mock_response

            with patch("sales_notes.exception_handler.logger") as mock_logger:
                response = custom_exception_handler(exc, context)

                # Verificar que es crida warning per errors 4xx
                mock_logger.warning.assert_called_once()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["status"] == "error"
        assert response.data["message"] == "Invalid token"

    def test_exception_handler_with_403_error(self, mock_request):
        """Test per errors de permisos (403)"""
        exc = PermissionDenied("Access denied")
        context = {"request": mock_request}

        with patch("sales_notes.exception_handler.exception_handler") as mock_handler:
            mock_response = Mock()
            mock_response.status_code = status.HTTP_403_FORBIDDEN
            mock_response.data = {"detail": "Access denied"}
            mock_handler.return_value = mock_response

            with patch("sales_notes.exception_handler.logger") as mock_logger:
                response = custom_exception_handler(exc, context)

                # Verificar que es crida warning per errors 4xx
                mock_logger.warning.assert_called_once()

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["message"] == "Access denied"

    def test_exception_handler_with_404_error(self, mock_request):
        """Test per errors de not found (404)"""
        exc = NotFound("Resource not found")
        context = {"request": mock_request}

        with patch("sales_notes.exception_handler.exception_handler") as mock_handler:
            mock_response = Mock()
            mock_response.status_code = status.HTTP_404_NOT_FOUND
            mock_response.data = {"detail": "Resource not found"}
            mock_handler.return_value = mock_response

            with patch("sales_notes.exception_handler.logger"):
                response = custom_exception_handler(exc, context)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["message"] == "Resource not found"

    def test_exception_handler_with_500_error(self, mock_request):
        """Test per errors 5xx (server error)"""
        exc = APIException("Internal server error")
        exc.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        context = {"request": mock_request}
        context["request"].DEBUG = False

        with patch("sales_notes.exception_handler.exception_handler") as mock_handler:
            mock_response = Mock()
            mock_response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            mock_response.data = {"detail": "Internal server error"}
            mock_handler.return_value = mock_response

            with patch("sales_notes.exception_handler.logger") as mock_logger:
                response = custom_exception_handler(exc, context)

                # Verificar que es crida error per errors 5xx
                mock_logger.error.assert_called_once()

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data["status"] == "error"
        # En producció (DEBUG=False), s'oculta el missatge real
        assert response.data["message"] == "Internal server error. Please contact support."

    def test_exception_handler_with_500_error_debug_mode(self, mock_request):
        """Test per errors 5xx en mode debug (mostra detalls)"""
        exc = APIException("Internal server error details")
        exc.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        context = {"request": mock_request}
        context["request"].DEBUG = True

        with patch("sales_notes.exception_handler.exception_handler") as mock_handler:
            mock_response = Mock()
            mock_response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            mock_response.data = {"detail": "Internal server error details"}
            mock_handler.return_value = mock_response

            with patch("sales_notes.exception_handler.logger"):
                response = custom_exception_handler(exc, context)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        # En debug mode, mostra el missatge real
        assert response.data["message"] == "Internal server error details"

    def test_exception_handler_with_request_id(self, mock_request):
        """Test que verifica que s'afegeix request_id si està disponible"""
        mock_request.id = "test-request-id-123"
        exc = ValidationError("Invalid data")
        context = {"request": mock_request}

        with patch("sales_notes.exception_handler.exception_handler") as mock_handler:
            mock_response = Mock()
            mock_response.status_code = status.HTTP_400_BAD_REQUEST
            mock_response.data = {"detail": "Invalid data"}
            mock_handler.return_value = mock_response

            with patch("sales_notes.exception_handler.logger"):
                response = custom_exception_handler(exc, context)

        assert "request_id" in response.data
        assert response.data["request_id"] == "test-request-id-123"

    def test_exception_handler_without_request_id(self, mock_request):
        """Test que verifica que no hi ha error si no hi ha request_id"""
        # El mock_request no té atribut 'id'
        exc = ValidationError("Invalid data")
        context = {"request": mock_request}

        with patch("sales_notes.exception_handler.exception_handler") as mock_handler:
            mock_response = Mock()
            mock_response.status_code = status.HTTP_400_BAD_REQUEST
            mock_response.data = {"detail": "Invalid data"}
            mock_handler.return_value = mock_response

            with patch("sales_notes.exception_handler.logger"):
                response = custom_exception_handler(exc, context)

        assert "request_id" not in response.data

    def test_exception_handler_without_request(self):
        """Test per quan no hi ha request disponible al context"""
        exc = ValidationError("Invalid data")
        context = {}  # No request

        with patch("sales_notes.exception_handler.exception_handler") as mock_handler:
            mock_response = Mock()
            mock_response.status_code = status.HTTP_400_BAD_REQUEST
            mock_response.data = {"detail": "Invalid data"}
            mock_handler.return_value = mock_response

            with patch("sales_notes.exception_handler.logger"):
                response = custom_exception_handler(exc, context)

        assert response.data["path"] is None

    def test_exception_handler_with_unauthenticated_user(self, mock_request):
        """Test per errors amb usuari no autenticat"""
        mock_request.user.is_authenticated = False
        exc = APIException("Server error")
        exc.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        context = {"request": mock_request}
        context["request"].DEBUG = False

        with patch("sales_notes.exception_handler.exception_handler") as mock_handler:
            mock_response = Mock()
            mock_response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            mock_response.data = {"detail": "Server error"}
            mock_handler.return_value = mock_response

            with patch("sales_notes.exception_handler.logger") as mock_logger:
                response = custom_exception_handler(exc, context)

                # Verificar que en el log es marca com Anonymous
                call_args = mock_logger.error.call_args
                assert call_args[1]["extra"]["user"] == "Anonymous"

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_exception_handler_message_from_exception_string(self, mock_request):
        """Test que usa str(exc) quan no hi ha 'detail' en response.data"""
        exc = ValidationError("Custom error message")
        context = {"request": mock_request}

        with patch("sales_notes.exception_handler.exception_handler") as mock_handler:
            mock_response = Mock()
            mock_response.status_code = status.HTTP_400_BAD_REQUEST
            mock_response.data = {}  # No 'detail'
            mock_handler.return_value = mock_response

            with patch("sales_notes.exception_handler.logger"):
                response = custom_exception_handler(exc, context)

        # Ha d'usar str(exc) com a fallback
        assert "Custom error message" in str(response.data["message"])
