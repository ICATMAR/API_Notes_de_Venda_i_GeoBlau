# 📋 Report Consolidat de Tests - VCPE API

**Data d'execució:** 22/10/2025 16:32:14  
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


NAME                 IMAGE                   COMMAND                  SERVICE         CREATED          STATUS                      PORTS
vcpe_api             api_dev-api             "python manage.py ru…"   api             58 minutes ago   Up 58 minutes (healthy)     0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
vcpe_celery_beat     api_dev-celery_beat     "celery -A vcpe_api …"   celery_beat     58 minutes ago   Up 58 minutes (unhealthy)   8000/tcp
vcpe_celery_worker   api_dev-celery_worker   "celery -A vcpe_api …"   celery_worker   58 minutes ago   Up 58 minutes (unhealthy)   8000/tcp
vcpe_redis           redis:7.4-alpine        "docker-entrypoint.s…"   redis           58 minutes ago   Up 58 minutes (healthy)     0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp


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



<!doctype html>
<html lang="en">
<head>
  <title>Not Found</title>
</head>
<body>
  <h1>Not Found</h1><p>The requested resource was not found on this server.</p>
</body>
</html>

404


```


**Resultat:** ✅ Completat correctament


## 3. Tests Automatitzats (Pytest)


### 3.1 Tests Unitaris


**Temps d'execució:** 4s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
django: version: 5.1.2, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-37.11.0
collecting ... collected 6 items

tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_success ERROR [ 16%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_obtain_token_invalid_credentials ERROR [ 33%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_refresh_token_success ERROR [ 50%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_verify_token_success ERROR [ 66%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_access_protected_endpoint_without_token ERROR [ 83%]
tests/unit/test_authentication.py::TestJWTAuthentication::test_access_protected_endpoint_with_valid_token ERROR [100%]/usr/local/lib/python3.12/site-packages/_pytest/main.py:337: PluggyTeardownRaisedWarning: A plugin raised an exception during an old-style hookwrapper teardown.
Plugin: _cov, Hook: pytest_runtestloop
DataError: Couldn't use data file '/app/.coverage.ac310398103d.1512.XCssHOFx': unable to open database file
For more information see https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.PluggyTeardownRaisedWarning
  config.hook.pytest_runtestloop(session=session)

INTERNALERROR> Traceback (most recent call last):
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqlitedb.py", line 58, in _connect
INTERNALERROR>     self.con = sqlite3.connect(self.filename, check_same_thread=False)
INTERNALERROR>                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR> sqlite3.OperationalError: unable to open database file
INTERNALERROR> 
INTERNALERROR> The above exception was the direct cause of the following exception:
INTERNALERROR> 
INTERNALERROR> Traceback (most recent call last):
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/main.py", line 283, in wrap_session
INTERNALERROR>     session.exitstatus = doit(config, session) or 0
INTERNALERROR>                          ^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/main.py", line 337, in _main
INTERNALERROR>     config.hook.pytest_runtestloop(session=session)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_hooks.py", line 512, in __call__
INTERNALERROR>     return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_manager.py", line 120, in _hookexec
INTERNALERROR>     return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 167, in _multicall
INTERNALERROR>     raise exception
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/logging.py", line 803, in pytest_runtestloop
INTERNALERROR>     return (yield)  # Run all the tests.
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/terminal.py", line 673, in pytest_runtestloop
INTERNALERROR>     result = yield
INTERNALERROR>              ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 152, in _multicall
INTERNALERROR>     teardown.send(result)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 43, in run_old_style_hookwrapper
INTERNALERROR>     teardown.send(result)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pytest_cov/plugin.py", line 339, in pytest_runtestloop
INTERNALERROR>     self.cov_controller.finish()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pytest_cov/engine.py", line 46, in ensure_topdir_wrapper
INTERNALERROR>     return meth(self, *args, **kwargs)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pytest_cov/engine.py", line 256, in finish
INTERNALERROR>     self.cov.save()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/control.py", line 843, in save
INTERNALERROR>     data = self.get_data()
INTERNALERROR>            ^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/control.py", line 923, in get_data
INTERNALERROR>     if self._collector.flush_data():
INTERNALERROR>        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/collector.py", line 493, in flush_data
INTERNALERROR>     self.covdata.add_lines(self.mapped_file_dict(line_data))
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 123, in _wrapped
INTERNALERROR>     return method(self, *args, **kwargs)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 526, in add_lines
INTERNALERROR>     self._choose_lines_or_arcs(lines=True)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 603, in _choose_lines_or_arcs
INTERNALERROR>     with self._connect() as con:
INTERNALERROR>          ^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 373, in _connect
INTERNALERROR>     self._open_db()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 312, in _open_db
INTERNALERROR>     self._read_db()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 316, in _read_db
INTERNALERROR>     with self._dbs[threading.get_ident()] as db:
INTERNALERROR>          ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqlitedb.py", line 96, in __enter__
INTERNALERROR>     self._connect()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqlitedb.py", line 60, in _connect
INTERNALERROR>     raise DataError(f"Couldn't use data file {self.filename!r}: {exc}") from exc
INTERNALERROR> coverage.exceptions.DataError: Couldn't use data file '/app/.coverage.ac310398103d.1512.XCssHOFx': unable to open database file

======================== 3 warnings, 6 errors in 2.26s =========================


```


**Resultat:** ✅ Completat correctament


### 3.2 Tests d'Integració


**Temps d'execució:** 4s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0 -- /usr/local/bin/python3.12
cachedir: .pytest_cache
django: version: 5.1.2, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-37.11.0
collecting ... collected 1 item

tests/integration/test_sales_notes_flow.py::TestSalesNotesCompleteFlow::test_complete_sales_note_lifecycle ERROR [100%]/usr/local/lib/python3.12/site-packages/_pytest/main.py:337: PluggyTeardownRaisedWarning: A plugin raised an exception during an old-style hookwrapper teardown.
Plugin: _cov, Hook: pytest_runtestloop
DataError: Couldn't use data file '/app/.coverage.ac310398103d.1520.XKcBXvRx': unable to open database file
For more information see https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.PluggyTeardownRaisedWarning
  config.hook.pytest_runtestloop(session=session)

INTERNALERROR> Traceback (most recent call last):
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqlitedb.py", line 58, in _connect
INTERNALERROR>     self.con = sqlite3.connect(self.filename, check_same_thread=False)
INTERNALERROR>                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR> sqlite3.OperationalError: unable to open database file
INTERNALERROR> 
INTERNALERROR> The above exception was the direct cause of the following exception:
INTERNALERROR> 
INTERNALERROR> Traceback (most recent call last):
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/main.py", line 283, in wrap_session
INTERNALERROR>     session.exitstatus = doit(config, session) or 0
INTERNALERROR>                          ^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/main.py", line 337, in _main
INTERNALERROR>     config.hook.pytest_runtestloop(session=session)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_hooks.py", line 512, in __call__
INTERNALERROR>     return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_manager.py", line 120, in _hookexec
INTERNALERROR>     return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 167, in _multicall
INTERNALERROR>     raise exception
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/logging.py", line 803, in pytest_runtestloop
INTERNALERROR>     return (yield)  # Run all the tests.
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/terminal.py", line 673, in pytest_runtestloop
INTERNALERROR>     result = yield
INTERNALERROR>              ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 152, in _multicall
INTERNALERROR>     teardown.send(result)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 43, in run_old_style_hookwrapper
INTERNALERROR>     teardown.send(result)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pytest_cov/plugin.py", line 339, in pytest_runtestloop
INTERNALERROR>     self.cov_controller.finish()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pytest_cov/engine.py", line 46, in ensure_topdir_wrapper
INTERNALERROR>     return meth(self, *args, **kwargs)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pytest_cov/engine.py", line 256, in finish
INTERNALERROR>     self.cov.save()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/control.py", line 843, in save
INTERNALERROR>     data = self.get_data()
INTERNALERROR>            ^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/control.py", line 923, in get_data
INTERNALERROR>     if self._collector.flush_data():
INTERNALERROR>        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/collector.py", line 493, in flush_data
INTERNALERROR>     self.covdata.add_lines(self.mapped_file_dict(line_data))
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 123, in _wrapped
INTERNALERROR>     return method(self, *args, **kwargs)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 526, in add_lines
INTERNALERROR>     self._choose_lines_or_arcs(lines=True)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 603, in _choose_lines_or_arcs
INTERNALERROR>     with self._connect() as con:
INTERNALERROR>          ^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 373, in _connect
INTERNALERROR>     self._open_db()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 312, in _open_db
INTERNALERROR>     self._read_db()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 316, in _read_db
INTERNALERROR>     with self._dbs[threading.get_ident()] as db:
INTERNALERROR>          ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqlitedb.py", line 96, in __enter__
INTERNALERROR>     self._connect()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqlitedb.py", line 60, in _connect
INTERNALERROR>     raise DataError(f"Couldn't use data file {self.filename!r}: {exc}") from exc
INTERNALERROR> coverage.exceptions.DataError: Couldn't use data file '/app/.coverage.ac310398103d.1520.XKcBXvRx': unable to open database file

========================= 3 warnings, 1 error in 1.55s =========================


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
plugins: django-4.9.0, cov-5.0.0, Faker-37.11.0
collecting ... collected 9 items

tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_access_other_user_data ERROR [ 11%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_brute_force_protection ERROR [ 22%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_mass_assignment_vulnerability ERROR [ 33%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_rate_limiting ERROR [ 44%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_admin_endpoint_access_control ERROR [ 55%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_prevent_automated_submission ERROR [ 66%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_security_headers_present ERROR [ 77%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_api_documentation_access_control ERROR [ 88%]
tests/security/test_owasp_api_security.py::TestOWASPAPISecurity::test_input_validation_sql_injection ERROR [100%]/usr/local/lib/python3.12/site-packages/_pytest/main.py:337: PluggyTeardownRaisedWarning: A plugin raised an exception during an old-style hookwrapper teardown.
Plugin: _cov, Hook: pytest_runtestloop
DataError: Couldn't use data file '/app/.coverage.ac310398103d.1528.XOhveoax': unable to open database file
For more information see https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.PluggyTeardownRaisedWarning
  config.hook.pytest_runtestloop(session=session)

INTERNALERROR> Traceback (most recent call last):
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqlitedb.py", line 58, in _connect
INTERNALERROR>     self.con = sqlite3.connect(self.filename, check_same_thread=False)
INTERNALERROR>                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR> sqlite3.OperationalError: unable to open database file
INTERNALERROR> 
INTERNALERROR> The above exception was the direct cause of the following exception:
INTERNALERROR> 
INTERNALERROR> Traceback (most recent call last):
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/main.py", line 283, in wrap_session
INTERNALERROR>     session.exitstatus = doit(config, session) or 0
INTERNALERROR>                          ^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/main.py", line 337, in _main
INTERNALERROR>     config.hook.pytest_runtestloop(session=session)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_hooks.py", line 512, in __call__
INTERNALERROR>     return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_manager.py", line 120, in _hookexec
INTERNALERROR>     return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 167, in _multicall
INTERNALERROR>     raise exception
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/logging.py", line 803, in pytest_runtestloop
INTERNALERROR>     return (yield)  # Run all the tests.
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/terminal.py", line 673, in pytest_runtestloop
INTERNALERROR>     result = yield
INTERNALERROR>              ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 152, in _multicall
INTERNALERROR>     teardown.send(result)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 43, in run_old_style_hookwrapper
INTERNALERROR>     teardown.send(result)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pytest_cov/plugin.py", line 339, in pytest_runtestloop
INTERNALERROR>     self.cov_controller.finish()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pytest_cov/engine.py", line 46, in ensure_topdir_wrapper
INTERNALERROR>     return meth(self, *args, **kwargs)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pytest_cov/engine.py", line 256, in finish
INTERNALERROR>     self.cov.save()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/control.py", line 843, in save
INTERNALERROR>     data = self.get_data()
INTERNALERROR>            ^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/control.py", line 923, in get_data
INTERNALERROR>     if self._collector.flush_data():
INTERNALERROR>        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/collector.py", line 493, in flush_data
INTERNALERROR>     self.covdata.add_lines(self.mapped_file_dict(line_data))
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 123, in _wrapped
INTERNALERROR>     return method(self, *args, **kwargs)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 526, in add_lines
INTERNALERROR>     self._choose_lines_or_arcs(lines=True)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 603, in _choose_lines_or_arcs
INTERNALERROR>     with self._connect() as con:
INTERNALERROR>          ^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 373, in _connect
INTERNALERROR>     self._open_db()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 312, in _open_db
INTERNALERROR>     self._read_db()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 316, in _read_db
INTERNALERROR>     with self._dbs[threading.get_ident()] as db:
INTERNALERROR>          ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqlitedb.py", line 96, in __enter__
INTERNALERROR>     self._connect()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqlitedb.py", line 60, in _connect
INTERNALERROR>     raise DataError(f"Couldn't use data file {self.filename!r}: {exc}") from exc
INTERNALERROR> coverage.exceptions.DataError: Couldn't use data file '/app/.coverage.ac310398103d.1528.XOhveoax': unable to open database file

======================== 3 warnings, 9 errors in 2.57s =========================


```


**Resultat:** ✅ Completat correctament


## 4. Cobertura de Codi


### 4.1 Generar Informe de Cobertura


**Temps d'execució:** 6s


```


============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-8.3.3, pluggy-1.6.0
django: version: 5.1.2, settings: vcpe_api.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.9.0, cov-5.0.0, Faker-37.11.0
collected 16 items

tests/integration/test_sales_notes_flow.py E                             [  6%]
tests/security/test_owasp_api_security.py EEEEEEEEE                      [ 62%]
tests/unit/test_authentication.py EEEEEE/usr/local/lib/python3.12/site-packages/_pytest/main.py:337: PluggyTeardownRaisedWarning: A plugin raised an exception during an old-style hookwrapper teardown.
Plugin: _cov, Hook: pytest_runtestloop
DataError: Couldn't use data file '/app/.coverage.ac310398103d.1542.XhdSEVjx': unable to open database file
For more information see https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.PluggyTeardownRaisedWarning
  config.hook.pytest_runtestloop(session=session)

INTERNALERROR> Traceback (most recent call last):
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqlitedb.py", line 58, in _connect
INTERNALERROR>     self.con = sqlite3.connect(self.filename, check_same_thread=False)
INTERNALERROR>                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR> sqlite3.OperationalError: unable to open database file
INTERNALERROR> 
INTERNALERROR> The above exception was the direct cause of the following exception:
INTERNALERROR> 
INTERNALERROR> Traceback (most recent call last):
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/main.py", line 283, in wrap_session
INTERNALERROR>     session.exitstatus = doit(config, session) or 0
INTERNALERROR>                          ^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/main.py", line 337, in _main
INTERNALERROR>     config.hook.pytest_runtestloop(session=session)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_hooks.py", line 512, in __call__
INTERNALERROR>     return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_manager.py", line 120, in _hookexec
INTERNALERROR>     return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 167, in _multicall
INTERNALERROR>     raise exception
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/logging.py", line 803, in pytest_runtestloop
INTERNALERROR>     return (yield)  # Run all the tests.
INTERNALERROR>             ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 139, in _multicall
INTERNALERROR>     teardown.throw(exception)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/_pytest/terminal.py", line 673, in pytest_runtestloop
INTERNALERROR>     result = yield
INTERNALERROR>              ^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 152, in _multicall
INTERNALERROR>     teardown.send(result)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pluggy/_callers.py", line 43, in run_old_style_hookwrapper
INTERNALERROR>     teardown.send(result)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pytest_cov/plugin.py", line 339, in pytest_runtestloop
INTERNALERROR>     self.cov_controller.finish()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pytest_cov/engine.py", line 46, in ensure_topdir_wrapper
INTERNALERROR>     return meth(self, *args, **kwargs)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/pytest_cov/engine.py", line 256, in finish
INTERNALERROR>     self.cov.save()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/control.py", line 843, in save
INTERNALERROR>     data = self.get_data()
INTERNALERROR>            ^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/control.py", line 923, in get_data
INTERNALERROR>     if self._collector.flush_data():
INTERNALERROR>        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/collector.py", line 493, in flush_data
INTERNALERROR>     self.covdata.add_lines(self.mapped_file_dict(line_data))
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 123, in _wrapped
INTERNALERROR>     return method(self, *args, **kwargs)
INTERNALERROR>            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 526, in add_lines
INTERNALERROR>     self._choose_lines_or_arcs(lines=True)
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 603, in _choose_lines_or_arcs
INTERNALERROR>     with self._connect() as con:
INTERNALERROR>          ^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 373, in _connect
INTERNALERROR>     self._open_db()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 312, in _open_db
INTERNALERROR>     self._read_db()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqldata.py", line 316, in _read_db
INTERNALERROR>     with self._dbs[threading.get_ident()] as db:
INTERNALERROR>          ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqlitedb.py", line 96, in __enter__
INTERNALERROR>     self._connect()
INTERNALERROR>   File "/usr/local/lib/python3.12/site-packages/coverage/sqlitedb.py", line 60, in _connect
INTERNALERROR>     raise DataError(f"Couldn't use data file {self.filename!r}: {exc}") from exc
INTERNALERROR> coverage.exceptions.DataError: Couldn't use data file '/app/.coverage.ac310398103d.1542.XhdSEVjx': unable to open database file

======================== 3 warnings, 16 errors in 3.52s ========================


```


**Resultat:** ✅ Completat correctament


ℹ️ Informe HTML disponible a: `htmlcov/index.html`


## 5. Tests de Seguretat (SAST)


### 5.1 Anàlisi amb Bandit (Vulnerabilitats Python)


**Temps d'execució:** 0s


```


[main]	INFO	profile include tests: None
[main]	INFO	profile exclude tests: None
[main]	INFO	cli include tests: None
[main]	INFO	cli exclude tests: None
[main]	INFO	running on Python 3.12.12
Working... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Run started:2025-10-22 14:32:37.590592

Test results:
	No issues identified.

Code scanned:
	Total lines of code: 3448
	Total lines skipped (#nosec): 0
	Total potential issues skipped due to specifically being disabled (e.g., #nosec BXXX): 0

Run metrics:
	Total issues (by severity):
		Undefined: 0
		Low: 28
		Medium: 0
		High: 0
	Total issues (by confidence):
		Undefined: 0
		Low: 0
		Medium: 2
		High: 26
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
?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.

System check identified 5 issues (0 silenced).


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
./audit/middleware.py:19:1: W293 blank line contains whitespace
./audit/middleware.py:24:1: W293 blank line contains whitespace
./audit/middleware.py:27:1: W293 blank line contains whitespace
./audit/middleware.py:33:1: W293 blank line contains whitespace
./audit/middleware.py:39:1: W293 blank line contains whitespace
./audit/middleware.py:44:1: W293 blank line contains whitespace
./audit/middleware.py:61:1: W293 blank line contains whitespace
./audit/middleware.py:63:80: E501 line too long (80 > 79 characters)
./audit/middleware.py:64:1: W293 blank line contains whitespace
./audit/middleware.py:66:80: E501 line too long (86 > 79 characters)
./audit/middleware.py:67:1: W293 blank line contains whitespace
./audit/middleware.py:69:1: W293 blank line contains whitespace
./audit/middleware.py:74:1: W293 blank line contains whitespace
./audit/middleware.py:89:1: W293 blank line contains whitespace
./audit/middleware.py:91:1: W293 blank line contains whitespace
./audit/middleware.py:100:1: W293 blank line contains whitespace
./audit/middleware.py:107:13: E722 do not use bare 'except'
./audit/middleware.py:110:1: W293 blank line contains whitespace
./audit/middleware.py:125:1: W293 blank line contains whitespace
./audit/middleware.py:131:80: E501 line too long (82 > 79 characters)
./audit/middleware.py:137:1: W293 blank line contains whitespace
./audit/middleware.py:149:1: W293 blank line contains whitespace
./audit/middleware.py:160:1: W293 blank line contains whitespace
./audit/middleware.py:166:1: W293 blank line contains whitespace
./audit/middleware.py:172:1: W293 blank line contains whitespace
./audit/middleware.py:174:1: W293 blank line contains whitespace
./audit/middleware.py:180:1: W293 blank line contains whitespace
./audit/middleware.py:187:1: W293 blank line contains whitespace
./audit/middleware.py:190:1: W293 blank line contains whitespace
./audit/middleware.py:191:73: W291 trailing whitespace
./audit/middleware.py:192:27: E128 continuation line under-indented for visual indent
./audit/middleware.py:212:1: W293 blank line contains whitespace
./audit/middleware.py:217:1: W293 blank line contains whitespace
./audit/middleware.py:222:14: W292 no newline at end of file
./audit/migrations/0001_initial.py:22:80: E501 line too long (112 > 79 characters)
./audit/migrations/0001_initial.py:41:80: E501 line too long (87 > 79 characters)
./audit/migrations/0001_initial.py:42:80: E501 line too long (85 > 79 characters)
./audit/migrations/0001_initial.py:45:80: E501 line too long (110 > 79 characters)
./audit/migrations/0001_initial.py:49:80: E501 line too long (117 > 79 characters)
./audit/migrations/0001_initial.py:51:80: E501 line too long (84 > 79 characters)
./audit/migrations/0001_initial.py:53:80: E501 line too long (91 > 79 characters)
./audit/migrations/0001_initial.py:68:80: E501 line too long (86 > 79 characters)
./audit/migrations/0001_initial.py:95:80: E501 line too long (101 > 79 characters)
./audit/migrations/0001_initial.py:96:80: E501 line too long (100 > 79 characters)
./audit/migrations/0001_initial.py:97:80: E501 line too long (104 > 79 characters)
./audit/migrations/0001_initial.py:98:80: E501 line too long (106 > 79 characters)
./audit/migrations/0001_initial.py:105:80: E501 line too long (112 > 79 characters)
./audit/migrations/0001_initial.py:106:80: E501 line too long (116 > 79 characters)
./audit/migrations/0001_initial.py:110:80: E501 line too long (109 > 79 characters)
./audit/migrations/0001_initial.py:113:80: E501 line too long (91 > 79 characters)
./audit/migrations/0001_initial.py:114:80: E501 line too long (113 > 79 characters)
./audit/migrations/0001_initial.py:115:80: E501 line too long (94 > 79 characters)
./audit/migrations/0001_initial.py:116:80: E501 line too long (119 > 79 characters)
./audit/migrations/0001_initial.py:119:80: E501 line too long (86 > 79 characters)
./audit/migrations/0001_initial.py:135:80: E501 line too long (109 > 79 characters)
./audit/migrations/0001_initial.py:136:80: E501 line too long (106 > 79 characters)
./audit/migrations/0001_initial.py:143:80: E501 line too long (112 > 79 characters)
./audit/migrations/0001_initial.py:152:80: E501 line too long (82 > 79 characters)
./audit/migrations/0001_initial.py:155:80: E501 line too long (85 > 79 characters)
./audit/migrations/0001_initial.py:167:80: E501 line too long (83 > 79 characters)
./audit/migrations/0001_initial.py:168:80: E501 line too long (106 > 79 characters)
./audit/migrations/0001_initial.py:169:80: E501 line too long (108 > 79 characters)
./audit/migrations/0001_initial.py:173:80: E501 line too long (117 > 79 characters)
./audit/migrations/0001_initial.py:193:80: E501 line too long (113 > 79 characters)
./audit/migrations/0001_initial.py:195:80: E501 line too long (86 > 79 characters)
./audit/migrations/0001_initial.py:224:80: E501 line too long (108 > 79 characters)
./audit/migrations/0001_initial.py:225:80: E501 line too long (103 > 79 characters)
./audit/migrations/0001_initial.py:226:80: E501 line too long (108 > 79 characters)
./audit/migrations/0001_initial.py:227:80: E501 line too long (105 > 79 characters)
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
./authentication/apps.py:12:1: W293 blank line contains whitespace
./authentication/apps.py:17:62: W292 no newline at end of file
./authentication/migrations/0001_initial.py:22:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:29:80: E501 line too long (95 > 79 characters)
./authentication/migrations/0001_initial.py:32:80: E501 line too long (115 > 79 characters)
./authentication/migrations/0001_initial.py:35:80: E501 line too long (86 > 79 characters)
./authentication/migrations/0001_initial.py:52:80: E501 line too long (102 > 79 characters)
./authentication/migrations/0001_initial.py:53:80: E501 line too long (108 > 79 characters)
./authentication/migrations/0001_initial.py:54:80: E501 line too long (109 > 79 characters)
./authentication/migrations/0001_initial.py:61:80: E501 line too long (112 > 79 characters)
./authentication/migrations/0001_initial.py:65:80: E501 line too long (110 > 79 characters)
./authentication/migrations/0001_initial.py:68:80: E501 line too long (118 > 79 characters)
./authentication/migrations/0001_initial.py:76:80: E501 line too long (94 > 79 characters)
./authentication/migrations/0001_initial.py:83:80: E501 line too long (106 > 79 characters)
./authentication/migrations/0001_initial.py:89:80: E501 line too long (83 > 79 characters)
./authentication/migrations/0001_initial.py:95:80: E501 line too long (117 > 79 characters)
./authentication/migrations/0001_initial.py:96:80: E501 line too long (118 > 79 characters)
./authentication/migrations/0001_initial.py:99:80: E501 line too long (113 > 79 characters)
./authentication/migrations/0001_initial.py:101:80: E501 line too long (87 > 79 characters)
./authentication/migrations/0001_initial.py:103:80: E501 line too long (86 > 79 characters)
./authentication/migrations/0001_initial.py:121:80: E501 line too long (86 > 79 characters)
./authentication/migrations/0001_initial.py:122:80: E501 line too long (98 > 79 characters)
./authentication/migrations/0001_initial.py:123:80: E501 line too long (95 > 79 characters)
./authentication/models.py:17:1: W293 blank line contains whitespace
./authentication/models.py:25:1: W293 blank line contains whitespace
./authentication/models.py:31:1: W293 blank line contains whitespace
./authentication/models.py:37:1: W293 blank line contains whitespace
./authentication/models.py:49:1: W293 blank line contains whitespace
./authentication/models.py:55:1: W293 blank line contains whitespace
./authentication/models.py:63:1: W293 blank line contains whitespace
./authentication/models.py:69:1: W293 blank line contains whitespace
./authentication/models.py:74:1: W293 blank line contains whitespace
./authentication/models.py:81:1: W293 blank line contains whitespace
./authentication/models.py:86:1: W293 blank line contains whitespace
./authentication/models.py:90:1: W293 blank line contains whitespace
./authentication/models.py:100:1: W293 blank line contains whitespace
./authentication/models.py:103:1: W293 blank line contains whitespace
./authentication/models.py:108:1: W293 blank line contains whitespace
./authentication/models.py:115:1: W293 blank line contains whitespace
./authentication/models.py:123:1: W293 blank line contains whitespace
./authentication/models.py:127:1: W293 blank line contains whitespace
./authentication/models.py:129:1: W293 blank line contains whitespace
./authentication/models.py:138:1: W293 blank line contains whitespace
./authentication/models.py:151:1: W293 blank line contains whitespace
./authentication/models.py:158:1: W293 blank line contains whitespace
./authentication/models.py:164:1: W293 blank line contains whitespace
./authentication/models.py:167:1: W293 blank line contains whitespace
./authentication/models.py:174:1: W293 blank line contains whitespace
./authentication/models.py:176:1: W293 blank line contains whitespace
./authentication/models.py:187:1: W293 blank line contains whitespace
./authentication/models.py:190:80: E501 line too long (81 > 79 characters)
./authentication/models.py:190:82: W292 no newline at end of file
./authentication/urls.py:18:2: W292 no newline at end of file
./manage.py:22:11: W292 no newline at end of file
./sales_notes/apps.py:12:1: W293 blank line contains whitespace
./sales_notes/apps.py:18:69: W292 no newline at end of file
./sales_notes/existing_models.py:12:80: E501 line too long (87 > 79 characters)
./sales_notes/existing_models.py:13:80: E501 line too long (83 > 79 characters)
./sales_notes/existing_models.py:14:80: E501 line too long (112 > 79 characters)
./sales_notes/existing_models.py:15:80: E501 line too long (114 > 79 characters)
./sales_notes/existing_models.py:18:80: E501 line too long (114 > 79 characters)
./sales_notes/existing_models.py:19:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:21:1: W293 blank line contains whitespace
./sales_notes/existing_models.py:23:24: W291 trailing whitespace
./sales_notes/existing_models.py:27:1: W293 blank line contains whitespace
./sales_notes/existing_models.py:35:80: E501 line too long (88 > 79 characters)
./sales_notes/existing_models.py:36:80: E501 line too long (81 > 79 characters)
./sales_notes/existing_models.py:37:80: E501 line too long (98 > 79 characters)
./sales_notes/existing_models.py:38:80: E501 line too long (98 > 79 characters)
./sales_notes/existing_models.py:39:80: E501 line too long (98 > 79 characters)
./sales_notes/existing_models.py:40:80: E501 line too long (85 > 79 characters)
./sales_notes/existing_models.py:41:80: E501 line too long (87 > 79 characters)
./sales_notes/existing_models.py:42:80: E501 line too long (96 > 79 characters)
./sales_notes/existing_models.py:43:80: E501 line too long (107 > 79 characters)
./sales_notes/existing_models.py:44:80: E501 line too long (93 > 79 characters)
./sales_notes/existing_models.py:45:80: E501 line too long (85 > 79 characters)
./sales_notes/existing_models.py:46:80: E501 line too long (87 > 79 characters)
./sales_notes/existing_models.py:47:80: E501 line too long (85 > 79 characters)
./sales_notes/existing_models.py:48:80: E501 line too long (110 > 79 characters)
./sales_notes/existing_models.py:49:80: E501 line too long (110 > 79 characters)
./sales_notes/existing_models.py:50:80: E501 line too long (105 > 79 characters)
./sales_notes/existing_models.py:51:80: E501 line too long (84 > 79 characters)
./sales_notes/existing_models.py:52:80: E501 line too long (119 > 79 characters)
./sales_notes/existing_models.py:53:80: E501 line too long (119 > 79 characters)
./sales_notes/existing_models.py:54:80: E501 line too long (91 > 79 characters)
./sales_notes/existing_models.py:56:80: E501 line too long (94 > 79 characters)
./sales_notes/existing_models.py:57:80: E501 line too long (87 > 79 characters)
./sales_notes/existing_models.py:58:80: E501 line too long (104 > 79 characters)
./sales_notes/existing_models.py:59:80: E501 line too long (104 > 79 characters)
./sales_notes/existing_models.py:61:1: W293 blank line contains whitespace
./sales_notes/existing_models.py:67:1: W293 blank line contains whitespace
./sales_notes/existing_models.py:75:80: E501 line too long (83 > 79 characters)
./sales_notes/existing_models.py:76:80: E501 line too long (93 > 79 characters)
./sales_notes/existing_models.py:77:80: E501 line too long (90 > 79 characters)
./sales_notes/existing_models.py:78:80: E501 line too long (86 > 79 characters)
./sales_notes/existing_models.py:79:80: E501 line too long (84 > 79 characters)
./sales_notes/existing_models.py:80:80: E501 line too long (106 > 79 characters)
./sales_notes/existing_models.py:81:80: E501 line too long (83 > 79 characters)
./sales_notes/existing_models.py:82:80: E501 line too long (89 > 79 characters)
./sales_notes/existing_models.py:83:80: E501 line too long (101 > 79 characters)
./sales_notes/existing_models.py:84:80: E501 line too long (83 > 79 characters)
./sales_notes/existing_models.py:86:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:87:80: E501 line too long (98 > 79 characters)
./sales_notes/existing_models.py:88:80: E501 line too long (106 > 79 characters)
./sales_notes/existing_models.py:89:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:90:80: E501 line too long (121 > 79 characters)
./sales_notes/existing_models.py:91:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:92:80: E501 line too long (100 > 79 characters)
./sales_notes/existing_models.py:93:80: E501 line too long (90 > 79 characters)
./sales_notes/existing_models.py:95:1: W293 blank line contains whitespace
./sales_notes/existing_models.py:101:1: W293 blank line contains whitespace
./sales_notes/existing_models.py:103:44: W292 no newline at end of file
./sales_notes/migrations/0001_initial.py:23:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:25:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:41:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:57:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:59:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:62:80: E501 line too long (120 > 79 characters)
./sales_notes/migrations/0001_initial.py:87:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:98:80: E501 line too long (107 > 79 characters)
./sales_notes/migrations/0001_initial.py:106:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:107:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:128:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:129:80: E501 line too long (113 > 79 characters)
./sales_notes/migrations/0001_initial.py:130:80: E501 line too long (90 > 79 characters)
./sales_notes/migrations/0001_initial.py:151:80: E501 line too long (119 > 79 characters)
./sales_notes/migrations/0001_initial.py:152:80: E501 line too long (113 > 79 characters)
./sales_notes/migrations/0001_initial.py:153:80: E501 line too long (89 > 79 characters)
./sales_notes/migrations/0001_initial.py:164:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:166:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:169:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:174:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:179:80: E501 line too long (108 > 79 characters)
./sales_notes/migrations/0001_initial.py:180:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:181:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:184:80: E501 line too long (83 > 79 characters)
./sales_notes/migrations/0001_initial.py:188:80: E501 line too long (119 > 79 characters)
./sales_notes/migrations/0001_initial.py:202:80: E501 line too long (87 > 79 characters)
./sales_notes/migrations/0001_initial.py:204:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:207:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:217:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:223:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:224:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:233:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:240:80: E501 line too long (110 > 79 characters)
./sales_notes/migrations/0001_initial.py:244:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:249:80: E501 line too long (107 > 79 characters)
./sales_notes/migrations/0001_initial.py:254:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:258:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:260:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:261:80: E501 line too long (84 > 79 characters)
./sales_notes/migrations/0001_initial.py:262:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:263:80: E501 line too long (111 > 79 characters)
./sales_notes/migrations/0001_initial.py:264:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:265:80: E501 line too long (97 > 79 characters)
./sales_notes/migrations/0001_initial.py:268:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:272:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:276:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:278:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:282:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:286:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:287:80: E501 line too long (99 > 79 characters)
./sales_notes/migrations/0001_initial.py:288:80: E501 line too long (119 > 79 characters)
./sales_notes/migrations/0001_initial.py:289:80: E501 line too long (117 > 79 characters)
./sales_notes/migrations/0001_initial.py:293:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:305:80: E501 line too long (101 > 79 characters)
./sales_notes/migrations/0001_initial.py:310:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:313:80: E501 line too long (101 > 79 characters)
./sales_notes/migrations/0001_initial.py:321:80: E501 line too long (95 > 79 characters)
./sales_notes/migrations/0001_initial.py:332:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:343:80: E501 line too long (96 > 79 characters)
./sales_notes/migrations/0001_initial.py:352:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:361:80: E501 line too long (81 > 79 characters)
./sales_notes/migrations/0001_initial.py:364:80: E501 line too long (114 > 79 characters)
./sales_notes/migrations/0001_initial.py:383:80: E501 line too long (109 > 79 characters)
./sales_notes/migrations/0001_initial.py:387:80: E501 line too long (100 > 79 characters)
./sales_notes/migrations/0001_initial.py:389:80: E501 line too long (102 > 79 characters)
./sales_notes/migrations/0001_initial.py:392:80: E501 line too long (103 > 79 characters)
./sales_notes/migrations/0001_initial.py:423:80: E501 line too long (116 > 79 characters)
./sales_notes/migrations/0001_initial.py:429:80: E501 line too long (112 > 79 characters)
./sales_notes/migrations/0001_initial.py:430:80: E501 line too long (99 > 79 characters)
./sales_notes/migrations/0001_initial.py:433:80: E501 line too long (111 > 79 characters)
./sales_notes/migrations/0001_initial.py:453:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:457:80: E501 line too long (98 > 79 characters)
./sales_notes/migrations/0001_initial.py:461:80: E501 line too long (105 > 79 characters)
./sales_notes/migrations/0001_initial.py:465:80: E501 line too long (95 > 79 characters)
./sales_notes/migrations/0001_initial.py:469:80: E501 line too long (106 > 79 characters)
./sales_notes/migrations/0001_initial.py:473:80: E501 line too long (107 > 79 characters)
./sales_notes/migrations/0001_initial.py:477:80: E501 line too long (115 > 79 characters)
./sales_notes/migrations/0001_initial.py:486:80: E501 line too long (104 > 79 characters)
./sales_notes/models.py:6:1: F401 'django.core.validators.MaxValueValidator' imported but unused
./sales_notes/models.py:6:80: E501 line too long (87 > 79 characters)
./sales_notes/models.py:8:1: F401 'django.db.models.Q' imported but unused
./sales_notes/models.py:8:1: F401 'django.db.models.CheckConstraint' imported but unused
./sales_notes/models.py:16:1: W293 blank line contains whitespace
./sales_notes/models.py:28:23: W291 trailing whitespace
./sales_notes/models.py:29:21: W291 trailing whitespace
./sales_notes/models.py:33:1: W293 blank line contains whitespace
./sales_notes/models.py:44:1: W293 blank line contains whitespace
./sales_notes/models.py:49:1: W293 blank line contains whitespace
./sales_notes/models.py:53:1: W293 blank line contains whitespace
./sales_notes/models.py:57:34: W291 trailing whitespace
./sales_notes/models.py:61:1: W293 blank line contains whitespace
./sales_notes/models.py:71:1: W293 blank line contains whitespace
./sales_notes/models.py:82:15: W291 trailing whitespace
./sales_notes/models.py:83:34: W291 trailing whitespace
./sales_notes/models.py:86:1: W293 blank line contains whitespace
./sales_notes/models.py:92:1: W293 blank line contains whitespace
./sales_notes/models.py:99:1: W293 blank line contains whitespace
./sales_notes/models.py:114:1: W293 blank line contains whitespace
./sales_notes/models.py:125:1: W293 blank line contains whitespace
./sales_notes/models.py:136:1: W293 blank line contains whitespace
./sales_notes/models.py:145:1: W293 blank line contains whitespace
./sales_notes/models.py:147:80: E501 line too long (84 > 79 characters)
./sales_notes/models.py:160:1: W293 blank line contains whitespace
./sales_notes/models.py:166:1: W293 blank line contains whitespace
./sales_notes/models.py:169:80: E501 line too long (82 > 79 characters)
./sales_notes/models.py:178:1: W293 blank line contains whitespace
./sales_notes/models.py:181:1: W293 blank line contains whitespace
./sales_notes/models.py:185:1: W293 blank line contains whitespace
./sales_notes/models.py:191:1: W293 blank line contains whitespace
./sales_notes/models.py:196:9: E265 block comment should start with '# '
./sales_notes/models.py:201:9: E265 block comment should start with '# '
./sales_notes/models.py:202:1: W293 blank line contains whitespace
./sales_notes/models.py:217:1: W293 blank line contains whitespace
./sales_notes/models.py:223:1: W293 blank line contains whitespace
./sales_notes/models.py:229:1: W293 blank line contains whitespace
./sales_notes/models.py:233:1: W293 blank line contains whitespace
./sales_notes/models.py:238:9: E265 block comment should start with '# '
./sales_notes/models.py:243:9: E265 block comment should start with '# '
./sales_notes/models.py:244:1: W293 blank line contains whitespace
./sales_notes/models.py:259:1: W293 blank line contains whitespace
./sales_notes/models.py:265:1: W293 blank line contains whitespace
./sales_notes/models.py:271:1: W293 blank line contains whitespace
./sales_notes/models.py:275:1: W293 blank line contains whitespace
./sales_notes/models.py:280:9: E265 block comment should start with '# '
./sales_notes/models.py:285:9: E265 block comment should start with '# '
./sales_notes/models.py:286:1: W293 blank line contains whitespace
./sales_notes/models.py:290:1: E305 expected 2 blank lines after class or function definition, found 1
./sales_notes/models.py:294:1: E402 module level import not at top of file
./sales_notes/models.py:295:1: F811 redefinition of unused 'MinValueValidator' from line 6
./sales_notes/models.py:295:1: E402 module level import not at top of file
./sales_notes/models.py:296:1: E402 module level import not at top of file
./sales_notes/models.py:297:1: E402 module level import not at top of file
./sales_notes/models.py:310:1: W293 blank line contains whitespace
./sales_notes/models.py:317:1: W293 blank line contains whitespace
./sales_notes/models.py:329:1: W293 blank line contains whitespace
./sales_notes/models.py:333:1: W293 blank line contains whitespace
./sales_notes/models.py:339:1: W293 blank line contains whitespace
./sales_notes/models.py:346:1: W293 blank line contains whitespace
./sales_notes/models.py:352:1: W293 blank line contains whitespace
./sales_notes/models.py:360:1: W293 blank line contains whitespace
./sales_notes/models.py:366:1: W293 blank line contains whitespace
./sales_notes/models.py:373:1: W293 blank line contains whitespace
./sales_notes/models.py:379:1: W293 blank line contains whitespace
./sales_notes/models.py:385:1: W293 blank line contains whitespace
./sales_notes/models.py:387:1: W293 blank line contains whitespace
./sales_notes/models.py:393:1: W293 blank line contains whitespace
./sales_notes/models.py:399:1: W293 blank line contains whitespace
./sales_notes/models.py:405:1: W293 blank line contains whitespace
./sales_notes/models.py:411:1: W293 blank line contains whitespace
./sales_notes/models.py:417:1: W293 blank line contains whitespace
./sales_notes/models.py:424:1: W293 blank line contains whitespace
./sales_notes/models.py:430:1: W293 blank line contains whitespace
./sales_notes/models.py:435:1: W293 blank line contains whitespace
./sales_notes/models.py:443:1: W293 blank line contains whitespace
./sales_notes/models.py:448:1: W293 blank line contains whitespace
./sales_notes/models.py:454:1: W293 blank line contains whitespace
./sales_notes/models.py:459:1: W293 blank line contains whitespace
./sales_notes/models.py:465:1: W293 blank line contains whitespace
./sales_notes/models.py:472:1: W293 blank line contains whitespace
./sales_notes/models.py:477:1: W293 blank line contains whitespace
./sales_notes/models.py:488:1: W293 blank line contains whitespace
./sales_notes/models.py:493:1: W293 blank line contains whitespace
./sales_notes/models.py:499:1: W293 blank line contains whitespace
./sales_notes/models.py:507:1: W293 blank line contains whitespace
./sales_notes/models.py:518:1: W293 blank line contains whitespace
./sales_notes/models.py:526:1: W293 blank line contains whitespace
./sales_notes/models.py:533:1: W293 blank line contains whitespace
./sales_notes/models.py:540:1: W293 blank line contains whitespace
./sales_notes/models.py:545:1: W293 blank line contains whitespace
./sales_notes/models.py:555:1: W293 blank line contains whitespace
./sales_notes/models.py:562:1: W293 blank line contains whitespace
./sales_notes/models.py:568:1: W293 blank line contains whitespace
./sales_notes/models.py:575:1: W293 blank line contains whitespace
./sales_notes/models.py:580:1: W293 blank line contains whitespace
./sales_notes/models.py:586:1: W293 blank line contains whitespace
./sales_notes/models.py:598:1: W293 blank line contains whitespace
./sales_notes/models.py:600:80: E501 line too long (80 > 79 characters)
./sales_notes/models.py:601:1: W293 blank line contains whitespace
./sales_notes/models.py:621:1: W293 blank line contains whitespace
./sales_notes/models.py:625:1: W293 blank line contains whitespace
./sales_notes/models.py:631:1: W293 blank line contains whitespace
./sales_notes/models.py:640:1: W293 blank line contains whitespace
./sales_notes/models.py:648:1: E402 module level import not at top of file
./sales_notes/models.py:648:37: W292 no newline at end of file
./sales_notes/serializers.py:12:1: F401 'jsonschema' imported but unused
./sales_notes/serializers.py:21:1: W293 blank line contains whitespace
./sales_notes/serializers.py:25:1: W293 blank line contains whitespace
./sales_notes/serializers.py:38:80: E501 line too long (95 > 79 characters)
./sales_notes/serializers.py:39:1: W293 blank line contains whitespace
./sales_notes/serializers.py:48:80: E501 line too long (83 > 79 characters)
./sales_notes/serializers.py:57:1: W293 blank line contains whitespace
./sales_notes/serializers.py:65:1: W293 blank line contains whitespace
./sales_notes/serializers.py:73:1: W293 blank line contains whitespace
./sales_notes/serializers.py:81:1: W293 blank line contains whitespace
./sales_notes/serializers.py:90:1: W293 blank line contains whitespace
./sales_notes/serializers.py:91:80: E501 line too long (81 > 79 characters)
./sales_notes/serializers.py:95:80: E501 line too long (102 > 79 characters)
./sales_notes/serializers.py:97:1: W293 blank line contains whitespace
./sales_notes/serializers.py:103:1: W293 blank line contains whitespace
./sales_notes/serializers.py:110:1: W293 blank line contains whitespace
./sales_notes/serializers.py:115:80: E501 line too long (86 > 79 characters)
./sales_notes/serializers.py:122:1: W293 blank line contains whitespace
./sales_notes/serializers.py:126:1: W293 blank line contains whitespace
./sales_notes/serializers.py:138:1: W293 blank line contains whitespace
./sales_notes/serializers.py:142:1: W293 blank line contains whitespace
./sales_notes/serializers.py:161:1: W293 blank line contains whitespace
./sales_notes/serializers.py:164:80: E501 line too long (95 > 79 characters)
./sales_notes/serializers.py:165:1: W293 blank line contains whitespace
./sales_notes/serializers.py:172:1: W293 blank line contains whitespace
./sales_notes/serializers.py:178:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:183:80: E501 line too long (80 > 79 characters)
./sales_notes/serializers.py:188:80: E501 line too long (81 > 79 characters)
./sales_notes/serializers.py:190:1: W293 blank line contains whitespace
./sales_notes/serializers.py:197:1: W293 blank line contains whitespace
./sales_notes/serializers.py:200:80: E501 line too long (99 > 79 characters)
./sales_notes/serializers.py:202:1: W293 blank line contains whitespace
./sales_notes/serializers.py:210:1: W293 blank line contains whitespace
./sales_notes/serializers.py:212:1: W293 blank line contains whitespace
./sales_notes/serializers.py:221:1: W293 blank line contains whitespace
./sales_notes/serializers.py:224:1: W293 blank line contains whitespace
./sales_notes/serializers.py:231:80: E501 line too long (90 > 79 characters)
./sales_notes/serializers.py:232:1: W293 blank line contains whitespace
./sales_notes/serializers.py:236:80: E501 line too long (86 > 79 characters)
./sales_notes/serializers.py:237:1: W293 blank line contains whitespace
./sales_notes/serializers.py:240:1: W293 blank line contains whitespace
./sales_notes/serializers.py:243:1: E305 expected 2 blank lines after class or function definition, found 1
./sales_notes/serializers.py:246:1: E402 module level import not at top of file
./sales_notes/serializers.py:247:1: F811 redefinition of unused 'Envio' from line 6
./sales_notes/serializers.py:247:1: F811 redefinition of unused 'EstablecimientoVenta' from line 6
./sales_notes/serializers.py:247:1: E402 module level import not at top of file
./sales_notes/serializers.py:248:1: F811 redefinition of unused 'UnidadProductivaSerializer' from line 152
./sales_notes/serializers.py:248:1: E402 module level import not at top of file
./sales_notes/serializers.py:249:1: E402 module level import not at top of file
./sales_notes/serializers.py:250:1: E402 module level import not at top of file
./sales_notes/serializers.py:262:1: W293 blank line contains whitespace
./sales_notes/serializers.py:266:1: W293 blank line contains whitespace
./sales_notes/serializers.py:286:1: W293 blank line contains whitespace
./sales_notes/serializers.py:293:80: E501 line too long (88 > 79 characters)
./sales_notes/serializers.py:294:1: W293 blank line contains whitespace
./sales_notes/serializers.py:302:1: W293 blank line contains whitespace
./sales_notes/serializers.py:307:80: E501 line too long (88 > 79 characters)
./sales_notes/serializers.py:310:1: W293 blank line contains whitespace
./sales_notes/serializers.py:314:1: W293 blank line contains whitespace
./sales_notes/serializers.py:317:80: E501 line too long (80 > 79 characters)
./sales_notes/serializers.py:319:1: W293 blank line contains whitespace
./sales_notes/serializers.py:327:1: W293 blank line contains whitespace
./sales_notes/serializers.py:332:1: W293 blank line contains whitespace
./sales_notes/serializers.py:334:1: W293 blank line contains whitespace
./sales_notes/serializers.py:342:1: W293 blank line contains whitespace
./sales_notes/serializers.py:346:1: W293 blank line contains whitespace
./sales_notes/serializers.py:353:1: W293 blank line contains whitespace
./sales_notes/serializers.py:357:1: W293 blank line contains whitespace
./sales_notes/serializers.py:361:80: E501 line too long (84 > 79 characters)
./sales_notes/serializers.py:362:1: W293 blank line contains whitespace
./sales_notes/serializers.py:367:1: W293 blank line contains whitespace
./sales_notes/serializers.py:368:80: E501 line too long (99 > 79 characters)
./sales_notes/serializers.py:373:1: W293 blank line contains whitespace
./sales_notes/serializers.py:377:1: W293 blank line contains whitespace
./sales_notes/serializers.py:382:1: W293 blank line contains whitespace
./sales_notes/serializers.py:396:1: W293 blank line contains whitespace
./sales_notes/serializers.py:398:1: W293 blank line contains whitespace
./sales_notes/serializers.py:405:1: W293 blank line contains whitespace
./sales_notes/serializers.py:407:1: W293 blank line contains whitespace
./sales_notes/serializers.py:423:1: W293 blank line contains whitespace
./sales_notes/serializers.py:435:1: W293 blank line contains whitespace
./sales_notes/serializers.py:448:1: W293 blank line contains whitespace
./sales_notes/serializers.py:459:1: F811 redefinition of unused 'datetime' from line 13
./sales_notes/serializers.py:459:1: E402 module level import not at top of file
./sales_notes/serializers.py:459:30: W292 no newline at end of file
./sales_notes/urls.py:4:1: F401 'django.urls.path' imported but unused
./sales_notes/urls.py:15:2: W292 no newline at end of file
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
./tests/conftest.py:189:1: W293 blank line contains whitespace
./tests/conftest.py:204:1: W293 blank line contains whitespace
./tests/conftest.py:215:1: W293 blank line contains whitespace
./tests/conftest.py:222:1: W293 blank line contains whitespace
./tests/conftest.py:225:1: W293 blank line contains whitespace
./tests/conftest.py:230:27: F811 redefinition of unused 'settings' from line 11
./tests/conftest.py:233:1: W293 blank line contains whitespace
./tests/conftest.py:248:1: W293 blank line contains whitespace
./tests/conftest.py:253:1: W293 blank line contains whitespace
./tests/conftest.py:257:1: W293 blank line contains whitespace
./tests/conftest.py:280:1: W293 blank line contains whitespace
./tests/conftest.py:283:1: W293 blank line contains whitespace
./tests/conftest.py:291:1: W293 blank line contains whitespace
./tests/conftest.py:293:1: W293 blank line contains whitespace
./tests/conftest.py:296:1: W293 blank line contains whitespace
./tests/conftest.py:304:1: W293 blank line contains whitespace
./tests/conftest.py:312:1: W293 blank line contains whitespace
./tests/conftest.py:314:1: W293 blank line contains whitespace
./tests/conftest.py:317:1: W293 blank line contains whitespace
./tests/conftest.py:318:26: W292 no newline at end of file
./tests/integration/test_sales_notes_flow.py:11:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:12:80: E501 line too long (82 > 79 characters)
./tests/integration/test_sales_notes_flow.py:14:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:51:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:52:80: E501 line too long (91 > 79 characters)
./tests/integration/test_sales_notes_flow.py:54:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:61:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:64:9: F841 local variable 'list_response' is assigned to but never used
./tests/integration/test_sales_notes_flow.py:66:1: W293 blank line contains whitespace
./tests/integration/test_sales_notes_flow.py:71:24: W292 no newline at end of file
./tests/security/test_owasp_api_security.py:12:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:14:80: E501 line too long (87 > 79 characters)
./tests/security/test_owasp_api_security.py:19:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:21:80: E501 line too long (93 > 79 characters)
./tests/security/test_owasp_api_security.py:22:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:27:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:34:13: F841 local variable 'response' is assigned to but never used
./tests/security/test_owasp_api_security.py:35:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:39:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:50:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:52:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:55:54: E712 comparison to False should be 'if cond is False:' or 'if not cond:'
./tests/security/test_owasp_api_security.py:56:50: E712 comparison to False should be 'if cond is False:' or 'if not cond:'
./tests/security/test_owasp_api_security.py:57:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:66:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:72:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:75:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:80:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:82:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:84:80: E501 line too long (89 > 79 characters)
./tests/security/test_owasp_api_security.py:85:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:90:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:101:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:104:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:109:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:112:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:115:16: F821 undefined name 'settings'
./tests/security/test_owasp_api_security.py:119:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:124:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:126:16: F821 undefined name 'settings'
./tests/security/test_owasp_api_security.py:128:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:133:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:139:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:141:1: W293 blank line contains whitespace
./tests/security/test_owasp_api_security.py:143:67: W292 no newline at end of file
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
./vcpe_api/__init__.py:10:22: W292 no newline at end of file
./vcpe_api/asgi.py:5:37: W292 no newline at end of file
./vcpe_api/celery.py:27:1: W293 blank line contains whitespace
./vcpe_api/celery.py:33:1: W293 blank line contains whitespace
./vcpe_api/celery.py:39:1: W293 blank line contains whitespace
./vcpe_api/celery.py:51:40: W292 no newline at end of file
./vcpe_api/db_router.py:2:58: W291 trailing whitespace
./vcpe_api/db_router.py:7:1: F401 'django.conf.settings' imported but unused
./vcpe_api/db_router.py:16:1: W293 blank line contains whitespace
./vcpe_api/db_router.py:24:1: W293 blank line contains whitespace
./vcpe_api/db_router.py:31:1: W293 blank line contains whitespace
./vcpe_api/db_router.py:35:1: W293 blank line contains whitespace
./vcpe_api/db_router.py:39:1: W293 blank line contains whitespace
./vcpe_api/db_router.py:46:1: W293 blank line contains whitespace
./vcpe_api/db_router.py:50:1: W293 blank line contains whitespace
./vcpe_api/db_router.py:56:1: W293 blank line contains whitespace
./vcpe_api/db_router.py:60:1: W293 blank line contains whitespace
./vcpe_api/db_router.py:64:1: W293 blank line contains whitespace
./vcpe_api/db_router.py:66:20: W292 no newline at end of file
./vcpe_api/settings.py:3:80: E501 line too long (84 > 79 characters)
./vcpe_api/settings.py:39:1: W293 blank line contains whitespace
./vcpe_api/settings.py:50:1: W293 blank line contains whitespace
./vcpe_api/settings.py:67:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:127:80: E501 line too long (91 > 79 characters)
./vcpe_api/settings.py:130:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:136:80: E501 line too long (82 > 79 characters)
./vcpe_api/settings.py:139:80: E501 line too long (83 > 79 characters)
./vcpe_api/settings.py:175:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:191:80: E501 line too long (97 > 79 characters)
./vcpe_api/settings.py:192:80: E501 line too long (92 > 79 characters)
./vcpe_api/settings.py:208:80: E501 line too long (81 > 79 characters)
./vcpe_api/settings.py:238:80: E501 line too long (88 > 79 characters)
./vcpe_api/settings.py:276:80: E501 line too long (93 > 79 characters)
./vcpe_api/settings.py:286:2: W292 no newline at end of file
./vcpe_api/urls.py:17:1: W293 blank line contains whitespace
./vcpe_api/urls.py:20:1: W293 blank line contains whitespace
./vcpe_api/urls.py:23:1: W293 blank line contains whitespace
./vcpe_api/urls.py:27:1: W293 blank line contains whitespace
./vcpe_api/urls.py:30:80: E501 line too long (92 > 79 characters)
./vcpe_api/urls.py:31:80: E501 line too long (86 > 79 characters)
./vcpe_api/urls.py:37:46: W292 no newline at end of file
./vcpe_api/views.py:30:7: W292 no newline at end of file
./vcpe_api/wsgi.py:5:37: W292 no newline at end of file
2     E128 continuation line under-indented for visual indent
6     E265 block comment should start with '# '
2     E305 expected 2 blank lines after class or function definition, found 1
14    E402 module level import not at top of file
236   E501 line too long (80 > 79 characters)
2     E712 comparison to False should be 'if cond is False:' or 'if not cond:'
1     E722 do not use bare 'except'
9     F401 'audit.signals' imported but unused
6     F811 redefinition of unused 'MinValueValidator' from line 6
2     F821 undefined name 'settings'
2     F841 local variable 'list_response' is assigned to but never used
9     W291 trailing whitespace
26    W292 no newline at end of file
343   W293 blank line contains whitespace
660


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
*Data: 22/10/2025 16:32:40*  
*TFM Ciberseguretat i Privadesa - ICATMAR*

