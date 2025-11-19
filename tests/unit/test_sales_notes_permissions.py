"""
Tests per les classes de permisos de sales_notes
"""
import pytest
from django.test import RequestFactory
from rest_framework.test import APIRequestFactory
from sales_notes.permissions import IsDARP, IsInvestigador, DARPCanCreateInvestigadorCanRead
from sales_notes.models import Envio


@pytest.mark.django_db
class TestIsDARPPermission:
    """Tests per IsDARP permission"""

    def setup_method(self):
        self.factory = APIRequestFactory()
        self.permission = IsDARP()

    def test_darp_user_has_permission(self, darp_user):
        """DARP user té permís"""
        request = self.factory.get('/api/sales-notes/')
        request.user = darp_user

        assert self.permission.has_permission(request, None)

    def test_investigador_no_permission(self, investigador_user):
        """Investigador no té permís IsDARP"""
        request = self.factory.get('/api/sales-notes/')
        request.user = investigador_user

        assert not self.permission.has_permission(request, None)

    def test_unauthenticated_no_permission(self):
        """Usuari no autenticat no té permís"""
        from django.contrib.auth.models import AnonymousUser

        request = self.factory.get('/api/sales-notes/')
        request.user = AnonymousUser()

        assert not self.permission.has_permission(request, None)


@pytest.mark.django_db
class TestIsInvestigadorPermission:
    """Tests per IsInvestigador permission"""

    def setup_method(self):
        self.factory = APIRequestFactory()
        self.permission = IsInvestigador()

    def test_investigador_has_permission(self, investigador_user):
        """Investigador té permís"""
        request = self.factory.get('/api/sales-notes/')
        request.user = investigador_user

        assert self.permission.has_permission(request, None)

    def test_darp_no_permission(self, darp_user):
        """DARP no té permís IsInvestigador"""
        request = self.factory.get('/api/sales-notes/')
        request.user = darp_user

        assert not self.permission.has_permission(request, None)


@pytest.mark.django_db
class TestDARPCanCreateInvestigadorCanReadPermission:
    """Tests per DARPCanCreateInvestigadorCanRead permission"""

    def setup_method(self):
        self.factory = APIRequestFactory()
        self.permission = DARPCanCreateInvestigadorCanRead()

    def test_darp_can_create(self, darp_user):
        """DARP pot crear (POST)"""
        request = self.factory.post('/api/sales-notes/')
        request.user = darp_user

        assert self.permission.has_permission(request, None)

    def test_darp_can_read(self, darp_user):
        """DARP pot llegir (GET)"""
        request = self.factory.get('/api/sales-notes/')
        request.user = darp_user

        assert self.permission.has_permission(request, None)

    def test_investigador_can_read(self, investigador_user):
        """Investigador pot llegir (GET)"""
        request = self.factory.get('/api/sales-notes/')
        request.user = investigador_user

        assert self.permission.has_permission(request, None)

    def test_investigador_cannot_create(self, investigador_user):
        """Investigador NO pot crear (POST)"""
        request = self.factory.post('/api/sales-notes/')
        request.user = investigador_user

        assert not self.permission.has_permission(request, None)

    def test_investigador_cannot_update(self, investigador_user):
        """Investigador NO pot actualitzar (PUT)"""
        request = self.factory.put('/api/sales-notes/1/')
        request.user = investigador_user

        assert not self.permission.has_permission(request, None)

    def test_investigador_cannot_delete(self, investigador_user):
        """Investigador NO pot esborrar (DELETE)"""
        request = self.factory.delete('/api/sales-notes/1/')
        request.user = investigador_user

        assert not self.permission.has_permission(request, None)

    def test_darp_can_access_own_envio(self, darp_user):
        """DARP pot accedir als seus enviaments"""
        envio = Envio.objects.create(
            num_envio='ENV001',
            tipo_respuesta=1,
            usuario_envio=darp_user
        )

        request = self.factory.get(f'/api/sales-notes/{envio.id}/')
        request.user = darp_user

        assert self.permission.has_object_permission(request, None, envio)

    def test_investigador_can_read_any_envio(self, investigador_user, darp_user):
        """Investigador pot llegir qualsevol enviament"""
        envio = Envio.objects.create(
            num_envio='ENV002',
            tipo_respuesta=1,
            usuario_envio=darp_user
        )

        request = self.factory.get(f'/api/sales-notes/{envio.id}/')
        request.user = investigador_user

        assert self.permission.has_object_permission(request, None, envio)

    def test_investigador_cannot_modify_envio(self, investigador_user, darp_user):
        """Investigador NO pot modificar enviaments"""
        envio = Envio.objects.create(
            num_envio='ENV003',
            tipo_respuesta=1,
            usuario_envio=darp_user
        )

        request = self.factory.put(f'/api/sales-notes/{envio.id}/')
        request.user = investigador_user

        # has_permission ja retorna False per PUT
        assert not self.permission.has_permission(request, None)
