# ADA-II-Algoritmo-mejora-sistema-de-matricula

Este es un proyecto que busca construir un algoritmo que mejore el procedimiento de matrícula utilizando diferentes enfoques algorítmicos.

## Descripción

Sistema inteligente de asignación de cupos que implementa y compara tres algoritmos diferentes:

- **Algoritmo Voraz (Greedy)**: Solución rápida y aproximada
- **Fuerza Bruta (Brute Force)**: Búsqueda exhaustiva del óptimo
- **Programación Dinámica**: Solución eficiente y óptima

## Uso Rápido - Ejecutable Standalone

### Descargar Ejecutable Pre-compilado

El proyecto incluye ejecutables standalone que NO requieren Python instalado:

- **Windows**: `dist/SistemaMatricula.exe`
- **Linux**: `dist/SistemaMatricula`

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
