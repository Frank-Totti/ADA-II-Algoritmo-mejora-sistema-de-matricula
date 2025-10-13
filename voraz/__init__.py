# Módulo del algoritmo voraz para el proyecto "Repartición Óptima de Cupos"
# Algoritmo VDC (Variable Demand Criticality)

from .voraz import (
    rocV,
    inicializar_capacidades,
    calcular_insatisfaccion_fallback,
    generar_estadisticas,
    ordenar_solicitudes_por_prioridad,
    copiar_lista,
    sumar_elementos,
    contar_asignaciones,
    contar_solicitudes,
    contar_estudiantes_atendidos
)

__all__ = [
    'rocV',
    'inicializar_capacidades', 
    'calcular_insatisfaccion_fallback',
    'generar_estadisticas',
    'ordenar_solicitudes_por_prioridad',
    'copiar_lista',
    'sumar_elementos',
    'contar_asignaciones',
    'contar_solicitudes',
    'contar_estudiantes_atendidos'
]
