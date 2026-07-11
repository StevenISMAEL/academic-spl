"""
Core Asset — GradeScaleConverter (CA-02)

Convierte calificaciones numéricas a la escala de presentación
configurada por el producto derivado (numeric o literal).

Este Core Asset es la prueba más visible de que el SPL es real:
el MISMO código de grading/router.py produce DISTINTA salida según
el `evaluation_scale` del product_config.yaml, SIN condicionales
sobre el nombre del producto.

- Colegio Básico  (evaluation_scale: "literal") → 8.5 → "Muy Bueno"
- Universidad     (evaluation_scale: "numeric") → 8.5 → 8.5

El Core Asset no sabe que uno es un colegio y el otro una universidad.
Solo recibe el parámetro `scale` que proviene del YAML.

Usado por:
  - features/grading/router.py   → al devolver la lista de calificaciones
  - Cualquier reporte futuro que necesite mostrar notas en la escala correcta

Escala literal (basada en el sistema de evaluación cualitativa común
en Ecuador para educación básica):
  - 9.0 - 10.0 → Sobresaliente (S)
  - 7.0 -  8.9 → Muy Bueno (MB)
  - 5.0 -  6.9 → Bueno (B)
  - 3.0 -  4.9 → Regular (R)
  - 0.0 -  2.9 → Insuficiente (I)
"""
from __future__ import annotations

from typing import Union


class GradeScaleConverter:
    """Convierte calificaciones entre escala numérica y literal.

    Todos los métodos son estáticos: no necesita instanciarse.
    """

    # Tabla de conversión numérico → literal
    # Tuplas: (mínimo_inclusive, máximo_inclusive, etiqueta)
    _LITERAL_TABLE = [
        (9.0, 10.0, "Sobresaliente"),
        (7.0,  8.9, "Muy Bueno"),
        (5.0,  6.9, "Bueno"),
        (3.0,  4.9, "Regular"),
        (0.0,  2.9, "Insuficiente"),
    ]

    # Escalas soportadas (deben coincidir con el enum del config_schema.json)
    SCALE_NUMERIC = "numeric"
    SCALE_LITERAL = "literal"

    @classmethod
    def to_display(cls, valor: float, scale: str) -> Union[float, str]:
        """Convierte un valor numérico a la representación de la escala activa.

        Este es el método principal del Core Asset. El router lo llama
        con el `scale` que leyó del YAML — nunca necesita saber si es
        colegio o universidad.

        Args:
            valor: Calificación numérica (0.0 – 10.0).
            scale: Escala de presentación. Valores válidos:
                   - "numeric" → retorna el número tal cual
                   - "literal" → retorna la etiqueta cualitativa

        Returns:
            El valor numérico (float) si scale="numeric",
            o la etiqueta literal (str) si scale="literal".

        Raises:
            ValueError: Si scale no es un valor soportado.

        Ejemplo:
            >>> GradeScaleConverter.to_display(8.5, "literal")
            'Muy Bueno'
            >>> GradeScaleConverter.to_display(8.5, "numeric")
            8.5
            >>> GradeScaleConverter.to_display(9.5, "literal")
            'Sobresaliente'
        """
        if scale == cls.SCALE_NUMERIC:
            return valor

        if scale == cls.SCALE_LITERAL:
            return cls.to_literal(valor)

        raise ValueError(
            f"Escala '{scale}' no soportada. "
            f"Valores validos: '{cls.SCALE_NUMERIC}', '{cls.SCALE_LITERAL}'."
        )

    @classmethod
    def to_literal(cls, valor: float) -> str:
        """Convierte un valor numérico directamente a su etiqueta literal.

        Args:
            valor: Calificación numérica (0.0 – 10.0).

        Returns:
            Etiqueta cualitativa correspondiente.
        """
        for minimo, maximo, etiqueta in cls._LITERAL_TABLE:
            if minimo <= valor <= maximo:
                return etiqueta
        # Valor fuera de rango: retornar el número como string para no perder info
        return str(round(valor, 2))

    @classmethod
    def convert_grades_list(
        cls, grades: list, scale: str, valor_field: str = "valor"
    ) -> list:
        """Convierte una lista completa de calificaciones a la escala activa.

        Transforma el campo `valor_field` de cada dict en la lista,
        agregando el campo `valor_display` con la versión en escala.
        El campo `valor` original se conserva para cálculos internos.

        Args:
            grades: Lista de dicts con calificaciones (de GradeRepository).
            scale: Escala activa del producto ("numeric" o "literal").
            valor_field: Nombre del campo numérico en cada dict.

        Returns:
            Nueva lista con `valor_display` agregado a cada elemento.

        Ejemplo:
            >>> grades = [{"id": "1", "valor": 8.5, "persona_id": "P-001"}]
            >>> GradeScaleConverter.convert_grades_list(grades, "literal")
            [{"id": "1", "valor": 8.5, "valor_display": "Muy Bueno", "persona_id": "P-001"}]
        """
        result = []
        for grade in grades:
            converted = dict(grade)
            converted["valor_display"] = cls.to_display(grade[valor_field], scale)
            result.append(converted)
        return result
