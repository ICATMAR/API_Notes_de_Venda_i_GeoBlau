# VCPE API - Sistema de Recepció de Notes de Venda

API REST segura per rebre i processar notes de venda del sector pesquer, desenvolupada per ICATMAR.

## 🔒 Seguretat (Security by Design)

Aquest projecte segueix els principis de **Security by Design** i implementa:

- ✅ **OWASP API Security Top 10 2023** - Protecció contra les 10 vulnerabilitats més crítiques
- ✅ **TLS 1.3** - Xifratge en trànsit
- ✅ **JWT amb rotació** - Autenticació robusta
- ✅ **Rate Limiting** - Protecció contra DDoS i brute force
- ✅ **Validació exhaustiva** - JSON Schema validation
- ✅ **Auditoria completa** - Logs detallats de totes les operacions
- ✅ **Contenidors hardened** - Docker amb principi de mínim privilegi
- ✅ **Hashing Argon2** - Contrasenyes amb l'algorisme més segur
- ✅ **CSP, HSTS, X-Frame-Options** - Headers de seguretat

## 📋 Requisits

- Docker >= 20.10
- Docker Compose >= 2.0
- Git
- Make (opcional, però recomanat)

## 🚀 Instal·lació Ràpida

### 1. Clonar el repositori

```bash
git clone https://github.com/icatmar/vcpe-api.git
cd vcpe-api
```

### 2. Configurar variables d'entorn

```bash
make setup
# o manualment:
cp .env.example .env
```

**IMPORTANT**: Edita el fitxer `.env` i canvia les contrasenyes i secrets:

```bash
# Genera secrets segurs amb:
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 3. Inicialitzar l'entorn de desenvolupament

```bash
make init-dev
# o manualment:
make build
make up
sleep 10  # Esperar que els serveis estiguin llestos
make migrate
```

### 4. Crear un superusuari

```bash
make createsuperuser
```

### 5. Accedir a l'aplicació

- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/
- **Documentació API**: http://localhost:8000/api/docs/
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/

## 📁 Estructura del Projecte

```
vcpe-api/
├── .env.example              # Plantilla variables d'entorn
├── .gitignore               # Fitxers a ignorar per Git
├── .pre-commit-config.yaml  # Hooks de pre-commit
├── docker-compose.yml       # Orquestració de contenidors
├── Dockerfile              # Imatge Docker de l'aplicació
├── Makefile                # Comandes ràpides
├── pyproject.toml          # Configuració eines Python
├── requirements.txt        # Dependències Python
├── init_db.sql            # Script inicialització BD
├── README.md              # Aquest fitxer
│
├── vcpe_api/              # Configuració Django
│   ├── settings.py        # Settings principals
│   ├── urls.py            # URLs del projecte
│   └── wsgi.py            # WSGI application
│
├── sales_notes/           # App principal (notes de venda)
│   ├── models.py          # Models de dades
│   ├── serializers.py     # Serialitzadors DRF
│   ├── views.py           # Views de l'API
│   ├── urls.py            # URLs de l'app
│   └── tests/             # Tests
│
├── authentication/        # App d'autenticació
│   ├── models.py          # Model APIUser
│   ├── views.py           # Login/logout
│   └── permissions.py     # Permisos personalitzats
│
└── audit/                 # App d'auditoria
    ├── models.py          # Logs i events de seguretat
    ├── middleware.py      # Middleware d'auditoria
    └── signals.py         # Signals per logging automàtic
```

## 🛠️ Comandes Disponibles

### Gestió de Contenidors

```bash
make up              # Iniciar contenidors
make down            # Aturar contenidors
make restart         # Reiniciar contenidors
make logs            # Veure logs
make logs-api        # Veure només logs de l'API
```

### Base de Dades

```bash
make migrate         # Executar migracions
make makemigrations  # Crear migracions
make shell-db        # Obrir shell PostgreSQL
make backup-db       # Fer backup de la BD
make restore-db FILE=backup.sql  # Restaurar backup
```

### Desenvolupament

```bash
make shell           # Obrir shell dins el contenidor
make test            # Executar tots els tests
make test-unit       # Tests unitaris
make test-security   # Tests de seguretat
make coverage        # Generar informe de cobertura
make lint            # Executar linters
make format          # Formatar codi (black + isort)
```

### Seguretat

```bash
make security-check  # Comprovar vulnerabilitats (bandit + safety)
make check-security  # Django security check
make pre-commit-run  # Executar totes les validacions
```

## 🔐 Autenticació

L'API utilitza **JWT (JSON Web Tokens)** per autenticació.

### 1. Obtenir token

```bash
POST /api/auth/token/
Content-Type: application/json

{
  "username": "usuari",
  "password": "contrasenya"
}
```

**Resposta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Usar el token

```bash
GET /api/sales-notes/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### 3. Refrescar token

```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 📝 Ús de l'API

### Enviar una nota de venda

```bash
POST /api/sales-notes/envios/
Authorization: Bearer <token>
Content-Type: application/json

{
  "NumEnvio": "ENV20251016001",
  "TipoRespuesta": 1,
  "EstablecimientosVenta": {
    "EstablecimientoVenta": [
      {
        "NumIdentificacionEstablec": "LLOTJA001",
        "NombreEstablecimiento": "Llotja de Barcelona" ,
        "Ventas": {
          "VentasUnidadProductiva": [
            {
              "DatosUnidadProductiva": {
                "MetodoProduccion": 1,
                "CodigoBuque": "3-PM-1-234",
                "PuertoAL5": "ESBAR",
                "FechaRegresoPuerto": "2025-10-16T08:30:00Z"
              },
              "Especies": {
                "Especie": [
                  {
                    "NumDocVenta": "NV2025001",
                    "EspecieAL3": "HKE",
                    "FechaVenta": "2025-10-16T10:00:00Z",
                    "Cantidad": 125.5,
                    "Precio": 450.75,
                    "TipoCifNifVendedor": 1,
                    "NIFVendedor": "12345678A",
                    "NombreVendedor": "Pescador Exemple",
                    "NIFComprador": "B12345678",
                    "IdTipoNifCifComprador": 1,
                    "NombreComprador": "Comprador SA"
                  }
                ]
              }
            }
          ]
        }
      }
    ]
  }
}
```

### Consultar estat d'un enviament

```bash
GET /api/sales-notes/envios/<num_envio>/
Authorization: Bearer <token>
```

### Llistar enviaments

```bash
GET /api/sales-notes/envios/?page=1&page_size=20
Authorization: Bearer <token>
```

## 🧪 Testing

### Executar tots els tests

```bash
make test
```

### Tests amb cobertura

```bash
make coverage
```

Això generarà un informe HTML a `htmlcov/index.html`

### Tests específics

```bash
# Tests unitaris
make test-unit

# Tests d'integració
make test-integration

# Tests de seguretat
make test-security
```

## 📊 Monitoratge i Logs

### Veure logs en temps real

```bash
make logs
# o només l'API:
make logs-api
```

### Logs d'auditoria

Tots els accessos i operacions crítiques es registren a:
- Base de dades: taules `api_access_log`, `audit_log`, `security_event`
- Fitxers: `/var/log/vcpe_api/api.log` i `/var/log/vcpe_api/security.log`

### Consultar logs d'auditoria

```python
from audit.models import AuditLog, SecurityEvent

# Últims 10 events de seguretat
SecurityEvent.objects.filter(severity='HIGH').order_by('-timestamp')[:10]

# Accions d'un usuari
AuditLog.objects.filter(user__username='usuari').order_by('-timestamp')
```

## 🔧 Configuració Avançada

### Variables d'entorn importants

| Variable | Descripció | Valor per defecte |
|----------|------------|-------------------|
| `DJANGO_SECRET_KEY` | Clau secreta Django | - (obligatori) |
| `DB_PASSWORD` | Contrasenya PostgreSQL | - (obligatori) |
| `JWT_SECRET_KEY` | Clau per JWT | - (obligatori) |
| `DJANGO_DEBUG` | Mode debug | `False` |
| `SECURE_SSL_REDIRECT` | Redirigir a HTTPS | `True` |
| `RATELIMIT_ENABLE` | Activar rate limiting | `True` |

### Rate Limiting

Per defecte:
- Usuaris anònims: 100 peticions/hora
- Usuaris autenticats: 1000 peticions/hora

Modificar a `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

## 🐛 Troubleshooting

### Error de connexió a la base de dades

```bash
# Comprovar que els contenidors estan actius
docker-compose ps

# Reiniciar la base de dades
docker-compose restart db

# Comprovar logs
make logs-db
```

### Errors de migració

```bash
# Esborrar migracions i tornar a crear
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
make makemigrations
make migrate
```

### Problemes amb pre-commit

```bash
# Reinstal·lar hooks
make pre-commit-install

# Executar manualment
make pre-commit-run
```

## 📚 Documentació Addicional

- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [Django Security](https://docs.djangoproject.com/en/5.1/topics/security/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [PostGIS Documentation](https://postgis.net/documentation/)

## 👥 Contribuir

1. Fork el projecte
2. Crea una branca per la teva feature (`git checkout -b feature/AmazingFeature`)
3. Commit els canvis (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branca (`git push origin feature/AmazingFeature`)
5. Obre un Pull Request

## 📄 Llicència

Aquest projecte és propietat d'ICATMAR. Tots els drets reservats.

## 📞 Contacte

- **Projecte**: TFM Ciberseguretat i Privadesa
- **Institució**: ICATMAR
- **Seguretat**: security@icatmar.cat
- **Web**: https://icatmar.cat

---

**Desenvolupat amb ❤️ seguint principis de Security by Design**
