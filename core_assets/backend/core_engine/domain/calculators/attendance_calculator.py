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

    # Defaults cuando el YAML no declara attendance_min_percentage
    # Regla de negocio del dominio académico ecuatoriano (Ministerio de Educación)
    DEFAULT_THRESHOLD_APPROVED = 80.0
    DEFAULT_THRESHOLD_AT_RISK  = 70.0

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
    def status(
        cls,
        percentage: float,
        threshold_approved: float | None = None,
        threshold_at_risk: float | None = None,
    ) -> str:
        """Determina el estado académico según el porcentaje de asistencia.

        Los umbrales vienen del product_config.yaml a través del router.
        Si el producto no los declara, se usan los defaults del dominio
        académico ecuatoriano (80% / 70%).

        Args:
            percentage: Porcentaje de asistencia (0.0 - 100.0).
            threshold_approved: % mínimo para estado APROBADO (del YAML).
                                Si es None, usa DEFAULT_THRESHOLD_APPROVED (80%).
            threshold_at_risk: % mínimo para estado EN_RIESGO (del YAML).
                               Si es None, usa DEFAULT_THRESHOLD_AT_RISK (70%).

        Returns:
            - "APROBADO"          si percentage >= threshold_approved
            - "EN_RIESGO"         si percentage >= threshold_at_risk (pero < approved)
            - "REPROBADO_FALTA"   si percentage < threshold_at_risk

        Ejemplo:
            # Con configuración de colegio (threshold_approved=80):
            >>> AttendanceCalculator.status(90.0, threshold_approved=80)
            'APROBADO'
            # Con configuración de universidad (threshold_approved=75):
            >>> AttendanceCalculator.status(77.0, threshold_approved=75)
            'APROBADO'
            >>> AttendanceCalculator.status(77.0, threshold_approved=80)
            'EN_RIESGO'
        """
        t_approved = threshold_approved if threshold_approved is not None else cls.DEFAULT_THRESHOLD_APPROVED
        t_at_risk  = threshold_at_risk  if threshold_at_risk  is not None else cls.DEFAULT_THRESHOLD_AT_RISK

        if percentage >= t_approved:
            return "APROBADO"
        elif percentage >= t_at_risk:
            return "EN_RIESGO"
        else:
            return "REPROBADO_FALTA"


    @classmethod
    def summarize(
        cls,
        records: List[Dict[str, Any]],
        threshold_approved: float | None = None,
        threshold_at_risk: float | None = None,
    ) -> Dict[str, Any]:
        """Calcula un resumen global de una lista de registros de asistencia.

        Args:
            records: Lista de dicts de AttendanceRepository con campo `presente`.
            threshold_approved: % mínimo para APROBADO (del YAML del producto).
            threshold_at_risk:  % mínimo para EN_RIESGO (del YAML del producto).

        Returns:
            Dict con total_registros, total_presentes, total_ausentes,
            porcentaje_asistencia, estado y los umbrales aplicados.
        """
        total = len(records)
        presentes = sum(1 for r in records if r.get("presente", False))
        ausentes = total - presentes
        pct = cls.percentage(presentes, total)
        t_app = threshold_approved if threshold_approved is not None else cls.DEFAULT_THRESHOLD_APPROVED
        t_risk = threshold_at_risk if threshold_at_risk is not None else cls.DEFAULT_THRESHOLD_AT_RISK
        return {
            "total_registros": total,
            "total_presentes": presentes,
            "total_ausentes": ausentes,
            "porcentaje_asistencia": pct,
            "estado": cls.status(pct, t_app, t_risk),
            "umbral_aprobado": t_app,
            "umbral_riesgo": t_risk,
        }

    @classmethod
    def summarize_by_persona(
        cls,
        records: List[Dict[str, Any]],
        threshold_approved: float | None = None,
        threshold_at_risk: float | None = None,
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
