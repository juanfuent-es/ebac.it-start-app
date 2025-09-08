// Capa de integración con API JSON para CRUD de Tareas

async function apiFetch(url, options = {}) {
  const headers = options.headers || {};
  if (options.body && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }
  const response = await fetch(url, { ...options, headers });
  if (response.status === 204) {
    return null;
  }
  let data = null;
  try {
    data = await response.json();
  } catch (e) {
    // Ignorar si no hay JSON
  }
  if (!response.ok) {
    const message = (data && (data.error || data.message)) || `Error HTTP ${response.status}`;
    const err = new Error(message);
    err.status = response.status;
    err.data = data;
    throw err;
  }
  return data;
}

function showFlash(message, category = 'info') {
  const container = document.querySelector('main.container');
  if (!container) return;
  const div = document.createElement('div');
  div.className = `alert alert-${category} mt-2`;
  div.setAttribute('role', 'alert');
  div.textContent = message;
  container.prepend(div);
  setTimeout(() => div.remove(), 3500);
}
