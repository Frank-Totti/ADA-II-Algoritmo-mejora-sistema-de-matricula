#!/bin/bash
# Script de construcción para Linux
# Genera el ejecutable de Sistema de Asignación de Cupos

echo "====================================="
echo "Building Sistema de Matricula (Linux)"
echo "====================================="
echo ""

# Activar entorno virtual si existe
if [ -f ".venv/bin/activate" ]; then
    echo "Activando entorno virtual..."
    source .venv/bin/activate
fi

# Limpiar builds anteriores
echo "Limpiando builds anteriores..."
rm -rf build dist __pycache__

# Verificar PyInstaller
echo "Verificando PyInstaller..."
if ! command -v pyinstaller &> /dev/null; then
    echo "ERROR: PyInstaller no está instalado"
    echo "Ejecuta: pip install pyinstaller"
    exit 1
fi

# Construir ejecutable
echo ""
echo "Construyendo ejecutable..."
pyinstaller --clean SistemaMatricula.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "====================================="
    echo "BUILD EXITOSO!"
    echo "====================================="
    echo ""
    echo "El ejecutable se encuentra en: dist/SistemaMatricula"
    echo ""
    
    # Hacer el ejecutable... ejecutable
    chmod +x dist/SistemaMatricula
    
    # Mostrar tamaño del ejecutable
    if [ -f "dist/SistemaMatricula" ]; then
        size=$(du -h dist/SistemaMatricula | cut -f1)
        echo "Tamaño del ejecutable: $size"
    fi
else
    echo ""
    echo "====================================="
    echo "BUILD FALLÓ"
    echo "====================================="
    exit 1
fi
