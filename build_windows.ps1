# Script de construcción para Windows
# Genera el ejecutable de Sistema de Asignación de Cupos

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Building Sistema de Matricula (Windows)" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual si existe
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
}

# Limpiar builds anteriores
Write-Host "Limpiando builds anteriores..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force build }
if (Test-Path "dist") { Remove-Item -Recurse -Force dist }
if (Test-Path "__pycache__") { Remove-Item -Recurse -Force __pycache__ }

# Verificar PyInstaller
Write-Host "Verificando PyInstaller..." -ForegroundColor Yellow
$pyinstaller = Get-Command pyinstaller -ErrorAction SilentlyContinue
if (-not $pyinstaller) {
    Write-Host "ERROR: PyInstaller no está instalado" -ForegroundColor Red
    Write-Host "Ejecuta: pip install pyinstaller" -ForegroundColor Red
    exit 1
}

# Construir ejecutable
Write-Host ""
Write-Host "Construyendo ejecutable..." -ForegroundColor Green
pyinstaller --clean SistemaMatricula.spec

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host "BUILD EXITOSO!" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "El ejecutable se encuentra en: dist\SistemaMatricula.exe" -ForegroundColor Cyan
    Write-Host ""
    
    # Mostrar tamaño del ejecutable
    $exePath = "dist\SistemaMatricula.exe"
    if (Test-Path $exePath) {
        $size = (Get-Item $exePath).Length / 1MB
        Write-Host "Tamaño del ejecutable: $([math]::Round($size, 2)) MB" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Red
    Write-Host "BUILD FALLÓ" -ForegroundColor Red
    Write-Host "=====================================" -ForegroundColor Red
    exit 1
}
