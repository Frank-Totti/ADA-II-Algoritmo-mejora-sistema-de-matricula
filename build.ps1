# Quick Build Script - Windows & Linux Compatible
# Detecta automáticamente el sistema operativo y construye el ejecutable

Write-Host "╔═══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Sistema de Matricula - Quick Build             ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$OS = [System.Environment]::OSVersion.Platform

Write-Host "Sistema detectado: $OS" -ForegroundColor Yellow
Write-Host ""

if ($OS -match "Win") {
    Write-Host "Ejecutando build para Windows..." -ForegroundColor Green
    & .\build_windows.ps1
} else {
    Write-Host "Ejecutando build para Linux..." -ForegroundColor Green
    bash ./build_linux.sh
}
