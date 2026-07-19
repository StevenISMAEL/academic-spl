#!/bin/sh
# =============================================================================
# Entrypoint del contenedor Frontend (Laravel)
#
# Genera el archivo .env de Laravel a partir de variables de entorno de
# Kubernetes (ConfigMap / Secret), luego arranca PHP-FPM y Nginx.
#
# Variables de entorno requeridas (inyectadas por Kubernetes):
#   - APP_NAME          → Nombre del producto (ej. "Universidad UTN")
#   - APP_KEY           → Clave de cifrado de Laravel (secreto de k8s)
#   - APP_URL           → URL pública del propio frontend
#   - APP_ENV           → Entorno (production / staging)
#   - BACKEND_URL       → URL interna del servicio backend en k8s
#                         (ej. http://backend-utn-service:8000)
# =============================================================================
set -e

echo ">>> Generando .env desde variables de entorno de Kubernetes..."
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

# Base de datos SQLite para sesiones y caché de Laravel
DB_CONNECTION=sqlite
DB_DATABASE=/var/www/html/database/database.sqlite

SESSION_DRIVER=database
SESSION_LIFETIME=120
CACHE_STORE=database
QUEUE_CONNECTION=sync

# URL del backend FastAPI — inyectada por Kubernetes
# En producción: http://<product>-backend-service:8000
# En staging:    http://<product>-backend-service:8000
CORE_ENGINE_BACKEND_URL=${BACKEND_URL:-http://localhost:8000}

VITE_APP_NAME="${APP_NAME:-Academic SPL}"
EOF

echo ">>> .env generado. CORE_ENGINE_BACKEND_URL = ${BACKEND_URL}"

echo ">>> Ejecutando migraciones de Laravel (sesiones, caché)..."
php /var/www/html/artisan migrate --force --no-interaction 2>/dev/null || true

echo ">>> Limpiando caché de configuración..."
php /var/www/html/artisan config:cache
php /var/www/html/artisan route:cache

echo ">>> Iniciando PHP-FPM en background..."
php-fpm -D

echo ">>> Iniciando Nginx en foreground..."
nginx -g "daemon off;"
