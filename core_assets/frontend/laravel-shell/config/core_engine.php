<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Core Engine Backend URL
    |--------------------------------------------------------------------------
    |
    | URL base del backend FastAPI (Core Engine). FeatureGate la usa para
    | consultar qué features están activas en el producto configurado.
    | Definir CORE_ENGINE_BACKEND_URL en el .env.
    |
    */
    'backend_url' => env('CORE_ENGINE_BACKEND_URL', 'http://127.0.0.1:8001/'),
];
