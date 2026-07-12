"""
Core Asset — EnrollmentLimitChecker (CA-05)

Verifica si un estudiante puede inscribirse en más cursos según el
límite configurado en el product_config.yaml del producto activo.

Este Core Asset previene over-enrollment: que un estudiante tome más
materias de las permitidas por la institución.

- Colegio Básico       → max_enrollments_per_period: 8
- Universidad Compleja → max_enrollments_per_period: 6
- Instituto Técnico    → max_enrollments_per_period: 5

El mismo EnrollmentRepository rechaza la inscripción N+1 si ya tiene
N activas — y N es diferente en cada institución sin cambiar el código.

Usado por:
  - features/enrollment/router.py → valida antes de POST /enrollment/
  - Cualquier proceso de inscripción masiva futuro
"""
from __future__ import annotations

from typing import Any, Dict, List


class EnrollmentLimitChecker:
    """Verifica el límite de inscripciones por período por estudiante.

    Todos los métodos son estáticos: no necesita instanciarse.
    El límite siempre viene del product_config.yaml — nunca hardcodeado.
    """

    # Default cuando el YAML no declara max_enrollments_per_period
    DEFAULT_MAX_ENROLLMENTS = 8

    @classmethod
    def can_enroll(
        cls,
        enrollments_in_period: int,
        max_enrollments: int | None = None,
    ) -> bool:
        """Determina si un estudiante puede inscribirse en un curso más.

        Args:
            enrollments_in_period: Número de matrículas activas del estudiante
                                   en el período actual.
            max_enrollments: Límite máximo del YAML del producto.
                             Si es None, usa el default (8).

        Returns:
            True si puede inscribirse (no ha alcanzado el límite).
            False si ya alcanzó o superó el límite.

        Ejemplo:
            >>> EnrollmentLimitChecker.can_enroll(5, max_enrollments=6)  # Universidad
            True
            >>> EnrollmentLimitChecker.can_enroll(5, max_enrollments=5)  # Técnico
            False
        """
        limit = max_enrollments if max_enrollments is not None else cls.DEFAULT_MAX_ENROLLMENTS
        return enrollments_in_period < limit

    @classmethod
    def validate_or_raise(
        cls,
        enrollments_in_period: int,
        max_enrollments: int | None = None,
        persona_id: str = "desconocido",
    ) -> None:
        """Valida el límite y lanza ValueError si se excede.

        Versión conveniente para usar en routers: valida y lanza
        error descriptivo si la inscripción no está permitida.

        Args:
            enrollments_in_period: Matrículas activas actuales del estudiante.
            max_enrollments: Límite del YAML del producto.
            persona_id: ID del estudiante para el mensaje de error.

        Raises:
            ValueError: Si el estudiante ya alcanzó el límite de inscripciones.

        Ejemplo:
            >>> EnrollmentLimitChecker.validate_or_raise(5, max_enrollments=5, persona_id="P-001")
            # Raises ValueError: "P-001 ya tiene 5 materias inscritas (limite: 5)"
        """
        limit = max_enrollments if max_enrollments is not None else cls.DEFAULT_MAX_ENROLLMENTS
        if not cls.can_enroll(enrollments_in_period, limit):
            raise ValueError(
                f"El estudiante '{persona_id}' ya tiene {enrollments_in_period} "
                f"materia(s) inscrita(s) en este periodo. "
                f"El limite configurado para este producto es {limit}."
            )

    @classmethod
    def slots_remaining(
        cls,
        enrollments_in_period: int,
        max_enrollments: int | None = None,
    ) -> int:
        """Calcula cuántos cupos de inscripción le quedan al estudiante.

        Args:
            enrollments_in_period: Matrículas activas actuales.
            max_enrollments: Límite del YAML.

        Returns:
            Número de cursos adicionales en que puede inscribirse. Mínimo 0.
        """
        limit = max_enrollments if max_enrollments is not None else cls.DEFAULT_MAX_ENROLLMENTS
        return max(0, limit - enrollments_in_period)
