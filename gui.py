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
import csv
import json
import threading
import tracemalloc

# Importar estilos y configuración
from gui_styles import GUIStyles, GUIIcons, GUIMessages

# Agregar paths necesarios para imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'input_output'))
sys.path.insert(0, os.path.join(current_dir, 'voraz'))
sys.path.insert(0, os.path.join(current_dir, 'brute'))
sys.path.insert(0, os.path.join(current_dir, 'dynamic'))

# Imports de los algoritmos
parse_input_file = None
try:
    input_path = os.path.join(current_dir, 'input_output', 'input.py')
    spec = importlib.util.spec_from_file_location("input_module", input_path)
    input_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(input_module)
    parse_input_file = input_module.parse_input_file
except Exception as e:
    print(f"Error importando parse_input_file: {e}")
    parse_input_file = None

# Importar voraz directamente del archivo, no del módulo
rocGreedy = None
try:
    import importlib.util
    voraz_path = os.path.join(current_dir, 'voraz', 'voraz.py')
    spec = importlib.util.spec_from_file_location("voraz_module", voraz_path)
    voraz_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(voraz_module)
    rocGreedy = voraz_module.rocGreedy
except Exception as e:
    print(f"Error importando voraz: {e}")
    rocGreedy = None

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
rocDP = None
try:
    dynamic_path = os.path.join(current_dir, 'dynamic', 'dynamic.py')
    spec = importlib.util.spec_from_file_location("dynamic_module", dynamic_path)
    dynamic_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dynamic_module)
    rocDP = dynamic_module.rocDP
except Exception as e:
    print(f"Error importando dynamic: {e}")
    rocDP = None


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
        # Datos acumulados para la tabla de resultados
        self.results = []  # lista de dicts: {algorithm, file, cost, time}
        self.stop_event = threading.Event()
        self.worker_thread = None
        self.next_result_id = 1
        # Captura de salida por ejecución
        self.capture_output = False
        self.current_output = []
        
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
        dynamic_rb = ttk.Radiobutton(algo_frame, 
                                    text=GUIMessages.ALGO_DYNAMIC, 
                                    variable=self.algorithm, 
                                    value="dynamic",
                                    style='Dark.TRadiobutton')
        dynamic_rb.grid(row=0, column=2, padx=15, pady=5, sticky=tk.W)
        if rocDP is None:
            dynamic_rb.config(state='disabled')
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
        
        # Botón para detener la ejecución
        self.stop_btn = ttk.Button(button_frame,
                                   text="Detener",
                                   command=self.stop_execution,
                                   style='Secondary.TButton')
        self.stop_btn.pack(side=tk.LEFT, padx=8)
        self.stop_btn.config(state='disabled')
        
        self.clear_btn = ttk.Button(button_frame, 
                                   text=GUIMessages.BTN_CLEAR, 
                                   command=self.clear_output,
                                   style='Secondary.TButton')
        self.clear_btn.pack(side=tk.LEFT, padx=8)
        
        # ===== SECCIÓN 4: Área de salida =====
        output_frame = ttk.LabelFrame(
            main_frame,
            text=GUIMessages.SECTION_OUTPUT,
            padding=str(GUIStyles.DIMENSIONS['padding_medium']),
            style='Dark.TLabelframe'
        )
        output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=8)
        # Dos columnas: izquierda (salida), derecha (tabla)
        output_frame.columnconfigure(0, weight=2)
        output_frame.columnconfigure(1, weight=1)
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
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Panel derecho: Tabla de resultados y controles
        right_panel = ttk.Frame(output_frame, style='Medium.TFrame')
        right_panel.grid(row=0, column=1, sticky=(tk.N, tk.E, tk.S, tk.W))
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)

        table_label = ttk.Label(right_panel, text="Resultados (comparación)", style='Dark.TLabel')
        table_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 6))

        # Treeview para resultados
        columns = ("algoritmo", "archivo", "costo", "tiempo", "mem_actual", "mem_pico")
        self.results_table = ttk.Treeview(right_panel, columns=columns, show='headings', height=10)
        self.results_table.heading("algoritmo", text="Algoritmo")
        self.results_table.heading("archivo", text="Archivo")
        self.results_table.heading("costo", text="Insatisfacción")
        self.results_table.heading("tiempo", text="Tiempo (s)")
        self.results_table.heading("mem_actual", text="Mem Actual (MB)")
        self.results_table.heading("mem_pico", text="Mem Pico (MB)")
        self.results_table.column("algoritmo", width=120, anchor=tk.W)
        self.results_table.column("archivo", width=140, anchor=tk.W)
        self.results_table.column("costo", width=110, anchor=tk.E)
        self.results_table.column("tiempo", width=90, anchor=tk.E)
        self.results_table.column("mem_actual", width=120, anchor=tk.E)
        self.results_table.column("mem_pico", width=110, anchor=tk.E)
        self.results_table.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Scrollbar vertical para la tabla
        scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.results_table.yview)
        self.results_table.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))

        # Botones de acciones de la tabla
        table_btns = ttk.Frame(right_panel, style='Medium.TFrame')
        table_btns.grid(row=2, column=0, columnspan=2, sticky=tk.E, pady=(8,0))
        save_btn = ttk.Button(table_btns, text="Guardar CSV", command=self.save_results_csv, style='Secondary.TButton')
        save_btn.pack(side=tk.RIGHT, padx=5)
        clear_tbl_btn = ttk.Button(table_btns, text="Limpiar Tabla", command=self.clear_results_table, style='Secondary.TButton')
        clear_tbl_btn.pack(side=tk.RIGHT, padx=5)
        delete_btn = ttk.Button(table_btns, text="Eliminar Selección", command=self.delete_selected_results, style='Secondary.TButton')
        delete_btn.pack(side=tk.RIGHT, padx=5)
        view_btn = ttk.Button(table_btns, text="Ver Detalle", command=self.show_selected_popup, style='Secondary.TButton')
        view_btn.pack(side=tk.RIGHT, padx=5)
        # Atajo de teclado Supr/Del para eliminar
        self.results_table.bind('<Delete>', lambda e: self.delete_selected_results())
        # Doble click para ver detalle
        self.results_table.bind('<Double-1>', lambda e: self.show_selected_popup())
        
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
        # Guardar en buffer si está activa la captura
        try:
            if self.capture_output:
                self.current_output.append(text)
        except Exception:
            pass

        # Asegurar actualización en el hilo de la GUI
        def _insert():
            self.output_text.insert(tk.END, text)
            self.output_text.see(tk.END)
            self.output_text.update()

        if threading.current_thread() is threading.main_thread():
            _insert()
        else:
            self.root.after(0, _insert)
        
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

        # Preparar estado y lanzar hilo
        self.stop_event.clear()
        algo = self.algorithm.get()
        self.status_var.set(GUIMessages.STATUS_RUNNING(GUIMessages.ALGO_NAMES.get(algo, algo.upper())))
        self.run_btn.config(state='disabled')
        self.stop_btn.config(state='normal')

        def worker():
            try:
                # Iniciar captura
                self.capture_output = True
                self.current_output = []
                # Medición de tiempo y memoria
                if algo == "voraz":
                    metrics = self.measure_time_memory(self.run_voraz)
                elif algo == "brute":
                    metrics = self.measure_time_memory(self.run_brute)
                elif algo == "dynamic":
                    metrics = self.measure_time_memory(self.run_dynamic)
                else:
                    metrics = {"tiempo_s": 0.0, "memoria_actual_MB": 0.0, "memoria_pico_MB": 0.0, "resultado": (0.0, {})}

                cost, assignment = metrics["resultado"]
                elapsed_time = metrics["tiempo_s"]
                mem_current = metrics["memoria_actual_MB"]
                mem_peak = metrics["memoria_pico_MB"]
                output_str = ''.join(self.current_output)

                # Agregar fila y actualizar estado en el hilo principal
                self.root.after(0, lambda: (
                    self.add_result_row(
                        algorithm=self.get_plain_algo_name(algo),
                        file=os.path.basename(self.file_path.get()),
                        cost=cost,
                        elapsed=elapsed_time,
                        mem_current=mem_current,
                        mem_peak=mem_peak,
                        output=output_str,
                        assignment=assignment
                    ),
                    self.status_var.set(GUIMessages.STATUS_COMPLETED(GUIMessages.ALGO_NAMES.get(algo, algo.upper()), elapsed_time))
                ))
            except KeyboardInterrupt:
                # Cancelación pedida
                self.root.after(0, lambda: self.append_output("\n[Ejecución cancelada]\n"))
                self.root.after(0, lambda: self.status_var.set("Ejecución cancelada"))
            except Exception as e:
                err = f"ERROR: {e}\n\n{traceback.format_exc()}"
                self.root.after(0, lambda: self.append_output(err))
                self.root.after(0, lambda: self.status_var.set(GUIMessages.STATUS_ERROR(GUIMessages.ALGO_NAMES.get(algo, algo.upper()))))
            finally:
                self.capture_output = False
                self.root.after(0, lambda: (
                    self.run_btn.config(state='normal'),
                    self.stop_btn.config(state='disabled')
                ))

        self.worker_thread = threading.Thread(target=worker, daemon=True)
        self.worker_thread.start()

    def measure_time_memory(self, func):
        """Mide tiempo y memoria de una función que retorna (costo, asignación)."""
        tracemalloc.start()
        inicio = time.perf_counter()
        result = func()
        fin = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return {
            "tiempo_s": fin - inicio,
            "memoria_actual_MB": current / 10**6,
            "memoria_pico_MB": peak / 10**6,
            "resultado": result
        }
            
    def run_voraz(self):
        """Ejecuta el algoritmo voraz"""
        if rocGreedy is None:
            raise ImportError("No se pudo importar el algoritmo Voraz (rocGreedy)")
        
        # Parsear entrada
        course_index_by_code, capacities, requests_by_student = parse_input_file(self.file_path.get())
        
        
        
        # Ejecutar algoritmo
        assignments, unsatisfaction = rocGreedy(course_index_by_code, capacities, requests_by_student)
        # Mostrar resultados en el formato solicitado (sin emojis)
        # Costo en primera línea y su valor en la siguiente
        self.append_output(f"{unsatisfaction:.6f}\n")
        # Por cada estudiante: "ei,ai" y luego las materias asignadas una por línea
        for student in sorted(assignments.keys()):
            courses = sorted(list(assignments[student]))
            self.append_output(f"{student},{len(courses)}\n")
            for course in courses:
                self.append_output(f"{course}\n")
        # Preparar asignación ordenada
        assignment_out = {s: sorted(list(courses)) for s, courses in assignments.items()}
        return float(unsatisfaction), assignment_out
        
    def run_brute(self):
        """Ejecuta el algoritmo de fuerza bruta usando el wrapper rocBrute"""
        try:
            brute_path = os.path.join(current_dir, 'brute', 'brute.py')
            spec = importlib.util.spec_from_file_location("brute_module", brute_path)
            brute_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(brute_module)
            rocBrute = brute_module.rocBrute
        except Exception as e:
            raise ImportError(f"No se pudo importar rocBrute: {e}")

        # Parsear entrada
        course_index_by_code, capacities, requests_by_student = parse_input_file(self.file_path.get())

        # Ejecutar wrapper
        try:
            assignment, average_dissatisfaction = rocBrute(course_index_by_code, capacities, requests_by_student, stop_event=self.stop_event)
        except KeyboardInterrupt:
            return 0.0, {}

        # Mostrar resultados en formato solicitado
   
        self.append_output(f"{average_dissatisfaction:.6f}\n")

        assignment_out = {}
        for student in sorted(assignment.keys()):
            courses = sorted(list(assignment[student]))
            assignment_out[student] = courses
            self.append_output(f"{student},{len(courses)}\n")
            for course in courses:
                self.append_output(f"{course}\n")
        return float(average_dissatisfaction), assignment_out
        
    def run_dynamic(self):
        """Ejecuta el algoritmo de programación dinámica"""
        if rocDP is None:
            raise ImportError(GUIMessages.ERROR_DYNAMIC_UNAVAILABLE)
        
        # Parsear entrada
        course_index_by_code, capacities, requests_by_student = parse_input_file(self.file_path.get())
        
        # Ejecutar algoritmo
        try:
            assignment, average_dissatisfaction = rocDP(course_index_by_code, capacities, requests_by_student, stop_event=self.stop_event)
        except KeyboardInterrupt:
            return 0.0, {}
        # Mostrar resultados en formato solicitado
        self.append_output(f"{average_dissatisfaction:.6f}\n")
        assignment_out = {}
        for student in sorted(assignment.keys()):
            courses = sorted(list(assignment[student]))
            assignment_out[student] = courses
            self.append_output(f"{student},{len(courses)}\n")
            for course in courses:
                self.append_output(f"{course}\n")
        return float(average_dissatisfaction), assignment_out

    def stop_execution(self):
        """Solicita la cancelación de la ejecución actual."""
        self.stop_event.set()

    # ===== Utilidades de resultados =====
    def get_plain_algo_name(self, algo_key: str) -> str:
        mapping = {
            'voraz': 'VORAZ',
            'brute': 'BRUTE FORCE',
            'dynamic': 'DINÁMICA',
        }
        return mapping.get(algo_key, algo_key.upper())

    def add_result_row(self, algorithm: str, file: str, cost: float, elapsed: float, mem_current: float, mem_peak: float, output: str, assignment: dict):
        row_id = self.next_result_id
        self.next_result_id += 1
        row = {
            'id': row_id,
            'algorithm': algorithm,
            'file': file,
            'cost': float(cost),
            'time': float(elapsed),
            'mem_current': float(mem_current),
            'mem_peak': float(mem_peak),
            'output': output,
            'assignment': assignment,
        }
        self.results.append(row)
        self.results_table.insert('', tk.END, iid=str(row_id), values=(
            algorithm,
            file,
            f"{cost:.6f}",
            f"{elapsed:.4f}",
            f"{mem_current:.3f}",
            f"{mem_peak:.3f}"
        ))

    def clear_results_table(self):
        for item in self.results_table.get_children():
            self.results_table.delete(item)
        self.results.clear()

    def save_results_csv(self):
        if not self.results:
            messagebox.showinfo("Guardar CSV", "No hay resultados para guardar.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV', '*.csv')],
            title='Guardar resultados como'
        )
        if not file_path:
            return
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['algorithm', 'file', 'cost', 'time', 'mem_current', 'mem_peak', 'assignment', 'output']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for r in self.results:
                    writer.writerow({
                        'algorithm': r.get('algorithm'),
                        'file': r.get('file'),
                        'cost': r.get('cost'),
                        'time': r.get('time'),
                        'mem_current': r.get('mem_current'),
                        'mem_peak': r.get('mem_peak'),
                        'assignment': json.dumps(r.get('assignment', {}), ensure_ascii=False),
                        'output': r.get('output', ''),
                    })
            messagebox.showinfo("Guardar CSV", f"Resultados guardados en {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Guardar CSV", f"No se pudo guardar el archivo.\n{e}")

    def delete_selected_results(self):
        """Elimina las filas seleccionadas de la tabla y del arreglo interno."""
        selected = self.results_table.selection()
        if not selected:
            return
        # Convertir a ints los iids seleccionados
        ids = set(int(iid) for iid in selected)
        # Filtrar resultados conservando el orden
        self.results = [row for row in self.results if row.get('id') not in ids]
        # Eliminar de la tabla
        for iid in selected:
            self.results_table.delete(iid)
    def on_table_select(self, event=None):
        """Muestra en el panel de salida el resultado textual guardado para la fila seleccionada."""
        selection = self.results_table.selection()
        if not selection:
            return
        # Solo tomar el primero si hay múltiples
        iid = int(selection[0])
        row = next((r for r in self.results if r.get('id') == iid), None)
        if not row:
            return
        # Mostrar salida guardada
        self.clear_output()
        output = row.get('output', '')
        # Insertar de golpe para eficiencia
        self.output_text.insert(tk.END, output)
        self.output_text.see(tk.END)

    def show_selected_popup(self):
        """Abre un popup con el detalle (salida y asignación) de la fila seleccionada."""
        selection = self.results_table.selection()
        if not selection:
            messagebox.showinfo("Detalle", "Selecciona una fila para ver su detalle.")
            return
        iid = int(selection[0])
        row = next((r for r in self.results if r.get('id') == iid), None)
        if not row:
            return

        win = tk.Toplevel(self.root)
        win.title(f"Detalle - {row.get('algorithm')} ({row.get('file')})")
        win.geometry("700x500")
        win.transient(self.root)
        # Asegurar que la ventana sea visible antes de aplicar el grab
        def _try_grab():
            try:
                win.grab_set()
            except tk.TclError:
                # Reintentar poco después hasta que sea visible
                win.after(20, _try_grab)
        win.after(0, _try_grab)
        win.lift()
        win.focus_set()

        nb = ttk.Notebook(win)
        nb.pack(fill=tk.BOTH, expand=True)

        # Tab: Salida
        frame_out = ttk.Frame(nb)
        nb.add(frame_out, text="Salida")
        txt_out = scrolledtext.ScrolledText(frame_out, wrap=tk.WORD, font=GUIStyles.FONTS['mono'])
        txt_out.pack(fill=tk.BOTH, expand=True)
        txt_out.insert(tk.END, row.get('output', ''))
        txt_out.configure(state='disabled')

        # Tab: Asignación (JSON)
        frame_json = ttk.Frame(nb)
        nb.add(frame_json, text="Asignación (JSON)")
        txt_json = scrolledtext.ScrolledText(frame_json, wrap=tk.WORD, font=GUIStyles.FONTS['mono'])
        txt_json.pack(fill=tk.BOTH, expand=True)
        try:
            json_text = json.dumps(row.get('assignment', {}), indent=2, ensure_ascii=False)
        except Exception:
            json_text = str(row.get('assignment', {}))
        txt_json.insert(tk.END, json_text)
        txt_json.configure(state='disabled')

        # Pie con datos clave
        footer = ttk.Frame(win)
        footer.pack(fill=tk.X, padx=10, pady=8)
        ttk.Label(footer, text=f"Algoritmo: {row.get('algorithm')}").pack(side=tk.LEFT, padx=5)
        ttk.Label(footer, text=f"Costo: {row.get('cost'):.6f}").pack(side=tk.LEFT, padx=5)
        ttk.Label(footer, text=f"Tiempo: {row.get('time'):.4f}s").pack(side=tk.LEFT, padx=5)
        if 'mem_current' in row and 'mem_peak' in row:
            ttk.Label(footer, text=f"Mem Act: {row.get('mem_current'):.3f} MB").pack(side=tk.LEFT, padx=5)
            ttk.Label(footer, text=f"Mem Pico: {row.get('mem_peak'):.3f} MB").pack(side=tk.LEFT, padx=5)


def main():
    """Función principal para ejecutar la GUI"""
    root = tk.Tk()
    
    # Configurar ícono de ventana (opcional)
    # root.iconbitmap('icon.ico')  # Si tienes un ícono
    
    app = AlgorithmGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
