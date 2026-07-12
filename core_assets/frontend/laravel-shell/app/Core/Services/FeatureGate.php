<?php

namespace App\Core\Services;

use Illuminate\Support\Facades\Cache;
use Exception;

/**
 * Core Asset — FeatureGate (COR-09)
 *
 * Resuelve la variabilidad del lado de Laravel consultando al Core
 * Engine (FastAPI) a través de CoreEngineClient. Esto evita
 * duplicar la lógica de resolución de variabilidad en dos lenguajes:
 * la fuente de verdad sigue siendo feature_flags.py.
 *
 * Este archivo NO conoce ningún producto. Solo sabe preguntarle al
 * backend "¿qué está activo?" y cachear la respuesta brevemente.
 */
class FeatureGate
{
    private const CACHE_KEY = 'core_engine_active_features';
    private const CACHE_TTL_SECONDS = 30;

    public static function isActive(string $featureName): bool
    {
        return in_array($featureName, self::activeFeatures(), true);
    }

    public static function setting(string $key, mixed $default = null): mixed
    {
        $info = self::productInfo();
        return data_get($info, "academic_settings.{$key}", $default);
    }

    public static function activeFeatures(): array
    {
        return self::productInfo()['active_optional_features'] ?? [];
    }

    public static function productInfo(): array
    {
        return Cache::remember(self::CACHE_KEY, self::CACHE_TTL_SECONDS, function () {
            try {
                $client = new CoreEngineClient();
                return $client->get('/');
            } catch (Exception $e) {
                // Fail-closed: si el backend no responde, NINGÚN feature
                // se muestra. Es más seguro mostrar de menos que mostrar
                // de más por error de configuración o caída del backend.
                return [
                    'product' => 'Desconectado',
                    'active_optional_features' => [],
                    'academic_settings' => []
                ];
            }
        });
    }
}

