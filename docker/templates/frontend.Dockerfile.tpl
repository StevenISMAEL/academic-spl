# =============================================================================
# Frontend Dockerfile — Laravel + Vite (Academic SPL)
# Core Asset compartido por todos los productos derivados.
# La URL del backend se inyecta en tiempo de ejecución via variable de entorno.
# =============================================================================

# ── Etapa 1: Build (Node + Composer) ─────────────────────────────────────────
FROM php:8.3-cli AS builder

# Instalar dependencias del sistema para Composer + extensiones PHP
RUN apt-get update && apt-get install -y \
    git curl unzip libzip-dev libpng-dev libonig-dev \
    && docker-php-ext-install zip pdo pdo_sqlite \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar Node.js 22 (para compilar assets con Vite)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Instalar Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /app

# Copiar solo los archivos de dependencias primero (optimiza la caché de Docker)
COPY core_assets/frontend/laravel-shell/composer.json \
     core_assets/frontend/laravel-shell/composer.lock ./
RUN composer install --no-dev --no-scripts --no-autoloader --prefer-dist

COPY core_assets/frontend/laravel-shell/package.json \
     core_assets/frontend/laravel-shell/package-lock.json ./
RUN npm ci --ignore-scripts

# Copiar el resto del código Laravel
COPY core_assets/frontend/laravel-shell/ .

# Generar autoloader optimizado para producción
RUN composer dump-autoload --optimize --no-dev

# Compilar los assets de Vite (CSS/JS) para producción
RUN npm run build

# ── Etapa 2: Runtime (servidor PHP de producción) ─────────────────────────────
FROM php:8.3-fpm-alpine AS runtime

# Instalar extensiones PHP necesarias en runtime
RUN apk add --no-cache \
    nginx \
    sqlite-dev \
    && docker-php-ext-install pdo pdo_sqlite

WORKDIR /var/www/html

# Copiar el build desde la etapa anterior
COPY --from=builder /app /var/www/html

# Crear el archivo SQLite para sesiones/caché de Laravel
RUN mkdir -p database \
    && touch database/database.sqlite \
    && chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html/storage \
    && chmod -R 755 /var/www/html/bootstrap/cache

# Configuración de Nginx
COPY docker/templates/nginx.conf /etc/nginx/nginx.conf

# Script de inicio que genera el .env en runtime con las variables de entorno
COPY docker/templates/frontend-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

# El entrypoint construye el .env desde variables de entorno y arranca Nginx + PHP-FPM
ENTRYPOINT ["/entrypoint.sh"]
