# 📋 Report Consolidat de Tests - VCPE API

**Data d'execució:** 19/11/2025 10:12:43  
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


NAME                 IMAGE                    COMMAND                  SERVICE         CREATED        STATUS                          PORTS
vcpe_api             api_dev-api              "python manage.py ru…"   api             22 hours ago   Up 49 minutes (healthy)         0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
vcpe_celery_beat     api_dev-celery_beat      "celery -A vcpe_api …"   celery_beat     22 hours ago   Restarting (1) 23 seconds ago   
vcpe_celery_worker   api_dev-celery_worker    "celery -A vcpe_api …"   celery_worker   22 hours ago   Restarting (1) 21 seconds ago   
vcpe_postgres        postgis/postgis:16-3.4   "docker-entrypoint.s…"   db              22 hours ago   Up 49 minutes (healthy)         0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp
vcpe_redis           redis:7.4-alpine         "docker-entrypoint.s…"   redis           22 hours ago   Up 49 minutes (healthy)         0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp


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
collecting ... collected 17 items

tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_success PASSED [  5%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_invalid_credentials PASSED [ 11%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_refresh_token_success PASSED [ 17%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_verify_token_success PASSED [ 23%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_access_protected_endpoint_without_token PASSED [ 29%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_access_protected_endpoint_with_valid_token PASSED [ 35%]
tests/unit/test_models.py::TestEnvioModel::test_create_envio_valid PASSED [ 41%]
tests/unit/test_models.py::TestEnvioModel::test_num_envio_unique PASSED  [ 47%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_create_envio PASSED [ 52%]
tests/unit/test_permissions.py::TestUserPermissions::test_investigador_cannot_create_envio PASSED [ 58%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_list_own_envios PASSED [ 64%]
tests/unit/test_permissions.py::TestUserPermissions::test_investigador_can_list_all_envios PASSED [ 70%]
tests/unit/test_permissions.py::TestUserPermissions::test_admin_can_list_all_envios PASSED [ 76%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_can_retrieve_own_envio PASSED [ 82%]
tests/unit/test_permissions.py::TestUserPermissions::test_darp_cannot_retrieve_other_envio PASSED [ 88%]
tests/unit/test_permissions.py::TestUserPermissions::test_investigador_can_retrieve_any_envio PASSED [ 94%]
tests/unit/test_permissions.py::TestUserPermissions::test_unauthenticated_cannot_access PASSED [100%]

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     26  70.45%   33, 74-75, 81-99, 105, 116-117, 137-138, 149, 163-182
audit/models.py                                               79      3  96.20%   105, 222, 289
audit/signals.py                                              77     30  61.04%   33-34, 46, 68-69, 75-96, 102-112, 135-137, 163-170, 176-188
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
sales_notes/models.py                                        206     18  91.26%   74, 102, 148, 224-225, 231, 254, 296, 338, 655-656, 679, 684-686, 721-723
sales_notes/permissions.py                                    30     10  66.67%   18-23, 38-43, 57, 72, 78, 89
sales_notes/serializers.py                                   275     60  78.18%   30-35, 63, 71, 79, 88-89, 95-96, 116, 131-135, 147-151, 179-189, 201, 208-211, 230-233, 241, 272, 300, 308, 318, 331, 385-397, 412, 420-424, 445, 491-498, 533, 577-578
sales_notes/tasks.py                                           0      0 100.00%
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                          72      9  87.50%   77, 84, 99, 144-145, 179-186
-----------------------------------------------------------------------------------------
TOTAL                                                       1340    354  73.58%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 73.58%

============================== 17 passed in 4.02s ==============================


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
collecting ... collected 6 items

tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_submission_success PASSED [ 16%]
tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_rate_limiting_batch PASSED [ 33%]
tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_darp_complete_lifecycle PASSED [ 50%]
tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_investigador_read_only_flow PASSED [ 66%]
tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_filtering_and_search PASSED [ 83%]
tests/integration/test_darp_batch.py::TestDARPBatchSubmission::test_batch_rollback_on_error PASSED [100%]

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     19  78.41%   33, 74-75, 81-99, 105, 116-117, 138, 149, 174, 180, 227-228
audit/models.py                                               79      3  96.20%   105, 222, 289
audit/signals.py                                              77     40  48.05%   33-34, 46, 68-69, 75-96, 102-112, 118-141, 163-170, 176-188
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
sales_notes/models.py                                        206     18  91.26%   74, 102, 148, 224-225, 231, 254, 296, 338, 655-656, 679, 684-686, 721-723
sales_notes/permissions.py                                    30     11  63.33%   18-23, 38-43, 57, 61, 72, 78, 89
sales_notes/serializers.py                                   275     58  78.91%   30-35, 63, 71, 79, 88-89, 95-96, 116, 131-135, 147-151, 179-189, 201, 208-211, 230-233, 241, 272, 300, 308, 318, 331, 385-397, 412, 420-424, 445, 491-498, 533
sales_notes/tasks.py                                           0      0 100.00%
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                          72      5  93.06%   66, 77, 99, 144-145
-----------------------------------------------------------------------------------------
TOTAL                                                       1340    352  73.73%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 73.73%

============================== 6 passed in 4.99s ===============================


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
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_brute_force_protection PASSED [ 22%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_mass_assignment_vulnerability PASSED [ 33%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_rate_limiting SKIPPED [ 44%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_admin_endpoint_access_control PASSED [ 55%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_prevent_automated_submission SKIPPED [ 66%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_security_headers_present PASSED [ 77%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_api_documentation_access_control SKIPPED [ 88%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_input_validation_sql_injection PASSED [100%]

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     23  73.86%   33, 74-75, 81-99, 105, 116-117, 126, 138, 149, 174, 180, 205-228
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
sales_notes/models.py                                        206     34  83.50%   74, 102, 148, 215-231, 235-236, 254, 296, 338, 648-656, 662-663, 679, 684-686, 721-723
sales_notes/permissions.py                                    30     17  43.33%   18-23, 38-43, 57, 61, 65, 72, 77-89
sales_notes/serializers.py                                   275    142  48.36%   30-35, 62-66, 70-74, 78-82, 87-100, 115-119, 131-135, 147-151, 173-213, 219-243, 271-275, 300, 308, 325-328, 335, 343-399, 406-427, 445, 460-467, 472-509, 513-542, 571, 575-579
sales_notes/tasks.py                                           0      0 100.00%
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                          72     34  52.78%   62-77, 81-85, 99, 113-118, 138-148, 158-165, 179-186
-----------------------------------------------------------------------------------------
TOTAL                                                       1340    503  62.46%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 62.46%

========================= 6 passed, 3 skipped in 2.92s =========================


```


**Resultat:** ✅ Completat correctament


## 4. Cobertura de Codi


### 4.1 Generar Informe de Cobertura


**Temps d'execució:** 9s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0
django: version: 5.1.2, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-38.0.0
collected 32 items

tests/integration/test_darp_batch.py ..                                  [  6%]
tests/integration/test_sales_notes_flow.py ...                           [ 15%]
tests/security/test_owasp_api_security.py ...s.s.s.                      [ 43%]
tests/unit/test_authentication.py ......                                 [ 62%]
tests/unit/test_models.py ..                                             [ 68%]
tests/unit/test_permissions.py .........                                 [ 96%]
tests/integration/test_darp_batch.py .                                   [100%]

---------- coverage: platform linux, python 3.12.12-final-0 ----------
Name                                                       Stmts   Miss   Cover   Missing
-----------------------------------------------------------------------------------------
audit/apps.py                                                  7      0 100.00%
audit/middleware.py                                           88     17  80.68%   33, 74-75, 81-99, 105, 116-117, 138, 149, 174, 180
audit/models.py                                               79      3  96.20%   105, 222, 289
audit/signals.py                                              77     30  61.04%   33-34, 46, 68-69, 75-96, 102-112, 135-137, 163-170, 176-188
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
sales_notes/models.py                                        206     18  91.26%   74, 102, 148, 224-225, 231, 254, 296, 338, 655-656, 679, 684-686, 721-723
sales_notes/permissions.py                                    30     10  66.67%   18-23, 38-43, 57, 72, 78, 89
sales_notes/serializers.py                                   275     56  79.64%   30-35, 63, 71, 79, 88-89, 95-96, 116, 131-135, 147-151, 179-189, 201, 208-211, 230-233, 241, 272, 300, 308, 385-397, 412, 420-424, 445, 491-498, 533
sales_notes/tasks.py                                           0      0 100.00%
sales_notes/urls.py                                            7      0 100.00%
sales_notes/views.py                                          72      4  94.44%   77, 99, 144-145
-----------------------------------------------------------------------------------------
TOTAL                                                       1340    336  74.93%
Coverage HTML written to dir htmlcov

FAIL Required test coverage of 80% not reached. Total coverage: 74.93%

======================== 29 passed, 3 skipped in 6.71s =========================


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
Run started:2025-11-19 09:13:16.268382

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
	Total lines of code: 6444
	Total lines skipped (#nosec): 0
	Total potential issues skipped due to specifically being disabled (e.g., #nosec BXXX): 0

Run metrics:
	Total issues (by severity):
		Undefined: 0
		Low: 78
		Medium: 1
		High: 0
	Total issues (by confidence):
		Undefined: 0
		Low: 0
		Medium: 8
		High: 71
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
./authentication/urls.py:5:80: E501 line too long (97 > 79 characters)
./authentication/urls.py:30:1: W293 blank line contains whitespace
./authentication/urls.py:42:1: W293 blank line contains whitespace
./authentication/urls.py:47:33: W291 trailing whitespace
./authentication/urls.py:59:1: W293 blank line contains whitespace
./authentication/urls.py:66:1: W293 blank line contains whitespace
./authentication/urls.py:73:2: W292 no newline at end of file
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
./sales_notes/migrations/0002_alter_buque_armador_alter_buque_capitan_and_more.py:26:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0002_alter_buque_armador_alter_buque_capitan_and_more.py:31:80: E501 line too long (107 > 79 characters)
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
./sales_notes/models.py:163:23: W291 trailing whitespace
./sales_notes/models.py:176:6: W291 trailing whitespace
./sales_notes/models.py:177:1: W293 blank line contains whitespace
./sales_notes/models.py:180:80: E501 line too long (82 > 79 characters)
./sales_notes/models.py:198:1: W293 blank line contains whitespace
./sales_notes/models.py:216:1: W293 blank line contains whitespace
./sales_notes/models.py:218:1: W293 blank line contains whitespace
./sales_notes/models.py:225:80: E501 line too long (94 > 79 characters)
./sales_notes/models.py:226:1: W293 blank line contains whitespace
./sales_notes/models.py:228:80: E501 line too long (87 > 79 characters)
./sales_notes/models.py:229:1: W293 blank line contains whitespace
./sales_notes/models.py:237:1: W293 blank line contains whitespace
./sales_notes/models.py:244:51: W291 trailing whitespace
./sales_notes/models.py:246:9: E265 block comment should start with '# '
./sales_notes/models.py:251:9: E265 block comment should start with '# '
./sales_notes/models.py:252:1: W293 blank line contains whitespace
./sales_notes/models.py:267:1: W293 blank line contains whitespace
./sales_notes/models.py:273:1: W293 blank line contains whitespace
./sales_notes/models.py:279:1: W293 blank line contains whitespace
./sales_notes/models.py:283:1: W293 blank line contains whitespace
./sales_notes/models.py:288:9: E265 block comment should start with '# '
./sales_notes/models.py:293:9: E265 block comment should start with '# '
./sales_notes/models.py:294:1: W293 blank line contains whitespace
./sales_notes/models.py:309:1: W293 blank line contains whitespace
./sales_notes/models.py:315:1: W293 blank line contains whitespace
./sales_notes/models.py:321:1: W293 blank line contains whitespace
./sales_notes/models.py:325:1: W293 blank line contains whitespace
./sales_notes/models.py:330:9: E265 block comment should start with '# '
./sales_notes/models.py:335:9: E265 block comment should start with '# '
./sales_notes/models.py:336:1: W293 blank line contains whitespace
./sales_notes/models.py:340:1: E305 expected 2 blank lines after class or function definition, found 1
./sales_notes/models.py:344:1: E402 module level import not at top of file
./sales_notes/models.py:345:1: F811 redefinition of unused 'MinValueValidator' from line 6
./sales_notes/models.py:345:1: E402 module level import not at top of file
./sales_notes/models.py:346:1: E402 module level import not at top of file
./sales_notes/models.py:347:1: E402 module level import not at top of file
./sales_notes/models.py:360:1: W293 blank line contains whitespace
./sales_notes/models.py:367:1: W293 blank line contains whitespace
./sales_notes/models.py:388:1: W293 blank line contains whitespace
./sales_notes/models.py:392:1: W293 blank line contains whitespace
./sales_notes/models.py:398:1: W293 blank line contains whitespace
./sales_notes/models.py:405:1: W293 blank line contains whitespace
./sales_notes/models.py:411:1: W293 blank line contains whitespace
./sales_notes/models.py:419:1: W293 blank line contains whitespace
./sales_notes/models.py:425:1: W293 blank line contains whitespace
./sales_notes/models.py:432:1: W293 blank line contains whitespace
./sales_notes/models.py:438:1: W293 blank line contains whitespace
./sales_notes/models.py:444:1: W293 blank line contains whitespace
./sales_notes/models.py:446:1: W293 blank line contains whitespace
./sales_notes/models.py:452:1: W293 blank line contains whitespace
./sales_notes/models.py:458:1: W293 blank line contains whitespace
./sales_notes/models.py:464:1: W293 blank line contains whitespace
./sales_notes/models.py:470:1: W293 blank line contains whitespace
./sales_notes/models.py:476:1: W293 blank line contains whitespace
./sales_notes/models.py:483:1: W293 blank line contains whitespace
./sales_notes/models.py:489:1: W293 blank line contains whitespace
./sales_notes/models.py:494:1: W293 blank line contains whitespace
./sales_notes/models.py:502:1: W293 blank line contains whitespace
./sales_notes/models.py:507:1: W293 blank line contains whitespace
./sales_notes/models.py:513:1: W293 blank line contains whitespace
./sales_notes/models.py:518:1: W293 blank line contains whitespace
./sales_notes/models.py:524:1: W293 blank line contains whitespace
./sales_notes/models.py:531:1: W293 blank line contains whitespace
./sales_notes/models.py:536:1: W293 blank line contains whitespace
./sales_notes/models.py:547:1: W293 blank line contains whitespace
./sales_notes/models.py:552:1: W293 blank line contains whitespace
./sales_notes/models.py:558:1: W293 blank line contains whitespace
./sales_notes/models.py:566:1: W293 blank line contains whitespace
./sales_notes/models.py:577:1: W293 blank line contains whitespace
./sales_notes/models.py:585:1: W293 blank line contains whitespace
./sales_notes/models.py:592:1: W293 blank line contains whitespace
./sales_notes/models.py:599:1: W293 blank line contains whitespace
./sales_notes/models.py:604:1: W293 blank line contains whitespace
./sales_notes/models.py:614:1: W293 blank line contains whitespace
./sales_notes/models.py:621:1: W293 blank line contains whitespace
./sales_notes/models.py:627:1: W293 blank line contains whitespace
./sales_notes/models.py:634:1: W293 blank line contains whitespace
./sales_notes/models.py:639:1: W293 blank line contains whitespace
./sales_notes/models.py:649:1: W293 blank line contains whitespace
./sales_notes/models.py:657:80: E501 line too long (88 > 79 characters)
./sales_notes/models.py:664:1: W293 blank line contains whitespace
./sales_notes/models.py:677:1: W293 blank line contains whitespace
./sales_notes/models.py:679:80: E501 line too long (80 > 79 characters)
./sales_notes/models.py:680:1: W293 blank line contains whitespace
./sales_notes/models.py:700:1: W293 blank line contains whitespace
./sales_notes/models.py:704:1: W293 blank line contains whitespace
./sales_notes/models.py:710:1: W293 blank line contains whitespace
./sales_notes/models.py:719:1: W293 blank line contains whitespace
./sales_notes/models.py:727:1: E402 module level import not at top of file
./sales_notes/models.py:727:37: W292 no newline at end of file
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
./sales_notes/serializers.py:166:80: E501 line too long (80 > 79 characters)
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
./sales_notes/serializers.py:434:1: W293 blank line contains whitespace
./sales_notes/serializers.py:443:80: E501 line too long (89 > 79 characters)
./sales_notes/serializers.py:446:1: W293 blank line contains whitespace
./sales_notes/serializers.py:451:80: E501 line too long (91 > 79 characters)
./sales_notes/serializers.py:451:92: W291 trailing whitespace
./sales_notes/serializers.py:453:1: W293 blank line contains whitespace
./sales_notes/serializers.py:455:1: W293 blank line contains whitespace
./sales_notes/serializers.py:461:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:469:1: W293 blank line contains whitespace
./sales_notes/serializers.py:476:1: W293 blank line contains whitespace
./sales_notes/serializers.py:480:1: W293 blank line contains whitespace
./sales_notes/serializers.py:488:80: E501 line too long (83 > 79 characters)
./sales_notes/serializers.py:503:1: W293 blank line contains whitespace
./sales_notes/serializers.py:506:80: E501 line too long (80 > 79 characters)
./sales_notes/serializers.py:507:1: W293 blank line contains whitespace
./sales_notes/serializers.py:510:1: W293 blank line contains whitespace
./sales_notes/serializers.py:529:1: W293 blank line contains whitespace
./sales_notes/serializers.py:531:80: E501 line too long (81 > 79 characters)
./sales_notes/serializers.py:540:1: W293 blank line contains whitespace
./sales_notes/serializers.py:543:1: W293 blank line contains whitespace
./sales_notes/serializers.py:544:1: E302 expected 2 blank lines, found 1
./sales_notes/serializers.py:547:1: W293 blank line contains whitespace
./sales_notes/serializers.py:553:1: W293 blank line contains whitespace
./sales_notes/serializers.py:568:1: W293 blank line contains whitespace
./sales_notes/serializers.py:572:1: W293 blank line contains whitespace
./sales_notes/serializers.py:597:1: W293 blank line contains whitespace
./sales_notes/serializers.py:598:5: F811 redefinition of unused 'Meta' from line 586
./sales_notes/serializers.py:606:1: E302 expected 2 blank lines, found 1
./sales_notes/serializers.py:612:1: E302 expected 2 blank lines, found 1
./sales_notes/serializers.py:618:1: E302 expected 2 blank lines, found 1
./sales_notes/serializers.py:625:1: F811 redefinition of unused 'datetime' from line 15
./sales_notes/serializers.py:625:1: E305 expected 2 blank lines after class or function definition, found 1
./sales_notes/serializers.py:625:1: E402 module level import not at top of file
./sales_notes/serializers.py:625:30: W292 no newline at end of file
./sales_notes/urls.py:23:2: W292 no newline at end of file
./sales_notes/views.py:10:80: E501 line too long (106 > 79 characters)
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
./sales_notes/views.py:87:80: E501 line too long (90 > 79 characters)
./sales_notes/views.py:93:80: E501 line too long (91 > 79 characters)
./sales_notes/views.py:95:1: W293 blank line contains whitespace
./sales_notes/views.py:98:80: E501 line too long (107 > 79 characters)
./sales_notes/views.py:100:80: E501 line too long (81 > 79 characters)
./sales_notes/views.py:103:1: W293 blank line contains whitespace
./sales_notes/views.py:107:1: W293 blank line contains whitespace
./sales_notes/views.py:109:80: E501 line too long (87 > 79 characters)
./sales_notes/views.py:111:1: W293 blank line contains whitespace
./sales_notes/views.py:114:1: W293 blank line contains whitespace
./sales_notes/views.py:115:80: E501 line too long (86 > 79 characters)
./sales_notes/views.py:116:1: W293 blank line contains whitespace
./sales_notes/views.py:123:1: W293 blank line contains whitespace
./sales_notes/views.py:127:1: W293 blank line contains whitespace
./sales_notes/views.py:131:1: W293 blank line contains whitespace
./sales_notes/views.py:139:1: W293 blank line contains whitespace
./sales_notes/views.py:141:1: W293 blank line contains whitespace
./sales_notes/views.py:146:1: W293 blank line contains whitespace
./sales_notes/views.py:149:1: W293 blank line contains whitespace
./sales_notes/views.py:153:1: W293 blank line contains whitespace
./sales_notes/views.py:159:1: W293 blank line contains whitespace
./sales_notes/views.py:163:1: W293 blank line contains whitespace
./sales_notes/views.py:166:1: W293 blank line contains whitespace
./sales_notes/views.py:171:1: W293 blank line contains whitespace
./sales_notes/views.py:173:1: W293 blank line contains whitespace
./sales_notes/views.py:180:1: W293 blank line contains whitespace
./sales_notes/views.py:184:1: W293 blank line contains whitespace
./sales_notes/views.py:186:41: W292 no newline at end of file
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
./tests/conftest.py:140:1: E302 expected 2 blank lines, found 1
./tests/conftest.py:144:1: W293 blank line contains whitespace
./tests/conftest.py:159:1: W293 blank line contains whitespace
./tests/conftest.py:170:1: W293 blank line contains whitespace
./tests/conftest.py:177:1: W293 blank line contains whitespace
./tests/conftest.py:180:1: W293 blank line contains whitespace
./tests/conftest.py:185:27: F811 redefinition of unused 'settings' from line 11
./tests/conftest.py:188:1: W293 blank line contains whitespace
./tests/conftest.py:203:1: W293 blank line contains whitespace
./tests/conftest.py:208:1: W293 blank line contains whitespace
./tests/conftest.py:212:1: W293 blank line contains whitespace
./tests/conftest.py:235:1: W293 blank line contains whitespace
./tests/conftest.py:238:1: W293 blank line contains whitespace
./tests/conftest.py:246:1: W293 blank line contains whitespace
./tests/conftest.py:248:1: W293 blank line contains whitespace
./tests/conftest.py:251:1: W293 blank line contains whitespace
./tests/conftest.py:259:1: W293 blank line contains whitespace
./tests/conftest.py:267:1: W293 blank line contains whitespace
./tests/conftest.py:269:1: W293 blank line contains whitespace
./tests/conftest.py:272:1: W293 blank line contains whitespace
./tests/conftest.py:275:1: E302 expected 2 blank lines, found 1
./tests/conftest.py:279:1: W293 blank line contains whitespace
./tests/conftest.py:290:1: E302 expected 2 blank lines, found 1
./tests/conftest.py:294:1: W293 blank line contains whitespace
./tests/conftest.py:300:1: W293 blank line contains whitespace
./tests/conftest.py:303:1: W293 blank line contains whitespace
./tests/conftest.py:320:25: W291 trailing whitespace
./tests/conftest.py:330:1: W293 blank line contains whitespace
./tests/conftest.py:336:1: W293 blank line contains whitespace
./tests/conftest.py:339:1: W293 blank line contains whitespace
./tests/conftest.py:366:1: W293 blank line contains whitespace
./tests/conftest.py:374:1: W293 blank line contains whitespace
./tests/conftest.py:388:1: W293 blank line contains whitespace
./tests/conftest.py:396:1: W293 blank line contains whitespace
./tests/conftest.py:401:1: W293 blank line contains whitespace
./tests/conftest.py:402:1: E302 expected 2 blank lines, found 1
./tests/conftest.py:407:1: W293 blank line contains whitespace
./tests/conftest.py:409:80: E501 line too long (82 > 79 characters)
./tests/conftest.py:412:1: W293 blank line contains whitespace
./tests/conftest.py:419:1: W293 blank line contains whitespace
./tests/conftest.py:425:44: W291 trailing whitespace
./tests/conftest.py:429:1: W293 blank line contains whitespace
./tests/conftest.py:437:1: W293 blank line contains whitespace
./tests/conftest.py:446:1: W293 blank line contains whitespace
./tests/conftest.py:449:1: E302 expected 2 blank lines, found 1
./tests/conftest.py:454:1: W293 blank line contains whitespace
./tests/conftest.py:494:1: E302 expected 2 blank lines, found 1
./tests/conftest.py:495:36: F811 redefinition of unused 'settings' from line 11
./tests/conftest.py:503:1: W293 blank line contains whitespace
./tests/conftest.py:506:26: F811 redefinition of unused 'settings' from line 11
./tests/conftest.py:511:1: W293 blank line contains whitespace
./tests/conftest.py:514:1: W293 blank line contains whitespace
./tests/conftest.py:525:1: W293 blank line contains whitespace
./tests/conftest.py:529:1: W293 blank line contains whitespace
./tests/conftest.py:534:35: W291 trailing whitespace
./tests/conftest.py:536:1: W293 blank line contains whitespace
./tests/conftest.py:538:1: W293 blank line contains whitespace
./tests/conftest.py:540:18: W292 no newline at end of file
./tests/integration/test_darp_batch.py:6:1: F401 'django.db.transaction' imported but unused
./tests/integration/test_darp_batch.py:12:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:13:80: E501 line too long (100 > 79 characters)
./tests/integration/test_darp_batch.py:17:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:23:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:24:80: E501 line too long (170 > 79 characters)
./tests/integration/test_darp_batch.py:26:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:29:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:32:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:37:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:39:80: E501 line too long (80 > 79 characters)
./tests/integration/test_darp_batch.py:42:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:45:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:50:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:54:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:57:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:58:80: E501 line too long (108 > 79 characters)
./tests/integration/test_darp_batch.py:60:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:61:80: E501 line too long (99 > 79 characters)
./tests/integration/test_darp_batch.py:64:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:69:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:71:1: W293 blank line contains whitespace
./tests/integration/test_darp_batch.py:73:77: W292 no newline at end of file
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
./tests/integration/test_sales_notes_flow.py:39:80: E501 line too long (96 > 79 characters)
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
./tests/security/test_owasp_api_security.py:68:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:74:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:78:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:83:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:85:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:87:80: E501 line too long (89 > 79 characters)
./tests/security/test_owasp_api_security.py:88:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:91:80: E501 line too long (107 > 79 characters)
./tests/security/test_owasp_api_security.py:93:20: W291 trailing whitespace
./tests/security/test_owasp_api_security.py:95:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:102:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:104:80: E501 line too long (164 > 79 characters)
./tests/security/test_owasp_api_security.py:105:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:108:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:112:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:117:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:120:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:127:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:133:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:134:80: E501 line too long (82 > 79 characters)
./tests/security/test_owasp_api_security.py:150:5: E301 expected 1 blank line, found 0
./tests/security/test_owasp_api_security.py:153:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:159:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:161:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:163:67: W292 no newline at end of file
./tests/unit/test_authentication.py:13:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:21:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:22:45: E231 missing whitespace after ','
./tests/unit/test_authentication.py:23:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:27:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:35:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:36:45: E231 missing whitespace after ','
./tests/unit/test_authentication.py:37:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:39:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:48:66: E231 missing whitespace after ','
./tests/unit/test_authentication.py:48:80: E501 line too long (80 > 79 characters)
./tests/unit/test_authentication.py:50:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:55:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:58:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:67:66: E231 missing whitespace after ','
./tests/unit/test_authentication.py:67:80: E501 line too long (80 > 79 characters)
./tests/unit/test_authentication.py:69:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:74:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:76:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:81:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:83:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:85:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:86:80: E501 line too long (84 > 79 characters)
./tests/unit/test_authentication.py:89:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:91:1: W293 blank line contains whitespace
./tests/unit/test_authentication.py:93:80: E501 line too long (86 > 79 characters)
./tests/unit/test_authentication.py:93:87: W292 no newline at end of file
./tests/unit/test_models.py:3:1: F401 'django.core.exceptions.ValidationError' imported but unused
./tests/unit/test_models.py:4:1: F401 'sales_notes.models.Buque' imported but unused
./tests/unit/test_models.py:6:1: E302 expected 2 blank lines, found 1
./tests/unit/test_models.py:16:32: E712 comparison to False should be 'if cond is False:' or 'if not cond:'
./tests/unit/test_models.py:17:1: W293 blank line contains whitespace
./tests/unit/test_models.py:20:80: E501 line too long (91 > 79 characters)
./tests/unit/test_models.py:21:1: W293 blank line contains whitespace
./tests/unit/test_models.py:23:80: E501 line too long (95 > 79 characters)
./tests/unit/test_models.py:24:1: W391 blank line at end of file
./tests/unit/test_permissions.py:11:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:15:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:28:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:29:80: E501 line too long (97 > 79 characters)
./tests/unit/test_permissions.py:32:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:33:80: E501 line too long (87 > 79 characters)
./tests/unit/test_permissions.py:34:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:36:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:40:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:42:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:46:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:47:80: E501 line too long (90 > 79 characters)
./tests/unit/test_permissions.py:50:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:52:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:56:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:57:80: E501 line too long (90 > 79 characters)
./tests/unit/test_permissions.py:60:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:62:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:66:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:71:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:73:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:76:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:77:80: E501 line too long (82 > 79 characters)
./tests/unit/test_permissions.py:81:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:83:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:86:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:87:80: E501 line too long (93 > 79 characters)
./tests/unit/test_permissions.py:92:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:94:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:97:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:101:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:103:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:106:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:110:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:112:1: W293 blank line contains whitespace
./tests/unit/test_permissions.py:113:68: W292 no newline at end of file
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
4     E231 missing whitespace after ','
9     E265 block comment should start with '# '
1     E301 expected 1 blank line, found 0
12    E302 expected 2 blank lines, found 1
1     E303 too many blank lines (3)
3     E305 expected 2 blank lines after class or function definition, found 1
14    E402 module level import not at top of file
438   E501 line too long (80 > 79 characters)
3     E712 comparison to False should be 'if cond is False:' or 'if not cond:'
1     E722 do not use bare 'except'
19    F401 'audit.signals' imported but unused
4     F541 f-string is missing placeholders
10    F811 redefinition of unused 'models' from line 5
1     F821 undefined name 'User'
1     F841 local variable 'response' is assigned to but never used
17    W291 trailing whitespace
37    W292 no newline at end of file
797   W293 blank line contains whitespace
1     W391 blank line at end of file
1376


```


**Resultat:** ✅ Completat correctament


## 7. Resum Executiu


## 📚 Referències per a la Memòria

- OWASP API Security Top 10 2023
- Django Security Checklist
- Microsoft Security Development Lifecycle (SDL)
- MAGERIT v3 - Metodologia de Análisis y Gestión de Riesgos

---

*Report generat automàticament per run_all_tests_with_report.sh*  
*Data: 19/11/2025 10:13:19*  
*TFM Ciberseguretat i Privadesa - ICATMAR*

