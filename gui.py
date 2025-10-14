"""
GUI para Algoritmos de Asignación de Cupos
==========================================

Interfaz gráfica para ejecutar y comparar algoritmos de asignación de materias:
- Voraz (Greedy)
- Fuerza Bruta (Brute Force)
- Programación Dinámica (Dynamic Programming)

Autor: Sistema de Asignación de Cupos
Fecha: Octubre 2025
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import sys
import os
from typing import Dict, List, Tuple
import traceback
import time
import importlib.util

# Importar estilos y configuración
from gui_styles import GUIStyles, GUIIcons, GUIMessages

# Agregar paths necesarios para imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'input-output'))
sys.path.insert(0, os.path.join(current_dir, 'voraz'))
sys.path.insert(0, os.path.join(current_dir, 'brute'))
sys.path.insert(0, os.path.join(current_dir, 'dinamic'))

# Imports de los algoritmos
parse_input_file = None
try:
    input_path = os.path.join(current_dir, 'input-output', 'input.py')
    spec = importlib.util.spec_from_file_location("input_module", input_path)
    input_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(input_module)
    parse_input_file = input_module.parse_input_file
except Exception as e:
    print(f"Error importando parse_input_file: {e}")
    parse_input_file = None

# Importar voraz directamente del archivo, no del módulo
rocV = None
try:
    import importlib.util
    voraz_path = os.path.join(current_dir, 'voraz', 'voraz.py')
    spec = importlib.util.spec_from_file_location("voraz_module", voraz_path)
    voraz_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(voraz_module)
    rocV = voraz_module.rocV
except Exception as e:
    print(f"Error importando voraz: {e}")
    rocV = None

# Importar brute de manera similar
construir_arbol = None
calc_insatisfaccion_brute = None
try:
    brute_path = os.path.join(current_dir, 'brute', 'brute.py')
    spec = importlib.util.spec_from_file_location("brute_module", brute_path)
    brute_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(brute_module)
    construir_arbol = brute_module.construir_arbol
    calc_insatisfaccion_brute = brute_module.calcular_insatisfaccion
except Exception as e:
    print(f"Error importando brute: {e}")
    construir_arbol = None
    calc_insatisfaccion_brute = None

# Importar programación dinámica de manera similar a los otros algoritmos
rocPD = None
try:
    dinamic_path = os.path.join(current_dir, 'dinamic', 'dinamic.py')
    spec = importlib.util.spec_from_file_location("dinamic_module", dinamic_path)
    dinamic_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dinamic_module)
    rocPD = dinamic_module.rocPD
except Exception as e:
    print(f"Error importando dinamic: {e}")
    rocPD = None


class AlgorithmGUI:
    """Clase principal de la GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(GUIMessages.WINDOW_TITLE)
        self.root.geometry(f"{GUIStyles.DIMENSIONS['window_width']}x{GUIStyles.DIMENSIONS['window_height']}")
        
        # Establecer tamaño mínimo de ventana para que sea usable
        self.root.minsize(600, 500)
        
        # Configurar colores del root
        self.root.configure(bg=GUIStyles.COLORS['bg_dark'])
        
        # Variables
        self.file_path = tk.StringVar()
        self.algorithm = tk.StringVar(value="voraz")
        
        # Configurar estilos personalizados
        GUIStyles.configure_styles()
        
        # Configurar la interfaz
        self.setup_ui()
        
        # Vincular evento de redimensionamiento para ajustes dinámicos
        self.root.bind('<Configure>', self.on_window_resize)
        self.last_width = self.root.winfo_width()
        self.last_height = self.root.winfo_height()
        
    def setup_ui(self):
        """Configura todos los elementos de la interfaz"""
        
        # Ajustar padding según tamaño inicial de ventana
        padding = GUIStyles.DIMENSIONS['padding_medium']
        
        # Frame principal con estilo oscuro
        main_frame = ttk.Frame(self.root, 
                              padding=str(padding), 
                              style='Dark.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar peso de las filas y columnas para que sean responsive
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        # Dar peso a la fila del output para que se expanda
        main_frame.rowconfigure(4, weight=1)
        
        # Guardar referencia al main_frame para ajustes dinámicos
        self.main_frame = main_frame
        
        # ===== TÍTULO =====
        title_label = ttk.Label(main_frame, 
                               text=GUIMessages.APP_TITLE,
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 15))
        
        # ===== SECCIÓN 1: Selección de archivo =====
        file_frame = ttk.LabelFrame(main_frame, 
                                   text=GUIMessages.SECTION_FILE,
                                   padding=str(GUIStyles.DIMENSIONS['padding_medium']),
                                   style='Dark.TLabelframe')
        file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=8)
        file_frame.columnconfigure(0, weight=1)
        
        # Entry para mostrar la ruta con estilo oscuro
        file_entry = ttk.Entry(file_frame, 
                              textvariable=self.file_path, 
                              state='readonly',
                              style='Dark.TEntry',
                              font=GUIStyles.FONTS['mono'])
        file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Botón para seleccionar archivo
        browse_btn = ttk.Button(file_frame, 
                               text=GUIMessages.BTN_BROWSE, 
                               command=self.browse_file,
                               style='Accent.TButton')
        browse_btn.grid(row=0, column=1)
        
        # ===== SECCIÓN 2: Selección de algoritmo =====
        algo_frame = ttk.LabelFrame(main_frame, 
                                   text=GUIMessages.SECTION_ALGORITHM,
                                   padding=str(GUIStyles.DIMENSIONS['padding_medium']),
                                   style='Dark.TLabelframe')
        algo_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=8)
        
        # Configurar columnas del frame de algoritmos para que se expandan
        algo_frame.columnconfigure(0, weight=1)
        algo_frame.columnconfigure(1, weight=1)
        algo_frame.columnconfigure(2, weight=1)
        
        # Radiobuttons para seleccionar algoritmo con íconos
        ttk.Radiobutton(algo_frame, 
                       text=GUIMessages.ALGO_VORAZ, 
                       variable=self.algorithm, 
                       value="voraz",
                       style='Dark.TRadiobutton').grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)
        
        ttk.Radiobutton(algo_frame, 
                       text=GUIMessages.ALGO_BRUTE, 
                       variable=self.algorithm, 
                       value="brute",
                       style='Dark.TRadiobutton').grid(row=0, column=1, padx=15, pady=5, sticky=tk.W)
        
        # Radio button para programación dinámica (deshabilitado si no está disponible)
        dinamic_rb = ttk.Radiobutton(algo_frame, 
                                    text=GUIMessages.ALGO_DYNAMIC, 
                                    variable=self.algorithm, 
                                    value="dinamic",
                                    style='Dark.TRadiobutton')
        dinamic_rb.grid(row=0, column=2, padx=15, pady=5, sticky=tk.W)
        if rocPD is None:
            dinamic_rb.config(state='disabled')
            # Mostrar mensaje de que no está disponible
            unavailable_label = ttk.Label(algo_frame, 
                                         text=GUIMessages.ALGO_UNAVAILABLE, 
                                         style='Dark.TLabel',
                                         foreground='#666666')
            unavailable_label.grid(row=1, column=2, padx=15)
        
        # ===== SECCIÓN 3: Botones de control =====
        button_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        button_frame.grid(row=3, column=0, pady=15)
        
        self.run_btn = ttk.Button(button_frame, 
                                 text=GUIMessages.BTN_RUN, 
                                 command=self.run_algorithm, 
                                 style='Accent.TButton')
        self.run_btn.pack(side=tk.LEFT, padx=8)
        
        self.clear_btn = ttk.Button(button_frame, 
                                   text=GUIMessages.BTN_CLEAR, 
                                   command=self.clear_output,
                                   style='Secondary.TButton')
        self.clear_btn.pack(side=tk.LEFT, padx=8)
        
        # ===== SECCIÓN 4: Área de salida =====
        output_frame = ttk.LabelFrame(main_frame, 
                                     text=GUIMessages.SECTION_OUTPUT,
                                     padding=str(GUIStyles.DIMENSIONS['padding_medium']),
                                     style='Dark.TLabelframe')
        output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=8)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Text widget con scroll para mostrar la salida con colores oscuros
        # Usar width=1 para que se ajuste al contenedor y sea responsive
        self.output_text = scrolledtext.ScrolledText(
            output_frame, 
            wrap=tk.WORD, 
            width=1,  # Permitir que se ajuste al ancho del contenedor
            height=10,  # Altura mínima razonable
            font=GUIStyles.FONTS['mono'],
            bg=GUIStyles.COLORS['bg_light'],
            fg=GUIStyles.COLORS['text'],
            insertbackground=GUIStyles.COLORS['text'],
            selectbackground=GUIStyles.COLORS['button'],
            selectforeground='white',
            relief=tk.FLAT,
            borderwidth=2
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ===== SECCIÓN 5: Barra de estado =====
        self.status_var = tk.StringVar(value=GUIMessages.STATUS_READY)
        status_bar = ttk.Label(main_frame, 
                              textvariable=self.status_var,
                              style='Dark.TLabel',
                              relief=tk.SUNKEN, 
                              anchor=tk.W,
                              padding=5)
        status_bar.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(8, 0))
    
    def on_window_resize(self, event):
        """Maneja el redimensionamiento de la ventana para ajustes responsive"""
        # Solo procesar eventos del root window, no de widgets hijos
        if event.widget != self.root:
            return
            
        current_width = event.width
        current_height = event.height
        
        # Evitar procesamiento excesivo verificando cambios significativos
        if (abs(current_width - self.last_width) > 10 or 
            abs(current_height - self.last_height) > 10):
            self.last_width = current_width
            self.last_height = current_height
            
            # Aquí puedes agregar ajustes dinámicos adicionales si es necesario
            # Por ejemplo, cambiar el tamaño de fuente en ventanas muy pequeñas
        
    def browse_file(self):
        """Abre un diálogo para seleccionar el archivo de entrada"""
        filename = filedialog.askopenfilename(
            title=GUIMessages.DIALOG_TITLE_SELECT,
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if filename:
            self.file_path.set(filename)
            self.status_var.set(GUIMessages.STATUS_FILE_SELECTED(os.path.basename(filename)))
            
    def clear_output(self):
        """Limpia el área de salida"""
        self.output_text.delete(1.0, tk.END)
        self.status_var.set(GUIMessages.STATUS_CLEANED)
        
    def append_output(self, text):
        """Agrega texto al área de salida"""
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.update()
        
    def run_algorithm(self):
        """Ejecuta el algoritmo seleccionado"""
        # Validar que se haya seleccionado un archivo
        if not self.file_path.get():
            messagebox.showerror(GUIMessages.DIALOG_ERROR_TITLE, GUIMessages.ERROR_NO_FILE)
            return
            
        # Validar que el archivo existe
        if not os.path.exists(self.file_path.get()):
            messagebox.showerror(GUIMessages.DIALOG_ERROR_TITLE, GUIMessages.ERROR_FILE_NOT_FOUND)
            return
            
        # Limpiar salida anterior
        self.clear_output()
        
        # Obtener algoritmo seleccionado
        algo = self.algorithm.get()
        
        # Ejecutar el algoritmo correspondiente
        try:
            self.status_var.set(GUIMessages.STATUS_RUNNING(GUIMessages.ALGO_NAMES.get(algo, algo.upper())))
            self.run_btn.config(state='disabled')
            self.root.update()
            
            start_time = time.time()
            
            if algo == "voraz":
                self.run_voraz()
            elif algo == "brute":
                self.run_brute()
            elif algo == "dinamic":
                self.run_dinamic()
                
            elapsed_time = time.time() - start_time
            
            self.append_output(f"\n{GUIMessages.SEPARATOR_LONG}\n")
            self.append_output(GUIMessages.RESULT_TIME(elapsed_time) + "\n")
            self.append_output(f"{GUIMessages.SEPARATOR_LONG}\n")
            self.status_var.set(GUIMessages.STATUS_COMPLETED(GUIMessages.ALGO_NAMES.get(algo, algo.upper()), elapsed_time))
            
        except Exception as e:
            error_msg = f"{GUIIcons.ERROR} ERROR: {str(e)}\n\n{traceback.format_exc()}"
            self.append_output(error_msg)
            self.status_var.set(GUIMessages.STATUS_ERROR(GUIMessages.ALGO_NAMES.get(algo, algo.upper())))
            messagebox.showerror(GUIMessages.DIALOG_ERROR_EXECUTION, str(e))
        finally:
            self.run_btn.config(state='normal')
            
    def run_voraz(self):
        """Ejecuta el algoritmo voraz"""
        if rocV is None:
            raise ImportError("No se pudo importar el algoritmo Voraz (rocV)")
            
        self.append_output(f"{GUIMessages.SEPARATOR_LONG}\n")
        self.append_output(f"{GUIMessages.HEADER_VORAZ}\n")
        self.append_output(f"{GUIMessages.SEPARATOR_LONG}\n\n")
        
        # Parsear entrada
        course_index_by_code, capacities, requests_by_student = parse_input_file(self.file_path.get())
        
        self.append_output("Ejecutando algoritmo voraz...\n\n")
        
        # Ejecutar algoritmo
        assignments, unsatisfaction = rocV(course_index_by_code, capacities, requests_by_student)
        
        # Mostrar resultados
        self.append_output(f"{GUIMessages.RESULT_ASSIGNMENT}\n")
        self.append_output(f"{GUIMessages.SEPARATOR_SHORT}\n")
        
        for student, courses in sorted(assignments.items()):
            courses_str = ', '.join(sorted(courses))
            self.append_output(GUIMessages.RESULT_STUDENT(student, courses_str) + "\n")
            
        self.append_output(f"\n{GUIMessages.SEPARATOR_SHORT}\n")
        self.append_output(GUIMessages.RESULT_SATISFACTION(unsatisfaction) + "\n")
        
    def run_brute(self):
        """Ejecuta el algoritmo de fuerza bruta"""
        if construir_arbol is None or calc_insatisfaccion_brute is None:
            raise ImportError("No se pudo importar el algoritmo Brute Force")
            
        self.append_output(f"{GUIMessages.SEPARATOR_LONG}\n")
        self.append_output(f"{GUIMessages.HEADER_BRUTE}\n")
        self.append_output(f"{GUIMessages.SEPARATOR_LONG}\n\n")
        
        # Parsear entrada
        course_index_by_code, capacities, requests_by_student = parse_input_file(self.file_path.get())
        
        self.append_output(GUIMessages.PROCESS_BRUTE)
        
        # Ejecutar algoritmo
        solucion_optima = construir_arbol(requests_by_student, requests_by_student, capacities)
        insatisfaccion = calc_insatisfaccion_brute(solucion_optima, requests_by_student)
        
        # Mostrar resultados
        self.append_output(f"{GUIMessages.RESULT_ASSIGNMENT}\n")
        self.append_output(f"{GUIMessages.SEPARATOR_SHORT}\n")
        
        # Invertir el mapeo de índices a códigos
        course_code_by_index = {idx: code for code, idx in course_index_by_code.items()}
        
        for estudiante, materias_asignadas in sorted(solucion_optima.items()):
            # Convertir índices a códigos de materia
            codigos_materias = []
            for materia_idx in materias_asignadas:
                codigo = course_code_by_index.get(materia_idx, str(materia_idx))
                codigos_materias.append(codigo)
            courses_str = ', '.join(sorted(codigos_materias))
            self.append_output(GUIMessages.RESULT_STUDENT(estudiante, courses_str) + "\n")
            
        self.append_output(f"\n{GUIMessages.SEPARATOR_SHORT}\n")
        self.append_output(GUIMessages.RESULT_SATISFACTION(insatisfaccion) + "\n")
        
    def run_dinamic(self):
        """Ejecuta el algoritmo de programación dinámica"""
        if rocPD is None:
            raise ImportError(GUIMessages.ERROR_DYNAMIC_UNAVAILABLE)
            
        self.append_output(f"{GUIMessages.SEPARATOR_LONG}\n")
        self.append_output(f"{GUIMessages.HEADER_DYNAMIC}\n")
        self.append_output(f"{GUIMessages.SEPARATOR_LONG}\n\n")
        
        # Parsear entrada
        course_index_by_code, capacities, requests_by_student = parse_input_file(self.file_path.get())
        
        self.append_output(GUIMessages.PROCESS_DYNAMIC)
        
        # Ejecutar algoritmo
        assignment, average_dissatisfaction = rocPD(course_index_by_code, capacities, requests_by_student)
        
        # Mostrar resultados
        self.append_output(f"{GUIMessages.RESULT_ASSIGNMENT}\n")
        self.append_output(f"{GUIMessages.SEPARATOR_SHORT}\n")
        
        for student, courses in sorted(assignment.items()):
            courses_str = ', '.join(sorted(courses))
            self.append_output(GUIMessages.RESULT_STUDENT(student, courses_str) + "\n")
            
        self.append_output(f"\n{GUIMessages.SEPARATOR_SHORT}\n")
        self.append_output(GUIMessages.RESULT_SATISFACTION(average_dissatisfaction) + "\n")


def main():
    """Función principal para ejecutar la GUI"""
    root = tk.Tk()
    
    # Configurar ícono de ventana (opcional)
    # root.iconbitmap('icon.ico')  # Si tienes un ícono
    
    app = AlgorithmGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
