# Guia de Correccions de Seguretat

Aquest document explica com corregir els problemes detectats per Bandit i Django Security Check.

## 📊 Resum de problemes

### Bandit
- **1 Medium** (B104: hardcoded_bind_all_interfaces) - ✅ CORREGIT
- **184 Low** - La majoria són warnings menors
- **177 High confidence** - Revisar segons prioritat

### Django Security Check
- **12 Warnings** - Configuracions de producció

---

## ✅ Problemes Corregits

### 1. B104: Hardcoded bind all interfaces

**Problema:** Ús de `'0.0.0.0'` com a fallback per IP
```python
# ABANS (authentication/views.py:48)
ip = request.META.get("REMOTE_ADDR", "0.0.0.0")
```

**Solució:** Utilitzar `'unknown'` en lloc de `'0.0.0.0'`
```python
# DESPRÉS
ip = request.META.get('REMOTE_ADDR', 'unknown')  # nosec B104
```

**Fitxer:** `authentication/views.py:47`
**Estat:** ✅ Corregit

---

## 🔧 Problemes per Corregir

### 2. DRF Spectacular Type Hints

**Problema:** drf_spectacular no pot resoldre type hints per alguns mètodes

**Fitxers afectats:**
- `authentication/serializers.py` - `get_is_account_locked()`
- `sales_notes/serializers.py` - `get_num_especies()`, `get_num_establecimientos()`

**Solució:** Afegir type hints amb `@extend_schema_field`

#### authentication/serializers.py

```python
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    is_account_locked = serializers.SerializerMethodField()

    @extend_schema_field(serializers.BooleanField())
    def get_is_account_locked(self, obj) -> bool:
        """Retorna si el compte està bloquejat per massa intents fallits"""
        from defender.utils import is_already_locked
        return is_already_locked(request=None, username=obj.username)
```

#### sales_notes/serializers.py

```python
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

class EnvioListSerializer(serializers.ModelSerializer):
    num_especies = serializers.SerializerMethodField()
    num_establecimientos = serializers.SerializerMethodField()

    @extend_schema_field(serializers.IntegerField())
    def get_num_especies(self, obj) -> int:
        """Retorna el nombre total d'espècies"""
        return obj.especies.count() if hasattr(obj, 'especies') else 0

    @extend_schema_field(serializers.IntegerField())
    def get_num_establecimientos(self, obj) -> int:
        """Retorna el nombre d'establiments"""
        return obj.establecimientos.count() if hasattr(obj, 'establecimientos') else 0
```

---

### 3. Django Security Warnings (Producció)

**Problema:** Configuracions de seguretat no establertes

⚠️ **IMPORTANT:** Aquestes configuracions NOMÉS per PRODUCCIÓ (DEBUG=False)

**Fitxer creat:** `vcpe_api/settings_production.py`

#### Aplicar configuració de producció

**Opció 1: Importació condicional (Recomanat)**

Afegir al final de `vcpe_api/settings.py`:

```python
# Al final del fitxer settings.py
if not DEBUG:
    from .settings_production import *
```

**Opció 2: Variable d'entorn**

```bash
# .env
DJANGO_SETTINGS_MODULE=vcpe_api.settings_production
```

**Opció 3: Especificar en execució**

```bash
python manage.py runserver --settings=vcpe_api.settings_production
gunicorn vcpe_api.wsgi:application --settings=vcpe_api.settings_production
```

#### Configuracions aplicades (settings_production.py)

✅ **SECURE_HSTS_SECONDS** = 31536000 (1 any)
✅ **SECURE_SSL_REDIRECT** = True
✅ **SESSION_COOKIE_SECURE** = True
✅ **CSRF_COOKIE_SECURE** = True
✅ **DEBUG** = False (via .env)

#### Variables .env necessàries per producció

```bash
# .env.production
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=vostra_secret_key_super_segura_aqui
DJANGO_ALLOWED_HOSTS=vostredomini.cat,www.vostredomini.cat
DATABASE_URL=postgis://user:password@host:5432/dbname
REDIS_URL=redis://redis:6379/0
```

---

## 🔐 Checklist de Seguretat per Producció

### Abans de deploiar

- [ ] `DEBUG = False` al .env de producció
- [ ] `SECRET_KEY` diferent a desenvolupament
- [ ] `ALLOWED_HOSTS` configurat amb dominis reals
- [ ] Certificat SSL/TLS configurat al servidor web (nginx/apache)
- [ ] Variables d'entorn sensibles fora del codi
- [ ] Base de dades amb credencials fortes
- [ ] Firewall configurat
- [ ] Logs configurats i monitoritzats

### Verificar seguretat

```bash
# Executar security check
make check-security
# o
docker-compose exec api python manage.py check --deploy

# Executar bandit
make security-check
# o
docker-compose exec api bandit -r . -c pyproject.toml
```

---

## 📝 Warnings de Bandit (Low Severity)

La majoria dels 184 warnings Low són:
- Ús de `assert` en tests (normal i acceptable)
- Imports de mòduls (falsos positius)
- Patrons comuns de Django/DRF

**Recomanació:** Revisar manualment els warnings Medium i High, ignorar els Low si són falsos positius.

### Suprimir warnings específics

Si un warning és un fals positiu, afegir comentari `# nosec`:

```python
# Exemple: suppress B101 (assert_used) en tests
def test_something():
    assert value == expected  # nosec B101
```

O configurar a `pyproject.toml`:

```toml
[tool.bandit]
exclude_dirs = ["tests", "migrations", ".venv"]
skips = ["B101", "B601"]  # Skip assert_used i shell=True en contexts segurs
```

---

## 🚀 Executar Correccions

### 1. Instal·lar pre-commit hooks

```bash
./setup_dev.sh
# o manualment
make install-hooks
```

### 2. Aplicar format a tot el repositori

```bash
./format_all.sh
# o
make format
```

### 3. Executar linting

```bash
make lint
```

### 4. Executar security checks

```bash
make security-check
make check-security
```

### 5. Executar tests

```bash
make test
```

---

## 📚 Referències

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/5.1/topics/security/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [DRF Security](https://www.django-rest-framework.org/topics/security/)
