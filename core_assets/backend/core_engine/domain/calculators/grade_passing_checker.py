"""
Core Asset — GradePassingChecker (CA-04)

Determina si una calificación aprueba o reprueba según la nota mínima
configurada en el product_config.yaml del producto activo.

Este Core Asset resuelve un problema que antes estaba silenciado:
el mismo GradeRepository devuelve notas a todos los productos, pero
¿qué significa "aprobado" en cada uno?

- Colegio Básico       → passing_grade: 7.0  → nota 6.5 = REPROBADO
- Universidad Compleja → passing_grade: 6.0  → nota 6.5 = APROBADO
- Instituto Técnico    → passing_grade: 7.0  → nota 6.5 = REPROBADO

El MISMO valor 6.5 tiene distinto significado según el producto.
Este Core Asset encapsula esa regla de dominio sin conocer el producto.

Usado por:
  - features/grading/router.py  → agrega campo "aprueba" a cada nota
  - Cualquier reporte futuro de rendimiento académico
"""
from __future__ import annotations

from typing import Any, Dict, List


class GradePassingChecker:
    """Evalúa si una calificación supera el umbral mínimo del producto.

    Todos los métodos son estáticos: no necesita instanciarse.
    El passing_grade siempre viene del product_config.yaml — nunca hardcodeado.
    """

    # Default usado cuando el YAML no declara passing_grade
    DEFAULT_PASSING_GRADE = 7.0

    @classmethod
    def passes(cls, valor: float, passing_grade: float | None = None) -> bool:
        """Determina si una nota aprueba.

        Args:
            valor: Calificación numérica a evaluar.
            passing_grade: Nota mínima de aprobación tomada del YAML del producto.
                           Si es None, usa el default (7.0).

        Returns:
            True si valor >= passing_grade. False si reprueba.

        Ejemplo:
            >>> GradePassingChecker.passes(6.5, passing_grade=6.0)  # Universidad
            True
            >>> GradePassingChecker.passes(6.5, passing_grade=7.0)  # Colegio
            False
        """
        threshold = passing_grade if passing_grade is not None else cls.DEFAULT_PASSING_GRADE
        return valor >= threshold

    @classmethod
    def status(cls, valor: float, passing_grade: float | None = None) -> str:
        """Devuelve el estado de aprobación como cadena de texto.

        Args:
            valor: Calificación numérica.
            passing_grade: Nota mínima de aprobación del YAML.

        Returns:
            "APROBADO" o "REPROBADO"

        Ejemplo:
            >>> GradePassingChecker.status(8.5, passing_grade=7.0)
            'APROBADO'
            >>> GradePassingChecker.status(5.0, passing_grade=7.0)
            'REPROBADO'
        """
        return "APROBADO" if cls.passes(valor, passing_grade) else "REPROBADO"

    @classmethod
    def annotate_grades_list(
        cls,
        grades: List[Dict[str, Any]],
        passing_grade: float | None = None,
        valor_field: str = "valor",
    ) -> List[Dict[str, Any]]:
        """Agrega el campo `aprueba` y `estado_aprobacion` a cada nota en la lista.

        Usado por grading/router.py para enriquecer la respuesta sin lógica
        de negocio en el router mismo.

        Args:
            grades: Lista de dicts de GradeRepository.
            passing_grade: Nota mínima de aprobación del YAML del producto.
            valor_field: Nombre del campo numérico en el dict.

        Returns:
            Lista con dos campos nuevos por elemento:
            - `aprueba` (bool): True si la nota pasa el umbral
            - `estado_aprobacion` (str): "APROBADO" o "REPROBADO"

        Ejemplo:
            >>> grades = [{"id": "1", "valor": 6.5}]
            >>> GradePassingChecker.annotate_grades_list(grades, passing_grade=6.0)
            [{"id": "1", "valor": 6.5, "aprueba": True, "estado_aprobacion": "APROBADO"}]
        """
        result = []
        for grade in grades:
            annotated = dict(grade)
            valor = grade.get(valor_field, 0)
            annotated["aprueba"] = cls.passes(valor, passing_grade)
            annotated["estado_aprobacion"] = cls.status(valor, passing_grade)
            result.append(annotated)
        return result
