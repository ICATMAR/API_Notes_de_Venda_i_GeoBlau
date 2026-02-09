"""
Tests bàsics per al custom exception handler
"""

import pytest
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound, ValidationError
from rest_framework.test import APIRequestFactory

from sales_notes.exception_handler import custom_exception_handler


@pytest.fixture
def rf():
    return APIRequestFactory()


class TestCustomExceptionHandler:
    """Tests per al custom exception handler"""

    def test_exception_handler_with_none_response(self, rf):
        """Test que retorna None per excepcions no DRF"""
        request = rf.get("/test/")
        request.user = AnonymousUser()
        exc = Exception("Generic error")
        context = {"request": request}

        response = custom_exception_handler(exc, context)

        assert response is None

    def test_exception_handler_with_validation_error(self, rf):
        """Test per ValidationError amb dict"""
        request = rf.get("/test/")
        request.user = AnonymousUser()
        # Passar un dict per obtenir un dict en response.data amb 'detail'
        exc = ValidationError(detail={"detail": "Invalid data"})
        context = {"request": request}

        response = custom_exception_handler(exc, context)

        assert response is not None
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["status"] == "error"
        assert "timestamp" in response.data
        assert "path" in response.data

    def test_exception_handler_with_not_found(self, rf):
        """Test per NotFound error"""
        request = rf.get("/test/")
        request.user = AnonymousUser()
        exc = NotFound("Resource not found")
        context = {"request": request}

        response = custom_exception_handler(exc, context)

        assert response is not None
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["status"] == "error"
        assert "timestamp" in response.data

    def test_exception_handler_with_server_error(self, rf, test_user):
        """Test per error 500 amb usuari autenticat"""
        request = rf.get("/test/")
        request.user = test_user
        request.DEBUG = False
        exc = APIException("Server error")
        exc.status_code = 500
        context = {"request": request}

        response = custom_exception_handler(exc, context)

        assert response is not None
        assert response.status_code == 500
        assert response.data["status"] == "error"
        # En producció oculta els detalls
        assert response.data["message"] == "Internal server error. Please contact support."

    def test_exception_handler_with_request_id(self, rf):
        """Test que afegeix request_id si està disponible"""
        request = rf.get("/test/")
        request.user = AnonymousUser()
        request.id = "test-request-123"
        exc = NotFound("Not found")
        context = {"request": request}

        response = custom_exception_handler(exc, context)

        assert response is not None
        assert "request_id" in response.data
        assert response.data["request_id"] == "test-request-123"

    def test_exception_handler_without_request(self):
        """Test sense request al context"""
        exc = NotFound("Not found")
        context = {}

        response = custom_exception_handler(exc, context)

        assert response is not None
        assert response.data["path"] is None
