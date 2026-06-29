<?php

// Core Asset — config/core_engine.php
//
// Punto único de configuración de dónde vive el backend. En Sprint 3,
// esto vendrá inyectado por variable de entorno según el producto
// que el pipeline esté ensamblando (mismo patrón que PRODUCT_CONFIG_PATH
// en el backend Python).

return [
    'backend_url' => env('CORE_ENGINE_BACKEND_URL', 'http://127.0.0.1:8001/'),
];
