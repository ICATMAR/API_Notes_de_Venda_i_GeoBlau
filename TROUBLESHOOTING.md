# Troubleshooting - Problemes amb Tests

## Problema: Tests es queden penjats al 2.1 (Obtenir Token JWT)

### Símptomes
- Els tests de connectivitat passen ✓
- El test 2.1 "Obtenir Token JWT" es queda penjat sense resposta
- L'API no respon als requests

### Causes possibles

1. **Error d'import de drf_spectacular** (més probable)
2. Error de sintaxi als serializers modificats
3. Container no ha instal·lat dependències correctament

### Diagnòstic

Executeu el script de diagnòstic:

```bash
./diagnose_serializers.sh
```

Això comprovarà:
- ✓ Si els imports funcionen
- ✓ Si drf_spectacular està disponible
- ✓ Si hi ha errors als logs
- ✓ Si Django pot arrencar

### Solució 1: Reinstal·lar dependències al container

Si el problema és que drf-spectacular no està instal·lat:

```bash
# Aturar containers
docker-compose down

# Rebuild forçant pip install
docker-compose build --no-cache api

# Arrencar de nou
docker-compose up -d

# Verificar que està instal·lat
docker-compose exec api pip list | grep drf-spectacular
# Hauria de mostrar: drf-spectacular    0.27.2
```

### Solució 2: Rollback temporal dels decorators

Si el problema persisteix, podem fer rollback temporal dels decorators de drf_spectacular:

**authentication/serializers.py** - Línia 14, comentar import:
```python
# from drf_spectacular.utils import extend_schema_field
```

**authentication/serializers.py** - Línia 127, comentar decorator:
```python
# @extend_schema_field(serializers.BooleanField())
def get_is_account_locked(self, obj) -> bool:
```

**authentication/serializers.py** - Línia 353, comentar decorator:
```python
# @extend_schema_field(serializers.BooleanField())
def get_is_valid_token(self, obj) -> bool:
```

**sales_notes/serializers.py** - Línia 6, comentar import:
```python
# from drf_spectacular.utils import extend_schema_field
```

**sales_notes/serializers.py** - Línies 570 i 575, comentar decorators:
```python
# @extend_schema_field(serializers.IntegerField())
def get_num_establecimientos(self, obj) -> int:

# @extend_schema_field(serializers.IntegerField())
def get_num_especies(self, obj) -> int:
```

Després:
```bash
docker-compose restart api
./run_all_tests.sh
```

### Solució 3: Verificar logs de l'API

```bash
# Veure logs en temps real
docker-compose logs -f api

# En una altra terminal, executar els tests
./run_all_tests.sh
```

Busqueu errors com:
- `ModuleNotFoundError: No module named 'drf_spectacular'`
- `ImportError`
- `SyntaxError`
- `AttributeError`

### Solució 4: Test manual de l'endpoint

```bash
# Verificar que l'API respon
curl -v http://localhost:8000/health/

# Provar l'endpoint d'autenticació directament
curl -v -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin_test", "password": "TestSecure123!"}'
```

Si curl també es queda penjat, el problema és a l'API, no als tests.

### Solució 5: Entrar al container i provar manualment

```bash
# Entrar al container
docker-compose exec api bash

# Dins del container, provar imports
python manage.py shell
>>> from authentication.serializers import UserSerializer
>>> from sales_notes.serializers import EnvioListSerializer
>>> from drf_spectacular.utils import extend_schema_field
>>> # Si no hi ha errors, imports OK

# Verificar Django check
python manage.py check

# Sortir
exit
```

### Solució 6: Crear usuari de test si no existeix

```bash
docker-compose exec api python manage.py shell <<EOF
from authentication.models import APIUser
if not APIUser.objects.filter(username='admin_test').exists():
    user = APIUser.objects.create_user(
        username='admin_test',
        password='TestSecure123!',
        email='admin@test.com',
        organization='DARP'
    )
    print('Usuari admin_test creat')
else:
    print('Usuari admin_test ja existeix')
EOF
```

## Checklist de Verificació

- [ ] Container API està running: `docker-compose ps`
- [ ] Logs sense errors: `docker-compose logs api --tail=50`
- [ ] drf-spectacular instal·lat: `docker-compose exec api pip list | grep drf`
- [ ] Django check passa: `docker-compose exec api python manage.py check`
- [ ] Health endpoint respon: `curl http://localhost:8000/health/`
- [ ] Imports funcionen: `./diagnose_serializers.sh`
- [ ] Usuari test existeix: verificar a la solució 6

## Si tot falla...

Rollback complet dels canvis als serializers:

```bash
git diff authentication/serializers.py
git diff sales_notes/serializers.py

# Si voleu restaurar versió anterior
git checkout HEAD~3 -- authentication/serializers.py sales_notes/serializers.py

# Restart
docker-compose restart api
```

## Contacte

Si el problema persisteix, guardeu:
1. Output de `./diagnose_serializers.sh`
2. Logs: `docker-compose logs api > api_logs.txt`
3. Docker ps output: `docker-compose ps`
