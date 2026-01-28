# 📋 Report Consolidat de Tests - VCPE API

**Data d'execució:** 15/01/2026 13:21:16
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


NAME                 IMAGE                    COMMAND                  SERVICE         CREATED      STATUS                PORTS
vcpe_api             api_dev-api              "python manage.py ru…"   api             9 days ago   Up 3 days (healthy)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
vcpe_celery_beat     api_dev-celery_beat      "celery -A vcpe_api …"   celery_beat     9 days ago   Up 3 days (healthy)   8000/tcp
vcpe_celery_worker   api_dev-celery_worker    "celery -A vcpe_api …"   celery_worker   9 days ago   Up 3 days (healthy)   8000/tcp
vcpe_postgres        postgis/postgis:16-3.4   "docker-entrypoint.s…"   db              9 days ago   Up 3 days (healthy)   0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp
vcpe_redis           redis:7.4-alpine         "docker-entrypoint.s…"   redis           9 days ago   Up 3 days (healthy)   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp


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


**Resultat:** ❌ Error obtenint token


**Error:** Assegura't que l'usuari admin_test existeix


### 2.3 Accés sense Token (ha de fallar amb 401)


**Temps d'execució:** 0s


```


{"detail":"Credencials d'autenticació no disponibles."}
401


```


**Resultat:** ✅ Completat correctament


## 3. Tests Automatitzats (Pytest)


### 3.1 Tests Unitaris


**Temps d'execució:** 9s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
django: version: 5.1.13, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.2.0
collecting ... collected 103 items

tests/unit/test_audit.py::TestAuditLog::test_audit_log_creation PASSED   [  0%]
tests/unit/test_audit.py::TestAuditLog::test_audit_log_with_old_new_values PASSED [  1%]
tests/unit/test_audit.py::TestAuditLog::test_audit_log_without_user PASSED [  2%]
tests/unit/test_audit.py::TestAuditLog::test_audit_log_ordering PASSED   [  3%]
tests/unit/test_audit.py::TestSecurityEvent::test_security_event_creation PASSED [  4%]
tests/unit/test_audit.py::TestSecurityEvent::test_security_event_with_user PASSED [  5%]
tests/unit/test_audit.py::TestAuditSignals::test_envio_creation_generates_audit_log PASSED [  6%]
tests/unit/test_audit.py::TestAuditSignals::test_failed_login_generates_audit_log PASSED [  7%]
tests/unit/test_audit.py::TestAuditSignals::test_successful_login_resets_failures FAILED [  8%]
tests/unit/test_audit.py::TestAuditSignals::test_failed_login_for_nonexistent_user_logs_warning PASSED [  9%]
tests/unit/test_audit.py::TestAuditSignals::test_envio_deleted_generates_critical_log PASSED [ 10%]
tests/unit/test_audit.py::TestAuditTasks::test_cleanup_old_logs_deletes_old_info_logs PASSED [ 11%]
tests/unit/test_audit.py::TestAuditTasks::test_cleanup_old_logs_keeps_critical_logs PASSED [ 12%]
tests/unit/test_audit.py::TestAuditTasks::test_check_security_events_detects_brute_force PASSED [ 13%]
tests/unit/test_audit.py::TestAuditTasks::test_check_security_events_detects_injections PASSED [ 14%]
tests/unit/test_audit.py::TestAuditTasks::test_check_security_events_no_alerts_when_empty PASSED [ 15%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_success PASSED [ 16%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_invalid_credentials PASSED [ 17%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_refresh_token_success PASSED [ 18%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_verify_token_success PASSED [ 19%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_access_protected_endpoint_without_token PASSED [ 20%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_access_protected_endpoint_with_valid_token PASSED [ 21%]
tests/unit/test_exception_handler.py::TestCustomExceptionHandler::test_exception_handler_with_none_response PASSED [ 22%]
tests/unit/test_exception_handler.py::TestCustomExceptionHandler::test_exception_handler_with_validation_error PASSED [ 23%]
tests/unit/test_exception_handler.py::TestCustomExceptionHandler::test_exception_handler_with_not_found PASSED [ 24%]
tests/unit/test_exception_handler.py::TestCustomExceptionHandler::test_exception_handler_with_server_error PASSED [ 25%]
tests/unit/test_exception_handler.py::TestCustomExceptionHandler::test_exception_handler_with_request_id PASSED [ 26%]
tests/unit/test_exception_handler.py::TestCustomExceptionHandler::test_exception_handler_without_request PASSED [ 27%]
tests/unit/test_models.py::TestEnvioModel::test_create_envio_valid PASSED [ 28%]
tests/unit/test_models.py::TestEnvioModel::test_num_envio_unique PASSED  [ 29%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_create_envio PASSED [ 30%]
tests/unit/test_permissions.py::TestUserPermissions::test_investigador_cannot_create_envio PASSED [ 31%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_list_own_envios PASSED [ 32%]
tests/unit/test_permissions.py::TestUserPermissions::test_investigador_can_list_all_envios PASSED [ 33%]
tests/unit/test_permissions.py::TestUserPermissions::test_admin_can_list_all_envios PASSED [ 33%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_retrieve_own_envio PASSED [ 34%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_cannot_retrieve_other_envio PASSED [ 35%]
tests/unit/test_permissions.py::TestUserPermissions::test_investigador_can_retrieve_any_envio PASSED [ 36%]
tests/unit/test_permissions.py::TestUserPermissions::test_unauthenticated_cannot_access PASSED [ 37%]
tests/unit/test_sales_notes_permissions.py::TestIsDARP::test_darp_user_has_permission PASSED [ 38%]
tests/unit/test_sales_notes_permissions.py::TestIsDARP::test_investigador_no_permission PASSED [ 39%]
tests/unit/test_sales_notes_permissions.py::TestIsDARP::test_unauthenticated_no_permission PASSED [ 40%]
tests/unit/test_sales_notes_permissions.py::TestIsInvestigador::test_investigador_has_permission PASSED [ 41%]
tests/unit/test_sales_notes_permissions.py::TestIsInvestigador::test_darp_no_investigador_permission PASSED [ 42%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_admin_full_access PASSED [ 43%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_darp_can_post PASSED [ 44%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_darp_can_get PASSED [ 45%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_investigador_can_get PASSED [ 46%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_investigador_cannot_post PASSED [ 47%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_investigador_cannot_put PASSED [ 48%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_darp_can_access_own_envio PASSED [ 49%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_darp_cannot_access_other_envio PASSED [ 50%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_investigador_can_read_any_envio PASSED [ 51%]
tests/unit/test_sales_notes_permissions.py::TestDARPCanCreateInvestigadorCanRead::test_investigador_cannot_modify_any_envio PASSED [ 52%]
tests/unit/test_serializers.py::TestFechaCapturaSerializer::test_valid_fecha_captura PASSED [ 53%]
tests/unit/test_serializers.py::TestFechaCapturaSerializer::test_fecha_captura_solo_inicio PASSED [ 54%]
tests/unit/test_serializers.py::TestFechaCapturaSerializer::test_fecha_fin_anterior_a_inicio_error PASSED [ 55%]
tests/unit/test_serializers.py::TestFechaCapturaSerializer::test_fechas_iguales_valido PASSED [ 56%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_especie_valida_completa PASSED [ 57%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_especie_al3_formato_invalido PASSED [ 58%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_especie_al3_con_numeros_invalido PASSED [ 59%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_especie_al3_uppercase PASSED [ 60%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_cantidad_negativa_invalida PASSED [ 61%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_cantidad_cero_invalida PASSED [ 62%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_precio_negativo_invalido PASSED [ 63%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_precio_cero_valido PASSED [ 64%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_retirada_con_destino_valido PASSED [ 65%]
tests/unit/test_serializers.py::TestEspecieSerializer::test_especie_con_fechas_captura PASSED [ 66%]
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

=================================== FAILURES ===================================
____________ TestAuditSignals.test_successful_login_resets_failures ____________
tests/unit/test_audit.py:166: in test_successful_login_resets_failures
    assert api_user.failed_login_attempts == 0
E   assert 3 == 0
E    +  where 3 = <APIUser: apiuser - API Test Org>.failed_login_attempts
----------------------------- Captured stderr call -----------------------------
ERROR 2026-01-15 13:21:23,560 signals 44321 128589690088320 Error auditant login: 'APIUser' object has no attribute 'reset_failed_login'
Traceback (most recent call last):
  File "/app/audit/signals.py", line 93, in audit_user_login
    user.reset_failed_login()
    ^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'APIUser' object has no attribute 'reset_failed_login'. Did you mean: 'last_failed_login'?

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     26  70.45%   36, 77-78, 84-102, 108, 119-120, 140-141, 152, 166-192
audit/models.py                                               79      3  96.20%   82, 173, 217
audit/signals.py                                              77     15  80.52%   36-37, 71-72, 94-96, 104-114, 169-170, 187-188
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
sales_notes/encrypted_fields.py                               90     14  84.44%   30, 42, 51-53, 92, 114, 128, 136, 143, 146-149
sales_notes/exception_handler.py                              19      0 100.00%
sales_notes/existing_models.py                                87      3  96.55%   31, 72, 112
sales_notes/models.py                                        201     17  91.54%   93, 135, 192-193, 199, 222, 252, 282, 454-455, 476, 481-483, 509-511
sales_notes/permissions.py                                    30      5  83.33%   39, 57, 72, 78, 89
sales_notes/serializers.py                                   273     38  86.08%   116, 122, 128, 136, 140-141, 156, 170, 184, 217, 220, 226, 255-258, 266, 290, 319, 325, 386-392, 415-419, 441, 487-494, 529, 575
sales_notes/tasks.py                                          27      0 100.00%
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                         104     33  68.27%   85, 105, 116-152, 188-189
-----------------------------------------------------------------------------------------
TOTAL                                                       1532    335  78.13%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 78.13%
=========================== short test summary info ============================
FAILED tests/unit/test_audit.py::TestAuditSignals::test_successful_login_resets_failures
======================== 1 failed, 102 passed in 7.07s =========================


```


**Resultat:** ✅ Completat correctament


### 3.2 Tests d'Integració


**Temps d'execució:** 9s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
django: version: 5.1.13, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.2.0
collecting ... collected 12 items

tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_submission_success PASSED [  8%]
tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_rate_limiting_batch PASSED [ 16%]
tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_post_success FAILED [ 25%]
tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_post_rollback_on_error FAILED [ 33%]
tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_darp_complete_lifecycle PASSED [ 41%]
tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_investigador_read_only_flow PASSED [ 50%]
tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_filtering_and_search PASSED [ 58%]
tests/integration/test_sales_notes_flow.py::TestAdvancedSalesNotesFlow::test_envio_lifecycle_with_validation PASSED [ 66%]
tests/integration/test_sales_notes_flow.py::TestAdvancedSalesNotesFlow::test_multiple_users_isolation PASSED [ 75%]
tests/integration/test_sales_notes_flow.py::TestAdvancedSalesNotesFlow::test_pagination_and_ordering PASSED [ 83%]
tests/integration/test_sales_notes_flow.py::TestAdvancedSalesNotesFlow::test_invalid_data_returns_detailed_errors PASSED [ 91%]
tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_rollback_on_error PASSED [100%]

=================================== FAILURES ===================================
_______________ TestDARPBatchSubmission.test_batch_post_success ________________
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:105: in _execute
    return self.cursor.execute(sql, params)
/usr/local/lib/python3.12/site-packages/psycopg/cursor.py:97: in execute
    raise ex.with_traceback(None)
E   psycopg.errors.UniqueViolation: duplicate key value violates unique constraint "species_3A_Code_key"
E   DETAIL:  Key ("3A_Code")=(HKE) already exists.

The above exception was the direct cause of the following exception:
tests/integration/test_darp_batch.py:84: in test_batch_post_success
    Species.objects.create(id=21001, code_3a="HKE", scientific_name="Hake")
/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:679: in create
    obj.save(force_insert=True, using=self.db)
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:892: in save
    self.save_base(
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:998: in save_base
    updated = self._save_table(
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:1161: in _save_table
    results = self._do_insert(
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:1202: in _do_insert
    return manager._insert(
/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:1847: in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
/usr/local/lib/python3.12/site-packages/django/db/models/sql/compiler.py:1836: in execute_sql
    cursor.execute(sql, params)
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:79: in execute
    return self._execute_with_wrappers(
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:92: in _execute_with_wrappers
    return executor(sql, params, many, context)
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:100: in _execute
    with self.db.wrap_database_errors:
/usr/local/lib/python3.12/site-packages/django/db/utils.py:91: in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:105: in _execute
    return self.cursor.execute(sql, params)
/usr/local/lib/python3.12/site-packages/psycopg/cursor.py:97: in execute
    raise ex.with_traceback(None)
E   django.db.utils.IntegrityError: duplicate key value violates unique constraint "species_3A_Code_key"
E   DETAIL:  Key ("3A_Code")=(HKE) already exists.
__________ TestDARPBatchSubmission.test_batch_post_rollback_on_error ___________
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:105: in _execute
    return self.cursor.execute(sql, params)
/usr/local/lib/python3.12/site-packages/psycopg/cursor.py:97: in execute
    raise ex.with_traceback(None)
E   psycopg.errors.UniqueViolation: duplicate key value violates unique constraint "species_3A_Code_key"
E   DETAIL:  Key ("3A_Code")=(HKE) already exists.

The above exception was the direct cause of the following exception:
tests/integration/test_darp_batch.py:115: in test_batch_post_rollback_on_error
    Species.objects.create(id=22001, code_3a="HKE", scientific_name="Hake")
/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:679: in create
    obj.save(force_insert=True, using=self.db)
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:892: in save
    self.save_base(
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:998: in save_base
    updated = self._save_table(
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:1161: in _save_table
    results = self._do_insert(
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:1202: in _do_insert
    return manager._insert(
/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:1847: in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
/usr/local/lib/python3.12/site-packages/django/db/models/sql/compiler.py:1836: in execute_sql
    cursor.execute(sql, params)
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:79: in execute
    return self._execute_with_wrappers(
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:92: in _execute_with_wrappers
    return executor(sql, params, many, context)
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:100: in _execute
    with self.db.wrap_database_errors:
/usr/local/lib/python3.12/site-packages/django/db/utils.py:91: in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:105: in _execute
    return self.cursor.execute(sql, params)
/usr/local/lib/python3.12/site-packages/psycopg/cursor.py:97: in execute
    raise ex.with_traceback(None)
E   django.db.utils.IntegrityError: duplicate key value violates unique constraint "species_3A_Code_key"
E   DETAIL:  Key ("3A_Code")=(HKE) already exists.

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
sales_notes/encrypted_fields.py                               90     14  84.44%   30, 42, 51-53, 92, 114, 128, 136, 143, 146-149
sales_notes/exception_handler.py                              19     19   0.00%   1-62
sales_notes/existing_models.py                                87      3  96.55%   31, 72, 112
sales_notes/models.py                                        201     18  91.04%   70, 93, 135, 192-193, 199, 222, 252, 282, 454-455, 476, 481-483, 509-511
sales_notes/permissions.py                                    30     11  63.33%   19-24, 38-43, 57, 61, 72, 78, 89
sales_notes/serializers.py                                   273     58  78.75%   38-41, 116, 122, 128, 135-136, 140-141, 156, 169-171, 183-185, 214-220, 226, 233-236, 255-258, 266, 290, 319, 325, 333, 344, 386-392, 407, 415-419, 441, 487-494, 529
sales_notes/tasks.py                                          27     27   0.00%   5-59
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                         104     34  67.31%   74, 85, 105, 116-152, 188-189
-----------------------------------------------------------------------------------------
TOTAL                                                       1532    472  69.19%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 69.19%
=========================== short test summary info ============================
FAILED tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_post_success
FAILED tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_post_rollback_on_error
========================= 2 failed, 10 passed in 6.37s =========================


```


**Resultat:** ✅ Completat correctament


### 3.3 Tests de Seguretat


**Temps d'execució:** 6s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
django: version: 5.1.13, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.2.0
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
sales_notes/encrypted_fields.py                               90     14  84.44%   30, 42, 51-53, 92, 114, 128, 136, 143, 146-149
sales_notes/exception_handler.py                              19     19   0.00%   1-62
sales_notes/existing_models.py                                87      3  96.55%   31, 72, 112
sales_notes/models.py                                        201     18  91.04%   70, 93, 135, 192-193, 199, 222, 252, 282, 454-455, 476, 481-483, 509-511
sales_notes/permissions.py                                    30     17  43.33%   19-24, 38-43, 57, 61, 65, 72, 77-89
sales_notes/serializers.py                                   273     62  77.29%   38-41, 116, 122, 128, 135-136, 140-141, 156, 169-171, 183-185, 214-220, 226, 233-236, 255-258, 266, 290, 319, 325, 386-392, 407, 415-419, 441, 487-494, 529, 567, 572-576
sales_notes/tasks.py                                          27     27   0.00%   5-59
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                         104     59  43.27%   70-85, 89-93, 105, 116-152, 182-192, 202-207, 221-226
-----------------------------------------------------------------------------------------
TOTAL                                                       1532    507  66.91%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 66.91%

======================== 11 passed, 3 skipped in 3.53s =========================


```


**Resultat:** ✅ Completat correctament


## 4. Cobertura de Codi


### 4.1 Generar Informe de Cobertura


**Temps d'execució:** 14s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0
django: version: 5.1.13, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.2.0
collected 129 items

tests/integration/test_darp_batch.py ..FF                                [  3%]
tests/integration/test_sales_notes_flow.py .......                       [  8%]
tests/security/test_owasp_api_security.py ...s.s.s......                 [ 19%]
tests/unit/test_audit.py ........F.......                                [ 31%]
tests/unit/test_authentication.py ......                                 [ 36%]
tests/unit/test_exception_handler.py ......                              [ 41%]
tests/unit/test_models.py ..                                             [ 42%]
tests/unit/test_permissions.py .........                                 [ 49%]
tests/unit/test_sales_notes_permissions.py ...............               [ 61%]
tests/unit/test_serializers.py .......................................   [ 91%]
tests/unit/test_tasks.py ..                                              [ 93%]
tests/unit/test_views.py ........                                        [ 99%]
tests/integration/test_darp_batch.py .                                   [100%]

=================================== FAILURES ===================================
_______________ TestDARPBatchSubmission.test_batch_post_success ________________

self = <django.db.backends.utils.CursorWrapper object at 0x77eafacd8ef0>
sql = 'INSERT INTO "species" ("Id", "3A_Code", "ScientificName", "CatalanName", "SpanishName", "EnglishName", "Group", "Grou...") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
params = (Int4(21001), 'HKE', 'Hake', None, None, None, ...)
ignored_wrapper_args = (False, {'connection': <DatabaseWrapper vendor='postgresql' alias='default'>, 'cursor': <django.db.backends.utils.CursorWrapper object at 0x77eafacd8ef0>})

    def _execute(self, sql, params, *ignored_wrapper_args):
        # Raise a warning during app initialization (stored_app_configs is only
        # ever set during testing).
        if not apps.ready and not apps.stored_app_configs:
            warnings.warn(self.APPS_NOT_READY_WARNING_MSG, category=RuntimeWarning)
        self.db.validate_no_broken_transaction()
        with self.db.wrap_database_errors:
            if params is None:
                # params default might be backend specific.
                return self.cursor.execute(sql)
            else:
>               return self.cursor.execute(sql, params)

/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:105:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <django.db.backends.postgresql.base.Cursor [closed] [INERROR] (host=db user=vcpe_user database=test_api_segura_bbdd) at 0x77eafb2ad250>
query = 'INSERT INTO "species" ("Id", "3A_Code", "ScientificName", "CatalanName", "SpanishName", "EnglishName", "Group", "Grou...") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
params = (Int4(21001), 'HKE', 'Hake', None, None, None, ...)

    def execute(
        self,
        query: Query,
        params: Params | None = None,
        *,
        prepare: bool | None = None,
        binary: bool | None = None,
    ) -> Self:
        """
        Execute a query or command to the database.
        """
        try:
            with self._conn.lock:
                self._conn.wait(
                    self._execute_gen(query, params, prepare=prepare, binary=binary)
                )
        except e._NO_TRACEBACK as ex:
>           raise ex.with_traceback(None)
E           psycopg.errors.UniqueViolation: duplicate key value violates unique constraint "species_3A_Code_key"
E           DETAIL:  Key ("3A_Code")=(HKE) already exists.

/usr/local/lib/python3.12/site-packages/psycopg/cursor.py:97: UniqueViolation

The above exception was the direct cause of the following exception:

self = <app.tests.integration.test_darp_batch.TestDARPBatchSubmission object at 0x77eafb2a12b0>
darp_client = <rest_framework.test.APIClient object at 0x77eafa9229f0>
sample_sales_note_data = {'EstablecimientosVenta': {'EstablecimientoVenta': [{'NombreEstablecimiento': 'Llotja de Test', 'NumIdentificacionEstablec': 'LLOTJA_TEST', 'Ventas': {'VentasUnidadProductiva': [{...}]}}]}, 'NumEnvio': 'TEST_001', 'TipoRespuesta': 1}

    def test_batch_post_success(self, darp_client, sample_sales_note_data):
        """Enviar una llista (batch) amb diversos enviaments vàlids en una sola POST"""
        from sales_notes.existing_models import Species, Vessel
        from sales_notes.models import Envio

        # Preparar catàleg mínim
>       Species.objects.create(id=21001, code_3a="HKE", scientific_name="Hake")

tests/integration/test_darp_batch.py:84:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:679: in create
    obj.save(force_insert=True, using=self.db)
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:892: in save
    self.save_base(
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:998: in save_base
    updated = self._save_table(
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:1161: in _save_table
    results = self._do_insert(
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:1202: in _do_insert
    return manager._insert(
/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:1847: in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
/usr/local/lib/python3.12/site-packages/django/db/models/sql/compiler.py:1836: in execute_sql
    cursor.execute(sql, params)
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:79: in execute
    return self._execute_with_wrappers(
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:92: in _execute_with_wrappers
    return executor(sql, params, many, context)
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:100: in _execute
    with self.db.wrap_database_errors:
/usr/local/lib/python3.12/site-packages/django/db/utils.py:91: in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:105: in _execute
    return self.cursor.execute(sql, params)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <django.db.backends.postgresql.base.Cursor [closed] [INERROR] (host=db user=vcpe_user database=test_api_segura_bbdd) at 0x77eafb2ad250>
query = 'INSERT INTO "species" ("Id", "3A_Code", "ScientificName", "CatalanName", "SpanishName", "EnglishName", "Group", "Grou...") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
params = (Int4(21001), 'HKE', 'Hake', None, None, None, ...)

    def execute(
        self,
        query: Query,
        params: Params | None = None,
        *,
        prepare: bool | None = None,
        binary: bool | None = None,
    ) -> Self:
        """
        Execute a query or command to the database.
        """
        try:
            with self._conn.lock:
                self._conn.wait(
                    self._execute_gen(query, params, prepare=prepare, binary=binary)
                )
        except e._NO_TRACEBACK as ex:
>           raise ex.with_traceback(None)
E           django.db.utils.IntegrityError: duplicate key value violates unique constraint "species_3A_Code_key"
E           DETAIL:  Key ("3A_Code")=(HKE) already exists.

/usr/local/lib/python3.12/site-packages/psycopg/cursor.py:97: IntegrityError
__________ TestDARPBatchSubmission.test_batch_post_rollback_on_error ___________

self = <django.db.backends.utils.CursorWrapper object at 0x77eafaec18b0>
sql = 'INSERT INTO "species" ("Id", "3A_Code", "ScientificName", "CatalanName", "SpanishName", "EnglishName", "Group", "Grou...") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
params = (Int4(22001), 'HKE', 'Hake', None, None, None, ...)
ignored_wrapper_args = (False, {'connection': <DatabaseWrapper vendor='postgresql' alias='default'>, 'cursor': <django.db.backends.utils.CursorWrapper object at 0x77eafaec18b0>})

    def _execute(self, sql, params, *ignored_wrapper_args):
        # Raise a warning during app initialization (stored_app_configs is only
        # ever set during testing).
        if not apps.ready and not apps.stored_app_configs:
            warnings.warn(self.APPS_NOT_READY_WARNING_MSG, category=RuntimeWarning)
        self.db.validate_no_broken_transaction()
        with self.db.wrap_database_errors:
            if params is None:
                # params default might be backend specific.
                return self.cursor.execute(sql)
            else:
>               return self.cursor.execute(sql, params)

/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:105:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <django.db.backends.postgresql.base.Cursor [closed] [INERROR] (host=db user=vcpe_user database=test_api_segura_bbdd) at 0x77eafaefba10>
query = 'INSERT INTO "species" ("Id", "3A_Code", "ScientificName", "CatalanName", "SpanishName", "EnglishName", "Group", "Grou...") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
params = (Int4(22001), 'HKE', 'Hake', None, None, None, ...)

    def execute(
        self,
        query: Query,
        params: Params | None = None,
        *,
        prepare: bool | None = None,
        binary: bool | None = None,
    ) -> Self:
        """
        Execute a query or command to the database.
        """
        try:
            with self._conn.lock:
                self._conn.wait(
                    self._execute_gen(query, params, prepare=prepare, binary=binary)
                )
        except e._NO_TRACEBACK as ex:
>           raise ex.with_traceback(None)
E           psycopg.errors.UniqueViolation: duplicate key value violates unique constraint "species_3A_Code_key"
E           DETAIL:  Key ("3A_Code")=(HKE) already exists.

/usr/local/lib/python3.12/site-packages/psycopg/cursor.py:97: UniqueViolation

The above exception was the direct cause of the following exception:

self = <app.tests.integration.test_darp_batch.TestDARPBatchSubmission object at 0x77eafb2e0290>
darp_client = <rest_framework.test.APIClient object at 0x77eafaec3380>
sample_sales_note_data = {'EstablecimientosVenta': {'EstablecimientoVenta': [{'NombreEstablecimiento': 'Llotja de Test', 'NumIdentificacionEstablec': 'LLOTJA_TEST', 'Ventas': {'VentasUnidadProductiva': [{...}]}}]}, 'NumEnvio': 'TEST_001', 'TipoRespuesta': 1}

    def test_batch_post_rollback_on_error(self, darp_client, sample_sales_note_data):
        """Enviar un batch amb una nota invàlida i verificar que tot el batch fa rollback"""
        from sales_notes.existing_models import Species, Vessel
        from sales_notes.models import Envio

        # Preparar catàleg mínim
>       Species.objects.create(id=22001, code_3a="HKE", scientific_name="Hake")

tests/integration/test_darp_batch.py:115:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:679: in create
    obj.save(force_insert=True, using=self.db)
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:892: in save
    self.save_base(
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:998: in save_base
    updated = self._save_table(
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:1161: in _save_table
    results = self._do_insert(
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:1202: in _do_insert
    return manager._insert(
/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:1847: in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
/usr/local/lib/python3.12/site-packages/django/db/models/sql/compiler.py:1836: in execute_sql
    cursor.execute(sql, params)
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:79: in execute
    return self._execute_with_wrappers(
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:92: in _execute_with_wrappers
    return executor(sql, params, many, context)
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:100: in _execute
    with self.db.wrap_database_errors:
/usr/local/lib/python3.12/site-packages/django/db/utils.py:91: in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
/usr/local/lib/python3.12/site-packages/django/db/backends/utils.py:105: in _execute
    return self.cursor.execute(sql, params)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <django.db.backends.postgresql.base.Cursor [closed] [INERROR] (host=db user=vcpe_user database=test_api_segura_bbdd) at 0x77eafaefba10>
query = 'INSERT INTO "species" ("Id", "3A_Code", "ScientificName", "CatalanName", "SpanishName", "EnglishName", "Group", "Grou...") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
params = (Int4(22001), 'HKE', 'Hake', None, None, None, ...)

    def execute(
        self,
        query: Query,
        params: Params | None = None,
        *,
        prepare: bool | None = None,
        binary: bool | None = None,
    ) -> Self:
        """
        Execute a query or command to the database.
        """
        try:
            with self._conn.lock:
                self._conn.wait(
                    self._execute_gen(query, params, prepare=prepare, binary=binary)
                )
        except e._NO_TRACEBACK as ex:
>           raise ex.with_traceback(None)
E           django.db.utils.IntegrityError: duplicate key value violates unique constraint "species_3A_Code_key"
E           DETAIL:  Key ("3A_Code")=(HKE) already exists.

/usr/local/lib/python3.12/site-packages/psycopg/cursor.py:97: IntegrityError
____________ TestAuditSignals.test_successful_login_resets_failures ____________

self = <app.tests.unit.test_audit.TestAuditSignals object at 0x77eafb355160>
api_user = <APIUser: apiuser - API Test Org>
rf = <django.test.client.RequestFactory object at 0x77eafacfd160>

    @pytest.mark.usefixtures("rf")
    def test_successful_login_resets_failures(self, api_user, rf):
        """Test que un login exitós reseteja el comptador de fallades i registra IP.
        (Cobreix la lògica 'user.reset_failed_login()' a audit/signals.py)
        """
        from django.contrib.auth import login
        from django.contrib.sessions.middleware import SessionMiddleware
        from django.urls import reverse  # Cal afegir import

        # 1. Preparar l'usuari amb intents fallits
        api_user.failed_login_attempts = 3
        api_user.save()

        # 2. Preparar la request (simulant middleware)
        request = rf.get(reverse("authentication:login"))
        SessionMiddleware(lambda r: r).process_request(request)
        request.session.save()
        request.META["REMOTE_ADDR"] = "192.168.1.50"

        # 3. Executar el signal (simulant el login)
        # Això dispara el signal user_logged_in
        login(request, api_user)

        # 4. Verificar el log
        log = AuditLog.objects.latest("timestamp")
        assert log.action == "LOGIN"
        assert log.user == api_user
        assert log.ip_address == "192.168.1.50"

        # 5. Verificar l'usuari
        api_user.refresh_from_db()
>       assert api_user.failed_login_attempts == 0
E       assert 3 == 0
E        +  where 3 = <APIUser: apiuser - API Test Org>.failed_login_attempts

tests/unit/test_audit.py:166: AssertionError
----------------------------- Captured stderr call -----------------------------
ERROR 2026-01-15 13:21:53,803 signals 50759 131851390106496 Error auditant login: 'APIUser' object has no attribute 'reset_failed_login'
Traceback (most recent call last):
  File "/app/audit/signals.py", line 93, in audit_user_login
    user.reset_failed_login()
    ^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'APIUser' object has no attribute 'reset_failed_login'. Did you mean: 'last_failed_login'?

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     17  80.68%   36, 77-78, 84-102, 108, 119-120, 141, 152, 184, 190
audit/models.py                                               79      3  96.20%   82, 173, 217
audit/signals.py                                              77     15  80.52%   36-37, 71-72, 94-96, 104-114, 169-170, 187-188
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
sales_notes/encrypted_fields.py                               90     14  84.44%   30, 42, 51-53, 92, 114, 128, 136, 143, 146-149
sales_notes/exception_handler.py                              19      0 100.00%
sales_notes/existing_models.py                                87      3  96.55%   31, 72, 112
sales_notes/models.py                                        201     17  91.54%   93, 135, 192-193, 199, 222, 252, 282, 454-455, 476, 481-483, 509-511
sales_notes/permissions.py                                    30      5  83.33%   39, 57, 72, 78, 89
sales_notes/serializers.py                                   273     37  86.45%   116, 122, 128, 136, 140-141, 156, 170, 184, 217, 220, 226, 255-258, 266, 290, 319, 325, 386-392, 415-419, 441, 487-494, 529
sales_notes/tasks.py                                          27      0 100.00%
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                         104     33  68.27%   85, 105, 116-152, 188-189
-----------------------------------------------------------------------------------------
TOTAL                                                       1532    325  78.79%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 78.79%
=========================== short test summary info ============================
FAILED tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_post_success
FAILED tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_post_rollback_on_error
FAILED tests/unit/test_audit.py::TestAuditSignals::test_successful_login_resets_failures
================== 3 failed, 123 passed, 3 skipped in 11.53s ===================


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
Run started:2026-01-15 12:21:59.570424

Test results:
	No issues identified.

Code scanned:
	Total lines of code: 7385
	Total lines skipped (#nosec): 0
	Total potential issues skipped due to specifically being disabled (e.g., #nosec BXXX): 2

Run metrics:
	Total issues (by severity):
		Undefined: 0
		Low: 274
		Medium: 0
		High: 0
	Total issues (by confidence):
		Undefined: 0
		Low: 0
		Medium: 5
		High: 269
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


**Temps d'execució:** 0s


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
./authentication/migrations/0004_alter_apiuser_groups_alter_apiuser_is_active.py:20:80: E501 line too long (80 > 79 characters)
./authentication/migrations/0004_alter_apiuser_groups_alter_apiuser_is_active.py:32:80: E501 line too long (86 > 79 characters)
./authentication/migrations/0005_alter_apiuser_groups_alter_apiuser_is_active.py:10:80: E501 line too long (80 > 79 characters)
./authentication/migrations/0005_alter_apiuser_groups_alter_apiuser_is_active.py:19:80: E501 line too long (126 > 79 characters)
./authentication/migrations/0005_alter_apiuser_groups_alter_apiuser_is_active.py:31:80: E501 line too long (130 > 79 characters)
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
./sales_notes/exception_handler.py:44:80: E501 line too long (103 > 79 characters)
./sales_notes/exception_handler.py:58:80: E501 line too long (89 > 79 characters)
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
./sales_notes/migrations/0003_remove_especie_especie_nif_ven_bace9e_idx_and_more.py:14:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0003_remove_especie_especie_nif_ven_bace9e_idx_and_more.py:31:80: E501 line too long (88 > 79 characters)
./sales_notes/migrations/0003_remove_especie_especie_nif_ven_bace9e_idx_and_more.py:51:80: E501 line too long (110 > 79 characters)
./sales_notes/migrations/0003_remove_especie_especie_nif_ven_bace9e_idx_and_more.py:56:80: E501 line too long (108 > 79 characters)
./sales_notes/migrations/0003_remove_especie_especie_nif_ven_bace9e_idx_and_more.py:62:80: E501 line too long (119 > 79 characters)
./sales_notes/models.py:35:80: E501 line too long (112 > 79 characters)
./sales_notes/models.py:43:80: E501 line too long (101 > 79 characters)
./sales_notes/models.py:57:80: E501 line too long (112 > 79 characters)
./sales_notes/models.py:79:80: E501 line too long (95 > 79 characters)
./sales_notes/models.py:82:80: E501 line too long (89 > 79 characters)
./sales_notes/models.py:103:80: E501 line too long (91 > 79 characters)
./sales_notes/models.py:112:80: E501 line too long (93 > 79 characters)
./sales_notes/models.py:135:80: E501 line too long (84 > 79 characters)
./sales_notes/models.py:144:80: E501 line too long (90 > 79 characters)
./sales_notes/models.py:147:80: E501 line too long (107 > 79 characters)
./sales_notes/models.py:160:80: E501 line too long (120 > 79 characters)
./sales_notes/models.py:163:80: E501 line too long (119 > 79 characters)
./sales_notes/models.py:178:80: E501 line too long (90 > 79 characters)
./sales_notes/models.py:180:80: E501 line too long (97 > 79 characters)
./sales_notes/models.py:193:80: E501 line too long (94 > 79 characters)
./sales_notes/models.py:196:80: E501 line too long (87 > 79 characters)
./sales_notes/models.py:231:80: E501 line too long (91 > 79 characters)
./sales_notes/models.py:234:80: E501 line too long (100 > 79 characters)
./sales_notes/models.py:236:80: E501 line too long (97 > 79 characters)
./sales_notes/models.py:261:80: E501 line too long (92 > 79 characters)
./sales_notes/models.py:264:80: E501 line too long (103 > 79 characters)
./sales_notes/models.py:266:80: E501 line too long (97 > 79 characters)
./sales_notes/models.py:297:80: E501 line too long (112 > 79 characters)
./sales_notes/models.py:300:80: E501 line too long (108 > 79 characters)
./sales_notes/models.py:303:80: E501 line too long (115 > 79 characters)
./sales_notes/models.py:314:80: E501 line too long (117 > 79 characters)
./sales_notes/models.py:321:80: E501 line too long (90 > 79 characters)
./sales_notes/models.py:324:80: E501 line too long (100 > 79 characters)
./sales_notes/models.py:327:80: E501 line too long (105 > 79 characters)
./sales_notes/models.py:330:80: E501 line too long (111 > 79 characters)
./sales_notes/models.py:332:80: E501 line too long (117 > 79 characters)
./sales_notes/models.py:335:80: E501 line too long (112 > 79 characters)
./sales_notes/models.py:337:80: E501 line too long (116 > 79 characters)
./sales_notes/models.py:339:80: E501 line too long (100 > 79 characters)
./sales_notes/models.py:343:80: E501 line too long (96 > 79 characters)
./sales_notes/models.py:345:80: E501 line too long (95 > 79 characters)
./sales_notes/models.py:348:80: E501 line too long (87 > 79 characters)
./sales_notes/models.py:350:80: E501 line too long (81 > 79 characters)
./sales_notes/models.py:352:80: E501 line too long (106 > 79 characters)
./sales_notes/models.py:355:80: E501 line too long (110 > 79 characters)
./sales_notes/models.py:357:80: E501 line too long (112 > 79 characters)
./sales_notes/models.py:359:80: E501 line too long (98 > 79 characters)
./sales_notes/models.py:370:80: E501 line too long (82 > 79 characters)
./sales_notes/models.py:373:80: E501 line too long (94 > 79 characters)
./sales_notes/models.py:374:80: E501 line too long (83 > 79 characters)
./sales_notes/models.py:376:80: E501 line too long (114 > 79 characters)
./sales_notes/models.py:378:80: E501 line too long (97 > 79 characters)
./sales_notes/models.py:381:80: E501 line too long (84 > 79 characters)
./sales_notes/models.py:384:80: E501 line too long (117 > 79 characters)
./sales_notes/models.py:386:80: E501 line too long (114 > 79 characters)
./sales_notes/models.py:389:80: E501 line too long (86 > 79 characters)
./sales_notes/models.py:391:80: E501 line too long (117 > 79 characters)
./sales_notes/models.py:400:80: E501 line too long (118 > 79 characters)
./sales_notes/models.py:402:80: E501 line too long (104 > 79 characters)
./sales_notes/models.py:414:80: E501 line too long (96 > 79 characters)
./sales_notes/models.py:418:80: E501 line too long (94 > 79 characters)
./sales_notes/models.py:421:80: E501 line too long (98 > 79 characters)
./sales_notes/models.py:434:80: E501 line too long (91 > 79 characters)
./sales_notes/models.py:437:80: E501 line too long (115 > 79 characters)
./sales_notes/models.py:440:80: E501 line too long (106 > 79 characters)
./sales_notes/models.py:442:80: E501 line too long (86 > 79 characters)
./sales_notes/models.py:444:80: E501 line too long (108 > 79 characters)
./sales_notes/models.py:455:80: E501 line too long (109 > 79 characters)
./sales_notes/models.py:476:80: E501 line too long (80 > 79 characters)
./sales_notes/models.py:493:80: E501 line too long (97 > 79 characters)
./sales_notes/models.py:495:80: E501 line too long (83 > 79 characters)
./sales_notes/models.py:497:80: E501 line too long (114 > 79 characters)
./sales_notes/permissions.py:24:80: E501 line too long (100 > 79 characters)
./sales_notes/permissions.py:65:80: E501 line too long (83 > 79 characters)
./sales_notes/permissions.py:68:80: E501 line too long (97 > 79 characters)
./sales_notes/permissions.py:85:80: E501 line too long (97 > 79 characters)
./sales_notes/serializers.py:40:80: E501 line too long (110 > 79 characters)
./sales_notes/serializers.py:49:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:51:80: E501 line too long (99 > 79 characters)
./sales_notes/serializers.py:54:80: E501 line too long (105 > 79 characters)
./sales_notes/serializers.py:57:80: E501 line too long (82 > 79 characters)
./sales_notes/serializers.py:58:80: E501 line too long (85 > 79 characters)
./sales_notes/serializers.py:60:80: E501 line too long (83 > 79 characters)
./sales_notes/serializers.py:63:80: E501 line too long (85 > 79 characters)
./sales_notes/serializers.py:116:80: E501 line too long (103 > 79 characters)
./sales_notes/serializers.py:122:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:136:80: E501 line too long (104 > 79 characters)
./sales_notes/serializers.py:138:80: E501 line too long (81 > 79 characters)
./sales_notes/serializers.py:141:80: E501 line too long (114 > 79 characters)
./sales_notes/serializers.py:151:80: E501 line too long (106 > 79 characters)
./sales_notes/serializers.py:156:80: E501 line too long (117 > 79 characters)
./sales_notes/serializers.py:170:80: E501 line too long (89 > 79 characters)
./sales_notes/serializers.py:184:80: E501 line too long (83 > 79 characters)
./sales_notes/serializers.py:201:80: E501 line too long (80 > 79 characters)
./sales_notes/serializers.py:214:80: E501 line too long (115 > 79 characters)
./sales_notes/serializers.py:217:80: E501 line too long (111 > 79 characters)
./sales_notes/serializers.py:220:80: E501 line too long (112 > 79 characters)
./sales_notes/serializers.py:223:80: E501 line too long (108 > 79 characters)
./sales_notes/serializers.py:227:80: E501 line too long (99 > 79 characters)
./sales_notes/serializers.py:258:80: E501 line too long (90 > 79 characters)
./sales_notes/serializers.py:263:80: E501 line too long (86 > 79 characters)
./sales_notes/serializers.py:281:80: E501 line too long (115 > 79 characters)
./sales_notes/serializers.py:290:80: E501 line too long (105 > 79 characters)
./sales_notes/serializers.py:300:80: E501 line too long (113 > 79 characters)
./sales_notes/serializers.py:314:80: E501 line too long (88 > 79 characters)
./sales_notes/serializers.py:319:80: E501 line too long (96 > 79 characters)
./sales_notes/serializers.py:325:80: E501 line too long (119 > 79 characters)
./sales_notes/serializers.py:333:80: E501 line too long (92 > 79 characters)
./sales_notes/serializers.py:344:80: E501 line too long (95 > 79 characters)
./sales_notes/serializers.py:361:80: E501 line too long (96 > 79 characters)
./sales_notes/serializers.py:363:80: E501 line too long (85 > 79 characters)
./sales_notes/serializers.py:368:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:370:80: E501 line too long (106 > 79 characters)
./sales_notes/serializers.py:372:80: E501 line too long (99 > 79 characters)
./sales_notes/serializers.py:383:80: E501 line too long (119 > 79 characters)
./sales_notes/serializers.py:387:80: E501 line too long (94 > 79 characters)
./sales_notes/serializers.py:389:80: E501 line too long (92 > 79 characters)
./sales_notes/serializers.py:439:80: E501 line too long (89 > 79 characters)
./sales_notes/serializers.py:447:80: E501 line too long (92 > 79 characters)
./sales_notes/serializers.py:457:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:484:80: E501 line too long (83 > 79 characters)
./sales_notes/serializers.py:502:80: E501 line too long (80 > 79 characters)
./sales_notes/serializers.py:527:80: E501 line too long (81 > 79 characters)
./sales_notes/serializers.py:530:80: E501 line too long (116 > 79 characters)
./sales_notes/serializers.py:584:80: E501 line too long (104 > 79 characters)
./sales_notes/tasks.py:27:80: E501 line too long (112 > 79 characters)
./sales_notes/tasks.py:33:80: E501 line too long (90 > 79 characters)
./sales_notes/tasks.py:49:80: E501 line too long (106 > 79 characters)
./sales_notes/views.py:14:80: E501 line too long (106 > 79 characters)
./sales_notes/views.py:81:80: E501 line too long (81 > 79 characters)
./sales_notes/views.py:95:80: E501 line too long (90 > 79 characters)
./sales_notes/views.py:100:80: E501 line too long (100 > 79 characters)
./sales_notes/views.py:104:80: E501 line too long (107 > 79 characters)
./sales_notes/views.py:106:80: E501 line too long (114 > 79 characters)
./sales_notes/views.py:118:80: E501 line too long (85 > 79 characters)
./sales_notes/views.py:128:80: E501 line too long (81 > 79 characters)
./sales_notes/views.py:137:80: E501 line too long (140 > 79 characters)
./sales_notes/views.py:141:80: E501 line too long (87 > 79 characters)
./sales_notes/views.py:158:80: E501 line too long (87 > 79 characters)
./sales_notes/views.py:163:80: E501 line too long (86 > 79 characters)
./sales_notes/views.py:166:80: E501 line too long (89 > 79 characters)
./sales_notes/views.py:204:80: E501 line too long (81 > 79 characters)
./sales_notes/views.py:223:80: E501 line too long (86 > 79 characters)
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
./tests/integration/test_darp_batch.py:79:80: E501 line too long (87 > 79 characters)
./tests/integration/test_darp_batch.py:96:80: E501 line too long (84 > 79 characters)
./tests/integration/test_darp_batch.py:97:80: E501 line too long (117 > 79 characters)
./tests/integration/test_darp_batch.py:99:80: E501 line too long (132 > 79 characters)
./tests/integration/test_darp_batch.py:107:80: E501 line too long (81 > 79 characters)
./tests/integration/test_darp_batch.py:109:80: E501 line too long (85 > 79 characters)
./tests/integration/test_darp_batch.py:110:80: E501 line too long (92 > 79 characters)
./tests/integration/test_darp_batch.py:126:80: E501 line too long (84 > 79 characters)
./tests/integration/test_darp_batch.py:127:80: E501 line too long (132 > 79 characters)
./tests/integration/test_darp_batch.py:128:80: E501 line too long (127 > 79 characters)
./tests/integration/test_darp_batch.py:136:80: E501 line too long (114 > 79 characters)
./tests/integration/test_darp_batch.py:137:80: E501 line too long (123 > 79 characters)
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
./tests/unit/test_audit.py:23:80: E501 line too long (116 > 79 characters)
./tests/unit/test_audit.py:58:80: E501 line too long (109 > 79 characters)
./tests/unit/test_audit.py:60:80: E501 line too long (108 > 79 characters)
./tests/unit/test_audit.py:109:80: E501 line too long (93 > 79 characters)
./tests/unit/test_audit.py:125:80: E501 line too long (103 > 79 characters)
./tests/unit/test_audit.py:129:80: E501 line too long (90 > 79 characters)
./tests/unit/test_audit.py:131:80: E501 line too long (80 > 79 characters)
./tests/unit/test_audit.py:137:80: E501 line too long (84 > 79 characters)
./tests/unit/test_audit.py:170:80: E501 line too long (94 > 79 characters)
./tests/unit/test_audit.py:175:80: E501 line too long (89 > 79 characters)
./tests/unit/test_audit.py:182:80: E501 line too long (90 > 79 characters)
./tests/unit/test_audit.py:184:80: E501 line too long (80 > 79 characters)
./tests/unit/test_audit.py:189:80: E501 line too long (101 > 79 characters)
./tests/unit/test_audit.py:191:80: E501 line too long (104 > 79 characters)
./tests/unit/test_audit.py:216:80: E501 line too long (115 > 79 characters)
./tests/unit/test_audit.py:221:80: E501 line too long (119 > 79 characters)
./tests/unit/test_audit.py:241:80: E501 line too long (97 > 79 characters)
./tests/unit/test_audit.py:261:80: E501 line too long (112 > 79 characters)
./tests/unit/test_audit.py:267:80: E501 line too long (91 > 79 characters)
./tests/unit/test_audit.py:273:80: E501 line too long (108 > 79 characters)
./tests/unit/test_audit.py:275:80: E501 line too long (106 > 79 characters)
./tests/unit/test_audit.py:280:80: E501 line too long (88 > 79 characters)
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
./tests/unit/test_views.py:19:80: E501 line too long (109 > 79 characters)
./tests/unit/test_views.py:33:80: E501 line too long (94 > 79 characters)
./tests/unit/test_views.py:45:80: E501 line too long (106 > 79 characters)
./tests/unit/test_views.py:62:80: E501 line too long (115 > 79 characters)
./tests/unit/test_views.py:88:80: E501 line too long (101 > 79 characters)
./tests/unit/test_views.py:98:80: E501 line too long (81 > 79 characters)
./tests/unit/test_views.py:105:80: E501 line too long (87 > 79 characters)
./tests/unit/test_views.py:106:80: E501 line too long (82 > 79 characters)
./tests/unit/test_views.py:110:80: E501 line too long (95 > 79 characters)
./tests/unit/test_views.py:111:80: E501 line too long (95 > 79 characters)
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
./vcpe_api/settings.py:33:80: E501 line too long (120 > 79 characters)
./vcpe_api/settings.py:76:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:139:80: E501 line too long (91 > 79 characters)
./vcpe_api/settings.py:142:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:148:80: E501 line too long (82 > 79 characters)
./vcpe_api/settings.py:151:80: E501 line too long (83 > 79 characters)
./vcpe_api/settings.py:187:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:190:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:200:80: E501 line too long (97 > 79 characters)
./vcpe_api/settings.py:201:80: E501 line too long (92 > 79 characters)
./vcpe_api/settings.py:217:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:247:80: E501 line too long (88 > 79 characters)
./vcpe_api/settings.py:285:80: E501 line too long (93 > 79 characters)
./vcpe_api/settings_production.py:89:80: E501 line too long (86 > 79 characters)
./vcpe_api/settings_production.py:92:80: E501 line too long (82 > 79 characters)
./vcpe_api/settings_production.py:224:80: E501 line too long (84 > 79 characters)
./vcpe_api/urls.py:7:80: E501 line too long (98 > 79 characters)
./vcpe_api/urls.py:19:80: E501 line too long (82 > 79 characters)
./vcpe_api/urls.py:23:80: E501 line too long (92 > 79 characters)
./vcpe_api/urls.py:24:80: E501 line too long (86 > 79 characters)
767   E501 line too long (80 > 79 characters)
3     E712 comparison to False should be 'if cond is False:' or 'if not cond:'
1     E722 do not use bare 'except'
9     F401 'audit.signals' imported but unused
4     F541 f-string is missing placeholders
3     F811 redefinition of unused 'settings' from line 9
3     F841 local variable 'response' is assigned to but never used
790


```


**Resultat:** ✅ Completat correctament

---

*Report generat automàticament per run_all_tests_with_report.sh*
*Data: 15/01/2026 13:22:02*
*TFM Ciberseguretat i Privadesa - ICATMAR*
