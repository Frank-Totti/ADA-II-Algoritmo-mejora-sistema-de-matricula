# Unión de todos los segmentos y/o componentes
import time
import tracemalloc

from dynamic.dynamic import dynamic
from brute.brute import construir_arbol

def take_time_and_memory(algorithm, *args, **kwargs):
    """Mide el tiempo y el uso de memoria en MB de una función."""
    tracemalloc.start()
    inicio = time.perf_counter()

    result = algorithm(*args, **kwargs)

    fin = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tiempo = fin - inicio
    memoria_usada = current / 10**6  # MB
    memoria_pico = peak / 10**6      # MB

    return {
        "tiempo_s": tiempo,
        "memoria_actual_MB": memoria_usada,
        "memoria_pico_MB": memoria_pico,
        "resultado": result
    }


def execute_algorithm(algorithm: str, capacities, request):
    """Ejecuta un algoritmo específico y mide su rendimiento."""
    if algorithm == "dynamic":
        return take_time_and_memory(dynamic, capacities, request)

    elif algorithm == "brute":
        #return take_time_and_memory(construir_arbol, capacities, request)
        pass

    elif algorithm == "voraz":
        # cuando implementes el algoritmo voraz, solo lo agregas aquí
        # return take_time_and_memory(voraz, capacities, request)
        pass

    else:
        raise ValueError(f"Algoritmo no válido: {algorithm!r}")
