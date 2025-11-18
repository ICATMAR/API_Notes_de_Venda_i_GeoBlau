"""
Tests d'integració del flux complet de notes de venda
"""
import pytest
from rest_framework import status


@pytest.mark.integration
class TestSalesNotesCompleteFlow:
    """Test del flux complet: crear, consultar, validar"""
    
    def test_darp_complete_lifecycle(self, darp_client, darp_user, sample_sales_note_data):
        """Test: Cicle de vida complet DARP - crear i consultar enviament"""
        
        # 1. Crear nota de venda
        create_url = '/api/sales-notes/envios/'
        
        response_create = darp_client.post(create_url, sample_sales_note_data, format='json')
        
        assert response_create.status_code == status.HTTP_201_CREATED
        assert 'NumEnvio' in response_create.data
        envio_id = response_create.data['id']
        num_envio = response_create.data['NumEnvio']
        
        # 2. Llistar enviaments (hauria de veure el que acaba de crear)
        list_url = '/api/sales-notes/envios/'
        response_list = darp_client.get(list_url)
        
        assert response_list.status_code == status.HTTP_200_OK
        assert len(response_list.data) >= 1
        assert any(e['NumEnvio'] == num_envio for e in response_list.data)
        
        # 3. Consultar detall de l'enviament
        detail_url = f'/api/sales-notes/envios/{envio_id}/'
        response_detail = darp_client.get(detail_url)
        
        assert response_detail.status_code == status.HTTP_200_OK
        assert response_detail.data['NumEnvio'] == num_envio
        assert response_detail.data['TipoRespuesta'] == sample_sales_note_data['TipoRespuesta']
        
        # 4. Consultar estat
        status_url = f'/api/sales-notes/envios/{envio_id}/status/'
        response_status = darp_client.get(status_url)
        
        assert response_status.status_code == status.HTTP_200_OK
        assert 'procesado' in response_status.data
        assert response_status.data['NumEnvio'] == num_envio
        
        # 5. Validar auditoria
        from audit.models import AuditLog
        logs = AuditLog.objects.filter(user=darp_user)
        assert logs.count() > 0
    
    def test_investigador_read_only_flow(self, investigador_client, darp_client, sample_sales_note_data):
        """Test: Investigador només pot llegir, no crear"""
        
        # 1. Investigador intenta crear (hauria de fallar)
        create_url = '/api/sales-notes/envios/'
        response_create = investigador_client.post(create_url, sample_sales_note_data, format='json')
        
        assert response_create.status_code == status.HTTP_403_FORBIDDEN
        
        # 2. DARP crea un enviament
        response_darp = darp_client.post(create_url, sample_sales_note_data, format='json')
        assert response_darp.status_code == status.HTTP_201_CREATED
        envio_id = response_darp.data['id']
        
        # 3. Investigador pot llistar (inclou l'enviament del DARP)
        list_url = '/api/sales-notes/envios/'
        response_list = investigador_client.get(list_url)
        
        assert response_list.status_code == status.HTTP_200_OK
        assert len(response_list.data) >= 1
        
        # 4. Investigador pot veure detall
        detail_url = f'/api/sales-notes/envios/{envio_id}/'
        response_detail = investigador_client.get(detail_url)
        
        assert response_detail.status_code == status.HTTP_200_OK
        assert response_detail.data['id'] == envio_id
    
    def test_filtering_and_search(self, darp_client, multiple_envios):
        """Test: Filtres i cerca funcionen correctament"""
        
        # 1. Filtrar per tipo_respuesta
        url = '/api/sales-notes/envios/?tipo_respuesta=1'
        response = darp_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert all(e['tipo_respuesta'] == 1 for e in response.data)
        
        # 2. Cerca per num_envio
        url = '/api/sales-notes/envios/?search=DARP_ENV_001'
        response = darp_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        
        # 3. Ordenació
        url = '/api/sales-notes/envios/?ordering=-fecha_recepcion'
        response = darp_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK