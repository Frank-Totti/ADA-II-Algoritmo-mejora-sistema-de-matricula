"""
Algoritmo de Programación Dinámica para Repartición Óptima de Cupos
==================================================================

Proyecto: Análisis y Diseño de Algoritmos II
Algoritmo: rocDP - Estrategia de Memoización con Subestructura Óptima
Fecha: 14 de Octubre 2025

Descripción:
    Implementa un algoritmo de programación dinámica que minimiza la
    insatisfacción promedio en la asignación de cupos de materias a
    estudiantes mediante exploración exhaustiva optimizada con memoización.

Estrategia de Programación Dinámica:
    - Explora todas las combinaciones posibles de asignaciones
    - Utiliza memoización (LRU cache) para evitar recalcular estados
    - Mantiene tabla de decisiones óptimas por estado
    - Construye solución óptima mediante backtracking
    - Garantiza la solución de mínima insatisfacción global
    - Complejidad optimizada mediante subestructura óptima
"""

from functools import lru_cache # permite guardar en cache la información del estado de cada recursión que se haga
from input_output import generar_subconjuntos, calcular_insatisfaccion_individual


def dynamic(capacities, requests_by_student, stop_event=None):
    """
    Algoritmo de programación dinámica con memoización para asignación óptima de cupos.
    Explora exhaustivamente todas las combinaciones posibles de asignaciones y utiliza
    LRU cache para evitar recalcular estados ya visitados.
    
    Args:
        capacities: Lista de capacidades disponibles por materia (índice)
        requests_by_student: Diccionario de solicitudes por estudiante {estudiante: [(materia_idx, prioridad), ...]}
        stop_event: threading.Event para cancelación cooperativa durante la ejecución (opcional)
    
    Returns:
        tuple: (asignaciones, insatisfaccion_promedio)
            - asignaciones: dict {estudiante: [lista de índices de materias asignadas]}
            - insatisfaccion_promedio: float con la insatisfacción promedio de la solución óptima
    """

    # Hacemos inmutables las solicitudes (para memoización)
    requests_immutable = {s: tuple(reqs) for s, reqs in requests_by_student.items()}
    students = list(requests_immutable.keys())
    initial_caps = tuple(capacities)

    # Diccionario para guardar las decisiones óptimas por estado (i, caps)
    choice = {}

    # Mejor total conocido desde el estado raíz (i=0, caps iniciales)
    root_best_total = [float("inf")]  # lista para mutabilidad en cierre

    def baseline_from(i: int) -> float:
        """Costo total si desde el estudiante i no se asigna ninguna materia (subconjunto vacío)."""
        total = 0.0
        for j in range(i, len(students)):
            opciones_j = requests_immutable[students[j]]
            total += calcular_insatisfaccion((), opciones_j)
        return total

    # inicializar mejor parcial como baseline desde la raíz
    root_best_total[0] = baseline_from(0)

    @lru_cache(maxsize=None)
    def dp(i, caps):
        # Cancelación cooperativa: devuelve mejor total conocido
        if stop_event is not None and getattr(stop_event, 'is_set', None) and stop_event.is_set():
            return root_best_total[0]
        if i == len(students):
            return 0.0

        student = students[i]
        opciones = requests_immutable[student]
        best = float("inf")
        best_subset = ()

        for subset in generar_subconjuntos(opciones):
            # Cancelación durante iteración
            if stop_event is not None and getattr(stop_event, 'is_set', None) and stop_event.is_set():
                return root_best_total[0]
            # verifica si hay cupos en las materias
            new_caps = list(caps)
            feasible = True
            for (c, _) in subset:
                if new_caps[c] <= 0:
                    feasible = False
                    break
                new_caps[c] -= 1
            if not feasible:
                continue

            f_j = calcular_insatisfaccion_individual(subset, opciones)
            total = f_j + dp(i + 1, tuple(new_caps))

            if total < best:
                best = total
                best_subset = subset
                # Guardar mejor hasta ahora para este estado
                choice[(i, caps)] = best_subset
                # Si estamos en el estado raíz, actualizar el mejor total conocido
                if i == 0 and total < root_best_total[0]:
                    root_best_total[0] = total

        # Guardar la mejor decisión para este estado
        choice[(i, caps)] = best_subset
        return best

    # Ejecutar DP desde el estado inicial
    best_total = dp(0, initial_caps)

    # Reconstrucción de asignaciones a partir de las mejores decisiones
    asignaciones = {}
    caps = list(initial_caps)
    for i, student in enumerate(students):
        # Durante cancelación, usamos la mejor decisión conocida o vacío
        subset = choice.get((i, tuple(caps)), ())
        asignaciones[student] = [c for (c, _) in subset]
        for (c, _) in subset:
            caps[c] -= 1

    # Devolver insatisfacción promedio (consistente con voraz y brute)
    num_students = len(students)
    average = best_total / num_students if num_students > 0 else 0.0
    return asignaciones, average


def rocDP(course_index_by_code, capacities, requests_by_student, stop_event=None):
    """
    Wrapper para el algoritmo de programación dinámica.
    Convierte las asignaciones de índices a códigos de materia.
    """
    asignaciones, promedio = dynamic(capacities, requests_by_student, stop_event=stop_event)
    course_code_by_index = {idx: code for code, idx in course_index_by_code.items()}
    asignaciones_con_codigos = {}
    for student, materias_idx in asignaciones.items():
        codigos = [course_code_by_index.get(idx, str(idx)) for idx in materias_idx]
        asignaciones_con_codigos[student] = codigos
    return asignaciones_con_codigos, promedio