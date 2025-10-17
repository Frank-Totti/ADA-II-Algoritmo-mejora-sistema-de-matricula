#!/bin/bash
# Quick Build Script - Automatically detects OS and builds executable

echo "╔═══════════════════════════════════════════════════╗"
echo "║   Sistema de Matricula - Quick Build             ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

OS=$(uname -s)
echo "Sistema detectado: $OS"
echo ""

case "$OS" in
    Linux*)
        echo "Ejecutando build para Linux..."
        ./build_linux.sh
        ;;
    Darwin*)
        echo "Ejecutando build para macOS..."
        ./build_linux.sh  # macOS usa el mismo script que Linux
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo "Ejecutando build para Windows..."
        powershell.exe -ExecutionPolicy Bypass -File build_windows.ps1
        ;;
    *)
        echo "Sistema operativo no reconocido: $OS"
        echo "Por favor, ejecuta manualmente build_linux.sh o build_windows.ps1"
        exit 1
        ;;
esac
