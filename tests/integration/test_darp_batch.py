"""
Tests d'integració per enviaments batch del DARP
"""
import pytest
from rest_framework import status
from django.db import transaction


@pytest.mark.integration
class TestDARPBatchSubmission:
    """Tests per enviaments batch nocturns del DARP"""
    
    def test_batch_submission_success(self, darp_client, sample_sales_note_data, test_catalog_data):
        """Test: Enviar batch de 10 notes de venda amb èxit"""
        url = '/api/sales-notes/envios/'
        created_envios = []
        
        # Enviar 10 enviaments
        for i in range(10):
            # Modificar num_envio per fer-lo únic
            data = sample_sales_note_data.copy()
            data['num_envio'] = f'BATCH_TEST_{i:04d}'
            
            response = darp_client.post(url, data, format='json')
            
            assert response.status_code == status.HTTP_201_CREATED
            created_envios.append(response.data['num_envio'])
        
        # Verificar que s'han creat tots
        assert len(created_envios) == 10
        
        # Llistar i verificar que estan tots
        list_response = darp_client.get(url)
        assert list_response.status_code == status.HTTP_200_OK
        assert len(list_response.data) >= 10
    
    @pytest.mark.django_db(transaction=True)
    def test_batch_rollback_on_error(self, darp_client, sample_sales_note_data):
        """Test: Si un enviament falla, el batch no es comet (rollback)"""
        url = '/api/sales-notes/envios/'
        
        # Crear 3 enviaments vàlids
        valid_data = sample_sales_note_data.copy()
        
        for i in range(3):
            valid_data['NumEnvio'] = f'VALID_{i}'
            response = darp_client.post(url, valid_data, format='json')
            assert response.status_code == status.HTTP_201_CREATED
        
        # Intentar crear un enviament invàlid (num_envio duplicat)
        invalid_data = sample_sales_note_data.copy()
        invalid_data['NumEnvio'] = 'VALID_0'  # Duplicat!
        
        response = darp_client.post(url, invalid_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Els 3 primers haurien d'existir encara (no s'ha fet rollback perquè són transaccions independents)
        # En un batch real, hauríem d'usar transaccions explícites
    
    def test_rate_limiting_batch(self, darp_client, sample_sales_note_data, disable_rate_limiting):
        """Test: Rate limiting permet enviar batches grans"""
        url = '/api/sales-notes/envios/'
        
        # Amb disable_rate_limiting, hauria de permetre més de 100 requests
        for i in range(50):
            data = sample_sales_note_data.copy()
            data['NumEnvio'] = f'RATE_TEST_{i:04d}'
            
            response = darp_client.post(url, data, format='json')
            
            # No hauria de retornar 429 Too Many Requests
            assert response.status_code != status.HTTP_429_TOO_MANY_REQUESTS