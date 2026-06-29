# Laravel Shell — Instrucciones de integración

Este código fue validado sintácticamente (`php -l`) pero **no
ejecutado dentro de un proyecto Laravel real**, porque generarlo
requiere Composer + Packagist, no disponibles en el entorno donde lo
construí. Sigue estos pasos en tu máquina (ya tienes Laragon
instalado según la guía de Windows):

## 1. Crear el proyecto base

```powershell
cd core_assets/frontend
composer create-project laravel/laravel laravel-shell
```

## 2. Copiar los archivos de este paquete dentro del proyecto recién creado

| Archivo en este paquete | Destino dentro de `laravel-shell/` |
|---|---|
| `app/Core/Services/FeatureGate.php` | mismo path |
| `app/Providers/FeatureGateServiceProvider.php` | mismo path |
| `app/Http/Controllers/Auth/LoginController.php` | mismo path |
| `app/Modules/AttendanceModule/**` | mismo path |
| `config/core_engine.php` | mismo path |
| `routes/web.php` | **reemplaza** el que trae Laravel por defecto |
| `resources/views/dashboard.blade.php` | mismo path |

## 3. Registrar el ServiceProvider

En Laravel 11 (bootstrap/providers.php):
```php
return [
    App\Providers\AppServiceProvider::class,
    App\Providers\FeatureGateServiceProvider::class,
];
```

En Laravel 10 o anterior (config/app.php, array `providers`):
```php
App\Providers\FeatureGateServiceProvider::class,
```

## 4. Configurar la URL del backend

En tu archivo `.env`:
```
CORE_ENGINE_BACKEND_URL=http://127.0.0.1:8001/
```

## 5. Crear un usuario de prueba para el login

```powershell
php artisan tinker
>>> App\Models\User::factory()->create(['email' => 'test@academic-spl.local', 'password' => bcrypt('password')]);
```

## 6. Levantar todo junto para la demo

Terminal 1 (backend, como ya sabes hacerlo):
```powershell
$env:PRODUCT_CONFIG_PATH="products/colegio-basico/product_config.yaml"
uvicorn run_app:app --port 8001
```

Terminal 2 (Laravel):
```powershell
cd core_assets/frontend/laravel-shell
php artisan serve
```

Entra a `http://127.0.0.1:8000/login`, inicia sesión, y en
`/dashboard` deberías ver únicamente las secciones de los features que
el backend (puerto 8001) reporta como activos para ese producto.

## Validación ya realizada (sin Laravel completo)

- `feature_gate_poc.php`: probado en vivo contra el backend real
  (FastAPI), demostrando que el patrón de consulta + decisión
  condicional funciona end-to-end entre PHP y Python.
- Todos los `.php` de este paquete: verificados con `php -l` (cero
  errores de sintaxis).

Lo único que falta para llamarlo "100% probado" es ejecutarlo dentro
del framework Laravel real, una vez instalado en sus máquinas.
