#!/bin/bash

# Script de diagnòstic per detectar errors als serializers

echo "🔍 Diagnòstic de problemes amb serializers..."
echo ""

echo "1. Comprovant imports d'authentication..."
docker-compose exec -T api python manage.py shell <<EOF
try:
    from authentication.serializers import UserSerializer
    print("✓ authentication.serializers OK")
except Exception as e:
    print("✗ ERROR en authentication.serializers:")
    print(str(e))
    import traceback
    traceback.print_exc()
EOF

echo ""
echo "2. Comprovant imports de sales_notes..."
docker-compose exec -T api python manage.py shell <<EOF
try:
    from sales_notes.serializers import EnvioListSerializer
    print("✓ sales_notes.serializers OK")
except Exception as e:
    print("✗ ERROR en sales_notes.serializers:")
    print(str(e))
    import traceback
    traceback.print_exc()
EOF

echo ""
echo "3. Comprovant drf_spectacular..."
docker-compose exec -T api python manage.py shell <<EOF
try:
    from drf_spectacular.utils import extend_schema_field
    print("✓ drf_spectacular.utils OK")
except Exception as e:
    print("✗ ERROR important drf_spectacular:")
    print(str(e))
EOF

echo ""
echo "4. Comprovant que l'API pot arrencar..."
docker-compose exec -T api python manage.py check

echo ""
echo "5. Comprovant logs recents..."
docker-compose logs api --tail=30

echo ""
echo "✅ Diagnòstic completat"
