/**
 * =============================================================================
 * FUNCIONES-GENERALES.JS - FUNCIONES UTILITARIAS GENERALES
 * =============================================================================
 * Este archivo contiene funciones JavaScript generales utilizadas en toda
 * la aplicación. Incluye:
 * - Funciones de API (fetch, manejo de errores)
 * - Funciones de interfaz (flash messages, validaciones)
 * - Funciones de utilidad general
 * =============================================================================
 */

// =============================================================================
// FUNCIONES DE API
// =============================================================================

/**
 * Función mejorada para hacer peticiones a la API
 * Maneja automáticamente headers, errores y respuestas
 * @param {string} url - URL de la API
 * @param {Object} options - Opciones de la petición (method, body, headers)
 * @returns {Promise} Respuesta de la API parseada como JSON
 */
async function apiFetch(url, options = {}) {
    const headers = options.headers || {};
    
    // Agregar Content-Type automáticamente si hay body y no se especifica
    if (options.body && !headers['Content-Type']) {
        headers['Content-Type'] = 'application/json';
    }
    
    console.log(`DEBUG: Realizando petición ${options.method || 'GET'} a ${url}`);
    
    try {
        const response = await fetch(url, { ...options, headers });
        
        // Si es respuesta 204 (No Content), no hay JSON
        if (response.status === 204) {
            console.log('DEBUG: Respuesta 204 - Sin contenido');
            return null;
        }
        
        let data = null;
        try {
            data = await response.json();
        } catch (e) {
            console.error("ERROR: No se pudo parsear el JSON de la respuesta", e);
            // Continuar sin datos si no hay JSON válido
        }
        
        // Verificar si la respuesta es exitosa
        if (!response.ok) {
            const message = (data && (data.error || data.message)) || `Error HTTP ${response.status}`;
            const error = new Error(message);
            error.status = response.status;
            error.data = data;
            console.error('ERROR: Petición fallida:', error);
            throw error;
        }
        
        console.log('DEBUG: Petición exitosa:', data);
        return data;
        
    } catch (error) {
        console.error('ERROR: Fallo en petición API:', error);
        throw error;
    }
}

// =============================================================================
// FUNCIONES DE INTERFAZ DE USUARIO
// =============================================================================

/**
 * Muestra un mensaje flash al usuario
 * @param {string} message - Mensaje a mostrar
 * @param {string} category - Categoría del mensaje (success, danger, warning, info)
 * @param {number} duration - Duración en milisegundos (por defecto 3500)
 */
function showFlash(message, category = 'info', duration = 3500) {
    const container = document.querySelector('main.container');
    if (!container) {
        console.warn('WARNING: No se encontró el contenedor main.container para mostrar flash');
        return;
    }
    
    // Crear elemento del mensaje
    const div = document.createElement('div');
    div.className = `alert alert-${category} mt-2`;
    div.setAttribute('role', 'alert');
    div.textContent = message;
    
    // Agregar botón de cerrar
    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'btn-close';
    closeButton.setAttribute('aria-label', 'Cerrar');
    closeButton.onclick = () => div.remove();
    div.appendChild(closeButton);
    
    // Insertar al principio del contenedor
    container.prepend(div);
    
    // Auto-remover después del tiempo especificado
    if (duration > 0) {
        setTimeout(() => {
            if (div.parentNode) {
                div.remove();
            }
        }, duration);
    }
    
    console.log(`DEBUG: Flash message mostrado - ${category}: ${message}`);
}

/**
 * Valida un formulario y muestra errores si los hay
 * @param {HTMLFormElement} form - Formulario a validar
 * @param {Object} rules - Reglas de validación
 * @returns {boolean} true si el formulario es válido
 */
function validarFormulario(form, rules = {}) {
    let esValido = true;
    const errores = [];
    
    // Validar campos requeridos
    const camposRequeridos = form.querySelectorAll('[required]');
    camposRequeridos.forEach(campo => {
        if (!campo.value.trim()) {
            esValido = false;
            errores.push(`El campo "${campo.name || campo.id}" es obligatorio`);
        }
    });
    
    // Validar reglas personalizadas
    Object.keys(rules).forEach(campoId => {
        const campo = form.querySelector(`[name="${campoId}"], #${campoId}`);
        if (campo) {
            const regla = rules[campoId];
            if (regla.required && !campo.value.trim()) {
                esValido = false;
                errores.push(regla.message || `El campo ${campoId} es obligatorio`);
            }
            if (regla.pattern && !regla.pattern.test(campo.value)) {
                esValido = false;
                errores.push(regla.message || `El campo ${campoId} tiene un formato inválido`);
            }
        }
    });
    
    // Mostrar errores si los hay
    if (!esValido) {
        showFlash(errores.join('. '), 'danger');
    }
    
    return esValido;
}

/**
 * Limpia todos los mensajes flash de la página
 */
function limpiarFlashMessages() {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(msg => msg.remove());
}

// =============================================================================
// FUNCIONES DE UTILIDAD
// =============================================================================

/**
 * Formatea una fecha para mostrar en la interfaz
 * @param {string|Date} fecha - Fecha a formatear
 * @param {string} formato - Formato deseado ('short', 'long', 'time')
 * @returns {string} Fecha formateada
 */
function formatearFecha(fecha, formato = 'short') {
    if (!fecha) return '';
    
    const fechaObj = new Date(fecha);
    if (isNaN(fechaObj.getTime())) return '';
    
    const opciones = {
        short: { 
            year: 'numeric', 
            month: '2-digit', 
            day: '2-digit' 
        },
        long: { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        },
        time: { 
            hour: '2-digit', 
            minute: '2-digit' 
        }
    };
    
    return fechaObj.toLocaleDateString('es-ES', opciones[formato] || opciones.short);
}

/**
 * Formatea un número como tiempo estimado (minutos a horas:minutos)
 * @param {number} minutos - Minutos a formatear
 * @returns {string} Tiempo formateado
 */
function formatearTiempoEstimado(minutos) {
    if (!minutos || minutos <= 0) return 'Sin estimar';
    
    const horas = Math.floor(minutos / 60);
    const mins = minutos % 60;
    
    if (horas > 0) {
        return mins > 0 ? `${horas}h ${mins}m` : `${horas}h`;
    }
    return `${mins}m`;
}

/**
 * Obtiene el texto de estado formateado
 * @param {string} estado - Estado de la tarea
 * @returns {string} Texto formateado del estado
 */
function formatearEstado(estado) {
    const estados = {
        'pendiente': 'Pendiente',
        'en_progreso': 'En Progreso',
        'completada': 'Completada'
    };
    return estados[estado] || estado;
}

/**
 * Obtiene el texto de prioridad formateado
 * @param {string} prioridad - Prioridad de la tarea
 * @returns {string} Texto formateado de la prioridad
 */
function formatearPrioridad(prioridad) {
    const prioridades = {
        'baja': 'Baja',
        'media': 'Media',
        'alta': 'Alta'
    };
    return prioridades[prioridad] || prioridad;
}

/**
 * Debounce function - retrasa la ejecución de una función
 * @param {Function} func - Función a ejecutar
 * @param {number} wait - Tiempo de espera en milisegundos
 * @returns {Function} Función con debounce aplicado
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Throttle function - limita la frecuencia de ejecución de una función
 * @param {Function} func - Función a ejecutar
 * @param {number} limit - Límite de tiempo en milisegundos
 * @returns {Function} Función con throttle aplicado
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// =============================================================================
// FUNCIONES DE MANEJO DE EVENTOS
// =============================================================================

/**
 * Agrega un event listener con cleanup automático
 * @param {Element} element - Elemento al que agregar el listener
 * @param {string} event - Tipo de evento
 * @param {Function} handler - Función manejadora
 * @param {Object} options - Opciones del event listener
 * @returns {Function} Función para remover el listener
 */
function addEventListenerWithCleanup(element, event, handler, options = {}) {
    element.addEventListener(event, handler, options);
    
    // Retornar función de cleanup
    return () => {
        element.removeEventListener(event, handler, options);
    };
}

/**
 * Maneja clicks fuera de un elemento
 * @param {Element} element - Elemento de referencia
 * @param {Function} callback - Función a ejecutar cuando se hace click fuera
 * @returns {Function} Función para limpiar el listener
 */
function onClickOutside(element, callback) {
    const handleClick = (event) => {
        if (!element.contains(event.target)) {
            callback();
        }
    };
    
    document.addEventListener('click', handleClick);
    
    // Retornar función de cleanup
    return () => {
        document.removeEventListener('click', handleClick);
    };
}

// =============================================================================
// FUNCIONES DE INICIALIZACIÓN
// =============================================================================

/**
 * Inicializa funciones generales cuando el DOM esté listo
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('DEBUG: Funciones generales inicializadas');
    
    // Configurar tooltips de Bootstrap si están disponibles
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Configurar popovers de Bootstrap si están disponibles
    if (typeof bootstrap !== 'undefined' && bootstrap.Popover) {
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }
});
