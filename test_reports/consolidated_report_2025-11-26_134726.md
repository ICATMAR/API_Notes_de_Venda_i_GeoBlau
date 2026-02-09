# 📋 Report Consolidat de Tests - VCPE API

**Data d'execució:** 26/11/2025 13:47:26
**Projecte:** TFM Ciberseguretat i Privadesa
**Institució:** ICATMAR
**Autor:** Aram Puig Capdevila

---

## 📑 Índex

1. [Resum Executiu](#resum-executiu)
2. [Tests de Connectivitat](#tests-de-connectivitat)
3. [Tests d'Autenticació JWT](#tests-dautenticació-jwt)
4. [Tests Automatitzats (Pytest)](#tests-automatitzats-pytest)
5. [Tests de Seguretat (SAST)](#tests-de-seguretat-sast)
6. [Cobertura de Codi](#cobertura-de-codi)
7. [Anàlisi de Vulnerabilitats](#anàlisi-de-vulnerabilitats)
8. [Conclusions i Recomanacions](#conclusions-i-recomanacions)

---


## 1. Tests de Connectivitat


### 1.1 Estat dels Contenidors Docker


**Temps d'execució:** 0s


```


NAME                 IMAGE                    COMMAND                  SERVICE         CREATED        STATUS                  PORTS
vcpe_api             api_dev-api              "python manage.py ru…"   api             25 hours ago   Up 24 hours (healthy)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
vcpe_celery_beat     api_dev-celery_beat      "celery -A vcpe_api …"   celery_beat     25 hours ago   Up 24 hours (healthy)   8000/tcp
vcpe_celery_worker   api_dev-celery_worker    "celery -A vcpe_api …"   celery_worker   25 hours ago   Up 24 hours (healthy)   8000/tcp
vcpe_postgres        postgis/postgis:16-3.4   "docker-entrypoint.s…"   db              25 hours ago   Up 24 hours (healthy)   0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp
vcpe_redis           redis:7.4-alpine         "docker-entrypoint.s…"   redis           25 hours ago   Up 24 hours (healthy)   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp


```


**Resultat:** ✅ Completat correctament


### 1.2 Health Check de l'API


**Temps d'execució:** 0s


```


{"status": "healthy", "service": "vcpe-api"}


```


**Resultat:** ✅ Completat correctament


### 1.3 Vista Root de l'API


**Temps d'execució:** 0s


```


{"service": "VCPE API - Notes de Venda", "version": "1.0.0", "institution": "ICATMAR", "documentation": "/api/docs/", "endpoints": {"auth": "/api/auth/", "sales_notes": "/api/sales-notes/", "admin": "/admin/"}}


```


**Resultat:** ✅ Completat correctament


### 1.4 Documentació Swagger Accessible


**Temps d'execució:** 0s


```


200


```


**Resultat:** ✅ Completat correctament


## 2. Tests d'Autenticació JWT


### 2.1 Obtenir Token JWT


**Resultat:** ✅ Token obtingut correctament


**Access Token:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90e...`


### 2.2 Verificar Token JWT


**Temps d'execució:** 0s


```


{}


```


**Resultat:** ✅ Completat correctament


### 2.3 Accés sense Token (ha de fallar amb 401)


**Temps d'execució:** 0s


```


{"detail":"Credencials d'autenticació no disponibles."}
401


```


**Resultat:** ✅ Completat correctament


### 2.4 Accés amb Token Vàlid


**Temps d'execució:** 0s


```


{"envios":"http://localhost:8000/api/sales-notes/envios/"}
200


```


**Resultat:** ✅ Completat correctament


## 3. Tests Automatitzats (Pytest)


### 3.1 Tests Unitaris


**Temps d'execució:** 9s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
django: version: 5.1.2, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.0.0
collecting ... collected 100 items

tests/unit/test_audit.py::TestAuditLog::test_audit_log_creation PASSED   [  1%]
tests/unit/test_audit.py::TestAuditLog::test_audit_log_with_old_new_values PASSED [  2%]
tests/unit/test_audit.py::TestAuditLog::test_audit_log_without_user PASSED [  3%]
tests/unit/test_audit.py::TestAuditLog::test_audit_log_ordering PASSED   [  4%]
tests/unit/test_audit.py::TestSecurityEvent::test_security_event_creation PASSED [  5%]
tests/unit/test_audit.py::TestSecurityEvent::test_security_event_with_user PASSED [  6%]
tests/unit/test_audit.py::TestAuditSignals::test_envio_creation_generates_audit_log PASSED [  7%]
tests/unit/test_audit.py::TestAuditSignals::test_failed_login_generates_audit_log PASSED [  8%]
tests/unit/test_audit.py::TestAuditTasks::test_cleanup_old_logs_deletes_old_info_logs PASSED [  9%]
tests/unit/test_audit.py::TestAuditTasks::test_cleanup_old_logs_keeps_critical_logs PASSED [ 10%]
tests/unit/test_audit.py::TestAuditTasks::test_check_security_events_detects_brute_force PASSED [ 11%]
tests/unit/test_audit.py::TestAuditTasks::test_check_security_events_detects_injections PASSED [ 12%]
tests/unit/test_audit.py::TestAuditTasks::test_check_security_events_no_alerts_when_empty PASSED [ 13%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_success PASSED [ 14%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_invalid_credentials PASSED [ 15%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_refresh_token_success PASSED [ 16%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_verify_token_success PASSED [ 17%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_access_protected_endpoint_without_token PASSED [ 18%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_access_protected_endpoint_with_valid_token PASSED [ 19%]
tests/unit/test_exception_handler.py::TestCustomExceptionHandler::test_exception_handler_with_none_response PASSED [ 20%]
tests/unit/test_exception_handler.py::TestCustomExceptionHandler::test_exception_handler_with_validation_error PASSED [ 21%]
tests/unit/test_exception_handler.py::TestCustomExceptionHandler::test_exception_handler_with_not_found PASSED [ 22%]
tests/unit/test_exception_handler.py::TestCustomExceptionHandler::test_exception_handler_with_server_error PASSED [ 23%]
tests/unit/test_exception_handler.py::TestCustomExceptionHandler::test_exception_handler_with_request_id PASSED [ 24%]
tests/unit/test_exception_handler.py::TestCustomExceptionHandler::test_exception_handler_without_request PASSED [ 25%]
tests/unit/test_models.py::TestEnvioModel::test_create_envio_valid PASSED [ 26%]
tests/unit/test_models.py::TestEnvioModel::test_num_envio_unique PASSED  [ 27%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_create_envio PASSED [ 28%]
tests/unit/test_permissions.py::TestUserPermissions::test_investigador_cannot_create_envio PASSED [ 29%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_list_own_envios PASSED [ 30%]
tests/unit/test_permissions.py::TestUserPermissions::test_investigador_can_list_all_envios PASSED [ 31%]
tests/unit/test_permissions.py::TestUserPermissions::test_admin_can_list_all_envios PASSED [ 32%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_retrieve_own_envio PASSED [ 33%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_cannot_retrieve_other_envio PASSED [ 34%]
tests/unit/test_permissions.py::TestUserPermissions::test_investigador_can_retrieve_any_envio PASSED [ 35%]
tests/unit/test_permissions.py::TestUserPermissions::test_unauthenticated_cannot_access PASSED [ 36%]
tests/unit/test_sales_notes_permissions.py::TestIsDARP::test_darp_user_has_permission PASSED [ 37%]
tests/unit/test_sales_notes_permissions.py::TestIsDARP::test_investigador_no_permission PASSED [ 38%]
tests/unit/test_sales_notes_permissions.py::TestIsDARP::test_unauthenticated_no_permission PASSED [ 39%]
tests/unit/test_sales_notes_permissions.py::TestIsInvestigador::test_investigador_has_permission PASSED [ 40%]
tests/unit/test_sales_notes_permissions.py::TestIsInvestigador::test_darp_no_investigador_permission PASSED [ 41%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_admin_full_access PASSED [ 42%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_darp_can_post PASSED [ 43%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_darp_can_get PASSED [ 44%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_investigador_can_get PASSED [ 45%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_investigador_cannot_post PASSED [ 46%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_investigador_cannot_put PASSED [ 47%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_darp_can_access_own_envio PASSED [ 48%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_darp_cannot_access_other_envio PASSED [ 49%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_investigador_can_read_any_envio PASSED [ 50%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_investigador_cannot_modify_any_envio PASSED [ 51%]
tests/unit/test_serializers.py::TestFechaCapturaSerializer::test_valid_fecha_captura PASSED [ 52%]
tests/unit/test_serializers.py::TestFechaCapturaSerializer::test_fecha_captura_solo_inicio PASSED [ 53%]
tests/unit/test_serializers.py::TestFechaCapturaSerializer::test_fecha_fin_anterior_a_inicio_error PASSED [ 54%]
tests/unit/test_serializers.py::TestFechaCapturaSerializer::test_fechas_iguales_valido PASSED [ 55%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_especie_valida_completa PASSED [ 56%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_especie_al3_formato_invalido PASSED [ 57%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_especie_al3_con_numeros_invalido PASSED [ 58%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_especie_al3_uppercase PASSED [ 59%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_cantidad_negativa_invalida PASSED [ 60%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_cantidad_cero_invalida PASSED [ 61%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_precio_negativo_invalido PASSED [ 62%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_precio_cero_valido PASSED [ 63%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_retirada_con_destino_valido PASSED [ 64%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_especie_con_fechas_captura PASSED [ 65%]
tests/unit/test_serializers.py::TestBuqueSerializer::test_buque_valido PASSED [ 66%]
tests/unit/test_serializers.py::TestBuqueSerializer::test_puerto_formato_invalido PASSED [ 67%]
tests/unit/test_serializers.py::TestGranjaSerializer::test_granja_valida PASSED [ 68%]
tests/unit/test_serializers.py::TestGranjaSerializer::test_codigo_rega_largo_invalido PASSED [ 69%]
tests/unit/test_serializers.py::TestPersonaFisicaJuridicaSerializer::test_persona_valida PASSED [ 70%]
tests/unit/test_serializers.py::TestPersonaFisicaJuridicaSerializer::test_nif_largo_invalido PASSED [ 71%]
tests/unit/test_serializers.py::TestUnidadProductivaSerializer::test_unidad_con_buque_valida PASSED [ 72%]
tests/unit/test_serializers.py::TestUnidadProductivaSerializer::test_unidad_con_granja_valida PASSED [ 73%]
tests/unit/test_serializers.py::TestUnidadProductivaSerializer::test_unidad_con_persona_valida PASSED [ 74%]
tests/unit/test_serializers.py::TestUnidadProductivaSerializer::test_metodo_1_sin_buque_ni_persona_invalido PASSED [ 75%]
tests/unit/test_serializers.py::TestEstablecimientoVentaSerializer::test_establecimiento_valido PASSED [ 76%]
tests/unit/test_serializers.py::TestEstablecimientoVentaSerializer::test_num_identificacion_vacio_invalido PASSED [ 77%]
tests/unit/test_serializers.py::TestEnvioSerializer::test_num_envio_duplicado_invalido PASSED [ 78%]
tests/unit/test_serializers.py::TestEnvioSerializer::test_tipo_respuesta_invalido PASSED [ 79%]
tests/unit/test_serializers.py::TestEnvioSerializer::test_to_representation_respuesta_reducida PASSED [ 80%]
tests/unit/test_serializers.py::TestEnvioListSerializer::test_list_serializer PASSED [ 81%]
tests/unit/test_serializers.py::TestEnvioStatusSerializer::test_status_serializer PASSED [ 82%]
tests/unit/test_serializers.py::TestSerializersEdgeCases::test_especie_talla_no_reglamentaria_sin_observaciones PASSED [ 83%]
tests/unit/test_serializers.py::TestSerializersEdgeCases::test_buque_puerto_none_valido PASSED [ 84%]
tests/unit/test_serializers.py::TestSerializersEdgeCases::test_granja_fecha_produccion_future PASSED [ 85%]
tests/unit/test_serializers.py::TestSerializersEdgeCases::test_envio_sin_establecimientos_warning PASSED [ 86%]
tests/unit/test_serializers.py::TestSerializersEdgeCases::test_unidad_productiva_metodo_4_con_persona PASSED [ 87%]
tests/unit/test_serializers.py::TestSerializersEdgeCases::test_especie_precio_decimal_precision PASSED [ 88%]
tests/unit/test_serializers.py::TestSerializersEdgeCases::test_fecha_captura_formato_iso PASSED [ 89%]
tests/unit/test_serializers.py::TestSerializersEdgeCases::test_puerto_al5_exactament_5_chars PASSED [ 90%]
tests/unit/test_tasks.py::TestTasks::test_generate_daily_report_executes PASSED [ 91%]
tests/unit/test_tasks.py::TestTasks::test_process_pending_envios_executes PASSED [ 92%]
tests/unit/test_views.py::TestEnvioViewSetCoverage::test_envio_status_endpoint PASSED [ 93%]
tests/unit/test_views.py::TestEnvioViewSetCoverage::test_list_uses_list_serializer PASSED [ 94%]
tests/unit/test_views.py::TestEnvioViewSetCoverage::test_retrieve_envio_detail PASSED [ 95%]
tests/unit/test_views.py::TestSerializersValidation::test_envio_serializer_with_invalid_tipo_respuesta PASSED [ 96%]
tests/unit/test_views.py::TestSerializersValidation::test_buque_serializer_validation PASSED [ 97%]
tests/unit/test_views.py::TestModelsEdgeCases::test_envio_str_representation PASSED [ 98%]
tests/unit/test_views.py::TestPermissionsEdgeCases::test_admin_has_full_access PASSED [ 99%]
tests/unit/test_views.py::TestPermissionsEdgeCases::test_investigador_can_see_all PASSED [100%]

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     26  70.45%   36, 77-78, 84-102, 108, 119-120, 140-141, 152, 166-192
audit/models.py                                               79      3  96.20%   82, 173, 217
audit/signals.py                                              77     27  64.94%   36-37, 71-72, 78-98, 104-114, 163-170, 176-188
audit/tasks.py                                                51      6  88.24%   78-79, 108, 134-141
authentication/apps.py                                         7      0 100.00%
authentication/management/commands/create_test_users.py       23     23   0.00%   5-52
authentication/management/commands/create_user_groups.py      17     17   0.00%   5-33
authentication/models.py                                     129     29  77.52%   94-99, 103-106, 110-113, 154, 219, 223-227, 231-235, 306-307, 314
authentication/permissions.py                                  0      0 100.00%
authentication/serializers.py                                 83     22  73.49%   59-61, 73-75, 123, 152-158, 227-235, 250-253, 310
authentication/urls.py                                         5      0 100.00%
authentication/views.py                                      121     84  30.58%   40-45, 58, 82-94, 136-289, 321-360, 394-417, 440, 462-463
sales_notes/apps.py                                            7      0 100.00%
sales_notes/exception_handler.py                              20      0 100.00%
sales_notes/existing_models.py                                87      3  96.55%   31, 72, 112
sales_notes/models.py                                        200     17  91.50%   92, 134, 191-192, 198, 221, 251, 281, 450-451, 472, 477-479, 505-507
sales_notes/permissions.py                                    30      5  83.33%   39, 57, 72, 78, 89
sales_notes/serializers.py                                   266     38  85.71%   98, 104, 110, 118, 122-123, 138, 152, 166, 199, 202, 208, 237-240, 248, 272, 301, 307, 368-374, 397-401, 423, 469-476, 511, 557
sales_notes/tasks.py                                          27      0 100.00%
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                          72      4  94.44%   85, 105, 145-146
-----------------------------------------------------------------------------------------
TOTAL                                                       1403    304  78.33%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 78.33%

============================= 100 passed in 6.82s ==============================


```


**Resultat:** ✅ Completat correctament


### 3.2 Tests d'Integració


**Temps d'execució:** 8s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
django: version: 5.1.2, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.0.0
collecting ... collected 10 items

tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_submission_success PASSED [ 10%]
tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_rate_limiting_batch PASSED [ 20%]
tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_darp_complete_lifecycle PASSED [ 30%]
tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_investigador_read_only_flow PASSED [ 40%]
tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_filtering_and_search PASSED [ 50%]
tests/integration/test_sales_notes_flow.py::TestAdvancedSalesNotesFlow::test_envio_lifecycle_with_validation PASSED [ 60%]
tests/integration/test_sales_notes_flow.py::TestAdvancedSalesNotesFlow::test_multiple_users_isolation PASSED [ 70%]
tests/integration/test_sales_notes_flow.py::TestAdvancedSalesNotesFlow::test_pagination_and_ordering PASSED [ 80%]
tests/integration/test_sales_notes_flow.py::TestAdvancedSalesNotesFlow::test_invalid_data_returns_detailed_errors PASSED [ 90%]
tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_rollback_on_error PASSED [100%]

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     19  78.41%   36, 77-78, 84-102, 108, 119-120, 141, 152, 184, 190, 228-229
audit/models.py                                               79      3  96.20%   82, 173, 217
audit/signals.py                                              77     40  48.05%   36-37, 49, 71-72, 78-98, 104-114, 120-141, 163-170, 176-188
audit/tasks.py                                                51     51   0.00%   5-146
authentication/apps.py                                         7      0 100.00%
authentication/management/commands/create_test_users.py       23     23   0.00%   5-52
authentication/management/commands/create_user_groups.py      17     17   0.00%   5-33
authentication/models.py                                     129     29  77.52%   94-99, 103-106, 110-113, 154, 219, 223-227, 231-235, 306-307, 314
authentication/permissions.py                                  0      0 100.00%
authentication/serializers.py                                 83     22  73.49%   59-61, 73-75, 123, 152-158, 227-235, 250-253, 310
authentication/urls.py                                         5      0 100.00%
authentication/views.py                                      121     84  30.58%   40-45, 58, 82-94, 136-289, 321-360, 394-417, 440, 462-463
sales_notes/apps.py                                            7      0 100.00%
sales_notes/exception_handler.py                              20     20   0.00%   1-63
sales_notes/existing_models.py                                87      3  96.55%   31, 72, 112
sales_notes/models.py                                        200     18  91.00%   69, 92, 134, 191-192, 198, 221, 251, 281, 450-451, 472, 477-479, 505-507
sales_notes/permissions.py                                    30     11  63.33%   19-24, 38-43, 57, 61, 72, 78, 89
sales_notes/serializers.py                                   266     58  78.20%   37-40, 98, 104, 110, 117-118, 122-123, 138, 151-153, 165-167, 196-202, 208, 215-218, 237-240, 248, 272, 301, 307, 315, 326, 368-374, 389, 397-401, 423, 469-476, 511
sales_notes/tasks.py                                          27     27   0.00%   5-59
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                          72      5  93.06%   74, 85, 105, 145-146
-----------------------------------------------------------------------------------------
TOTAL                                                       1403    430  69.35%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 69.35%

============================== 10 passed in 5.66s ==============================


```


**Resultat:** ✅ Completat correctament


### 3.3 Tests de Seguretat


**Temps d'execució:** 6s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
django: version: 5.1.2, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.0.0
collecting ... collected 14 items

tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_access_other_user_data PASSED [  7%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_brute_force_protection PASSED [ 14%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_mass_assignment_vulnerability PASSED [ 21%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_rate_limiting SKIPPED [ 28%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_admin_endpoint_access_control PASSED [ 35%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_prevent_automated_submission SKIPPED [ 42%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_security_headers_present PASSED [ 50%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_api_documentation_access_control SKIPPED [ 57%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_input_validation_sql_injection PASSED [ 64%]
tests/security/test_owasp_api_security.py::TestAdditionalSecurityControls::test_no_information_disclosure_on_error PASSED [ 71%]
tests/security/test_owasp_api_security.py::TestAdditionalSecurityControls::test_csrf_protection PASSED [ 78%]
tests/security/test_owasp_api_security.py::TestAdditionalSecurityControls::test_cors_headers_not_too_permissive PASSED [ 85%]
tests/security/test_owasp_api_security.py::TestAdditionalSecurityControls::test_audit_log_created_on_envio_creation PASSED [ 92%]
tests/security/test_owasp_api_security.py::TestAdditionalSecurityControls::test_sensitive_data_not_in_logs PASSED [100%]

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     19  78.41%   36, 77-78, 84-102, 108, 119-120, 141, 152, 184, 190, 228-229
audit/models.py                                               79      3  96.20%   82, 173, 217
audit/signals.py                                              77     40  48.05%   36-37, 49, 71-72, 78-98, 104-114, 120-141, 163-170, 176-188
audit/tasks.py                                                51     51   0.00%   5-146
authentication/apps.py                                         7      0 100.00%
authentication/management/commands/create_test_users.py       23     23   0.00%   5-52
authentication/management/commands/create_user_groups.py      17     17   0.00%   5-33
authentication/models.py                                     129     29  77.52%   94-99, 103-106, 110-113, 154, 219, 223-227, 231-235, 306-307, 314
authentication/permissions.py                                  0      0 100.00%
authentication/serializers.py                                 83     22  73.49%   59-61, 73-75, 123, 152-158, 227-235, 250-253, 310
authentication/urls.py                                         5      0 100.00%
authentication/views.py                                      121     84  30.58%   40-45, 58, 82-94, 136-289, 321-360, 394-417, 440, 462-463
sales_notes/apps.py                                            7      0 100.00%
sales_notes/exception_handler.py                              20     20   0.00%   1-63
sales_notes/existing_models.py                                87      3  96.55%   31, 72, 112
sales_notes/models.py                                        200     18  91.00%   69, 92, 134, 191-192, 198, 221, 251, 281, 450-451, 472, 477-479, 505-507
sales_notes/permissions.py                                    30     17  43.33%   19-24, 38-43, 57, 61, 65, 72, 77-89
sales_notes/serializers.py                                   266     62  76.69%   37-40, 98, 104, 110, 117-118, 122-123, 138, 151-153, 165-167, 196-202, 208, 215-218, 237-240, 248, 272, 301, 307, 368-374, 389, 397-401, 423, 469-476, 511, 549, 554-558
sales_notes/tasks.py                                          27     27   0.00%   5-59
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                          72     30  58.33%   70-85, 89-93, 105, 139-149, 159-164, 178-183
-----------------------------------------------------------------------------------------
TOTAL                                                       1403    465  66.86%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 66.86%

======================== 11 passed, 3 skipped in 3.28s =========================


```


**Resultat:** ✅ Completat correctament


## 4. Cobertura de Codi


### 4.1 Generar Informe de Cobertura


**Temps d'execució:** 12s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0
django: version: 5.1.2, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.0.0
collected 124 items

tests/integration/test_darp_batch.py ..                                  [  1%]
tests/integration/test_sales_notes_flow.py .......                       [  7%]
tests/security/test_owasp_api_security.py ...s.s.s......                 [ 18%]
tests/unit/test_audit.py .............                                   [ 29%]
tests/unit/test_authentication.py ......                                 [ 33%]
tests/unit/test_exception_handler.py ......                              [ 38%]
tests/unit/test_models.py ..                                             [ 40%]
tests/unit/test_permissions.py .........                                 [ 47%]
tests/unit/test_sales_notes_permissions.py ...............               [ 59%]
tests/unit/test_serializers.py .......................................   [ 91%]
tests/unit/test_tasks.py ..                                              [ 92%]
tests/unit/test_views.py ........                                        [ 99%]
tests/integration/test_darp_batch.py .                                   [100%]

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     17  80.68%   36, 77-78, 84-102, 108, 119-120, 141, 152, 184, 190
audit/models.py                                               79      3  96.20%   82, 173, 217
audit/signals.py                                              77     27  64.94%   36-37, 71-72, 78-98, 104-114, 163-170, 176-188
audit/tasks.py                                                51      6  88.24%   78-79, 108, 134-141
authentication/apps.py                                         7      0 100.00%
authentication/management/commands/create_test_users.py       23     23   0.00%   5-52
authentication/management/commands/create_user_groups.py      17     17   0.00%   5-33
authentication/models.py                                     129     29  77.52%   94-99, 103-106, 110-113, 154, 219, 223-227, 231-235, 306-307, 314
authentication/permissions.py                                  0      0 100.00%
authentication/serializers.py                                 83     22  73.49%   59-61, 73-75, 123, 152-158, 227-235, 250-253, 310
authentication/urls.py                                         5      0 100.00%
authentication/views.py                                      121     84  30.58%   40-45, 58, 82-94, 136-289, 321-360, 394-417, 440, 462-463
sales_notes/apps.py                                            7      0 100.00%
sales_notes/exception_handler.py                              20      0 100.00%
sales_notes/existing_models.py                                87      3  96.55%   31, 72, 112
sales_notes/models.py                                        200     17  91.50%   92, 134, 191-192, 198, 221, 251, 281, 450-451, 472, 477-479, 505-507
sales_notes/permissions.py                                    30      5  83.33%   39, 57, 72, 78, 89
sales_notes/serializers.py                                   266     37  86.09%   98, 104, 110, 118, 122-123, 138, 152, 166, 199, 202, 208, 237-240, 248, 272, 301, 307, 368-374, 397-401, 423, 469-476, 511
sales_notes/tasks.py                                          27      0 100.00%
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                          72      4  94.44%   85, 105, 145-146
-----------------------------------------------------------------------------------------
TOTAL                                                       1403    294  79.04%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 79.04%

======================== 121 passed, 3 skipped in 9.80s ========================


```


**Resultat:** ✅ Completat correctament


ℹ️ Informe HTML disponible a: `htmlcov/index.html`


## 5. Tests de Seguretat (SAST)


### 5.1 Anàlisi amb Bandit (Vulnerabilitats Python)


**Temps d'execució:** 1s


```


[main]	INFO	profile include tests: None
[main]	INFO	profile exclude tests: None
[main]	INFO	cli include tests: None
[main]	INFO	cli exclude tests: None
[main]	INFO	running on Python 3.12.12
Working... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Run started:2025-11-26 12:48:06.470079

Test results:
	No issues identified.

Code scanned:
	Total lines of code: 7017
	Total lines skipped (#nosec): 0
	Total potential issues skipped due to specifically being disabled (e.g., #nosec BXXX): 2

Run metrics:
	Total issues (by severity):
		Undefined: 0
		Low: 257
		Medium: 0
		High: 0
	Total issues (by confidence):
		Undefined: 0
		Low: 0
		Medium: 5
		High: 252
Files skipped (0):


```


**Resultat:** ✅ Completat correctament


⚠️ **Safety no disponible**


### 5.3 Django Security Check


**Temps d'execució:** 1s


```


System check identified some issues:

WARNINGS:
?: (django_ratelimit.W001) cache backend django.core.cache.backends.redis.RedisCache is not officially supported
?: (drf_spectacular.W001) Warning: encountered multiple names for the same choice set (IdTipoNifCifCompradorEnum). This may be unwanted even though the generated schema is technically correct. Add an entry to ENUM_NAME_OVERRIDES to fix the naming.
?: (drf_spectacular.W002) /app/authentication/views.py: Error [LogoutView]: unable to guess serializer. This is graceful fallback handling for APIViews. Consider using GenericAPIView as view base class, if view is under your control. Either way you may want to add a serializer_class (or method). Ignoring view for now.
?: (drf_spectacular.W002) /app/authentication/views.py: Error [PasswordChangeView]: unable to guess serializer. This is graceful fallback handling for APIViews. Consider using GenericAPIView as view base class, if view is under your control. Either way you may want to add a serializer_class (or method). Ignoring view for now.
?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
?: (security.W018) You should not have DEBUG set to True in deployment.

System check identified 9 issues (0 silenced).


```


**Resultat:** ✅ Completat correctament


## 6. Anàlisi de Qualitat de Codi


### 6.1 Linting amb Flake8


**Temps d'execució:** 1s


```


./__init__.py:55:9: F401 'audit.signals' imported but unused
./audit/middleware.py:75:80: E501 line too long (80 > 79 characters)
./audit/middleware.py:78:80: E501 line too long (86 > 79 characters)
./audit/middleware.py:119:13: E722 do not use bare 'except'
./audit/middleware.py:143:80: E501 line too long (82 > 79 characters)
./audit/middleware.py:202:80: E501 line too long (115 > 79 characters)
./audit/middleware.py:207:80: E501 line too long (119 > 79 characters)
./audit/middleware.py:220:80: E501 line too long (113 > 79 characters)
./audit/middleware.py:226:80: E501 line too long (116 > 79 characters)
./audit/middleware.py:229:80: E501 line too long (89 > 79 characters)
./audit/migrations/0001_initial.py:24:80: E501 line too long (112 > 79 characters)
./audit/migrations/0001_initial.py:43:80: E501 line too long (87 > 79 characters)
./audit/migrations/0001_initial.py:44:80: E501 line too long (85 > 79 characters)
./audit/migrations/0001_initial.py:47:80: E501 line too long (110 > 79 characters)
./audit/migrations/0001_initial.py:51:80: E501 line too long (117 > 79 characters)
./audit/migrations/0001_initial.py:53:80: E501 line too long (84 > 79 characters)
./audit/migrations/0001_initial.py:55:80: E501 line too long (91 > 79 characters)
./audit/migrations/0001_initial.py:70:80: E501 line too long (86 > 79 characters)
./audit/migrations/0001_initial.py:97:80: E501 line too long (101 > 79 characters)
./audit/migrations/0001_initial.py:98:80: E501 line too long (100 > 79 characters)
./audit/migrations/0001_initial.py:99:80: E501 line too long (104 > 79 characters)
./audit/migrations/0001_initial.py:100:80: E501 line too long (106 > 79 characters)
./audit/migrations/0001_initial.py:107:80: E501 line too long (112 > 79 characters)
./audit/migrations/0001_initial.py:108:80: E501 line too long (116 > 79 characters)
./audit/migrations/0001_initial.py:112:80: E501 line too long (109 > 79 characters)
./audit/migrations/0001_initial.py:115:80: E501 line too long (91 > 79 characters)
./audit/migrations/0001_initial.py:116:80: E501 line too long (113 > 79 characters)
./audit/migrations/0001_initial.py:117:80: E501 line too long (94 > 79 characters)
./audit/migrations/0001_initial.py:118:80: E501 line too long (119 > 79 characters)
./audit/migrations/0001_initial.py:121:80: E501 line too long (86 > 79 characters)
./audit/migrations/0001_initial.py:137:80: E501 line too long (109 > 79 characters)
./audit/migrations/0001_initial.py:138:80: E501 line too long (106 > 79 characters)
./audit/migrations/0001_initial.py:145:80: E501 line too long (112 > 79 characters)
./audit/migrations/0001_initial.py:154:80: E501 line too long (82 > 79 characters)
./audit/migrations/0001_initial.py:157:80: E501 line too long (85 > 79 characters)
./audit/migrations/0001_initial.py:169:80: E501 line too long (83 > 79 characters)
./audit/migrations/0001_initial.py:170:80: E501 line too long (106 > 79 characters)
./audit/migrations/0001_initial.py:171:80: E501 line too long (108 > 79 characters)
./audit/migrations/0001_initial.py:175:80: E501 line too long (117 > 79 characters)
./audit/migrations/0001_initial.py:195:80: E501 line too long (113 > 79 characters)
./audit/migrations/0001_initial.py:197:80: E501 line too long (86 > 79 characters)
./audit/migrations/0001_initial.py:226:80: E501 line too long (108 > 79 characters)
./audit/migrations/0001_initial.py:227:80: E501 line too long (103 > 79 characters)
./audit/migrations/0001_initial.py:228:80: E501 line too long (108 > 79 characters)
./audit/migrations/0001_initial.py:229:80: E501 line too long (105 > 79 characters)
./audit/models.py:32:80: E501 line too long (83 > 79 characters)
./audit/models.py:36:80: E501 line too long (109 > 79 characters)
./audit/models.py:40:80: E501 line too long (98 > 79 characters)
./audit/models.py:48:80: E501 line too long (105 > 79 characters)
./audit/models.py:49:80: E501 line too long (112 > 79 characters)
./audit/models.py:64:80: E501 line too long (103 > 79 characters)
./audit/models.py:104:80: E501 line too long (91 > 79 characters)
./audit/models.py:108:80: E501 line too long (114 > 79 characters)
./audit/models.py:121:80: E501 line too long (90 > 79 characters)
./audit/models.py:123:80: E501 line too long (92 > 79 characters)
./audit/models.py:133:80: E501 line too long (105 > 79 characters)
./audit/models.py:142:80: E501 line too long (98 > 79 characters)
./audit/models.py:145:80: E501 line too long (97 > 79 characters)
./audit/models.py:173:80: E501 line too long (86 > 79 characters)
./audit/models.py:183:80: E501 line too long (110 > 79 characters)
./audit/models.py:186:80: E501 line too long (100 > 79 characters)
./audit/models.py:188:80: E501 line too long (120 > 79 characters)
./audit/models.py:193:80: E501 line too long (97 > 79 characters)
./audit/models.py:198:80: E501 line too long (103 > 79 characters)
./audit/signals.py:7:80: E501 line too long (90 > 79 characters)
./audit/signals.py:13:1: F401 'sales_notes.models.Especie' imported but unused
./audit/signals.py:53:80: E501 line too long (86 > 79 characters)
./audit/signals.py:64:80: E501 line too long (83 > 79 characters)
./audit/signals.py:72:80: E501 line too long (82 > 79 characters)
./audit/signals.py:94:80: E501 line too long (103 > 79 characters)
./audit/signals.py:128:80: E501 line too long (82 > 79 characters)
./audit/signals.py:139:80: E501 line too long (81 > 79 characters)
./audit/signals.py:152:80: E501 line too long (90 > 79 characters)
./audit/signals.py:162:80: E501 line too long (91 > 79 characters)
./audit/tasks.py:24:80: E501 line too long (107 > 79 characters)
./audit/tasks.py:27:80: E501 line too long (92 > 79 characters)
./audit/tasks.py:32:80: E501 line too long (96 > 79 characters)
./audit/tasks.py:38:80: E501 line too long (80 > 79 characters)
./audit/tasks.py:39:80: E501 line too long (80 > 79 characters)
./audit/tasks.py:50:80: E501 line too long (93 > 79 characters)
./audit/tasks.py:51:80: E501 line too long (93 > 79 characters)
./audit/tasks.py:89:80: E501 line too long (85 > 79 characters)
./audit/tasks.py:90:80: E501 line too long (89 > 79 characters)
./audit/tasks.py:100:80: E501 line too long (97 > 79 characters)
./audit/tasks.py:111:80: E501 line too long (93 > 79 characters)
./audit/tasks.py:117:80: E501 line too long (99 > 79 characters)
./audit/tasks.py:153:80: E501 line too long (97 > 79 characters)
./authentication/admin.py:37:80: E501 line too long (87 > 79 characters)
./authentication/admin.py:53:80: E501 line too long (103 > 79 characters)
./authentication/admin.py:54:80: E501 line too long (112 > 79 characters)
./authentication/admin.py:57:80: E501 line too long (115 > 79 characters)
./authentication/admin.py:61:80: E501 line too long (104 > 79 characters)
./authentication/admin.py:83:80: E501 line too long (103 > 79 characters)
./authentication/admin.py:86:80: E501 line too long (82 > 79 characters)
./authentication/admin.py:89:80: E501 line too long (93 > 79 characters)
./authentication/admin.py:130:80: E501 line too long (108 > 79 characters)
./authentication/admin.py:160:80: E501 line too long (80 > 79 characters)
./authentication/admin.py:161:80: E501 line too long (92 > 79 characters)
./authentication/admin.py:174:80: E501 line too long (119 > 79 characters)
./authentication/admin.py:198:80: E501 line too long (82 > 79 characters)
./authentication/admin.py:201:80: E501 line too long (103 > 79 characters)
./authentication/admin.py:260:80: E501 line too long (112 > 79 characters)
./authentication/admin.py:275:80: E501 line too long (116 > 79 characters)
./authentication/admin.py:279:80: E501 line too long (103 > 79 characters)
./authentication/admin.py:296:80: E501 line too long (92 > 79 characters)
./authentication/admin.py:328:80: E501 line too long (104 > 79 characters)
./authentication/management/commands/create_test_users.py:31:80: E501 line too long (93 > 79 characters)
./authentication/management/commands/create_test_users.py:33:50: F541 f-string is missing placeholders
./authentication/management/commands/create_test_users.py:50:80: E501 line too long (100 > 79 characters)
./authentication/management/commands/create_test_users.py:52:50: F541 f-string is missing placeholders
./authentication/management/commands/create_test_users.py:52:80: E501 line too long (85 > 79 characters)
./authentication/management/commands/create_user_groups.py:20:80: E501 line too long (89 > 79 characters)
./authentication/management/commands/create_user_groups.py:21:80: E501 line too long (87 > 79 characters)
./authentication/management/commands/create_user_groups.py:26:80: E501 line too long (99 > 79 characters)
./authentication/management/commands/create_user_groups.py:31:80: E501 line too long (108 > 79 characters)
./authentication/migrations/0001_initial.py:26:80: E501 line too long (88 > 79 characters)
./authentication/migrations/0001_initial.py:27:80: E501 line too long (103 > 79 characters)
./authentication/migrations/0001_initial.py:32:80: E501 line too long (117 > 79 characters)
./authentication/migrations/0001_initial.py:39:80: E501 line too long (95 > 79 characters)
./authentication/migrations/0001_initial.py:40:80: E501 line too long (107 > 79 characters)
./authentication/migrations/0001_initial.py:43:80: E501 line too long (95 > 79 characters)
./authentication/migrations/0001_initial.py:47:80: E501 line too long (104 > 79 characters)
./authentication/migrations/0001_initial.py:48:80: E501 line too long (102 > 79 characters)
./authentication/migrations/0001_initial.py:49:80: E501 line too long (103 > 79 characters)
./authentication/migrations/0001_initial.py:54:80: E501 line too long (94 > 79 characters)
./authentication/migrations/0001_initial.py:62:80: E501 line too long (94 > 79 characters)
./authentication/migrations/0001_initial.py:67:80: E501 line too long (117 > 79 characters)
./authentication/migrations/0001_initial.py:68:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:72:80: E501 line too long (110 > 79 characters)
./authentication/migrations/0001_initial.py:75:80: E501 line too long (118 > 79 characters)
./authentication/migrations/0001_initial.py:83:80: E501 line too long (94 > 79 characters)
./authentication/migrations/0001_initial.py:90:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:96:80: E501 line too long (83 > 79 characters)
./authentication/migrations/0001_initial.py:102:80: E501 line too long (117 > 79 characters)
./authentication/migrations/0001_initial.py:103:80: E501 line too long (118 > 79 characters)
./authentication/migrations/0001_initial.py:106:80: E501 line too long (113 > 79 characters)
./authentication/migrations/0001_initial.py:110:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:114:80: E501 line too long (110 > 79 characters)
./authentication/migrations/0001_initial.py:118:80: E501 line too long (117 > 79 characters)
./authentication/migrations/0001_initial.py:126:80: E501 line too long (85 > 79 characters)
./authentication/migrations/0001_initial.py:158:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:165:80: E501 line too long (95 > 79 characters)
./authentication/migrations/0001_initial.py:168:80: E501 line too long (115 > 79 characters)
./authentication/migrations/0001_initial.py:171:80: E501 line too long (86 > 79 characters)
./authentication/migrations/0001_initial.py:192:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:199:80: E501 line too long (83 > 79 characters)
./authentication/migrations/0001_initial.py:214:80: E501 line too long (88 > 79 characters)
./authentication/migrations/0001_initial.py:215:80: E501 line too long (88 > 79 characters)
./authentication/migrations/0001_initial.py:216:80: E501 line too long (120 > 79 characters)
./authentication/migrations/0001_initial.py:217:80: E501 line too long (102 > 79 characters)
./authentication/migrations/0001_initial.py:233:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:256:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:261:80: E501 line too long (84 > 79 characters)
./authentication/migrations/0001_initial.py:270:80: E501 line too long (91 > 79 characters)
./authentication/migrations/0001_initial.py:276:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:277:80: E501 line too long (95 > 79 characters)
./authentication/migrations/0001_initial.py:278:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:279:80: E501 line too long (103 > 79 characters)
./authentication/migrations/0001_initial.py:280:80: E501 line too long (118 > 79 characters)
./authentication/migrations/0001_initial.py:281:80: E501 line too long (88 > 79 characters)
./authentication/migrations/0001_initial.py:282:80: E501 line too long (88 > 79 characters)
./authentication/migrations/0001_initial.py:313:80: E501 line too long (96 > 79 characters)
./authentication/migrations/0001_initial.py:317:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:321:80: E501 line too long (100 > 79 characters)
./authentication/migrations/0001_initial.py:325:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:329:80: E501 line too long (107 > 79 characters)
./authentication/migrations/0001_initial.py:333:80: E501 line too long (93 > 79 characters)
./authentication/migrations/0001_initial.py:337:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:341:80: E501 line too long (100 > 79 characters)
./authentication/migrations/0001_initial.py:345:80: E501 line too long (104 > 79 characters)
./authentication/migrations/0001_initial.py:349:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:353:80: E501 line too long (114 > 79 characters)
./authentication/migrations/0001_initial.py:357:80: E501 line too long (95 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:31:80: E501 line too long (115 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:36:80: E501 line too long (114 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:41:80: E501 line too long (104 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:46:80: E501 line too long (115 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:52:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:58:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:62:80: E501 line too long (96 > 79 characters)
./authentication/migrations/0003_alter_apiuser_cif_organization.py:9:80: E501 line too long (87 > 79 characters)
./authentication/migrations/0003_alter_apiuser_cif_organization.py:16:80: E501 line too long (85 > 79 characters)
./authentication/models.py:23:80: E501 line too long (94 > 79 characters)
./authentication/models.py:26:80: E501 line too long (89 > 79 characters)
./authentication/models.py:28:80: E501 line too long (112 > 79 characters)
./authentication/models.py:30:80: E501 line too long (115 > 79 characters)
./authentication/models.py:32:80: E501 line too long (103 > 79 characters)
./authentication/models.py:34:80: E501 line too long (119 > 79 characters)
./authentication/models.py:36:80: E501 line too long (119 > 79 characters)
./authentication/models.py:39:80: E501 line too long (98 > 79 characters)
./authentication/models.py:46:80: E501 line too long (99 > 79 characters)
./authentication/models.py:50:80: E501 line too long (105 > 79 characters)
./authentication/models.py:53:80: E501 line too long (117 > 79 characters)
./authentication/models.py:57:80: E501 line too long (101 > 79 characters)
./authentication/models.py:59:80: E501 line too long (102 > 79 characters)
./authentication/models.py:62:80: E501 line too long (110 > 79 characters)
./authentication/models.py:65:80: E501 line too long (111 > 79 characters)
./authentication/models.py:67:80: E501 line too long (117 > 79 characters)
./authentication/models.py:70:80: E501 line too long (82 > 79 characters)
./authentication/models.py:94:80: E501 line too long (84 > 79 characters)
./authentication/models.py:97:80: E501 line too long (86 > 79 characters)
./authentication/models.py:105:80: E501 line too long (87 > 79 characters)
./authentication/models.py:106:80: E501 line too long (82 > 79 characters)
./authentication/models.py:113:80: E501 line too long (99 > 79 characters)
./authentication/models.py:122:80: E501 line too long (103 > 79 characters)
./authentication/models.py:135:80: E501 line too long (118 > 79 characters)
./authentication/models.py:154:80: E501 line too long (87 > 79 characters)
./authentication/models.py:165:80: E501 line too long (103 > 79 characters)
./authentication/models.py:188:80: E501 line too long (86 > 79 characters)
./authentication/models.py:192:80: E501 line too long (80 > 79 characters)
./authentication/models.py:202:80: E501 line too long (92 > 79 characters)
./authentication/models.py:219:80: E501 line too long (89 > 79 characters)
./authentication/models.py:235:80: E501 line too long (96 > 79 characters)
./authentication/models.py:270:80: E501 line too long (101 > 79 characters)
./authentication/models.py:275:80: E501 line too long (94 > 79 characters)
./authentication/models.py:288:80: E501 line too long (117 > 79 characters)
./authentication/models.py:291:80: E501 line too long (86 > 79 characters)
./authentication/models.py:306:80: E501 line too long (92 > 79 characters)
./authentication/models.py:307:80: E501 line too long (81 > 79 characters)
./authentication/models.py:311:80: E501 line too long (115 > 79 characters)
./authentication/serializers.py:37:80: E501 line too long (114 > 79 characters)
./authentication/serializers.py:42:80: E501 line too long (119 > 79 characters)
./authentication/serializers.py:60:80: E501 line too long (94 > 79 characters)
./authentication/serializers.py:133:80: E501 line too long (95 > 79 characters)
./authentication/serializers.py:136:80: E501 line too long (102 > 79 characters)
./authentication/serializers.py:156:80: E501 line too long (91 > 79 characters)
./authentication/serializers.py:168:80: E501 line too long (112 > 79 characters)
./authentication/serializers.py:171:80: E501 line too long (88 > 79 characters)
./authentication/serializers.py:174:80: E501 line too long (108 > 79 characters)
./authentication/serializers.py:176:80: E501 line too long (113 > 79 characters)
./authentication/serializers.py:178:80: E501 line too long (88 > 79 characters)
./authentication/serializers.py:188:80: E501 line too long (92 > 79 characters)
./authentication/serializers.py:199:80: E501 line too long (105 > 79 characters)
./authentication/serializers.py:211:80: E501 line too long (109 > 79 characters)
./authentication/serializers.py:228:80: E501 line too long (102 > 79 characters)
./authentication/serializers.py:232:80: E501 line too long (91 > 79 characters)
./authentication/serializers.py:252:80: E501 line too long (81 > 79 characters)
./authentication/serializers.py:264:80: E501 line too long (91 > 79 characters)
./authentication/serializers.py:276:80: E501 line too long (86 > 79 characters)
./authentication/serializers.py:279:80: E501 line too long (107 > 79 characters)
./authentication/serializers.py:321:80: E501 line too long (97 > 79 characters)
./authentication/serializers.py:325:80: E501 line too long (97 > 79 characters)
./authentication/serializers.py:329:80: E501 line too long (99 > 79 characters)
./authentication/urls.py:6:80: E501 line too long (97 > 79 characters)
./authentication/urls.py:8:80: E501 line too long (117 > 79 characters)
./authentication/urls.py:14:80: E501 line too long (80 > 79 characters)
./authentication/urls.py:24:80: E501 line too long (83 > 79 characters)
./authentication/views.py:91:80: E501 line too long (104 > 79 characters)
./authentication/views.py:159:80: E501 line too long (101 > 79 characters)
./authentication/views.py:163:80: E501 line too long (85 > 79 characters)
./authentication/views.py:166:80: E501 line too long (114 > 79 characters)
./authentication/views.py:182:80: E501 line too long (86 > 79 characters)
./authentication/views.py:187:80: E501 line too long (91 > 79 characters)
./authentication/views.py:203:80: E501 line too long (106 > 79 characters)
./authentication/views.py:206:80: E501 line too long (118 > 79 characters)
./authentication/views.py:209:80: E501 line too long (106 > 79 characters)
./authentication/views.py:235:80: E501 line too long (115 > 79 characters)
./authentication/views.py:251:80: E501 line too long (116 > 79 characters)
./authentication/views.py:290:80: E501 line too long (102 > 79 characters)
./authentication/views.py:337:80: E501 line too long (95 > 79 characters)
./authentication/views.py:338:80: E501 line too long (95 > 79 characters)
./authentication/views.py:355:80: E501 line too long (105 > 79 characters)
./authentication/views.py:361:80: E501 line too long (97 > 79 characters)
./authentication/views.py:394:80: E501 line too long (94 > 79 characters)
./authentication/views.py:404:80: E501 line too long (92 > 79 characters)
./authentication/views.py:418:80: E501 line too long (107 > 79 characters)
./authentication/views.py:463:80: E501 line too long (92 > 79 characters)
./sales_notes/exception_handler.py:4:1: F401 'rest_framework.response.Response' imported but unused
./sales_notes/exception_handler.py:45:80: E501 line too long (103 > 79 characters)
./sales_notes/exception_handler.py:59:80: E501 line too long (89 > 79 characters)
./sales_notes/existing_models.py:14:80: E501 line too long (87 > 79 characters)
./sales_notes/existing_models.py:15:80: E501 line too long (83 > 79 characters)
./sales_notes/existing_models.py:16:80: E501 line too long (112 > 79 characters)
./sales_notes/existing_models.py:17:80: E501 line too long (114 > 79 characters)
./sales_notes/existing_models.py:20:80: E501 line too long (114 > 79 characters)
./sales_notes/existing_models.py:21:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:38:80: E501 line too long (93 > 79 characters)
./sales_notes/existing_models.py:39:80: E501 line too long (81 > 79 characters)
./sales_notes/existing_models.py:40:80: E501 line too long (98 > 79 characters)
./sales_notes/existing_models.py:41:80: E501 line too long (98 > 79 characters)
./sales_notes/existing_models.py:42:80: E501 line too long (98 > 79 characters)
./sales_notes/existing_models.py:43:80: E501 line too long (85 > 79 characters)
./sales_notes/existing_models.py:44:80: E501 line too long (87 > 79 characters)
./sales_notes/existing_models.py:45:80: E501 line too long (96 > 79 characters)
./sales_notes/existing_models.py:46:80: E501 line too long (107 > 79 characters)
./sales_notes/existing_models.py:47:80: E501 line too long (93 > 79 characters)
./sales_notes/existing_models.py:48:80: E501 line too long (85 > 79 characters)
./sales_notes/existing_models.py:49:80: E501 line too long (87 > 79 characters)
./sales_notes/existing_models.py:50:80: E501 line too long (85 > 79 characters)
./sales_notes/existing_models.py:51:80: E501 line too long (110 > 79 characters)
./sales_notes/existing_models.py:52:80: E501 line too long (110 > 79 characters)
./sales_notes/existing_models.py:53:80: E501 line too long (105 > 79 characters)
./sales_notes/existing_models.py:54:80: E501 line too long (84 > 79 characters)
./sales_notes/existing_models.py:55:80: E501 line too long (119 > 79 characters)
./sales_notes/existing_models.py:56:80: E501 line too long (119 > 79 characters)
./sales_notes/existing_models.py:57:80: E501 line too long (91 > 79 characters)
./sales_notes/existing_models.py:59:80: E501 line too long (94 > 79 characters)
./sales_notes/existing_models.py:60:80: E501 line too long (87 > 79 characters)
./sales_notes/existing_models.py:61:80: E501 line too long (104 > 79 characters)
./sales_notes/existing_models.py:62:80: E501 line too long (104 > 79 characters)
./sales_notes/existing_models.py:79:80: E501 line too long (88 > 79 characters)
./sales_notes/existing_models.py:80:80: E501 line too long (93 > 79 characters)
./sales_notes/existing_models.py:81:80: E501 line too long (90 > 79 characters)
./sales_notes/existing_models.py:82:80: E501 line too long (86 > 79 characters)
./sales_notes/existing_models.py:83:80: E501 line too long (84 > 79 characters)
./sales_notes/existing_models.py:84:80: E501 line too long (106 > 79 characters)
./sales_notes/existing_models.py:85:80: E501 line too long (83 > 79 characters)
./sales_notes/existing_models.py:86:80: E501 line too long (89 > 79 characters)
./sales_notes/existing_models.py:87:80: E501 line too long (101 > 79 characters)
./sales_notes/existing_models.py:88:80: E501 line too long (83 > 79 characters)
./sales_notes/existing_models.py:90:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:91:80: E501 line too long (98 > 79 characters)
./sales_notes/existing_models.py:92:80: E501 line too long (106 > 79 characters)
./sales_notes/existing_models.py:93:80: E501 line too long (106 > 79 characters)
./sales_notes/existing_models.py:94:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:95:80: E501 line too long (102 > 79 characters)
./sales_notes/existing_models.py:97:80: E501 line too long (88 > 79 characters)
./sales_notes/existing_models.py:99:80: E501 line too long (119 > 79 characters)
./sales_notes/existing_models.py:100:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:101:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:102:80: E501 line too long (90 > 79 characters)
./sales_notes/migrations/0001_initial.py:26:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:28:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:44:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:60:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:62:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:65:80: E501 line too long (120 > 79 characters)
./sales_notes/migrations/0001_initial.py:78:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:80:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:81:80: E501 line too long (99 > 79 characters)
./sales_notes/migrations/0001_initial.py:84:80: E501 line too long (118 > 79 characters)
./sales_notes/migrations/0001_initial.py:88:80: E501 line too long (119 > 79 characters)
./sales_notes/migrations/0001_initial.py:99:80: E501 line too long (108 > 79 characters)
./sales_notes/migrations/0001_initial.py:101:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:102:80: E501 line too long (93 > 79 characters)
./sales_notes/migrations/0001_initial.py:114:80: E501 line too long (95 > 79 characters)
./sales_notes/migrations/0001_initial.py:115:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:116:80: E501 line too long (97 > 79 characters)
./sales_notes/migrations/0001_initial.py:117:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:118:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:119:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:120:80: E501 line too long (101 > 79 characters)
./sales_notes/migrations/0001_initial.py:121:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:122:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:125:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:127:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:128:80: E501 line too long (101 > 79 characters)
./sales_notes/migrations/0001_initial.py:129:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:130:80: E501 line too long (101 > 79 characters)
./sales_notes/migrations/0001_initial.py:133:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:137:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:141:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:143:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:147:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:153:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:156:80: E501 line too long (107 > 79 characters)
./sales_notes/migrations/0001_initial.py:157:80: E501 line too long (94 > 79 characters)
./sales_notes/migrations/0001_initial.py:158:80: E501 line too long (110 > 79 characters)
./sales_notes/migrations/0001_initial.py:159:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:160:80: E501 line too long (120 > 79 characters)
./sales_notes/migrations/0001_initial.py:161:80: E501 line too long (120 > 79 characters)
./sales_notes/migrations/0001_initial.py:162:80: E501 line too long (94 > 79 characters)
./sales_notes/migrations/0001_initial.py:174:80: E501 line too long (95 > 79 characters)
./sales_notes/migrations/0001_initial.py:175:80: E501 line too long (104 > 79 characters)
./sales_notes/migrations/0001_initial.py:176:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:177:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:178:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:179:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:182:80: E501 line too long (104 > 79 characters)
./sales_notes/migrations/0001_initial.py:184:80: E501 line too long (99 > 79 characters)
./sales_notes/migrations/0001_initial.py:185:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:186:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:187:80: E501 line too long (99 > 79 characters)
./sales_notes/migrations/0001_initial.py:188:80: E501 line too long (85 > 79 characters)
./sales_notes/migrations/0001_initial.py:189:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:190:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:193:80: E501 line too long (115 > 79 characters)
./sales_notes/migrations/0001_initial.py:197:80: E501 line too long (115 > 79 characters)
./sales_notes/migrations/0001_initial.py:199:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:200:80: E501 line too long (118 > 79 characters)
./sales_notes/migrations/0001_initial.py:204:80: E501 line too long (104 > 79 characters)
./sales_notes/migrations/0001_initial.py:210:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:213:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:214:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:215:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:216:80: E501 line too long (85 > 79 characters)
./sales_notes/migrations/0001_initial.py:238:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:239:80: E501 line too long (113 > 79 characters)
./sales_notes/migrations/0001_initial.py:240:80: E501 line too long (90 > 79 characters)
./sales_notes/migrations/0001_initial.py:261:80: E501 line too long (119 > 79 characters)
./sales_notes/migrations/0001_initial.py:262:80: E501 line too long (113 > 79 characters)
./sales_notes/migrations/0001_initial.py:263:80: E501 line too long (89 > 79 characters)
./sales_notes/migrations/0001_initial.py:274:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:276:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:279:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:284:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:289:80: E501 line too long (108 > 79 characters)
./sales_notes/migrations/0001_initial.py:290:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:291:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:294:80: E501 line too long (83 > 79 characters)
./sales_notes/migrations/0001_initial.py:298:80: E501 line too long (119 > 79 characters)
./sales_notes/migrations/0001_initial.py:312:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:314:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:317:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:327:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:333:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:334:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:343:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:350:80: E501 line too long (110 > 79 characters)
./sales_notes/migrations/0001_initial.py:354:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:359:80: E501 line too long (107 > 79 characters)
./sales_notes/migrations/0001_initial.py:364:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:368:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:370:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:371:80: E501 line too long (84 > 79 characters)
./sales_notes/migrations/0001_initial.py:372:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:373:80: E501 line too long (111 > 79 characters)
./sales_notes/migrations/0001_initial.py:374:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:375:80: E501 line too long (97 > 79 characters)
./sales_notes/migrations/0001_initial.py:378:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:382:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:386:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:388:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:392:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:396:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:397:80: E501 line too long (99 > 79 characters)
./sales_notes/migrations/0001_initial.py:398:80: E501 line too long (119 > 79 characters)
./sales_notes/migrations/0001_initial.py:399:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:403:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:415:80: E501 line too long (101 > 79 characters)
./sales_notes/migrations/0001_initial.py:420:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:423:80: E501 line too long (101 > 79 characters)
./sales_notes/migrations/0001_initial.py:431:80: E501 line too long (95 > 79 characters)
./sales_notes/migrations/0001_initial.py:442:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:453:80: E501 line too long (96 > 79 characters)
./sales_notes/migrations/0001_initial.py:462:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:471:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:474:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:493:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:497:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:499:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:502:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:545:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:551:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:552:80: E501 line too long (99 > 79 characters)
./sales_notes/migrations/0001_initial.py:555:80: E501 line too long (111 > 79 characters)
./sales_notes/migrations/0001_initial.py:588:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:599:80: E501 line too long (107 > 79 characters)
./sales_notes/migrations/0001_initial.py:607:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:608:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:641:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:645:80: E501 line too long (98 > 79 characters)
./sales_notes/migrations/0001_initial.py:649:80: E501 line too long (115 > 79 characters)
./sales_notes/migrations/0001_initial.py:658:80: E501 line too long (104 > 79 characters)
./sales_notes/migrations/0001_initial.py:663:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:667:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:671:80: E501 line too long (95 > 79 characters)
./sales_notes/migrations/0001_initial.py:675:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:679:80: E501 line too long (107 > 79 characters)
./sales_notes/migrations/0001_initial.py:683:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:687:80: E501 line too long (85 > 79 characters)
./sales_notes/migrations/0002_alter_buque_armador_alter_buque_capitan_and_more.py:26:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0002_alter_buque_armador_alter_buque_capitan_and_more.py:31:80: E501 line too long (107 > 79 characters)
./sales_notes/models.py:34:80: E501 line too long (112 > 79 characters)
./sales_notes/models.py:42:80: E501 line too long (101 > 79 characters)
./sales_notes/models.py:56:80: E501 line too long (112 > 79 characters)
./sales_notes/models.py:78:80: E501 line too long (95 > 79 characters)
./sales_notes/models.py:81:80: E501 line too long (89 > 79 characters)
./sales_notes/models.py:102:80: E501 line too long (91 > 79 characters)
./sales_notes/models.py:111:80: E501 line too long (93 > 79 characters)
./sales_notes/models.py:134:80: E501 line too long (84 > 79 characters)
./sales_notes/models.py:143:80: E501 line too long (90 > 79 characters)
./sales_notes/models.py:146:80: E501 line too long (107 > 79 characters)
./sales_notes/models.py:159:80: E501 line too long (120 > 79 characters)
./sales_notes/models.py:162:80: E501 line too long (119 > 79 characters)
./sales_notes/models.py:177:80: E501 line too long (90 > 79 characters)
./sales_notes/models.py:179:80: E501 line too long (97 > 79 characters)
./sales_notes/models.py:192:80: E501 line too long (94 > 79 characters)
./sales_notes/models.py:195:80: E501 line too long (87 > 79 characters)
./sales_notes/models.py:230:80: E501 line too long (91 > 79 characters)
./sales_notes/models.py:233:80: E501 line too long (100 > 79 characters)
./sales_notes/models.py:235:80: E501 line too long (97 > 79 characters)
./sales_notes/models.py:260:80: E501 line too long (92 > 79 characters)
./sales_notes/models.py:263:80: E501 line too long (103 > 79 characters)
./sales_notes/models.py:265:80: E501 line too long (97 > 79 characters)
./sales_notes/models.py:296:80: E501 line too long (112 > 79 characters)
./sales_notes/models.py:299:80: E501 line too long (108 > 79 characters)
./sales_notes/models.py:302:80: E501 line too long (115 > 79 characters)
./sales_notes/models.py:313:80: E501 line too long (117 > 79 characters)
./sales_notes/models.py:320:80: E501 line too long (90 > 79 characters)
./sales_notes/models.py:323:80: E501 line too long (100 > 79 characters)
./sales_notes/models.py:326:80: E501 line too long (105 > 79 characters)
./sales_notes/models.py:329:80: E501 line too long (111 > 79 characters)
./sales_notes/models.py:331:80: E501 line too long (117 > 79 characters)
./sales_notes/models.py:334:80: E501 line too long (112 > 79 characters)
./sales_notes/models.py:336:80: E501 line too long (116 > 79 characters)
./sales_notes/models.py:338:80: E501 line too long (100 > 79 characters)
./sales_notes/models.py:342:80: E501 line too long (96 > 79 characters)
./sales_notes/models.py:344:80: E501 line too long (95 > 79 characters)
./sales_notes/models.py:347:80: E501 line too long (87 > 79 characters)
./sales_notes/models.py:349:80: E501 line too long (81 > 79 characters)
./sales_notes/models.py:351:80: E501 line too long (106 > 79 characters)
./sales_notes/models.py:354:80: E501 line too long (110 > 79 characters)
./sales_notes/models.py:356:80: E501 line too long (112 > 79 characters)
./sales_notes/models.py:358:80: E501 line too long (98 > 79 characters)
./sales_notes/models.py:369:80: E501 line too long (82 > 79 characters)
./sales_notes/models.py:372:80: E501 line too long (98 > 79 characters)
./sales_notes/models.py:374:80: E501 line too long (83 > 79 characters)
./sales_notes/models.py:376:80: E501 line too long (103 > 79 characters)
./sales_notes/models.py:379:80: E501 line too long (101 > 79 characters)
./sales_notes/models.py:382:80: E501 line too long (84 > 79 characters)
./sales_notes/models.py:385:80: E501 line too long (117 > 79 characters)
./sales_notes/models.py:387:80: E501 line too long (114 > 79 characters)
./sales_notes/models.py:390:80: E501 line too long (86 > 79 characters)
./sales_notes/models.py:392:80: E501 line too long (106 > 79 characters)
./sales_notes/models.py:396:80: E501 line too long (112 > 79 characters)
./sales_notes/models.py:399:80: E501 line too long (118 > 79 characters)
./sales_notes/models.py:401:80: E501 line too long (104 > 79 characters)
./sales_notes/models.py:406:80: E501 line too long (118 > 79 characters)
./sales_notes/models.py:410:80: E501 line too long (96 > 79 characters)
./sales_notes/models.py:414:80: E501 line too long (94 > 79 characters)
./sales_notes/models.py:417:80: E501 line too long (98 > 79 characters)
./sales_notes/models.py:430:80: E501 line too long (91 > 79 characters)
./sales_notes/models.py:433:80: E501 line too long (115 > 79 characters)
./sales_notes/models.py:436:80: E501 line too long (106 > 79 characters)
./sales_notes/models.py:438:80: E501 line too long (86 > 79 characters)
./sales_notes/models.py:440:80: E501 line too long (108 > 79 characters)
./sales_notes/models.py:451:80: E501 line too long (109 > 79 characters)
./sales_notes/models.py:472:80: E501 line too long (80 > 79 characters)
./sales_notes/models.py:489:80: E501 line too long (97 > 79 characters)
./sales_notes/models.py:491:80: E501 line too long (83 > 79 characters)
./sales_notes/models.py:493:80: E501 line too long (114 > 79 characters)
./sales_notes/permissions.py:24:80: E501 line too long (100 > 79 characters)
./sales_notes/permissions.py:65:80: E501 line too long (83 > 79 characters)
./sales_notes/permissions.py:68:80: E501 line too long (97 > 79 characters)
./sales_notes/permissions.py:85:80: E501 line too long (97 > 79 characters)
./sales_notes/serializers.py:39:80: E501 line too long (110 > 79 characters)
./sales_notes/serializers.py:98:80: E501 line too long (103 > 79 characters)
./sales_notes/serializers.py:104:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:118:80: E501 line too long (104 > 79 characters)
./sales_notes/serializers.py:120:80: E501 line too long (81 > 79 characters)
./sales_notes/serializers.py:123:80: E501 line too long (114 > 79 characters)
./sales_notes/serializers.py:133:80: E501 line too long (106 > 79 characters)
./sales_notes/serializers.py:138:80: E501 line too long (117 > 79 characters)
./sales_notes/serializers.py:152:80: E501 line too long (89 > 79 characters)
./sales_notes/serializers.py:166:80: E501 line too long (83 > 79 characters)
./sales_notes/serializers.py:183:80: E501 line too long (80 > 79 characters)
./sales_notes/serializers.py:196:80: E501 line too long (115 > 79 characters)
./sales_notes/serializers.py:199:80: E501 line too long (111 > 79 characters)
./sales_notes/serializers.py:202:80: E501 line too long (112 > 79 characters)
./sales_notes/serializers.py:205:80: E501 line too long (108 > 79 characters)
./sales_notes/serializers.py:209:80: E501 line too long (99 > 79 characters)
./sales_notes/serializers.py:240:80: E501 line too long (90 > 79 characters)
./sales_notes/serializers.py:245:80: E501 line too long (86 > 79 characters)
./sales_notes/serializers.py:263:80: E501 line too long (115 > 79 characters)
./sales_notes/serializers.py:272:80: E501 line too long (105 > 79 characters)
./sales_notes/serializers.py:282:80: E501 line too long (113 > 79 characters)
./sales_notes/serializers.py:296:80: E501 line too long (88 > 79 characters)
./sales_notes/serializers.py:301:80: E501 line too long (96 > 79 characters)
./sales_notes/serializers.py:307:80: E501 line too long (119 > 79 characters)
./sales_notes/serializers.py:315:80: E501 line too long (92 > 79 characters)
./sales_notes/serializers.py:326:80: E501 line too long (95 > 79 characters)
./sales_notes/serializers.py:343:80: E501 line too long (96 > 79 characters)
./sales_notes/serializers.py:345:80: E501 line too long (85 > 79 characters)
./sales_notes/serializers.py:350:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:352:80: E501 line too long (106 > 79 characters)
./sales_notes/serializers.py:354:80: E501 line too long (99 > 79 characters)
./sales_notes/serializers.py:365:80: E501 line too long (119 > 79 characters)
./sales_notes/serializers.py:369:80: E501 line too long (94 > 79 characters)
./sales_notes/serializers.py:371:80: E501 line too long (92 > 79 characters)
./sales_notes/serializers.py:421:80: E501 line too long (89 > 79 characters)
./sales_notes/serializers.py:429:80: E501 line too long (92 > 79 characters)
./sales_notes/serializers.py:439:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:466:80: E501 line too long (83 > 79 characters)
./sales_notes/serializers.py:484:80: E501 line too long (80 > 79 characters)
./sales_notes/serializers.py:509:80: E501 line too long (81 > 79 characters)
./sales_notes/serializers.py:512:80: E501 line too long (116 > 79 characters)
./sales_notes/serializers.py:566:80: E501 line too long (104 > 79 characters)
./sales_notes/tasks.py:27:80: E501 line too long (112 > 79 characters)
./sales_notes/tasks.py:33:80: E501 line too long (90 > 79 characters)
./sales_notes/tasks.py:49:80: E501 line too long (106 > 79 characters)
./sales_notes/views.py:14:80: E501 line too long (106 > 79 characters)
./sales_notes/views.py:81:80: E501 line too long (81 > 79 characters)
./sales_notes/views.py:95:80: E501 line too long (90 > 79 characters)
./sales_notes/views.py:100:80: E501 line too long (100 > 79 characters)
./sales_notes/views.py:104:80: E501 line too long (107 > 79 characters)
./sales_notes/views.py:106:80: E501 line too long (114 > 79 characters)
./sales_notes/views.py:114:80: E501 line too long (87 > 79 characters)
./sales_notes/views.py:120:80: E501 line too long (86 > 79 characters)
./sales_notes/views.py:123:80: E501 line too long (89 > 79 characters)
./sales_notes/views.py:161:80: E501 line too long (81 > 79 characters)
./sales_notes/views.py:180:80: E501 line too long (86 > 79 characters)
./tests/conftest.py:9:1: F401 'django.conf.settings' imported but unused
./tests/conftest.py:184:27: F811 redefinition of unused 'settings' from line 9
./tests/conftest.py:219:80: E501 line too long (86 > 79 characters)
./tests/conftest.py:370:80: E501 line too long (101 > 79 characters)
./tests/conftest.py:373:80: E501 line too long (101 > 79 characters)
./tests/conftest.py:378:80: E501 line too long (102 > 79 characters)
./tests/conftest.py:381:80: E501 line too long (85 > 79 characters)
./tests/conftest.py:391:80: E501 line too long (82 > 79 characters)
./tests/conftest.py:412:80: E501 line too long (97 > 79 characters)
./tests/conftest.py:450:80: E501 line too long (81 > 79 characters)
./tests/conftest.py:457:80: E501 line too long (81 > 79 characters)
./tests/conftest.py:465:80: E501 line too long (83 > 79 characters)
./tests/conftest.py:479:36: F811 redefinition of unused 'settings' from line 9
./tests/conftest.py:490:26: F811 redefinition of unused 'settings' from line 9
./tests/integration/test_darp_batch.py:6:1: F401 'django.db.transaction' imported but unused
./tests/integration/test_darp_batch.py:14:80: E501 line too long (100 > 79 characters)
./tests/integration/test_darp_batch.py:25:80: E501 line too long (120 > 79 characters)
./tests/integration/test_darp_batch.py:42:80: E501 line too long (80 > 79 characters)
./tests/integration/test_darp_batch.py:61:80: E501 line too long (108 > 79 characters)
./tests/integration/test_darp_batch.py:64:80: E501 line too long (99 > 79 characters)
./tests/integration/test_sales_notes_flow.py:13:80: E501 line too long (91 > 79 characters)
./tests/integration/test_sales_notes_flow.py:19:80: E501 line too long (93 > 79 characters)
./tests/integration/test_sales_notes_flow.py:40:80: E501 line too long (96 > 79 characters)
./tests/integration/test_sales_notes_flow.py:56:80: E501 line too long (105 > 79 characters)
./tests/integration/test_sales_notes_flow.py:61:80: E501 line too long (101 > 79 characters)
./tests/integration/test_sales_notes_flow.py:66:80: E501 line too long (91 > 79 characters)
./tests/integration/test_sales_notes_flow.py:112:80: E501 line too long (99 > 79 characters)
./tests/integration/test_sales_notes_flow.py:115:80: E501 line too long (102 > 79 characters)
./tests/integration/test_sales_notes_flow.py:120:80: E501 line too long (81 > 79 characters)
./tests/integration/test_sales_notes_flow.py:126:80: E501 line too long (88 > 79 characters)
./tests/integration/test_sales_notes_flow.py:131:80: E501 line too long (102 > 79 characters)
./tests/integration/test_sales_notes_flow.py:132:80: E501 line too long (91 > 79 characters)
./tests/integration/test_sales_notes_flow.py:136:80: E501 line too long (86 > 79 characters)
./tests/integration/test_sales_notes_flow.py:163:80: E501 line too long (96 > 79 characters)
./tests/integration/test_sales_notes_flow.py:173:80: E501 line too long (92 > 79 characters)
./tests/integration/test_sales_notes_flow.py:175:80: E501 line too long (84 > 79 characters)
./tests/security/test_owasp_api_security.py:16:80: E501 line too long (87 > 79 characters)
./tests/security/test_owasp_api_security.py:23:80: E501 line too long (93 > 79 characters)
./tests/security/test_owasp_api_security.py:33:13: F841 local variable 'response' is assigned to but never used
./tests/security/test_owasp_api_security.py:54:54: E712 comparison to False should be 'if cond is False:' or 'if not cond:'
./tests/security/test_owasp_api_security.py:55:50: E712 comparison to False should be 'if cond is False:' or 'if not cond:'
./tests/security/test_owasp_api_security.py:71:80: E501 line too long (114 > 79 characters)
./tests/security/test_owasp_api_security.py:81:80: E501 line too long (89 > 79 characters)
./tests/security/test_owasp_api_security.py:85:80: E501 line too long (107 > 79 characters)
./tests/security/test_owasp_api_security.py:99:80: E501 line too long (120 > 79 characters)
./tests/security/test_owasp_api_security.py:107:80: E501 line too long (114 > 79 characters)
./tests/security/test_owasp_api_security.py:130:80: E501 line too long (82 > 79 characters)
./tests/security/test_owasp_api_security.py:134:80: E501 line too long (117 > 79 characters)
./tests/security/test_owasp_api_security.py:148:80: E501 line too long (80 > 79 characters)
./tests/security/test_owasp_api_security.py:185:9: F841 local variable 'client' is assigned to but never used
./tests/security/test_owasp_api_security.py:197:80: E501 line too long (103 > 79 characters)
./tests/security/test_owasp_api_security.py:203:80: E501 line too long (102 > 79 characters)
./tests/security/test_owasp_api_security.py:209:80: E501 line too long (91 > 79 characters)
./tests/security/test_owasp_api_security.py:214:13: F841 local variable 'response' is assigned to but never used
./tests/security/test_owasp_api_security.py:214:80: E501 line too long (106 > 79 characters)
./tests/unit/test_audit.py:21:80: E501 line too long (116 > 79 characters)
./tests/unit/test_audit.py:56:80: E501 line too long (109 > 79 characters)
./tests/unit/test_audit.py:58:80: E501 line too long (108 > 79 characters)
./tests/unit/test_audit.py:107:80: E501 line too long (93 > 79 characters)
./tests/unit/test_audit.py:123:80: E501 line too long (103 > 79 characters)
./tests/unit/test_audit.py:127:80: E501 line too long (90 > 79 characters)
./tests/unit/test_audit.py:129:80: E501 line too long (80 > 79 characters)
./tests/unit/test_audit.py:145:80: E501 line too long (115 > 79 characters)
./tests/unit/test_audit.py:150:80: E501 line too long (119 > 79 characters)
./tests/unit/test_audit.py:170:80: E501 line too long (97 > 79 characters)
./tests/unit/test_audit.py:190:80: E501 line too long (112 > 79 characters)
./tests/unit/test_audit.py:196:80: E501 line too long (91 > 79 characters)
./tests/unit/test_audit.py:202:80: E501 line too long (108 > 79 characters)
./tests/unit/test_audit.py:204:80: E501 line too long (106 > 79 characters)
./tests/unit/test_audit.py:209:80: E501 line too long (88 > 79 characters)
./tests/unit/test_authentication.py:47:80: E501 line too long (81 > 79 characters)
./tests/unit/test_authentication.py:65:80: E501 line too long (81 > 79 characters)
./tests/unit/test_authentication.py:84:80: E501 line too long (84 > 79 characters)
./tests/unit/test_authentication.py:91:80: E501 line too long (86 > 79 characters)
./tests/unit/test_exception_handler.py:78:80: E501 line too long (91 > 79 characters)
./tests/unit/test_models.py:3:1: F401 'django.core.exceptions.ValidationError' imported but unused
./tests/unit/test_models.py:5:1: F401 'sales_notes.models.Buque' imported but unused
./tests/unit/test_models.py:12:80: E501 line too long (99 > 79 characters)
./tests/unit/test_models.py:14:32: E712 comparison to False should be 'if cond is False:' or 'if not cond:'
./tests/unit/test_models.py:18:80: E501 line too long (91 > 79 characters)
./tests/unit/test_models.py:21:80: E501 line too long (95 > 79 characters)
./tests/unit/test_permissions.py:30:80: E501 line too long (97 > 79 characters)
./tests/unit/test_permissions.py:34:80: E501 line too long (87 > 79 characters)
./tests/unit/test_permissions.py:48:80: E501 line too long (90 > 79 characters)
./tests/unit/test_permissions.py:58:80: E501 line too long (90 > 79 characters)
./tests/unit/test_permissions.py:78:80: E501 line too long (82 > 79 characters)
./tests/unit/test_permissions.py:88:80: E501 line too long (93 > 79 characters)
./tests/unit/test_sales_notes_permissions.py:2:1: F401 'django.contrib.auth.models.Group' imported but unused
./tests/unit/test_sales_notes_permissions.py:6:80: E501 line too long (92 > 79 characters)
./tests/unit/test_sales_notes_permissions.py:116:80: E501 line too long (99 > 79 characters)
./tests/unit/test_sales_notes_permissions.py:125:80: E501 line too long (99 > 79 characters)
./tests/unit/test_sales_notes_permissions.py:132:80: E501 line too long (81 > 79 characters)
./tests/unit/test_sales_notes_permissions.py:134:80: E501 line too long (99 > 79 characters)
./tests/unit/test_sales_notes_permissions.py:141:80: E501 line too long (86 > 79 characters)
./tests/unit/test_sales_notes_permissions.py:143:80: E501 line too long (99 > 79 characters)
./tests/unit/test_serializers.py:257:80: E501 line too long (106 > 79 characters)
./tests/unit/test_serializers.py:299:80: E501 line too long (120 > 79 characters)
./tests/unit/test_serializers.py:320:80: E501 line too long (116 > 79 characters)
./tests/unit/test_serializers.py:418:80: E501 line too long (91 > 79 characters)
./tests/unit/test_serializers.py:430:80: E501 line too long (82 > 79 characters)
./tests/unit/test_serializers.py:446:80: E501 line too long (82 > 79 characters)
./tests/unit/test_serializers.py:452:80: E501 line too long (99 > 79 characters)
./tests/unit/test_serializers.py:471:80: E501 line too long (99 > 79 characters)
./tests/unit/test_serializers.py:472:80: E501 line too long (94 > 79 characters)
./tests/unit/test_serializers.py:473:80: E501 line too long (94 > 79 characters)
./tests/unit/test_serializers.py:490:80: E501 line too long (104 > 79 characters)
./tests/unit/test_serializers.py:508:80: E501 line too long (90 > 79 characters)
./tests/unit/test_serializers.py:538:80: E501 line too long (103 > 79 characters)
./tests/unit/test_serializers.py:571:80: E501 line too long (105 > 79 characters)
./tests/unit/test_serializers.py:573:80: E501 line too long (82 > 79 characters)
./tests/unit/test_tasks.py:19:80: E501 line too long (94 > 79 characters)
./tests/unit/test_tasks.py:36:80: E501 line too long (107 > 79 characters)
./tests/unit/test_views.py:117:80: E501 line too long (81 > 79 characters)
./tests/unit/test_views.py:124:80: E501 line too long (87 > 79 characters)
./tests/unit/test_views.py:125:80: E501 line too long (82 > 79 characters)
./tests/unit/test_views.py:129:80: E501 line too long (95 > 79 characters)
./tests/unit/test_views.py:130:80: E501 line too long (95 > 79 characters)
./validate_vcpe_schema.py:12:1: F401 'jsonschema' imported but unused
./validate_vcpe_schema.py:13:1: F401 'jsonschema.validate' imported but unused
./validate_vcpe_schema.py:32:80: E501 line too long (82 > 79 characters)
./validate_vcpe_schema.py:84:80: E501 line too long (90 > 79 characters)
./validate_vcpe_schema.py:85:80: E501 line too long (87 > 79 characters)
./validate_vcpe_schema.py:86:80: E501 line too long (80 > 79 characters)
./validate_vcpe_schema.py:90:80: E501 line too long (97 > 79 characters)
./validate_vcpe_schema.py:98:80: E501 line too long (111 > 79 characters)
./validate_vcpe_schema.py:104:80: E501 line too long (111 > 79 characters)
./validate_vcpe_schema.py:110:80: E501 line too long (114 > 79 characters)
./validate_vcpe_schema.py:142:80: E501 line too long (80 > 79 characters)
./validate_vcpe_schema.py:152:80: E501 line too long (104 > 79 characters)
./validate_vcpe_schema.py:189:80: E501 line too long (94 > 79 characters)
./validate_vcpe_schema.py:205:80: E501 line too long (120 > 79 characters)
./validate_vcpe_schema.py:224:80: E501 line too long (110 > 79 characters)
./validate_vcpe_schema.py:241:80: E501 line too long (102 > 79 characters)
./validate_vcpe_schema.py:311:11: F541 f-string is missing placeholders
./validate_vcpe_schema.py:312:11: F541 f-string is missing placeholders
./vcpe_api/settings.py:3:80: E501 line too long (84 > 79 characters)
./vcpe_api/settings.py:67:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:130:80: E501 line too long (91 > 79 characters)
./vcpe_api/settings.py:133:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:139:80: E501 line too long (82 > 79 characters)
./vcpe_api/settings.py:142:80: E501 line too long (83 > 79 characters)
./vcpe_api/settings.py:178:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:181:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:191:80: E501 line too long (97 > 79 characters)
./vcpe_api/settings.py:192:80: E501 line too long (92 > 79 characters)
./vcpe_api/settings.py:208:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:238:80: E501 line too long (88 > 79 characters)
./vcpe_api/settings.py:276:80: E501 line too long (93 > 79 characters)
./vcpe_api/settings_production.py:89:80: E501 line too long (86 > 79 characters)
./vcpe_api/settings_production.py:92:80: E501 line too long (82 > 79 characters)
./vcpe_api/settings_production.py:224:80: E501 line too long (84 > 79 characters)
./vcpe_api/urls.py:7:80: E501 line too long (98 > 79 characters)
./vcpe_api/urls.py:19:80: E501 line too long (82 > 79 characters)
./vcpe_api/urls.py:23:80: E501 line too long (92 > 79 characters)
./vcpe_api/urls.py:24:80: E501 line too long (86 > 79 characters)
723   E501 line too long (80 > 79 characters)
3     E712 comparison to False should be 'if cond is False:' or 'if not cond:'
1     E722 do not use bare 'except'
10    F401 'audit.signals' imported but unused
4     F541 f-string is missing placeholders
3     F811 redefinition of unused 'settings' from line 9
3     F841 local variable 'response' is assigned to but never used
747


```


**Resultat:** ✅ Completat correctament

---

*Report generat automàticament per run_all_tests_with_report.sh*
*Data: 26/11/2025 13:48:09*
*TFM Ciberseguretat i Privadesa - ICATMAR*
