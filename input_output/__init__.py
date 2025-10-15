"""
Módulo de entrada/salida para el sistema de asignación de cupos
"""

from .input import (
    parse_input_file,
    gamma,
    funcionGamma,
    calcular_insatisfaccion_individual,
    calcular_insatisfaccion_general,
    generar_subconjuntos,
    subconjuntos,
    maximaPrioridadPermitida,
    restriccionMaximoSumaPrioridades
)

__all__ = [
    'parse_input_file',
    'gamma',
    'funcionGamma',
    'calcular_insatisfaccion_individual',
    'calcular_insatisfaccion_general',
    'generar_subconjuntos',
    'subconjuntos',
    'maximaPrioridadPermitida',
    'restriccionMaximoSumaPrioridades'
]