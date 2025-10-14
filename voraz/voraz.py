# Logíca de la solución voraz
"""
Algoritmo Voraz para Repartición Óptima de Cupos
================================================

Proyecto: Análisis y Diseño de Algoritmos II
Algoritmo: rocV - Estrategia VDC (Variable Demand Criticality)
Fecha: 13 de Octubre 2025

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
# from utils_insatisfaccion import calcular_insatisfaccion  # No disponible, usar fallback
from input import parse_input_file

def ordenar_solicitudes_por_prioridad(lista_solicitudes: List[Tuple[int, str, int]]) -> List[Tuple[int, str, int]]:
    """
    Ordena las solicitudes por prioridad en orden descendente.
    
    Args:
        lista_solicitudes: Lista de tuplas (prioridad, estudiante, curso_idx)
        
    Returns:
        Lista ordenada por prioridad de mayor a menor
        
    Complejidad: O(n²)
    """
    n = len(lista_solicitudes)
    # Crear copia para preservar la lista original
    solicitudes_copia = []
    for item in lista_solicitudes:
        solicitudes_copia.append(item)
    
    # Algoritmo de ordenamiento burbuja
    for i in range(n):
        intercambio_realizado = False
        
        for j in range(0, n - i - 1):
            # Comparar prioridades (orden descendente)
            if solicitudes_copia[j][0] < solicitudes_copia[j + 1][0]:
                # Intercambiar elementos
                temp = solicitudes_copia[j]
                solicitudes_copia[j] = solicitudes_copia[j + 1]
                solicitudes_copia[j + 1] = temp
                intercambio_realizado = True
        
        # Optimización: terminar si la lista está ordenada
        if not intercambio_realizado:
            break
    
    return solicitudes_copia


def copiar_lista(lista_original: List[int]) -> List[int]:
    """
    Crea una copia independiente de una lista.
    
    Args:
        lista_original: Lista de enteros a copiar
        
    Returns:
        Nueva lista con los mismos elementos
    """
    lista_copia = []
    for elemento in lista_original:
        lista_copia.append(elemento)
    return lista_copia


def sumar_elementos(lista: List[int]) -> int:
    """
    Calcula la suma total de elementos en una lista.
    
    Args:
        lista: Lista de números enteros
        
    Returns:
        Suma total de todos los elementos
    """
    total = 0
    for elemento in lista:
        total += elemento
    return total


def contar_asignaciones(assignments: Dict[str, List[str]]) -> int:
    """
    Cuenta el total de asignaciones realizadas.
    
    Args:
        assignments: Diccionario de asignaciones por estudiante
        
    Returns:
        Número total de asignaciones realizadas
    """
    total_asignaciones = 0
    for estudiante in assignments:
        total_asignaciones += len(assignments[estudiante])
    return total_asignaciones


def contar_solicitudes(requests_by_student: Dict[str, List[Tuple[int, int]]]) -> int:
    """
    Cuenta el total de solicitudes realizadas.
    
    Args:
        requests_by_student: Diccionario de solicitudes por estudiante
        
    Returns:
        Número total de solicitudes realizadas
    """
    total_solicitudes = 0
    for estudiante in requests_by_student:
        total_solicitudes += len(requests_by_student[estudiante])
    return total_solicitudes


def contar_estudiantes_atendidos(assignments: Dict[str, List[str]]) -> int:
    """
    Cuenta cuántos estudiantes recibieron al menos una asignación.
    
    Args:
        assignments: Diccionario de asignaciones por estudiante
        
    Returns:
        Número de estudiantes que recibieron al menos una materia
    """
    estudiantes_atendidos = 0
    for estudiante in assignments:
        if len(assignments[estudiante]) > 0:
            estudiantes_atendidos += 1
    return estudiantes_atendidos


def inicializar_capacidades(capacities: List[int]) -> List[int]:
    """
    Inicializa las capacidades disponibles de las materias.
    
    Args:
        capacities: Lista con las capacidades iniciales de cada materia
        
    Returns:
        Lista con capacidades disponibles para asignación
    """
    return copiar_lista(capacities)


def calcular_insatisfaccion_fallback(assignments: Dict[str, List[str]], 
                                   requests_by_student: Dict[str, List[Tuple[int, int]]],
                                   course_code_by_index: Dict[int, str]) -> float:
    """
    Cálculo de insatisfacción como respaldo en caso de errores.
    
    Args:
        assignments: Diccionario de asignaciones por estudiante
        requests_by_student: Solicitudes por estudiante en formato índice
        course_code_by_index: Mapeo de índices a códigos de materia
        
    Returns:
        Insatisfacción promedio calculada
    """
    total_insatisfaction = 0.0
    total_students = len(requests_by_student)
    
    for student_code, requests in requests_by_student.items():
        assigned_courses = set(assignments.get(student_code, []))
        student_insatisfaction = 0.0
        
        # Sumar prioridades de materias no asignadas
        for course_idx, priority in requests:
            course_code = course_code_by_index[course_idx]
            if course_code not in assigned_courses:
                student_insatisfaction += priority
        
        total_insatisfaction += student_insatisfaction
    
    return total_insatisfaction / total_students if total_students > 0 else 0.0


def rocV(file_path: str) -> Tuple[Dict[str, List[str]], float]:
    """
    Algoritmo Voraz VDC (Variable Demand Criticality) para asignación óptima de cupos.
    
    Implementa una estrategia voraz que prioriza las solicitudes con mayor prioridad
    para minimizar la insatisfacción promedio en la asignación de cupos.
    
    Args:
        file_path: Ruta al archivo de entrada con formato del proyecto grupal
        
    Returns:
        Tupla con:
            - assignments: Diccionario {codigo_estudiante: [codigos_materias_asignadas]}
            - unsatisfaction: Valor de insatisfacción promedio (float)
    
    Raises:
        FileNotFoundError: Si el archivo de entrada no existe
        ValueError: Si hay errores en el formato o validación de datos
    """
    # FASE 1: Parsear archivo de entrada
    course_index_by_code, capacities, requests_by_student = parse_input_file(file_path)
    
    # FASE 2: Preparar estructuras de datos
    course_code_by_index = {idx: code for code, idx in course_index_by_code.items()}
    remaining_capacities = inicializar_capacidades(capacities)
    assignments = {student_code: [] for student_code in requests_by_student.keys()}
    
    # FASE 3: Recopilar todas las solicitudes
    all_requests = []
    for student_code, requests in requests_by_student.items():
        for course_idx, priority in requests:
            all_requests.append((priority, student_code, course_idx))
    
    # FASE 4: Aplicar estrategia voraz - ordenar por prioridad descendente (implementación manual)
    all_requests = ordenar_solicitudes_por_prioridad(all_requests)
    
    # FASE 5: Asignar cupos según disponibilidad
    for priority, student_code, course_idx in all_requests:
        if remaining_capacities[course_idx] > 0:
            course_code = course_code_by_index[course_idx]
            
            # Evitar asignaciones duplicadas por estudiante
            if course_code not in assignments[student_code]:
                assignments[student_code].append(course_code)
                remaining_capacities[course_idx] -= 1
    
    # FASE 6: Calcular insatisfacción resultante
    try:
        # Convertir a formato compatible para cálculo de insatisfacción
        E_format = []
        for student_code, requests in requests_by_student.items():
            student_requests = []
            for course_idx, priority in requests:
                course_code = course_code_by_index[course_idx]
                student_requests.append((course_code, priority))
            E_format.append((student_code, student_requests))
        
        # Usar directamente la función fallback ya que utils_insatisfaccion no existe
        unsatisfaction = calcular_insatisfaccion_fallback(
            assignments, requests_by_student, course_code_by_index
        )
    except Exception:
        # Cálculo alternativo en caso de error
        unsatisfaction = calcular_insatisfaccion_fallback(
            assignments, requests_by_student, course_code_by_index
        )
    
    return assignments, unsatisfaction


def generar_estadisticas(assignments: Dict[str, List[str]], 
                        capacities: List[int], 
                        requests_by_student: Dict[str, List[Tuple[int, int]]]) -> Dict[str, any]:
    """
    Genera estadísticas detalladas del resultado de la asignación.
    
    Args:
        assignments: Asignaciones realizadas por estudiante
        capacities: Capacidades totales por materia
        requests_by_student: Solicitudes originales de los estudiantes
    
    Returns:
        Diccionario con estadísticas de la asignación
    """
    total_assignments = contar_asignaciones(assignments)
    total_capacity = sumar_elementos(capacities)
    total_requests = contar_solicitudes(requests_by_student)
    
    return {
        'total_asignaciones': total_assignments,
        'capacidad_total': total_capacity,
        'total_solicitudes': total_requests,
        'eficiencia_uso': (total_assignments / total_capacity) * 100 if total_capacity > 0 else 0,
        'tasa_satisfaccion': (total_assignments / total_requests) * 100 if total_requests > 0 else 0,
        'estudiantes_atendidos': contar_estudiantes_atendidos(assignments)
    }
