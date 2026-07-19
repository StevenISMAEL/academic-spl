# =============================================================================
# Frontend Dockerfile — Laravel + Vite (Academic SPL)
# Imagen única basada en Debian (php:8.3-apache) — más estable que Alpine
# para producción con Laravel. La URL del backend se inyecta en runtime.
# =============================================================================

FROM php:8.3-apache

# Instalar extensiones PHP + dependencias del sistema
RUN apt-get update && apt-get install -y \
    git curl unzip libzip-dev libpng-dev libonig-dev libsqlite3-dev nodejs npm \
    && docker-php-ext-install zip pdo pdo_sqlite \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Habilitar mod_rewrite de Apache para Laravel
RUN a2enmod rewrite

# Instalar Composer
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

# Copiar archivos de dependencias primero (cache de Docker)
COPY core_assets/frontend/laravel-shell/composer.json \
     core_assets/frontend/laravel-shell/composer.lock ./
RUN composer install --no-dev --no-scripts --no-autoloader --prefer-dist

COPY core_assets/frontend/laravel-shell/package.json \
     core_assets/frontend/laravel-shell/package-lock.json ./
RUN npm ci --ignore-scripts

# Copiar el resto del código Laravel
COPY core_assets/frontend/laravel-shell/ .

# Generar autoloader optimizado y compilar assets Vite
RUN composer dump-autoload --optimize --no-dev
RUN npm run build

# Crear SQLite para sesiones/caché y ajustar permisos
RUN mkdir -p database \
    && touch database/database.sqlite \
    && chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html/storage \
    && chmod -R 755 /var/www/html/bootstrap/cache

# Configurar Apache para apuntar al public/ de Laravel
RUN echo '<VirtualHost *:80>\n\
    DocumentRoot /var/www/html/public\n\
    <Directory /var/www/html/public>\n\
        AllowOverride All\n\
        Require all granted\n\
    </Directory>\n\
    ErrorLog ${APACHE_LOG_DIR}/error.log\n\
    CustomLog ${APACHE_LOG_DIR}/access.log combined\n\
</VirtualHost>' > /etc/apache2/sites-available/000-default.conf

# Script de inicio que genera el .env desde variables de entorno de Kubernetes
COPY docker/templates/frontend-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
