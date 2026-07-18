<?php

namespace Tests\Unit\Helpers;

use App\Core\Helpers\GradeHelper;
use InvalidArgumentException;
use PHPUnit\Framework\TestCase;

/**
 * Tests unitarios para GradeHelper.
 *
 * Cobertura completa de todos los métodos del helper:
 *   - toLiteral()   → todos los rangos + valor fuera de rango
 *   - passes()      → con y sin umbral, en el límite, bajo y sobre
 *   - status()      → aprobado y reprobado
 *   - toDisplay()   → escala numeric y literal, escala inválida
 *   - annotateList() → lista completa, vacía, campo personalizado
 *
 * Estos tests no usan Laravel (extienden PHPUnit\Framework\TestCase)
 * para que sean lo más rápidos y aislados posible.
 */
class GradeHelperTest extends TestCase
{
    // ─── toLiteral ──────────────────────────────────────────────────────────────

    public function test_to_literal_devuelve_sobresaliente_para_nota_10(): void
    {
        $this->assertSame('Sobresaliente', GradeHelper::toLiteral(10.0));
    }

    public function test_to_literal_devuelve_sobresaliente_para_limite_inferior_9(): void
    {
        $this->assertSame('Sobresaliente', GradeHelper::toLiteral(9.0));
    }

    public function test_to_literal_devuelve_muy_bueno_para_nota_8_5(): void
    {
        $this->assertSame('Muy Bueno', GradeHelper::toLiteral(8.5));
    }

    public function test_to_literal_devuelve_muy_bueno_para_limite_inferior_7(): void
    {
        $this->assertSame('Muy Bueno', GradeHelper::toLiteral(7.0));
    }

    public function test_to_literal_devuelve_bueno_para_nota_6(): void
    {
        $this->assertSame('Bueno', GradeHelper::toLiteral(6.0));
    }

    public function test_to_literal_devuelve_bueno_para_limite_inferior_5(): void
    {
        $this->assertSame('Bueno', GradeHelper::toLiteral(5.0));
    }

    public function test_to_literal_devuelve_regular_para_nota_4(): void
    {
        $this->assertSame('Regular', GradeHelper::toLiteral(4.0));
    }

    public function test_to_literal_devuelve_regular_para_limite_inferior_3(): void
    {
        $this->assertSame('Regular', GradeHelper::toLiteral(3.0));
    }

    public function test_to_literal_devuelve_insuficiente_para_nota_2(): void
    {
        $this->assertSame('Insuficiente', GradeHelper::toLiteral(2.0));
    }

    public function test_to_literal_devuelve_insuficiente_para_nota_cero(): void
    {
        $this->assertSame('Insuficiente', GradeHelper::toLiteral(0.0));
    }

    public function test_to_literal_retorna_string_numerico_para_valor_fuera_de_rango(): void
    {
        $result = GradeHelper::toLiteral(11.5);
        $this->assertStringContainsString('11.5', $result);
    }

    public function test_to_literal_retorna_string_numerico_para_nota_negativa(): void
    {
        $result = GradeHelper::toLiteral(-1.0);
        $this->assertIsString($result);
    }

    // ─── passes ─────────────────────────────────────────────────────────────────

    public function test_passes_retorna_true_cuando_nota_supera_umbral(): void
    {
        $this->assertTrue(GradeHelper::passes(8.0, 7.0));
    }

    public function test_passes_retorna_true_cuando_nota_igual_al_umbral(): void
    {
        $this->assertTrue(GradeHelper::passes(7.0, 7.0));
    }

    public function test_passes_retorna_false_cuando_nota_por_debajo_del_umbral(): void
    {
        $this->assertFalse(GradeHelper::passes(6.9, 7.0));
    }

    public function test_passes_usa_default_cuando_umbral_es_null(): void
    {
        $this->assertTrue(GradeHelper::passes(7.0));
        $this->assertFalse(GradeHelper::passes(6.9));
    }

    public function test_passes_con_umbral_universidad_6(): void
    {
        $this->assertTrue(GradeHelper::passes(6.5, 6.0));
        $this->assertFalse(GradeHelper::passes(5.9, 6.0));
    }

    public function test_passes_con_nota_diez_siempre_retorna_true(): void
    {
        $this->assertTrue(GradeHelper::passes(10.0, 7.0));
    }

    public function test_passes_con_nota_cero_siempre_retorna_false(): void
    {
        $this->assertFalse(GradeHelper::passes(0.0, 6.0));
    }

    // ─── status ─────────────────────────────────────────────────────────────────

    public function test_status_retorna_aprobado_cuando_pasa(): void
    {
        $this->assertSame('Aprobado', GradeHelper::status(8.0, 7.0));
    }

    public function test_status_retorna_reprobado_cuando_no_pasa(): void
    {
        $this->assertSame('Reprobado', GradeHelper::status(5.0, 7.0));
    }

    public function test_status_usa_default_cuando_umbral_es_null(): void
    {
        $this->assertSame('Aprobado', GradeHelper::status(7.0));
        $this->assertSame('Reprobado', GradeHelper::status(6.9));
    }

    // ─── toDisplay ──────────────────────────────────────────────────────────────

    public function test_to_display_numeric_retorna_numero_formateado(): void
    {
        $result = GradeHelper::toDisplay(8.5, 'numeric');
        $this->assertSame('8.50', $result);
    }

    public function test_to_display_literal_retorna_etiqueta(): void
    {
        $result = GradeHelper::toDisplay(8.5, 'literal');
        $this->assertSame('Muy Bueno', $result);
    }

    public function test_to_display_escala_invalida_lanza_exception(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessageMatches('/no soportada/');
        GradeHelper::toDisplay(8.5, 'percentual');
    }

    // ─── annotateList ────────────────────────────────────────────────────────────

    public function test_annotate_list_agrega_campos_aprueba_y_estado(): void
    {
        $grades = [['valor' => 8.0]];
        $result = GradeHelper::annotateList($grades, 7.0);

        $this->assertTrue($result[0]['aprueba']);
        $this->assertSame('Aprobado', $result[0]['estado_aprobacion']);
    }

    public function test_annotate_list_marca_reprobado_correctamente(): void
    {
        $grades = [['valor' => 5.0]];
        $result = GradeHelper::annotateList($grades, 7.0);

        $this->assertFalse($result[0]['aprueba']);
        $this->assertSame('Reprobado', $result[0]['estado_aprobacion']);
    }

    public function test_annotate_list_preserva_campos_originales(): void
    {
        $grades = [['id' => 'E-001', 'valor' => 9.0, 'curso_id' => 'C-MAT']];
        $result = GradeHelper::annotateList($grades, 7.0);

        $this->assertSame('E-001', $result[0]['id']);
        $this->assertSame('C-MAT', $result[0]['curso_id']);
        $this->assertSame(9.0, $result[0]['valor']);
    }

    public function test_annotate_list_lista_vacia_retorna_lista_vacia(): void
    {
        $result = GradeHelper::annotateList([], 7.0);
        $this->assertSame([], $result);
    }

    public function test_annotate_list_campo_personalizado_funciona(): void
    {
        $grades = [['score' => 8.0]];
        $result = GradeHelper::annotateList($grades, 7.0, 'score');

        $this->assertTrue($result[0]['aprueba']);
    }

    public function test_annotate_list_usa_default_cuando_umbral_es_null(): void
    {
        $grades = [['valor' => 7.0], ['valor' => 6.9]];
        $result = GradeHelper::annotateList($grades);

        $this->assertTrue($result[0]['aprueba']);
        $this->assertFalse($result[1]['aprueba']);
    }

    public function test_annotate_list_procesa_multiples_notas(): void
    {
        $grades = [
            ['valor' => 9.0],  // Aprobado
            ['valor' => 5.0],  // Reprobado
            ['valor' => 7.0],  // Aprobado (en el límite)
        ];
        $result = GradeHelper::annotateList($grades, 7.0);

        $this->assertTrue($result[0]['aprueba']);
        $this->assertFalse($result[1]['aprueba']);
        $this->assertTrue($result[2]['aprueba']);
    }
}
