/**
 * =============================================================================
 * TAREAS.JS - FUNCIONES ESPECÍFICAS PARA MANEJO DE TAREAS
 * =============================================================================
 * Este archivo contiene funciones JavaScript específicas para el manejo
 * de tareas en las vistas de lista, formularios, etc. Incluye:
 * - Funciones de CRUD para tareas
 * - Validaciones específicas de tareas
 * - Manejo de formularios de tareas
 * - Funciones de filtrado y búsqueda
 * =============================================================================
 */

// =============================================================================
// FUNCIONES DE VALIDACIÓN DE TAREAS
// =============================================================================

/**
 * Valida los datos de una tarea antes de enviarlos al servidor
 * @param {Object} datos - Datos de la tarea a validar
 * @returns {Object} Objeto con {valido: boolean, errores: array}
 */
function validarDatosTarea(datos) {
    const errores = [];
    
    // Validar nombre (obligatorio)
    if (!datos.nombre || datos.nombre.trim() === '') {
        errores.push('El nombre de la tarea es obligatorio');
    }
    
    // Validar categoría (obligatorio)
    if (!datos.categoria || datos.categoria.trim() === '') {
        errores.push('La categoría es obligatoria');
    }
    
    // Validar prioridad
    if (datos.prioridad && !['baja', 'media', 'alta'].includes(datos.prioridad)) {
        errores.push('La prioridad debe ser: baja, media o alta');
    }
    
    // Validar tiempo estimado
    if (datos.tiempo_estimado !== null && datos.tiempo_estimado !== undefined) {
        const tiempo = parseInt(datos.tiempo_estimado);
        if (isNaN(tiempo) || tiempo < 0) {
            errores.push('El tiempo estimado debe ser un número positivo');
        }
    }
    
    // Validar fecha límite
    if (datos.fecha_limite) {
        const fecha = new Date(datos.fecha_limite);
        if (isNaN(fecha.getTime())) {
            errores.push('La fecha límite tiene un formato inválido');
        }
    }
    
    return {
        valido: errores.length === 0,
        errores: errores
    };
}

/**
 * Valida un formulario de tarea
 * @param {HTMLFormElement} form - Formulario a validar
 * @returns {boolean} true si el formulario es válido
 */
function validarFormularioTarea(form) {
    const formData = new FormData(form);
    const datos = {
        nombre: formData.get('title') || formData.get('nombre'),
        categoria: formData.get('categoria'),
        prioridad: formData.get('prioridad') || null,
        tiempo_estimado: formData.get('tiempo_estimado') || null,
        fecha_limite: formData.get('fecha_limite') || null
    };
    
    const validacion = validarDatosTarea(datos);
    
    if (!validacion.valido) {
        showFlash(validacion.errores.join('. '), 'danger');
        return false;
    }
    
    return true;
}

// =============================================================================
// FUNCIONES DE CRUD DE TAREAS
// =============================================================================

/**
 * Crea una nueva tarea
 * @param {Object} datos - Datos de la tarea
 * @returns {Promise<Object>} Tarea creada
 */
async function crearTarea(datos) {
    console.log('DEBUG: Creando nueva tarea:', datos);
    
    // Validar datos antes de enviar
    const validacion = validarDatosTarea(datos);
    if (!validacion.valido) {
        throw new Error(validacion.errores.join('. '));
    }
    
    try {
        const response = await apiFetch('/api/tareas', {
            method: 'POST',
            body: JSON.stringify(datos)
        });
        
        console.log('DEBUG: Tarea creada exitosamente:', response);
        showFlash('Tarea creada correctamente', 'success');
        return response;
        
    } catch (error) {
        console.error('ERROR: Fallo al crear tarea:', error);
        showFlash(error.message || 'Error al crear la tarea', 'danger');
        throw error;
    }
}

/**
 * Actualiza una tarea existente
 * @param {number} id - ID de la tarea
 * @param {Object} datos - Datos actualizados
 * @returns {Promise<Object>} Tarea actualizada
 */
async function actualizarTarea(id, datos) {
    console.log(`DEBUG: Actualizando tarea ${id}:`, datos);
    
    // Validar datos antes de enviar
    const validacion = validarDatosTarea(datos);
    if (!validacion.valido) {
        throw new Error(validacion.errores.join('. '));
    }
    
    try {
        const response = await apiFetch(`/api/tarea/${id}`, {
            method: 'PUT',
            body: JSON.stringify(datos)
        });
        
        console.log('DEBUG: Tarea actualizada exitosamente:', response);
        showFlash('Tarea actualizada correctamente', 'success');
        return response;
        
    } catch (error) {
        console.error('ERROR: Fallo al actualizar tarea:', error);
        showFlash(error.message || 'Error al actualizar la tarea', 'danger');
        throw error;
    }
}

/**
 * Elimina una tarea
 * @param {number} id - ID de la tarea
 * @returns {Promise<void>}
 */
async function eliminarTarea(id) {
    console.log(`DEBUG: Eliminando tarea ${id}`);
    
    try {
        await apiFetch(`/api/tarea/${id}`, {
            method: 'DELETE'
        });
        
        console.log('DEBUG: Tarea eliminada exitosamente');
        showFlash('Tarea eliminada correctamente', 'success');
        
    } catch (error) {
        console.error('ERROR: Fallo al eliminar tarea:', error);
        showFlash(error.message || 'Error al eliminar la tarea', 'danger');
        throw error;
    }
}

/**
 * Alterna el estado de una tarea
 * @param {number} id - ID de la tarea
 * @returns {Promise<Object>} Tarea con estado actualizado
 */
async function alternarEstadoTarea(id) {
    console.log(`DEBUG: Alternando estado de tarea ${id}`);
    
    try {
        const response = await apiFetch(`/api/tarea/${id}/toggle-estado`, {
            method: 'POST'
        });
        
        console.log('DEBUG: Estado de tarea alternado exitosamente:', response);
        showFlash(`Tarea marcada como ${response.estado}`, 'success');
        return response;
        
    } catch (error) {
        console.error('ERROR: Fallo al alternar estado:', error);
        showFlash(error.message || 'Error al cambiar el estado', 'danger');
        throw error;
    }
}

// =============================================================================
// FUNCIONES DE MANEJO DE FORMULARIOS
// =============================================================================

/**
 * Maneja el envío de un formulario de tarea
 * @param {Event} event - Evento de envío del formulario
 * @param {string} tipo - Tipo de operación ('crear' o 'editar')
 * @param {number} id - ID de la tarea (solo para editar)
 */
async function manejarEnvioFormulario(event, tipo = 'crear', id = null) {
    event.preventDefault();
    
    const form = event.target;
    
    // Validar formulario
    if (!validarFormularioTarea(form)) {
        return;
    }
    
    // Obtener datos del formulario
    const formData = new FormData(form);
    const datos = {
        nombre: formData.get('title') || formData.get('nombre'),
        categoria: formData.get('categoria'),
        prioridad: formData.get('prioridad') || null,
        tiempo_estimado: formData.get('tiempo_estimado') ? parseInt(formData.get('tiempo_estimado')) : null,
        fecha_limite: formData.get('fecha_limite') || null
    };
    
    try {
        if (tipo === 'crear') {
            await crearTarea(datos);
            // Redirigir o limpiar formulario según sea necesario
            if (form.reset) {
                form.reset();
            }
        } else if (tipo === 'editar' && id) {
            await actualizarTarea(id, datos);
            // Redirigir a la vista de detalle o lista
            window.location.href = `/tarea/${id}`;
        }
        
    } catch (error) {
        console.error('ERROR: Fallo en manejo de formulario:', error);
        // El error ya se mostró en las funciones específicas
    }
}

/**
 * Configura los event listeners para un formulario de tarea
 * @param {HTMLFormElement} form - Formulario a configurar
 * @param {string} tipo - Tipo de operación ('crear' o 'editar')
 * @param {number} id - ID de la tarea (solo para editar)
 */
function configurarFormularioTarea(form, tipo = 'crear', id = null) {
    if (!form) {
        console.warn('WARNING: No se encontró el formulario para configurar');
        return;
    }
    
    // Configurar envío del formulario
    form.addEventListener('submit', (event) => {
        manejarEnvioFormulario(event, tipo, id);
    });
    
    // Configurar validación en tiempo real
    const campos = form.querySelectorAll('input, select, textarea');
    campos.forEach(campo => {
        campo.addEventListener('blur', () => {
            // Validar campo individual
            if (campo.hasAttribute('required') && !campo.value.trim()) {
                campo.classList.add('is-invalid');
            } else {
                campo.classList.remove('is-invalid');
            }
        });
        
        campo.addEventListener('input', () => {
            campo.classList.remove('is-invalid');
        });
    });
    
    console.log(`DEBUG: Formulario de tarea configurado para ${tipo}`);
}

// =============================================================================
// FUNCIONES DE FILTRADO Y BÚSQUEDA
// =============================================================================

/**
 * Filtra tareas por criterios específicos
 * @param {Array} tareas - Array de tareas
 * @param {Object} filtros - Objeto con criterios de filtrado
 * @returns {Array} Tareas filtradas
 */
function filtrarTareas(tareas, filtros = {}) {
    return tareas.filter(tarea => {
        // Filtro por estado
        if (filtros.estado && tarea.estado !== filtros.estado) {
            return false;
        }
        
        // Filtro por prioridad
        if (filtros.prioridad && tarea.prioridad !== filtros.prioridad) {
            return false;
        }
        
        // Filtro por categoría
        if (filtros.categoria && tarea.categoria !== filtros.categoria) {
            return false;
        }
        
        // Filtro por texto (buscar en nombre)
        if (filtros.texto) {
            const texto = filtros.texto.toLowerCase();
            if (!tarea.nombre.toLowerCase().includes(texto)) {
                return false;
            }
        }
        
        // Filtro por fecha
        if (filtros.fecha_desde || filtros.fecha_hasta) {
            const fechaTarea = new Date(tarea.fecha_creacion);
            
            if (filtros.fecha_desde) {
                const fechaDesde = new Date(filtros.fecha_desde);
                if (fechaTarea < fechaDesde) {
                    return false;
                }
            }
            
            if (filtros.fecha_hasta) {
                const fechaHasta = new Date(filtros.fecha_hasta);
                if (fechaTarea > fechaHasta) {
                    return false;
                }
            }
        }
        
        return true;
    });
}

/**
 * Ordena tareas según un criterio
 * @param {Array} tareas - Array de tareas
 * @param {string} criterio - Criterio de ordenamiento
 * @param {string} direccion - Dirección del ordenamiento ('asc' o 'desc')
 * @returns {Array} Tareas ordenadas
 */
function ordenarTareas(tareas, criterio = 'fecha_creacion', direccion = 'desc') {
    return tareas.sort((a, b) => {
        let valorA, valorB;
        
        switch (criterio) {
            case 'nombre':
                valorA = a.nombre.toLowerCase();
                valorB = b.nombre.toLowerCase();
                break;
            case 'prioridad':
                const prioridades = { 'alta': 3, 'media': 2, 'baja': 1 };
                valorA = prioridades[a.prioridad] || 0;
                valorB = prioridades[b.prioridad] || 0;
                break;
            case 'estado':
                valorA = a.estado;
                valorB = b.estado;
                break;
            case 'fecha_creacion':
            default:
                valorA = new Date(a.fecha_creacion);
                valorB = new Date(b.fecha_creacion);
                break;
        }
        
        if (direccion === 'asc') {
            return valorA > valorB ? 1 : -1;
        } else {
            return valorA < valorB ? 1 : -1;
        }
    });
}

// =============================================================================
// FUNCIONES DE INICIALIZACIÓN
// =============================================================================

/**
 * Inicializa las funciones de tareas cuando el DOM esté listo
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('DEBUG: Funciones de tareas inicializadas');
    
    // Configurar formularios de tarea automáticamente
    const formulariosTarea = document.querySelectorAll('form[data-tipo="tarea"]');
    formulariosTarea.forEach(form => {
        const tipo = form.dataset.operacion || 'crear';
        const id = form.dataset.id ? parseInt(form.dataset.id) : null;
        configurarFormularioTarea(form, tipo, id);
    });
    
    // Configurar botones de alternar estado
    const botonesToggle = document.querySelectorAll('[data-action="toggle-estado"]');
    botonesToggle.forEach(boton => {
        boton.addEventListener('click', async (event) => {
            event.preventDefault();
            const id = parseInt(boton.dataset.id);
            if (id) {
                try {
                    await alternarEstadoTarea(id);
                    // Recargar la página o actualizar la vista
                    location.reload();
                } catch (error) {
                    console.error('ERROR: Fallo al alternar estado:', error);
                }
            }
        });
    });
    
    // Configurar botones de eliminar
    const botonesEliminar = document.querySelectorAll('[data-action="eliminar"]');
    botonesEliminar.forEach(boton => {
        boton.addEventListener('click', async (event) => {
            event.preventDefault();
            const id = parseInt(boton.dataset.id);
            if (id && confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
                try {
                    await eliminarTarea(id);
                    // Recargar la página o actualizar la vista
                    location.reload();
                } catch (error) {
                    console.error('ERROR: Fallo al eliminar tarea:', error);
                }
            }
        });
    });
});
