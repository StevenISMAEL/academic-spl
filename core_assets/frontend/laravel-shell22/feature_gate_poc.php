<?php
/**
 * POC del patrón FeatureGate — PHP plano, sin framework.
 *
 * Este script NO es parte del Laravel Shell final. Es una prueba
 * aislada para demostrar, de forma ejecutable, el mismo patrón que
 * implementará FeatureGate.php dentro de Laravel: consultar al
 * backend (Core Engine) qué features están activos, y decidir si
 * renderizar un bloque de contenido o no.
 *
 * Por qué existe: no fue posible instalar Laravel completo en este
 * entorno (requiere Composer + Packagist, no disponibles aquí). Esto
 * prueba que la LÓGICA funciona de verdad contra el backend real,
 * para que el equipo solo tenga que "envolverla" en código Laravel.
 */

function fetch_active_features(string $backend_url): array
{
    $json = @file_get_contents($backend_url);
    if ($json === false) {
        throw new RuntimeException("No se pudo contactar al backend en: {$backend_url}");
    }
    $data = json_decode($json, true);
    return $data['active_features'] ?? [];
}

function feature_is_active(array $active_features, string $feature_name): bool
{
    return in_array($feature_name, $active_features, true);
}

// --- Simulación de lo que hará @feature('attendance') ... @endfeature ---
function render_block(string $product_label, array $active_features, string $feature_name, string $content): void
{
    echo "[{$product_label}] @feature('{$feature_name}') -> ";
    if (feature_is_active($active_features, $feature_name)) {
        echo "ACTIVO -> se renderiza: \"{$content}\"\n";
    } else {
        echo "INACTIVO -> bloque omitido (no se renderiza nada)\n";
    }
}

$colegio_url = $argv[1] ?? 'http://127.0.0.1:8021/';
$universidad_url = $argv[2] ?? 'http://127.0.0.1:8022/';

echo "=== Consultando backend real (Colegio Básico) ===\n";
$colegio_features = fetch_active_features($colegio_url);
echo "Features activos recibidos: " . implode(', ', $colegio_features) . "\n\n";

echo "=== Consultando backend real (Universidad Compleja) ===\n";
$universidad_features = fetch_active_features($universidad_url);
echo "Features activos recibidos: " . implode(', ', $universidad_features) . "\n\n";

echo "=== Simulación de renderizado condicional (FeatureGate) ===\n";
render_block('Colegio', $colegio_features, 'attendance', '<div>Tabla de asistencia</div>');
render_block('Colegio', $colegio_features, 'enrollment', '<div>Formulario de matrícula por créditos</div>');
render_block('Universidad', $universidad_features, 'attendance', '<div>Tabla de asistencia</div>');
render_block('Universidad', $universidad_features, 'enrollment', '<div>Formulario de matrícula por créditos</div>');
