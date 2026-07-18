<?php

namespace App\Core\Helpers;

/**
 * GradeHelper — Capa de presentación para conversión de calificaciones.
 *
 * Replica la lógica del Core Asset Python GradeScaleConverter (CA-02)
 * y GradePassingChecker (CA-04) para la capa de visualización PHP/Laravel.
 *
 * IMPORTANTE: Este helper es de solo presentación. Las validaciones de
 * negocio definitivas viven en el backend Python (FastAPI). Este helper
 * formatea valores ya calculados para mostrarlos en las vistas Blade.
 *
 * Escala literal (sistema educativo ecuatoriano — educación básica):
 *   9.0 - 10.0 → Sobresaliente
 *   7.0 -  8.9 → Muy Bueno
 *   5.0 -  6.9 → Bueno
 *   3.0 -  4.9 → Regular
 *   0.0 -  2.9 → Insuficiente
 */
class GradeHelper
{
    /**
     * Nota mínima de aprobación por defecto (sistema ecuatoriano básico).
     * Puede ser sobreescrita por el product_config.yaml de cada producto.
     */
    public const DEFAULT_PASSING_GRADE = 7.0;

    /**
     * Tabla de conversión numérico → literal.
     * Cada entrada: [min, max, etiqueta]
     */
    private const LITERAL_TABLE = [
        [9.0, 10.0, 'Sobresaliente'],
        [7.0,  8.9, 'Muy Bueno'],
        [5.0,  6.9, 'Bueno'],
        [3.0,  4.9, 'Regular'],
        [0.0,  2.9, 'Insuficiente'],
    ];

    /**
     * Convierte una nota numérica a su etiqueta literal.
     *
     * @param  float  $valor  Calificación numérica (0.0 – 10.0).
     * @return string         Etiqueta cualitativa correspondiente.
     */
    public static function toLiteral(float $valor): string
    {
        foreach (self::LITERAL_TABLE as [$min, $max, $label]) {
            if ($valor >= $min && $valor <= $max) {
                return $label;
            }
        }

        // Valor fuera de rango: retornar número como string para no perder información.
        return (string) round($valor, 2);
    }

    /**
     * Determina si una nota aprueba según el umbral mínimo del producto.
     *
     * @param  float       $valor        Calificación numérica.
     * @param  float|null  $passingGrade Nota mínima de aprobación del producto.
     *                                  Si es null, usa DEFAULT_PASSING_GRADE.
     * @return bool        True si la nota supera o iguala el umbral.
     */
    public static function passes(float $valor, ?float $passingGrade = null): bool
    {
        $threshold = $passingGrade ?? self::DEFAULT_PASSING_GRADE;
        return $valor >= $threshold;
    }

    /**
     * Retorna el estado de aprobación como cadena.
     *
     * @param  float       $valor        Calificación numérica.
     * @param  float|null  $passingGrade Nota mínima de aprobación.
     * @return string      'Aprobado' | 'Reprobado'
     */
    public static function status(float $valor, ?float $passingGrade = null): string
    {
        return self::passes($valor, $passingGrade) ? 'Aprobado' : 'Reprobado';
    }

    /**
     * Formatea una nota para mostrar en la vista, según la escala del producto.
     *
     * @param  float   $valor  Calificación numérica.
     * @param  string  $scale  'numeric' (retorna el número formateado) |
     *                         'literal' (retorna etiqueta cualitativa).
     * @return string  Valor formateado para mostrar al usuario.
     *
     * @throws \InvalidArgumentException Si la escala no es soportada.
     */
    public static function toDisplay(float $valor, string $scale): string
    {
        return match ($scale) {
            'numeric' => number_format($valor, 2),
            'literal' => self::toLiteral($valor),
            default   => throw new \InvalidArgumentException(
                "Escala '{$scale}' no soportada. Valores válidos: 'numeric', 'literal'."
            ),
        };
    }

    /**
     * Agrega los campos 'aprueba' y 'estado_aprobacion' a cada nota de una lista.
     *
     * Útil para enriquecer colecciones de notas antes de pasarlas a las vistas.
     *
     * @param  array<array<string, mixed>>  $grades       Lista de calificaciones.
     * @param  float|null                   $passingGrade Umbral mínimo de aprobación.
     * @param  string                       $valorField   Campo numérico en cada elemento.
     * @return array<array<string, mixed>>  Lista con campos 'aprueba' y 'estado_aprobacion'.
     */
    public static function annotateList(array $grades, ?float $passingGrade = null, string $valorField = 'valor'): array
    {
        return array_map(function (array $grade) use ($passingGrade, $valorField): array {
            $valor = (float) ($grade[$valorField] ?? 0);
            $grade['aprueba']           = self::passes($valor, $passingGrade);
            $grade['estado_aprobacion'] = self::status($valor, $passingGrade);
            return $grade;
        }, $grades);
    }
}
