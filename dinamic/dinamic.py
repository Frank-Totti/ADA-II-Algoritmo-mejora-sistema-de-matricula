from functools import lru_cache # permite guardar en cache la información del estado de cada recursión que se haga
import itertools # para realizar todas las posibles combinaciones

def gamma(x: int) -> int:
    return 3 * x - 1

# Cálculo de insatisfacción 

def calcular_insatisfaccion(asignadas, opciones_totales):

    k = len(opciones_totales)
    if k == 0:
        return 0.0 # Retorna 0 porque al no haber materias por asignar la insatisfacción es nula.
    assigned_count = len(asignadas)
    assigned_courses = {c for (c, _) in asignadas}
    unassigned_sum = sum(p for (c, p) in opciones_totales if c not in assigned_courses) # Se suman las proridades de las materias que no les asignaron 
    return (1 - assigned_count / k) * (unassigned_sum / gamma(k)) # Formula del enunciado


# Generar todos los subconjuntos válidos

def generar_subconjuntos(opciones):
    """Genera todos los subconjuntos posibles de materias solicitadas por un estudiante."""
    n = len(opciones)
    for r in range(n + 1):
        for comb in itertools.combinations(opciones, r):
            yield comb

#   Programa principal

def dinamic(capacities, requests_by_student):

    # Hacemos inmutables las solicitudes (para memoización)
    requests_immutable = {s: tuple(reqs) for s, reqs in requests_by_student.items()}
    students = list(requests_immutable.keys())
    initial_caps = tuple(capacities)

    # Diccionario para guardar las decisiones óptimas
    choice = {}

    @lru_cache(maxsize=None)
    def dp(i, caps):
        if i == len(students):
            return 0.0  # cuando se completen todos los estudiantes se le suma 0 dado que ya no hay insatisfacción para este caso

        student = students[i]
        opciones = requests_immutable[student]
        best = float("inf")
        best_subset = ()

        for subset in generar_subconjuntos(opciones):
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

            f_j = calcular_insatisfaccion(subset, opciones)
            total = f_j + dp(i + 1, tuple(new_caps))

            if total < best:
                best = total
                best_subset = subset

        # Guardar la mejor decisión para este estado
        choice[(i, caps)] = best_subset
        return best

    best_total = dp(0, initial_caps)

    asignaciones = {}
    caps = list(initial_caps)
    for i, student in enumerate(students):
        subset = choice.get((i, tuple(caps)), ())
        asignaciones[student] = [c for (c, _) in subset]
        # actualizar capacidades
        for (c, _) in subset:
            caps[c] -= 1

    promedio = best_total / len(students)

    return asignaciones, promedio