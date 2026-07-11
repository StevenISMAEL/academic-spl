"""
Core Asset — AttendanceCalculator (CA-03)

Calcula estadísticas de asistencia para una colección de registros.

Este Core Asset convierte datos crudos de asistencia (lista de presente/ausente)
en información útil: porcentaje, estado de riesgo, resumen por persona.

No sabe qué producto lo usa. Recibe listas de dicts (de AttendanceRepository)
y devuelve estadísticas. El umbral de riesgo podría en el futuro ser
configurable por el YAML del producto — por ahora usa el estándar educativo
ecuatoriano del 75% mínimo de asistencia.

Usado por:
  - features/attendance/router.py  → agrega estadísticas al GET /attendance/
  - Cualquier reporte futuro de asistencia
  - Potencialmente por enrollment para verificar si un estudiante puede rendir examen

Regla de negocio del dominio académico ecuatoriano:
  - >= 80% asistencia → Estado APROBADO (puede rendir evaluaciones)
  - 70% - 79%         → Estado EN RIESGO (advertencia)
  - < 70%             → Estado REPROBADO POR FALTA (pierde la materia automáticamente)
"""
from __future__ import annotations

from typing import Any, Dict, List


class AttendanceCalculator:
    """Calcula estadísticas de asistencia académica.

    Todos los métodos son estáticos: no necesita instanciarse.
    """

    # Umbrales de riesgo — regla de negocio del dominio académico
    THRESHOLD_APPROVED = 80.0   # >= 80% → aprobado en asistencia
    THRESHOLD_AT_RISK  = 70.0   # 70-79% → en riesgo
    # < 70% → reprobado por falta (pierde la materia)

    @classmethod
    def percentage(cls, presentes: int, total: int) -> float:
        """Calcula el porcentaje de asistencia.

        Args:
            presentes: Número de clases a las que asistió.
            total: Total de clases del período.

        Returns:
            Porcentaje de asistencia (0.0 - 100.0).
            Retorna 0.0 si total es 0 (división por cero segura).

        Ejemplo:
            >>> AttendanceCalculator.percentage(18, 20)
            90.0
            >>> AttendanceCalculator.percentage(14, 20)
            70.0
        """
        if total == 0:
            return 0.0
        return round((presentes / total) * 100, 2)

    @classmethod
    def status(cls, percentage: float) -> str:
        """Determina el estado académico según el porcentaje de asistencia.

        Args:
            percentage: Porcentaje de asistencia (0.0 - 100.0).

        Returns:
            - "APROBADO"          si >= 80%
            - "EN_RIESGO"         si entre 70% y 79.99%
            - "REPROBADO_FALTA"   si < 70%

        Ejemplo:
            >>> AttendanceCalculator.status(90.0)
            'APROBADO'
            >>> AttendanceCalculator.status(75.0)
            'EN_RIESGO'
            >>> AttendanceCalculator.status(65.0)
            'REPROBADO_FALTA'
        """
        if percentage >= cls.THRESHOLD_APPROVED:
            return "APROBADO"
        elif percentage >= cls.THRESHOLD_AT_RISK:
            return "EN_RIESGO"
        else:
            return "REPROBADO_FALTA"

    @classmethod
    def summarize(cls, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcula un resumen global de una lista de registros de asistencia.

        Args:
            records: Lista de dicts de AttendanceRepository. Cada dict
                     debe tener al menos el campo `presente` (bool).

        Returns:
            Dict con:
            - total_registros: total de clases registradas
            - total_presentes: clases con asistencia
            - total_ausentes: clases sin asistencia
            - porcentaje_asistencia: float
            - estado: "APROBADO" | "EN_RIESGO" | "REPROBADO_FALTA"

        Ejemplo:
            >>> records = [{"presente": True}, {"presente": False}, {"presente": True}]
            >>> AttendanceCalculator.summarize(records)
            {"total_registros": 3, "total_presentes": 2, "total_ausentes": 1,
             "porcentaje_asistencia": 66.67, "estado": "REPROBADO_FALTA"}
        """
        total = len(records)
        presentes = sum(1 for r in records if r.get("presente", False))
        ausentes = total - presentes
        pct = cls.percentage(presentes, total)
        return {
            "total_registros": total,
            "total_presentes": presentes,
            "total_ausentes": ausentes,
            "porcentaje_asistencia": pct,
            "estado": cls.status(pct),
        }

    @classmethod
    def summarize_by_persona(
        cls, records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Agrupa y resume la asistencia por persona.

        Útil para la vista de un curso completo: cuánto asistió cada
        estudiante al mismo tiempo.

        Args:
            records: Lista de dicts de AttendanceRepository con campos
                     `persona_id` y `presente`.

        Returns:
            Lista de resúmenes, uno por persona encontrada en los registros.
            Ordenada por porcentaje de asistencia ascendente (primero los en riesgo).
        """
        # Agrupar registros por persona
        by_persona: Dict[str, List[Dict[str, Any]]] = {}
        for record in records:
            pid = record["persona_id"]
            by_persona.setdefault(pid, []).append(record)

        # Calcular resumen por persona
        summaries = []
        for persona_id, persona_records in by_persona.items():
            summary = cls.summarize(persona_records)
            summary["persona_id"] = persona_id
            summaries.append(summary)

        # Ordenar: primero los que tienen menor asistencia (más en riesgo)
        summaries.sort(key=lambda x: x["porcentaje_asistencia"])
        return summaries
