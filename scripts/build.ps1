# Quick Build Script - Windows & Linux Compatible
# Detecta automáticamente el sistema operativo y construye el ejecutable

Write-Host "╔═══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Sistema de Matricula - Quick Build             ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio raíz del proyecto
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

$OS = [System.Environment]::OSVersion.Platform

Write-Host "Sistema detectado: $OS" -ForegroundColor Yellow
Write-Host ""

if ($OS -match "Win") {
    Write-Host "Ejecutando build para Windows..." -ForegroundColor Green
    & .\scripts\build_windows.ps1
} else {
    Write-Host "Ejecutando build para Linux..." -ForegroundColor Green
    bash ./scripts/build_linux.sh
}
