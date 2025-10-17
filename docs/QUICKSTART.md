# Guía de Inicio Rápido

## Sistema de Asignación de Cupos

### Para Usuarios Finales

#### Ejecutar el Programa

**Windows:**

```
Doble clic en dist\SistemaMatricula.exe
```

**Linux:**

```bash
./dist/SistemaMatricula
```

#### Uso Básico

1. Haz clic en "Examinar" para seleccionar un archivo de prueba (.txt)
2. Selecciona un algoritmo:
   - **Voraz**: Rápido y eficiente
   - **Fuerza Bruta**: Exhaustivo (puede ser lento)
   - **Programación Dinámica**: Óptimo y eficiente
3. Haz clic en "Ejecutar Algoritmo"
4. Revisa los resultados en el panel de salida

Para más detalles, consulta [USAGE.md](USAGE.md)

---

### Para Desarrolladores

#### Construir Ejecutable

**Windows:**

```powershell
.\scripts\build_windows.ps1
```

**Linux:**

```bash
chmod +x scripts/build_linux.sh
./scripts/build_linux.sh
```

**Auto-detección de SO:**

```powershell
# Windows
.\scripts\build.ps1
```

```bash
# Linux
chmod +x scripts/build.sh
./scripts/build.sh
```

Para más detalles, consulta [BUILD_README.md](BUILD_README.md)

---

### Ejecutar desde Código Fuente

```bash
# Activar entorno virtual
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux

# Ejecutar GUI
python gui.py
```

---

### Formato de Archivo de Entrada

```
M1 50
M2 30
M3 40
---
E1 M1 M2 M3
E2 M2 M3 M1
E3 M3 M1 M2
```

- Primera sección: Materias (Código Capacidad)
- Separador: ---
- Segunda sección: Estudiantes y sus preferencias ordenadas

---

### Estructura del Proyecto

```
.
├── gui.py                 # Interfaz gráfica principal
├── gui_styles.py         # Estilos de la GUI
├── main.py               # Punto de entrada alternativo
├── voraz/                # Algoritmo Voraz
├── brute/                # Algoritmo de Fuerza Bruta
├── dynamic/              # Programación Dinámica
├── input_output/         # Manejo de entrada/salida
├── data/                 # Archivos de prueba (46 casos)
├── scripts/              # Scripts de construcción
│   ├── build_windows.ps1
│   ├── build_linux.sh
│   ├── build.ps1
│   ├── build.sh
│   └── SistemaMatricula.spec
└── docs/                 # Documentación
    ├── BUILD_README.md
    ├── USAGE.md
    ├── RELEASE_NOTES.md
    └── QUICKSTART.md
```

---

### Requisitos

**Para ejecutable:**

- Windows 10/11 o Linux moderno
- Aprox. 50 MB de RAM
- Aprox. 11 MB de espacio en disco
- NO requiere Python instalado

**Para desarrollo:**

- Python 3.8+
- PyInstaller 6.16.0+
- tkinter (incluido con Python)

---

### Soporte

- Repositorio: https://github.com/Frank-Totti/ADA-II-Algoritmo-mejora-sistema-de-matricula
- Issues: Reportar bugs en GitHub Issues
- Documentación completa en el directorio docs/
