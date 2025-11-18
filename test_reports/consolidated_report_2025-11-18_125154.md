# 📋 Report Consolidat de Tests - VCPE API

**Data d'execució:** 18/11/2025 12:51:54  
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


NAME                 IMAGE                    COMMAND                  SERVICE         CREATED          STATUS                            PORTS
vcpe_api             api_dev-api              "python manage.py ru…"   api             52 minutes ago   Up 5 seconds (health: starting)   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
vcpe_celery_beat     api_dev-celery_beat      "celery -A vcpe_api …"   celery_beat     56 minutes ago   Restarting (1) 36 seconds ago     
vcpe_celery_worker   api_dev-celery_worker    "celery -A vcpe_api …"   celery_worker   56 minutes ago   Restarting (1) 34 seconds ago     
vcpe_postgres        postgis/postgis:16-3.4   "docker-entrypoint.s…"   db              56 minutes ago   Up 56 minutes (healthy)           0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp
vcpe_redis           redis:7.4-alpine         "docker-entrypoint.s…"   redis           56 minutes ago   Up 56 minutes (healthy)           0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp


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


**Temps d'execució:** 6s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
django: version: 5.1.2, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.0.0
collecting ... collected 21 items

tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_success FAILED [  4%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_invalid_credentials FAILED [  9%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_refresh_token_success FAILED [ 14%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_verify_token_success FAILED [ 19%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_access_protected_endpoint_without_token PASSED [ 23%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_access_protected_endpoint_with_valid_token PASSED [ 28%]
tests/unit/test_models.py::TestEnvioModel::test_create_envio_valid ERROR [ 33%]
tests/unit/test_models.py::TestEnvioModel::test_num_envio_unique ERROR   [ 38%]
tests/unit/test_models.py::TestEnvioAPI::test_create_envio_authenticated ERROR [ 42%]
tests/unit/test_models.py::TestEnvioAPI::test_create_envio_unauthenticated ERROR [ 47%]
tests/unit/test_models.py::TestEnvioAPI::test_rate_limiting ERROR        [ 52%]
tests/unit/test_models.py::TestOWASPCompliance::test_sql_injection_protection ERROR [ 57%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_create_envio FAILED [ 61%]
tests/unit/test_permissions.py::TestUserPermissions::test_investigador_cannot_create_envio PASSED [ 66%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_list_own_envios PASSED [ 71%]
tests/unit/test_permissions.py::TestUserPermissions::test_investigador_can_list_all_envios PASSED [ 76%]
tests/unit/test_permissions.py::TestUserPermissions::test_admin_can_list_all_envios PASSED [ 80%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_retrieve_own_envio FAILED [ 85%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_cannot_retrieve_other_envio PASSED [ 90%]
tests/unit/test_permissions.py::TestUserPermissions::test_investigador_can_retrieve_any_envio FAILED [ 95%]
tests/unit/test_permissions.py::TestUserPermissions::test_unauthenticated_cannot_access PASSED [100%]

==================================== ERRORS ====================================
___________ ERROR at setup of TestEnvioModel.test_create_envio_valid ___________
tests/conftest.py:330: in api_user
    api_user_profile = APIUser.objects.create(
/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:677: in create
    obj = self.model(**kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:567: in __init__
    raise TypeError(
E   TypeError: APIUser() got unexpected keyword arguments: 'user'
____________ ERROR at setup of TestEnvioModel.test_num_envio_unique ____________
tests/conftest.py:330: in api_user
    api_user_profile = APIUser.objects.create(
/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:677: in create
    obj = self.model(**kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/base.py:567: in __init__
    raise TypeError(
E   TypeError: APIUser() got unexpected keyword arguments: 'user'
________ ERROR at setup of TestEnvioAPI.test_create_envio_authenticated ________
file /app/tests/unit/test_models.py, line 32
      def test_create_envio_authenticated(self, api_client, auth_token, sample_envio_data):
E       fixture 'auth_token' not found
>       available fixtures: _dj_autoclear_mailbox, _django_clear_site_cache, _django_db_helper, _django_db_marker, _django_set_urlconf, _django_setup_unittest, _fail_for_invalid_template_variable, _live_server_helper, _session_faker, _template_string_if_invalid_marker, admin_client, admin_user, api_client, api_user, async_client, async_rf, authenticated_admin_client, authenticated_client, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capture_audit_logs, capture_security_events, client, cov, darp_client, darp_user, db, disable_rate_limiting, django_assert_max_num_queries, django_assert_num_queries, django_capture_on_commit_callbacks, django_db_blocker, django_db_createdb, django_db_keepdb, django_db_modify_db_settings, django_db_modify_db_settings_parallel_suffix, django_db_modify_db_settings_tox_suffix, django_db_modify_db_settings_xdist_suffix, django_db_reset_sequences, django_db_serialized_rollback, django_db_setup, django_db_use_migrations, django_mail_dnsname, django_mail_patch_dns, django_test_environment, django_user_model, django_username_field, doctest_namespace, enable_db_access_for_all_tests, faker, invalid_sales_note_data, investigador_client, investigador_user, live_server, mailoutbox, mock_redis, monkeypatch, multiple_envios, multiple_test_users, no_cover, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, rf, sample_sales_note_data, settings, test_user, test_user_credentials, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory, transactional_db
>       use 'pytest --fixtures [testpath]' for help on them.

/app/tests/unit/test_models.py:32
_______ ERROR at setup of TestEnvioAPI.test_create_envio_unauthenticated _______
file /app/tests/unit/test_models.py, line 40
      def test_create_envio_unauthenticated(self, api_client, sample_envio_data):
E       fixture 'sample_envio_data' not found
>       available fixtures: _dj_autoclear_mailbox, _django_clear_site_cache, _django_db_helper, _django_db_marker, _django_set_urlconf, _django_setup_unittest, _fail_for_invalid_template_variable, _live_server_helper, _session_faker, _template_string_if_invalid_marker, admin_client, admin_user, api_client, api_user, async_client, async_rf, authenticated_admin_client, authenticated_client, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capture_audit_logs, capture_security_events, client, cov, darp_client, darp_user, db, disable_rate_limiting, django_assert_max_num_queries, django_assert_num_queries, django_capture_on_commit_callbacks, django_db_blocker, django_db_createdb, django_db_keepdb, django_db_modify_db_settings, django_db_modify_db_settings_parallel_suffix, django_db_modify_db_settings_tox_suffix, django_db_modify_db_settings_xdist_suffix, django_db_reset_sequences, django_db_serialized_rollback, django_db_setup, django_db_use_migrations, django_mail_dnsname, django_mail_patch_dns, django_test_environment, django_user_model, django_username_field, doctest_namespace, enable_db_access_for_all_tests, faker, invalid_sales_note_data, investigador_client, investigador_user, live_server, mailoutbox, mock_redis, monkeypatch, multiple_envios, multiple_test_users, no_cover, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, rf, sample_sales_note_data, settings, test_user, test_user_credentials, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory, transactional_db
>       use 'pytest --fixtures [testpath]' for help on them.

/app/tests/unit/test_models.py:40
______________ ERROR at setup of TestEnvioAPI.test_rate_limiting _______________
file /app/tests/unit/test_models.py, line 45
      def test_rate_limiting(self, api_client, auth_token, sample_envio_data):
E       fixture 'auth_token' not found
>       available fixtures: _dj_autoclear_mailbox, _django_clear_site_cache, _django_db_helper, _django_db_marker, _django_set_urlconf, _django_setup_unittest, _fail_for_invalid_template_variable, _live_server_helper, _session_faker, _template_string_if_invalid_marker, admin_client, admin_user, api_client, api_user, async_client, async_rf, authenticated_admin_client, authenticated_client, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capture_audit_logs, capture_security_events, client, cov, darp_client, darp_user, db, disable_rate_limiting, django_assert_max_num_queries, django_assert_num_queries, django_capture_on_commit_callbacks, django_db_blocker, django_db_createdb, django_db_keepdb, django_db_modify_db_settings, django_db_modify_db_settings_parallel_suffix, django_db_modify_db_settings_tox_suffix, django_db_modify_db_settings_xdist_suffix, django_db_reset_sequences, django_db_serialized_rollback, django_db_setup, django_db_use_migrations, django_mail_dnsname, django_mail_patch_dns, django_test_environment, django_user_model, django_username_field, doctest_namespace, enable_db_access_for_all_tests, faker, invalid_sales_note_data, investigador_client, investigador_user, live_server, mailoutbox, mock_redis, monkeypatch, multiple_envios, multiple_test_users, no_cover, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, rf, sample_sales_note_data, settings, test_user, test_user_credentials, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory, transactional_db
>       use 'pytest --fixtures [testpath]' for help on them.

/app/tests/unit/test_models.py:45
_____ ERROR at setup of TestOWASPCompliance.test_sql_injection_protection ______
file /app/tests/unit/test_models.py, line 60
      def test_sql_injection_protection(self, api_client, auth_token):
E       fixture 'auth_token' not found
>       available fixtures: _dj_autoclear_mailbox, _django_clear_site_cache, _django_db_helper, _django_db_marker, _django_set_urlconf, _django_setup_unittest, _fail_for_invalid_template_variable, _live_server_helper, _session_faker, _template_string_if_invalid_marker, admin_client, admin_user, api_client, api_user, async_client, async_rf, authenticated_admin_client, authenticated_client, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capture_audit_logs, capture_security_events, client, cov, darp_client, darp_user, db, disable_rate_limiting, django_assert_max_num_queries, django_assert_num_queries, django_capture_on_commit_callbacks, django_db_blocker, django_db_createdb, django_db_keepdb, django_db_modify_db_settings, django_db_modify_db_settings_parallel_suffix, django_db_modify_db_settings_tox_suffix, django_db_modify_db_settings_xdist_suffix, django_db_reset_sequences, django_db_serialized_rollback, django_db_setup, django_db_use_migrations, django_mail_dnsname, django_mail_patch_dns, django_test_environment, django_user_model, django_username_field, doctest_namespace, enable_db_access_for_all_tests, faker, invalid_sales_note_data, investigador_client, investigador_user, live_server, mailoutbox, mock_redis, monkeypatch, multiple_envios, multiple_test_users, no_cover, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, rf, sample_sales_note_data, settings, test_user, test_user_credentials, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory, transactional_db
>       use 'pytest --fixtures [testpath]' for help on them.

/app/tests/unit/test_models.py:60
=================================== FAILURES ===================================
_______________ TestJWTAuthentication.test_obtain_token_success ________________
tests/unit/test_authentication.py:15: in test_obtain_token_success
    url = reverse('authentication:token_obtain_pair')
/usr/local/lib/python3.12/site-packages/django/urls/base.py:88: in reverse
    return resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py:831: in _reverse_with_prefix
    raise NoReverseMatch(msg)
E   django.urls.exceptions.NoReverseMatch: Reverse for 'token_obtain_pair' not found. 'token_obtain_pair' is not a valid view function or pattern name.
---------------------------- Captured stderr setup -----------------------------
Creating test database for alias 'default'...
_________ TestJWTAuthentication.test_obtain_token_invalid_credentials __________
tests/unit/test_authentication.py:29: in test_obtain_token_invalid_credentials
    url = reverse('authentication:token_obtain_pair')
/usr/local/lib/python3.12/site-packages/django/urls/base.py:88: in reverse
    return resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py:831: in _reverse_with_prefix
    raise NoReverseMatch(msg)
E   django.urls.exceptions.NoReverseMatch: Reverse for 'token_obtain_pair' not found. 'token_obtain_pair' is not a valid view function or pattern name.
_______________ TestJWTAuthentication.test_refresh_token_success _______________
tests/unit/test_authentication.py:42: in test_refresh_token_success
    url_obtain = reverse('authentication:token_obtain_pair')
/usr/local/lib/python3.12/site-packages/django/urls/base.py:88: in reverse
    return resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py:831: in _reverse_with_prefix
    raise NoReverseMatch(msg)
E   django.urls.exceptions.NoReverseMatch: Reverse for 'token_obtain_pair' not found. 'token_obtain_pair' is not a valid view function or pattern name.
_______________ TestJWTAuthentication.test_verify_token_success ________________
tests/unit/test_authentication.py:61: in test_verify_token_success
    url_obtain = reverse('authentication:token_obtain_pair')
/usr/local/lib/python3.12/site-packages/django/urls/base.py:88: in reverse
    return resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py:831: in _reverse_with_prefix
    raise NoReverseMatch(msg)
E   django.urls.exceptions.NoReverseMatch: Reverse for 'token_obtain_pair' not found. 'token_obtain_pair' is not a valid view function or pattern name.
________________ TestUserPermissions.test_darp_can_create_envio ________________
tests/unit/test_permissions.py:18: in test_darp_can_create_envio
    assert response.status_code == status.HTTP_201_CREATED
E   assert 400 == 201
E    +  where 400 = <Response status_code=400, "application/json">.status_code
E    +  and   201 = status.HTTP_201_CREATED
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:01,328 log 32 131959510838144 Bad Request: /api/sales-notes/envios/
_____________ TestUserPermissions.test_darp_can_retrieve_own_envio _____________
tests/unit/test_permissions.py:67: in test_darp_can_retrieve_own_envio
    assert response.data['NumEnvio'] == envio.num_envio
E   KeyError: 'NumEnvio'
---------------------------- Captured stderr setup -----------------------------
INFO 2025-11-18 12:52:01,869 signals 32 131959510838144 Auditat creació d'enviament DARP_ENV_001
INFO 2025-11-18 12:52:01,871 signals 32 131959510838144 Auditat creació d'enviament DARP_ENV_002
INFO 2025-11-18 12:52:01,873 signals 32 131959510838144 Auditat creació d'enviament OTHER_ENV_001
_________ TestUserPermissions.test_investigador_can_retrieve_any_envio _________
tests/unit/test_permissions.py:88: in test_investigador_can_retrieve_any_envio
    assert response.data['NumEnvio'] == darp_envio.num_envio
E   KeyError: 'NumEnvio'
---------------------------- Captured stderr setup -----------------------------
INFO 2025-11-18 12:52:02,109 signals 32 131959510838144 Auditat creació d'enviament DARP_ENV_001
INFO 2025-11-18 12:52:02,111 signals 32 131959510838144 Auditat creació d'enviament DARP_ENV_002
INFO 2025-11-18 12:52:02,112 signals 32 131959510838144 Auditat creació d'enviament OTHER_ENV_001

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     19  78.41%   33, 74-75, 81-99, 105, 116-117, 138, 149, 174, 180, 227-228
audit/models.py                                               79      3  96.20%   105, 222, 289
audit/signals.py                                              77     43  44.16%   33-34, 45-57, 68-69, 75-96, 102-112, 118-141, 163-170, 176-188
audit/tasks.py                                                 0      0 100.00%
authentication/apps.py                                         7      0 100.00%
authentication/management/commands/create_test_users.py       23     23   0.00%   4-51
authentication/management/commands/create_user_groups.py      17     17   0.00%   4-31
authentication/models.py                                     129     29  77.52%   146-151, 155-158, 162-165, 214, 282, 286-290, 294-298, 368-369, 375
authentication/permissions.py                                  0      0 100.00%
authentication/serializers.py                                 80     22  72.50%   71-75, 87-89, 136, 171-179, 271-281, 296-299, 361
authentication/urls.py                                         5      0 100.00%
authentication/views.py                                      123     84  31.71%   42-47, 60, 84-100, 142-309, 341-389, 423-453, 476, 498-499
sales_notes/apps.py                                            7      0 100.00%
sales_notes/exception_handler.py                              20     20   0.00%   1-62
sales_notes/existing_models.py                                88      3  96.59%   31, 71, 108
sales_notes/models.py                                        206     34  83.50%   74, 102, 148, 214-230, 234-235, 253, 295, 337, 647-655, 661-662, 678, 683-685, 720-722
sales_notes/permissions.py                                    30     10  66.67%   18-23, 38-43, 57, 72, 78, 89
sales_notes/serializers.py                                   278    152  45.32%   30-35, 62-66, 70-74, 78-82, 87-100, 115-119, 131-135, 147-151, 173-213, 219-243, 271-275, 299-303, 307-311, 315-335, 343-399, 412, 420-424, 449-462, 466-476, 480-517, 521-550, 585-586
sales_notes/tasks.py                                           0      0 100.00%
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                          53     15  71.70%   77, 84, 92-119
-----------------------------------------------------------------------------------------
TOTAL                                                       1324    474  64.20%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 64.20%
=========================== short test summary info ============================
FAILED tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_success
FAILED tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_invalid_credentials
FAILED tests/unit/test_authentication.py::TestJWTAuthentication::test_refresh_token_success
FAILED tests/unit/test_authentication.py::TestJWTAuthentication::test_verify_token_success
FAILED tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_create_envio
FAILED tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_retrieve_own_envio
FAILED tests/unit/test_permissions.py::TestUserPermissions::test_investigador_can_retrieve_any_envio
ERROR tests/unit/test_models.py::TestEnvioModel::test_create_envio_valid - Ty...
ERROR tests/unit/test_models.py::TestEnvioModel::test_num_envio_unique - Type...
ERROR tests/unit/test_models.py::TestEnvioAPI::test_create_envio_authenticated
ERROR tests/unit/test_models.py::TestEnvioAPI::test_create_envio_unauthenticated
ERROR tests/unit/test_models.py::TestEnvioAPI::test_rate_limiting
ERROR tests/unit/test_models.py::TestOWASPCompliance::test_sql_injection_protection
==================== 7 failed, 8 passed, 6 errors in 4.30s =====================


```


**Resultat:** ✅ Completat correctament


### 3.2 Tests d'Integració


**Temps d'execució:** 7s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
django: version: 5.1.2, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.0.0
collecting ... collected 6 items

tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_submission_success FAILED [ 16%]
tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_rate_limiting_batch PASSED [ 33%]
tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_darp_complete_lifecycle FAILED [ 50%]
tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_investigador_read_only_flow FAILED [ 66%]
tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_filtering_and_search FAILED [ 83%]
tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_rollback_on_error FAILED [100%]

=================================== FAILURES ===================================
____________ TestDARPBatchSubmission.test_batch_submission_success _____________
tests/integration/test_darp_batch.py:26: in test_batch_submission_success
    assert response.status_code == status.HTTP_201_CREATED
E   assert 400 == 201
E    +  where 400 = <Response status_code=400, "application/json">.status_code
E    +  and   201 = status.HTTP_201_CREATED
---------------------------- Captured stderr setup -----------------------------
Creating test database for alias 'default'...
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:07,313 log 1576 133077091634048 Bad Request: /api/sales-notes/envios/
___________ TestSalesNotesCompleteFlow.test_darp_complete_lifecycle ____________
tests/integration/test_sales_notes_flow.py:20: in test_darp_complete_lifecycle
    assert response_create.status_code == status.HTTP_201_CREATED
E   assert 400 == 201
E    +  where 400 = <Response status_code=400, "application/json">.status_code
E    +  and   201 = status.HTTP_201_CREATED
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:07,717 log 1576 133077091634048 Bad Request: /api/sales-notes/envios/
_________ TestSalesNotesCompleteFlow.test_investigador_read_only_flow __________
tests/integration/test_sales_notes_flow.py:61: in test_investigador_read_only_flow
    assert response_create.status_code == status.HTTP_403_FORBIDDEN
E   assert 400 == 403
E    +  where 400 = <Response status_code=400, "application/json">.status_code
E    +  and   403 = status.HTTP_403_FORBIDDEN
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:07,812 log 1576 133077091634048 Bad Request: /api/sales-notes/envios/
_____________ TestSalesNotesCompleteFlow.test_filtering_and_search _____________
tests/integration/test_sales_notes_flow.py:94: in test_filtering_and_search
    response = darp_client.get(url)
/usr/local/lib/python3.12/site-packages/rest_framework/test.py:288: in get
    response = super().get(path, data=data, **extra)
/usr/local/lib/python3.12/site-packages/rest_framework/test.py:205: in get
    return self.generic('GET', path, **r)
/usr/local/lib/python3.12/site-packages/rest_framework/test.py:233: in generic
    return super().generic(
/usr/local/lib/python3.12/site-packages/django/test/client.py:676: in generic
    return self.request(**r)
/usr/local/lib/python3.12/site-packages/rest_framework/test.py:285: in request
    return super().request(**kwargs)
/usr/local/lib/python3.12/site-packages/rest_framework/test.py:237: in request
    request = super().request(**kwargs)
/usr/local/lib/python3.12/site-packages/django/test/client.py:1092: in request
    self.check_exception(response)
/usr/local/lib/python3.12/site-packages/django/test/client.py:805: in check_exception
    raise exc_value
/usr/local/lib/python3.12/site-packages/django/core/handlers/exception.py:55: in inner
    response = get_response(request)
/usr/local/lib/python3.12/site-packages/django/core/handlers/base.py:197: in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
/usr/local/lib/python3.12/site-packages/django/views/decorators/csrf.py:65: in _view_wrapper
    return view_func(request, *args, **kwargs)
/usr/local/lib/python3.12/site-packages/rest_framework/viewsets.py:124: in view
    return self.dispatch(request, *args, **kwargs)
/usr/local/lib/python3.12/site-packages/rest_framework/views.py:509: in dispatch
    response = self.handle_exception(exc)
/usr/local/lib/python3.12/site-packages/rest_framework/views.py:469: in handle_exception
    self.raise_uncaught_exception(exc)
/usr/local/lib/python3.12/site-packages/rest_framework/views.py:480: in raise_uncaught_exception
    raise exc
/usr/local/lib/python3.12/site-packages/rest_framework/views.py:506: in dispatch
    response = handler(request, *args, **kwargs)
/usr/local/lib/python3.12/site-packages/rest_framework/mixins.py:38: in list
    queryset = self.filter_queryset(self.get_queryset())
/usr/local/lib/python3.12/site-packages/rest_framework/generics.py:154: in filter_queryset
    queryset = backend().filter_queryset(self.request, queryset, self)
/usr/local/lib/python3.12/site-packages/rest_framework/filters.py:167: in filter_queryset
    queryset = queryset.filter(reduce(operator.and_, conditions))
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:1476: in filter
    return self._filter_or_exclude(False, args, kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:1494: in _filter_or_exclude
    clone._filter_or_exclude_inplace(negate, args, kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:1501: in _filter_or_exclude_inplace
    self._query.add_q(Q(*args, **kwargs))
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1609: in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1641: in _add_q
    child_clause, needed_inner = self.build_filter(
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1468: in build_filter
    return self._add_q(
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1641: in _add_q
    child_clause, needed_inner = self.build_filter(
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1555: in build_filter
    condition = self.build_lookup(lookups, col, value)
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1372: in build_lookup
    lhs = self.try_transform(lhs, name)
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1423: in try_transform
    raise FieldError(
E   django.core.exceptions.FieldError: Unsupported lookup 'nombre_establecimiento' for ManyToOneRel or join on the field not permitted.
---------------------------- Captured stderr setup -----------------------------
INFO 2025-11-18 12:52:07,902 signals 1576 133077091634048 Auditat creació d'enviament DARP_ENV_001
INFO 2025-11-18 12:52:07,903 signals 1576 133077091634048 Auditat creació d'enviament DARP_ENV_002
INFO 2025-11-18 12:52:07,905 signals 1576 133077091634048 Auditat creació d'enviament OTHER_ENV_001
----------------------------- Captured stderr call -----------------------------
ERROR 2025-11-18 12:52:07,929 log 1576 133077091634048 Internal Server Error: /api/sales-notes/envios/
Traceback (most recent call last):
  File "/usr/local/lib/python3.12/site-packages/django/core/handlers/exception.py", line 55, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/core/handlers/base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/views/decorators/csrf.py", line 65, in _view_wrapper
    return view_func(request, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/viewsets.py", line 124, in view
    return self.dispatch(request, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/views.py", line 509, in dispatch
    response = self.handle_exception(exc)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/views.py", line 469, in handle_exception
    self.raise_uncaught_exception(exc)
  File "/usr/local/lib/python3.12/site-packages/rest_framework/views.py", line 480, in raise_uncaught_exception
    raise exc
  File "/usr/local/lib/python3.12/site-packages/rest_framework/views.py", line 506, in dispatch
    response = handler(request, *args, **kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/mixins.py", line 38, in list
    queryset = self.filter_queryset(self.get_queryset())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/generics.py", line 154, in filter_queryset
    queryset = backend().filter_queryset(self.request, queryset, self)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/filters.py", line 167, in filter_queryset
    queryset = queryset.filter(reduce(operator.and_, conditions))
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/query.py", line 1476, in filter
    return self._filter_or_exclude(False, args, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/query.py", line 1494, in _filter_or_exclude
    clone._filter_or_exclude_inplace(negate, args, kwargs)
  File "/usr/local/lib/python3.12/site-packages/django/db/models/query.py", line 1501, in _filter_or_exclude_inplace
    self._query.add_q(Q(*args, **kwargs))
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1609, in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1641, in _add_q
    child_clause, needed_inner = self.build_filter(
                                 ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1468, in build_filter
    return self._add_q(
           ^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1641, in _add_q
    child_clause, needed_inner = self.build_filter(
                                 ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1555, in build_filter
    condition = self.build_lookup(lookups, col, value)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1372, in build_lookup
    lhs = self.try_transform(lhs, name)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1423, in try_transform
    raise FieldError(
django.core.exceptions.FieldError: Unsupported lookup 'nombre_establecimiento' for ManyToOneRel or join on the field not permitted.
_____________ TestDARPBatchSubmission.test_batch_rollback_on_error _____________
tests/integration/test_darp_batch.py:48: in test_batch_rollback_on_error
    assert response.status_code == status.HTTP_201_CREATED
E   assert 400 == 201
E    +  where 400 = <Response status_code=400, "application/json">.status_code
E    +  and   201 = status.HTTP_201_CREATED
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:08,352 log 1576 133077091634048 Bad Request: /api/sales-notes/envios/
--------------------------- Captured stderr teardown ---------------------------
Destroying test database for alias 'default'...

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     19  78.41%   33, 48, 74-75, 96-97, 105, 116-117, 126, 138, 149, 174, 180, 205-228
audit/models.py                                               79      3  96.20%   105, 222, 289
audit/signals.py                                              77     43  44.16%   33-34, 45-57, 68-69, 75-96, 102-112, 118-141, 163-170, 176-188
audit/tasks.py                                                 0      0 100.00%
authentication/apps.py                                         7      0 100.00%
authentication/management/commands/create_test_users.py       23     23   0.00%   4-51
authentication/management/commands/create_user_groups.py      17     17   0.00%   4-31
authentication/models.py                                     129     29  77.52%   146-151, 155-158, 162-165, 214, 282, 286-290, 294-298, 368-369, 375
authentication/permissions.py                                  0      0 100.00%
authentication/serializers.py                                 80     22  72.50%   71-75, 87-89, 136, 171-179, 271-281, 296-299, 361
authentication/urls.py                                         5      0 100.00%
authentication/views.py                                      123     84  31.71%   42-47, 60, 84-100, 142-309, 341-389, 423-453, 476, 498-499
sales_notes/apps.py                                            7      0 100.00%
sales_notes/exception_handler.py                              20     20   0.00%   1-62
sales_notes/existing_models.py                                88      3  96.59%   31, 71, 108
sales_notes/models.py                                        206     34  83.50%   74, 102, 148, 214-230, 234-235, 253, 295, 337, 647-655, 661-662, 678, 683-685, 720-722
sales_notes/permissions.py                                    30     17  43.33%   18-23, 38-43, 57, 61, 65, 72, 77-89
sales_notes/serializers.py                                   278    157  43.53%   30-35, 62-66, 70-74, 78-82, 87-100, 115-119, 131-135, 147-151, 173-213, 219-243, 271-275, 299-303, 307-311, 315-335, 343-399, 406-427, 449-462, 466-476, 480-517, 521-550, 585-586
sales_notes/tasks.py                                           0      0 100.00%
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                          53     17  67.92%   66, 70, 77, 84, 92-119
-----------------------------------------------------------------------------------------
TOTAL                                                       1324    488  63.14%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 63.14%
=========================== short test summary info ============================
FAILED tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_submission_success
FAILED tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_darp_complete_lifecycle
FAILED tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_investigador_read_only_flow
FAILED tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_filtering_and_search
FAILED tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_rollback_on_error
========================= 5 failed, 1 passed in 4.00s ==========================


```


**Resultat:** ✅ Completat correctament


### 3.3 Tests de Seguretat


**Temps d'execució:** 5s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
django: version: 5.1.2, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.0.0
collecting ... collected 9 items

tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_access_other_user_data PASSED [ 11%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_brute_force_protection FAILED [ 22%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_mass_assignment_vulnerability PASSED [ 33%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_rate_limiting FAILED [ 44%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_admin_endpoint_access_control PASSED [ 55%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_prevent_automated_submission FAILED [ 66%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_security_headers_present PASSED [ 77%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_api_documentation_access_control FAILED [ 88%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_input_validation_sql_injection FAILED [100%]

=================================== FAILURES ===================================
_______________ TestOWASPAPISecurity.test_brute_force_protection _______________
tests/security/test_owasp_api_security.py:27: in test_brute_force_protection
    url = reverse('authentication:token_obtain_pair')
/usr/local/lib/python3.12/site-packages/django/urls/base.py:88: in reverse
    return resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py:831: in _reverse_with_prefix
    raise NoReverseMatch(msg)
E   django.urls.exceptions.NoReverseMatch: Reverse for 'token_obtain_pair' not found. 'token_obtain_pair' is not a valid view function or pattern name.
___________________ TestOWASPAPISecurity.test_rate_limiting ____________________
tests/security/test_owasp_api_security.py:62: in test_rate_limiting
    url = reverse('authentication:token_obtain_pair')
/usr/local/lib/python3.12/site-packages/django/urls/base.py:88: in reverse
    return resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py:831: in _reverse_with_prefix
    raise NoReverseMatch(msg)
E   django.urls.exceptions.NoReverseMatch: Reverse for 'token_obtain_pair' not found. 'token_obtain_pair' is not a valid view function or pattern name.
____________ TestOWASPAPISecurity.test_prevent_automated_submission ____________
tests/security/test_owasp_api_security.py:104: in test_prevent_automated_submission
    assert status.HTTP_429_TOO_MANY_REQUESTS in responses
E   assert 429 in [403, 403, 403, 403, 403, 403, ...]
E    +  where 429 = status.HTTP_429_TOO_MANY_REQUESTS
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:13,844 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,845 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,848 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,849 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,852 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,853 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,856 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,857 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,860 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,860 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,864 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,864 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,867 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,868 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,871 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,872 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,876 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,876 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,880 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,880 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,883 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,884 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,887 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,888 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,891 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,892 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,895 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,896 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,953 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,954 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,958 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,959 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,963 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,964 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,967 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,968 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,971 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,971 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:13,975 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:13,976 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
__________ TestOWASPAPISecurity.test_api_documentation_access_control __________
tests/security/test_owasp_api_security.py:128: in test_api_documentation_access_control
    assert response.status_code == status.HTTP_403_FORBIDDEN
E   assert 200 == 403
E    +  where 200 = <Response status_code=200, "text/html; charset=utf-8">.status_code
E    +  and   403 = status.HTTP_403_FORBIDDEN
___________ TestOWASPAPISecurity.test_input_validation_sql_injection ___________
tests/security/test_owasp_api_security.py:144: in test_input_validation_sql_injection
    assert response.status_code == status.HTTP_400_BAD_REQUEST
E   assert 403 == 400
E    +  where 403 = <Response status_code=403, "application/json">.status_code
E    +  and   400 = status.HTTP_400_BAD_REQUEST
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:14,130 middleware 2096 128093532961664 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:14,131 log 2096 128093532961664 Forbidden: /api/sales-notes/envios/
--------------------------- Captured stderr teardown ---------------------------
Destroying test database for alias 'default'...

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     30  65.91%   33, 49-50, 74-75, 81-99, 105, 116-117, 137-138, 149, 163-182, 227-228
audit/models.py                                               79      3  96.20%   105, 222, 289
audit/signals.py                                              77     52  32.47%   18-34, 40-69, 75-96, 102-112, 118-141, 163-170, 176-188
audit/tasks.py                                                 0      0 100.00%
authentication/apps.py                                         7      0 100.00%
authentication/management/commands/create_test_users.py       23     23   0.00%   4-51
authentication/management/commands/create_user_groups.py      17     17   0.00%   4-31
authentication/models.py                                     129     29  77.52%   146-151, 155-158, 162-165, 214, 282, 286-290, 294-298, 368-369, 375
authentication/permissions.py                                  0      0 100.00%
authentication/serializers.py                                 80     22  72.50%   71-75, 87-89, 136, 171-179, 271-281, 296-299, 361
authentication/urls.py                                         5      0 100.00%
authentication/views.py                                      123     84  31.71%   42-47, 60, 84-100, 142-309, 341-389, 423-453, 476, 498-499
sales_notes/apps.py                                            7      0 100.00%
sales_notes/exception_handler.py                              20     20   0.00%   1-62
sales_notes/existing_models.py                                88      3  96.59%   31, 71, 108
sales_notes/models.py                                        206     34  83.50%   74, 102, 148, 214-230, 234-235, 253, 295, 337, 647-655, 661-662, 678, 683-685, 720-722
sales_notes/permissions.py                                    30     17  43.33%   18-23, 38-43, 57, 61, 65, 69, 77-89
sales_notes/serializers.py                                   278    161  42.09%   30-35, 62-66, 70-74, 78-82, 87-100, 115-119, 131-135, 147-151, 173-213, 219-243, 271-275, 299-303, 307-311, 315-335, 343-399, 406-427, 449-462, 466-476, 480-517, 521-550, 579, 583-587
sales_notes/tasks.py                                           0      0 100.00%
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                          53     26  50.94%   62-77, 81-85, 92-119
-----------------------------------------------------------------------------------------
TOTAL                                                       1324    521  60.65%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 60.65%
=========================== short test summary info ============================
FAILED tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_brute_force_protection
FAILED tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_rate_limiting
FAILED tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_prevent_automated_submission
FAILED tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_api_documentation_access_control
FAILED tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_input_validation_sql_injection
========================= 5 failed, 4 passed in 3.21s ==========================


```


**Resultat:** ✅ Completat correctament


## 4. Cobertura de Codi


### 4.1 Generar Informe de Cobertura


**Temps d'execució:** 8s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0
django: version: 5.1.2, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.0.0
collected 36 items

tests/integration/test_darp_batch.py F.                                  [  5%]
tests/integration/test_sales_notes_flow.py FFF                           [ 13%]
tests/security/test_owasp_api_security.py .F.F.F.FF                      [ 38%]
tests/unit/test_authentication.py FFFF..                                 [ 55%]
tests/unit/test_models.py EEEEEE                                         [ 72%]
tests/unit/test_permissions.py F....F.F.                                 [ 97%]
tests/integration/test_darp_batch.py F                                   [100%]

==================================== ERRORS ====================================
___________ ERROR at setup of TestEnvioModel.test_create_envio_valid ___________

db = None

    @pytest.fixture
    def api_user(db):
        """Usuari API bàsic (mateix que test_user)"""
        from authentication.models import APIUser
        user = User.objects.create_user(
            username='apiuser',
            password='ApiPassword123!',
            organization='API Test Org'
        )
>       api_user_profile = APIUser.objects.create(
            user=user,
            organization='API Test Org',
            cif_organization='B12345678',
            max_requests_per_day=1000,
            is_api_active=True
        )

tests/conftest.py:330: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:677: in create
    obj = self.model(**kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <APIUser:  - API Test Org>, args = ()
kwargs = {'user': <APIUser: apiuser - API Test Org>}
cls = <class 'authentication.models.APIUser'>, opts = <Options for APIUser>
_setattr = <built-in function setattr>, _DEFERRED = <Deferred field>
fields_iter = <tuple_iterator object at 0x7923e727bc40>, val = None
field = <django.db.models.fields.DateTimeField: updated_at>
is_related_object = False
property_names = frozenset({'is_anonymous', 'is_authenticated', 'pk'})

    def __init__(self, *args, **kwargs):
        # Alias some things as locals to avoid repeat global lookups
        cls = self.__class__
        opts = self._meta
        _setattr = setattr
        _DEFERRED = DEFERRED
        if opts.abstract:
            raise TypeError("Abstract models cannot be instantiated.")
    
        pre_init.send(sender=cls, args=args, kwargs=kwargs)
    
        # Set up the storage for instance state
        self._state = ModelState()
    
        # There is a rather weird disparity here; if kwargs, it's set, then args
        # overrides it. It should be one or the other; don't duplicate the work
        # The reason for the kwargs check is that standard iterator passes in by
        # args, and instantiation for iteration is 33% faster.
        if len(args) > len(opts.concrete_fields):
            # Daft, but matches old exception sans the err msg.
            raise IndexError("Number of args exceeds number of fields")
    
        if not kwargs:
            fields_iter = iter(opts.concrete_fields)
            # The ordering of the zip calls matter - zip throws StopIteration
            # when an iter throws it. So if the first iter throws it, the second
            # is *not* consumed. We rely on this, so don't change the order
            # without changing the logic.
            for val, field in zip(args, fields_iter):
                if val is _DEFERRED:
                    continue
                _setattr(self, field.attname, val)
        else:
            # Slower, kwargs-ready version.
            fields_iter = iter(opts.fields)
            for val, field in zip(args, fields_iter):
                if val is _DEFERRED:
                    continue
                _setattr(self, field.attname, val)
                if kwargs.pop(field.name, NOT_PROVIDED) is not NOT_PROVIDED:
                    raise TypeError(
                        f"{cls.__qualname__}() got both positional and "
                        f"keyword arguments for field '{field.name}'."
                    )
    
        # Now we're left with the unprocessed fields that *must* come from
        # keywords, or default.
    
        for field in fields_iter:
            is_related_object = False
            # Virtual field
            if field.attname not in kwargs and field.column is None or field.generated:
                continue
            if kwargs:
                if isinstance(field.remote_field, ForeignObjectRel):
                    try:
                        # Assume object instance was passed in.
                        rel_obj = kwargs.pop(field.name)
                        is_related_object = True
                    except KeyError:
                        try:
                            # Object instance wasn't passed in -- must be an ID.
                            val = kwargs.pop(field.attname)
                        except KeyError:
                            val = field.get_default()
                else:
                    try:
                        val = kwargs.pop(field.attname)
                    except KeyError:
                        # This is done with an exception rather than the
                        # default argument on pop because we don't want
                        # get_default() to be evaluated, and then not used.
                        # Refs #12057.
                        val = field.get_default()
            else:
                val = field.get_default()
    
            if is_related_object:
                # If we are passed a related instance, set it using the
                # field.name instead of field.attname (e.g. "user" instead of
                # "user_id") so that the object gets properly cached (and type
                # checked) by the RelatedObjectDescriptor.
                if rel_obj is not _DEFERRED:
                    _setattr(self, field.name, rel_obj)
            else:
                if val is not _DEFERRED:
                    _setattr(self, field.attname, val)
    
        if kwargs:
            property_names = opts._property_names
            unexpected = ()
            for prop, value in kwargs.items():
                # Any remaining kwargs must correspond to properties or virtual
                # fields.
                if prop in property_names:
                    if value is not _DEFERRED:
                        _setattr(self, prop, value)
                else:
                    try:
                        opts.get_field(prop)
                    except FieldDoesNotExist:
                        unexpected += (prop,)
                    else:
                        if value is not _DEFERRED:
                            _setattr(self, prop, value)
            if unexpected:
                unexpected_names = ", ".join(repr(n) for n in unexpected)
>               raise TypeError(
                    f"{cls.__name__}() got unexpected keyword arguments: "
                    f"{unexpected_names}"
                )
E               TypeError: APIUser() got unexpected keyword arguments: 'user'

/usr/local/lib/python3.12/site-packages/django/db/models/base.py:567: TypeError
____________ ERROR at setup of TestEnvioModel.test_num_envio_unique ____________

db = None

    @pytest.fixture
    def api_user(db):
        """Usuari API bàsic (mateix que test_user)"""
        from authentication.models import APIUser
        user = User.objects.create_user(
            username='apiuser',
            password='ApiPassword123!',
            organization='API Test Org'
        )
>       api_user_profile = APIUser.objects.create(
            user=user,
            organization='API Test Org',
            cif_organization='B12345678',
            max_requests_per_day=1000,
            is_api_active=True
        )

tests/conftest.py:330: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/usr/local/lib/python3.12/site-packages/django/db/models/manager.py:87: in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:677: in create
    obj = self.model(**kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <APIUser:  - API Test Org>, args = ()
kwargs = {'user': <APIUser: apiuser - API Test Org>}
cls = <class 'authentication.models.APIUser'>, opts = <Options for APIUser>
_setattr = <built-in function setattr>, _DEFERRED = <Deferred field>
fields_iter = <tuple_iterator object at 0x7923e730d7e0>, val = None
field = <django.db.models.fields.DateTimeField: updated_at>
is_related_object = False
property_names = frozenset({'is_anonymous', 'is_authenticated', 'pk'})

    def __init__(self, *args, **kwargs):
        # Alias some things as locals to avoid repeat global lookups
        cls = self.__class__
        opts = self._meta
        _setattr = setattr
        _DEFERRED = DEFERRED
        if opts.abstract:
            raise TypeError("Abstract models cannot be instantiated.")
    
        pre_init.send(sender=cls, args=args, kwargs=kwargs)
    
        # Set up the storage for instance state
        self._state = ModelState()
    
        # There is a rather weird disparity here; if kwargs, it's set, then args
        # overrides it. It should be one or the other; don't duplicate the work
        # The reason for the kwargs check is that standard iterator passes in by
        # args, and instantiation for iteration is 33% faster.
        if len(args) > len(opts.concrete_fields):
            # Daft, but matches old exception sans the err msg.
            raise IndexError("Number of args exceeds number of fields")
    
        if not kwargs:
            fields_iter = iter(opts.concrete_fields)
            # The ordering of the zip calls matter - zip throws StopIteration
            # when an iter throws it. So if the first iter throws it, the second
            # is *not* consumed. We rely on this, so don't change the order
            # without changing the logic.
            for val, field in zip(args, fields_iter):
                if val is _DEFERRED:
                    continue
                _setattr(self, field.attname, val)
        else:
            # Slower, kwargs-ready version.
            fields_iter = iter(opts.fields)
            for val, field in zip(args, fields_iter):
                if val is _DEFERRED:
                    continue
                _setattr(self, field.attname, val)
                if kwargs.pop(field.name, NOT_PROVIDED) is not NOT_PROVIDED:
                    raise TypeError(
                        f"{cls.__qualname__}() got both positional and "
                        f"keyword arguments for field '{field.name}'."
                    )
    
        # Now we're left with the unprocessed fields that *must* come from
        # keywords, or default.
    
        for field in fields_iter:
            is_related_object = False
            # Virtual field
            if field.attname not in kwargs and field.column is None or field.generated:
                continue
            if kwargs:
                if isinstance(field.remote_field, ForeignObjectRel):
                    try:
                        # Assume object instance was passed in.
                        rel_obj = kwargs.pop(field.name)
                        is_related_object = True
                    except KeyError:
                        try:
                            # Object instance wasn't passed in -- must be an ID.
                            val = kwargs.pop(field.attname)
                        except KeyError:
                            val = field.get_default()
                else:
                    try:
                        val = kwargs.pop(field.attname)
                    except KeyError:
                        # This is done with an exception rather than the
                        # default argument on pop because we don't want
                        # get_default() to be evaluated, and then not used.
                        # Refs #12057.
                        val = field.get_default()
            else:
                val = field.get_default()
    
            if is_related_object:
                # If we are passed a related instance, set it using the
                # field.name instead of field.attname (e.g. "user" instead of
                # "user_id") so that the object gets properly cached (and type
                # checked) by the RelatedObjectDescriptor.
                if rel_obj is not _DEFERRED:
                    _setattr(self, field.name, rel_obj)
            else:
                if val is not _DEFERRED:
                    _setattr(self, field.attname, val)
    
        if kwargs:
            property_names = opts._property_names
            unexpected = ()
            for prop, value in kwargs.items():
                # Any remaining kwargs must correspond to properties or virtual
                # fields.
                if prop in property_names:
                    if value is not _DEFERRED:
                        _setattr(self, prop, value)
                else:
                    try:
                        opts.get_field(prop)
                    except FieldDoesNotExist:
                        unexpected += (prop,)
                    else:
                        if value is not _DEFERRED:
                            _setattr(self, prop, value)
            if unexpected:
                unexpected_names = ", ".join(repr(n) for n in unexpected)
>               raise TypeError(
                    f"{cls.__name__}() got unexpected keyword arguments: "
                    f"{unexpected_names}"
                )
E               TypeError: APIUser() got unexpected keyword arguments: 'user'

/usr/local/lib/python3.12/site-packages/django/db/models/base.py:567: TypeError
________ ERROR at setup of TestEnvioAPI.test_create_envio_authenticated ________
file /app/tests/unit/test_models.py, line 32
      def test_create_envio_authenticated(self, api_client, auth_token, sample_envio_data):
E       fixture 'auth_token' not found
>       available fixtures: _dj_autoclear_mailbox, _django_clear_site_cache, _django_db_helper, _django_db_marker, _django_set_urlconf, _django_setup_unittest, _fail_for_invalid_template_variable, _live_server_helper, _session_faker, _template_string_if_invalid_marker, admin_client, admin_user, api_client, api_user, async_client, async_rf, authenticated_admin_client, authenticated_client, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capture_audit_logs, capture_security_events, client, cov, darp_client, darp_user, db, disable_rate_limiting, django_assert_max_num_queries, django_assert_num_queries, django_capture_on_commit_callbacks, django_db_blocker, django_db_createdb, django_db_keepdb, django_db_modify_db_settings, django_db_modify_db_settings_parallel_suffix, django_db_modify_db_settings_tox_suffix, django_db_modify_db_settings_xdist_suffix, django_db_reset_sequences, django_db_serialized_rollback, django_db_setup, django_db_use_migrations, django_mail_dnsname, django_mail_patch_dns, django_test_environment, django_user_model, django_username_field, doctest_namespace, enable_db_access_for_all_tests, faker, invalid_sales_note_data, investigador_client, investigador_user, live_server, mailoutbox, mock_redis, monkeypatch, multiple_envios, multiple_test_users, no_cover, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, rf, sample_sales_note_data, settings, test_user, test_user_credentials, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory, transactional_db
>       use 'pytest --fixtures [testpath]' for help on them.

/app/tests/unit/test_models.py:32
_______ ERROR at setup of TestEnvioAPI.test_create_envio_unauthenticated _______
file /app/tests/unit/test_models.py, line 40
      def test_create_envio_unauthenticated(self, api_client, sample_envio_data):
E       fixture 'sample_envio_data' not found
>       available fixtures: _dj_autoclear_mailbox, _django_clear_site_cache, _django_db_helper, _django_db_marker, _django_set_urlconf, _django_setup_unittest, _fail_for_invalid_template_variable, _live_server_helper, _session_faker, _template_string_if_invalid_marker, admin_client, admin_user, api_client, api_user, async_client, async_rf, authenticated_admin_client, authenticated_client, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capture_audit_logs, capture_security_events, client, cov, darp_client, darp_user, db, disable_rate_limiting, django_assert_max_num_queries, django_assert_num_queries, django_capture_on_commit_callbacks, django_db_blocker, django_db_createdb, django_db_keepdb, django_db_modify_db_settings, django_db_modify_db_settings_parallel_suffix, django_db_modify_db_settings_tox_suffix, django_db_modify_db_settings_xdist_suffix, django_db_reset_sequences, django_db_serialized_rollback, django_db_setup, django_db_use_migrations, django_mail_dnsname, django_mail_patch_dns, django_test_environment, django_user_model, django_username_field, doctest_namespace, enable_db_access_for_all_tests, faker, invalid_sales_note_data, investigador_client, investigador_user, live_server, mailoutbox, mock_redis, monkeypatch, multiple_envios, multiple_test_users, no_cover, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, rf, sample_sales_note_data, settings, test_user, test_user_credentials, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory, transactional_db
>       use 'pytest --fixtures [testpath]' for help on them.

/app/tests/unit/test_models.py:40
______________ ERROR at setup of TestEnvioAPI.test_rate_limiting _______________
file /app/tests/unit/test_models.py, line 45
      def test_rate_limiting(self, api_client, auth_token, sample_envio_data):
E       fixture 'auth_token' not found
>       available fixtures: _dj_autoclear_mailbox, _django_clear_site_cache, _django_db_helper, _django_db_marker, _django_set_urlconf, _django_setup_unittest, _fail_for_invalid_template_variable, _live_server_helper, _session_faker, _template_string_if_invalid_marker, admin_client, admin_user, api_client, api_user, async_client, async_rf, authenticated_admin_client, authenticated_client, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capture_audit_logs, capture_security_events, client, cov, darp_client, darp_user, db, disable_rate_limiting, django_assert_max_num_queries, django_assert_num_queries, django_capture_on_commit_callbacks, django_db_blocker, django_db_createdb, django_db_keepdb, django_db_modify_db_settings, django_db_modify_db_settings_parallel_suffix, django_db_modify_db_settings_tox_suffix, django_db_modify_db_settings_xdist_suffix, django_db_reset_sequences, django_db_serialized_rollback, django_db_setup, django_db_use_migrations, django_mail_dnsname, django_mail_patch_dns, django_test_environment, django_user_model, django_username_field, doctest_namespace, enable_db_access_for_all_tests, faker, invalid_sales_note_data, investigador_client, investigador_user, live_server, mailoutbox, mock_redis, monkeypatch, multiple_envios, multiple_test_users, no_cover, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, rf, sample_sales_note_data, settings, test_user, test_user_credentials, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory, transactional_db
>       use 'pytest --fixtures [testpath]' for help on them.

/app/tests/unit/test_models.py:45
_____ ERROR at setup of TestOWASPCompliance.test_sql_injection_protection ______
file /app/tests/unit/test_models.py, line 60
      def test_sql_injection_protection(self, api_client, auth_token):
E       fixture 'auth_token' not found
>       available fixtures: _dj_autoclear_mailbox, _django_clear_site_cache, _django_db_helper, _django_db_marker, _django_set_urlconf, _django_setup_unittest, _fail_for_invalid_template_variable, _live_server_helper, _session_faker, _template_string_if_invalid_marker, admin_client, admin_user, api_client, api_user, async_client, async_rf, authenticated_admin_client, authenticated_client, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capture_audit_logs, capture_security_events, client, cov, darp_client, darp_user, db, disable_rate_limiting, django_assert_max_num_queries, django_assert_num_queries, django_capture_on_commit_callbacks, django_db_blocker, django_db_createdb, django_db_keepdb, django_db_modify_db_settings, django_db_modify_db_settings_parallel_suffix, django_db_modify_db_settings_tox_suffix, django_db_modify_db_settings_xdist_suffix, django_db_reset_sequences, django_db_serialized_rollback, django_db_setup, django_db_use_migrations, django_mail_dnsname, django_mail_patch_dns, django_test_environment, django_user_model, django_username_field, doctest_namespace, enable_db_access_for_all_tests, faker, invalid_sales_note_data, investigador_client, investigador_user, live_server, mailoutbox, mock_redis, monkeypatch, multiple_envios, multiple_test_users, no_cover, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, rf, sample_sales_note_data, settings, test_user, test_user_credentials, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory, transactional_db
>       use 'pytest --fixtures [testpath]' for help on them.

/app/tests/unit/test_models.py:60
=================================== FAILURES ===================================
____________ TestDARPBatchSubmission.test_batch_submission_success _____________

self = <app.tests.integration.test_darp_batch.TestDARPBatchSubmission object at 0x7923e7955550>
darp_client = <rest_framework.test.APIClient object at 0x7923e6fa97f0>
sample_sales_note_data = {'EstablecimientosVenta': {'EstablecimientoVenta': [{'NombreEstablecimiento': 'Llotja de Test', 'NumIdentificacionEstablec': 'LLOTJA_TEST', 'Ventas': {'VentasUnidadProductiva': [{...}]}}]}, 'NumEnvio': 'TEST_001', 'TipoRespuesta': 1}

    def test_batch_submission_success(self, darp_client, sample_sales_note_data):
        """Test: Enviar batch de 10 notes de venda amb èxit"""
        url = '/api/sales-notes/envios/'
        created_envios = []
    
        # Enviar 10 enviaments
        for i in range(10):
            # Modificar num_envio per fer-lo únic
            data = sample_sales_note_data.copy()
            data['NumEnvio'] = f'BATCH_TEST_{i:04d}'
    
            response = darp_client.post(url, data, format='json')
    
>           assert response.status_code == status.HTTP_201_CREATED
E           assert 400 == 201
E            +  where 400 = <Response status_code=400, "application/json">.status_code
E            +  and   201 = status.HTTP_201_CREATED

tests/integration/test_darp_batch.py:26: AssertionError
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:21,149 log 2494 133195374553984 Bad Request: /api/sales-notes/envios/
___________ TestSalesNotesCompleteFlow.test_darp_complete_lifecycle ____________

self = <app.tests.integration.test_sales_notes_flow.TestSalesNotesCompleteFlow object at 0x7923e776b4a0>
darp_client = <rest_framework.test.APIClient object at 0x7923e735fce0>
darp_user = <APIUser: darp_user - DARP - Generalitat de Catalunya>
sample_sales_note_data = {'EstablecimientosVenta': {'EstablecimientoVenta': [{'NombreEstablecimiento': 'Llotja de Test', 'NumIdentificacionEstablec': 'LLOTJA_TEST', 'Ventas': {'VentasUnidadProductiva': [{...}]}}]}, 'NumEnvio': 'TEST_001', 'TipoRespuesta': 1}

    def test_darp_complete_lifecycle(self, darp_client, darp_user, sample_sales_note_data):
        """Test: Cicle de vida complet DARP - crear i consultar enviament"""
    
        # 1. Crear nota de venda
        create_url = '/api/sales-notes/envios/'
    
        response_create = darp_client.post(create_url, sample_sales_note_data, format='json')
    
>       assert response_create.status_code == status.HTTP_201_CREATED
E       assert 400 == 201
E        +  where 400 = <Response status_code=400, "application/json">.status_code
E        +  and   201 = status.HTTP_201_CREATED

tests/integration/test_sales_notes_flow.py:20: AssertionError
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:21,546 log 2494 133195374553984 Bad Request: /api/sales-notes/envios/
_________ TestSalesNotesCompleteFlow.test_investigador_read_only_flow __________

self = <app.tests.integration.test_sales_notes_flow.TestSalesNotesCompleteFlow object at 0x7923e7784620>
investigador_client = <rest_framework.test.APIClient object at 0x7923e7080d40>
darp_client = <rest_framework.test.APIClient object at 0x7923e7080d40>
sample_sales_note_data = {'EstablecimientosVenta': {'EstablecimientoVenta': [{'NombreEstablecimiento': 'Llotja de Test', 'NumIdentificacionEstablec': 'LLOTJA_TEST', 'Ventas': {'VentasUnidadProductiva': [{...}]}}]}, 'NumEnvio': 'TEST_001', 'TipoRespuesta': 1}

    def test_investigador_read_only_flow(self, investigador_client, darp_client, sample_sales_note_data):
        """Test: Investigador només pot llegir, no crear"""
    
        # 1. Investigador intenta crear (hauria de fallar)
        create_url = '/api/sales-notes/envios/'
        response_create = investigador_client.post(create_url, sample_sales_note_data, format='json')
    
>       assert response_create.status_code == status.HTTP_403_FORBIDDEN
E       assert 400 == 403
E        +  where 400 = <Response status_code=400, "application/json">.status_code
E        +  and   403 = status.HTTP_403_FORBIDDEN

tests/integration/test_sales_notes_flow.py:61: AssertionError
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:21,646 log 2494 133195374553984 Bad Request: /api/sales-notes/envios/
_____________ TestSalesNotesCompleteFlow.test_filtering_and_search _____________

self = <app.tests.integration.test_sales_notes_flow.TestSalesNotesCompleteFlow object at 0x7923e7784770>
darp_client = <rest_framework.test.APIClient object at 0x7923e7080830>
multiple_envios = {'darp_envios': [<Envio: Envio DARP_ENV_001 - 2025-11-18 11:52:21.734562+00:00>, <Envio: Envio DARP_ENV_002 - 2025-11-18 11:52:21.737374+00:00>], 'other_envios': [<Envio: Envio OTHER_ENV_001 - 2025-11-18 11:52:21.738957+00:00>]}

    def test_filtering_and_search(self, darp_client, multiple_envios):
        """Test: Filtres i cerca funcionen correctament"""
    
        # 1. Filtrar per tipo_respuesta
        url = '/api/sales-notes/envios/?tipo_respuesta=1'
        response = darp_client.get(url)
    
        assert response.status_code == status.HTTP_200_OK
        assert all(e['tipo_respuesta'] == 1 for e in response.data)
    
        # 2. Cerca per num_envio
        url = '/api/sales-notes/envios/?search=DARP_ENV_001'
>       response = darp_client.get(url)

tests/integration/test_sales_notes_flow.py:94: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/usr/local/lib/python3.12/site-packages/rest_framework/test.py:288: in get
    response = super().get(path, data=data, **extra)
/usr/local/lib/python3.12/site-packages/rest_framework/test.py:205: in get
    return self.generic('GET', path, **r)
/usr/local/lib/python3.12/site-packages/rest_framework/test.py:233: in generic
    return super().generic(
/usr/local/lib/python3.12/site-packages/django/test/client.py:676: in generic
    return self.request(**r)
/usr/local/lib/python3.12/site-packages/rest_framework/test.py:285: in request
    return super().request(**kwargs)
/usr/local/lib/python3.12/site-packages/rest_framework/test.py:237: in request
    request = super().request(**kwargs)
/usr/local/lib/python3.12/site-packages/django/test/client.py:1092: in request
    self.check_exception(response)
/usr/local/lib/python3.12/site-packages/django/test/client.py:805: in check_exception
    raise exc_value
/usr/local/lib/python3.12/site-packages/django/core/handlers/exception.py:55: in inner
    response = get_response(request)
/usr/local/lib/python3.12/site-packages/django/core/handlers/base.py:197: in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
/usr/local/lib/python3.12/site-packages/django/views/decorators/csrf.py:65: in _view_wrapper
    return view_func(request, *args, **kwargs)
/usr/local/lib/python3.12/site-packages/rest_framework/viewsets.py:124: in view
    return self.dispatch(request, *args, **kwargs)
/usr/local/lib/python3.12/site-packages/rest_framework/views.py:509: in dispatch
    response = self.handle_exception(exc)
/usr/local/lib/python3.12/site-packages/rest_framework/views.py:469: in handle_exception
    self.raise_uncaught_exception(exc)
/usr/local/lib/python3.12/site-packages/rest_framework/views.py:480: in raise_uncaught_exception
    raise exc
/usr/local/lib/python3.12/site-packages/rest_framework/views.py:506: in dispatch
    response = handler(request, *args, **kwargs)
/usr/local/lib/python3.12/site-packages/rest_framework/mixins.py:38: in list
    queryset = self.filter_queryset(self.get_queryset())
/usr/local/lib/python3.12/site-packages/rest_framework/generics.py:154: in filter_queryset
    queryset = backend().filter_queryset(self.request, queryset, self)
/usr/local/lib/python3.12/site-packages/rest_framework/filters.py:167: in filter_queryset
    queryset = queryset.filter(reduce(operator.and_, conditions))
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:1476: in filter
    return self._filter_or_exclude(False, args, kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:1494: in _filter_or_exclude
    clone._filter_or_exclude_inplace(negate, args, kwargs)
/usr/local/lib/python3.12/site-packages/django/db/models/query.py:1501: in _filter_or_exclude_inplace
    self._query.add_q(Q(*args, **kwargs))
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1609: in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1641: in _add_q
    child_clause, needed_inner = self.build_filter(
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1468: in build_filter
    return self._add_q(
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1641: in _add_q
    child_clause, needed_inner = self.build_filter(
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1555: in build_filter
    condition = self.build_lookup(lookups, col, value)
/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1372: in build_lookup
    lhs = self.try_transform(lhs, name)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <django.db.models.sql.query.Query object at 0x7923e7349d60>
lhs = Col(establecimiento_venta, sales_notes.EstablecimientoVenta.id)
name = 'nombre_establecimiento'

    def try_transform(self, lhs, name):
        """
        Helper method for build_lookup(). Try to fetch and initialize
        a transform for name parameter from lhs.
        """
        transform_class = lhs.get_transform(name)
        if transform_class:
            return transform_class(lhs)
        else:
            output_field = lhs.output_field.__class__
            suggested_lookups = difflib.get_close_matches(
                name, lhs.output_field.get_lookups()
            )
            if suggested_lookups:
                suggestion = ", perhaps you meant %s?" % " or ".join(suggested_lookups)
            else:
                suggestion = "."
>           raise FieldError(
                "Unsupported lookup '%s' for %s or join on the field not "
                "permitted%s" % (name, output_field.__name__, suggestion)
            )
E           django.core.exceptions.FieldError: Unsupported lookup 'nombre_establecimiento' for ManyToOneRel or join on the field not permitted.

/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py:1423: FieldError
---------------------------- Captured stderr setup -----------------------------
INFO 2025-11-18 12:52:21,737 signals 2494 133195374553984 Auditat creació d'enviament DARP_ENV_001
INFO 2025-11-18 12:52:21,738 signals 2494 133195374553984 Auditat creació d'enviament DARP_ENV_002
INFO 2025-11-18 12:52:21,740 signals 2494 133195374553984 Auditat creació d'enviament OTHER_ENV_001
----------------------------- Captured stderr call -----------------------------
ERROR 2025-11-18 12:52:21,764 log 2494 133195374553984 Internal Server Error: /api/sales-notes/envios/
Traceback (most recent call last):
  File "/usr/local/lib/python3.12/site-packages/django/core/handlers/exception.py", line 55, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/core/handlers/base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/views/decorators/csrf.py", line 65, in _view_wrapper
    return view_func(request, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/viewsets.py", line 124, in view
    return self.dispatch(request, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/views.py", line 509, in dispatch
    response = self.handle_exception(exc)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/views.py", line 469, in handle_exception
    self.raise_uncaught_exception(exc)
  File "/usr/local/lib/python3.12/site-packages/rest_framework/views.py", line 480, in raise_uncaught_exception
    raise exc
  File "/usr/local/lib/python3.12/site-packages/rest_framework/views.py", line 506, in dispatch
    response = handler(request, *args, **kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/mixins.py", line 38, in list
    queryset = self.filter_queryset(self.get_queryset())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/generics.py", line 154, in filter_queryset
    queryset = backend().filter_queryset(self.request, queryset, self)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/rest_framework/filters.py", line 167, in filter_queryset
    queryset = queryset.filter(reduce(operator.and_, conditions))
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/query.py", line 1476, in filter
    return self._filter_or_exclude(False, args, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/query.py", line 1494, in _filter_or_exclude
    clone._filter_or_exclude_inplace(negate, args, kwargs)
  File "/usr/local/lib/python3.12/site-packages/django/db/models/query.py", line 1501, in _filter_or_exclude_inplace
    self._query.add_q(Q(*args, **kwargs))
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1609, in add_q
    clause, _ = self._add_q(q_object, self.used_aliases)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1641, in _add_q
    child_clause, needed_inner = self.build_filter(
                                 ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1468, in build_filter
    return self._add_q(
           ^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1641, in _add_q
    child_clause, needed_inner = self.build_filter(
                                 ^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1555, in build_filter
    condition = self.build_lookup(lookups, col, value)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1372, in build_lookup
    lhs = self.try_transform(lhs, name)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/django/db/models/sql/query.py", line 1423, in try_transform
    raise FieldError(
django.core.exceptions.FieldError: Unsupported lookup 'nombre_establecimiento' for ManyToOneRel or join on the field not permitted.
_______________ TestOWASPAPISecurity.test_brute_force_protection _______________

self = <app.tests.security.test_owasp_api_security.TestOWASPAPISecurity object at 0x7923e7787590>
api_client = <rest_framework.test.APIClient object at 0x7923e72e1580>

    def test_brute_force_protection(self, api_client):
        """Test: Protecció contra brute force"""
>       url = reverse('authentication:token_obtain_pair')

tests/security/test_owasp_api_security.py:27: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/usr/local/lib/python3.12/site-packages/django/urls/base.py:88: in reverse
    return resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <URLResolver <URLResolver list> (None:None) '^/'>
lookup_view = 'token_obtain_pair', _prefix = '/', args = (), kwargs = {}
possibilities = []

    def _reverse_with_prefix(self, lookup_view, _prefix, *args, **kwargs):
        if args and kwargs:
            raise ValueError("Don't mix *args and **kwargs in call to reverse()!")
    
        if not self._populated:
            self._populate()
    
        possibilities = self.reverse_dict.getlist(lookup_view)
    
        for possibility, pattern, defaults, converters in possibilities:
            for result, params in possibility:
                if args:
                    if len(args) != len(params):
                        continue
                    candidate_subs = dict(zip(params, args))
                else:
                    if set(kwargs).symmetric_difference(params).difference(defaults):
                        continue
                    matches = True
                    for k, v in defaults.items():
                        if k in params:
                            continue
                        if kwargs.get(k, v) != v:
                            matches = False
                            break
                    if not matches:
                        continue
                    candidate_subs = kwargs
                # Convert the candidate subs to text using Converter.to_url().
                text_candidate_subs = {}
                match = True
                for k, v in candidate_subs.items():
                    if k in converters:
                        try:
                            text_candidate_subs[k] = converters[k].to_url(v)
                        except ValueError:
                            match = False
                            break
                    else:
                        text_candidate_subs[k] = str(v)
                if not match:
                    continue
                # WSGI provides decoded URLs, without %xx escapes, and the URL
                # resolver operates on such URLs. First substitute arguments
                # without quoting to build a decoded URL and look for a match.
                # Then, if we have a match, redo the substitution with quoted
                # arguments in order to return a properly encoded URL.
                candidate_pat = _prefix.replace("%", "%%") + result
                if re.search(
                    "^%s%s" % (re.escape(_prefix), pattern),
                    candidate_pat % text_candidate_subs,
                ):
                    # safe characters from `pchar` definition of RFC 3986
                    url = quote(
                        candidate_pat % text_candidate_subs,
                        safe=RFC3986_SUBDELIMS + "/~:@",
                    )
                    # Don't allow construction of scheme relative urls.
                    return escape_leading_slashes(url)
        # lookup_view can be URL name or callable, but callables are not
        # friendly in error messages.
        m = getattr(lookup_view, "__module__", None)
        n = getattr(lookup_view, "__name__", None)
        if m is not None and n is not None:
            lookup_view_s = "%s.%s" % (m, n)
        else:
            lookup_view_s = lookup_view
    
        patterns = [pattern for (_, pattern, _, _) in possibilities]
        if patterns:
            if args:
                arg_msg = "arguments '%s'" % (args,)
            elif kwargs:
                arg_msg = "keyword arguments '%s'" % kwargs
            else:
                arg_msg = "no arguments"
            msg = "Reverse for '%s' with %s not found. %d pattern(s) tried: %s" % (
                lookup_view_s,
                arg_msg,
                len(patterns),
                patterns,
            )
        else:
            msg = (
                "Reverse for '%(view)s' not found. '%(view)s' is not "
                "a valid view function or pattern name." % {"view": lookup_view_s}
            )
>       raise NoReverseMatch(msg)
E       django.urls.exceptions.NoReverseMatch: Reverse for 'token_obtain_pair' not found. 'token_obtain_pair' is not a valid view function or pattern name.

/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py:831: NoReverseMatch
___________________ TestOWASPAPISecurity.test_rate_limiting ____________________

self = <app.tests.security.test_owasp_api_security.TestOWASPAPISecurity object at 0x7923e7786ab0>
api_client = <rest_framework.test.APIClient object at 0x7923e7082b10>

    def test_rate_limiting(self, api_client):
        """Test: Rate limiting funciona"""
>       url = reverse('authentication:token_obtain_pair')

tests/security/test_owasp_api_security.py:62: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/usr/local/lib/python3.12/site-packages/django/urls/base.py:88: in reverse
    return resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <URLResolver <URLResolver list> (None:None) '^/'>
lookup_view = 'token_obtain_pair', _prefix = '/', args = (), kwargs = {}
possibilities = []

    def _reverse_with_prefix(self, lookup_view, _prefix, *args, **kwargs):
        if args and kwargs:
            raise ValueError("Don't mix *args and **kwargs in call to reverse()!")
    
        if not self._populated:
            self._populate()
    
        possibilities = self.reverse_dict.getlist(lookup_view)
    
        for possibility, pattern, defaults, converters in possibilities:
            for result, params in possibility:
                if args:
                    if len(args) != len(params):
                        continue
                    candidate_subs = dict(zip(params, args))
                else:
                    if set(kwargs).symmetric_difference(params).difference(defaults):
                        continue
                    matches = True
                    for k, v in defaults.items():
                        if k in params:
                            continue
                        if kwargs.get(k, v) != v:
                            matches = False
                            break
                    if not matches:
                        continue
                    candidate_subs = kwargs
                # Convert the candidate subs to text using Converter.to_url().
                text_candidate_subs = {}
                match = True
                for k, v in candidate_subs.items():
                    if k in converters:
                        try:
                            text_candidate_subs[k] = converters[k].to_url(v)
                        except ValueError:
                            match = False
                            break
                    else:
                        text_candidate_subs[k] = str(v)
                if not match:
                    continue
                # WSGI provides decoded URLs, without %xx escapes, and the URL
                # resolver operates on such URLs. First substitute arguments
                # without quoting to build a decoded URL and look for a match.
                # Then, if we have a match, redo the substitution with quoted
                # arguments in order to return a properly encoded URL.
                candidate_pat = _prefix.replace("%", "%%") + result
                if re.search(
                    "^%s%s" % (re.escape(_prefix), pattern),
                    candidate_pat % text_candidate_subs,
                ):
                    # safe characters from `pchar` definition of RFC 3986
                    url = quote(
                        candidate_pat % text_candidate_subs,
                        safe=RFC3986_SUBDELIMS + "/~:@",
                    )
                    # Don't allow construction of scheme relative urls.
                    return escape_leading_slashes(url)
        # lookup_view can be URL name or callable, but callables are not
        # friendly in error messages.
        m = getattr(lookup_view, "__module__", None)
        n = getattr(lookup_view, "__name__", None)
        if m is not None and n is not None:
            lookup_view_s = "%s.%s" % (m, n)
        else:
            lookup_view_s = lookup_view
    
        patterns = [pattern for (_, pattern, _, _) in possibilities]
        if patterns:
            if args:
                arg_msg = "arguments '%s'" % (args,)
            elif kwargs:
                arg_msg = "keyword arguments '%s'" % kwargs
            else:
                arg_msg = "no arguments"
            msg = "Reverse for '%s' with %s not found. %d pattern(s) tried: %s" % (
                lookup_view_s,
                arg_msg,
                len(patterns),
                patterns,
            )
        else:
            msg = (
                "Reverse for '%(view)s' not found. '%(view)s' is not "
                "a valid view function or pattern name." % {"view": lookup_view_s}
            )
>       raise NoReverseMatch(msg)
E       django.urls.exceptions.NoReverseMatch: Reverse for 'token_obtain_pair' not found. 'token_obtain_pair' is not a valid view function or pattern name.

/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py:831: NoReverseMatch
____________ TestOWASPAPISecurity.test_prevent_automated_submission ____________

self = <app.tests.security.test_owasp_api_security.TestOWASPAPISecurity object at 0x7923e77876e0>
authenticated_client = <rest_framework.test.APIClient object at 0x7923e6f94560>

    def test_prevent_automated_submission(self, authenticated_client):
        """Test: Prevenir enviaments automatitzats massius"""
        url = '/api/sales-notes/envios/'
    
        # Intentar crear moltes notes de venda ràpidament
        responses = []
        for i in range(20):
            data = {
                'NumEnvio': f'TEST{i:04d}',
                'TipoRespuesta': 1,
                # ... més camps
            }
            response = authenticated_client.post(url, data)
            responses.append(response.status_code)
    
        # Hauria d'haver rate limiting
>       assert status.HTTP_429_TOO_MANY_REQUESTS in responses
E       assert 429 in [403, 403, 403, 403, 403, 403, ...]
E        +  where 429 = status.HTTP_429_TOO_MANY_REQUESTS

tests/security/test_owasp_api_security.py:104: AssertionError
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:22,444 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,445 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,449 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,449 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,452 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,453 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,456 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,457 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,460 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,461 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,464 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,465 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,468 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,468 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,471 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,472 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,475 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,475 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,478 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,479 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,482 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,483 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,485 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,486 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,489 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,490 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,493 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,493 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,496 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,497 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,500 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,501 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,503 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,504 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,507 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,508 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,511 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,511 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
WARNING 2025-11-18 12:52:22,514 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,515 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
__________ TestOWASPAPISecurity.test_api_documentation_access_control __________

self = <app.tests.security.test_owasp_api_security.TestOWASPAPISecurity object at 0x7923e77acdd0>
api_client = <rest_framework.test.APIClient object at 0x7923e7083020>

    def test_api_documentation_access_control(self, api_client):
        """Test: Documentació API no accessible públicament en producció"""
        response = api_client.get('/api/docs/')
    
        # En producció hauria d'estar restringida
        if not settings.DEBUG:
>           assert response.status_code == status.HTTP_403_FORBIDDEN
E           assert 200 == 403
E            +  where 200 = <Response status_code=200, "text/html; charset=utf-8">.status_code
E            +  and   403 = status.HTTP_403_FORBIDDEN

tests/security/test_owasp_api_security.py:128: AssertionError
___________ TestOWASPAPISecurity.test_input_validation_sql_injection ___________

self = <app.tests.security.test_owasp_api_security.TestOWASPAPISecurity object at 0x7923e77ad400>
authenticated_client = <rest_framework.test.APIClient object at 0x7923e7250200>

    def test_input_validation_sql_injection(self, authenticated_client):
        """Test: Validació d'inputs contra SQL injection"""
        url = '/api/sales-notes/envios/'
    
        # Intent de SQL injection
        data = {
            'NumEnvio': "'; DROP TABLE sales_notes; --",
            'TipoRespuesta': 1
        }
    
        response = authenticated_client.post(url, data)
    
        # Hauria de fallar la validació, no executar SQL
>       assert response.status_code == status.HTTP_400_BAD_REQUEST
E       assert 403 == 400
E        +  where 403 = <Response status_code=403, "application/json">.status_code
E        +  and   400 = status.HTTP_400_BAD_REQUEST

tests/security/test_owasp_api_security.py:144: AssertionError
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:22,591 middleware 2494 133195374553984 Event de seguretat: UNAUTHORIZED_ACCESS - Intent d'accés no autoritzat a /api/sales-notes/envios/ (IP: 127.0.0.1, User: testuser - ICATMAR Test)
WARNING 2025-11-18 12:52:22,593 log 2494 133195374553984 Forbidden: /api/sales-notes/envios/
_______________ TestJWTAuthentication.test_obtain_token_success ________________

self = <app.tests.unit.test_authentication.TestJWTAuthentication object at 0x7923e77ae930>
api_client = <rest_framework.test.APIClient object at 0x7923e72520f0>
test_user = <APIUser: testuser - ICATMAR Test>

    def test_obtain_token_success(self, api_client, test_user):
        """Test: Obtenir token amb credencials vàlides"""
>       url = reverse('authentication:token_obtain_pair')

tests/unit/test_authentication.py:15: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/usr/local/lib/python3.12/site-packages/django/urls/base.py:88: in reverse
    return resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <URLResolver <URLResolver list> (None:None) '^/'>
lookup_view = 'token_obtain_pair', _prefix = '/', args = (), kwargs = {}
possibilities = []

    def _reverse_with_prefix(self, lookup_view, _prefix, *args, **kwargs):
        if args and kwargs:
            raise ValueError("Don't mix *args and **kwargs in call to reverse()!")
    
        if not self._populated:
            self._populate()
    
        possibilities = self.reverse_dict.getlist(lookup_view)
    
        for possibility, pattern, defaults, converters in possibilities:
            for result, params in possibility:
                if args:
                    if len(args) != len(params):
                        continue
                    candidate_subs = dict(zip(params, args))
                else:
                    if set(kwargs).symmetric_difference(params).difference(defaults):
                        continue
                    matches = True
                    for k, v in defaults.items():
                        if k in params:
                            continue
                        if kwargs.get(k, v) != v:
                            matches = False
                            break
                    if not matches:
                        continue
                    candidate_subs = kwargs
                # Convert the candidate subs to text using Converter.to_url().
                text_candidate_subs = {}
                match = True
                for k, v in candidate_subs.items():
                    if k in converters:
                        try:
                            text_candidate_subs[k] = converters[k].to_url(v)
                        except ValueError:
                            match = False
                            break
                    else:
                        text_candidate_subs[k] = str(v)
                if not match:
                    continue
                # WSGI provides decoded URLs, without %xx escapes, and the URL
                # resolver operates on such URLs. First substitute arguments
                # without quoting to build a decoded URL and look for a match.
                # Then, if we have a match, redo the substitution with quoted
                # arguments in order to return a properly encoded URL.
                candidate_pat = _prefix.replace("%", "%%") + result
                if re.search(
                    "^%s%s" % (re.escape(_prefix), pattern),
                    candidate_pat % text_candidate_subs,
                ):
                    # safe characters from `pchar` definition of RFC 3986
                    url = quote(
                        candidate_pat % text_candidate_subs,
                        safe=RFC3986_SUBDELIMS + "/~:@",
                    )
                    # Don't allow construction of scheme relative urls.
                    return escape_leading_slashes(url)
        # lookup_view can be URL name or callable, but callables are not
        # friendly in error messages.
        m = getattr(lookup_view, "__module__", None)
        n = getattr(lookup_view, "__name__", None)
        if m is not None and n is not None:
            lookup_view_s = "%s.%s" % (m, n)
        else:
            lookup_view_s = lookup_view
    
        patterns = [pattern for (_, pattern, _, _) in possibilities]
        if patterns:
            if args:
                arg_msg = "arguments '%s'" % (args,)
            elif kwargs:
                arg_msg = "keyword arguments '%s'" % kwargs
            else:
                arg_msg = "no arguments"
            msg = "Reverse for '%s' with %s not found. %d pattern(s) tried: %s" % (
                lookup_view_s,
                arg_msg,
                len(patterns),
                patterns,
            )
        else:
            msg = (
                "Reverse for '%(view)s' not found. '%(view)s' is not "
                "a valid view function or pattern name." % {"view": lookup_view_s}
            )
>       raise NoReverseMatch(msg)
E       django.urls.exceptions.NoReverseMatch: Reverse for 'token_obtain_pair' not found. 'token_obtain_pair' is not a valid view function or pattern name.

/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py:831: NoReverseMatch
_________ TestJWTAuthentication.test_obtain_token_invalid_credentials __________

self = <app.tests.unit.test_authentication.TestJWTAuthentication object at 0x7923e77adfd0>
api_client = <rest_framework.test.APIClient object at 0x7923e727a420>
test_user = <APIUser: testuser - ICATMAR Test>

    def test_obtain_token_invalid_credentials(self, api_client, test_user):
        """Test: Token amb credencials invàlides"""
>       url = reverse('authentication:token_obtain_pair')

tests/unit/test_authentication.py:29: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/usr/local/lib/python3.12/site-packages/django/urls/base.py:88: in reverse
    return resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <URLResolver <URLResolver list> (None:None) '^/'>
lookup_view = 'token_obtain_pair', _prefix = '/', args = (), kwargs = {}
possibilities = []

    def _reverse_with_prefix(self, lookup_view, _prefix, *args, **kwargs):
        if args and kwargs:
            raise ValueError("Don't mix *args and **kwargs in call to reverse()!")
    
        if not self._populated:
            self._populate()
    
        possibilities = self.reverse_dict.getlist(lookup_view)
    
        for possibility, pattern, defaults, converters in possibilities:
            for result, params in possibility:
                if args:
                    if len(args) != len(params):
                        continue
                    candidate_subs = dict(zip(params, args))
                else:
                    if set(kwargs).symmetric_difference(params).difference(defaults):
                        continue
                    matches = True
                    for k, v in defaults.items():
                        if k in params:
                            continue
                        if kwargs.get(k, v) != v:
                            matches = False
                            break
                    if not matches:
                        continue
                    candidate_subs = kwargs
                # Convert the candidate subs to text using Converter.to_url().
                text_candidate_subs = {}
                match = True
                for k, v in candidate_subs.items():
                    if k in converters:
                        try:
                            text_candidate_subs[k] = converters[k].to_url(v)
                        except ValueError:
                            match = False
                            break
                    else:
                        text_candidate_subs[k] = str(v)
                if not match:
                    continue
                # WSGI provides decoded URLs, without %xx escapes, and the URL
                # resolver operates on such URLs. First substitute arguments
                # without quoting to build a decoded URL and look for a match.
                # Then, if we have a match, redo the substitution with quoted
                # arguments in order to return a properly encoded URL.
                candidate_pat = _prefix.replace("%", "%%") + result
                if re.search(
                    "^%s%s" % (re.escape(_prefix), pattern),
                    candidate_pat % text_candidate_subs,
                ):
                    # safe characters from `pchar` definition of RFC 3986
                    url = quote(
                        candidate_pat % text_candidate_subs,
                        safe=RFC3986_SUBDELIMS + "/~:@",
                    )
                    # Don't allow construction of scheme relative urls.
                    return escape_leading_slashes(url)
        # lookup_view can be URL name or callable, but callables are not
        # friendly in error messages.
        m = getattr(lookup_view, "__module__", None)
        n = getattr(lookup_view, "__name__", None)
        if m is not None and n is not None:
            lookup_view_s = "%s.%s" % (m, n)
        else:
            lookup_view_s = lookup_view
    
        patterns = [pattern for (_, pattern, _, _) in possibilities]
        if patterns:
            if args:
                arg_msg = "arguments '%s'" % (args,)
            elif kwargs:
                arg_msg = "keyword arguments '%s'" % kwargs
            else:
                arg_msg = "no arguments"
            msg = "Reverse for '%s' with %s not found. %d pattern(s) tried: %s" % (
                lookup_view_s,
                arg_msg,
                len(patterns),
                patterns,
            )
        else:
            msg = (
                "Reverse for '%(view)s' not found. '%(view)s' is not "
                "a valid view function or pattern name." % {"view": lookup_view_s}
            )
>       raise NoReverseMatch(msg)
E       django.urls.exceptions.NoReverseMatch: Reverse for 'token_obtain_pair' not found. 'token_obtain_pair' is not a valid view function or pattern name.

/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py:831: NoReverseMatch
_______________ TestJWTAuthentication.test_refresh_token_success _______________

self = <app.tests.unit.test_authentication.TestJWTAuthentication object at 0x7923e77ae660>
api_client = <rest_framework.test.APIClient object at 0x7923e727a9c0>
test_user = <APIUser: testuser - ICATMAR Test>

    def test_refresh_token_success(self, api_client, test_user):
        """Test: Refrescar token vàlid"""
        # Primer obtenim tokens
>       url_obtain = reverse('authentication:token_obtain_pair')

tests/unit/test_authentication.py:42: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/usr/local/lib/python3.12/site-packages/django/urls/base.py:88: in reverse
    return resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <URLResolver <URLResolver list> (None:None) '^/'>
lookup_view = 'token_obtain_pair', _prefix = '/', args = (), kwargs = {}
possibilities = []

    def _reverse_with_prefix(self, lookup_view, _prefix, *args, **kwargs):
        if args and kwargs:
            raise ValueError("Don't mix *args and **kwargs in call to reverse()!")
    
        if not self._populated:
            self._populate()
    
        possibilities = self.reverse_dict.getlist(lookup_view)
    
        for possibility, pattern, defaults, converters in possibilities:
            for result, params in possibility:
                if args:
                    if len(args) != len(params):
                        continue
                    candidate_subs = dict(zip(params, args))
                else:
                    if set(kwargs).symmetric_difference(params).difference(defaults):
                        continue
                    matches = True
                    for k, v in defaults.items():
                        if k in params:
                            continue
                        if kwargs.get(k, v) != v:
                            matches = False
                            break
                    if not matches:
                        continue
                    candidate_subs = kwargs
                # Convert the candidate subs to text using Converter.to_url().
                text_candidate_subs = {}
                match = True
                for k, v in candidate_subs.items():
                    if k in converters:
                        try:
                            text_candidate_subs[k] = converters[k].to_url(v)
                        except ValueError:
                            match = False
                            break
                    else:
                        text_candidate_subs[k] = str(v)
                if not match:
                    continue
                # WSGI provides decoded URLs, without %xx escapes, and the URL
                # resolver operates on such URLs. First substitute arguments
                # without quoting to build a decoded URL and look for a match.
                # Then, if we have a match, redo the substitution with quoted
                # arguments in order to return a properly encoded URL.
                candidate_pat = _prefix.replace("%", "%%") + result
                if re.search(
                    "^%s%s" % (re.escape(_prefix), pattern),
                    candidate_pat % text_candidate_subs,
                ):
                    # safe characters from `pchar` definition of RFC 3986
                    url = quote(
                        candidate_pat % text_candidate_subs,
                        safe=RFC3986_SUBDELIMS + "/~:@",
                    )
                    # Don't allow construction of scheme relative urls.
                    return escape_leading_slashes(url)
        # lookup_view can be URL name or callable, but callables are not
        # friendly in error messages.
        m = getattr(lookup_view, "__module__", None)
        n = getattr(lookup_view, "__name__", None)
        if m is not None and n is not None:
            lookup_view_s = "%s.%s" % (m, n)
        else:
            lookup_view_s = lookup_view
    
        patterns = [pattern for (_, pattern, _, _) in possibilities]
        if patterns:
            if args:
                arg_msg = "arguments '%s'" % (args,)
            elif kwargs:
                arg_msg = "keyword arguments '%s'" % kwargs
            else:
                arg_msg = "no arguments"
            msg = "Reverse for '%s' with %s not found. %d pattern(s) tried: %s" % (
                lookup_view_s,
                arg_msg,
                len(patterns),
                patterns,
            )
        else:
            msg = (
                "Reverse for '%(view)s' not found. '%(view)s' is not "
                "a valid view function or pattern name." % {"view": lookup_view_s}
            )
>       raise NoReverseMatch(msg)
E       django.urls.exceptions.NoReverseMatch: Reverse for 'token_obtain_pair' not found. 'token_obtain_pair' is not a valid view function or pattern name.

/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py:831: NoReverseMatch
_______________ TestJWTAuthentication.test_verify_token_success ________________

self = <app.tests.unit.test_authentication.TestJWTAuthentication object at 0x7923e77aed50>
api_client = <rest_framework.test.APIClient object at 0x7923e727b440>
test_user = <APIUser: testuser - ICATMAR Test>

    def test_verify_token_success(self, api_client, test_user):
        """Test: Verificar token vàlid"""
        # Obtenir token
>       url_obtain = reverse('authentication:token_obtain_pair')

tests/unit/test_authentication.py:61: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/usr/local/lib/python3.12/site-packages/django/urls/base.py:88: in reverse
    return resolver._reverse_with_prefix(view, prefix, *args, **kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <URLResolver <URLResolver list> (None:None) '^/'>
lookup_view = 'token_obtain_pair', _prefix = '/', args = (), kwargs = {}
possibilities = []

    def _reverse_with_prefix(self, lookup_view, _prefix, *args, **kwargs):
        if args and kwargs:
            raise ValueError("Don't mix *args and **kwargs in call to reverse()!")
    
        if not self._populated:
            self._populate()
    
        possibilities = self.reverse_dict.getlist(lookup_view)
    
        for possibility, pattern, defaults, converters in possibilities:
            for result, params in possibility:
                if args:
                    if len(args) != len(params):
                        continue
                    candidate_subs = dict(zip(params, args))
                else:
                    if set(kwargs).symmetric_difference(params).difference(defaults):
                        continue
                    matches = True
                    for k, v in defaults.items():
                        if k in params:
                            continue
                        if kwargs.get(k, v) != v:
                            matches = False
                            break
                    if not matches:
                        continue
                    candidate_subs = kwargs
                # Convert the candidate subs to text using Converter.to_url().
                text_candidate_subs = {}
                match = True
                for k, v in candidate_subs.items():
                    if k in converters:
                        try:
                            text_candidate_subs[k] = converters[k].to_url(v)
                        except ValueError:
                            match = False
                            break
                    else:
                        text_candidate_subs[k] = str(v)
                if not match:
                    continue
                # WSGI provides decoded URLs, without %xx escapes, and the URL
                # resolver operates on such URLs. First substitute arguments
                # without quoting to build a decoded URL and look for a match.
                # Then, if we have a match, redo the substitution with quoted
                # arguments in order to return a properly encoded URL.
                candidate_pat = _prefix.replace("%", "%%") + result
                if re.search(
                    "^%s%s" % (re.escape(_prefix), pattern),
                    candidate_pat % text_candidate_subs,
                ):
                    # safe characters from `pchar` definition of RFC 3986
                    url = quote(
                        candidate_pat % text_candidate_subs,
                        safe=RFC3986_SUBDELIMS + "/~:@",
                    )
                    # Don't allow construction of scheme relative urls.
                    return escape_leading_slashes(url)
        # lookup_view can be URL name or callable, but callables are not
        # friendly in error messages.
        m = getattr(lookup_view, "__module__", None)
        n = getattr(lookup_view, "__name__", None)
        if m is not None and n is not None:
            lookup_view_s = "%s.%s" % (m, n)
        else:
            lookup_view_s = lookup_view
    
        patterns = [pattern for (_, pattern, _, _) in possibilities]
        if patterns:
            if args:
                arg_msg = "arguments '%s'" % (args,)
            elif kwargs:
                arg_msg = "keyword arguments '%s'" % kwargs
            else:
                arg_msg = "no arguments"
            msg = "Reverse for '%s' with %s not found. %d pattern(s) tried: %s" % (
                lookup_view_s,
                arg_msg,
                len(patterns),
                patterns,
            )
        else:
            msg = (
                "Reverse for '%(view)s' not found. '%(view)s' is not "
                "a valid view function or pattern name." % {"view": lookup_view_s}
            )
>       raise NoReverseMatch(msg)
E       django.urls.exceptions.NoReverseMatch: Reverse for 'token_obtain_pair' not found. 'token_obtain_pair' is not a valid view function or pattern name.

/usr/local/lib/python3.12/site-packages/django/urls/resolvers.py:831: NoReverseMatch
________________ TestUserPermissions.test_darp_can_create_envio ________________

self = <app.tests.unit.test_permissions.TestUserPermissions object at 0x7923e77b2c00>
darp_client = <rest_framework.test.APIClient object at 0x7923e7373a10>
sample_sales_note_data = {'EstablecimientosVenta': {'EstablecimientoVenta': [{'NombreEstablecimiento': 'Llotja de Test', 'NumIdentificacionEstablec': 'LLOTJA_TEST', 'Ventas': {'VentasUnidadProductiva': [{...}]}}]}, 'NumEnvio': 'TEST_001', 'TipoRespuesta': 1}

    def test_darp_can_create_envio(self, darp_client, sample_sales_note_data):
        """Test: DARP pot crear enviaments"""
        url = '/api/sales-notes/envios/'
    
        response = darp_client.post(url, sample_sales_note_data, format='json')
    
>       assert response.status_code == status.HTTP_201_CREATED
E       assert 400 == 201
E        +  where 400 = <Response status_code=400, "application/json">.status_code
E        +  and   201 = status.HTTP_201_CREATED

tests/unit/test_permissions.py:18: AssertionError
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:23,201 log 2494 133195374553984 Bad Request: /api/sales-notes/envios/
_____________ TestUserPermissions.test_darp_can_retrieve_own_envio _____________

self = <app.tests.unit.test_permissions.TestUserPermissions object at 0x7923e77b4f80>
darp_client = <rest_framework.test.APIClient object at 0x7923e7419d00>
multiple_envios = {'darp_envios': [<Envio: Envio DARP_ENV_001 - 2025-11-18 11:52:23.730927+00:00>, <Envio: Envio DARP_ENV_002 - 2025-11-18 11:52:23.732638+00:00>], 'other_envios': [<Envio: Envio OTHER_ENV_001 - 2025-11-18 11:52:23.734070+00:00>]}

    def test_darp_can_retrieve_own_envio(self, darp_client, multiple_envios):
        """Test: DARP pot veure detall dels seus enviaments"""
        envio = multiple_envios['darp_envios'][0]
        url = f'/api/sales-notes/envios/{envio.id}/'
    
        response = darp_client.get(url)
    
        assert response.status_code == status.HTTP_200_OK
>       assert response.data['NumEnvio'] == envio.num_envio
E       KeyError: 'NumEnvio'

tests/unit/test_permissions.py:67: KeyError
---------------------------- Captured stderr setup -----------------------------
INFO 2025-11-18 12:52:23,732 signals 2494 133195374553984 Auditat creació d'enviament DARP_ENV_001
INFO 2025-11-18 12:52:23,733 signals 2494 133195374553984 Auditat creació d'enviament DARP_ENV_002
INFO 2025-11-18 12:52:23,735 signals 2494 133195374553984 Auditat creació d'enviament OTHER_ENV_001
_________ TestUserPermissions.test_investigador_can_retrieve_any_envio _________

self = <app.tests.unit.test_permissions.TestUserPermissions object at 0x7923e77b5cd0>
investigador_client = <rest_framework.test.APIClient object at 0x7923e743e120>
multiple_envios = {'darp_envios': [<Envio: Envio DARP_ENV_001 - 2025-11-18 11:52:23.977050+00:00>, <Envio: Envio DARP_ENV_002 - 2025-11-18 11:52:23.979195+00:00>], 'other_envios': [<Envio: Envio OTHER_ENV_001 - 2025-11-18 11:52:23.980887+00:00>]}

    def test_investigador_can_retrieve_any_envio(self, investigador_client, multiple_envios):
        """Test: Investigador pot veure detall de qualsevol enviament"""
        # Provar amb enviament del DARP
        darp_envio = multiple_envios['darp_envios'][0]
        url = f'/api/sales-notes/envios/{darp_envio.id}/'
    
        response = investigador_client.get(url)
    
        assert response.status_code == status.HTTP_200_OK
>       assert response.data['NumEnvio'] == darp_envio.num_envio
E       KeyError: 'NumEnvio'

tests/unit/test_permissions.py:88: KeyError
---------------------------- Captured stderr setup -----------------------------
INFO 2025-11-18 12:52:23,979 signals 2494 133195374553984 Auditat creació d'enviament DARP_ENV_001
INFO 2025-11-18 12:52:23,980 signals 2494 133195374553984 Auditat creació d'enviament DARP_ENV_002
INFO 2025-11-18 12:52:23,982 signals 2494 133195374553984 Auditat creació d'enviament OTHER_ENV_001
_____________ TestDARPBatchSubmission.test_batch_rollback_on_error _____________

self = <app.tests.integration.test_darp_batch.TestDARPBatchSubmission object at 0x7923e7769d30>
darp_client = <rest_framework.test.APIClient object at 0x7923e73718e0>
sample_sales_note_data = {'EstablecimientosVenta': {'EstablecimientoVenta': [{'NombreEstablecimiento': 'Llotja de Test', 'NumIdentificacionEstablec': 'LLOTJA_TEST', 'Ventas': {'VentasUnidadProductiva': [{...}]}}]}, 'NumEnvio': 'TEST_001', 'TipoRespuesta': 1}

    @pytest.mark.django_db(transaction=True)
    def test_batch_rollback_on_error(self, darp_client, sample_sales_note_data):
        """Test: Si un enviament falla, el batch no es comet (rollback)"""
        url = '/api/sales-notes/envios/'
    
        # Crear 3 enviaments vàlids
        valid_data = sample_sales_note_data.copy()
    
        for i in range(3):
            valid_data['NumEnvio'] = f'VALID_{i}'
            response = darp_client.post(url, valid_data, format='json')
>           assert response.status_code == status.HTTP_201_CREATED
E           assert 400 == 201
E            +  where 400 = <Response status_code=400, "application/json">.status_code
E            +  and   201 = status.HTTP_201_CREATED

tests/integration/test_darp_batch.py:48: AssertionError
----------------------------- Captured stderr call -----------------------------
WARNING 2025-11-18 12:52:24,060 log 2494 133195374553984 Bad Request: /api/sales-notes/envios/

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     14  84.09%   33, 74-75, 96-97, 105, 116-117, 138, 149, 174, 180, 227-228
audit/models.py                                               79      3  96.20%   105, 222, 289
audit/signals.py                                              77     43  44.16%   33-34, 45-57, 68-69, 75-96, 102-112, 118-141, 163-170, 176-188
audit/tasks.py                                                 0      0 100.00%
authentication/apps.py                                         7      0 100.00%
authentication/management/commands/create_test_users.py       23     23   0.00%   4-51
authentication/management/commands/create_user_groups.py      17     17   0.00%   4-31
authentication/models.py                                     129     29  77.52%   146-151, 155-158, 162-165, 214, 282, 286-290, 294-298, 368-369, 375
authentication/permissions.py                                  0      0 100.00%
authentication/serializers.py                                 80     22  72.50%   71-75, 87-89, 136, 171-179, 271-281, 296-299, 361
authentication/urls.py                                         5      0 100.00%
authentication/views.py                                      123     84  31.71%   42-47, 60, 84-100, 142-309, 341-389, 423-453, 476, 498-499
sales_notes/apps.py                                            7      0 100.00%
sales_notes/exception_handler.py                              20     20   0.00%   1-62
sales_notes/existing_models.py                                88      3  96.59%   31, 71, 108
sales_notes/models.py                                        206     33  83.98%   102, 148, 214-230, 234-235, 253, 295, 337, 647-655, 661-662, 678, 683-685, 720-722
sales_notes/permissions.py                                    30      9  70.00%   18-23, 38-43, 57, 78, 89
sales_notes/serializers.py                                   278    152  45.32%   30-35, 62-66, 70-74, 78-82, 87-100, 115-119, 131-135, 147-151, 173-213, 219-243, 271-275, 299-303, 307-311, 315-335, 343-399, 412, 420-424, 449-462, 466-476, 480-517, 521-550, 585-586
sales_notes/tasks.py                                           0      0 100.00%
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                          53     15  71.70%   77, 84, 92-119
-----------------------------------------------------------------------------------------
TOTAL                                                       1324    467  64.73%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 64.73%
=========================== short test summary info ============================
FAILED tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_submission_success
FAILED tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_darp_complete_lifecycle
FAILED tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_investigador_read_only_flow
FAILED tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_filtering_and_search
FAILED tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_brute_force_protection
FAILED tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_rate_limiting
FAILED tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_prevent_automated_submission
FAILED tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_api_documentation_access_control
FAILED tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_input_validation_sql_injection
FAILED tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_success
FAILED tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_invalid_credentials
FAILED tests/unit/test_authentication.py::TestJWTAuthentication::test_refresh_token_success
FAILED tests/unit/test_authentication.py::TestJWTAuthentication::test_verify_token_success
FAILED tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_create_envio
FAILED tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_retrieve_own_envio
FAILED tests/unit/test_permissions.py::TestUserPermissions::test_investigador_can_retrieve_any_envio
FAILED tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_rollback_on_error
ERROR tests/unit/test_models.py::TestEnvioModel::test_create_envio_valid - Ty...
ERROR tests/unit/test_models.py::TestEnvioModel::test_num_envio_unique - Type...
ERROR tests/unit/test_models.py::TestEnvioAPI::test_create_envio_authenticated
ERROR tests/unit/test_models.py::TestEnvioAPI::test_create_envio_unauthenticated
ERROR tests/unit/test_models.py::TestEnvioAPI::test_rate_limiting
ERROR tests/unit/test_models.py::TestOWASPCompliance::test_sql_injection_protection
=================== 17 failed, 13 passed, 6 errors in 6.08s ====================


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
Run started:2025-11-18 11:52:26.142884

Test results:
>> Issue: [B104:hardcoded_bind_all_interfaces] Possible binding to all interfaces.
   Severity: Medium   Confidence: Medium
   CWE: CWE-605 (https://cwe.mitre.org/data/definitions/605.html)
   More Info: https://bandit.readthedocs.io/en/1.7.10/plugins/b104_hardcoded_bind_all_interfaces.html
   Location: ./authentication/views.py:46:45
45	    else:
46	        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
47	    return ip

--------------------------------------------------

Code scanned:
	Total lines of code: 6352
	Total lines skipped (#nosec): 0
	Total potential issues skipped due to specifically being disabled (e.g., #nosec BXXX): 0

Run metrics:
	Total issues (by severity):
		Undefined: 0
		Low: 82
		Medium: 1
		High: 0
	Total issues (by confidence):
		Undefined: 0
		Low: 0
		Medium: 8
		High: 75
Files skipped (0):


```


**Resultat:** ✅ Completat correctament


⚠️ **Safety no disponible**


### 5.3 Django Security Check


**Temps d'execució:** 2s


```


System check identified some issues:

WARNINGS:
?: (django_ratelimit.W001) cache backend django.core.cache.backends.redis.RedisCache is not officially supported
?: (drf_spectacular.W001) /app/authentication/serializers.py: Warning [UserProfileView > UserSerializer]: unable to resolve type hint for function "get_is_account_locked". Consider using a type hint or @extend_schema_field. Defaulting to string.
?: (drf_spectacular.W001) /app/sales_notes/serializers.py: Warning [EnvioViewSet > EnvioListSerializer]: unable to resolve type hint for function "get_num_especies". Consider using a type hint or @extend_schema_field. Defaulting to string.
?: (drf_spectacular.W001) /app/sales_notes/serializers.py: Warning [EnvioViewSet > EnvioListSerializer]: unable to resolve type hint for function "get_num_establecimientos". Consider using a type hint or @extend_schema_field. Defaulting to string.
?: (drf_spectacular.W001) Warning: encountered multiple names for the same choice set (IdTipoNifCifCompradorEnum). This may be unwanted even though the generated schema is technically correct. Add an entry to ENUM_NAME_OVERRIDES to fix the naming.
?: (drf_spectacular.W002) /app/authentication/views.py: Error [LogoutView]: unable to guess serializer. This is graceful fallback handling for APIViews. Consider using GenericAPIView as view base class, if view is under your control. Either way you may want to add a serializer_class (or method). Ignoring view for now.
?: (drf_spectacular.W002) /app/authentication/views.py: Error [PasswordChangeView]: unable to guess serializer. This is graceful fallback handling for APIViews. Consider using GenericAPIView as view base class, if view is under your control. Either way you may want to add a serializer_class (or method). Ignoring view for now.
?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
?: (security.W018) You should not have DEBUG set to True in deployment.

System check identified 12 issues (0 silenced).


```


**Resultat:** ✅ Completat correctament


## 6. Anàlisi de Qualitat de Codi


### 6.1 Linting amb Flake8


**Temps d'execució:** 1s


```


./__init__.py:10:1: E402 module level import not at top of file
./__init__.py:28:1: E402 module level import not at top of file
./__init__.py:46:1: E402 module level import not at top of file
./__init__.py:53:1: W293 blank line contains whitespace
./__init__.py:56:9: F401 'audit.signals' imported but unused
./__init__.py:56:29: W292 no newline at end of file
./audit/apps.py:12:1: W293 blank line contains whitespace
./audit/apps.py:18:43: W292 no newline at end of file
./audit/middleware.py:20:1: W293 blank line contains whitespace
./audit/middleware.py:25:1: W293 blank line contains whitespace
./audit/middleware.py:28:1: W293 blank line contains whitespace
./audit/middleware.py:34:1: W293 blank line contains whitespace
./audit/middleware.py:40:1: W293 blank line contains whitespace
./audit/middleware.py:53:1: W293 blank line contains whitespace
./audit/middleware.py:70:1: W293 blank line contains whitespace
./audit/middleware.py:72:80: E501 line too long (80 > 79 characters)
./audit/middleware.py:73:1: W293 blank line contains whitespace
./audit/middleware.py:75:80: E501 line too long (86 > 79 characters)
./audit/middleware.py:76:1: W293 blank line contains whitespace
./audit/middleware.py:78:1: W293 blank line contains whitespace
./audit/middleware.py:83:1: W293 blank line contains whitespace
./audit/middleware.py:98:1: W293 blank line contains whitespace
./audit/middleware.py:100:1: W293 blank line contains whitespace
./audit/middleware.py:109:1: W293 blank line contains whitespace
./audit/middleware.py:116:13: E722 do not use bare 'except'
./audit/middleware.py:119:1: W293 blank line contains whitespace
./audit/middleware.py:134:1: W293 blank line contains whitespace
./audit/middleware.py:140:80: E501 line too long (82 > 79 characters)
./audit/middleware.py:146:1: W293 blank line contains whitespace
./audit/middleware.py:158:1: W293 blank line contains whitespace
./audit/middleware.py:169:1: W293 blank line contains whitespace
./audit/middleware.py:175:1: W293 blank line contains whitespace
./audit/middleware.py:181:1: W293 blank line contains whitespace
./audit/middleware.py:183:1: W293 blank line contains whitespace
./audit/middleware.py:189:1: W293 blank line contains whitespace
./audit/middleware.py:196:1: W293 blank line contains whitespace
./audit/middleware.py:199:1: W293 blank line contains whitespace
./audit/middleware.py:200:73: W291 trailing whitespace
./audit/middleware.py:201:27: E128 continuation line under-indented for visual indent
./audit/middleware.py:221:1: W293 blank line contains whitespace
./audit/middleware.py:226:1: W293 blank line contains whitespace
./audit/middleware.py:231:14: W292 no newline at end of file
./audit/migrations/0001_initial.py:23:80: E501 line too long (112 > 79 characters)
./audit/migrations/0001_initial.py:42:80: E501 line too long (87 > 79 characters)
./audit/migrations/0001_initial.py:43:80: E501 line too long (85 > 79 characters)
./audit/migrations/0001_initial.py:46:80: E501 line too long (110 > 79 characters)
./audit/migrations/0001_initial.py:50:80: E501 line too long (117 > 79 characters)
./audit/migrations/0001_initial.py:52:80: E501 line too long (84 > 79 characters)
./audit/migrations/0001_initial.py:54:80: E501 line too long (91 > 79 characters)
./audit/migrations/0001_initial.py:69:80: E501 line too long (86 > 79 characters)
./audit/migrations/0001_initial.py:96:80: E501 line too long (101 > 79 characters)
./audit/migrations/0001_initial.py:97:80: E501 line too long (100 > 79 characters)
./audit/migrations/0001_initial.py:98:80: E501 line too long (104 > 79 characters)
./audit/migrations/0001_initial.py:99:80: E501 line too long (106 > 79 characters)
./audit/migrations/0001_initial.py:106:80: E501 line too long (112 > 79 characters)
./audit/migrations/0001_initial.py:107:80: E501 line too long (116 > 79 characters)
./audit/migrations/0001_initial.py:111:80: E501 line too long (109 > 79 characters)
./audit/migrations/0001_initial.py:114:80: E501 line too long (91 > 79 characters)
./audit/migrations/0001_initial.py:115:80: E501 line too long (113 > 79 characters)
./audit/migrations/0001_initial.py:116:80: E501 line too long (94 > 79 characters)
./audit/migrations/0001_initial.py:117:80: E501 line too long (119 > 79 characters)
./audit/migrations/0001_initial.py:120:80: E501 line too long (86 > 79 characters)
./audit/migrations/0001_initial.py:136:80: E501 line too long (109 > 79 characters)
./audit/migrations/0001_initial.py:137:80: E501 line too long (106 > 79 characters)
./audit/migrations/0001_initial.py:144:80: E501 line too long (112 > 79 characters)
./audit/migrations/0001_initial.py:153:80: E501 line too long (82 > 79 characters)
./audit/migrations/0001_initial.py:156:80: E501 line too long (85 > 79 characters)
./audit/migrations/0001_initial.py:168:80: E501 line too long (83 > 79 characters)
./audit/migrations/0001_initial.py:169:80: E501 line too long (106 > 79 characters)
./audit/migrations/0001_initial.py:170:80: E501 line too long (108 > 79 characters)
./audit/migrations/0001_initial.py:174:80: E501 line too long (117 > 79 characters)
./audit/migrations/0001_initial.py:194:80: E501 line too long (113 > 79 characters)
./audit/migrations/0001_initial.py:196:80: E501 line too long (86 > 79 characters)
./audit/migrations/0001_initial.py:225:80: E501 line too long (108 > 79 characters)
./audit/migrations/0001_initial.py:226:80: E501 line too long (103 > 79 characters)
./audit/migrations/0001_initial.py:227:80: E501 line too long (108 > 79 characters)
./audit/migrations/0001_initial.py:228:80: E501 line too long (105 > 79 characters)
./audit/models.py:15:1: W293 blank line contains whitespace
./audit/models.py:28:1: W293 blank line contains whitespace
./audit/models.py:34:1: W293 blank line contains whitespace
./audit/models.py:43:1: W293 blank line contains whitespace
./audit/models.py:53:1: W293 blank line contains whitespace
./audit/models.py:56:1: W293 blank line contains whitespace
./audit/models.py:68:1: W293 blank line contains whitespace
./audit/models.py:73:1: W293 blank line contains whitespace
./audit/models.py:81:1: W293 blank line contains whitespace
./audit/models.py:88:1: W293 blank line contains whitespace
./audit/models.py:91:1: W293 blank line contains whitespace
./audit/models.py:103:1: W293 blank line contains whitespace
./audit/models.py:113:1: W293 blank line contains whitespace
./audit/models.py:125:1: W293 blank line contains whitespace
./audit/models.py:131:1: W293 blank line contains whitespace
./audit/models.py:140:1: W293 blank line contains whitespace
./audit/models.py:143:1: W293 blank line contains whitespace
./audit/models.py:149:1: W293 blank line contains whitespace
./audit/models.py:155:1: W293 blank line contains whitespace
./audit/models.py:160:1: W293 blank line contains whitespace
./audit/models.py:168:1: W293 blank line contains whitespace
./audit/models.py:175:1: W293 blank line contains whitespace
./audit/models.py:182:1: W293 blank line contains whitespace
./audit/models.py:189:1: W293 blank line contains whitespace
./audit/models.py:195:1: W293 blank line contains whitespace
./audit/models.py:197:1: W293 blank line contains whitespace
./audit/models.py:208:1: W293 blank line contains whitespace
./audit/models.py:220:1: W293 blank line contains whitespace
./audit/models.py:222:80: E501 line too long (86 > 79 characters)
./audit/models.py:230:1: W293 blank line contains whitespace
./audit/models.py:236:1: W293 blank line contains whitespace
./audit/models.py:243:1: W293 blank line contains whitespace
./audit/models.py:249:1: W293 blank line contains whitespace
./audit/models.py:253:1: W293 blank line contains whitespace
./audit/models.py:259:1: W293 blank line contains whitespace
./audit/models.py:264:1: W293 blank line contains whitespace
./audit/models.py:271:1: W293 blank line contains whitespace
./audit/models.py:275:1: W293 blank line contains whitespace
./audit/models.py:277:1: W293 blank line contains whitespace
./audit/models.py:287:1: W293 blank line contains whitespace
./audit/models.py:289:80: W292 no newline at end of file
./audit/signals.py:6:80: E501 line too long (90 > 79 characters)
./audit/signals.py:7:1: F401 'sales_notes.models.Especie' imported but unused
./audit/signals.py:43:1: W293 blank line contains whitespace
./audit/signals.py:50:80: E501 line too long (86 > 79 characters)
./audit/signals.py:55:1: W293 blank line contains whitespace
./audit/signals.py:61:80: E501 line too long (83 > 79 characters)
./audit/signals.py:69:80: E501 line too long (82 > 79 characters)
./audit/signals.py:77:1: W293 blank line contains whitespace
./audit/signals.py:86:1: W293 blank line contains whitespace
./audit/signals.py:91:79: W291 trailing whitespace
./audit/signals.py:92:37: E128 continuation line under-indented for visual indent
./audit/signals.py:93:1: W293 blank line contains whitespace
./audit/signals.py:121:1: W293 blank line contains whitespace
./audit/signals.py:126:80: E501 line too long (82 > 79 characters)
./audit/signals.py:129:1: W293 blank line contains whitespace
./audit/signals.py:136:1: W293 blank line contains whitespace
./audit/signals.py:152:80: E501 line too long (90 > 79 characters)
./audit/signals.py:162:80: E501 line too long (91 > 79 characters)
./audit/signals.py:188:76: W292 no newline at end of file
./authentication/admin.py:21:1: W293 blank line contains whitespace
./authentication/admin.py:25:1: W293 blank line contains whitespace
./authentication/admin.py:35:1: W293 blank line contains whitespace
./authentication/admin.py:43:1: W293 blank line contains whitespace
./authentication/admin.py:50:1: W293 blank line contains whitespace
./authentication/admin.py:52:1: W293 blank line contains whitespace
./authentication/admin.py:61:1: W293 blank line contains whitespace
./authentication/admin.py:109:1: W293 blank line contains whitespace
./authentication/admin.py:130:1: W293 blank line contains whitespace
./authentication/admin.py:136:1: W293 blank line contains whitespace
./authentication/admin.py:140:1: W293 blank line contains whitespace
./authentication/admin.py:143:1: W293 blank line contains whitespace
./authentication/admin.py:165:1: W293 blank line contains whitespace
./authentication/admin.py:167:1: W293 blank line contains whitespace
./authentication/admin.py:171:1: W293 blank line contains whitespace
./authentication/admin.py:186:1: W293 blank line contains whitespace
./authentication/admin.py:190:1: W293 blank line contains whitespace
./authentication/admin.py:194:1: W293 blank line contains whitespace
./authentication/admin.py:208:1: W293 blank line contains whitespace
./authentication/admin.py:212:1: W293 blank line contains whitespace
./authentication/admin.py:216:1: W293 blank line contains whitespace
./authentication/admin.py:229:1: W293 blank line contains whitespace
./authentication/admin.py:239:1: W293 blank line contains whitespace
./authentication/admin.py:242:1: W293 blank line contains whitespace
./authentication/admin.py:252:1: W293 blank line contains whitespace
./authentication/admin.py:259:1: W293 blank line contains whitespace
./authentication/admin.py:266:1: W293 blank line contains whitespace
./authentication/admin.py:281:1: W293 blank line contains whitespace
./authentication/admin.py:283:1: W293 blank line contains whitespace
./authentication/admin.py:314:1: W293 blank line contains whitespace
./authentication/admin.py:316:1: W293 blank line contains whitespace
./authentication/admin.py:320:1: W293 blank line contains whitespace
./authentication/admin.py:323:1: W293 blank line contains whitespace
./authentication/admin.py:328:1: W293 blank line contains whitespace
./authentication/admin.py:330:1: W293 blank line contains whitespace
./authentication/admin.py:334:1: W293 blank line contains whitespace
./authentication/admin.py:337:1: W293 blank line contains whitespace
./authentication/admin.py:359:1: W293 blank line contains whitespace
./authentication/admin.py:361:1: W293 blank line contains whitespace
./authentication/admin.py:365:1: W293 blank line contains whitespace
./authentication/admin.py:379:1: W293 blank line contains whitespace
./authentication/admin.py:389:1: W293 blank line contains whitespace
./authentication/admin.py:392:1: W293 blank line contains whitespace
./authentication/admin.py:401:1: W293 blank line contains whitespace
./authentication/admin.py:407:1: W293 blank line contains whitespace
./authentication/admin.py:415:1: W293 blank line contains whitespace
./authentication/admin.py:427:1: W293 blank line contains whitespace
./authentication/admin.py:429:1: W293 blank line contains whitespace
./authentication/admin.py:457:1: W293 blank line contains whitespace
./authentication/admin.py:461:1: W293 blank line contains whitespace
./authentication/admin.py:464:1: W293 blank line contains whitespace
./authentication/admin.py:471:1: W293 blank line contains whitespace
./authentication/admin.py:473:1: W293 blank line contains whitespace
./authentication/admin.py:477:1: W293 blank line contains whitespace
./authentication/admin.py:480:1: W293 blank line contains whitespace
./authentication/admin.py:490:1: W293 blank line contains whitespace
./authentication/admin.py:492:1: W293 blank line contains whitespace
./authentication/admin.py:500:1: W293 blank line contains whitespace
./authentication/admin.py:502:1: W293 blank line contains whitespace
./authentication/admin.py:506:1: W293 blank line contains whitespace
./authentication/admin.py:511:1: W293 blank line contains whitespace
./authentication/admin.py:515:1: W293 blank line contains whitespace
./authentication/admin.py:519:21: W292 no newline at end of file
./authentication/apps.py:12:1: W293 blank line contains whitespace
./authentication/apps.py:17:62: W292 no newline at end of file
./authentication/management/commands/create_test_users.py:13:1: W293 blank line contains whitespace
./authentication/management/commands/create_test_users.py:30:80: E501 line too long (93 > 79 characters)
./authentication/management/commands/create_test_users.py:32:50: F541 f-string is missing placeholders
./authentication/management/commands/create_test_users.py:33:1: W293 blank line contains whitespace
./authentication/management/commands/create_test_users.py:49:80: E501 line too long (100 > 79 characters)
./authentication/management/commands/create_test_users.py:51:50: F541 f-string is missing placeholders
./authentication/management/commands/create_test_users.py:51:80: E501 line too long (85 > 79 characters)
./authentication/management/commands/create_test_users.py:51:86: W292 no newline at end of file
./authentication/management/commands/create_user_groups.py:12:1: W293 blank line contains whitespace
./authentication/management/commands/create_user_groups.py:16:1: W293 blank line contains whitespace
./authentication/management/commands/create_user_groups.py:18:80: E501 line too long (89 > 79 characters)
./authentication/management/commands/create_user_groups.py:19:80: E501 line too long (87 > 79 characters)
./authentication/management/commands/create_user_groups.py:20:1: W293 blank line contains whitespace
./authentication/management/commands/create_user_groups.py:24:80: E501 line too long (99 > 79 characters)
./authentication/management/commands/create_user_groups.py:25:1: W293 blank line contains whitespace
./authentication/management/commands/create_user_groups.py:29:80: E501 line too long (108 > 79 characters)
./authentication/management/commands/create_user_groups.py:30:1: W293 blank line contains whitespace
./authentication/management/commands/create_user_groups.py:31:76: W292 no newline at end of file
./authentication/migrations/0001_initial.py:25:80: E501 line too long (88 > 79 characters)
./authentication/migrations/0001_initial.py:26:80: E501 line too long (103 > 79 characters)
./authentication/migrations/0001_initial.py:31:80: E501 line too long (117 > 79 characters)
./authentication/migrations/0001_initial.py:38:80: E501 line too long (95 > 79 characters)
./authentication/migrations/0001_initial.py:39:80: E501 line too long (107 > 79 characters)
./authentication/migrations/0001_initial.py:42:80: E501 line too long (95 > 79 characters)
./authentication/migrations/0001_initial.py:46:80: E501 line too long (104 > 79 characters)
./authentication/migrations/0001_initial.py:47:80: E501 line too long (102 > 79 characters)
./authentication/migrations/0001_initial.py:48:80: E501 line too long (103 > 79 characters)
./authentication/migrations/0001_initial.py:53:80: E501 line too long (94 > 79 characters)
./authentication/migrations/0001_initial.py:61:80: E501 line too long (138 > 79 characters)
./authentication/migrations/0001_initial.py:65:80: E501 line too long (117 > 79 characters)
./authentication/migrations/0001_initial.py:66:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:70:80: E501 line too long (110 > 79 characters)
./authentication/migrations/0001_initial.py:73:80: E501 line too long (118 > 79 characters)
./authentication/migrations/0001_initial.py:81:80: E501 line too long (94 > 79 characters)
./authentication/migrations/0001_initial.py:88:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:94:80: E501 line too long (83 > 79 characters)
./authentication/migrations/0001_initial.py:100:80: E501 line too long (117 > 79 characters)
./authentication/migrations/0001_initial.py:101:80: E501 line too long (118 > 79 characters)
./authentication/migrations/0001_initial.py:104:80: E501 line too long (113 > 79 characters)
./authentication/migrations/0001_initial.py:108:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:112:80: E501 line too long (110 > 79 characters)
./authentication/migrations/0001_initial.py:116:80: E501 line too long (117 > 79 characters)
./authentication/migrations/0001_initial.py:124:80: E501 line too long (134 > 79 characters)
./authentication/migrations/0001_initial.py:155:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:162:80: E501 line too long (95 > 79 characters)
./authentication/migrations/0001_initial.py:165:80: E501 line too long (115 > 79 characters)
./authentication/migrations/0001_initial.py:168:80: E501 line too long (86 > 79 characters)
./authentication/migrations/0001_initial.py:189:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:196:80: E501 line too long (83 > 79 characters)
./authentication/migrations/0001_initial.py:211:80: E501 line too long (88 > 79 characters)
./authentication/migrations/0001_initial.py:212:80: E501 line too long (88 > 79 characters)
./authentication/migrations/0001_initial.py:213:80: E501 line too long (120 > 79 characters)
./authentication/migrations/0001_initial.py:214:80: E501 line too long (102 > 79 characters)
./authentication/migrations/0001_initial.py:230:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:253:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:258:80: E501 line too long (84 > 79 characters)
./authentication/migrations/0001_initial.py:267:80: E501 line too long (91 > 79 characters)
./authentication/migrations/0001_initial.py:273:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:274:80: E501 line too long (95 > 79 characters)
./authentication/migrations/0001_initial.py:275:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:276:80: E501 line too long (103 > 79 characters)
./authentication/migrations/0001_initial.py:277:80: E501 line too long (118 > 79 characters)
./authentication/migrations/0001_initial.py:278:80: E501 line too long (88 > 79 characters)
./authentication/migrations/0001_initial.py:279:80: E501 line too long (88 > 79 characters)
./authentication/migrations/0001_initial.py:310:80: E501 line too long (96 > 79 characters)
./authentication/migrations/0001_initial.py:314:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:318:80: E501 line too long (100 > 79 characters)
./authentication/migrations/0001_initial.py:322:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:326:80: E501 line too long (107 > 79 characters)
./authentication/migrations/0001_initial.py:330:80: E501 line too long (93 > 79 characters)
./authentication/migrations/0001_initial.py:334:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:338:80: E501 line too long (100 > 79 characters)
./authentication/migrations/0001_initial.py:342:80: E501 line too long (104 > 79 characters)
./authentication/migrations/0001_initial.py:346:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:350:80: E501 line too long (114 > 79 characters)
./authentication/migrations/0001_initial.py:354:80: E501 line too long (95 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:31:80: E501 line too long (115 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:36:80: E501 line too long (114 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:41:80: E501 line too long (104 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:46:80: E501 line too long (115 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:52:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:58:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0002_remove_apiuser_api_user_cif_org_f8feeb_idx_and_more.py:62:80: E501 line too long (96 > 79 characters)
./authentication/migrations/0003_alter_apiuser_cif_organization.py:9:80: E501 line too long (87 > 79 characters)
./authentication/migrations/0003_alter_apiuser_cif_organization.py:16:80: E501 line too long (85 > 79 characters)
./authentication/models.py:17:1: W293 blank line contains whitespace
./authentication/models.py:23:1: W293 blank line contains whitespace
./authentication/models.py:60:80: E501 line too long (83 > 79 characters)
./authentication/models.py:62:1: W293 blank line contains whitespace
./authentication/models.py:74:1: W293 blank line contains whitespace
./authentication/models.py:80:1: W293 blank line contains whitespace
./authentication/models.py:88:1: W293 blank line contains whitespace
./authentication/models.py:94:1: W293 blank line contains whitespace
./authentication/models.py:99:1: W293 blank line contains whitespace
./authentication/models.py:106:1: W293 blank line contains whitespace
./authentication/models.py:113:1: W293 blank line contains whitespace
./authentication/models.py:118:1: W293 blank line contains whitespace
./authentication/models.py:124:1: W293 blank line contains whitespace
./authentication/models.py:128:1: W293 blank line contains whitespace
./authentication/models.py:137:1: W293 blank line contains whitespace
./authentication/models.py:140:1: W293 blank line contains whitespace
./authentication/models.py:146:80: E501 line too long (84 > 79 characters)
./authentication/models.py:149:80: E501 line too long (86 > 79 characters)
./authentication/models.py:152:1: W293 blank line contains whitespace
./authentication/models.py:157:80: E501 line too long (87 > 79 characters)
./authentication/models.py:158:80: E501 line too long (82 > 79 characters)
./authentication/models.py:159:1: W293 blank line contains whitespace
./authentication/models.py:165:80: E501 line too long (99 > 79 characters)
./authentication/models.py:179:1: W293 blank line contains whitespace
./authentication/models.py:182:1: W293 blank line contains whitespace
./authentication/models.py:185:1: W293 blank line contains whitespace
./authentication/models.py:187:1: W293 blank line contains whitespace
./authentication/models.py:190:1: W293 blank line contains whitespace
./authentication/models.py:196:1: W293 blank line contains whitespace
./authentication/models.py:198:1: W293 blank line contains whitespace
./authentication/models.py:200:1: W293 blank line contains whitespace
./authentication/models.py:212:1: W293 blank line contains whitespace
./authentication/models.py:214:80: E501 line too long (87 > 79 characters)
./authentication/models.py:218:1: E303 too many blank lines (3)
./authentication/models.py:223:1: W293 blank line contains whitespace
./authentication/models.py:230:1: W293 blank line contains whitespace
./authentication/models.py:239:1: W293 blank line contains whitespace
./authentication/models.py:249:1: W293 blank line contains whitespace
./authentication/models.py:251:80: E501 line too long (86 > 79 characters)
./authentication/models.py:253:1: W293 blank line contains whitespace
./authentication/models.py:255:80: E501 line too long (80 > 79 characters)
./authentication/models.py:265:80: E501 line too long (92 > 79 characters)
./authentication/models.py:266:1: W293 blank line contains whitespace
./authentication/models.py:270:1: W293 blank line contains whitespace
./authentication/models.py:280:1: W293 blank line contains whitespace
./authentication/models.py:282:80: E501 line too long (89 > 79 characters)
./authentication/models.py:283:1: W293 blank line contains whitespace
./authentication/models.py:291:1: W293 blank line contains whitespace
./authentication/models.py:298:80: E501 line too long (96 > 79 characters)
./authentication/models.py:307:1: W293 blank line contains whitespace
./authentication/models.py:316:1: W293 blank line contains whitespace
./authentication/models.py:331:1: W293 blank line contains whitespace
./authentication/models.py:332:80: E501 line too long (101 > 79 characters)
./authentication/models.py:333:1: W293 blank line contains whitespace
./authentication/models.py:337:80: E501 line too long (94 > 79 characters)
./authentication/models.py:338:1: W293 blank line contains whitespace
./authentication/models.py:341:1: W293 blank line contains whitespace
./authentication/models.py:349:1: W293 blank line contains whitespace
./authentication/models.py:350:80: E501 line too long (117 > 79 characters)
./authentication/models.py:351:1: W293 blank line contains whitespace
./authentication/models.py:353:80: E501 line too long (86 > 79 characters)
./authentication/models.py:354:1: W293 blank line contains whitespace
./authentication/models.py:366:1: W293 blank line contains whitespace
./authentication/models.py:368:80: E501 line too long (92 > 79 characters)
./authentication/models.py:369:80: E501 line too long (81 > 79 characters)
./authentication/models.py:370:1: W293 blank line contains whitespace
./authentication/models.py:372:80: E501 line too long (80 > 79 characters)
./authentication/models.py:383:10: W292 no newline at end of file
./authentication/serializers.py:12:1: F401 'django.core.exceptions.ValidationError as DjangoValidationError' imported but unused
./authentication/serializers.py:21:1: W293 blank line contains whitespace
./authentication/serializers.py:25:1: W293 blank line contains whitespace
./authentication/serializers.py:33:1: W293 blank line contains whitespace
./authentication/serializers.py:40:1: W293 blank line contains whitespace
./authentication/serializers.py:57:1: W293 blank line contains whitespace
./authentication/serializers.py:61:1: W293 blank line contains whitespace
./authentication/serializers.py:64:1: W293 blank line contains whitespace
./authentication/serializers.py:67:1: W293 blank line contains whitespace
./authentication/serializers.py:76:1: W293 blank line contains whitespace
./authentication/serializers.py:80:1: W293 blank line contains whitespace
./authentication/serializers.py:83:1: W293 blank line contains whitespace
./authentication/serializers.py:88:16: F821 undefined name 'User'
./authentication/serializers.py:95:1: W293 blank line contains whitespace
./authentication/serializers.py:98:1: W293 blank line contains whitespace
./authentication/serializers.py:100:1: W293 blank line contains whitespace
./authentication/serializers.py:125:1: W293 blank line contains whitespace
./authentication/serializers.py:129:1: W293 blank line contains whitespace
./authentication/serializers.py:132:1: W293 blank line contains whitespace
./authentication/serializers.py:142:1: W293 blank line contains whitespace
./authentication/serializers.py:145:1: W293 blank line contains whitespace
./authentication/serializers.py:150:1: W293 blank line contains whitespace
./authentication/serializers.py:157:1: W293 blank line contains whitespace
./authentication/serializers.py:161:1: W293 blank line contains whitespace
./authentication/serializers.py:164:1: W293 blank line contains whitespace
./authentication/serializers.py:167:1: W293 blank line contains whitespace
./authentication/serializers.py:173:1: W293 blank line contains whitespace
./authentication/serializers.py:178:1: W293 blank line contains whitespace
./authentication/serializers.py:185:1: W293 blank line contains whitespace
./authentication/serializers.py:188:1: W293 blank line contains whitespace
./authentication/serializers.py:193:1: W293 blank line contains whitespace
./authentication/serializers.py:198:1: W293 blank line contains whitespace
./authentication/serializers.py:204:1: W293 blank line contains whitespace
./authentication/serializers.py:209:1: W293 blank line contains whitespace
./authentication/serializers.py:219:1: W293 blank line contains whitespace
./authentication/serializers.py:222:1: W293 blank line contains whitespace
./authentication/serializers.py:232:1: W293 blank line contains whitespace
./authentication/serializers.py:235:1: W293 blank line contains whitespace
./authentication/serializers.py:242:1: W293 blank line contains whitespace
./authentication/serializers.py:250:1: W293 blank line contains whitespace
./authentication/serializers.py:257:1: W293 blank line contains whitespace
./authentication/serializers.py:261:1: W293 blank line contains whitespace
./authentication/serializers.py:264:1: W293 blank line contains whitespace
./authentication/serializers.py:267:1: W293 blank line contains whitespace
./authentication/serializers.py:275:1: W293 blank line contains whitespace
./authentication/serializers.py:278:80: E501 line too long (89 > 79 characters)
./authentication/serializers.py:280:1: W293 blank line contains whitespace
./authentication/serializers.py:282:1: W293 blank line contains whitespace
./authentication/serializers.py:286:1: W293 blank line contains whitespace
./authentication/serializers.py:289:1: W293 blank line contains whitespace
./authentication/serializers.py:292:1: W293 blank line contains whitespace
./authentication/serializers.py:298:80: E501 line too long (81 > 79 characters)
./authentication/serializers.py:305:1: W293 blank line contains whitespace
./authentication/serializers.py:308:1: W293 blank line contains whitespace
./authentication/serializers.py:319:1: W293 blank line contains whitespace
./authentication/serializers.py:322:1: W293 blank line contains whitespace
./authentication/serializers.py:328:1: W293 blank line contains whitespace
./authentication/serializers.py:332:1: W293 blank line contains whitespace
./authentication/serializers.py:350:1: W293 blank line contains whitespace
./authentication/serializers.py:354:1: W293 blank line contains whitespace
./authentication/serializers.py:357:1: W293 blank line contains whitespace
./authentication/serializers.py:367:1: W293 blank line contains whitespace
./authentication/serializers.py:370:1: W293 blank line contains whitespace
./authentication/serializers.py:376:1: W293 blank line contains whitespace
./authentication/serializers.py:382:1: W293 blank line contains whitespace
./authentication/serializers.py:388:1: W293 blank line contains whitespace
./authentication/serializers.py:405:34: W292 no newline at end of file
./authentication/urls.py:30:1: W293 blank line contains whitespace
./authentication/urls.py:42:1: W293 blank line contains whitespace
./authentication/urls.py:54:1: W293 blank line contains whitespace
./authentication/urls.py:61:1: W293 blank line contains whitespace
./authentication/urls.py:68:2: W292 no newline at end of file
./authentication/views.py:9:1: F401 'rest_framework_simplejwt.views.TokenRefreshView' imported but unused
./authentication/views.py:10:1: F401 'django.contrib.auth.authenticate' imported but unused
./authentication/views.py:18:1: F401 '.serializers.TokenResponseSerializer' imported but unused
./authentication/views.py:18:1: F401 '.serializers.TokenRefreshSerializer' imported but unused
./authentication/views.py:35:1: W293 blank line contains whitespace
./authentication/views.py:38:1: W293 blank line contains whitespace
./authentication/views.py:53:1: W293 blank line contains whitespace
./authentication/views.py:56:1: W293 blank line contains whitespace
./authentication/views.py:66:1: W293 blank line contains whitespace
./authentication/views.py:69:1: W293 blank line contains whitespace
./authentication/views.py:72:1: W293 blank line contains whitespace
./authentication/views.py:76:1: W293 blank line contains whitespace
./authentication/views.py:80:1: W293 blank line contains whitespace
./authentication/views.py:85:1: W293 blank line contains whitespace
./authentication/views.py:99:1: W293 blank line contains whitespace
./authentication/views.py:106:1: W293 blank line contains whitespace
./authentication/views.py:109:1: W293 blank line contains whitespace
./authentication/views.py:111:1: W293 blank line contains whitespace
./authentication/views.py:117:1: W293 blank line contains whitespace
./authentication/views.py:127:1: W293 blank line contains whitespace
./authentication/views.py:130:1: W293 blank line contains whitespace
./authentication/views.py:134:1: W293 blank line contains whitespace
./authentication/views.py:137:1: W293 blank line contains whitespace
./authentication/views.py:144:1: W293 blank line contains whitespace
./authentication/views.py:147:1: W293 blank line contains whitespace
./authentication/views.py:150:1: W293 blank line contains whitespace
./authentication/views.py:153:1: W293 blank line contains whitespace
./authentication/views.py:165:80: E501 line too long (100 > 79 characters)
./authentication/views.py:168:1: W293 blank line contains whitespace
./authentication/views.py:169:80: E501 line too long (85 > 79 characters)
./authentication/views.py:170:1: W293 blank line contains whitespace
./authentication/views.py:176:1: W293 blank line contains whitespace
./authentication/views.py:188:1: W293 blank line contains whitespace
./authentication/views.py:189:80: E501 line too long (86 > 79 characters)
./authentication/views.py:190:1: W293 blank line contains whitespace
./authentication/views.py:193:80: E501 line too long (86 > 79 characters)
./authentication/views.py:195:1: W293 blank line contains whitespace
./authentication/views.py:199:1: W293 blank line contains whitespace
./authentication/views.py:212:1: W293 blank line contains whitespace
./authentication/views.py:217:1: W293 blank line contains whitespace
./authentication/views.py:222:1: W293 blank line contains whitespace
./authentication/views.py:227:1: W293 blank line contains whitespace
./authentication/views.py:234:1: W293 blank line contains whitespace
./authentication/views.py:236:1: W293 blank line contains whitespace
./authentication/views.py:246:1: W293 blank line contains whitespace
./authentication/views.py:252:1: W293 blank line contains whitespace
./authentication/views.py:261:1: W293 blank line contains whitespace
./authentication/views.py:264:1: W293 blank line contains whitespace
./authentication/views.py:273:1: W293 blank line contains whitespace
./authentication/views.py:282:1: W293 blank line contains whitespace
./authentication/views.py:284:1: W293 blank line contains whitespace
./authentication/views.py:293:1: W293 blank line contains whitespace
./authentication/views.py:295:1: W293 blank line contains whitespace
./authentication/views.py:306:1: W293 blank line contains whitespace
./authentication/views.py:308:1: W293 blank line contains whitespace
./authentication/views.py:318:1: W293 blank line contains whitespace
./authentication/views.py:320:1: W293 blank line contains whitespace
./authentication/views.py:322:1: W293 blank line contains whitespace
./authentication/views.py:328:1: W293 blank line contains whitespace
./authentication/views.py:330:1: W293 blank line contains whitespace
./authentication/views.py:334:1: W293 blank line contains whitespace
./authentication/views.py:337:1: W293 blank line contains whitespace
./authentication/views.py:343:1: W293 blank line contains whitespace
./authentication/views.py:347:1: W293 blank line contains whitespace
./authentication/views.py:349:1: W293 blank line contains whitespace
./authentication/views.py:355:1: W293 blank line contains whitespace
./authentication/views.py:365:1: W293 blank line contains whitespace
./authentication/views.py:371:1: W293 blank line contains whitespace
./authentication/views.py:374:1: W293 blank line contains whitespace
./authentication/views.py:377:1: W293 blank line contains whitespace
./authentication/views.py:386:1: W293 blank line contains whitespace
./authentication/views.py:388:1: W293 blank line contains whitespace
./authentication/views.py:398:1: W293 blank line contains whitespace
./authentication/views.py:400:1: W293 blank line contains whitespace
./authentication/views.py:402:1: W293 blank line contains whitespace
./authentication/views.py:410:1: W293 blank line contains whitespace
./authentication/views.py:412:1: W293 blank line contains whitespace
./authentication/views.py:416:1: W293 blank line contains whitespace
./authentication/views.py:419:1: W293 blank line contains whitespace
./authentication/views.py:428:1: W293 blank line contains whitespace
./authentication/views.py:431:1: W293 blank line contains whitespace
./authentication/views.py:441:1: W293 blank line contains whitespace
./authentication/views.py:450:1: W293 blank line contains whitespace
./authentication/views.py:452:1: W293 blank line contains whitespace
./authentication/views.py:462:1: W293 blank line contains whitespace
./authentication/views.py:465:1: W293 blank line contains whitespace
./authentication/views.py:468:1: W293 blank line contains whitespace
./authentication/views.py:472:1: W293 blank line contains whitespace
./authentication/views.py:482:1: W293 blank line contains whitespace
./authentication/views.py:484:1: W293 blank line contains whitespace
./authentication/views.py:487:1: W293 blank line contains whitespace
./authentication/views.py:490:1: W293 blank line contains whitespace
./authentication/views.py:494:1: W293 blank line contains whitespace
./authentication/views.py:501:39: W292 no newline at end of file
./manage.py:22:11: W292 no newline at end of file
./sales_notes/apps.py:12:1: W293 blank line contains whitespace
./sales_notes/apps.py:18:69: W292 no newline at end of file
./sales_notes/exception_handler.py:2:1: F401 'rest_framework.response.Response' imported but unused
./sales_notes/exception_handler.py:12:1: W293 blank line contains whitespace
./sales_notes/exception_handler.py:19:1: W293 blank line contains whitespace
./sales_notes/exception_handler.py:23:1: W293 blank line contains whitespace
./sales_notes/exception_handler.py:32:1: W293 blank line contains whitespace
./sales_notes/exception_handler.py:36:1: W293 blank line contains whitespace
./sales_notes/exception_handler.py:44:80: E501 line too long (103 > 79 characters)
./sales_notes/exception_handler.py:55:1: W293 blank line contains whitespace
./sales_notes/exception_handler.py:58:80: E501 line too long (89 > 79 characters)
./sales_notes/exception_handler.py:59:1: W293 blank line contains whitespace
./sales_notes/exception_handler.py:61:1: W293 blank line contains whitespace
./sales_notes/exception_handler.py:62:20: W292 no newline at end of file
./sales_notes/existing_models.py:7:1: F811 redefinition of unused 'models' from line 5
./sales_notes/existing_models.py:14:80: E501 line too long (87 > 79 characters)
./sales_notes/existing_models.py:15:80: E501 line too long (83 > 79 characters)
./sales_notes/existing_models.py:16:80: E501 line too long (112 > 79 characters)
./sales_notes/existing_models.py:17:80: E501 line too long (114 > 79 characters)
./sales_notes/existing_models.py:20:80: E501 line too long (114 > 79 characters)
./sales_notes/existing_models.py:21:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:23:1: W293 blank line contains whitespace
./sales_notes/existing_models.py:29:1: W293 blank line contains whitespace
./sales_notes/existing_models.py:37:80: E501 line too long (93 > 79 characters)
./sales_notes/existing_models.py:38:80: E501 line too long (81 > 79 characters)
./sales_notes/existing_models.py:39:80: E501 line too long (98 > 79 characters)
./sales_notes/existing_models.py:40:80: E501 line too long (98 > 79 characters)
./sales_notes/existing_models.py:41:80: E501 line too long (98 > 79 characters)
./sales_notes/existing_models.py:42:80: E501 line too long (85 > 79 characters)
./sales_notes/existing_models.py:43:80: E501 line too long (87 > 79 characters)
./sales_notes/existing_models.py:44:80: E501 line too long (96 > 79 characters)
./sales_notes/existing_models.py:45:80: E501 line too long (107 > 79 characters)
./sales_notes/existing_models.py:46:80: E501 line too long (93 > 79 characters)
./sales_notes/existing_models.py:47:80: E501 line too long (85 > 79 characters)
./sales_notes/existing_models.py:48:80: E501 line too long (87 > 79 characters)
./sales_notes/existing_models.py:49:80: E501 line too long (85 > 79 characters)
./sales_notes/existing_models.py:50:80: E501 line too long (110 > 79 characters)
./sales_notes/existing_models.py:51:80: E501 line too long (110 > 79 characters)
./sales_notes/existing_models.py:52:80: E501 line too long (105 > 79 characters)
./sales_notes/existing_models.py:53:80: E501 line too long (84 > 79 characters)
./sales_notes/existing_models.py:54:80: E501 line too long (119 > 79 characters)
./sales_notes/existing_models.py:55:80: E501 line too long (119 > 79 characters)
./sales_notes/existing_models.py:56:80: E501 line too long (91 > 79 characters)
./sales_notes/existing_models.py:58:80: E501 line too long (94 > 79 characters)
./sales_notes/existing_models.py:59:80: E501 line too long (87 > 79 characters)
./sales_notes/existing_models.py:60:80: E501 line too long (104 > 79 characters)
./sales_notes/existing_models.py:61:80: E501 line too long (104 > 79 characters)
./sales_notes/existing_models.py:63:1: W293 blank line contains whitespace
./sales_notes/existing_models.py:69:1: W293 blank line contains whitespace
./sales_notes/existing_models.py:77:80: E501 line too long (88 > 79 characters)
./sales_notes/existing_models.py:78:80: E501 line too long (93 > 79 characters)
./sales_notes/existing_models.py:79:80: E501 line too long (90 > 79 characters)
./sales_notes/existing_models.py:80:80: E501 line too long (86 > 79 characters)
./sales_notes/existing_models.py:81:80: E501 line too long (84 > 79 characters)
./sales_notes/existing_models.py:82:80: E501 line too long (106 > 79 characters)
./sales_notes/existing_models.py:83:80: E501 line too long (83 > 79 characters)
./sales_notes/existing_models.py:84:80: E501 line too long (89 > 79 characters)
./sales_notes/existing_models.py:85:80: E501 line too long (101 > 79 characters)
./sales_notes/existing_models.py:86:80: E501 line too long (83 > 79 characters)
./sales_notes/existing_models.py:88:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:89:80: E501 line too long (98 > 79 characters)
./sales_notes/existing_models.py:90:80: E501 line too long (106 > 79 characters)
./sales_notes/existing_models.py:91:80: E501 line too long (106 > 79 characters)
./sales_notes/existing_models.py:92:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:93:80: E501 line too long (102 > 79 characters)
./sales_notes/existing_models.py:94:80: E501 line too long (121 > 79 characters)
./sales_notes/existing_models.py:95:80: E501 line too long (119 > 79 characters)
./sales_notes/existing_models.py:96:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:97:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:98:80: E501 line too long (90 > 79 characters)
./sales_notes/existing_models.py:100:1: W293 blank line contains whitespace
./sales_notes/existing_models.py:106:1: W293 blank line contains whitespace
./sales_notes/existing_models.py:108:44: W292 no newline at end of file
./sales_notes/migrations/0001_initial.py:25:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:27:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:43:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:59:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:61:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:64:80: E501 line too long (120 > 79 characters)
./sales_notes/migrations/0001_initial.py:77:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:79:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:80:80: E501 line too long (99 > 79 characters)
./sales_notes/migrations/0001_initial.py:83:80: E501 line too long (118 > 79 characters)
./sales_notes/migrations/0001_initial.py:87:80: E501 line too long (119 > 79 characters)
./sales_notes/migrations/0001_initial.py:98:80: E501 line too long (108 > 79 characters)
./sales_notes/migrations/0001_initial.py:100:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:101:80: E501 line too long (93 > 79 characters)
./sales_notes/migrations/0001_initial.py:113:80: E501 line too long (95 > 79 characters)
./sales_notes/migrations/0001_initial.py:114:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:115:80: E501 line too long (97 > 79 characters)
./sales_notes/migrations/0001_initial.py:116:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:117:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:118:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:119:80: E501 line too long (101 > 79 characters)
./sales_notes/migrations/0001_initial.py:120:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:121:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:124:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:126:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:127:80: E501 line too long (101 > 79 characters)
./sales_notes/migrations/0001_initial.py:128:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:129:80: E501 line too long (101 > 79 characters)
./sales_notes/migrations/0001_initial.py:132:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:136:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:140:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:142:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:146:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:152:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:155:80: E501 line too long (107 > 79 characters)
./sales_notes/migrations/0001_initial.py:156:80: E501 line too long (94 > 79 characters)
./sales_notes/migrations/0001_initial.py:157:80: E501 line too long (110 > 79 characters)
./sales_notes/migrations/0001_initial.py:158:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:159:80: E501 line too long (120 > 79 characters)
./sales_notes/migrations/0001_initial.py:160:80: E501 line too long (120 > 79 characters)
./sales_notes/migrations/0001_initial.py:161:80: E501 line too long (94 > 79 characters)
./sales_notes/migrations/0001_initial.py:173:80: E501 line too long (95 > 79 characters)
./sales_notes/migrations/0001_initial.py:174:80: E501 line too long (104 > 79 characters)
./sales_notes/migrations/0001_initial.py:175:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:176:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:177:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:178:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:181:80: E501 line too long (104 > 79 characters)
./sales_notes/migrations/0001_initial.py:183:80: E501 line too long (99 > 79 characters)
./sales_notes/migrations/0001_initial.py:184:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:185:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:186:80: E501 line too long (99 > 79 characters)
./sales_notes/migrations/0001_initial.py:187:80: E501 line too long (85 > 79 characters)
./sales_notes/migrations/0001_initial.py:188:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:189:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:192:80: E501 line too long (115 > 79 characters)
./sales_notes/migrations/0001_initial.py:196:80: E501 line too long (115 > 79 characters)
./sales_notes/migrations/0001_initial.py:198:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:199:80: E501 line too long (118 > 79 characters)
./sales_notes/migrations/0001_initial.py:203:80: E501 line too long (104 > 79 characters)
./sales_notes/migrations/0001_initial.py:209:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:212:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:213:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:214:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:215:80: E501 line too long (85 > 79 characters)
./sales_notes/migrations/0001_initial.py:237:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:238:80: E501 line too long (113 > 79 characters)
./sales_notes/migrations/0001_initial.py:239:80: E501 line too long (90 > 79 characters)
./sales_notes/migrations/0001_initial.py:260:80: E501 line too long (119 > 79 characters)
./sales_notes/migrations/0001_initial.py:261:80: E501 line too long (113 > 79 characters)
./sales_notes/migrations/0001_initial.py:262:80: E501 line too long (89 > 79 characters)
./sales_notes/migrations/0001_initial.py:273:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:275:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:278:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:283:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:288:80: E501 line too long (108 > 79 characters)
./sales_notes/migrations/0001_initial.py:289:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:290:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:293:80: E501 line too long (83 > 79 characters)
./sales_notes/migrations/0001_initial.py:297:80: E501 line too long (119 > 79 characters)
./sales_notes/migrations/0001_initial.py:311:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:313:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:316:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:326:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:332:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:333:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:342:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:349:80: E501 line too long (110 > 79 characters)
./sales_notes/migrations/0001_initial.py:353:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:358:80: E501 line too long (107 > 79 characters)
./sales_notes/migrations/0001_initial.py:363:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:367:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:369:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:370:80: E501 line too long (84 > 79 characters)
./sales_notes/migrations/0001_initial.py:371:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:372:80: E501 line too long (111 > 79 characters)
./sales_notes/migrations/0001_initial.py:373:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:374:80: E501 line too long (97 > 79 characters)
./sales_notes/migrations/0001_initial.py:377:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:381:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:385:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:387:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:391:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:395:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:396:80: E501 line too long (99 > 79 characters)
./sales_notes/migrations/0001_initial.py:397:80: E501 line too long (119 > 79 characters)
./sales_notes/migrations/0001_initial.py:398:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:402:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:414:80: E501 line too long (101 > 79 characters)
./sales_notes/migrations/0001_initial.py:419:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:422:80: E501 line too long (101 > 79 characters)
./sales_notes/migrations/0001_initial.py:430:80: E501 line too long (95 > 79 characters)
./sales_notes/migrations/0001_initial.py:441:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:452:80: E501 line too long (96 > 79 characters)
./sales_notes/migrations/0001_initial.py:461:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:470:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:473:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:492:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:496:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:498:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:501:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:544:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:550:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:551:80: E501 line too long (99 > 79 characters)
./sales_notes/migrations/0001_initial.py:554:80: E501 line too long (111 > 79 characters)
./sales_notes/migrations/0001_initial.py:587:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:598:80: E501 line too long (107 > 79 characters)
./sales_notes/migrations/0001_initial.py:606:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:607:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:640:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:644:80: E501 line too long (98 > 79 characters)
./sales_notes/migrations/0001_initial.py:648:80: E501 line too long (115 > 79 characters)
./sales_notes/migrations/0001_initial.py:657:80: E501 line too long (104 > 79 characters)
./sales_notes/migrations/0001_initial.py:662:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:666:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:670:80: E501 line too long (95 > 79 characters)
./sales_notes/migrations/0001_initial.py:674:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:678:80: E501 line too long (107 > 79 characters)
./sales_notes/migrations/0001_initial.py:682:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:686:80: E501 line too long (85 > 79 characters)
./sales_notes/models.py:6:1: F401 'django.core.validators.MaxValueValidator' imported but unused
./sales_notes/models.py:6:80: E501 line too long (87 > 79 characters)
./sales_notes/models.py:8:1: F401 'django.db.models.Q' imported but unused
./sales_notes/models.py:8:1: F401 'django.db.models.CheckConstraint' imported but unused
./sales_notes/models.py:17:1: W293 blank line contains whitespace
./sales_notes/models.py:29:23: W291 trailing whitespace
./sales_notes/models.py:30:21: W291 trailing whitespace
./sales_notes/models.py:34:1: W293 blank line contains whitespace
./sales_notes/models.py:45:1: W293 blank line contains whitespace
./sales_notes/models.py:50:1: W293 blank line contains whitespace
./sales_notes/models.py:54:1: W293 blank line contains whitespace
./sales_notes/models.py:58:34: W291 trailing whitespace
./sales_notes/models.py:62:1: W293 blank line contains whitespace
./sales_notes/models.py:72:1: W293 blank line contains whitespace
./sales_notes/models.py:83:15: W291 trailing whitespace
./sales_notes/models.py:84:34: W291 trailing whitespace
./sales_notes/models.py:87:1: W293 blank line contains whitespace
./sales_notes/models.py:93:1: W293 blank line contains whitespace
./sales_notes/models.py:100:1: W293 blank line contains whitespace
./sales_notes/models.py:115:1: W293 blank line contains whitespace
./sales_notes/models.py:126:1: W293 blank line contains whitespace
./sales_notes/models.py:137:1: W293 blank line contains whitespace
./sales_notes/models.py:146:1: W293 blank line contains whitespace
./sales_notes/models.py:148:80: E501 line too long (84 > 79 characters)
./sales_notes/models.py:161:1: W293 blank line contains whitespace
./sales_notes/models.py:176:6: W291 trailing whitespace
./sales_notes/models.py:177:1: W293 blank line contains whitespace
./sales_notes/models.py:180:80: E501 line too long (82 > 79 characters)
./sales_notes/models.py:198:1: W293 blank line contains whitespace
./sales_notes/models.py:201:1: W293 blank line contains whitespace
./sales_notes/models.py:205:1: W293 blank line contains whitespace
./sales_notes/models.py:215:1: W293 blank line contains whitespace
./sales_notes/models.py:217:1: W293 blank line contains whitespace
./sales_notes/models.py:224:80: E501 line too long (94 > 79 characters)
./sales_notes/models.py:225:1: W293 blank line contains whitespace
./sales_notes/models.py:227:80: E501 line too long (87 > 79 characters)
./sales_notes/models.py:228:1: W293 blank line contains whitespace
./sales_notes/models.py:236:1: W293 blank line contains whitespace
./sales_notes/models.py:243:51: W291 trailing whitespace
./sales_notes/models.py:245:9: E265 block comment should start with '# '
./sales_notes/models.py:250:9: E265 block comment should start with '# '
./sales_notes/models.py:251:1: W293 blank line contains whitespace
./sales_notes/models.py:266:1: W293 blank line contains whitespace
./sales_notes/models.py:272:1: W293 blank line contains whitespace
./sales_notes/models.py:278:1: W293 blank line contains whitespace
./sales_notes/models.py:282:1: W293 blank line contains whitespace
./sales_notes/models.py:287:9: E265 block comment should start with '# '
./sales_notes/models.py:292:9: E265 block comment should start with '# '
./sales_notes/models.py:293:1: W293 blank line contains whitespace
./sales_notes/models.py:308:1: W293 blank line contains whitespace
./sales_notes/models.py:314:1: W293 blank line contains whitespace
./sales_notes/models.py:320:1: W293 blank line contains whitespace
./sales_notes/models.py:324:1: W293 blank line contains whitespace
./sales_notes/models.py:329:9: E265 block comment should start with '# '
./sales_notes/models.py:334:9: E265 block comment should start with '# '
./sales_notes/models.py:335:1: W293 blank line contains whitespace
./sales_notes/models.py:339:1: E305 expected 2 blank lines after class or function definition, found 1
./sales_notes/models.py:343:1: E402 module level import not at top of file
./sales_notes/models.py:344:1: F811 redefinition of unused 'MinValueValidator' from line 6
./sales_notes/models.py:344:1: E402 module level import not at top of file
./sales_notes/models.py:345:1: E402 module level import not at top of file
./sales_notes/models.py:346:1: E402 module level import not at top of file
./sales_notes/models.py:359:1: W293 blank line contains whitespace
./sales_notes/models.py:366:1: W293 blank line contains whitespace
./sales_notes/models.py:387:1: W293 blank line contains whitespace
./sales_notes/models.py:391:1: W293 blank line contains whitespace
./sales_notes/models.py:397:1: W293 blank line contains whitespace
./sales_notes/models.py:404:1: W293 blank line contains whitespace
./sales_notes/models.py:410:1: W293 blank line contains whitespace
./sales_notes/models.py:418:1: W293 blank line contains whitespace
./sales_notes/models.py:424:1: W293 blank line contains whitespace
./sales_notes/models.py:431:1: W293 blank line contains whitespace
./sales_notes/models.py:437:1: W293 blank line contains whitespace
./sales_notes/models.py:443:1: W293 blank line contains whitespace
./sales_notes/models.py:445:1: W293 blank line contains whitespace
./sales_notes/models.py:451:1: W293 blank line contains whitespace
./sales_notes/models.py:457:1: W293 blank line contains whitespace
./sales_notes/models.py:463:1: W293 blank line contains whitespace
./sales_notes/models.py:469:1: W293 blank line contains whitespace
./sales_notes/models.py:475:1: W293 blank line contains whitespace
./sales_notes/models.py:482:1: W293 blank line contains whitespace
./sales_notes/models.py:488:1: W293 blank line contains whitespace
./sales_notes/models.py:493:1: W293 blank line contains whitespace
./sales_notes/models.py:501:1: W293 blank line contains whitespace
./sales_notes/models.py:506:1: W293 blank line contains whitespace
./sales_notes/models.py:512:1: W293 blank line contains whitespace
./sales_notes/models.py:517:1: W293 blank line contains whitespace
./sales_notes/models.py:523:1: W293 blank line contains whitespace
./sales_notes/models.py:530:1: W293 blank line contains whitespace
./sales_notes/models.py:535:1: W293 blank line contains whitespace
./sales_notes/models.py:546:1: W293 blank line contains whitespace
./sales_notes/models.py:551:1: W293 blank line contains whitespace
./sales_notes/models.py:557:1: W293 blank line contains whitespace
./sales_notes/models.py:565:1: W293 blank line contains whitespace
./sales_notes/models.py:576:1: W293 blank line contains whitespace
./sales_notes/models.py:584:1: W293 blank line contains whitespace
./sales_notes/models.py:591:1: W293 blank line contains whitespace
./sales_notes/models.py:598:1: W293 blank line contains whitespace
./sales_notes/models.py:603:1: W293 blank line contains whitespace
./sales_notes/models.py:613:1: W293 blank line contains whitespace
./sales_notes/models.py:620:1: W293 blank line contains whitespace
./sales_notes/models.py:626:1: W293 blank line contains whitespace
./sales_notes/models.py:633:1: W293 blank line contains whitespace
./sales_notes/models.py:638:1: W293 blank line contains whitespace
./sales_notes/models.py:648:1: W293 blank line contains whitespace
./sales_notes/models.py:656:80: E501 line too long (88 > 79 characters)
./sales_notes/models.py:663:1: W293 blank line contains whitespace
./sales_notes/models.py:676:1: W293 blank line contains whitespace
./sales_notes/models.py:678:80: E501 line too long (80 > 79 characters)
./sales_notes/models.py:679:1: W293 blank line contains whitespace
./sales_notes/models.py:699:1: W293 blank line contains whitespace
./sales_notes/models.py:703:1: W293 blank line contains whitespace
./sales_notes/models.py:709:1: W293 blank line contains whitespace
./sales_notes/models.py:718:1: W293 blank line contains whitespace
./sales_notes/models.py:726:1: E402 module level import not at top of file
./sales_notes/models.py:726:37: W292 no newline at end of file
./sales_notes/permissions.py:10:1: W293 blank line contains whitespace
./sales_notes/permissions.py:15:1: W293 blank line contains whitespace
./sales_notes/permissions.py:20:1: W293 blank line contains whitespace
./sales_notes/permissions.py:24:16: E127 continuation line over-indented for visual indent
./sales_notes/permissions.py:30:1: W293 blank line contains whitespace
./sales_notes/permissions.py:35:1: W293 blank line contains whitespace
./sales_notes/permissions.py:40:1: W293 blank line contains whitespace
./sales_notes/permissions.py:53:1: W293 blank line contains whitespace
./sales_notes/permissions.py:58:1: W293 blank line contains whitespace
./sales_notes/permissions.py:62:1: W293 blank line contains whitespace
./sales_notes/permissions.py:65:80: E501 line too long (83 > 79 characters)
./sales_notes/permissions.py:66:1: W293 blank line contains whitespace
./sales_notes/permissions.py:68:80: E501 line too long (97 > 79 characters)
./sales_notes/permissions.py:70:1: W293 blank line contains whitespace
./sales_notes/permissions.py:73:1: W293 blank line contains whitespace
./sales_notes/permissions.py:79:1: W293 blank line contains whitespace
./sales_notes/permissions.py:83:1: W293 blank line contains whitespace
./sales_notes/permissions.py:85:80: E501 line too long (97 > 79 characters)
./sales_notes/permissions.py:88:1: W293 blank line contains whitespace
./sales_notes/permissions.py:89:21: W292 no newline at end of file
./sales_notes/serializers.py:14:1: F401 'jsonschema' imported but unused
./sales_notes/serializers.py:23:1: W293 blank line contains whitespace
./sales_notes/serializers.py:27:1: W293 blank line contains whitespace
./sales_notes/serializers.py:41:1: W293 blank line contains whitespace
./sales_notes/serializers.py:50:80: E501 line too long (83 > 79 characters)
./sales_notes/serializers.py:59:1: W293 blank line contains whitespace
./sales_notes/serializers.py:67:1: W293 blank line contains whitespace
./sales_notes/serializers.py:75:1: W293 blank line contains whitespace
./sales_notes/serializers.py:83:1: W293 blank line contains whitespace
./sales_notes/serializers.py:92:1: W293 blank line contains whitespace
./sales_notes/serializers.py:93:80: E501 line too long (81 > 79 characters)
./sales_notes/serializers.py:97:80: E501 line too long (102 > 79 characters)
./sales_notes/serializers.py:99:1: W293 blank line contains whitespace
./sales_notes/serializers.py:105:1: W293 blank line contains whitespace
./sales_notes/serializers.py:112:1: W293 blank line contains whitespace
./sales_notes/serializers.py:117:80: E501 line too long (86 > 79 characters)
./sales_notes/serializers.py:124:1: W293 blank line contains whitespace
./sales_notes/serializers.py:128:1: W293 blank line contains whitespace
./sales_notes/serializers.py:140:1: W293 blank line contains whitespace
./sales_notes/serializers.py:144:1: W293 blank line contains whitespace
./sales_notes/serializers.py:163:1: W293 blank line contains whitespace
./sales_notes/serializers.py:166:80: E501 line too long (95 > 79 characters)
./sales_notes/serializers.py:167:1: W293 blank line contains whitespace
./sales_notes/serializers.py:174:1: W293 blank line contains whitespace
./sales_notes/serializers.py:180:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:185:80: E501 line too long (80 > 79 characters)
./sales_notes/serializers.py:190:80: E501 line too long (81 > 79 characters)
./sales_notes/serializers.py:192:1: W293 blank line contains whitespace
./sales_notes/serializers.py:199:1: W293 blank line contains whitespace
./sales_notes/serializers.py:202:80: E501 line too long (99 > 79 characters)
./sales_notes/serializers.py:204:1: W293 blank line contains whitespace
./sales_notes/serializers.py:212:1: W293 blank line contains whitespace
./sales_notes/serializers.py:214:1: W293 blank line contains whitespace
./sales_notes/serializers.py:223:1: W293 blank line contains whitespace
./sales_notes/serializers.py:226:1: W293 blank line contains whitespace
./sales_notes/serializers.py:233:80: E501 line too long (90 > 79 characters)
./sales_notes/serializers.py:234:1: W293 blank line contains whitespace
./sales_notes/serializers.py:238:80: E501 line too long (86 > 79 characters)
./sales_notes/serializers.py:239:1: W293 blank line contains whitespace
./sales_notes/serializers.py:242:1: W293 blank line contains whitespace
./sales_notes/serializers.py:245:1: E305 expected 2 blank lines after class or function definition, found 1
./sales_notes/serializers.py:248:1: E402 module level import not at top of file
./sales_notes/serializers.py:249:1: F811 redefinition of unused 'Envio' from line 6
./sales_notes/serializers.py:249:1: F811 redefinition of unused 'EstablecimientoVenta' from line 6
./sales_notes/serializers.py:249:1: E402 module level import not at top of file
./sales_notes/serializers.py:250:1: F811 redefinition of unused 'UnidadProductivaSerializer' from line 154
./sales_notes/serializers.py:250:1: E402 module level import not at top of file
./sales_notes/serializers.py:251:1: E402 module level import not at top of file
./sales_notes/serializers.py:252:1: E402 module level import not at top of file
./sales_notes/serializers.py:264:1: W293 blank line contains whitespace
./sales_notes/serializers.py:268:1: W293 blank line contains whitespace
./sales_notes/serializers.py:288:1: W293 blank line contains whitespace
./sales_notes/serializers.py:295:80: E501 line too long (88 > 79 characters)
./sales_notes/serializers.py:296:1: W293 blank line contains whitespace
./sales_notes/serializers.py:304:1: W293 blank line contains whitespace
./sales_notes/serializers.py:309:80: E501 line too long (88 > 79 characters)
./sales_notes/serializers.py:312:1: W293 blank line contains whitespace
./sales_notes/serializers.py:316:1: W293 blank line contains whitespace
./sales_notes/serializers.py:319:80: E501 line too long (80 > 79 characters)
./sales_notes/serializers.py:321:1: W293 blank line contains whitespace
./sales_notes/serializers.py:329:1: W293 blank line contains whitespace
./sales_notes/serializers.py:334:1: W293 blank line contains whitespace
./sales_notes/serializers.py:336:1: W293 blank line contains whitespace
./sales_notes/serializers.py:344:1: W293 blank line contains whitespace
./sales_notes/serializers.py:348:1: W293 blank line contains whitespace
./sales_notes/serializers.py:355:1: W293 blank line contains whitespace
./sales_notes/serializers.py:359:1: W293 blank line contains whitespace
./sales_notes/serializers.py:363:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:364:1: W293 blank line contains whitespace
./sales_notes/serializers.py:369:1: W293 blank line contains whitespace
./sales_notes/serializers.py:370:80: E501 line too long (99 > 79 characters)
./sales_notes/serializers.py:375:1: W293 blank line contains whitespace
./sales_notes/serializers.py:379:1: W293 blank line contains whitespace
./sales_notes/serializers.py:384:1: W293 blank line contains whitespace
./sales_notes/serializers.py:398:1: W293 blank line contains whitespace
./sales_notes/serializers.py:400:1: W293 blank line contains whitespace
./sales_notes/serializers.py:407:1: W293 blank line contains whitespace
./sales_notes/serializers.py:409:1: W293 blank line contains whitespace
./sales_notes/serializers.py:425:1: W293 blank line contains whitespace
./sales_notes/serializers.py:429:1: E302 expected 2 blank lines, found 1
./sales_notes/serializers.py:442:1: W293 blank line contains whitespace
./sales_notes/serializers.py:451:80: E501 line too long (89 > 79 characters)
./sales_notes/serializers.py:454:1: W293 blank line contains whitespace
./sales_notes/serializers.py:459:80: E501 line too long (85 > 79 characters)
./sales_notes/serializers.py:461:1: W293 blank line contains whitespace
./sales_notes/serializers.py:463:1: W293 blank line contains whitespace
./sales_notes/serializers.py:469:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:477:1: W293 blank line contains whitespace
./sales_notes/serializers.py:484:1: W293 blank line contains whitespace
./sales_notes/serializers.py:488:1: W293 blank line contains whitespace
./sales_notes/serializers.py:496:80: E501 line too long (83 > 79 characters)
./sales_notes/serializers.py:511:1: W293 blank line contains whitespace
./sales_notes/serializers.py:514:80: E501 line too long (80 > 79 characters)
./sales_notes/serializers.py:515:1: W293 blank line contains whitespace
./sales_notes/serializers.py:518:1: W293 blank line contains whitespace
./sales_notes/serializers.py:537:1: W293 blank line contains whitespace
./sales_notes/serializers.py:539:80: E501 line too long (81 > 79 characters)
./sales_notes/serializers.py:548:1: W293 blank line contains whitespace
./sales_notes/serializers.py:551:1: W293 blank line contains whitespace
./sales_notes/serializers.py:552:1: E302 expected 2 blank lines, found 1
./sales_notes/serializers.py:555:1: W293 blank line contains whitespace
./sales_notes/serializers.py:561:1: W293 blank line contains whitespace
./sales_notes/serializers.py:576:1: W293 blank line contains whitespace
./sales_notes/serializers.py:580:1: W293 blank line contains whitespace
./sales_notes/serializers.py:605:1: W293 blank line contains whitespace
./sales_notes/serializers.py:606:5: F811 redefinition of unused 'Meta' from line 594
./sales_notes/serializers.py:614:1: E302 expected 2 blank lines, found 1
./sales_notes/serializers.py:620:1: E302 expected 2 blank lines, found 1
./sales_notes/serializers.py:626:1: E302 expected 2 blank lines, found 1
./sales_notes/serializers.py:633:1: F811 redefinition of unused 'datetime' from line 15
./sales_notes/serializers.py:633:1: E305 expected 2 blank lines after class or function definition, found 1
./sales_notes/serializers.py:633:1: E402 module level import not at top of file
./sales_notes/serializers.py:633:30: W292 no newline at end of file
./sales_notes/urls.py:23:2: W292 no newline at end of file
./sales_notes/views.py:10:80: E501 line too long (84 > 79 characters)
./sales_notes/views.py:23:1: W293 blank line contains whitespace
./sales_notes/views.py:28:1: W293 blank line contains whitespace
./sales_notes/views.py:35:1: W293 blank line contains whitespace
./sales_notes/views.py:36:80: E501 line too long (84 > 79 characters)
./sales_notes/views.py:43:1: W293 blank line contains whitespace
./sales_notes/views.py:50:1: W293 blank line contains whitespace
./sales_notes/views.py:53:1: W293 blank line contains whitespace
./sales_notes/views.py:57:1: W293 blank line contains whitespace
./sales_notes/views.py:63:1: W293 blank line contains whitespace
./sales_notes/views.py:67:1: W293 blank line contains whitespace
./sales_notes/views.py:71:1: W293 blank line contains whitespace
./sales_notes/views.py:73:80: E501 line too long (81 > 79 characters)
./sales_notes/views.py:75:1: W293 blank line contains whitespace
./sales_notes/views.py:78:1: W293 blank line contains whitespace
./sales_notes/views.py:86:1: W293 blank line contains whitespace
./sales_notes/views.py:87:1: E302 expected 2 blank lines, found 1
./sales_notes/views.py:93:80: E501 line too long (87 > 79 characters)
./sales_notes/views.py:95:1: W293 blank line contains whitespace
./sales_notes/views.py:98:80: E501 line too long (103 > 79 characters)
./sales_notes/views.py:103:1: W293 blank line contains whitespace
./sales_notes/views.py:105:24: F821 undefined name 'EnvioInputSerializer'
./sales_notes/views.py:108:1: W293 blank line contains whitespace
./sales_notes/views.py:110:80: E501 line too long (83 > 79 characters)
./sales_notes/views.py:112:1: W293 blank line contains whitespace
./sales_notes/views.py:115:1: W293 blank line contains whitespace
./sales_notes/views.py:116:80: E501 line too long (82 > 79 characters)
./sales_notes/views.py:117:1: W293 blank line contains whitespace
./sales_notes/views.py:124:1: W293 blank line contains whitespace
./sales_notes/views.py:128:1: W293 blank line contains whitespace
./sales_notes/views.py:132:1: W293 blank line contains whitespace
./sales_notes/views.py:140:1: W293 blank line contains whitespace
./sales_notes/views.py:142:1: W293 blank line contains whitespace
./sales_notes/views.py:147:1: W293 blank line contains whitespace
./sales_notes/views.py:150:1: W293 blank line contains whitespace
./sales_notes/views.py:154:1: W293 blank line contains whitespace
./sales_notes/views.py:160:1: W293 blank line contains whitespace
./sales_notes/views.py:164:1: W293 blank line contains whitespace
./sales_notes/views.py:167:1: W293 blank line contains whitespace
./sales_notes/views.py:172:1: W293 blank line contains whitespace
./sales_notes/views.py:174:1: W293 blank line contains whitespace
./sales_notes/views.py:181:1: W293 blank line contains whitespace
./sales_notes/views.py:185:1: W293 blank line contains whitespace
./sales_notes/views.py:187:41: W292 no newline at end of file
./tests/conftest.py:11:1: F401 'django.conf.settings' imported but unused
./tests/conftest.py:20:1: W293 blank line contains whitespace
./tests/conftest.py:33:1: W293 blank line contains whitespace
./tests/conftest.py:53:1: W293 blank line contains whitespace
./tests/conftest.py:66:1: W293 blank line contains whitespace
./tests/conftest.py:68:1: W293 blank line contains whitespace
./tests/conftest.py:83:1: W293 blank line contains whitespace
./tests/conftest.py:104:1: W293 blank line contains whitespace
./tests/conftest.py:119:1: W293 blank line contains whitespace
./tests/conftest.py:122:1: W293 blank line contains whitespace
./tests/conftest.py:145:1: W293 blank line contains whitespace
./tests/conftest.py:190:1: W293 blank line contains whitespace
./tests/conftest.py:205:1: W293 blank line contains whitespace
./tests/conftest.py:216:1: W293 blank line contains whitespace
./tests/conftest.py:223:1: W293 blank line contains whitespace
./tests/conftest.py:226:1: W293 blank line contains whitespace
./tests/conftest.py:231:27: F811 redefinition of unused 'settings' from line 11
./tests/conftest.py:234:1: W293 blank line contains whitespace
./tests/conftest.py:249:1: W293 blank line contains whitespace
./tests/conftest.py:254:1: W293 blank line contains whitespace
./tests/conftest.py:258:1: W293 blank line contains whitespace
./tests/conftest.py:281:1: W293 blank line contains whitespace
./tests/conftest.py:284:1: W293 blank line contains whitespace
./tests/conftest.py:292:1: W293 blank line contains whitespace
./tests/conftest.py:294:1: W293 blank line contains whitespace
./tests/conftest.py:297:1: W293 blank line contains whitespace
./tests/conftest.py:305:1: W293 blank line contains whitespace
./tests/conftest.py:313:1: W293 blank line contains whitespace
./tests/conftest.py:315:1: W293 blank line contains whitespace
./tests/conftest.py:318:1: W293 blank line contains whitespace
./tests/conftest.py:321:1: E302 expected 2 blank lines, found 1
./tests/conftest.py:330:5: F841 local variable 'api_user_profile' is assigned to but never used
./tests/conftest.py:339:1: E302 expected 2 blank lines, found 1
./tests/conftest.py:343:1: W293 blank line contains whitespace
./tests/conftest.py:349:1: W293 blank line contains whitespace
./tests/conftest.py:352:1: W293 blank line contains whitespace
./tests/conftest.py:376:1: W293 blank line contains whitespace
./tests/conftest.py:382:1: W293 blank line contains whitespace
./tests/conftest.py:385:1: W293 blank line contains whitespace
./tests/conftest.py:409:1: W293 blank line contains whitespace
./tests/conftest.py:417:1: W293 blank line contains whitespace
./tests/conftest.py:431:1: W293 blank line contains whitespace
./tests/conftest.py:439:1: W293 blank line contains whitespace
./tests/conftest.py:443:6: W292 no newline at end of file
./tests/integration/test_darp_batch.py:6:1: F401 'django.db.transaction' imported but unused
./tests/integration/test_darp_batch.py:12:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:13:80: E501 line too long (81 > 79 characters)
./tests/integration/test_darp_batch.py:17:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:23:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:25:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:28:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:31:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:36:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:38:80: E501 line too long (80 > 79 characters)
./tests/integration/test_darp_batch.py:41:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:44:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:49:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:53:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:56:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:57:80: E501 line too long (108 > 79 characters)
./tests/integration/test_darp_batch.py:59:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:60:80: E501 line too long (99 > 79 characters)
./tests/integration/test_darp_batch.py:63:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:68:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:70:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:72:77: W292 no newline at end of file
./tests/integration/test_sales_notes_flow.py:11:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:12:80: E501 line too long (91 > 79 characters)
./tests/integration/test_sales_notes_flow.py:14:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:17:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:18:80: E501 line too long (93 > 79 characters)
./tests/integration/test_sales_notes_flow.py:19:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:24:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:28:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:32:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:36:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:39:80: E501 line too long (95 > 79 characters)
./tests/integration/test_sales_notes_flow.py:40:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:44:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:48:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:53:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:54:80: E501 line too long (105 > 79 characters)
./tests/integration/test_sales_notes_flow.py:56:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:59:80: E501 line too long (101 > 79 characters)
./tests/integration/test_sales_notes_flow.py:60:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:62:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:64:80: E501 line too long (91 > 79 characters)
./tests/integration/test_sales_notes_flow.py:67:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:71:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:74:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:78:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:81:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:84:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:88:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:91:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:95:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:98:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:102:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:103:58: W292 no newline at end of file
./tests/security/test_owasp_api_security.py:13:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:15:80: E501 line too long (87 > 79 characters)
./tests/security/test_owasp_api_security.py:20:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:22:80: E501 line too long (93 > 79 characters)
./tests/security/test_owasp_api_security.py:23:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:28:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:35:13: F841 local variable 'response' is assigned to but never used
./tests/security/test_owasp_api_security.py:36:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:40:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:51:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:53:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:56:54: E712 comparison to False should be 'if cond is False:' or 'if not cond:'
./tests/security/test_owasp_api_security.py:57:50: E712 comparison to False should be 'if cond is False:' or 'if not cond:'
./tests/security/test_owasp_api_security.py:58:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:67:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:73:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:76:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:81:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:83:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:85:80: E501 line too long (89 > 79 characters)
./tests/security/test_owasp_api_security.py:86:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:91:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:102:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:105:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:110:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:113:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:120:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:125:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:129:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:134:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:140:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:142:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:144:67: W292 no newline at end of file
./tests/unit/test_authentication.py:12:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:20:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:22:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:26:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:34:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:36:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:38:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:49:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:54:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:57:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:68:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:73:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:75:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:80:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:82:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:84:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:85:80: E501 line too long (84 > 79 characters)
./tests/unit/test_authentication.py:88:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:90:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:92:80: E501 line too long (86 > 79 characters)
./tests/unit/test_authentication.py:92:87: W292 no newline at end of file
./tests/unit/test_models.py:3:1: F401 'django.core.exceptions.ValidationError' imported but unused
./tests/unit/test_models.py:4:1: F401 'sales_notes.models.Buque' imported but unused
./tests/unit/test_models.py:6:1: E302 expected 2 blank lines, found 1
./tests/unit/test_models.py:16:32: E712 comparison to False should be 'if cond is False:' or 'if not cond:'
./tests/unit/test_models.py:17:1: W293 blank line contains whitespace
./tests/unit/test_models.py:20:80: E501 line too long (91 > 79 characters)
./tests/unit/test_models.py:21:1: W293 blank line contains whitespace
./tests/unit/test_models.py:23:80: E501 line too long (95 > 79 characters)
./tests/unit/test_models.py:26:1: E305 expected 2 blank lines after class or function definition, found 1
./tests/unit/test_models.py:26:1: E402 module level import not at top of file
./tests/unit/test_models.py:27:1: F401 'rest_framework.test.APIClient' imported but unused
./tests/unit/test_models.py:27:1: E402 module level import not at top of file
./tests/unit/test_models.py:28:1: E402 module level import not at top of file
./tests/unit/test_models.py:30:1: E302 expected 2 blank lines, found 1
./tests/unit/test_models.py:32:80: E501 line too long (89 > 79 characters)
./tests/unit/test_models.py:35:80: E501 line too long (84 > 79 characters)
./tests/unit/test_models.py:36:1: W293 blank line contains whitespace
./tests/unit/test_models.py:39:1: W293 blank line contains whitespace
./tests/unit/test_models.py:42:80: E501 line too long (84 > 79 characters)
./tests/unit/test_models.py:44:1: W293 blank line contains whitespace
./tests/unit/test_models.py:48:1: W293 blank line contains whitespace
./tests/unit/test_models.py:51:80: E501 line too long (117 > 79 characters)
./tests/unit/test_models.py:52:1: W293 blank line contains whitespace
./tests/unit/test_models.py:57:1: E305 expected 2 blank lines after class or function definition, found 1
./tests/unit/test_models.py:57:1: E402 module level import not at top of file
./tests/unit/test_models.py:59:1: E302 expected 2 blank lines, found 1
./tests/unit/test_models.py:64:1: W293 blank line contains whitespace
./tests/unit/test_models.py:67:77: W292 no newline at end of file
./tests/unit/test_permissions.py:11:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:15:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:17:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:20:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:21:80: E501 line too long (97 > 79 characters)
./tests/unit/test_permissions.py:24:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:25:80: E501 line too long (87 > 79 characters)
./tests/unit/test_permissions.py:26:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:28:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:32:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:34:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:38:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:39:80: E501 line too long (90 > 79 characters)
./tests/unit/test_permissions.py:42:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:44:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:48:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:49:80: E501 line too long (90 > 79 characters)
./tests/unit/test_permissions.py:52:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:54:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:58:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:63:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:65:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:68:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:69:80: E501 line too long (82 > 79 characters)
./tests/unit/test_permissions.py:73:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:75:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:78:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:79:80: E501 line too long (93 > 79 characters)
./tests/unit/test_permissions.py:84:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:86:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:89:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:93:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:95:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:98:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:102:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:104:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:105:68: W292 no newline at end of file
./validate_vcpe_schema.py:8:1: F401 'jsonschema' imported but unused
./validate_vcpe_schema.py:9:1: F401 'jsonschema.validate' imported but unused
./validate_vcpe_schema.py:17:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:21:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:27:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:30:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:31:80: E501 line too long (82 > 79 characters)
./validate_vcpe_schema.py:34:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:37:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:42:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:46:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:52:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:58:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:60:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:68:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:72:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:75:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:80:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:83:80: E501 line too long (90 > 79 characters)
./validate_vcpe_schema.py:84:80: E501 line too long (87 > 79 characters)
./validate_vcpe_schema.py:85:80: E501 line too long (80 > 79 characters)
./validate_vcpe_schema.py:87:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:89:80: E501 line too long (97 > 79 characters)
./validate_vcpe_schema.py:93:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:97:80: E501 line too long (111 > 79 characters)
./validate_vcpe_schema.py:99:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:103:80: E501 line too long (111 > 79 characters)
./validate_vcpe_schema.py:105:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:109:80: E501 line too long (114 > 79 characters)
./validate_vcpe_schema.py:111:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:113:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:117:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:120:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:125:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:139:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:141:80: E501 line too long (80 > 79 characters)
./validate_vcpe_schema.py:152:80: E501 line too long (93 > 79 characters)
./validate_vcpe_schema.py:154:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:156:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:158:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:162:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:165:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:181:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:185:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:187:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:201:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:223:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:243:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:264:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:278:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:284:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:289:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:298:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:303:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:306:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:315:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:318:1: W293 blank line contains whitespace
./validate_vcpe_schema.py:324:11: F541 f-string is missing placeholders
./validate_vcpe_schema.py:325:11: F541 f-string is missing placeholders
./validate_vcpe_schema.py:330:11: W292 no newline at end of file
./vcpe_api/__init__.py:10:22: W292 no newline at end of file
./vcpe_api/_legacy_db_router.py:2:58: W291 trailing whitespace
./vcpe_api/_legacy_db_router.py:7:1: F401 'django.conf.settings' imported but unused
./vcpe_api/_legacy_db_router.py:16:1: W293 blank line contains whitespace
./vcpe_api/_legacy_db_router.py:24:1: W293 blank line contains whitespace
./vcpe_api/_legacy_db_router.py:31:1: W293 blank line contains whitespace
./vcpe_api/_legacy_db_router.py:35:1: W293 blank line contains whitespace
./vcpe_api/_legacy_db_router.py:39:1: W293 blank line contains whitespace
./vcpe_api/_legacy_db_router.py:46:1: W293 blank line contains whitespace
./vcpe_api/_legacy_db_router.py:50:1: W293 blank line contains whitespace
./vcpe_api/_legacy_db_router.py:56:1: W293 blank line contains whitespace
./vcpe_api/_legacy_db_router.py:60:1: W293 blank line contains whitespace
./vcpe_api/_legacy_db_router.py:64:1: W293 blank line contains whitespace
./vcpe_api/_legacy_db_router.py:66:20: W292 no newline at end of file
./vcpe_api/asgi.py:5:37: W292 no newline at end of file
./vcpe_api/celery.py:27:1: W293 blank line contains whitespace
./vcpe_api/celery.py:33:1: W293 blank line contains whitespace
./vcpe_api/celery.py:39:1: W293 blank line contains whitespace
./vcpe_api/celery.py:51:40: W292 no newline at end of file
./vcpe_api/settings.py:3:80: E501 line too long (84 > 79 characters)
./vcpe_api/settings.py:39:1: W293 blank line contains whitespace
./vcpe_api/settings.py:50:1: W293 blank line contains whitespace
./vcpe_api/settings.py:67:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:102:13: E265 block comment should start with '# '
./vcpe_api/settings.py:107:1: E265 block comment should start with '# '
./vcpe_api/settings.py:130:80: E501 line too long (91 > 79 characters)
./vcpe_api/settings.py:133:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:139:80: E501 line too long (82 > 79 characters)
./vcpe_api/settings.py:142:80: E501 line too long (83 > 79 characters)
./vcpe_api/settings.py:178:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:181:5: E265 block comment should start with '# '
./vcpe_api/settings.py:181:80: E501 line too long (80 > 79 characters)
./vcpe_api/settings.py:194:80: E501 line too long (97 > 79 characters)
./vcpe_api/settings.py:195:80: E501 line too long (92 > 79 characters)
./vcpe_api/settings.py:211:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:241:80: E501 line too long (88 > 79 characters)
./vcpe_api/settings.py:279:80: E501 line too long (93 > 79 characters)
./vcpe_api/settings.py:289:2: W292 no newline at end of file
./vcpe_api/urls.py:17:1: W293 blank line contains whitespace
./vcpe_api/urls.py:20:1: W293 blank line contains whitespace
./vcpe_api/urls.py:23:1: W293 blank line contains whitespace
./vcpe_api/urls.py:25:80: E501 line too long (82 > 79 characters)
./vcpe_api/urls.py:27:1: W293 blank line contains whitespace
./vcpe_api/urls.py:30:80: E501 line too long (92 > 79 characters)
./vcpe_api/urls.py:31:80: E501 line too long (86 > 79 characters)
./vcpe_api/urls.py:37:46: W292 no newline at end of file
./vcpe_api/views.py:30:7: W292 no newline at end of file
./vcpe_api/wsgi.py:5:37: W292 no newline at end of file
1     E127 continuation line over-indented for visual indent
2     E128 continuation line under-indented for visual indent
9     E265 block comment should start with '# '
11    E302 expected 2 blank lines, found 1
1     E303 too many blank lines (3)
5     E305 expected 2 blank lines after class or function definition, found 1
18    E402 module level import not at top of file
430   E501 line too long (80 > 79 characters)
3     E712 comparison to False should be 'if cond is False:' or 'if not cond:'
1     E722 do not use bare 'except'
20    F401 'audit.signals' imported but unused
4     F541 f-string is missing placeholders
8     F811 redefinition of unused 'models' from line 5
2     F821 undefined name 'User'
2     F841 local variable 'api_user_profile' is assigned to but never used
10    W291 trailing whitespace
38    W292 no newline at end of file
790   W293 blank line contains whitespace
1355


```


**Resultat:** ✅ Completat correctament


## 7. Resum Executiu


| Categoria | Estat |
|-----------|-------|
| **Connectivitat** | ✅ Operatiu |
| **Autenticació JWT** | ✅ Implementat |
| **Tests Automatitzats** | ⚠️ En desenvolupament |
| **Seguretat (SAST)** | ✅ Analitzat |
| **Cobertura Codi** | ⚠️ Per completar |
| **Documentació** | ✅ Accessible |

---

## 8. Conclusions i Recomanacions

### ✅ Punts Forts

1. **Infraestructura Docker**: Correctament configurada amb docker-compose
2. **Autenticació JWT**: Sistema implementat i funcional
3. **Health Checks**: Endpoints de monitoratge operatius
4. **Documentació API**: Swagger/ReDoc accessibles i actualitzats
5. **Seguretat**: Headers i configuracions bàsiques implementades

### ⚠️ Àrees de Millora

1. **Tests Automatitzats**: Completar suite de tests pytest (OE5-T5.1)
2. **Cobertura de Codi**: Incrementar fins >80% (objectiu TFM)
3. **Base de Dades**: Configurar PostgreSQL/PostGIS (OE3-T3.1)
4. **Endpoints**: Implementar CRUD de sales_notes (OE2-T2.2)
5. **Validacions**: Sistema de validació automàtica (OE2-T2.5)

### 📋 Següents Passos per al TFM

**Prioritat Alta (Aquesta setmana):**
1. Configurar PostgreSQL/PostGIS
2. Executar migracions
3. Implementar models de sales_notes
4. Crear tests unitaris per autenticació

**Prioritat Mitjana (Propera setmana):**
1. Desenvolupar endpoints CRUD
2. Implementar validacions
3. Tests d'integració
4. Tests de seguretat OWASP

**Prioritat Baixa (Abans de lliurament):**
1. Tests de performance (Locust)
2. OWASP ZAP penetration testing
3. Documentació completa
4. Anàlisi de riscos MAGERIT

---

## 📊 Mètriques del Projecte

| Mètrica | Valor Actual | Objectiu TFM |
|---------|--------------|--------------|
| Cobertura Tests | TBD | >80% |
| Tests Automatitzats | 0 | >50 |
| Vulnerabilitats High | 0 | 0 |
| Endpoints Implementats | 3 | >10 |
| Temps Resposta API | <100ms | <500ms |

---

## 📚 Referències per a la Memòria

- OWASP API Security Top 10 2023
- Django Security Checklist
- Microsoft Security Development Lifecycle (SDL)
- MAGERIT v3 - Metodologia de Análisis y Gestión de Riesgos

---

*Report generat automàticament per run_all_tests_with_report.sh*  
*Data: 18/11/2025 12:52:29*  
*TFM Ciberseguretat i Privadesa - ICATMAR*

