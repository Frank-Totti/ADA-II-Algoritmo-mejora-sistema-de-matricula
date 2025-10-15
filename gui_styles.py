"""
Estilos y configuración visual para la GUI
==========================================

Define la paleta de colores, estilos de widgets y configuración visual
para el Sistema de Asignación de Cupos.

Autor: Sistema de Asignación de Cupos
Fecha: Octubre 2025
"""

from tkinter import ttk


class GUIStyles:
    """Clase que contiene todos los estilos visuales de la GUI"""
    
    # ===== PALETA DE COLORES AZUL OSCURO =====
    COLORS = {
        'bg_dark': '#0a1929',           # Fondo principal muy oscuro
        'bg_medium': '#1a2332',         # Fondo medio
        'bg_light': '#243447',          # Fondo claro
        'accent': '#2e7d32',            # Verde acento
        'accent_hover': '#388e3c',      # Verde acento hover
        'button': '#1976d2',            # Azul botones
        'button_hover': '#2196f3',      # Azul botones hover
        'text': '#e3f2fd',              # Texto claro
        'text_secondary': '#90caf9',    # Texto secundario
        'border': '#42a5f5',            # Bordes
        'error': '#f44336',             # Rojo error
        'success': '#4caf50',           # Verde éxito
        'frame_bg': '#1e2936',          # Fondo de frames
    }
    
    # ===== FUENTES =====
    FONTS = {
        'title': ('Segoe UI', 16, 'bold'),
        'heading': ('Segoe UI', 11, 'bold'),
        'normal': ('Segoe UI', 10),
        'button': ('Segoe UI', 10, 'bold'),
        'mono': ('Consolas', 10),
    }
    
    # ===== DIMENSIONES =====
    DIMENSIONS = {
        'window_width': 900,
        'window_height': 700,
        'min_width': 600,
        'min_height': 500,
        'text_width': 90,
        'text_height': 22,
        'padding_large': 15,
        'padding_medium': 10,
        'padding_small': 5,
    }
    
    @staticmethod
    def configure_styles():
        """Configura todos los estilos ttk personalizados"""
        style = ttk.Style()
        
        # Configurar tema base
        style.theme_use('clam')
        
        # ===== ESTILOS PARA FRAMES =====
        style.configure('Dark.TFrame', 
                       background=GUIStyles.COLORS['bg_dark'])
        
        style.configure('Medium.TFrame',
                       background=GUIStyles.COLORS['bg_medium'])
        
        # ===== ESTILOS PARA LABELS =====
        style.configure('Dark.TLabel',
                       background=GUIStyles.COLORS['bg_dark'],
                       foreground=GUIStyles.COLORS['text'],
                       font=GUIStyles.FONTS['normal'])
        
        style.configure('Title.TLabel',
                       background=GUIStyles.COLORS['bg_dark'],
                       foreground=GUIStyles.COLORS['text'],
                       font=GUIStyles.FONTS['title'])
        
        # ===== ESTILOS PARA LABELFRAME =====
        style.configure('Dark.TLabelframe',
                       background=GUIStyles.COLORS['frame_bg'],
                       foreground=GUIStyles.COLORS['text'],
                       bordercolor=GUIStyles.COLORS['border'],
                       borderwidth=2)
        
        style.configure('Dark.TLabelframe.Label',
                       background=GUIStyles.COLORS['frame_bg'],
                       foreground=GUIStyles.COLORS['text_secondary'],
                       font=GUIStyles.FONTS['heading'])
        
        # ===== ESTILOS PARA ENTRY =====
        style.configure('Dark.TEntry',
                       fieldbackground=GUIStyles.COLORS['bg_light'],
                       foreground=GUIStyles.COLORS['text'],
                       bordercolor=GUIStyles.COLORS['border'],
                       lightcolor=GUIStyles.COLORS['border'],
                       darkcolor=GUIStyles.COLORS['border'])
        
        # ===== ESTILOS PARA RADIOBUTTONS =====
        style.configure('Dark.TRadiobutton',
                       background=GUIStyles.COLORS['frame_bg'],
                       foreground=GUIStyles.COLORS['text'],
                       font=GUIStyles.FONTS['normal'])
        
        style.map('Dark.TRadiobutton',
                 background=[('active', GUIStyles.COLORS['bg_light'])],
                 foreground=[('disabled', '#666666')])
        
        # ===== ESTILOS PARA BOTONES PRINCIPALES =====
        style.configure('Accent.TButton',
                       background=GUIStyles.COLORS['button'],
                       foreground='white',
                       bordercolor=GUIStyles.COLORS['border'],
                       focuscolor=GUIStyles.COLORS['accent'],
                       font=GUIStyles.FONTS['button'],
                       padding=10)
        
        style.map('Accent.TButton',
                 background=[('active', GUIStyles.COLORS['button_hover']),
                           ('pressed', GUIStyles.COLORS['accent'])])
        
        # ===== ESTILOS PARA BOTONES SECUNDARIOS =====
        style.configure('Secondary.TButton',
                       background=GUIStyles.COLORS['bg_light'],
                       foreground=GUIStyles.COLORS['text'],
                       bordercolor=GUIStyles.COLORS['border'],
                       font=GUIStyles.FONTS['normal'],
                       padding=8)
        
        style.map('Secondary.TButton',
                 background=[('active', GUIStyles.COLORS['bg_medium'])])


class GUIIcons:
    """Iconos deshabilitados (sin emojis). Se mantienen constantes vacías para compatibilidad."""
    TITLE = ""
    FILE = ""
    SETTINGS = ""
    OUTPUT = ""
    FOLDER = ""
    TRASH = ""
    PLAY = ""
    VORAZ = ""
    BRUTE = ""
    DYNAMIC = ""
    SUCCESS = ""
    ERROR = ""
    LOADING = ""
    CLOCK = ""
    CLEAN = ""
    DOCUMENT = ""
    LIST = ""
    USER = ""
    CHART = ""
    REFRESH = ""


class GUIMessages:
    """Clase que contiene los mensajes de la GUI"""
    
    # Títulos
    WINDOW_TITLE = "Sistema de Asignación de Cupos - Comparador de Algoritmos"
    APP_TITLE = f"Sistema de Asignación de Cupos"
    
    # Secciones
    SECTION_FILE = "Archivo de Entrada"
    SECTION_ALGORITHM = "Algoritmo"
    SECTION_OUTPUT = "Salida del Algoritmo"
    
    # Botones
    BTN_BROWSE = "Buscar..."
    BTN_RUN = "Ejecutar Algoritmo"
    BTN_CLEAR = "Limpiar"
    
    # Algoritmos
    ALGO_VORAZ = "Voraz (Greedy)"
    ALGO_BRUTE = "Fuerza Bruta (Brute Force)"
    ALGO_DYNAMIC = "Programación Dinámica (Dynamic)"
    ALGO_UNAVAILABLE = "(No disponible)"
    
    # Estados
    STATUS_READY = "Listo para comenzar"
    STATUS_FILE_SELECTED = lambda filename: f"Archivo seleccionado: {filename}"
    STATUS_CLEANED = "Salida limpiada - Listo para ejecutar"
    STATUS_RUNNING = lambda algo_name: f"Ejecutando {algo_name}..."
    STATUS_COMPLETED = lambda algo_name, time: f"{algo_name} completado en {time:.4f}s"
    STATUS_ERROR = lambda algo_name: f"Error al ejecutar {algo_name}"
    
    # Nombres de algoritmos para mensajes
    ALGO_NAMES = {
        'voraz': 'VORAZ',
        'brute': 'FUERZA BRUTA',
        'dynamic': 'PROGRAMACIÓN DINÁMICA'
    }
    
    # Errores
    ERROR_NO_FILE = "Por favor seleccione un archivo de entrada"
    ERROR_FILE_NOT_FOUND = "El archivo seleccionado no existe"
    
    # Diálogos
    DIALOG_TITLE_SELECT = "Seleccionar archivo de entrada"
    DIALOG_ERROR_TITLE = "Error"
    DIALOG_ERROR_EXECUTION = "Error de Ejecución"
    
    # Separadores
    SEPARATOR_LONG = "="*70
    SEPARATOR_SHORT = "-"*70
    
    # Resultados
    RESULT_ASSIGNMENT = "Asignación Óptima:"
    RESULT_STUDENT = lambda student, courses: f"  {student}: [{courses}]"
    RESULT_SATISFACTION = lambda value: f"Insatisfacción F⟨M,E⟩(A) = {value:.6f}"
    RESULT_TIME = lambda time: f"Tiempo de ejecución: {time:.4f} segundos"
    
    # Headers de algoritmos
    HEADER_VORAZ = "ALGORITMO VORAZ (GREEDY) - Estrategia VDC"
    HEADER_BRUTE = "ALGORITMO FUERZA BRUTA (BRUTE FORCE)"
    HEADER_DYNAMIC = "ALGORITMO PROGRAMACIÓN DINÁMICA (DYNAMIC PROGRAMMING)"
    
    # Mensajes de proceso
    PROCESS_BRUTE = "Procesando todas las combinaciones posibles...\n\n"
    PROCESS_DYNAMIC = "Resolviendo con memoización...\n\n"
    
    # Error de algoritmo no disponible
    ERROR_DYNAMIC_UNAVAILABLE = (
        "El algoritmo de Programación Dinámica no está disponible.\n\n"
        "Posibles soluciones:\n"
        "1. Implementa el algoritmo en: dynamic/dynamic.py\n"
        "2. O copia la implementación desde otro módulo\n"
        "3. Asegúrate de exportar la función 'rocDP'"
    )
