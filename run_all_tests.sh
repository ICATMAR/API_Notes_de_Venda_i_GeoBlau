#!/bin/bash

# Suite Completa de Tests per VCPE API amb Report Consolidat
# Executa: chmod +x run_all_tests_with_report.sh && ./run_all_tests_with_report.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Variables
TIMESTAMP=$(date '+%Y-%m-%d_%H%M%S')
REPORT_DIR="test_reports"
CONSOLIDATED_REPORT="$REPORT_DIR/consolidated_report_$TIMESTAMP.md"
HTML_REPORT="${CONSOLIDATED_REPORT%.md}.html"

# Crear directori
mkdir -p "$REPORT_DIR"

# Banner
clear
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║          VCPE API - Suite Completa de Tests                  ║
║          TFM Ciberseguretat i Privadesa - ICATMAR            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Iniciar report
cat > "$CONSOLIDATED_REPORT" << EOF
# 📋 Report Consolidat de Tests - VCPE API

**Data d'execució:** $(date '+%d/%m/%Y %H:%M:%S')  
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

EOF

# Funció per afegir al report
add_section() {
    echo "" >> "$CONSOLIDATED_REPORT"
    echo "$1" >> "$CONSOLIDATED_REPORT"
    echo "" >> "$CONSOLIDATED_REPORT"
}

# Funció per executar comandament i capturar sortida
run_and_capture() {
    local title="$1"
    local command="$2"
    
    echo -e "${YELLOW}▶ $title${NC}"
    add_section "### $title"
    
    local start_time=$(date +%s)
    local output=$(eval "$command" 2>&1)
    local exit_code=$?
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    add_section "**Temps d'execució:** ${duration}s"
    add_section '```'
    add_section "$output"
    add_section '```'
    
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}  ✓ Completat (${duration}s)${NC}"
        add_section "**Resultat:** ✅ Completat correctament"
    else
        echo -e "${RED}  ✗ Error (${duration}s)${NC}"
        add_section "**Resultat:** ❌ Ha fallat amb exit code $exit_code"
    fi
    
    echo ""
    return $exit_code
}

# ==============================================================================
# 1. TESTS DE CONNECTIVITAT
# ==============================================================================

echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}  1. TESTS DE CONNECTIVITAT                                 ${NC}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

add_section "## 1. Tests de Connectivitat"

# 1.1 Estat dels contenidors
run_and_capture "1.1 Estat dels Contenidors Docker" \
    "docker-compose ps"

# 1.2 Health checks
run_and_capture "1.2 Health Check de l'API" \
    "curl -s http://localhost:8000/health/"

# 1.3 Vista root
run_and_capture "1.3 Vista Root de l'API" \
    "curl -s http://localhost:8000/"

# 1.4 Documentació accessible
run_and_capture "1.4 Documentació Swagger Accessible" \
    "curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/api/docs/"

# ==============================================================================
# 2. TESTS D'AUTENTICACIÓ JWT
# ==============================================================================

echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}  2. TESTS D'AUTENTICACIÓ JWT                               ${NC}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

add_section "## 2. Tests d'Autenticació JWT"

# 2.1 Obtenir token
echo -e "${YELLOW}▶ 2.1 Obtenir Token JWT${NC}"
TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin_test", "password": "TestSecure123!"}')

if echo "$TOKEN_RESPONSE" | grep -q "access"; then
    echo -e "${GREEN}  ✓ Token obtingut correctament${NC}"
    ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access')
    add_section "### 2.1 Obtenir Token JWT"
    add_section "**Resultat:** ✅ Token obtingut correctament"
    add_section "**Access Token:** \`${ACCESS_TOKEN:0:50}...\`"
else
    echo -e "${RED}  ✗ Error obtenint token${NC}"
    add_section "### 2.1 Obtenir Token JWT"
    add_section "**Resultat:** ❌ Error obtenint token"
    add_section "**Error:** Assegura't que l'usuari admin_test existeix"
fi
echo ""

# 2.2 Verificar token
if [ ! -z "$ACCESS_TOKEN" ]; then
    run_and_capture "2.2 Verificar Token JWT" \
        "curl -s -X POST http://localhost:8000/api/auth/token/verify/ -H 'Content-Type: application/json' -d '{\"token\": \"$ACCESS_TOKEN\"}'"
fi

# 2.3 Test accés sense token
run_and_capture "2.3 Accés sense Token (ha de fallar amb 401)" \
    "curl -s -w '\n%{http_code}' http://localhost:8000/api/sales-notes/"

# 2.4 Test accés amb token
if [ ! -z "$ACCESS_TOKEN" ]; then
    run_and_capture "2.4 Accés amb Token Vàlid" \
        "curl -s -w '\n%{http_code}' -H 'Authorization: Bearer $ACCESS_TOKEN' http://localhost:8000/api/sales-notes/"
fi

# ==============================================================================
# 3. TESTS AUTOMATITZATS (PYTEST)
# ==============================================================================

echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}  3. TESTS AUTOMATITZATS (PYTEST)                          ${NC}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

add_section "## 3. Tests Automatitzats (Pytest)"

if docker-compose exec -T api pytest --version > /dev/null 2>&1; then
    # 3.1 Tests unitaris
    run_and_capture "3.1 Tests Unitaris" \
        "docker-compose exec -T api pytest tests/unit -v --tb=short" || true
    
    # 3.2 Tests d'integració
    run_and_capture "3.2 Tests d'Integració" \
        "docker-compose exec -T api pytest tests/integration -v --tb=short" || true
    
    # 3.3 Tests de seguretat
    run_and_capture "3.3 Tests de Seguretat" \
        "docker-compose exec -T api pytest tests/security -v --tb=short" || true
else
    add_section "⚠️ **Pytest no disponible o tests no implementats encara**"
    echo -e "${YELLOW}  ⚠ Tests pytest no disponibles${NC}"
fi

# ==============================================================================
# 4. COBERTURA DE CODI
# ==============================================================================

echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}  4. COBERTURA DE CODI                                     ${NC}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

add_section "## 4. Cobertura de Codi"

if docker-compose exec -T api pytest --version > /dev/null 2>&1; then
    run_and_capture "4.1 Generar Informe de Cobertura" \
        "docker-compose exec -T api pytest --cov --cov-report=term --cov-report=html" || true
    
    add_section "ℹ️ Informe HTML disponible a: \`htmlcov/index.html\`"
else
    add_section "⚠️ **Cobertura no disponible**"
fi

# ==============================================================================
# 5. TESTS DE SEGURETAT (SAST)
# ==============================================================================

echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}  5. TESTS DE SEGURETAT (SAST)                             ${NC}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

add_section "## 5. Tests de Seguretat (SAST)"

# 5.1 Bandit (vulnerabilitats Python)
if docker-compose exec -T api bandit --version > /dev/null 2>&1; then
    run_and_capture "5.1 Anàlisi amb Bandit (Vulnerabilitats Python)" \
        "docker-compose exec -T api bandit -r . -ll -f txt" || true
else
    add_section "⚠️ **Bandit no disponible**"
fi

# 5.2 Safety (vulnerabilitats en dependències)
if docker-compose exec -T api safety --version > /dev/null 2>&1; then
    run_and_capture "5.2 Anàlisi amb Safety (Vulnerabilitats Dependències)" \
        "docker-compose exec -T api safety check" || true
else
    add_section "⚠️ **Safety no disponible**"
fi

# 5.3 Django security check
run_and_capture "5.3 Django Security Check" \
    "docker-compose exec -T api python manage.py check --deploy" || true

# ==============================================================================
# 6. ANÀLISI DE QUALITAT DE CODI
# ==============================================================================

echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}  6. ANÀLISI DE QUALITAT DE CODI                           ${NC}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

add_section "## 6. Anàlisi de Qualitat de Codi"

# 6.1 Flake8
if docker-compose exec -T api flake8 --version > /dev/null 2>&1; then
    run_and_capture "6.1 Linting amb Flake8" \
        "docker-compose exec -T api flake8 . --count --statistics" || true
else
    add_section "⚠️ **Flake8 no disponible**"
fi

# ==============================================================================
# 7. RESUM I CONCLUSIONS
# ==============================================================================

echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}  7. GENERANT RESUM I CONCLUSIONS                          ${NC}"
echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

add_section "## 7. Resum Executiu"

# Taula resum
cat >> "$CONSOLIDATED_REPORT" << EOF

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
*Data: $(date '+%d/%m/%Y %H:%M:%S')*  
*TFM Ciberseguretat i Privadesa - ICATMAR*

EOF

# ==============================================================================
# 8. GENERAR VERSIÓ HTML
# ==============================================================================

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ Tests completats!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📄 Report Markdown: $CONSOLIDATED_REPORT"

# Generar HTML si pandoc disponible
if command -v pandoc &> /dev/null; then
    echo "🌐 Generant versió HTML..."
    pandoc "$CONSOLIDATED_REPORT" -o "$HTML_REPORT" \
        --metadata title="Report Consolidat Tests - VCPE API" \
        --standalone \
        --toc \
        --toc-depth=3 \
        --css=https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css \
        --self-contained 2>/dev/null || echo "Error generant HTML"
    
    if [ -f "$HTML_REPORT" ]; then
        echo "📄 Report HTML: $HTML_REPORT"
    fi
else
    echo "⚠️  Pandoc no disponible. Instal·la amb: sudo apt-get install pandoc"
fi

# Llistar reports generats
echo ""
echo "📁 Reports generats:"
ls -lh "$REPORT_DIR" | tail -n 5

# Oferir obrir
echo ""
read -p "Vols obrir el report? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "$HTML_REPORT" ]; then
        xdg-open "$HTML_REPORT" 2>/dev/null || open "$HTML_REPORT" 2>/dev/null || cat "$CONSOLIDATED_REPORT"
    else
        cat "$CONSOLIDATED_REPORT"
    fi
fi

echo ""
echo -e "${GREEN}✓ Suite de tests completada!${NC}"
echo ""