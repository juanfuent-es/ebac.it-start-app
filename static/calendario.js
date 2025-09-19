/**
 * =============================================================================
 * CALENDARIO.JS - FUNCIONES PARA EL CALENDARIO DE TAREAS
 * =============================================================================
 * Este archivo contiene todas las funciones JavaScript necesarias para manejar
 * el calendario de tareas con FullCalendar. Incluye:
 * - Inicialización del calendario
 * - Transformación de datos JSON a eventos de FullCalendar
 * - Manejo de eventos (crear, editar, eliminar)
 * - Funciones de utilidad para colores y fechas
 * =============================================================================
 */

// =============================================================================
// VARIABLES GLOBALES
// =============================================================================
let calendar;
let eventoActual = null;
let eventoAEliminar = null;

// =============================================================================
// FUNCIONES DE UTILIDAD
// =============================================================================

/**
 * Obtiene el color correspondiente a la prioridad de una tarea
 * @param {string} prioridad - Prioridad de la tarea (alta, media, baja)
 * @returns {string} Color hexadecimal
 */
function getColorPrioridad(prioridad) {
    const colores = {
        "alta": "#dc3545",    // Rojo
        "media": "#ffc107",   // Amarillo
        "baja": "#28a745"     // Verde
    };
    return colores[prioridad] || "#007bff"; // Azul por defecto
}

/**
 * Obtiene el color de texto según la prioridad
 * @param {string} prioridad - Prioridad de la tarea
 * @returns {string} Color de texto
 */
function getTextColorPrioridad(prioridad) {
    return prioridad === "media" ? "#000000" : "#ffffff";
}

/**
 * Transforma una tarea del JSON en un evento de FullCalendar
 * @param {Object} tarea - Objeto tarea del servidor
 * @returns {Object} Evento formateado para FullCalendar
 */
function transformarTareaAEvento(tarea) {
    // Determinar la fecha de inicio para el evento
    // Si tiene fecha_limite, usar esa fecha; sino usar fecha_creacion
    const fechaInicio = tarea.fecha_limite || tarea.fecha_creacion;
    
    // Crear título informativo
    const titulo = tarea.fecha_limite 
        ? `${tarea.nombre} (Con fecha límite)`
        : `${tarea.nombre} (Sin fecha límite)`;
    
    // Configurar colores según prioridad
    let backgroundColor = getColorPrioridad(tarea.prioridad);
    let borderColor = getColorPrioridad(tarea.prioridad);
    let textColor = getTextColorPrioridad(tarea.prioridad);
    
    // Si la tarea está completada, cambiar a gris
    if (tarea.estado === "completada") {
        backgroundColor = "#6c757d";
        borderColor = "#6c757d";
        textColor = "#ffffff";
    }
    
    return {
        id: tarea.id,
        title: titulo,
        start: fechaInicio,
        allDay: true,
        backgroundColor: backgroundColor,
        borderColor: borderColor,
        textColor: textColor,
        extendedProps: {
            categoria: tarea.categoria,
            prioridad: tarea.prioridad,
            estado: tarea.estado,
            tiempo_estimado: tarea.tiempo_estimado,
            fecha_limite: tarea.fecha_limite,
            completado_en: tarea.completado_en,
            nombre_original: tarea.nombre // Guardar nombre original sin modificaciones
        }
    };
}

/**
 * Carga las tareas desde el servidor y las transforma en eventos del calendario
 * @returns {Promise<Array>} Array de eventos para FullCalendar
 */
async function cargarEventosDelServidor() {
    try {
        console.log('DEBUG: Cargando tareas desde el servidor...');
        const response = await apiFetch('/api/tareas');
        
        if (!Array.isArray(response)) {
            throw new Error('Respuesta del servidor no es un array');
        }
        
        console.log(`DEBUG: Se recibieron ${response.length} tareas del servidor`);
        
        // Transformar cada tarea en un evento de FullCalendar
        const eventos = response.map(tarea => {
            console.log(`DEBUG: Transformando tarea ${tarea.id}: "${tarea.nombre}"`);
            return transformarTareaAEvento(tarea);
        });
        
        console.log(`DEBUG: Se transformaron ${eventos.length} eventos para FullCalendar`);
        return eventos;
        
    } catch (error) {
        console.error('ERROR: No se pudieron cargar las tareas:', error);
        showFlash('Error al cargar las tareas del calendario', 'danger');
        return [];
    }
}

// =============================================================================
// INICIALIZACIÓN DEL CALENDARIO
// =============================================================================

/**
 * Inicializa el calendario FullCalendar
 */
function inicializarCalendario() {
    const calendarEl = document.getElementById('calendar');
    
    if (!calendarEl) {
        console.error('ERROR: No se encontró el elemento #calendar');
        return;
    }
    
    console.log('DEBUG: Inicializando FullCalendar...');
    
    calendar = new FullCalendar.Calendar(calendarEl, {
        // Configuración básica
        initialView: 'dayGridMonth',
        locale: 'es',
        
        // Barra de herramientas
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        
        // Cargar eventos usando función personalizada
        events: async function(info, successCallback, failureCallback) {
            try {
                const eventos = await cargarEventosDelServidor();
                successCallback(eventos);
            } catch (error) {
                console.error('ERROR: Fallo al cargar eventos:', error);
                failureCallback(error);
            }
        },
        
        // Formato de tiempo
        eventTimeFormat: {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        },
        
        // Configuración de eventos
        eventDisplay: 'block',
        eventColor: '#007bff',
        eventTextColor: '#ffffff',
        selectable: true,
        selectMirror: true,
        selectOverlap: false,
        editable: true,
        droppable: true,
        
        // Eventos del calendario
        eventClick: function(info) {
            mostrarMenuEvento(info.event, info.jsEvent);
        },
        
        dateClick: function(info) {
            abrirModalCrearEvento(info.dateStr);
        },
        
        eventDrop: function(info) {
            actualizarFechasEvento(info.event);
        },
        
        eventResize: function(info) {
            actualizarFechasEvento(info.event);
        },
        
        // Personalizar apariencia de eventos
        eventDidMount: function(info) {
            // El color ya está configurado en transformarTareaAEvento
            // Solo agregar tooltip con información adicional
            const prioridad = info.event.extendedProps.prioridad;
            const categoria = info.event.extendedProps.categoria;
            info.el.title = `${info.event.title}\nCategoría: ${categoria}\nPrioridad: ${prioridad || 'Sin especificar'}`;
        }
    });
    
    calendar.render();
    console.log('DEBUG: FullCalendar inicializado correctamente');
}

// =============================================================================
// FUNCIONES DE MODALES
// =============================================================================

/**
 * Abre el modal para crear un nuevo evento
 * @param {string} fecha - Fecha en formato YYYY-MM-DD (opcional)
 */
function abrirModalCrearEvento(fecha = null) {
    eventoActual = null;
    document.getElementById('eventoModalLabel').textContent = 'Nueva Tarea';
    document.getElementById('eventoForm').reset();
    
    if (fecha) {
        document.getElementById('eventoFechaInicio').value = fecha + 'T09:00';
    }
    
    const modal = new bootstrap.Modal(document.getElementById('eventoModal'));
    modal.show();
}

/**
 * Abre el modal para editar un evento existente
 * @param {Object} evento - Evento de FullCalendar a editar
 */
function abrirModalEditarEvento(evento) {
    eventoActual = evento;
    document.getElementById('eventoModalLabel').textContent = 'Editar Tarea';
    
    // Llenar formulario con datos del evento
    document.getElementById('eventoId').value = evento.id;
    document.getElementById('eventoNombre').value = evento.extendedProps.nombre_original;
    document.getElementById('eventoCategoria').value = evento.extendedProps.categoria || '';
    document.getElementById('eventoPrioridad').value = evento.extendedProps.prioridad || '';
    document.getElementById('eventoTiempoEstimado').value = evento.extendedProps.tiempo_estimado || '';
    document.getElementById('eventoEstado').value = evento.extendedProps.estado || 'pendiente';
    
    // Formatear fechas para datetime-local
    if (evento.start) {
        const fechaInicio = new Date(evento.start);
        if (!evento.allDay) {
            fechaInicio.setMinutes(fechaInicio.getMinutes() - fechaInicio.getTimezoneOffset());
            document.getElementById('eventoFechaInicio').value = fechaInicio.toISOString().slice(0, 16);
        } else {
            document.getElementById('eventoFechaInicio').value = fechaInicio.toISOString().slice(0, 10) + 'T09:00';
        }
    }
    
    if (evento.extendedProps.fecha_limite) {
        const fechaLimite = new Date(evento.extendedProps.fecha_limite);
        fechaLimite.setMinutes(fechaLimite.getMinutes() - fechaLimite.getTimezoneOffset());
        document.getElementById('eventoFechaLimite').value = fechaLimite.toISOString().slice(0, 16);
    }
    
    const modal = new bootstrap.Modal(document.getElementById('eventoModal'));
    modal.show();
}

// =============================================================================
// FUNCIONES DE CRUD (CREAR, LEER, ACTUALIZAR, ELIMINAR)
// =============================================================================

/**
 * Guarda un evento (crear nuevo o actualizar existente)
 */
async function guardarEvento() {
    const form = document.getElementById('eventoForm');
    
    // Validar formulario antes de enviar
    if (!validarFormularioTarea(form)) {
        return;
    }
    
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
        let response;
        if (eventoActual) {
            // Actualizar evento existente
            console.log(`DEBUG: Actualizando tarea ${eventoActual.id}`);
            response = await actualizarTarea(eventoActual.id, datos);
        } else {
            // Crear nuevo evento
            console.log('DEBUG: Creando nueva tarea');
            response = await crearTarea(datos);
        }
        
        // Cerrar modal y recargar calendario
        bootstrap.Modal.getInstance(document.getElementById('eventoModal')).hide();
        calendar.refetchEvents();
        
    } catch (error) {
        console.error('ERROR: Fallo al guardar tarea:', error);
        // El error ya se mostró en las funciones específicas
    }
}

/**
 * Actualiza las fechas de un evento cuando se arrastra o redimensiona
 * @param {Object} evento - Evento de FullCalendar
 */
async function actualizarFechasEvento(evento) {
    const datos = {
        nombre: evento.extendedProps.nombre_original,
        categoria: evento.extendedProps.categoria,
        fecha_limite: evento.end ? evento.end.toISOString() : evento.start.toISOString(),
        prioridad: evento.extendedProps.prioridad,
        tiempo_estimado: evento.extendedProps.tiempo_estimado
    };
    
    try {
        console.log(`DEBUG: Actualizando fechas de tarea ${evento.id}`);
        await actualizarTarea(evento.id, datos);
    } catch (error) {
        console.error('ERROR: Fallo al actualizar fechas:', error);
        calendar.refetchEvents(); // Recargar para revertir cambios
    }
}

/**
 * Elimina un evento (con confirmación)
 * @param {Object} evento - Evento de FullCalendar a eliminar
 */
function eliminarEvento(evento) {
    eventoAEliminar = evento;
    const modal = new bootstrap.Modal(document.getElementById('eliminarModal'));
    modal.show();
}

/**
 * Confirma la eliminación de un evento
 */
async function confirmarEliminacion() {
    if (!eventoAEliminar) return;
    
    try {
        console.log(`DEBUG: Eliminando tarea ${eventoAEliminar.id}`);
        await eliminarTarea(eventoAEliminar.id);
        
        bootstrap.Modal.getInstance(document.getElementById('eliminarModal')).hide();
        calendar.refetchEvents();
        eventoAEliminar = null;
        
    } catch (error) {
        console.error('ERROR: Fallo al eliminar tarea:', error);
        // El error ya se mostró en la función eliminarTarea
    }
}

/**
 * Alterna el estado de un evento entre pendiente y completada
 * @param {Object} evento - Evento de FullCalendar
 */
async function alternarEstadoEvento(evento) {
    try {
        console.log(`DEBUG: Alternando estado de tarea ${evento.id}`);
        await alternarEstadoTarea(evento.id);
        calendar.refetchEvents();
        
    } catch (error) {
        console.error('ERROR: Fallo al cambiar estado:', error);
        // El error ya se mostró en la función alternarEstadoTarea
    }
}

// =============================================================================
// FUNCIONES DE INTERFAZ DE USUARIO
// =============================================================================

/**
 * Muestra un menú contextual para eventos con opciones de edición
 * @param {Object} evento - Evento de FullCalendar
 * @param {Event} jsEvent - Evento JavaScript del click
 */
function mostrarMenuEvento(evento, jsEvent) {
    const menu = document.createElement('div');
    menu.className = 'dropdown-menu show position-absolute';
    menu.style.left = jsEvent.pageX + 'px';
    menu.style.top = jsEvent.pageY + 'px';
    menu.style.zIndex = '9999';
    
    const opciones = [
        { 
            text: 'Editar', 
            icon: 'bi-pencil-square', 
            action: () => abrirModalEditarEvento(evento) 
        },
        { 
            text: 'Alternar Estado', 
            icon: 'bi-check-circle', 
            action: () => alternarEstadoEvento(evento) 
        },
        { 
            text: 'Eliminar', 
            icon: 'bi-trash', 
            action: () => eliminarEvento(evento), 
            class: 'text-danger' 
        }
    ];
    
    opciones.forEach(opcion => {
        const item = document.createElement('a');
        item.className = `dropdown-item ${opcion.class || ''}`;
        item.href = '#';
        item.innerHTML = `<i class="${opcion.icon} me-2"></i>${opcion.text}`;
        item.onclick = (e) => {
            e.preventDefault();
            opcion.action();
            menu.remove();
        };
        menu.appendChild(item);
    });
    
    document.body.appendChild(menu);
    
    // Cerrar menú al hacer clic fuera
    setTimeout(() => {
        document.addEventListener('click', function cerrarMenu() {
            menu.remove();
            document.removeEventListener('click', cerrarMenu);
        });
    }, 100);
}

// =============================================================================
// INICIALIZACIÓN CUANDO EL DOM ESTÉ LISTO
// =============================================================================

/**
 * Inicializa el calendario cuando el DOM esté completamente cargado
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('DEBUG: DOM cargado, inicializando calendario...');
    inicializarCalendario();
});
