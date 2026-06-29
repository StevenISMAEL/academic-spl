<?php

namespace App\Providers;

use App\Core\Services\FeatureGate;
use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

/**
 * Core Asset — Registro de la directiva Blade @feature (COR-09)
 *
 * Una vez registrado, cualquier vista puede usar:
 *
 *   @feature('attendance')
 *       <div>Tabla de asistencia</div>
 *   @endfeature
 *
 * Sin que la vista necesite saber CÓMO se resuelve esa decisión.
 */
class FeatureGateServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        Blade::if('feature', function (string $featureName) {
            return FeatureGate::isActive($featureName);
        });

        // Variante con bloque @feature/@endfeature (equivalente a @if/@endif)
        Blade::directive('feature', function ($expression) {
            return "<?php if (\App\Core\Services\FeatureGate::isActive({$expression})): ?>";
        });

        Blade::directive('endfeature', function () {
            return '<?php endif; ?>';
        });
    }
}

// Recuerda registrar este provider en config/app.php (providers array)
// o en bootstrap/providers.php según la versión de Laravel que instalen.
