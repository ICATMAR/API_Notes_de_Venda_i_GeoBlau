#!/bin/bash

# Tests d'Autenticació JWT per VCPE API amb Report
# Per executar: chmod +x test_auth_with_report.sh && ./test_auth_with_report.sh

set -e

# Colors per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables globals per report
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
REPORT_DIR="test_reports"
REPORT_FILE="$REPORT_DIR/auth_test_report_$(date '+%Y%m%d_%H%M%S').md"
HTML_REPORT="${REPORT_FILE%.md}.html"
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Crear directori de reports si no existeix
mkdir -p "$REPORT_DIR"

# Funció per afegir al report
add_to_report() {
    echo "$1" >> "$REPORT_FILE"
}

# Funció per executar test i registrar resultat
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected="$3"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Test $TOTAL_TESTS: $test_name${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

    add_to_report ""
    add_to_report "### Test $TOTAL_TESTS: $test_name"
    add_to_report ""
    add_to_report "**Hora d'execució:** $(date '+%H:%M:%S')"
    add_to_report ""

    # Executar el test i capturar resultat
    local start_time=$(date +%s%N)
    local result=$(eval "$test_command" 2>&1)
    local exit_code=$?
    local end_time=$(date +%s%N)
    local duration=$(( (end_time - start_time) / 1000000 ))

    # Mostrar resultat
    echo "Temps d'execució: ${duration}ms"
    echo ""
    echo "Resultat:"
    echo "$result"
    echo ""

    add_to_report "**Temps d'execució:** ${duration}ms"
    add_to_report ""
    add_to_report "**Comanda executada:**"
    add_to_report '```bash'
    add_to_report "$test_command"
    add_to_report '```'
    add_to_report ""

    # Verificar si el test ha passat
    if echo "$result" | grep -q "$expected"; then
        echo -e "${GREEN}✓ PASS${NC}"
        add_to_report "**Resultat:** ✅ **PASS**"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAIL${NC}"
        add_to_report "**Resultat:** ❌ **FAIL**"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi

    add_to_report ""
    add_to_report "<details>"
    add_to_report "<summary>Resposta completa (clica per veure)</summary>"
    add_to_report ""
    add_to_report '```json'
    add_to_report "$result"
    add_to_report '```'
    add_to_report ""
    add_to_report "</details>"
    add_to_report ""
    add_to_report "---"

    return $exit_code
}

# Iniciar report
echo "================================================"
echo "VCPE API - Suite de Tests d'Autenticació JWT"
echo "================================================"
echo "Data: $TIMESTAMP"
echo ""

add_to_report "# Report de Tests d'Autenticació JWT - VCPE API"
add_to_report ""
add_to_report "**Data d'execució:** $TIMESTAMP"
add_to_report ""
add_to_report "**Projecte:** API d'ingesta de dades d'ICATMAR"
add_to_report ""
add_to_report "---"
add_to_report ""

# Test 1: Health Check
run_test "Health Check de l'API" \
    "curl -s http://localhost:8000/health/" \
    "healthy"

# Test 2: Vista Root
run_test "Vista Root de l'API" \
    "curl -s http://localhost:8000/" \
    "vcpe-api"

# Test 3: Obtenir Token JWT
echo -e "${YELLOW}Nota: Assegura't que l'usuari admin_test existeix (make createsuperuser)${NC}"

TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin_test",
    "password": "admin"
  }')

run_test "Obtenir Token JWT amb credencials vàlides" \
    "echo '$TOKEN_RESPONSE'" \
    "access"

if echo "$TOKEN_RESPONSE" | grep -q "access"; then
    ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access' 2>/dev/null || echo "")
    REFRESH_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.refresh' 2>/dev/null || echo "")

    # Guardar tokens
    echo "export ACCESS_TOKEN='$ACCESS_TOKEN'" > .tokens
    echo "export REFRESH_TOKEN='$REFRESH_TOKEN'" >> .tokens

    add_to_report ""
    add_to_report "**Tokens obtinguts:**"
    add_to_report "- Access Token: \`${ACCESS_TOKEN:0:50}...\`"
    add_to_report "- Refresh Token: \`${REFRESH_TOKEN:0:50}...\`"
    add_to_report ""

    # Test 4: Verificar Token
    run_test "Verificar Token JWT vàlid" \
        "curl -s -X POST http://localhost:8000/api/auth/token/verify/ -H 'Content-Type: application/json' -d '{\"token\": \"$ACCESS_TOKEN\"}'" \
        ""

    # Test 5: Refrescar Token
    run_test "Refrescar Token JWT" \
        "curl -s -X POST http://localhost:8000/api/auth/token/refresh/ -H 'Content-Type: application/json' -d '{\"refresh\": \"$REFRESH_TOKEN\"}'" \
        "access"

    # Test 6: Accés sense token (ha de fallar)
    run_test "Accés a endpoint protegit sense token (ha de retornar 401)" \
        "curl -s -w '\n%{http_code}' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "401"

    # Test 7: Accés amb token vàlid
    run_test "Accés a endpoint protegit amb token vàlid" \
        "curl -s -w '\n%{http_code}' -H 'Authorization: Bearer $ACCESS_TOKEN' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "200\|404"

    # Test 8: Token manipulat (ha de fallar)
    FAKE_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"

    run_test "Token JWT manipulat (ha de retornar 401)" \
        "curl -s -w '\n%{http_code}' -H 'Authorization: Bearer $FAKE_TOKEN' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "401"
else
    echo -e "${RED}No s'han pogut obtenir els tokens. Els següents tests es saltaran.${NC}"
    add_to_report ""
    add_to_report "⚠️ **Error:** No s'han pogut obtenir els tokens JWT. Tests posteriors saltats."
    add_to_report ""
fi

# Test 9: Credencials invàlides
run_test "Login amb credencials invàlides (ha de retornar 401)" \
    "curl -s -w '\n%{http_code}' -X POST http://localhost:8000/api/auth/token/ -H 'Content-Type: application/json' -d '{\"username\": \"usuari_inexistent\", \"password\": \"PasswordIncorrecte\"}' | tail -n 1" \
    "401"

# Test 10: Documentació API accessible
run_test "Documentació Swagger accessible" \
    "curl -s -w '\n%{http_code}' http://localhost:8000/api/docs/ | tail -n 1" \
    "200"

# Resum Final
echo ""
echo "================================================"
echo -e "${GREEN}RESUM DELS TESTS${NC}"
echo "================================================"
echo "Total de tests executats: $TOTAL_TESTS"
echo -e "${GREEN}Tests passats: $PASSED_TESTS${NC}"
echo -e "${RED}Tests fallats: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ Tots els tests han passat correctament!${NC}"
    FINAL_STATUS="success"
else
    echo -e "${RED}✗ Hi ha tests que han fallat. Revisa el report.${NC}"
    FINAL_STATUS="failure"
fi

echo ""
echo "Report generat a: $REPORT_FILE"
echo "================================================"

# Afegir resum al report
add_to_report ""
add_to_report "## 📊 Resum d'Execució"
add_to_report ""
add_to_report "| Mètrica | Valor |"
add_to_report "|---------|-------|"
add_to_report "| **Total Tests** | $TOTAL_TESTS |"
add_to_report "| **Tests Passats** | ✅ $PASSED_TESTS |"
add_to_report "| **Tests Fallats** | ❌ $FAILED_TESTS |"
add_to_report "| **Taxa d'Èxit** | $(( PASSED_TESTS * 100 / TOTAL_TESTS ))% |"
add_to_report ""

if [ "$FINAL_STATUS" == "success" ]; then
    add_to_report "### ✅ Resultat Final: ÈXIT"
    add_to_report ""
    add_to_report "Tots els tests d'autenticació han passat correctament."
else
    add_to_report "### ❌ Resultat Final: FALLAT"
    add_to_report ""
    add_to_report "Hi ha tests que han fallat. Revisa els detalls anteriors."
fi

add_to_report ""
add_to_report "---"
add_to_report ""
add_to_report "## 📝 Següents Passos"
add_to_report ""
add_to_report "1. **Tests Automatitzats**: Implementar tests amb pytest"
add_to_report "2. **Tests de Seguretat**: Executar suite OWASP"
add_to_report "3. **Tests de Performance**: Load testing amb Locust"
add_to_report ""
add_to_report "---"
add_to_report ""
add_to_report "*Report generat automàticament per test_auth_with_report.sh*"
add_to_report ""
add_to_report "*API d'ingesta de dades d'ICATMAR - $(date '+%Y')*"

# Generar versió HTML del report
echo ""
echo "Generant versió HTML del report..."

if command -v pandoc &> /dev/null; then
    pandoc "$REPORT_FILE" -o "$HTML_REPORT" \
        --metadata title="Report Tests JWT - VCPE API" \
        --standalone \
        --css=https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css \
        --self-contained
    echo "Report HTML generat a: $HTML_REPORT"
else
    echo "pandoc no està instal·lat. Report HTML no generat."
    echo "Per instal·lar: sudo apt-get install pandoc"
fi

# Mostrar fitxers generats
echo ""
echo "Fitxers generats:"
ls -lh "$REPORT_DIR"/*.md "$REPORT_DIR"/*.html 2>/dev/null | tail -n 2

# Oferir obrir el report
echo ""
read -p "Vols obrir el report? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "$HTML_REPORT" ]; then
        xdg-open "$HTML_REPORT" 2>/dev/null || open "$HTML_REPORT" 2>/dev/null || echo "No s'ha pogut obrir automàticament. Obre manualment: $HTML_REPORT"
    else
        cat "$REPORT_FILE"
    fi
fi

# Exit code segons resultat
if [ "$FINAL_STATUS" == "success" ]; then
    exit 0
else
    exit 1
fi#!/bin/bash

# Tests d'Autenticació JWT per VCPE API amb Report
# Per executar: chmod +x test_auth_with_report.sh && ./test_auth_with_report.sh

set -e

# Colors per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables globals per report
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
REPORT_DIR="test_reports"
REPORT_FILE="$REPORT_DIR/auth_test_report_$(date '+%Y%m%d_%H%M%S').md"
HTML_REPORT="${REPORT_FILE%.md}.html"
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Crear directori de reports si no existeix
mkdir -p "$REPORT_DIR"

# Funció per afegir al report
add_to_report() {
    echo "$1" >> "$REPORT_FILE"
}

# Funció per executar test i registrar resultat
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected="$3"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Test $TOTAL_TESTS: $test_name${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

    add_to_report ""
    add_to_report "### Test $TOTAL_TESTS: $test_name"
    add_to_report ""
    add_to_report "**Hora d'execució:** $(date '+%H:%M:%S')"
    add_to_report ""

    # Executar el test i capturar resultat
    local start_time=$(date +%s%N)
    local result=$(eval "$test_command" 2>&1)
    local exit_code=$?
    local end_time=$(date +%s%N)
    local duration=$(( (end_time - start_time) / 1000000 ))

    # Mostrar resultat
    echo "Temps d'execució: ${duration}ms"
    echo ""
    echo "Resultat:"
    echo "$result"
    echo ""

    add_to_report "**Temps d'execució:** ${duration}ms"
    add_to_report ""
    add_to_report "**Comanda executada:**"
    add_to_report '```bash'
    add_to_report "$test_command"
    add_to_report '```'
    add_to_report ""

    # Verificar si el test ha passat
    if echo "$result" | grep -q "$expected"; then
        echo -e "${GREEN}✓ PASS${NC}"
        add_to_report "**Resultat:** ✅ **PASS**"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAIL${NC}"
        add_to_report "**Resultat:** ❌ **FAIL**"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi

    add_to_report ""
    add_to_report "<details>"
    add_to_report "<summary>Resposta completa (clica per veure)</summary>"
    add_to_report ""
    add_to_report '```json'
    add_to_report "$result"
    add_to_report '```'
    add_to_report ""
    add_to_report "</details>"
    add_to_report ""
    add_to_report "---"

    return $exit_code
}

# Iniciar report
echo "================================================"
echo "VCPE API - Suite de Tests d'Autenticació JWT"
echo "================================================"
echo "Data: $TIMESTAMP"
echo ""

add_to_report "# Report de Tests d'Autenticació JWT - VCPE API"
add_to_report ""
add_to_report "**Data d'execució:** $TIMESTAMP"
add_to_report ""
add_to_report "**Projecte:** API d'ingesta de dades d'ICATMAR"
add_to_report ""
add_to_report "---"
add_to_report ""

# Test 1: Health Check
run_test "Health Check de l'API" \
    "curl -s http://localhost:8000/health/" \
    "healthy"

# Test 2: Vista Root
run_test "Vista Root de l'API" \
    "curl -s http://localhost:8000/" \
    "vcpe-api"

# Test 3: Obtenir Token JWT
echo -e "${YELLOW}Nota: Assegura't que l'usuari admin_test existeix (make createsuperuser)${NC}"

TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin_test",
    "password": "admin"
  }')

run_test "Obtenir Token JWT amb credencials vàlides" \
    "echo '$TOKEN_RESPONSE'" \
    "access"

if echo "$TOKEN_RESPONSE" | grep -q "access"; then
    ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access' 2>/dev/null || echo "")
    REFRESH_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.refresh' 2>/dev/null || echo "")

    # Guardar tokens
    echo "export ACCESS_TOKEN='$ACCESS_TOKEN'" > .tokens
    echo "export REFRESH_TOKEN='$REFRESH_TOKEN'" >> .tokens

    add_to_report ""
    add_to_report "**Tokens obtinguts:**"
    add_to_report "- Access Token: \`${ACCESS_TOKEN:0:50}...\`"
    add_to_report "- Refresh Token: \`${REFRESH_TOKEN:0:50}...\`"
    add_to_report ""

    # Test 4: Verificar Token
    run_test "Verificar Token JWT vàlid" \
        "curl -s -X POST http://localhost:8000/api/auth/token/verify/ -H 'Content-Type: application/json' -d '{\"token\": \"$ACCESS_TOKEN\"}'" \
        ""

    # Test 5: Refrescar Token
    run_test "Refrescar Token JWT" \
        "curl -s -X POST http://localhost:8000/api/auth/token/refresh/ -H 'Content-Type: application/json' -d '{\"refresh\": \"$REFRESH_TOKEN\"}'" \
        "access"

    # Test 6: Accés sense token (ha de fallar)
    run_test "Accés a endpoint protegit sense token (ha de retornar 401)" \
        "curl -s -w '\n%{http_code}' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "401"

    # Test 7: Accés amb token vàlid
    run_test "Accés a endpoint protegit amb token vàlid" \
        "curl -s -w '\n%{http_code}' -H 'Authorization: Bearer $ACCESS_TOKEN' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "200\|404"

    # Test 8: Token manipulat (ha de fallar)
    FAKE_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"

    run_test "Token JWT manipulat (ha de retornar 401)" \
        "curl -s -w '\n%{http_code}' -H 'Authorization: Bearer $FAKE_TOKEN' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "401"
else
    echo -e "${RED}No s'han pogut obtenir els tokens. Els següents tests es saltaran.${NC}"
    add_to_report ""
    add_to_report "⚠️ **Error:** No s'han pogut obtenir els tokens JWT. Tests posteriors saltats."
    add_to_report ""
fi

# Test 9: Credencials invàlides
run_test "Login amb credencials invàlides (ha de retornar 401)" \
    "curl -s -w '\n%{http_code}' -X POST http://localhost:8000/api/auth/token/ -H 'Content-Type: application/json' -d '{\"username\": \"usuari_inexistent\", \"password\": \"PasswordIncorrecte\"}' | tail -n 1" \
    "401"

# Test 10: Documentació API accessible
run_test "Documentació Swagger accessible" \
    "curl -s -w '\n%{http_code}' http://localhost:8000/api/docs/ | tail -n 1" \
    "200"

# Resum Final
echo ""
echo "================================================"
echo -e "${GREEN}RESUM DELS TESTS${NC}"
echo "================================================"
echo "Total de tests executats: $TOTAL_TESTS"
echo -e "${GREEN}Tests passats: $PASSED_TESTS${NC}"
echo -e "${RED}Tests fallats: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ Tots els tests han passat correctament!${NC}"
    FINAL_STATUS="success"
else
    echo -e "${RED}✗ Hi ha tests que han fallat. Revisa el report.${NC}"
    FINAL_STATUS="failure"
fi

echo ""
echo "Report generat a: $REPORT_FILE"
echo "================================================"

# Afegir resum al report
add_to_report ""
add_to_report "## 📊 Resum d'Execució"
add_to_report ""
add_to_report "| Mètrica | Valor |"
add_to_report "|---------|-------|"
add_to_report "| **Total Tests** | $TOTAL_TESTS |"
add_to_report "| **Tests Passats** | ✅ $PASSED_TESTS |"
add_to_report "| **Tests Fallats** | ❌ $FAILED_TESTS |"
add_to_report "| **Taxa d'Èxit** | $(( PASSED_TESTS * 100 / TOTAL_TESTS ))% |"
add_to_report ""

if [ "$FINAL_STATUS" == "success" ]; then
    add_to_report "### ✅ Resultat Final: ÈXIT"
    add_to_report ""
    add_to_report "Tots els tests d'autenticació han passat correctament."
else
    add_to_report "### ❌ Resultat Final: FALLAT"
    add_to_report ""
    add_to_report "Hi ha tests que han fallat. Revisa els detalls anteriors."
fi

add_to_report ""
add_to_report "---"
add_to_report ""
add_to_report "## 📝 Següents Passos"
add_to_report ""
add_to_report "1. **Tests Automatitzats**: Implementar tests amb pytest"
add_to_report "2. **Tests de Seguretat**: Executar suite OWASP"
add_to_report "3. **Tests de Performance**: Load testing amb Locust"
add_to_report ""
add_to_report "---"
add_to_report ""
add_to_report "*Report generat automàticament per test_auth_with_report.sh*"
add_to_report ""
add_to_report "*API d'ingesta de dades d'ICATMAR - $(date '+%Y')*"

# Generar versió HTML del report
echo ""
echo "Generant versió HTML del report..."

if command -v pandoc &> /dev/null; then
    pandoc "$REPORT_FILE" -o "$HTML_REPORT" \
        --metadata title="Report Tests JWT - VCPE API" \
        --standalone \
        --css=https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css \
        --self-contained
    echo "Report HTML generat a: $HTML_REPORT"
else
    echo "pandoc no està instal·lat. Report HTML no generat."
    echo "Per instal·lar: sudo apt-get install pandoc"
fi

# Mostrar fitxers generats
echo ""
echo "Fitxers generats:"
ls -lh "$REPORT_DIR"/*.md "$REPORT_DIR"/*.html 2>/dev/null | tail -n 2

# Oferir obrir el report
echo ""
read -p "Vols obrir el report? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "$HTML_REPORT" ]; then
        xdg-open "$HTML_REPORT" 2>/dev/null || open "$HTML_REPORT" 2>/dev/null || echo "No s'ha pogut obrir automàticament. Obre manualment: $HTML_REPORT"
    else
        cat "$REPORT_FILE"
    fi
fi

# Exit code segons resultat
if [ "$FINAL_STATUS" == "success" ]; then
    exit 0
else
    exit 1
fi#!/bin/bash

# Tests d'Autenticació JWT per VCPE API amb Report
# Per executar: chmod +x test_auth_with_report.sh && ./test_auth_with_report.sh

set -e

# Colors per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables globals per report
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
REPORT_DIR="test_reports"
REPORT_FILE="$REPORT_DIR/auth_test_report_$(date '+%Y%m%d_%H%M%S').md"
HTML_REPORT="${REPORT_FILE%.md}.html"
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Crear directori de reports si no existeix
mkdir -p "$REPORT_DIR"

# Funció per afegir al report
add_to_report() {
    echo "$1" >> "$REPORT_FILE"
}

# Funció per executar test i registrar resultat
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected="$3"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Test $TOTAL_TESTS: $test_name${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

    add_to_report ""
    add_to_report "### Test $TOTAL_TESTS: $test_name"
    add_to_report ""
    add_to_report "**Hora d'execució:** $(date '+%H:%M:%S')"
    add_to_report ""

    # Executar el test i capturar resultat
    local start_time=$(date +%s%N)
    local result=$(eval "$test_command" 2>&1)
    local exit_code=$?
    local end_time=$(date +%s%N)
    local duration=$(( (end_time - start_time) / 1000000 ))

    # Mostrar resultat
    echo "Temps d'execució: ${duration}ms"
    echo ""
    echo "Resultat:"
    echo "$result"
    echo ""

    add_to_report "**Temps d'execució:** ${duration}ms"
    add_to_report ""
    add_to_report "**Comanda executada:**"
    add_to_report '```bash'
    add_to_report "$test_command"
    add_to_report '```'
    add_to_report ""

    # Verificar si el test ha passat
    if echo "$result" | grep -q "$expected"; then
        echo -e "${GREEN}✓ PASS${NC}"
        add_to_report "**Resultat:** ✅ **PASS**"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAIL${NC}"
        add_to_report "**Resultat:** ❌ **FAIL**"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi

    add_to_report ""
    add_to_report "<details>"
    add_to_report "<summary>Resposta completa (clica per veure)</summary>"
    add_to_report ""
    add_to_report '```json'
    add_to_report "$result"
    add_to_report '```'
    add_to_report ""
    add_to_report "</details>"
    add_to_report ""
    add_to_report "---"

    return $exit_code
}

# Iniciar report
echo "================================================"
echo "VCPE API - Suite de Tests d'Autenticació JWT"
echo "================================================"
echo "Data: $TIMESTAMP"
echo ""

add_to_report "# Report de Tests d'Autenticació JWT - VCPE API"
add_to_report ""
add_to_report "**Data d'execució:** $TIMESTAMP"
add_to_report ""
add_to_report "**Projecte:** API d'ingesta de dades d'ICATMAR"
add_to_report ""
add_to_report "---"
add_to_report ""

# Test 1: Health Check
run_test "Health Check de l'API" \
    "curl -s http://localhost:8000/health/" \
    "healthy"

# Test 2: Vista Root
run_test "Vista Root de l'API" \
    "curl -s http://localhost:8000/" \
    "vcpe-api"

# Test 3: Obtenir Token JWT
echo -e "${YELLOW}Nota: Assegura't que l'usuari admin_test existeix (make createsuperuser)${NC}"

TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin_test",
    "password": "admin"
  }')

run_test "Obtenir Token JWT amb credencials vàlides" \
    "echo '$TOKEN_RESPONSE'" \
    "access"

if echo "$TOKEN_RESPONSE" | grep -q "access"; then
    ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access' 2>/dev/null || echo "")
    REFRESH_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.refresh' 2>/dev/null || echo "")

    # Guardar tokens
    echo "export ACCESS_TOKEN='$ACCESS_TOKEN'" > .tokens
    echo "export REFRESH_TOKEN='$REFRESH_TOKEN'" >> .tokens

    add_to_report ""
    add_to_report "**Tokens obtinguts:**"
    add_to_report "- Access Token: \`${ACCESS_TOKEN:0:50}...\`"
    add_to_report "- Refresh Token: \`${REFRESH_TOKEN:0:50}...\`"
    add_to_report ""

    # Test 4: Verificar Token
    run_test "Verificar Token JWT vàlid" \
        "curl -s -X POST http://localhost:8000/api/auth/token/verify/ -H 'Content-Type: application/json' -d '{\"token\": \"$ACCESS_TOKEN\"}'" \
        ""

    # Test 5: Refrescar Token
    run_test "Refrescar Token JWT" \
        "curl -s -X POST http://localhost:8000/api/auth/token/refresh/ -H 'Content-Type: application/json' -d '{\"refresh\": \"$REFRESH_TOKEN\"}'" \
        "access"

    # Test 6: Accés sense token (ha de fallar)
    run_test "Accés a endpoint protegit sense token (ha de retornar 401)" \
        "curl -s -w '\n%{http_code}' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "401"

    # Test 7: Accés amb token vàlid
    run_test "Accés a endpoint protegit amb token vàlid" \
        "curl -s -w '\n%{http_code}' -H 'Authorization: Bearer $ACCESS_TOKEN' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "200\|404"

    # Test 8: Token manipulat (ha de fallar)
    FAKE_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"

    run_test "Token JWT manipulat (ha de retornar 401)" \
        "curl -s -w '\n%{http_code}' -H 'Authorization: Bearer $FAKE_TOKEN' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "401"
else
    echo -e "${RED}No s'han pogut obtenir els tokens. Els següents tests es saltaran.${NC}"
    add_to_report ""
    add_to_report "⚠️ **Error:** No s'han pogut obtenir els tokens JWT. Tests posteriors saltats."
    add_to_report ""
fi

# Test 9: Credencials invàlides
run_test "Login amb credencials invàlides (ha de retornar 401)" \
    "curl -s -w '\n%{http_code}' -X POST http://localhost:8000/api/auth/token/ -H 'Content-Type: application/json' -d '{\"username\": \"usuari_inexistent\", \"password\": \"PasswordIncorrecte\"}' | tail -n 1" \
    "401"

# Test 10: Documentació API accessible
run_test "Documentació Swagger accessible" \
    "curl -s -w '\n%{http_code}' http://localhost:8000/api/docs/ | tail -n 1" \
    "200"

# Resum Final
echo ""
echo "================================================"
echo -e "${GREEN}RESUM DELS TESTS${NC}"
echo "================================================"
echo "Total de tests executats: $TOTAL_TESTS"
echo -e "${GREEN}Tests passats: $PASSED_TESTS${NC}"
echo -e "${RED}Tests fallats: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ Tots els tests han passat correctament!${NC}"
    FINAL_STATUS="success"
else
    echo -e "${RED}✗ Hi ha tests que han fallat. Revisa el report.${NC}"
    FINAL_STATUS="failure"
fi

echo ""
echo "Report generat a: $REPORT_FILE"
echo "================================================"

# Afegir resum al report
add_to_report ""
add_to_report "## 📊 Resum d'Execució"
add_to_report ""
add_to_report "| Mètrica | Valor |"
add_to_report "|---------|-------|"
add_to_report "| **Total Tests** | $TOTAL_TESTS |"
add_to_report "| **Tests Passats** | ✅ $PASSED_TESTS |"
add_to_report "| **Tests Fallats** | ❌ $FAILED_TESTS |"
add_to_report "| **Taxa d'Èxit** | $(( PASSED_TESTS * 100 / TOTAL_TESTS ))% |"
add_to_report ""

if [ "$FINAL_STATUS" == "success" ]; then
    add_to_report "### ✅ Resultat Final: ÈXIT"
    add_to_report ""
    add_to_report "Tots els tests d'autenticació han passat correctament."
else
    add_to_report "### ❌ Resultat Final: FALLAT"
    add_to_report ""
    add_to_report "Hi ha tests que han fallat. Revisa els detalls anteriors."
fi

add_to_report ""
add_to_report "---"
add_to_report ""
add_to_report "## 📝 Següents Passos"
add_to_report ""
add_to_report "1. **Tests Automatitzats**: Implementar tests amb pytest"
add_to_report "2. **Tests de Seguretat**: Executar suite OWASP"
add_to_report "3. **Tests de Performance**: Load testing amb Locust"
add_to_report ""
add_to_report "---"
add_to_report ""
add_to_report "*Report generat automàticament per test_auth_with_report.sh*"
add_to_report ""
add_to_report "*API d'ingesta de dades d'ICATMAR - $(date '+%Y')*"

# Generar versió HTML del report
echo ""
echo "Generant versió HTML del report..."

if command -v pandoc &> /dev/null; then
    pandoc "$REPORT_FILE" -o "$HTML_REPORT" \
        --metadata title="Report Tests JWT - VCPE API" \
        --standalone \
        --css=https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css \
        --self-contained
    echo "Report HTML generat a: $HTML_REPORT"
else
    echo "pandoc no està instal·lat. Report HTML no generat."
    echo "Per instal·lar: sudo apt-get install pandoc"
fi

# Mostrar fitxers generats
echo ""
echo "Fitxers generats:"
ls -lh "$REPORT_DIR"/*.md "$REPORT_DIR"/*.html 2>/dev/null | tail -n 2

# Oferir obrir el report
echo ""
read -p "Vols obrir el report? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "$HTML_REPORT" ]; then
        xdg-open "$HTML_REPORT" 2>/dev/null || open "$HTML_REPORT" 2>/dev/null || echo "No s'ha pogut obrir automàticament. Obre manualment: $HTML_REPORT"
    else
        cat "$REPORT_FILE"
    fi
fi

# Exit code segons resultat
if [ "$FINAL_STATUS" == "success" ]; then
    exit 0
else
    exit 1
fi#!/bin/bash

# Tests d'Autenticació JWT per VCPE API amb Report
# Per executar: chmod +x test_auth_with_report.sh && ./test_auth_with_report.sh

set -e

# Colors per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables globals per report
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
REPORT_DIR="test_reports"
REPORT_FILE="$REPORT_DIR/auth_test_report_$(date '+%Y%m%d_%H%M%S').md"
HTML_REPORT="${REPORT_FILE%.md}.html"
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Crear directori de reports si no existeix
mkdir -p "$REPORT_DIR"

# Funció per afegir al report
add_to_report() {
    echo "$1" >> "$REPORT_FILE"
}

# Funció per executar test i registrar resultat
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected="$3"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Test $TOTAL_TESTS: $test_name${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

    add_to_report ""
    add_to_report "### Test $TOTAL_TESTS: $test_name"
    add_to_report ""
    add_to_report "**Hora d'execució:** $(date '+%H:%M:%S')"
    add_to_report ""

    # Executar el test i capturar resultat
    local start_time=$(date +%s%N)
    local result=$(eval "$test_command" 2>&1)
    local exit_code=$?
    local end_time=$(date +%s%N)
    local duration=$(( (end_time - start_time) / 1000000 ))

    # Mostrar resultat
    echo "Temps d'execució: ${duration}ms"
    echo ""
    echo "Resultat:"
    echo "$result"
    echo ""

    add_to_report "**Temps d'execució:** ${duration}ms"
    add_to_report ""
    add_to_report "**Comanda executada:**"
    add_to_report '```bash'
    add_to_report "$test_command"
    add_to_report '```'
    add_to_report ""

    # Verificar si el test ha passat
    if echo "$result" | grep -q "$expected"; then
        echo -e "${GREEN}✓ PASS${NC}"
        add_to_report "**Resultat:** ✅ **PASS**"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAIL${NC}"
        add_to_report "**Resultat:** ❌ **FAIL**"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi

    add_to_report ""
    add_to_report "<details>"
    add_to_report "<summary>Resposta completa (clica per veure)</summary>"
    add_to_report ""
    add_to_report '```json'
    add_to_report "$result"
    add_to_report '```'
    add_to_report ""
    add_to_report "</details>"
    add_to_report ""
    add_to_report "---"

    return $exit_code
}

# Iniciar report
echo "================================================"
echo "VCPE API - Suite de Tests d'Autenticació JWT"
echo "================================================"
echo "Data: $TIMESTAMP"
echo ""

add_to_report "# Report de Tests d'Autenticació JWT - VCPE API"
add_to_report ""
add_to_report "**Data d'execució:** $TIMESTAMP"
add_to_report ""
add_to_report "**Projecte:** API d'ingesta de dades d'ICATMAR"
add_to_report ""
add_to_report "---"
add_to_report ""

# Test 1: Health Check
run_test "Health Check de l'API" \
    "curl -s http://localhost:8000/health/" \
    "healthy"

# Test 2: Vista Root
run_test "Vista Root de l'API" \
    "curl -s http://localhost:8000/" \
    "vcpe-api"

# Test 3: Obtenir Token JWT
echo -e "${YELLOW}Nota: Assegura't que l'usuari admin_test existeix (make createsuperuser)${NC}"

TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin_test",
    "password": "admin"
  }')

run_test "Obtenir Token JWT amb credencials vàlides" \
    "echo '$TOKEN_RESPONSE'" \
    "access"

if echo "$TOKEN_RESPONSE" | grep -q "access"; then
    ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access' 2>/dev/null || echo "")
    REFRESH_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.refresh' 2>/dev/null || echo "")

    # Guardar tokens
    echo "export ACCESS_TOKEN='$ACCESS_TOKEN'" > .tokens
    echo "export REFRESH_TOKEN='$REFRESH_TOKEN'" >> .tokens

    add_to_report ""
    add_to_report "**Tokens obtinguts:**"
    add_to_report "- Access Token: \`${ACCESS_TOKEN:0:50}...\`"
    add_to_report "- Refresh Token: \`${REFRESH_TOKEN:0:50}...\`"
    add_to_report ""

    # Test 4: Verificar Token
    run_test "Verificar Token JWT vàlid" \
        "curl -s -X POST http://localhost:8000/api/auth/token/verify/ -H 'Content-Type: application/json' -d '{\"token\": \"$ACCESS_TOKEN\"}'" \
        ""

    # Test 5: Refrescar Token
    run_test "Refrescar Token JWT" \
        "curl -s -X POST http://localhost:8000/api/auth/token/refresh/ -H 'Content-Type: application/json' -d '{\"refresh\": \"$REFRESH_TOKEN\"}'" \
        "access"

    # Test 6: Accés sense token (ha de fallar)
    run_test "Accés a endpoint protegit sense token (ha de retornar 401)" \
        "curl -s -w '\n%{http_code}' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "401"

    # Test 7: Accés amb token vàlid
    run_test "Accés a endpoint protegit amb token vàlid" \
        "curl -s -w '\n%{http_code}' -H 'Authorization: Bearer $ACCESS_TOKEN' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "200\|404"

    # Test 8: Token manipulat (ha de fallar)
    FAKE_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"

    run_test "Token JWT manipulat (ha de retornar 401)" \
        "curl -s -w '\n%{http_code}' -H 'Authorization: Bearer $FAKE_TOKEN' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "401"
else
    echo -e "${RED}No s'han pogut obtenir els tokens. Els següents tests es saltaran.${NC}"
    add_to_report ""
    add_to_report "⚠️ **Error:** No s'han pogut obtenir els tokens JWT. Tests posteriors saltats."
    add_to_report ""
fi

# Test 9: Credencials invàlides
run_test "Login amb credencials invàlides (ha de retornar 401)" \
    "curl -s -w '\n%{http_code}' -X POST http://localhost:8000/api/auth/token/ -H 'Content-Type: application/json' -d '{\"username\": \"usuari_inexistent\", \"password\": \"PasswordIncorrecte\"}' | tail -n 1" \
    "401"

# Test 10: Documentació API accessible
run_test "Documentació Swagger accessible" \
    "curl -s -w '\n%{http_code}' http://localhost:8000/api/docs/ | tail -n 1" \
    "200"

# Resum Final
echo ""
echo "================================================"
echo -e "${GREEN}RESUM DELS TESTS${NC}"
echo "================================================"
echo "Total de tests executats: $TOTAL_TESTS"
echo -e "${GREEN}Tests passats: $PASSED_TESTS${NC}"
echo -e "${RED}Tests fallats: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ Tots els tests han passat correctament!${NC}"
    FINAL_STATUS="success"
else
    echo -e "${RED}✗ Hi ha tests que han fallat. Revisa el report.${NC}"
    FINAL_STATUS="failure"
fi

echo ""
echo "Report generat a: $REPORT_FILE"
echo "================================================"

# Afegir resum al report
add_to_report ""
add_to_report "## 📊 Resum d'Execució"
add_to_report ""
add_to_report "| Mètrica | Valor |"
add_to_report "|---------|-------|"
add_to_report "| **Total Tests** | $TOTAL_TESTS |"
add_to_report "| **Tests Passats** | ✅ $PASSED_TESTS |"
add_to_report "| **Tests Fallats** | ❌ $FAILED_TESTS |"
add_to_report "| **Taxa d'Èxit** | $(( PASSED_TESTS * 100 / TOTAL_TESTS ))% |"
add_to_report ""

if [ "$FINAL_STATUS" == "success" ]; then
    add_to_report "### ✅ Resultat Final: ÈXIT"
    add_to_report ""
    add_to_report "Tots els tests d'autenticació han passat correctament."
else
    add_to_report "### ❌ Resultat Final: FALLAT"
    add_to_report ""
    add_to_report "Hi ha tests que han fallat. Revisa els detalls anteriors."
fi

add_to_report ""
add_to_report "---"
add_to_report ""
add_to_report "## 📝 Següents Passos"
add_to_report ""
add_to_report "1. **Tests Automatitzats**: Implementar tests amb pytest"
add_to_report "2. **Tests de Seguretat**: Executar suite OWASP"
add_to_report "3. **Tests de Performance**: Load testing amb Locust"
add_to_report ""
add_to_report "---"
add_to_report ""
add_to_report "*Report generat automàticament per test_auth_with_report.sh*"
add_to_report ""
add_to_report "*API d'ingesta de dades d'ICATMAR - $(date '+%Y')*"

# Generar versió HTML del report
echo ""
echo "Generant versió HTML del report..."

if command -v pandoc &> /dev/null; then
    pandoc "$REPORT_FILE" -o "$HTML_REPORT" \
        --metadata title="Report Tests JWT - VCPE API" \
        --standalone \
        --css=https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css \
        --self-contained
    echo "Report HTML generat a: $HTML_REPORT"
else
    echo "pandoc no està instal·lat. Report HTML no generat."
    echo "Per instal·lar: sudo apt-get install pandoc"
fi

# Mostrar fitxers generats
echo ""
echo "Fitxers generats:"
ls -lh "$REPORT_DIR"/*.md "$REPORT_DIR"/*.html 2>/dev/null | tail -n 2

# Oferir obrir el report
echo ""
read -p "Vols obrir el report? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "$HTML_REPORT" ]; then
        xdg-open "$HTML_REPORT" 2>/dev/null || open "$HTML_REPORT" 2>/dev/null || echo "No s'ha pogut obrir automàticament. Obre manualment: $HTML_REPORT"
    else
        cat "$REPORT_FILE"
    fi
fi

# Exit code segons resultat
if [ "$FINAL_STATUS" == "success" ]; then
    exit 0
else
    exit 1
fi#!/bin/bash

# Tests d'Autenticació JWT per VCPE API amb Report
# Per executar: chmod +x test_auth_with_report.sh && ./test_auth_with_report.sh

set -e

# Colors per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables globals per report
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
REPORT_DIR="test_reports"
REPORT_FILE="$REPORT_DIR/auth_test_report_$(date '+%Y%m%d_%H%M%S').md"
HTML_REPORT="${REPORT_FILE%.md}.html"
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Crear directori de reports si no existeix
mkdir -p "$REPORT_DIR"

# Funció per afegir al report
add_to_report() {
    echo "$1" >> "$REPORT_FILE"
}

# Funció per executar test i registrar resultat
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected="$3"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Test $TOTAL_TESTS: $test_name${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

    add_to_report ""
    add_to_report "### Test $TOTAL_TESTS: $test_name"
    add_to_report ""
    add_to_report "**Hora d'execució:** $(date '+%H:%M:%S')"
    add_to_report ""

    # Executar el test i capturar resultat
    local start_time=$(date +%s%N)
    local result=$(eval "$test_command" 2>&1)
    local exit_code=$?
    local end_time=$(date +%s%N)
    local duration=$(( (end_time - start_time) / 1000000 ))

    # Mostrar resultat
    echo "Temps d'execució: ${duration}ms"
    echo ""
    echo "Resultat:"
    echo "$result"
    echo ""

    add_to_report "**Temps d'execució:** ${duration}ms"
    add_to_report ""
    add_to_report "**Comanda executada:**"
    add_to_report '```bash'
    add_to_report "$test_command"
    add_to_report '```'
    add_to_report ""

    # Verificar si el test ha passat
    if echo "$result" | grep -q "$expected"; then
        echo -e "${GREEN}✓ PASS${NC}"
        add_to_report "**Resultat:** ✅ **PASS**"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAIL${NC}"
        add_to_report "**Resultat:** ❌ **FAIL**"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi

    add_to_report ""
    add_to_report "<details>"
    add_to_report "<summary>Resposta completa (clica per veure)</summary>"
    add_to_report ""
    add_to_report '```json'
    add_to_report "$result"
    add_to_report '```'
    add_to_report ""
    add_to_report "</details>"
    add_to_report ""
    add_to_report "---"

    return $exit_code
}

# Iniciar report
echo "================================================"
echo "VCPE API - Suite de Tests d'Autenticació JWT"
echo "================================================"
echo "Data: $TIMESTAMP"
echo ""

add_to_report "# Report de Tests d'Autenticació JWT - VCPE API"
add_to_report ""
add_to_report "**Data d'execució:** $TIMESTAMP"
add_to_report ""
add_to_report "**Projecte:** API d'ingesta de dades d'ICATMAR"
add_to_report ""
add_to_report "---"
add_to_report ""

# Test 1: Health Check
run_test "Health Check de l'API" \
    "curl -s http://localhost:8000/health/" \
    "healthy"

# Test 2: Vista Root
run_test "Vista Root de l'API" \
    "curl -s http://localhost:8000/" \
    "vcpe-api"

# Test 3: Obtenir Token JWT
echo -e "${YELLOW}Nota: Assegura't que l'usuari admin_test existeix (make createsuperuser)${NC}"

TOKEN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin_test",
    "password": "admin"
  }')

run_test "Obtenir Token JWT amb credencials vàlides" \
    "echo '$TOKEN_RESPONSE'" \
    "access"

if echo "$TOKEN_RESPONSE" | grep -q "access"; then
    ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access' 2>/dev/null || echo "")
    REFRESH_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.refresh' 2>/dev/null || echo "")

    # Guardar tokens
    echo "export ACCESS_TOKEN='$ACCESS_TOKEN'" > .tokens
    echo "export REFRESH_TOKEN='$REFRESH_TOKEN'" >> .tokens

    add_to_report ""
    add_to_report "**Tokens obtinguts:**"
    add_to_report "- Access Token: \`${ACCESS_TOKEN:0:50}...\`"
    add_to_report "- Refresh Token: \`${REFRESH_TOKEN:0:50}...\`"
    add_to_report ""

    # Test 4: Verificar Token
    run_test "Verificar Token JWT vàlid" \
        "curl -s -X POST http://localhost:8000/api/auth/token/verify/ -H 'Content-Type: application/json' -d '{\"token\": \"$ACCESS_TOKEN\"}'" \
        ""

    # Test 5: Refrescar Token
    run_test "Refrescar Token JWT" \
        "curl -s -X POST http://localhost:8000/api/auth/token/refresh/ -H 'Content-Type: application/json' -d '{\"refresh\": \"$REFRESH_TOKEN\"}'" \
        "access"

    # Test 6: Accés sense token (ha de fallar)
    run_test "Accés a endpoint protegit sense token (ha de retornar 401)" \
        "curl -s -w '\n%{http_code}' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "401"

    # Test 7: Accés amb token vàlid
    run_test "Accés a endpoint protegit amb token vàlid" \
        "curl -s -w '\n%{http_code}' -H 'Authorization: Bearer $ACCESS_TOKEN' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "200\|404"

    # Test 8: Token manipulat (ha de fallar)
    FAKE_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"

    run_test "Token JWT manipulat (ha de retornar 401)" \
        "curl -s -w '\n%{http_code}' -H 'Authorization: Bearer $FAKE_TOKEN' http://localhost:8000/api/sales-notes/ | tail -n 1" \
        "401"
else
    echo -e "${RED}No s'han pogut obtenir els tokens. Els següents tests es saltaran.${NC}"
    add_to_report ""
    add_to_report "⚠️ **Error:** No s'han pogut obtenir els tokens JWT. Tests posteriors saltats."
    add_to_report ""
fi

# Test 9: Credencials invàlides
run_test "Login amb credencials invàlides (ha de retornar 401)" \
    "curl -s -w '\n%{http_code}' -X POST http://localhost:8000/api/auth/token/ -H 'Content-Type: application/json' -d '{\"username\": \"usuari_inexistent\", \"password\": \"PasswordIncorrecte\"}' | tail -n 1" \
    "401"

# Test 10: Documentació API accessible
run_test "Documentació Swagger accessible" \
    "curl -s -w '\n%{http_code}' http://localhost:8000/api/docs/ | tail -n 1" \
    "200"

# Resum Final
echo ""
echo "================================================"
echo -e "${GREEN}RESUM DELS TESTS${NC}"
echo "================================================"
echo "Total de tests executats: $TOTAL_TESTS"
echo -e "${GREEN}Tests passats: $PASSED_TESTS${NC}"
echo -e "${RED}Tests fallats: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}✓ Tots els tests han passat correctament!${NC}"
    FINAL_STATUS="success"
else
    echo -e "${RED}✗ Hi ha tests que han fallat. Revisa el report.${NC}"
    FINAL_STATUS="failure"
fi

echo ""
echo "Report generat a: $REPORT_FILE"
echo "================================================"

# Afegir resum al report
add_to_report ""
add_to_report "## 📊 Resum d'Execució"
add_to_report ""
add_to_report "| Mètrica | Valor |"
add_to_report "|---------|-------|"
add_to_report "| **Total Tests** | $TOTAL_TESTS |"
add_to_report "| **Tests Passats** | ✅ $PASSED_TESTS |"
add_to_report "| **Tests Fallats** | ❌ $FAILED_TESTS |"
add_to_report "| **Taxa d'Èxit** | $(( PASSED_TESTS * 100 / TOTAL_TESTS ))% |"
add_to_report ""

if [ "$FINAL_STATUS" == "success" ]; then
    add_to_report "### ✅ Resultat Final: ÈXIT"
    add_to_report ""
    add_to_report "Tots els tests d'autenticació han passat correctament."
else
    add_to_report "### ❌ Resultat Final: FALLAT"
    add_to_report ""
    add_to_report "Hi ha tests que han fallat. Revisa els detalls anteriors."
fi

add_to_report ""
add_to_report "---"
add_to_report ""
add_to_report "## 📝 Següents Passos"
add_to_report ""
add_to_report "1. **Tests Automatitzats**: Implementar tests amb pytest"
add_to_report "2. **Tests de Seguretat**: Executar suite OWASP"
add_to_report "3. **Tests de Performance**: Load testing amb Locust"
add_to_report ""
add_to_report "---"
add_to_report ""
add_to_report "*Report generat automàticament per test_auth_with_report.sh*"
add_to_report ""
add_to_report "*API d'ingesta de dades d'ICATMAR - $(date '+%Y')*"

# Generar versió HTML del report
echo ""
echo "Generant versió HTML del report..."

if command -v pandoc &> /dev/null; then
    pandoc "$REPORT_FILE" -o "$HTML_REPORT" \
        --metadata title="Report Tests JWT - VCPE API" \
        --standalone \
        --css=https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css \
        --self-contained
    echo "Report HTML generat a: $HTML_REPORT"
else
    echo "pandoc no està instal·lat. Report HTML no generat."
    echo "Per instal·lar: sudo apt-get install pandoc"
fi

# Mostrar fitxers generats
echo ""
echo "Fitxers generats:"
ls -lh "$REPORT_DIR"/*.md "$REPORT_DIR"/*.html 2>/dev/null | tail -n 2

# Oferir obrir el report
echo ""
read -p "Vols obrir el report? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -f "$HTML_REPORT" ]; then
        xdg-open "$HTML_REPORT" 2>/dev/null || open "$HTML_REPORT" 2>/dev/null || echo "No s'ha pogut obrir automàticament. Obre manualment: $HTML_REPORT"
    else
        cat "$REPORT_FILE"
    fi
fi

# Exit code segons resultat
if [ "$FINAL_STATUS" == "success" ]; then
    exit 0
else
    exit 1
fi
