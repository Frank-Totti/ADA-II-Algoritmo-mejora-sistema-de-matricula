"""
Algoritmo de Fuerza Bruta para Repartición Óptima de Cupos
=========================================================

Proyecto: Análisis y Diseño de Algoritmos II
Algoritmo: rocBrute - Estrategia de Búsqueda Exhaustiva Completa
Fecha: 14 de Octubre 2025

Descripción:
    Implementa un algoritmo de fuerza bruta que garantiza encontrar la
    asignación óptima de cupos de materias a estudiantes mediante
    exploración exhaustiva de todas las combinaciones posibles.

Estrategia de Fuerza Bruta:
    - Genera todos los subconjuntos posibles de asignaciones por estudiante
    - Explora el árbol completo de decisiones mediante backtracking
    - Valida restricciones de capacidad en cada estado
    - Calcula insatisfacción para cada solución completa
    - Mantiene registro de la mejor solución encontrada
    - Garantiza optimalidad global a costa de complejidad exponencial
"""


from input_output import funcionGamma, calcular_insatisfaccion_general, maximaPrioridadPermitida, restriccionMaximoSumaPrioridades, subconjuntos


# --- Definición del nodo del árbol ---
class Nodo:
    """
    Clase que representa un nodo en el árbol de decisiones.
    """
    def __init__(self, estudiante, materias_asignadas, nivel=0):
        self.estudiante = estudiante
        self.materias_asignadas = materias_asignadas  # subconjunto elegido
        self.hijos = []  # hijos en el árbol
        self.nivel = nivel

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

    def __repr__(self):
        return {self.estudiante: self.materias_asignadas}


def validar_cupos(solucion_completa, capacities):
        """
        Verifica que no se exceda el cupo de ninguna materia usando índices
        """
        conteo_materias = [0] * len(capacities)  # Inicializar contador para cada índice
        
        for estudiante, materias_est in solucion_completa.items():
            for materia_idx in materias_est:  # materia_idx es directamente el índice
                conteo_materias[materia_idx] += 1
        
        # Verificar que no se exceda ningún cupo
        return all(count <= capacities[idx] for idx, count in enumerate(conteo_materias))


def construir_arbol(estudiantes_dict, estudiantes, materias, stop_event=None):
    """
    Construye el árbol de decisiones y encuentra la solución óptima.
    Args:
        estudiantes_dict: dict {estudiante: [(materia, prioridad), ...]}
    """
    global mejor_solucion, mejor_insatisfaccion
    lista_estudiantes = list(estudiantes_dict.keys())
    cancelado = False  # flag local para cortar búsqueda sin excepciones

    def expandir(idx, solucion_actual, estudiantes, materias):
        nonlocal cancelado
        # Cancelación cooperativa
        if stop_event is not None and getattr(stop_event, 'is_set', None) and stop_event.is_set():
            cancelado = True
            return
        if cancelado:
            return
        global mejor_solucion, mejor_insatisfaccion
        
        # Caso base: hemos asignado materias a todos los estudiantes
        if idx >= len(lista_estudiantes):
            if validar_cupos(solucion_actual,materias):
                insatisfaccion = calcular_insatisfaccion_general(solucion_actual, estudiantes)
                if insatisfaccion < mejor_insatisfaccion:
                    mejor_insatisfaccion = insatisfaccion
                    mejor_solucion = solucion_actual.copy()
            return
        
        # Estudiante actual
        estudiante = lista_estudiantes[idx]
        materias_estudiante = estudiantes_dict[estudiante]
        
        # Probar todos los subconjuntos posibles para este estudiante
        for subconjunto in subconjuntos(materias_estudiante):
            if cancelado:
                return
            materias_asignadas = [materia for materia, prioridad in subconjunto]
            solucion_actual[estudiante] = materias_asignadas
            
            # Continuar con el siguiente estudiante
            expandir(idx + 1, solucion_actual, estudiantes, materias)
            if cancelado:
                return
    
    # Inicializar y comenzar la búsqueda
    # Baseline: solución factible con cero asignaciones para todos los estudiantes
    mejor_solucion = {est: [] for est in lista_estudiantes}
    mejor_insatisfaccion = calcular_insatisfaccion_general(mejor_solucion, estudiantes)

    expandir(0, {}, estudiantes, materias)
    return mejor_solucion


def rocBrute(course_index_by_code, capacities, requests_by_student, stop_event=None):
    """
    Wrapper para el algoritmo de fuerza bruta.
    Convierte las asignaciones de índices a códigos de materia.
    Args:
        course_index_by_code: Diccionario que mapea códigos de materias a índices
        capacities: Lista de capacidades por materia (índice)
        requests_by_student: Diccionario de solicitudes por estudiante
        stop_event: threading.Event para cancelación cooperativa (opcional)
    Returns:
        tuple: (asignaciones_con_codigos, insatisfaccion_promedio)
    """
    solucion_optima = construir_arbol(requests_by_student, requests_by_student, capacities, stop_event=stop_event)
    promedio = calcular_insatisfaccion_general(solucion_optima, requests_by_student)
    course_code_by_index = {idx: code for code, idx in course_index_by_code.items()}
    asignaciones_con_codigos = {}
    for student, materias_idx in solucion_optima.items():
        codigos = [course_code_by_index.get(idx, str(idx)) for idx in materias_idx]
        asignaciones_con_codigos[student] = codigos
    return asignaciones_con_codigos, promedio