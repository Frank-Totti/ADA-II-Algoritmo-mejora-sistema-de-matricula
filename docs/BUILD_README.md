# Guía de Construcción de Ejecutables

Este proyecto puede ser compilado a un ejecutable standalone para Windows y Linux usando PyInstaller.

## 📋 Requisitos Previos

- Python 3.8 o superior
- PyInstaller (`pip install pyinstaller`)
- Todas las dependencias del proyecto instaladas

## 🪟 Windows

### Opción 1: Usando el script de PowerShell (Recomendado)

```powershell
.\build_windows.ps1
```

### Opción 2: Manual

```powershell
# Instalar PyInstaller si no está instalado
pip install pyinstaller

# Limpiar builds anteriores
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# Construir ejecutable
pyinstaller --clean SistemaMatricula.spec
```

El ejecutable se generará en: `dist\SistemaMatricula.exe`

## 🐧 Linux

### Opción 1: Usando el script de Bash (Recomendado)

```bash
chmod +x build_linux.sh
./build_linux.sh
```

### Opción 2: Manual

```bash
# Instalar PyInstaller si no está instalado
pip install pyinstaller

# Limpiar builds anteriores
rm -rf build dist __pycache__

# Construir ejecutable
pyinstaller --clean SistemaMatricula.spec

# Hacer el ejecutable ejecutable
chmod +x dist/SistemaMatricula
```

El ejecutable se generará en: `dist/SistemaMatricula`

## 📦 Características del Ejecutable

- **Standalone**: No requiere Python instalado
- **GUI Integrada**: Ejecuta automáticamente la interfaz gráfica
- **Portable**: Puede copiarse y ejecutarse en cualquier máquina compatible
- **Optimizado**: Comprimido con UPX para reducir tamaño
- **Sin Consola**: Solo muestra la ventana de la GUI (sin terminal)

## 🚀 Uso del Ejecutable

### Windows

Doble clic en `SistemaMatricula.exe` o ejecutar desde PowerShell:

```powershell
.\dist\SistemaMatricula.exe
```

### Linux

```bash
./dist/SistemaMatricula
```

## 📁 Estructura de Archivos

El ejecutable incluye:

- ✅ GUI (interfaz gráfica)
- ✅ Algoritmo Voraz
- ✅ Algoritmo de Fuerza Bruta
- ✅ Programación Dinámica
- ✅ Módulos de entrada/salida
- ❌ Directorio `data/` (excluido - usar archivos externos)

## ⚠️ Notas Importantes

1. **Archivos de Prueba**: El directorio `data/` NO se incluye en el ejecutable. Los archivos de prueba deben proporcionarse externamente.

2. **Tamaño**: El ejecutable puede ocupar 20-50 MB debido a las dependencias embebidas.

3. **Antivirus**: Algunos antivirus pueden marcar ejecutables de PyInstaller como falsos positivos. Esto es normal.

4. **Plataforma Específica**: El ejecutable de Windows solo funciona en Windows, y el de Linux solo en Linux.

## 🔧 Personalización

Para modificar la configuración del build, edita `SistemaMatricula.spec`:

- `name='SistemaMatricula'`: Nombre del ejecutable
- `console=False`: `True` para mostrar consola, `False` para ocultarla
- `excludes=['data']`: Directorios/módulos a excluir
- `icon='icon.ico'`: Agregar un ícono personalizado (descomentar y proporcionar archivo)

## 🐛 Troubleshooting

### Error: "No module named 'tkinter'"

PyInstaller debe detectar tkinter automáticamente. Si no lo hace, agrega a `hiddenimports` en el spec.

### El ejecutable es muy grande

- Considera usar `--onefile` si prefieres un solo archivo
- Verifica que no se estén incluyendo módulos innecesarios

### Error al ejecutar en Linux

Asegúrate de que el archivo tenga permisos de ejecución:

```bash
chmod +x dist/SistemaMatricula
```

## 📝 Licencia y Distribución

Al distribuir el ejecutable, asegúrate de:

- Incluir instrucciones de uso
- Proporcionar archivos de prueba de ejemplo
- Mencionar que el directorio `data/` debe estar disponible para las pruebas
