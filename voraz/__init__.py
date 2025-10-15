# Módulo del algoritmo voraz para el proyecto "Repartición Óptima de Cupos"
# Algoritmo VDC (Variable Demand Criticality)

from .voraz import (
    rocV,
    voraz,
    calcular_insatisfaccion,
    ordenar_por_prioridad
)

__all__ = [
    'rocV',
    'voraz',
    'calcular_insatisfaccion',
    'ordenar_por_prioridad'
]
