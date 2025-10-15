""""
Módulo para manejar la entrada de datos en el proyecto de asignación de cursos.
"""


import os
from typing import Dict, List, Tuple
import itertools


# -------------- Restricciones -----------------
def funcionGamma(X):
    """Priority cap function: γ(x) = 3x - 1."""
    return 3*X-1

# Alias para compatibilidad
gamma = funcionGamma


def maximaPrioridadPermitida(prioridades, estudiantes):
    """ 
    Verifica si todas las prioridades de los estudiantes están dentro del rango permitido.
    Si alguna prioridad está fuera del rango, retorna True (restricción violada).
    """
    min_prioridad = min(prioridades)
    max_prioridad = max(prioridades)
    
    for estudiante, preferencias in estudiantes.items():
        for _, prioridad in preferencias:
            if prioridad < min_prioridad or prioridad > max_prioridad:
                print(f"Prioridad {prioridad} de {estudiante} está fuera del rango permitido.")
                return True
    return False


def restriccionMaximoSumaPrioridades(estudiantes):
    """ 
    Verifica si algún estudiante excede la prioridad máxima permitida.
    Si algún estudiante excede, retorna True (restricción violada).
    """
    for estudiante, preferencias in estudiantes.items():
        suma = sum(prioridad for _, prioridad in preferencias)
        gamma = funcionGamma(len(preferencias))
        if suma > gamma:
            return True
    return False


# ----------------- Algoritmos -----------------
def subconjuntos(materias):
    """
    Genera todos los subconjuntos posibles de una lista de materias.
    Args:
        materias: lista de materias (pueden ser índices o códigos)
    Returns:
        lista de listas, cada una representando un subconjunto posible
    """
    resultado = []
    for r in range(len(materias) + 1):
        for combo in itertools.combinations(materias, r):
            resultado.append(list(combo))
    return resultado


def generar_subconjuntos(opciones):
    """
    Genera todos los subconjuntos posibles de materias solicitadas por un estudiante.
    Args:
        opciones: lista de tuplas (materia_idx, prioridad)
    Yields:
            lista de tuplas (materia_idx, prioridad) representando un subconjunto posible
    """
    n = len(opciones)
    for r in range(n + 1):
        for comb in itertools.combinations(opciones, r):
            yield comb
            
# -------------- Input/Output -----------------
def parse_input_file(path: str):
    """
    Parse a plain-text input file for the course-allocation project.

    Returns:
        - course_index_by_code (Dict[str, int]):
            Maps course code (e.g., "1001") to its index (0..k-1).
        - capacities (List[int]):
            capacities[i] is the capacity for the course at index i.
        - requests_by_student (Dict[str, List[Tuple[int, int]]]):
            For each student code, a list of (course_idx, priority) pairs.

    Validations performed (inline):
        1) For each student, number of requests s must be in [1..7].
        2) A student must not request the same course more than once.
        3) Each priority must be in [1..5].
        4) For each student, sum of priorities must satisfy sum ≤ γ(s) = 3*s - 1.

    """
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    idx = 0
    num_courses = int(lines[idx]); idx += 1

    course_index_by_code: Dict[str, int] = {}
    capacities: List[int] = []
    for i in range(num_courses):
        code, capacity = lines[idx].split(',')
        course_index_by_code[code] = i
        capacities.append(int(capacity))
        idx += 1

    num_students = int(lines[idx]); idx += 1  # kept for format parity, not otherwise used

    requests_by_student: Dict[str, List[Tuple[int, int]]] = {}
    while idx < len(lines):
        student_code, n_requests_str = lines[idx].split(',')
        idx += 1

        # CHECK 1: number of requests s in [1..7]
        s = int(n_requests_str)
        if not (1 <= s <= 7):
            raise ValueError(f"Student {student_code}: invalid number of requests: {s} (expected 1..7)")

        requests_by_student[student_code] = []
        priority_sum = 0  # for γ(s)
        seen_course_indices = set()  # to forbid duplicates for this student

        for _ in range(s):
            course_code, priority_str = lines[idx].split(',')
            idx += 1

            # map to course index (assumes course exists in the header)
            course_idx = course_index_by_code[course_code]

            # CHECK 2: no duplicated course requests per student
            if course_idx in seen_course_indices:
                raise ValueError(
                    f"Student {student_code}: repeated course request for {course_code}"
                )
            seen_course_indices.add(course_idx)

            # CHECK 3: priority in [1..5]
            p = int(priority_str)
            if not (1 <= p <= 5):
                raise ValueError(
                    f"Student {student_code}: priority out of range (1..5) for course {course_code}: {p}"
                )

            requests_by_student[student_code].append((course_idx, p))
            priority_sum += p

        # CHECK 4: sum of priorities ≤ γ(s) = 3s - 1
        if priority_sum > funcionGamma(s):
            raise ValueError(
                f"Student {student_code}: priority sum {priority_sum} exceeds γ({s})={funcionGamma(s)}"
            )

    return course_index_by_code, capacities, requests_by_student


# -------------- Cálculo de insatisfacción -----------------
def calcular_insatisfaccion_individual(asignadas, opciones_totales):
    """
    Calcula la insatisfacción de un solo estudiante.
    
    Args:
        asignadas: lista de tuplas (curso_idx, prioridad) asignadas al estudiante
        opciones_totales: lista de tuplas (curso_idx, prioridad) solicitadas por el estudiante
    
    Returns:
        float: nivel de insatisfacción del estudiante
    """
    k = len(opciones_totales)
    if k == 0:
        return 0.0
    
    assigned_count = len(asignadas)
    assigned_courses = {c for (c, _) in asignadas}
    unassigned_sum = sum(p for (c, p) in opciones_totales if c not in assigned_courses)
    
    return (1 - assigned_count / k) * (unassigned_sum / funcionGamma(k))


def calcular_insatisfaccion_general(solucion, estudiantes):
    """
    Calcula el nivel de insatisfacción general de toda la solución.
    
    Args:
        solucion: dict {estudiante: [lista de índices de materias asignadas]}
        estudiantes: dict {estudiante: [(materia_idx, prioridad), ...]}
    
    Returns:
        float: promedio de insatisfacción de todos los estudiantes
    """
    valor_insatisfaccion = 0
    
    for estudiante in solucion:
        materias_solicitadas = estudiantes[estudiante]  # lista de (materia, prioridad)
        materias_asignadas_idx = solucion[estudiante]   # lista de índices de materias
        
        # Convertir índices a tuplas (idx, prioridad) para usar la función individual
        asignadas = [(idx, p) for idx, p in materias_solicitadas if idx in materias_asignadas_idx]
        
        # Usar la función individual
        fj = calcular_insatisfaccion_individual(asignadas, materias_solicitadas)
        valor_insatisfaccion += fj
    
    # insatisfacción general (promedio)
    insatisfaccion_general = valor_insatisfaccion / len(estudiantes) if len(estudiantes) > 0 else 0.0
    
    return insatisfaccion_general