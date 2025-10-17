#!/bin/bash
# Quick Build Script - Automatically detects OS and builds executable

echo "╔═══════════════════════════════════════════════════╗"
echo "║   Sistema de Matricula - Quick Build             ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Cambiar al directorio raíz del proyecto
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

OS=$(uname -s)
echo "Sistema detectado: $OS"
echo ""

case "$OS" in
    Linux*)
        echo "Ejecutando build para Linux..."
        ./scripts/build_linux.sh
        ;;
    Darwin*)
        echo "Ejecutando build para macOS..."
        ./scripts/build_linux.sh  # macOS usa el mismo script que Linux
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo "Ejecutando build para Windows..."
        powershell.exe -ExecutionPolicy Bypass -File scripts/build_windows.ps1
        ;;
    *)
        echo "Sistema operativo no reconocido: $OS"
        echo "Por favor, ejecuta manualmente scripts/build_linux.sh o scripts/build_windows.ps1"
        exit 1
        ;;
esac
