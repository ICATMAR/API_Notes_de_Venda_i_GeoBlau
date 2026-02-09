import pytest
from django.contrib.auth.models import Group
from rest_framework.test import APIRequestFactory

from sales_notes.models import Envio
from sales_notes.permissions import DARPCanCreateInvestigadorCanRead, IsDARP, IsInvestigador


@pytest.mark.django_db
class TestIsDARP:
    """Tests per permís IsDARP"""

    def setup_method(self):
        self.factory = APIRequestFactory()
        self.permission = IsDARP()

    def test_darp_user_has_permission(self, darp_user):
        """Usuari DARP té permís"""
        request = self.factory.get("/api/sales-notes/")
        request.user = darp_user

        assert self.permission.has_permission(request, None)

    def test_investigador_no_permission(self, investigador_user):
        """Investigador NO té permís DARP"""
        request = self.factory.get("/api/sales-notes/")
        request.user = investigador_user

        assert not self.permission.has_permission(request, None)

    def test_unauthenticated_no_permission(self):
        """Usuari no autenticat no té permís"""
        from django.contrib.auth.models import AnonymousUser

        request = self.factory.get("/api/sales-notes/")
        request.user = AnonymousUser()

        assert not self.permission.has_permission(request, None)


@pytest.mark.django_db
class TestIsInvestigador:
    """Tests per permís IsInvestigador"""

    def setup_method(self):
        self.factory = APIRequestFactory()
        self.permission = IsInvestigador()

    def test_investigador_has_permission(self, investigador_user):
        """Investigador té permís"""
        request = self.factory.get("/api/sales-notes/")
        request.user = investigador_user

        assert self.permission.has_permission(request, None)

    def test_darp_no_investigador_permission(self, darp_user):
        """DARP NO té permís d'investigador"""
        request = self.factory.get("/api/sales-notes/")
        request.user = darp_user

        assert not self.permission.has_permission(request, None)


@pytest.mark.django_db
class TestDARPCanCreateInvestigadorCanRead:
    """Tests per permís combinat principal"""

    def setup_method(self):
        self.factory = APIRequestFactory()
        self.permission = DARPCanCreateInvestigadorCanRead()

    def test_admin_full_access(self, admin_user):
        """Admin té accés complet"""
        request = self.factory.post("/api/sales-notes/")
        request.user = admin_user

        assert self.permission.has_permission(request, None)

    def test_darp_can_post(self, darp_user):
        """DARP pot crear (POST)"""
        request = self.factory.post("/api/sales-notes/")
        request.user = darp_user

        assert self.permission.has_permission(request, None)

    def test_darp_can_get(self, darp_user):
        """DARP pot llegir (GET)"""
        request = self.factory.get("/api/sales-notes/")
        request.user = darp_user

        assert self.permission.has_permission(request, None)

    def test_investigador_can_get(self, investigador_user):
        """Investigador pot llegir (GET)"""
        request = self.factory.get("/api/sales-notes/")
        request.user = investigador_user

        assert self.permission.has_permission(request, None)

    def test_investigador_cannot_post(self, investigador_user):
        """Investigador NO pot crear (POST)"""
        request = self.factory.post("/api/sales-notes/")
        request.user = investigador_user

        assert not self.permission.has_permission(request, None)

    def test_investigador_cannot_put(self, investigador_user):
        """Investigador NO pot modificar (PUT)"""
        request = self.factory.put("/api/sales-notes/123/")
        request.user = investigador_user

        assert not self.permission.has_permission(request, None)

    def test_darp_can_access_own_envio(self, darp_user):
        """DARP pot accedir als seus enviaments"""
        envio = Envio.objects.create(num_envio="ENV001", tipo_respuesta=1, usuario_envio=darp_user)

        request = self.factory.get(f"/api/sales-notes/{envio.id}/")
        request.user = darp_user

        assert self.permission.has_object_permission(request, None, envio)

    def test_darp_cannot_access_other_envio(self, darp_user, test_user):
        """DARP NO pot accedir a enviaments d'altres"""
        envio = Envio.objects.create(num_envio="ENV002", tipo_respuesta=1, usuario_envio=test_user)

        request = self.factory.get(f"/api/sales-notes/{envio.id}/")
        request.user = darp_user

        assert not self.permission.has_object_permission(request, None, envio)

    def test_investigador_can_read_any_envio(self, investigador_user, darp_user):
        """Investigador pot llegir qualsevol enviament"""
        envio = Envio.objects.create(num_envio="ENV003", tipo_respuesta=1, usuario_envio=darp_user)

        request = self.factory.get(f"/api/sales-notes/{envio.id}/")
        request.user = investigador_user

        assert self.permission.has_object_permission(request, None, envio)

    def test_investigador_cannot_modify_any_envio(self, investigador_user, darp_user):
        """Investigador NO pot modificar cap enviament"""
        envio = Envio.objects.create(num_envio="ENV004", tipo_respuesta=1, usuario_envio=darp_user)

        request = self.factory.put(f"/api/sales-notes/{envio.id}/")
        request.user = investigador_user

        assert not self.permission.has_object_permission(request, None, envio)
