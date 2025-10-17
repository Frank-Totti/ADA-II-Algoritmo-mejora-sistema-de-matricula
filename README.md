# ADA-II-Algoritmo-mejora-sistema-de-matricula

Este es un proyecto que busca construir un algoritmo que mejore el procedimiento de matrícula utilizando diferentes enfoques algorítmicos.

## Inicio Rápido

**El ejecutable está listo para usar en la raíz del proyecto!**

Para comenzar inmediatamente:

1. Ejecuta `SistemaMatricula.exe` (Windows) desde la raíz del proyecto
2. O consulta [docs/QUICKSTART.md](docs/QUICKSTART.md) para más detalles

## Descripción

Sistema inteligente de asignación de cupos que implementa y compara tres algoritmos diferentes:

- **Algoritmo Voraz (Greedy)**: Solución rápida y aproximada
- **Fuerza Bruta (Brute Force)**: Búsqueda exhaustiva del óptimo
- **Programación Dinámica**: Solución eficiente y óptima

## Uso Rápido - Ejecutable Standalone

### Ejecutable Incluido (Listo para Usar)

El proyecto incluye un ejecutable pre-compilado en la raíz del repositorio:

- **Windows**: `SistemaMatricula.exe` (en la raíz)
- **Alternativa**: `dist/SistemaMatricula.exe`

**Simplemente haz doble clic en el archivo para ejecutar!**

### Construir tu Propio Ejecutable

#### Windows

```powershell
.\scripts\build_windows.ps1
```

#### Linux

```bash
chmod +x scripts/build_linux.sh
./scripts/build_linux.sh
```

**Documentación completa**: Ver [docs/BUILD_README.md](docs/BUILD_README.md) y [docs/USAGE.md](docs/USAGE.md)

## Desarrollo

### Requisitos

- Python 3.8+
- tkinter (incluido con Python)
- PyInstaller (solo para construir ejecutables)

### Instalación para Desarrollo

```bash
# Clonar el repositorio
git clone https://github.com/Frank-Totti/ADA-II-Algoritmo-mejora-sistema-de-matricula.git
cd ADA-II-Algoritmo-mejora-sistema-de-matricula

# Crear entorno virtual (recomendado)
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias (si las hay)
pip install -r requirements.txt  # Si existe
```

### Ejecutar desde Código Fuente

```bash
python gui.py
```

## Estructura del Proyecto

```
.
├── gui.py                  # Interfaz gráfica principal
├── gui_styles.py          # Estilos y configuración de la GUI
├── main.py                # Punto de entrada alternativo
├── voraz/                 # Algoritmo Voraz
├── brute/                 # Algoritmo de Fuerza Bruta
├── dynamic/               # Programación Dinámica
├── input_output/          # Manejo de entrada/salida
├── data/                  # Archivos de prueba (46 casos)
├── scripts/               # Scripts de construcción
│   ├── build_windows.ps1  # Build para Windows
│   ├── build_linux.sh     # Build para Linux
│   └── SistemaMatricula.spec  # Configuración PyInstaller
└── docs/                  # Documentación
    ├── BUILD_README.md    # Guía de construcción
    ├── USAGE.md           # Guía de uso
    ├── RELEASE_NOTES.md   # Notas de versión
    └── QUICKSTART.txt     # Inicio rápido
```

## Casos de Prueba

El proyecto incluye una batería de 46 casos de prueba en el directorio `data/`:

- `Prueba1.txt` a `Prueba46.txt`: Diversos escenarios de asignación
- Casos pequeños, medianos y grandes para evaluar rendimiento

## Características de la GUI

- Interfaz gráfica moderna con tema oscuro
- Selección visual de algoritmos
- Tabla comparativa de resultados
- Medición de tiempo y memoria
- Exportación de resultados a CSV
- Cancelación de ejecuciones largas
- Vista detallada de asignaciones (JSON)
- Responsive design

## Resultados y Análisis

Los algoritmos se evalúan según:

- **Costo de Insatisfacción**: Métrica de calidad de asignación
- **Tiempo de Ejecución**: Performance temporal
- **Uso de Memoria**: Eficiencia espacial

## Detalles de Implementación

### Entorno de Desarrollo

La implementación se realizó en **Python 3.13**, aprovechando su sintaxis concisa y bibliotecas estándar. El código está organizado en módulos separados para facilitar la mantenibilidad:

- **`input_output/`**: Lectura/escritura de archivos y cálculo de insatisfacción
- **`brute/`**: Implementación del algoritmo de fuerza bruta
- **`dynamic/`**: Implementación del algoritmo de programación dinámica
- **`voraz/`**: Implementación del algoritmo voraz
- **`gui.py`**: Interfaz gráfica para ejecutar y comparar algoritmos

### Funciones Principales

Cada algoritmo expone una función wrapper que encapsula su ejecución completa:

#### rocBrute (Fuerza Bruta)

```python
def rocBrute(course_index_by_code, capacities, requests_by_student, stop_event=None)
```

- Explora todas las posibles asignaciones de materias a estudiantes
- Encuentra la solución óptima que minimiza la insatisfacción global
- Retorna: tupla `(assignment, average_dissatisfaction)`

#### rocGreedy (Voraz)

```python
def rocGreedy(course_index_by_code, capacities, requests_by_student)
```

- Procesa estudiantes secuencialmente según prioridad
- Asigna materias de mayor a menor preferencia mientras haya cupo
- Retorna: tupla `(assignments, unsatisfaction)`

#### rocDP (Programación Dinámica)

```python
def rocDP(course_index_by_code, capacities, requests_by_student, stop_event=None)
```

- Utiliza memoización para evitar recálculos
- Construye la solución óptima de forma incremental
- Reconstruye la asignación final desde la tabla de estados
- Retorna: tupla `(assignment, average_dissatisfaction)`

### Formato de Entrada/Salida

**Archivo de Entrada:**
```
M1 50    # Materia M1 con capacidad de 50 estudiantes
M2 30
---      # Separador
E1 M1 M2 # Estudiante E1 prefiere M1, luego M2
E2 M2 M1
```

**Salida del Programa:**
```
0.333333           # Insatisfacción promedio
E1,2               # Estudiante E1 recibió 2 materias
M1                 # Primera materia asignada
M2                 # Segunda materia asignada
E2,1
M2
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'feat: add nueva caracteristica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## Licencia

[Especificar licencia aquí]

## Autores

- Juan Francesco Totti Astaiza - [Frank-Totti](https://github.com/Frank-Totti)
- Andrey Quiceno - [AndreyQuicenoC](https://github.com/AndreyQuicenoC)
- Jonathan Aristizabal - [JonMesiter](https://github.com/JonMesiter)
- Ivan Ausecha - [IvanAusechaS](https://github.com/IvanAusechaS)

## Enlaces

- Repositorio: https://github.com/Frank-Totti/ADA-II-Algoritmo-mejora-sistema-de-matricula
