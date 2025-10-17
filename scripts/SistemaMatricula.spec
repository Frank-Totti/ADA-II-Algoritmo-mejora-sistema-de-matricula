# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Sistema de Asignación de Cupos
Genera un ejecutable standalone que incluye todos los módulos necesarios
"""

block_cipher = None

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('gui_styles.py', '.'),
        ('voraz/*.py', 'voraz'),
        ('brute/*.py', 'brute'),
        ('dynamic/*.py', 'dynamic'),
        ('input_output/*.py', 'input_output'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['data'],  # Excluir directorio de pruebas
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SistemaMatricula',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana de consola para GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
