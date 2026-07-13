"""
Tests unitarios de los 5 Core Assets (COR-25 parte 1)

Estos tests verifican la lógica de negocio de los Core Assets sin necesidad
de levantar FastAPI ni base de datos. Son tests puros de Python.
"""
import pytest

from core_assets.backend.core_engine.domain.validators.cedula_validator import CedulaValidator
from core_assets.backend.core_engine.domain.calculators.grade_scale_converter import GradeScaleConverter
from core_assets.backend.core_engine.domain.calculators.attendance_calculator import AttendanceCalculator
from core_assets.backend.core_engine.domain.calculators.grade_passing_checker import GradePassingChecker
from core_assets.backend.core_engine.domain.calculators.enrollment_limit_checker import EnrollmentLimitChecker


# CA-01: CedulaValidator
def test_cedula_valida():
    assert CedulaValidator.validate("1713175071") is True


def test_cedula_invalida():
    assert CedulaValidator.validate("1234567890") is False


def test_cedula_longitud_incorrecta():
    assert CedulaValidator.validate("123") is False


def test_cedula_validate_or_raise_invalida():
    with pytest.raises(ValueError):
        CedulaValidator.validate_or_raise("1234567890")


# CA-02: GradeScaleConverter
def test_grade_literal_sobresaliente():
    assert GradeScaleConverter.to_display(9.5, "literal") == "Sobresaliente"


def test_grade_literal_muy_bueno():
    assert GradeScaleConverter.to_display(8.5, "literal") == "Muy Bueno"


def test_grade_literal_regular():
    assert GradeScaleConverter.to_display(4.0, "literal") == "Regular"


def test_grade_numeric():
    assert GradeScaleConverter.to_display(8.5, "numeric") == 8.5


# CA-03: AttendanceCalculator (ahora con umbrales configurables)
def test_attendance_percentage():
    assert AttendanceCalculator.percentage(18, 20) == 90.0


def test_attendance_approved_colegio():
    assert AttendanceCalculator.status(85.0, threshold_approved=80.0) == "APROBADO"


def test_attendance_en_riesgo_colegio():
    assert AttendanceCalculator.status(77.0, threshold_approved=80.0) == "EN_RIESGO"


def test_attendance_approved_universidad():
    assert AttendanceCalculator.status(77.0, threshold_approved=75.0) == "APROBADO"


def test_attendance_umbral_en_resumen():
    records = [{"presente": True}] * 8 + [{"presente": False}] * 2
    result = AttendanceCalculator.summarize(records, threshold_approved=80.0)
    assert result["umbral_aprobado"] == 80.0
    assert result["estado"] == "APROBADO"


# CA-04: GradePassingChecker
def test_grade_passing_universidad():
    assert GradePassingChecker.passes(6.5, passing_grade=6.0) is True


def test_grade_failing_colegio():
    assert GradePassingChecker.passes(6.5, passing_grade=7.0) is False


def test_grade_status():
    assert GradePassingChecker.status(9.0, passing_grade=7.0) == "APROBADO"


def test_grade_annotate_list():
    result = GradePassingChecker.annotate_grades_list([{"valor": 6.5}], passing_grade=7.0)
    assert result[0]["aprueba"] is False
    assert result[0]["estado_aprobacion"] == "REPROBADO"


# CA-05: EnrollmentLimitChecker
def test_enrollment_can_enroll():
    assert EnrollmentLimitChecker.can_enroll(5, max_enrollments=6) is True


def test_enrollment_at_limit():
    assert EnrollmentLimitChecker.can_enroll(5, max_enrollments=5) is False


def test_enrollment_slots_remaining():
    assert EnrollmentLimitChecker.slots_remaining(3, max_enrollments=8) == 5


def test_enrollment_validate_or_raise():
    with pytest.raises(ValueError):
        EnrollmentLimitChecker.validate_or_raise(5, 5, "P-001")
