FROM python:3.12-slim

# Metadata
LABEL maintainer="ICATMAR <info@icatmar.cat>"
LABEL description="VCPE API - Sistema segur de recepció notes de venda"

# Variables d'entorn per evitar fitxers .pyc i buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Directori de treball
WORKDIR /app

# Instal·lació de dependències del sistema per PostGIS
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    gdal-bin \
    libgdal-dev \
    gcc \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Actualització de pip i setuptools
RUN pip install --upgrade pip setuptools wheel

# Còpia i instal·lació de dependències Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Còpia del codi de l'aplicació
COPY . /app/

# Creació d'usuari no-root per seguretat
RUN useradd -m -u 1000 vcpe_user && \
    mkdir -p /app/staticfiles /app/mediafiles /app/logs && \
    chown -R vcpe_user:vcpe_user /app

# Canvi a usuari no-root
USER vcpe_user

# Port d'exposició
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/', timeout=5)"

# Script d'inici per defecte (pot ser sobreescrit)
CMD ["gunicorn", "vcpe_api.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
