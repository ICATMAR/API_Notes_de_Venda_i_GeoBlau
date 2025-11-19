#!/bin/bash

echo "🚀 Configurant entorn de desenvolupament..."
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Instal·lar pre-commit
echo -e "${YELLOW}1. Instal·lant pre-commit...${NC}"
pip install pre-commit || { echo -e "${RED}❌ Error instal·lant pre-commit${NC}"; exit 1; }
echo -e "${GREEN}✓ pre-commit instal·lat${NC}"
echo ""

# 2. Instal·lar git hooks
echo -e "${YELLOW}2. Instal·lant git hooks...${NC}"
pre-commit install || { echo -e "${RED}❌ Error instal·lant hooks${NC}"; exit 1; }
pre-commit install --hook-type commit-msg || { echo -e "${RED}❌ Error instal·lant commit-msg hook${NC}"; exit 1; }
echo -e "${GREEN}✓ Git hooks instal·lats${NC}"
echo ""

# 3. Instal·lar totes les eines de linting
echo -e "${YELLOW}3. Verificant eines de linting...${NC}"
pip install black flake8 isort mypy bandit django-stubs || { echo -e "${RED}❌ Error instal·lant eines${NC}"; exit 1; }
echo -e "${GREEN}✓ Eines verificades${NC}"
echo ""

# 4. Executar pre-commit per primera vegada (opcional)
echo -e "${YELLOW}4. Voleu executar pre-commit en tots els fitxers ara? (s/n)${NC}"
read -r response
if [[ "$response" =~ ^([sS][iI]?|[yY][eE][sS]?)$ ]]; then
    echo -e "${YELLOW}Executant pre-commit...${NC}"
    pre-commit run --all-files || echo -e "${YELLOW}⚠ Alguns checks han fallat, revisar sortida${NC}"
fi
echo ""

echo -e "${GREEN}✅ Entorn de desenvolupament configurat!${NC}"
echo ""
echo "📚 Comandes disponibles:"
echo "  make format          - Aplicar format a tot el codi"
echo "  make lint            - Comprovar lint (sense canvis)"
echo "  make security        - Executar checks de seguretat"
echo "  make test            - Executar tests"
echo "  make check           - Lint + security + tests"
echo "  make install-hooks   - (Re)instal·lar pre-commit hooks"
echo "  ./format_all.sh      - Format complet del repositori"
echo ""
echo "🎨 A partir d'ara, pre-commit s'executarà automàticament en cada commit."
