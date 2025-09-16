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

def limpiar_datos():
    print("Iniciando limpieza de datos...")

    # Solo convertir columnas de fecha a datetime
    columnas_fecha = ['fecha_creacion','fecha_limite','completado_en', 'fecha_actualizacion', 'fecha_limite']
    for col in columnas_fecha:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    print(f"Formato de fecha corregido para: {columnas_fecha}")
    # 
    df['estado'] = df['estado'].str.lower().str.strip()
    print("Texto normalizado a minúsculas en columna 'estado'")

# 1) Gráfico de barras – comparar categorías (prioridad)
def grafico_barras_prioridad():
    """Muestra cantidad de tareas por prioridad (responde: ¿qué categoría domina?)."""
    df["prioridad"].value_counts().sort_index().plot(kind="bar")
    plt.title("Tareas por prioridad")
    plt.xlabel("Prioridad")
    plt.ylabel("No de Tareas")
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()

# 2) Gráfico de líneas – evolución en el tiempo (tareas creadas por día)
def grafico_lineas_creadas_por_dia():
    """Evolución diaria de creación (responde: ¿cómo cambia en el tiempo?)."""
    conteo_diario = df.groupby(df["fecha_creacion"].dt.date).size()
    conteo_diario.plot(kind="line")
    plt.title("Tareas creadas por día")
    plt.xlabel("Fecha")
    plt.ylabel("Tareas creadas")
    plt.grid(True, linestyle="--", alpha=0.9)
    plt.tight_layout()
    plt.show()

# 3) Gráfico de pastel – proporciones por estado
def grafico_pastel_estado():
    """Distribución de estados (responde: ¿qué proporción ocupa cada estado?)."""
    df["estado"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Distribución por estado")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()

limpiar_datos()
grafico_pastel_estado()

# 4) Dispersión – relación entre tiempo estimado y prioridad
def grafico_dispersion_tiempo_vs_prioridad():
    """Relación entre duración estimada y prioridad (responde: ¿existe correlación?)."""
    # Si prioridad es categórica, convertirla a códigos para el eje Y
    prioridad_cods = df["prioridad"] #.astype("category")
    plt.scatter(df["tiempo_estimado"], prioridad_cods, alpha=0.6)
    plt.title("Duración estimada vs Prioridad")
    plt.xlabel("Minutos estimados")
    plt.ylabel("Prioridad (codificada)")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()

grafico_dispersion_tiempo_vs_prioridad()

# 5) Evolución semanal con unstack por prioridad
def grafico_lineas_semana_por_prioridad():
    """Tareas creadas por semana separadas por prioridad (unstack)."""
    df_tmp = df.copy()
    df_tmp["semana"] = df_tmp["fecha_creacion"].dt.isocalendar().week
    conteo = df_tmp.groupby(["semana", "prioridad"]).size().unstack(fill_value=0)
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
    df["prioridad"].value_counts().sort_values().plot(kind="bar")
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
    df["prioridad"].value_counts().plot(kind="bar")
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
    if df.empty:
        print("No hay datos para ejemplos.")
        return
    # Categorías desordenadas vs ordenadas
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    df["prioridad"].value_counts().plot(kind="bar")
    plt.title("Desordenado")
    plt.xticks(rotation=90)
    plt.subplot(1, 2, 2)
    df["prioridad"].value_counts().sort_values().plot(kind="bar")
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
    pendientes = df[df["estado"] == "pendiente"].copy()
    if pendientes.empty:
        print("No hay tareas pendientes para mostrar.")
        return
    conteo = pendientes["prioridad"].value_counts()
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
limpiar_datos()

# Visualizaciones base
#grafico_barras_prioridad()
# grafico_lineas_creadas_por_dia()
# grafico_pastel_estado()
# grafico_dispersion_tiempo_vs_prioridad()
# # Evolución semanal
grafico_lineas_semana_por_prioridad()
# Legibilidad y contexto
demo_personalizacion_barras()
agregar_contexto_minimo()
# Errores comunes
ejemplos_errores_comunes()
# Narrativa visual
narrativa_visual_pendientes_resaltado()
