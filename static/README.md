# Estructura de Archivos JavaScript

Esta carpeta contiene los archivos JavaScript organizados de manera modular para facilitar el mantenimiento y la comprensión del código.

## Archivos

### `app.js`
Archivo principal de JavaScript que mantiene compatibilidad hacia atrás. Contiene funciones básicas de API y flash messages como respaldo.

### `funciones-generales.js`
Funciones utilitarias generales utilizadas en toda la aplicación:
- **API**: `apiFetch()` - Función mejorada para peticiones HTTP
- **UI**: `showFlash()` - Mensajes flash al usuario
- **Validación**: `validarFormulario()` - Validación de formularios
- **Utilidades**: Formateo de fechas, tiempo, estados, etc.
- **Eventos**: Manejo de event listeners con cleanup automático

### `tareas.js`
Funciones específicas para el manejo de tareas:
- **Validación**: `validarDatosTarea()` - Validación específica de tareas
- **CRUD**: `crearTarea()`, `actualizarTarea()`, `eliminarTarea()`, `alternarEstadoTarea()`
- **Formularios**: `manejarEnvioFormulario()`, `configurarFormularioTarea()`
- **Filtrado**: `filtrarTareas()`, `ordenarTareas()`

### `calendario.js`
Funciones específicas para el calendario de tareas con FullCalendar:
- **Inicialización**: `inicializarCalendario()` - Configuración de FullCalendar
- **Transformación**: `transformarTareaAEvento()` - Convierte datos JSON a eventos
- **Carga**: `cargarEventosDelServidor()` - Obtiene y procesa datos del servidor
- **Modales**: `crearNuevaTarea()`, `editarTarea()`
- **CRUD**: `guardarTarea()`, `alternarEstado()`, `eliminarTarea()`
- **UI**: `mostrarMenuEvento()` - Menú contextual para eventos

## Flujo de Datos

1. **Servidor** (`app.py`): Devuelve JSON limpio sin formato específico
2. **Cliente** (`calendario.js`): Transforma JSON en eventos de FullCalendar
3. **Procesamiento**: Los datos se procesan en JavaScript según las necesidades de la UI

## Ventajas de esta Estructura

- **Separación de responsabilidades**: Cada archivo tiene un propósito específico
- **Mantenibilidad**: Código organizado y bien documentado
- **Reutilización**: Funciones generales pueden usarse en múltiples vistas
- **Compatibilidad**: El archivo original `app.js` mantiene compatibilidad hacia atrás
- **Escalabilidad**: Fácil agregar nuevas funcionalidades sin afectar código existente

## Uso

Los archivos se cargan automáticamente en el `layout.html` en el siguiente orden:
1. `funciones-generales.js` - Funciones base
2. `tareas.js` - Funciones específicas de tareas
3. `app.js` - Compatibilidad hacia atrás

Cada archivo se inicializa automáticamente cuando el DOM está listo.
