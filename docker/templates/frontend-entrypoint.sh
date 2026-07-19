#!/bin/bash
# =============================================================================
# Entrypoint del contenedor Frontend (Laravel + Apache)
#
# Genera el .env de Laravel desde variables de entorno de Kubernetes,
# ejecuta migraciones y arranca Apache en foreground.
#
# Variables requeridas (desde ConfigMap/Secret de Kubernetes):
#   APP_NAME     - Nombre del producto
#   APP_KEY      - Clave de cifrado de Laravel (desde Secret)
#   APP_URL      - URL pública del frontend
#   APP_ENV      - Entorno (production/staging)
#   BACKEND_URL  - URL interna del backend en el clúster
# =============================================================================
set -e

echo ">>> [Frontend] Generando .env desde variables de entorno..."
cat > /var/www/html/.env << EOF
APP_NAME="${APP_NAME:-Academic SPL}"
APP_ENV=${APP_ENV:-production}
APP_KEY=${APP_KEY}
APP_DEBUG=false
APP_URL=${APP_URL:-http://localhost}

APP_LOCALE=en
APP_FALLBACK_LOCALE=en

LOG_CHANNEL=stderr
LOG_LEVEL=warning

DB_CONNECTION=sqlite
DB_DATABASE=/var/www/html/database/database.sqlite

SESSION_DRIVER=database
SESSION_LIFETIME=120
CACHE_STORE=database
QUEUE_CONNECTION=sync

# URL interna del backend FastAPI en el mismo clúster de Kubernetes
CORE_ENGINE_BACKEND_URL=${BACKEND_URL:-http://localhost:8000}

VITE_APP_NAME="${APP_NAME:-Academic SPL}"
EOF

echo ">>> [Frontend] APP_KEY presente: $([ -n "${APP_KEY}" ] && echo 'SÍ' || echo 'NO - ERROR')"
echo ">>> [Frontend] BACKEND_URL = ${BACKEND_URL:-no configurado}"

echo ">>> [Frontend] Ejecutando migraciones de Laravel..."
php artisan migrate --force --no-interaction 2>/dev/null || true

echo ">>> [Frontend] Sembrando datos iniciales (usuario de prueba)..."
php artisan db:seed --force --no-interaction 2>/dev/null || true

echo ">>> [Frontend] Limpiando y reconstruyendo caché..."
php artisan config:cache  2>/dev/null || true
php artisan route:cache   2>/dev/null || true
php artisan view:cache    2>/dev/null || true

echo ">>> [Frontend] Iniciando Apache..."
exec apache2-foreground
