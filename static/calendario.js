/**
 * =============================================================================
 * CALENDARIO.JS - CALENDARIO SIMPLE PARA PRINCIPIANTES
 * =============================================================================
 * Este archivo contiene las funciones básicas para manejar el calendario
 * de tareas. Diseñado para ser fácil de entender y modificar.
 * =============================================================================
 */

// Variables globales
let calendar;
let eventoSeleccionado = null;

// =============================================================================
// FUNCIONES DE UTILIDAD
// =============================================================================

/**
 * Obtiene el color según la prioridad de la tarea
 */
function obtenerColor(prioridad) {
    const colores = {
        "alta": "#dc3545",    // Rojo
        "media": "#ffc107",   // Amarillo  
        "baja": "#28a745"     // Verde
    };
    return colores[prioridad] || "#007bff"; // Azul por defecto
}

/**
 * Convierte una tarea en un evento del calendario
 */
function crearEvento(tarea) {
    // Determinar qué fecha usar y formatearla correctamente
    let fecha;
    
    if (tarea.completado_en) {
        // Si está completada, usar la fecha de completado
        fecha = tarea.completado_en;
    } else if (tarea.fecha_limite) {
        // Si tiene fecha límite, usarla
        fecha = tarea.fecha_limite;
        // Asegurar que tenga formato completo de fecha
        if (!fecha.includes('T')) {
            fecha = fecha + 'T09:00:00';
        } else if (!fecha.includes(':')) {
            fecha = fecha + ':00';
        }
        // Si la fecha límite está en el futuro, usar fecha de creación en su lugar
        const fechaLimite = new Date(fecha);
        const hoy = new Date();
        if (fechaLimite > hoy) {
            console.log(`DEBUG: Fecha límite ${fecha} está en el futuro, usando fecha de creación`);
            fecha = tarea.fecha_creacion;
        }
    } else {
        // Usar fecha de creación como último recurso
        fecha = tarea.fecha_creacion;
    }
    
    // Crear título simple
    const titulo = tarea.nombre;
    
    // Color según prioridad
    let color = obtenerColor(tarea.prioridad);
    
    // Si está completada, usar gris
    if (tarea.estado === "completada") {
        color = "#6c757d";
    }
    
    console.log(`DEBUG: Creando evento para tarea ${tarea.id}:`, {
        nombre: tarea.nombre,
        fecha: fecha,
        estado: tarea.estado
    });
    
    return {
        id: tarea.id,
        title: titulo,
        start: fecha,
        allDay: false, // Mostrar por hora
        backgroundColor: color,
        borderColor: color,
        textColor: "#ffffff",
        extendedProps: {
            categoria: tarea.categoria,
            prioridad: tarea.prioridad,
            estado: tarea.estado,
            tiempo_estimado: tarea.tiempo_estimado,
            fecha_limite: tarea.fecha_limite,
            nombre_original: tarea.nombre
        }
    };
}

/**
 * Carga las tareas desde el servidor
 */
async function cargarTareas() {
    try {
        console.log('DEBUG: Cargando tareas desde /api/tareas');
        const response = await apiFetch('/api/tareas');
        console.log('DEBUG: Respuesta de API:', response);
        
        const eventos = response.map(tarea => crearEvento(tarea));
        console.log('DEBUG: Eventos creados:', eventos);
        
        return eventos;
    } catch (error) {
        console.error('Error al cargar tareas:', error);
        showFlash('Error al cargar las tareas', 'danger');
        return [];
    }
}

// =============================================================================
// INICIALIZACIÓN DEL CALENDARIO
// =============================================================================

/**
 * Inicializa el calendario
 */
function inicializarCalendario() {
    const calendarEl = document.getElementById('calendar');
    
    if (!calendarEl) {
        console.error('No se encontró el elemento #calendar');
        return;
    }
    
    calendar = new FullCalendar.Calendar(calendarEl, {
        // Vista inicial
        initialView: 'timeGridWeek',
        locale: 'es',
        initialDate: '2025-09-18', // Mostrar la fecha de las tareas
        
        // Barra de herramientas
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        
        // Cargar eventos
        events: async function(info, successCallback, failureCallback) {
            try {
                console.log('DEBUG: FullCalendar solicitando eventos para rango:', info.start, 'a', info.end);
                const eventos = await cargarTareas();
                console.log('DEBUG: Enviando eventos a FullCalendar:', eventos);
                successCallback(eventos);
            } catch (error) {
                console.error('Error al cargar eventos:', error);
                failureCallback(error);
            }
        },
        
        // Configuración de tiempo
        slotMinTime: '08:00:00',
        slotMaxTime: '20:00:00',
        slotDuration: '01:00:00',
        eventTimeFormat: {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        },
        
        // Interacciones
        selectable: true,
        editable: true,
        
        // Eventos
        eventClick: function(info) {
            mostrarModalEvento(info.event);
        },
        
        dateClick: function(info) {
            crearNuevaTarea(info.dateStr);
        }
    });
    
    calendar.render();
}

// =============================================================================
// FUNCIONES DE MODALES
// =============================================================================

/**
 * Crea una nueva tarea
 */
function crearNuevaTarea(fecha = null) {
    alert('crearNuevaTarea');
    eventoSeleccionado = null;
    document.getElementById('eventoModalLabel').textContent = 'Nueva Tarea';
    document.getElementById('eventoForm').reset();
    
    if (fecha) {
        document.getElementById('eventoFechaInicio').value = fecha + 'T09:00';
    }
    
    const modal = new bootstrap.Modal(document.getElementById('eventoModal'));
    modal.show();
}

/**
 * Muestra el modal con las acciones del evento
 */
function mostrarModalEvento(evento) {
    eventoSeleccionado = evento;
    
    // Llenar información del evento
    document.getElementById('eventoInfoNombre').textContent = evento.title;
    document.getElementById('eventoInfoCategoria').textContent = evento.extendedProps.categoria || 'Sin categoría';
    document.getElementById('eventoInfoPrioridad').textContent = evento.extendedProps.prioridad || 'Sin prioridad';
    document.getElementById('eventoInfoEstado').textContent = evento.extendedProps.estado || 'pendiente';
    
    // Mostrar modal
    const modal = new bootstrap.Modal(document.getElementById('accionesModal'));
    modal.show();
}

// =============================================================================
// FUNCIONES DE ACCIONES
// =============================================================================

/**
 * Guarda una nueva tarea
 */
async function guardarTarea() {
    const form = document.getElementById('eventoForm');
    const formData = new FormData(form);
    
    const datos = {
        nombre: formData.get('nombre'),
        categoria: formData.get('categoria'),
        prioridad: formData.get('prioridad') || null,
        tiempo_estimado: formData.get('tiempo_estimado') ? parseInt(formData.get('tiempo_estimado')) : null,
        estado: formData.get('estado'),
        fecha_limite: formData.get('fecha_limite') || null
    };
    
    try {
        await crearTarea(datos);
        bootstrap.Modal.getInstance(document.getElementById('eventoModal')).hide();
        calendar.refetchEvents();
    } catch (error) {
        console.error('Error al guardar tarea:', error);
    }
}

/**
 * Edita una tarea existente
 */
function editarTarea() {
    if (!eventoSeleccionado) return;
    
    // Llenar formulario con datos del evento
    document.getElementById('eventoId').value = eventoSeleccionado.id;
    document.getElementById('eventoNombre').value = eventoSeleccionado.extendedProps.nombre_original;
    document.getElementById('eventoCategoria').value = eventoSeleccionado.extendedProps.categoria || '';
    document.getElementById('eventoPrioridad').value = eventoSeleccionado.extendedProps.prioridad || '';
    document.getElementById('eventoTiempoEstimado').value = eventoSeleccionado.extendedProps.tiempo_estimado || '';
    document.getElementById('eventoEstado').value = eventoSeleccionado.extendedProps.estado || 'pendiente';
    
    // Cerrar modal de acciones y abrir modal de edición
    bootstrap.Modal.getInstance(document.getElementById('accionesModal')).hide();
    const modal = new bootstrap.Modal(document.getElementById('eventoModal'));
    modal.show();
}

/**
 * Alterna el estado de la tarea
 */
async function alternarEstado() {
    if (!eventoSeleccionado) return;
    
    try {
        await alternarEstadoTarea(eventoSeleccionado.id);
        bootstrap.Modal.getInstance(document.getElementById('accionesModal')).hide();
        calendar.refetchEvents();
    } catch (error) {
        console.error('Error al cambiar estado:', error);
    }
}

/**
 * Elimina una tarea
 */
async function eliminarTareaCalendario() {
    if (!eventoSeleccionado) return;
    
    if (confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
        try {
            await eliminarTarea(eventoSeleccionado.id);
            bootstrap.Modal.getInstance(document.getElementById('accionesModal')).hide();
            calendar.refetchEvents();
        } catch (error) {
            console.error('Error al eliminar tarea:', error);
        }
    }
}

/**
 * Confirma la eliminación de una tarea (para modal de confirmación)
 */
async function confirmarEliminacion() {
    if (!eventoSeleccionado) return;
    
    try {
        await eliminarTarea(eventoSeleccionado.id);
        bootstrap.Modal.getInstance(document.getElementById('accionesModal')).hide();
        calendar.refetchEvents();
    } catch (error) {
        console.error('Error al eliminar tarea:', error);
    }
}

// =============================================================================
// INICIALIZACIÓN
// =============================================================================

/**
 * Inicializa el calendario cuando el DOM esté listo
 */
document.addEventListener('DOMContentLoaded', function() {
    inicializarCalendario();
});
