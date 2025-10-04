# Logíca de la solución por fuerza bruta
import itertools

# --- Cálculo de insatisfacción ---

def calcular_insatisfaccion(solucion, estudiantes):
    """
    Calcula el nivel de insatisfacción de la solución actual.
    """     
    valor_insatisfaccion = 0
    
    for clave in solucion:  # cada estudiante
        materias_solicitadas = estudiantes[clave]       # lista de (materia, prioridad)
        materias_asignadas = solucion[clave]            # lista de materias realmente asignadas

        # total materias solicitadas
        total_solicitadas = len(materias_solicitadas)
        total_asignadas = len(materias_asignadas)

        # prioridades de materias NO asignadas
        no_asignadas = [p for (m, p) in materias_solicitadas if m not in materias_asignadas]
        suma_prioridades_no_asignadas = sum(no_asignadas)

        # fórmula de insatisfacción individual
        fj = (1 - total_asignadas / total_solicitadas) * (suma_prioridades_no_asignadas / funcionGamma(total_solicitadas))
        
        valor_insatisfaccion += fj

    # insatisfacción general
    insatisfaccion_general = valor_insatisfaccion / len(estudiantes)

    return insatisfaccion_general

# --- Restricciones ---
def funcionGamma(X):
    """
    Función gamma para normalizar la insatisfacción
    """
    return 3*X-1

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

# --- Generador de subconjuntos ---
def subconjuntos(materias):
    resultado = []
    for r in range(len(materias) + 1):
        for combo in itertools.combinations(materias, r):
            resultado.append(list(combo))
    return resultado

# --- Definición del nodo del árbol ---
class Nodo:
    def __init__(self, estudiante, materias_asignadas, nivel=0):
        self.estudiante = estudiante
        self.materias_asignadas = materias_asignadas  # subconjunto elegido
        self.hijos = []  # hijos en el árbol
        self.nivel = nivel

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

    def __repr__(self):
        return {self.estudiante: self.materias_asignadas}

def validar_cupos(solucion_completa, materias):
        """Verifica que no se exceda el cupo de ninguna materia"""
        conteo_materias = {}
        for estudiante, materias_est in solucion_completa.items():
            for materia in materias_est:
                conteo_materias[materia] = conteo_materias.get(materia, 0) + 1
        
        for materia, count in conteo_materias.items():
            if count > materias[materia]:  # Excede el cupo
                return False
        return True

# --- Construcción del árbol ---
def construir_arbol(estudiantes_dict, estudiantes, materias):
    """
    estudiantes_dict: dict {estudiante: [(materia, prioridad), ...]}
    """
    global mejor_solucion, mejor_insatisfaccion
    lista_estudiantes = list(estudiantes_dict.keys())
    
    def expandir(idx, solucion_actual, estudiantes, materias):
        global mejor_solucion, mejor_insatisfaccion
        
        # Caso base: hemos asignado materias a todos los estudiantes
        if idx >= len(lista_estudiantes):
            if validar_cupos(solucion_actual,materias):
                insatisfaccion = calcular_insatisfaccion(solucion_actual, estudiantes)
                if insatisfaccion < mejor_insatisfaccion:
                    mejor_insatisfaccion = insatisfaccion
                    mejor_solucion = solucion_actual.copy()
            return
        
        # Estudiante actual
        estudiante = lista_estudiantes[idx]
        materias_estudiante = estudiantes_dict[estudiante]
        
        # Probar todos los subconjuntos posibles para este estudiante
        for subconjunto in subconjuntos(materias_estudiante):
            materias_asignadas = [materia for materia, prioridad in subconjunto]
            solucion_actual[estudiante] = materias_asignadas
            
            # Continuar con el siguiente estudiante
            expandir(idx + 1, solucion_actual, estudiantes, materias)
    
    # Inicializar y comenzar la búsqueda
    mejor_solucion = {}
    mejor_insatisfaccion = float('inf')

    expandir(0, {}, estudiantes, materias)
    return mejor_solucion



def main():
    # --- Datos de entrada ---

    # Diccionario de materias con su respectivo cupo
    materias = {
        "M1": 3,
        "M2": 4,
        "M3": 2,
    }
    maximo_materias = 7
    prioridad = [1,2,3,4,5]

    # Diccionario de estudiantes con sus preferencias (materia, prioridad)
    estudiantes = {
        "ms1": [("M1", 5), ("M2", 2), ("M3", 1)],
        "ms2": [("M1", 4), ("M2", 1), ("M3", 3)],
        "ms3": [("M2", 3), ("M3", 2)],
        "ms4": [("M1", 2), ("M3", 3)],
        "ms5": [("M1", 3), ("M2", 2), ("M3", 3)]
    }
    
    if maximaPrioridadPermitida(prioridad, estudiantes):
        print(f"Prioridades deben ser entre {min(prioridad)} y {max(prioridad)}.")
        return
    
    if restriccionMaximoSumaPrioridades(estudiantes):
        print("Algún estudiante excede la prioridad máxima permitida.")
        return
    
    if len(estudiantes) > maximo_materias:
        print("Número de estudiantes excede el máximo permitido.")
        return

    solucion_optima = construir_arbol(estudiantes, estudiantes, materias)
    # print("Solución óptima encontrada:")
    # for estudiante, materias_asignadas in solucion_optima.items():
    #     print(f" - {estudiante}: {materias_asignadas}")
    # print("Con insatisfacción de:", calcular_insatisfaccion(solucion_optima, estudiantes))
    print(round(calcular_insatisfaccion(solucion_optima, estudiantes), 5))
    for estudiante, materias_asignadas in solucion_optima.items():
        print(f"{estudiante}, {len(materias_asignadas)}")
        for materia in materias_asignadas:
            print(materia)
    
    
if __name__ == "__main__":
    main()