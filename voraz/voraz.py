# Logíca de la solución voraz
"""
Algoritmo Voraz para Repartición Óptima de Cupos
================================================

Proyecto: Análisis y Diseño de Algoritmos II
Algoritmo: rocGreedy - Estrategia VDC (Variable Demand Criticality)
Fecha: 14 de Octubre 2025

Descripción:
    Implementa un algoritmo voraz que minimiza la insatisfacción promedio
    en la asignación de cupos de materias a estudiantes mediante una
    estrategia de priorización por demanda crítica variable.

Estrategia VDC:
    - Procesa solicitudes en orden de prioridad descendente
    - Asigna cupos según disponibilidad
    - Previene asignaciones duplicadas por estudiante
    - Optimiza la satisfacción global del sistema

"""

import sys
import os
from typing import Dict, List, Tuple

# Configuración de imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'input-output'))
from input import gamma

def calcular_insatisfaccion(asignadas, opciones_totales):
    """
    Calcula la insatisfacción de un estudiante según la fórmula del proyecto.
    
    Fórmula: (1 - k'/k) * (Σp_no_asignadas / γ(k))
    donde:
        - k = número total de materias solicitadas
        - k' = número de materias asignadas
        - γ(k) = 3k - 1
    
    Args:
        asignadas: Conjunto de códigos de materias asignadas
        opciones_totales: Lista de tuplas (codigo_materia, prioridad) solicitadas
        
    Returns:
        float: Valor de insatisfacción del estudiante
    """
    k = len(opciones_totales)
    if k == 0:
        return 0.0
    
    assigned_count = len(asignadas)
    unassigned_sum = sum(p for (c, p) in opciones_totales if c not in asignadas)
    
    return (1 - assigned_count / k) * (unassigned_sum / gamma(k))


def ordenar_por_prioridad(solicitudes):
    """
    Ordena solicitudes por prioridad en orden descendente usando bubble sort.
    
    Args:
        solicitudes: Lista de tuplas (prioridad, estudiante, curso_idx)
        
    Returns:
        Lista ordenada por prioridad (mayor a menor)
    """
    n = len(solicitudes)
    result = list(solicitudes)  # Crear copia
    
    for i in range(n):
        intercambiado = False
        for j in range(0, n - i - 1):
            if result[j][0] < result[j + 1][0]:
                result[j], result[j + 1] = result[j + 1], result[j]
                intercambiado = True
        if not intercambiado:
            break
    
    return result


def voraz(capacities, requests_by_student):
    """
    Algoritmo voraz para asignación de cupos.
    
    Estrategia: Procesar todas las solicitudes ordenadas por prioridad descendente,
    asignando cupos mientras haya disponibilidad.
    
    Args:
        capacities: Lista con capacidades de cada materia (por índice)
        requests_by_student: Diccionario {codigo_estudiante: [(idx_materia, prioridad), ...]}
        
    Returns:
        tuple: (asignaciones, insatisfaccion_promedio)
            - asignaciones: Dict[str, List[int]] - materias asignadas por estudiante (índices)
            - insatisfaccion_promedio: float
    """
    # Inicializar capacidades restantes y asignaciones
    remaining_caps = list(capacities)
    assignments = {student: [] for student in requests_by_student.keys()}
    
    # Recopilar todas las solicitudes con formato (prioridad, estudiante, idx_materia)
    all_requests = []
    for student_code, requests in requests_by_student.items():
        for course_idx, priority in requests:
            all_requests.append((priority, student_code, course_idx))
    
    # Ordenar por prioridad descendente
    all_requests = ordenar_por_prioridad(all_requests)
    
    # Asignar cupos según disponibilidad
    for priority, student_code, course_idx in all_requests:
        if remaining_caps[course_idx] > 0:
            # Verificar que el estudiante no tenga ya asignada esta materia
            if course_idx not in assignments[student_code]:
                assignments[student_code].append(course_idx)
                remaining_caps[course_idx] -= 1
    
    # Calcular insatisfacción promedio
    total_insatisfaction = 0.0
    num_students = len(requests_by_student)
    
    for student_code, requests in requests_by_student.items():
        assigned_set = set(assignments[student_code])
        student_insatisfaction = calcular_insatisfaccion(assigned_set, requests)
        total_insatisfaction += student_insatisfaction
    
    promedio = total_insatisfaction / num_students if num_students > 0 else 0.0
    
    return assignments, promedio


def rocGreedy(course_index_by_code, capacities, requests_by_student):
    """
    Wrapper para el algoritmo voraz.
    
    Convierte las asignaciones de índices a códigos de materia.
    
    Args:
        course_index_by_code: Diccionario que mapea códigos de materias a índices
        capacities: Lista de capacidades por materia (índice)
        requests_by_student: Diccionario de solicitudes por estudiante
        
    Returns:
        tuple: (asignaciones_con_codigos, insatisfaccion_promedio)
    """
    # Ejecutar el algoritmo voraz
    asignaciones, promedio = voraz(capacities, requests_by_student)
    
    # Invertir el mapeo de índices a códigos
    course_code_by_index = {idx: code for code, idx in course_index_by_code.items()}
    
    # Convertir las asignaciones de índices a códigos de materia
    asignaciones_con_codigos = {}
    for student, materias_idx in asignaciones.items():
        codigos = [course_code_by_index.get(idx, str(idx)) for idx in materias_idx]
        asignaciones_con_codigos[student] = codigos
    
    return asignaciones_con_codigos, promedio
