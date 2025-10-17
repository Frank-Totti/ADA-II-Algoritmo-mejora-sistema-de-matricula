# 🚀 Guía Rápida de Uso del Ejecutable

## Sistema de Asignación de Cupos - Ejecutable Standalone

### 📥 Descarga

El ejecutable se genera en el directorio `dist/` después de ejecutar el script de construcción:
- **Windows**: `dist\SistemaMatricula.exe`
- **Linux**: `dist/SistemaMatricula`

### ▶️ Ejecución

#### Windows
1. **Doble clic** en `SistemaMatricula.exe`, o
2. Desde PowerShell/CMD:
   ```powershell
   .\SistemaMatricula.exe
   ```

#### Linux
1. Dar permisos de ejecución (solo la primera vez):
   ```bash
   chmod +x SistemaMatricula
   ```
2. Ejecutar:
   ```bash
   ./SistemaMatricula
   ```

### 🖥️ Uso de la Aplicación

1. **Seleccionar Archivo de Entrada**
   - Haz clic en "Examinar"
   - Selecciona un archivo `.txt` con los datos de entrada
   - Formato esperado: capacidades de materias y solicitudes de estudiantes

2. **Seleccionar Algoritmo**
   - 🏃 **Voraz (Greedy)**: Rápido, solución aproximada
   - 💪 **Fuerza Bruta**: Exhaustivo, encuentra el óptimo (lento para datos grandes)
   - 🧠 **Programación Dinámica**: Eficiente, solución óptima

3. **Ejecutar**
   - Haz clic en "Ejecutar Algoritmo"
   - Espera los resultados (tiempo varía según algoritmo y tamaño de datos)
   - Los resultados aparecerán en el panel de salida

4. **Ver Resultados**
   - **Panel izquierdo**: Salida detallada del algoritmo
   - **Panel derecho**: Tabla comparativa de ejecuciones
   - **Doble clic en fila**: Ver detalle completo (salida + asignación JSON)

5. **Funciones Adicionales**
   - **Detener**: Cancela la ejecución actual (útil para algoritmos lentos)
   - **Limpiar**: Borra el panel de salida
   - **Guardar CSV**: Exporta la tabla de resultados
   - **Eliminar Selección**: Borra filas de la tabla (o presiona `Supr`)

### 📁 Formato de Archivo de Entrada

Ejemplo de estructura:
```
M1 50
M2 30
M3 40
---
E1 M1 M2 M3
E2 M2 M3
E3 M1 M3
```

- Primera sección: Materias y sus capacidades (`Código Capacidad`)
- Separador: `---`
- Segunda sección: Estudiantes y sus preferencias ordenadas

### 📊 Interpretación de Resultados

**Costo de Insatisfacción**: Promedio de insatisfacción de los estudiantes
- Menor valor = Mejor asignación
- 0.0 = Todos recibieron su primera opción

**Tiempo**: Duración de la ejecución en segundos

**Memoria**: Uso de memoria durante la ejecución
- Mem Actual: Memoria al finalizar
- Mem Pico: Máximo uso de memoria

**Parcial**: Indica si la ejecución fue detenida antes de completarse

### 🔧 Troubleshooting

**El ejecutable no abre**
- En Windows: Marca como seguro si el Defender lo bloquea
- En Linux: Verifica permisos con `ls -l` (debe tener `x`)

**Error al seleccionar archivo**
- Verifica que el formato sea correcto
- Asegúrate de que el archivo tenga la extensión `.txt`

**Algoritmo muy lento**
- Usa Voraz para pruebas rápidas
- Fuerza Bruta puede tardar minutos/horas con muchos estudiantes
- Usa el botón "Detener" para cancelar

**Sin archivos de prueba**
- El directorio `data/` no se incluye en el ejecutable
- Debes proporcionar tus propios archivos de entrada
- Puedes obtener los archivos de prueba del repositorio

### 📦 Distribución

Si quieres compartir el ejecutable:
1. Comprime el archivo `.exe` (Windows) o el binario (Linux)
2. Incluye esta guía de uso
3. Opcionalmente, incluye archivos de prueba de ejemplo
4. El ejecutable NO requiere Python instalado en el sistema destino

### 🆘 Soporte

Para reportar problemas o sugerencias:
- Repositorio: [GitHub](https://github.com/Frank-Totti/ADA-II-Algoritmo-mejora-sistema-de-matricula)
- Rama actual: `executable`

---

**Nota**: Este es un ejecutable standalone que no requiere instalación. Simplemente ejecuta y usa! 🎉
