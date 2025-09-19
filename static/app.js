/**
 * =============================================================================
 * APP.JS - ARCHIVO PRINCIPAL DE JAVASCRIPT
 * =============================================================================
 * Este archivo mantiene las funciones básicas de la aplicación.
 * Las funciones más complejas están en archivos separados:
 * - funciones-generales.js: Funciones utilitarias generales
 * - calendario.js: Funciones específicas del calendario
 * =============================================================================
 */

// Las funciones apiFetch y showFlash ahora están en funciones-generales.js
// Este archivo se mantiene para compatibilidad hacia atrás

// La función apiFetch ahora está completamente implementada en funciones-generales.js
// Este archivo se mantiene para compatibilidad hacia atrás

// Función de compatibilidad - redirige a la nueva implementación
function showFlash(message, category = 'info') {
    // Si la nueva función está disponible, usarla
    if (typeof window.showFlash === 'function') {
        return window.showFlash(message, category);
    }
    
    // Implementación básica de respaldo
    const container = document.querySelector('main.container');
    if (!container) return;
    const div = document.createElement('div');
    div.className = `alert alert-${category} mt-2`;
    div.setAttribute('role', 'alert');
    div.textContent = message;
    container.prepend(div);
    setTimeout(() => div.remove(), 3500);
}
