import requests
import pandas as pd
import matplotlib.pyplot as plt

resp = requests.get("http://localhost:5000/api/tareas")
try:
    datos = resp.json()
    df = pd.DataFrame(datos)
    print("Datos cargados correctamente")
    print(f"Total de tareas: {len(df)}")
    print(f"Columnas disponibles: {list(df.columns)}")
except Exception as e:
    print(f"Error al cargar datos: {e}")
    print("Sugerencia: Asegúrate de que la aplicación Flask esté ejecutándose en localhost:5000")
    df = pd.DataFrame()


# Utilidades
def _get_col(df, posibles_nombres):
    """Devuelve el primer nombre de columna existente en df dentro de posibles_nombres."""
    for nombre in posibles_nombres:
        if nombre in df.columns:
            return nombre
    return None


def preparar_df_para_visualizacion():
    """Estandariza columnas clave y prepara tipos para graficar."""
    if df.empty:
        return
    # Mapear columnas posibles (es/en)
    col_fecha_creacion = _get_col(df, ["created_at", "fecha_creacion"]) 
    col_prioridad = _get_col(df, ["priority", "prioridad"]) 
    col_estado = _get_col(df, ["status", "estado"]) 
    col_tiempo = _get_col(df, ["estimated_time", "tiempo_estimado"]) 

    # Conversión de tipos
    if col_fecha_creacion:
        df[col_fecha_creacion] = pd.to_datetime(df[col_fecha_creacion], errors="coerce")
    if col_tiempo:
        df[col_tiempo] = pd.to_numeric(df[col_tiempo], errors="coerce")

    # Crear alias uniformes si no existen
    if "created_at" not in df.columns and col_fecha_creacion:
        df["created_at"] = df[col_fecha_creacion]
    if "priority" not in df.columns and col_prioridad:
        df["priority"] = df[col_prioridad]
    if "status" not in df.columns and col_estado:
        df["status"] = df[col_estado]
    if "estimated_time" not in df.columns and col_tiempo:
        df["estimated_time"] = df[col_tiempo]


# 1) Gráfico de barras – comparar categorías (prioridad)
def grafico_barras_prioridad():
    """Muestra cantidad de tareas por prioridad (responde: ¿qué categoría domina?)."""
    if df.empty or "priority" not in df.columns:
        print("No hay datos o falta la columna 'priority'/'prioridad'.")
        return
    df["priority"].value_counts().sort_index().plot(kind="bar")
    plt.title("Tareas por prioridad")
    plt.xlabel("Prioridad")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()


# 2) Gráfico de líneas – evolución en el tiempo (tareas creadas por día)
def grafico_lineas_creadas_por_dia():
    """Evolución diaria de creación (responde: ¿cómo cambia en el tiempo?)."""
    if df.empty or "created_at" not in df.columns:
        print("No hay datos o falta la columna de fecha 'created_at'/'fecha_creacion'.")
        return
    conteo_diario = df.groupby(df["created_at"].dt.date).size()
    conteo_diario.plot(kind="line", marker="o")
    plt.title("Tareas creadas por día")
    plt.xlabel("Fecha")
    plt.ylabel("Tareas creadas")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()


# 3) Gráfico de pastel – proporciones por estado
def grafico_pastel_estado():
    """Distribución de estados (responde: ¿qué proporción ocupa cada estado?)."""
    if df.empty or "status" not in df.columns:
        print("No hay datos o falta la columna 'status'/'estado'.")
        return
    df["status"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Distribución por estado")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()


# 4) Dispersión – relación entre tiempo estimado y prioridad
def grafico_dispersion_tiempo_vs_prioridad():
    """Relación entre duración estimada y prioridad (responde: ¿existe correlación?)."""
    if df.empty or "estimated_time" not in df.columns or "priority" not in df.columns:
        print("Faltan columnas 'estimated_time'/'tiempo_estimado' o 'priority'/'prioridad'.")
        return
    # Si prioridad es categórica, convertirla a códigos para el eje Y
    prioridad_cods = df["priority"].astype("category").cat.codes
    plt.scatter(df["estimated_time"], prioridad_cods, alpha=0.6)
    plt.title("Duración estimada vs Prioridad")
    plt.xlabel("Minutos estimados")
    plt.ylabel("Prioridad (codificada)")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()


# 5) Evolución semanal con unstack por prioridad
def grafico_lineas_semana_por_prioridad():
    """Tareas creadas por semana separadas por prioridad (unstack)."""
    if df.empty or "created_at" not in df.columns or "priority" not in df.columns:
        print("Faltan columnas para agrupar por semana o prioridad.")
        return
    df_tmp = df.copy()
    df_tmp["semana"] = df_tmp["created_at"].dt.isocalendar().week
    conteo = df_tmp.groupby(["semana", "priority"]).size().unstack(fill_value=0)
    conteo.plot(kind="line", marker="o")
    plt.title("Tareas creadas por semana y prioridad")
    plt.xlabel("Semana del año")
    plt.ylabel("Cantidad de tareas")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend(title="Prioridad")
    plt.tight_layout()
    plt.show()


# 6) Personalización/legibilidad en barras (demostración)
def demo_personalizacion_barras():
    """Demuestra cómo pequeñas personalizaciones mejoran la legibilidad."""
    if df.empty or "priority" not in df.columns:
        print("No hay datos o falta la columna 'priority'/'prioridad'.")
        return
    df["priority"].value_counts().sort_values().plot(kind="bar")
    plt.title("Cantidad de tareas por prioridad")
    plt.xlabel("Prioridad")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


# 7) Agregar contexto mínimo (título, ejes, leyenda opcional)
def agregar_contexto_minimo():
    """Ilustra el impacto de título/etiquetas/leyenda en claridad."""
    if df.empty or "priority" not in df.columns:
        print("No hay datos o falta la columna 'priority'/'prioridad'.")
        return
    df["priority"].value_counts().plot(kind="bar")
    plt.title("Distribución de tareas por prioridad")
    plt.xlabel("Prioridad")
    plt.ylabel("Cantidad")
    plt.legend(["Cantidad de tareas"])  # solo si es necesario
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()


# 8) Errores comunes y buenas prácticas (con ejemplos simples)
def ejemplos_errores_comunes():
    """Muestra prácticas que afectan la percepción y cómo corregirlas."""
    if df.empty or "priority" not in df.columns:
        print("No hay datos o falta la columna 'priority'/'prioridad' para ejemplos.")
        return
    # Categorías desordenadas vs ordenadas
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    df["priority"].value_counts().plot(kind="bar")
    plt.title("Desordenado")
    plt.xticks(rotation=90)
    plt.subplot(1, 2, 2)
    df["priority"].value_counts().sort_values().plot(kind="bar")
    plt.title("Ordenado por valor")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    print("Sugerencias:")
    print("- Usa paletas con buen contraste para mejorar legibilidad.")
    print("- Evita gráficos de pastel con demasiadas categorías; prefiere barras o agrupa 'Otros'.")
    print("- Para barras, comienza eje Y en cero salvo justificación clara, para no exagerar diferencias.")


# 9) Narrativa visual: pregunta -> filtro -> agrupación -> contexto -> énfasis
def narrativa_visual_pendientes_resaltado():
    """Historia visual: ¿qué prioridad concentra más tareas pendientes?"""
    if df.empty or "status" not in df.columns or "priority" not in df.columns:
        print("Faltan columnas 'status'/'estado' o 'priority'/'prioridad'.")
        return
    pendientes = df[df["status"] == "pendiente"].copy()
    if pendientes.empty:
        print("No hay tareas pendientes para mostrar.")
        return
    conteo = pendientes["priority"].value_counts()
    # Resaltar la barra máxima
    colores = ["gray"] * len(conteo)
    idx_max = conteo.values.argmax()
    colores[idx_max] = "red"
    conteo.plot(kind="bar", color=colores)
    plt.title("Tareas pendientes por prioridad")
    plt.xlabel("Prioridad")
    plt.ylabel("Cantidad")
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()


# Preparación y ejecución de demostraciones
preparar_df_para_visualizacion()

if not df.empty:
    # Visualizaciones base
    grafico_barras_prioridad()
    grafico_lineas_creadas_por_dia()
    grafico_pastel_estado()
    grafico_dispersion_tiempo_vs_prioridad()
    # Evolución semanal
    grafico_lineas_semana_por_prioridad()
    # Legibilidad y contexto
    demo_personalizacion_barras()
    agregar_contexto_minimo()
    # Errores comunes
    ejemplos_errores_comunes()
    # Narrativa visual
    narrativa_visual_pendientes_resaltado()
