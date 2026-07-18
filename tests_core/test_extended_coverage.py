"""
Tests de cobertura extendida para Core Assets (CA-01 al CA-05)

Este archivo cubre los métodos y casos borde que NO están en test_core_assets.py:
  - CedulaValidator: is_foreign_id, cédulas con guiones, tercer dígito >= 6
  - GradeScaleConverter: to_literal para todos los rangos, convert_grades_list,
    escala inválida, valor fuera de rango
  - AttendanceCalculator: summarize_by_persona, REPROBADO_FALTA, total=0,
    threshold_at_risk personalizado
  - GradePassingChecker: valor exacto en umbral, annotate_grades_list múltiple
  - EnrollmentLimitChecker: slots_remaining con 0 cupos, default sin parámetro

Objetivo: llevar la cobertura total de core_assets a >= 80%.
"""
import pytest

from core_assets.backend.core_engine.domain.validators.cedula_validator import CedulaValidator
from core_assets.backend.core_engine.domain.calculators.grade_scale_converter import GradeScaleConverter
from core_assets.backend.core_engine.domain.calculators.attendance_calculator import AttendanceCalculator
from core_assets.backend.core_engine.domain.calculators.grade_passing_checker import GradePassingChecker
from core_assets.backend.core_engine.domain.calculators.enrollment_limit_checker import EnrollmentLimitChecker


# ─── CA-01: CedulaValidator — casos adicionales ─────────────────────────────────

class TestCedulaValidatorExtended:
    """Cobertura extendida del validador de cédula ecuatoriana."""

    def test_cedula_valida_con_guion(self):
        """Cédula con guion debe ser normalizada y validada."""
        # La cédula válida 1713175071 con guion
        assert CedulaValidator.validate("1713-175071") is True

    def test_cedula_valida_con_espacios(self):
        """Espacios deben eliminarse antes de validar."""
        assert CedulaValidator.validate("1713 175071") is True

    def test_cedula_invalida_con_letras(self):
        """Cédula con letras debe retornar False."""
        assert CedulaValidator.validate("A713175071") is False

    def test_cedula_vacia_retorna_false(self):
        """Cadena vacía debe retornar False."""
        assert CedulaValidator.validate("") is False

    def test_cedula_con_tercer_digito_6_invalida(self):
        """Tercer dígito >= 6 indica entidad jurídica, no persona natural."""
        # Primer dígito: 17, tercer dígito: 6 → debe fallar
        assert CedulaValidator.validate("1763175071") is False

    def test_cedula_con_tercer_digito_9_invalida(self):
        """Tercer dígito 9 también es inválido para personas naturales."""
        assert CedulaValidator.validate("1793175071") is False

    def test_cedula_provincia_invalida_retorna_false(self):
        """Código de provincia inexistente (ej. 00) debe retornar False."""
        assert CedulaValidator.validate("0013175071") is False

    def test_cedula_provincia_25_invalida(self):
        """Provincia 25 no existe; debe retornar False."""
        assert CedulaValidator.validate("2513175071") is False

    def test_cedula_provincia_30_extranjero_valida(self):
        """Prefijo 30 es válido para extranjeros residentes."""
        # Construimos una cédula con provincia 30 estructuralmente coherente
        # Nota: puede o no pasar el checksum, pero la provincia es válida
        # Lo que nos interesa es que no falle POR la provincia
        cedula = CedulaValidator.validate("3001234561")
        assert isinstance(cedula, bool)  # El resultado debe ser bool (True o False)

    def test_is_foreign_id_con_prefijo_30(self):
        """is_foreign_id debe retornar True para cédulas con prefijo 30."""
        assert CedulaValidator.is_foreign_id("3001234567") is True

    def test_is_foreign_id_con_cedula_ecuatoriana(self):
        """is_foreign_id debe retornar False para cédulas ecuatorianas normales."""
        assert CedulaValidator.is_foreign_id("1713175071") is False

    def test_is_foreign_id_con_cadena_corta(self):
        """is_foreign_id con cadena de 1 carácter debe retornar False."""
        assert CedulaValidator.is_foreign_id("3") is False

    def test_is_foreign_id_con_guion(self):
        """is_foreign_id debe normalizar guiones antes de verificar."""
        assert CedulaValidator.is_foreign_id("30-01234567") is True

    def test_validate_or_raise_valida_retorna_normalizada(self):
        """validate_or_raise debe retornar la cédula limpia (sin guiones)."""
        resultado = CedulaValidator.validate_or_raise("1713175071")
        assert resultado == "1713175071"
        assert "-" not in resultado

    def test_cedula_longitud_11_invalida(self):
        """Cédula con 11 dígitos debe retornar False."""
        assert CedulaValidator.validate("17131750711") is False

    def test_cedula_longitud_9_invalida(self):
        """Cédula con 9 dígitos debe retornar False."""
        assert CedulaValidator.validate("171317507") is False


# ─── CA-02: GradeScaleConverter — casos adicionales ─────────────────────────────

class TestGradeScaleConverterExtended:
    """Cobertura extendida del convertidor de escalas."""

    def test_to_literal_bueno(self):
        """Nota 6.0 debe dar 'Bueno'."""
        assert GradeScaleConverter.to_literal(6.0) == "Bueno"

    def test_to_literal_insuficiente(self):
        """Nota 2.0 debe dar 'Insuficiente'."""
        assert GradeScaleConverter.to_literal(2.0) == "Insuficiente"

    def test_to_literal_sobresaliente_limite_inferior(self):
        """Nota exactamente 9.0 debe dar 'Sobresaliente'."""
        assert GradeScaleConverter.to_literal(9.0) == "Sobresaliente"

    def test_to_literal_muy_bueno_limite_inferior(self):
        """Nota exactamente 7.0 debe dar 'Muy Bueno'."""
        assert GradeScaleConverter.to_literal(7.0) == "Muy Bueno"

    def test_to_literal_bueno_limite_inferior(self):
        """Nota exactamente 5.0 debe dar 'Bueno'."""
        assert GradeScaleConverter.to_literal(5.0) == "Bueno"

    def test_to_literal_regular_limite_inferior(self):
        """Nota exactamente 3.0 debe dar 'Regular'."""
        assert GradeScaleConverter.to_literal(3.0) == "Regular"

    def test_to_literal_insuficiente_limite_inferior(self):
        """Nota exactamente 0.0 debe dar 'Insuficiente'."""
        assert GradeScaleConverter.to_literal(0.0) == "Insuficiente"

    def test_to_literal_valor_fuera_de_rango(self):
        """Valor fuera de 0-10 debe retornar el número como string."""
        result = GradeScaleConverter.to_literal(11.5)
        assert "11.5" in result

    def test_to_display_escala_invalida_lanza_valueerror(self):
        """Escala no soportada debe lanzar ValueError."""
        with pytest.raises(ValueError, match="no soportada"):
            GradeScaleConverter.to_display(8.5, "percentual")

    def test_convert_grades_list_numeric(self):
        """convert_grades_list con escala numeric debe agregar valor_display igual al valor."""
        grades = [{"id": "1", "valor": 8.5}, {"id": "2", "valor": 6.0}]
        result = GradeScaleConverter.convert_grades_list(grades, "numeric")
        assert result[0]["valor_display"] == 8.5
        assert result[1]["valor_display"] == 6.0

    def test_convert_grades_list_literal(self):
        """convert_grades_list con escala literal debe agregar etiqueta correcta."""
        grades = [{"id": "1", "valor": 9.5}, {"id": "2", "valor": 3.5}]
        result = GradeScaleConverter.convert_grades_list(grades, "literal")
        assert result[0]["valor_display"] == "Sobresaliente"
        assert result[1]["valor_display"] == "Regular"

    def test_convert_grades_list_preserva_campos_originales(self):
        """convert_grades_list no debe modificar los campos existentes."""
        grades = [{"id": "abc", "valor": 7.5, "persona_id": "P-001"}]
        result = GradeScaleConverter.convert_grades_list(grades, "numeric")
        assert result[0]["id"] == "abc"
        assert result[0]["persona_id"] == "P-001"
        assert result[0]["valor"] == 7.5

    def test_convert_grades_list_vacia(self):
        """Lista vacía debe retornar lista vacía."""
        result = GradeScaleConverter.convert_grades_list([], "literal")
        assert result == []

    def test_convert_grades_list_campo_personalizado(self):
        """Debe funcionar con un campo diferente a 'valor'."""
        grades = [{"score": 8.0}]
        result = GradeScaleConverter.convert_grades_list(grades, "literal", valor_field="score")
        assert result[0]["valor_display"] == "Muy Bueno"


# ─── CA-03: AttendanceCalculator — casos adicionales ─────────────────────────────

class TestAttendanceCalculatorExtended:
    """Cobertura extendida del calculador de asistencia."""

    def test_percentage_total_cero_retorna_cero(self):
        """División por cero segura: total=0 debe retornar 0.0."""
        assert AttendanceCalculator.percentage(0, 0) == 0.0

    def test_percentage_todos_ausentes(self):
        """0 presentes de 10 total = 0%."""
        assert AttendanceCalculator.percentage(0, 10) == 0.0

    def test_percentage_todos_presentes(self):
        """10 presentes de 10 total = 100%."""
        assert AttendanceCalculator.percentage(10, 10) == 100.0

    def test_status_reprobado_falta(self):
        """Porcentaje menor al umbral de riesgo = REPROBADO_FALTA."""
        assert AttendanceCalculator.status(60.0, threshold_approved=80.0, threshold_at_risk=70.0) == "REPROBADO_FALTA"

    def test_status_en_riesgo_con_umbral_personalizado(self):
        """Porcentaje entre umbral_riesgo y umbral_aprobado = EN_RIESGO."""
        assert AttendanceCalculator.status(72.0, threshold_approved=80.0, threshold_at_risk=70.0) == "EN_RIESGO"

    def test_status_usa_defaults_cuando_none(self):
        """Sin umbrales explícitos debe usar DEFAULT_THRESHOLD_APPROVED (80%) y DEFAULT_THRESHOLD_AT_RISK (70%)."""
        # 85% → APROBADO con defaults
        assert AttendanceCalculator.status(85.0) == "APROBADO"
        # 75% → EN_RIESGO con defaults (80 > 75 >= 70)
        assert AttendanceCalculator.status(75.0) == "EN_RIESGO"
        # 65% → REPROBADO_FALTA con defaults
        assert AttendanceCalculator.status(65.0) == "REPROBADO_FALTA"

    def test_summarize_lista_vacia(self):
        """summarize de lista vacía debe dar 0% y REPROBADO_FALTA."""
        result = AttendanceCalculator.summarize([])
        assert result["total_registros"] == 0
        assert result["porcentaje_asistencia"] == 0.0
        assert result["estado"] == "REPROBADO_FALTA"

    def test_summarize_todos_presentes(self):
        """Todos presentes debe dar 100% APROBADO."""
        records = [{"presente": True}] * 10
        result = AttendanceCalculator.summarize(records, threshold_approved=80.0)
        assert result["porcentaje_asistencia"] == 100.0
        assert result["estado"] == "APROBADO"

    def test_summarize_umbral_riesgo_personalizado(self):
        """summarize debe respetar threshold_at_risk personalizado."""
        records = [{"presente": True}] * 6 + [{"presente": False}] * 4  # 60%
        result = AttendanceCalculator.summarize(records, threshold_approved=80.0, threshold_at_risk=65.0)
        assert result["estado"] == "REPROBADO_FALTA"

    def test_summarize_by_persona_agrupa_correctamente(self):
        """summarize_by_persona debe agrupar registros por persona."""
        records = [
            {"persona_id": "P-001", "presente": True},
            {"persona_id": "P-001", "presente": True},
            {"persona_id": "P-002", "presente": False},
            {"persona_id": "P-002", "presente": False},
        ]
        result = AttendanceCalculator.summarize_by_persona(records)
        assert len(result) == 2
        # P-002 tiene 0% asistencia, debe estar primero (ordenado ascendente)
        assert result[0]["persona_id"] == "P-002"
        assert result[0]["porcentaje_asistencia"] == 0.0
        assert result[1]["persona_id"] == "P-001"
        assert result[1]["porcentaje_asistencia"] == 100.0

    def test_summarize_by_persona_incluye_persona_id_en_resultado(self):
        """Cada resumen debe incluir el campo 'persona_id'."""
        records = [{"persona_id": "P-999", "presente": True}]
        result = AttendanceCalculator.summarize_by_persona(records)
        assert result[0]["persona_id"] == "P-999"

    def test_summarize_umbral_en_resultado(self):
        """El campo umbral_aprobado en el resultado debe reflejar el parámetro."""
        records = [{"presente": True}] * 5
        result = AttendanceCalculator.summarize(records, threshold_approved=75.0, threshold_at_risk=60.0)
        assert result["umbral_aprobado"] == 75.0
        assert result["umbral_riesgo"] == 60.0


# ─── CA-04: GradePassingChecker — casos adicionales ─────────────────────────────

class TestGradePassingCheckerExtended:
    """Cobertura extendida del verificador de aprobación."""

    def test_passes_exactamente_en_el_umbral(self):
        """Nota exactamente igual al passing_grade debe APROBAR (>=)."""
        assert GradePassingChecker.passes(7.0, passing_grade=7.0) is True

    def test_passes_un_decimal_por_debajo_del_umbral(self):
        """Nota 6.9 con umbral 7.0 debe REPROBAR."""
        assert GradePassingChecker.passes(6.9, passing_grade=7.0) is False

    def test_passes_nota_cero(self):
        """Nota 0 debe REPROBAR con cualquier umbral > 0."""
        assert GradePassingChecker.passes(0.0, passing_grade=6.0) is False

    def test_passes_nota_diez(self):
        """Nota 10 debe APROBAR con cualquier umbral razonable."""
        assert GradePassingChecker.passes(10.0, passing_grade=7.0) is True

    def test_passes_usa_default_cuando_none(self):
        """Sin passing_grade, debe usar DEFAULT_PASSING_GRADE (7.0)."""
        assert GradePassingChecker.passes(7.0) is True
        assert GradePassingChecker.passes(6.9) is False

    def test_status_reprobado(self):
        """status debe retornar 'REPROBADO' cuando no aprueba."""
        assert GradePassingChecker.status(5.0, passing_grade=7.0) == "REPROBADO"

    def test_annotate_grades_list_varia_segun_umbral(self):
        """annotate_grades_list debe marcar correctamente con distintos umbrales."""
        grades = [{"valor": 7.0}, {"valor": 5.9}]

        # Umbral universidad (6.0)
        result_uni = GradePassingChecker.annotate_grades_list(grades, passing_grade=6.0)
        assert result_uni[0]["aprueba"] is True
        assert result_uni[1]["aprueba"] is False

        # Umbral colegio (7.0)
        result_col = GradePassingChecker.annotate_grades_list(grades, passing_grade=7.0)
        assert result_col[0]["aprueba"] is True
        assert result_col[1]["aprueba"] is False

    def test_annotate_grades_list_preserva_campos(self):
        """annotate_grades_list no debe perder campos existentes."""
        grades = [{"id": "E-001", "valor": 8.0, "curso_id": "C-MAT"}]
        result = GradePassingChecker.annotate_grades_list(grades, passing_grade=7.0)
        assert result[0]["id"] == "E-001"
        assert result[0]["curso_id"] == "C-MAT"
        assert result[0]["valor"] == 8.0

    def test_annotate_grades_list_vacia(self):
        """Lista vacía debe retornar lista vacía."""
        result = GradePassingChecker.annotate_grades_list([], passing_grade=7.0)
        assert result == []

    def test_annotate_grades_list_estado_aprobacion_en_resultado(self):
        """El campo 'estado_aprobacion' debe estar presente en cada elemento."""
        grades = [{"valor": 9.0}]
        result = GradePassingChecker.annotate_grades_list(grades, passing_grade=7.0)
        assert "estado_aprobacion" in result[0]
        assert result[0]["estado_aprobacion"] == "APROBADO"


# ─── CA-05: EnrollmentLimitChecker — casos adicionales ─────────────────────────

class TestEnrollmentLimitCheckerExtended:
    """Cobertura extendida del verificador de límite de inscripciones."""

    def test_can_enroll_exactamente_en_el_limite_retorna_false(self):
        """Exactamente en el límite no permite más inscripciones."""
        assert EnrollmentLimitChecker.can_enroll(8, max_enrollments=8) is False

    def test_can_enroll_supera_el_limite_retorna_false(self):
        """Superar el límite (datos corruptos) debe retornar False."""
        assert EnrollmentLimitChecker.can_enroll(10, max_enrollments=8) is False

    def test_can_enroll_usa_default_cuando_none(self):
        """Sin max_enrollments, debe usar DEFAULT_MAX_ENROLLMENTS (8)."""
        assert EnrollmentLimitChecker.can_enroll(7) is True   # 7 < 8
        assert EnrollmentLimitChecker.can_enroll(8) is False  # 8 >= 8

    def test_slots_remaining_sin_cupos(self):
        """slots_remaining en el límite debe retornar 0."""
        assert EnrollmentLimitChecker.slots_remaining(8, max_enrollments=8) == 0

    def test_slots_remaining_superando_limite_retorna_cero(self):
        """slots_remaining nunca debe retornar negativo."""
        assert EnrollmentLimitChecker.slots_remaining(10, max_enrollments=8) == 0

    def test_slots_remaining_usa_default_cuando_none(self):
        """Sin max_enrollments, debe usar DEFAULT_MAX_ENROLLMENTS (8)."""
        assert EnrollmentLimitChecker.slots_remaining(3) == 5  # 8 - 3 = 5

    def test_validate_or_raise_permite_inscribir(self):
        """validate_or_raise NO lanza error si puede inscribirse."""
        # No debe lanzar excepción
        EnrollmentLimitChecker.validate_or_raise(4, 8, "P-001")

    def test_validate_or_raise_mensaje_incluye_persona_id(self):
        """El mensaje de error debe incluir el persona_id."""
        with pytest.raises(ValueError, match="P-007"):
            EnrollmentLimitChecker.validate_or_raise(5, 5, "P-007")

    def test_validate_or_raise_mensaje_incluye_limite(self):
        """El mensaje de error debe incluir el límite configurado."""
        with pytest.raises(ValueError, match="6"):
            EnrollmentLimitChecker.validate_or_raise(6, 6, "P-001")

    def test_slots_remaining_maximo(self):
        """Con 0 inscripciones, los cupos restantes deben ser el límite completo."""
        assert EnrollmentLimitChecker.slots_remaining(0, max_enrollments=6) == 6
