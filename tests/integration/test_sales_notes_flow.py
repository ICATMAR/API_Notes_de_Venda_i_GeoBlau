"""
Tests d'integració del flux complet de notes de venda
"""
import pytest
from rest_framework import status


@pytest.mark.integration
class TestSalesNotesCompleteFlow:
    """Test del flux complet: crear, consultar, validar"""
    
    def test_complete_sales_note_lifecycle(self, authenticated_client, test_user):
        """Test: Cicle de vida complet d'una nota de venda"""
        
        # 1. Crear nota de venda
        create_url = '/api/sales-notes/envios/'
        create_data = {
            "NumEnvio": "INT_TEST_001",
            "TipoRespuesta": 1,
            "EstablecimientosVenta": {
                "EstablecimientoVenta": [{
                    "NumIdentificacionEstablec": "LLOTJA_TEST",
                    "Ventas": {
                        "VentasUnidadProductiva": [{
                            "DatosUnidadProductiva": {
                                "MetodoProduccion": 1,
                                "CodigoBuque": "TEST-001",
                                "PuertoAL5": "ESBAR",
                                "FechaRegresoPuerto": "2025-10-22T10:00:00Z"
                            },
                            "Especies": {
                                "Especie": [{
                                    "NumDocVenta": "NV_TEST_001",
                                    "EspecieAL3": "HKE",
                                    "FechaVenta": "2025-10-22T11:00:00Z",
                                    "Cantidad": 100.5,
                                    "Precio": 350.00,
                                    "TipoCifNifVendedor": 1,
                                    "NIFVendedor": "12345678A",
                                    "NombreVendedor": "Test Pescador",
                                    "NIFComprador": "B12345678",
                                    "IdTipoNifCifComprador": 1,
                                    "NombreComprador": "Test Comprador SA"
                                }]
                            }
                        }]
                    }
                }]
            }
        }
        
        create_response = authenticated_client.post(create_url, create_data, format='json')
        assert create_response.status_code == status.HTTP_201_CREATED
        
        # 2. Consultar la nota creada
        num_envio = create_response.data['NumEnvio']
        detail_url = f'/api/sales-notes/envios/{num_envio}/'
        detail_response = authenticated_client.get(detail_url)
        assert detail_response.status_code == status.HTTP_200_OK
        assert detail_response.data['NumEnvio'] == num_envio
        
        # 3. Llistar totes les notes
        list_url = '/api/sales-notes/envios/'
        list_response = authenticated_client.get(list_url)
        assert create_response.status_code == status.HTTP_200_OK
        
        # 4. Validar auditoria
        # Comprovar que s'han creat logs d'auditoria
        from audit.models import AuditLog
        logs = AuditLog.objects.filter(user=test_user).count()
        assert logs > 0