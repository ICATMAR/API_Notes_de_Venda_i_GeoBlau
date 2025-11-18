# sales_notes/tests/test_models.py
import pytest
from django.core.exceptions import ValidationError
from sales_notes.models import Envio, Buque

@pytest.mark.django_db
class TestEnvioModel:
    def test_create_envio_valid(self, api_user):
        """Test creació d'enviament vàlid"""
        envio = Envio.objects.create(
            num_envio="TEST001",
            tipo_respuesta=1,
            usuario_envio=api_user
        )
        assert envio.num_envio == "TEST001"
        assert envio.procesado == False
    
    def test_num_envio_unique(self, api_user):
        """Test constraint d'unicitat"""
        Envio.objects.create(num_envio="TEST001", tipo_respuesta=1, usuario_envio=api_user)
        
        with pytest.raises(Exception):  # IntegrityError
            Envio.objects.create(num_envio="TEST001", tipo_respuesta=1, usuario_envio=api_user)

