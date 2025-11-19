#!/bin/bash

echo "🎨 Aplicant format a tot el repositori..."
echo ""

# Colors per output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Black
echo -e "${YELLOW}1/5 Executant black...${NC}"
black . || { echo -e "${RED}❌ Black ha fallat${NC}"; exit 1; }
echo -e "${GREEN}✓ Black completat${NC}"
echo ""

# 2. isort
echo -e "${YELLOW}2/5 Executant isort...${NC}"
isort . || { echo -e "${RED}❌ isort ha fallat${NC}"; exit 1; }
echo -e "${GREEN}✓ isort completat${NC}"
echo ""

# 3. Flake8 (només check)
echo -e "${YELLOW}3/5 Comprovant amb flake8...${NC}"
flake8 . || echo -e "${YELLOW}⚠ Flake8 ha trobat problemes (revisar manualment)${NC}"
echo ""

# 4. Bandit (només check)
echo -e "${YELLOW}4/5 Comprovant seguretat amb bandit...${NC}"
bandit -r . -c pyproject.toml || echo -e "${YELLOW}⚠ Bandit ha trobat problemes (revisar manualment)${NC}"
echo ""

# 5. mypy (només check)
echo -e "${YELLOW}5/5 Comprovant types amb mypy...${NC}"
mypy . || echo -e "${YELLOW}⚠ mypy ha trobat problemes (revisar manualment)${NC}"
echo ""

echo -e "${GREEN}✅ Format aplicat a tot el repositori!${NC}"
echo ""
echo "📝 Revisar els warnings anteriors i corregir manualment si cal."
