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
# 4) Dispersión – relación entre tiempo estimado y prioridad
def grafico_dispersion_tiempo_vs_prioridad():
    """Relación entre duración estimada y prioridad (responde: ¿existe correlación?)."""
    plt.scatter(df["tiempo_estimado"], df["prioridad"], alpha=0.6)
    plt.title("Duración estimada vs Prioridad")
    plt.xlabel("Minutos estimados")
    plt.ylabel("Prioridad")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()
# 5) Evolución semanal de creación de tareas por prioridad
def grafico_lineas_semana_por_prioridad():
    """Tareas creadas por semana separadas por prioridad (unstack)."""
    # Usar la fecha de inicio de la semana (lunes) como eje X
    df["semana_fecha"] = df["fecha_creacion"].dt.to_period('W-MON').apply(lambda p: p.start_time)
    conteo = df.groupby(["semana_fecha", "prioridad"]).size().unstack(fill_value=0)
    conteo = conteo.sort_index()
    conteo.plot(kind="line", marker="o")
    plt.title("Tareas creadas por semana y prioridad")
    plt.xlabel("Semana (fecha de inicio)")
    plt.ylabel("Cantidad de tareas")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend(title="Prioridad")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 6) Análisis de tareas más repetidas cruzadas con estado y fechas
def graficar_top_tareas_mas_repetidas():
    """Gráfico de barras con el top 10 de tareas más repetidas."""
    tareas_repetidas = df['nombre'].value_counts().sort_values(ascending=False).head(10)
    tareas_repetidas.plot(kind='bar')
    plt.title('Top 10 Tareas Más Repetidas')
    plt.xlabel('Nombre de la Tarea')
    plt.ylabel('Frecuencia')
    plt.tick_params(axis='x', rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

def graficar_estado_de_top_tareas():
    """Barras apiladas de estado para las 5 tareas más repetidas."""
    tareas_top = df['nombre'].value_counts().head(20).index
    df_top_tareas = df[df['nombre'].isin(tareas_top)]
    estado_por_tarea = df_top_tareas.groupby(['nombre', 'estado']).size().unstack(fill_value=0)
    colores = ['#ff9999', '#66b3ff', '#99ff99']
    estado_por_tarea.plot(kind='bar', stacked=True, color=colores)
    plt.title('Estado de las 5 Tareas Más Repetidas')
    plt.xlabel('Nombre de la Tarea')
    plt.ylabel('Cantidad')
    plt.tick_params(axis='x', rotation=45)
    plt.legend(title='Estado')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

def graficar_evolucion_mensual_top3():
    """Líneas: evolución mensual de las 3 tareas más repetidas."""
    df['mes'] = df['fecha_creacion'].dt.to_period('M')
    top_3_tareas = df['nombre'].value_counts().head(3).index
    df_top3 = df[df['nombre'].isin(top_3_tareas)]
    evolucion_temporal = df_top3.groupby(['mes', 'nombre']).size().unstack(fill_value=0)
    evolucion_temporal.plot(kind='line', marker='o', linewidth=2)
    plt.title('Evolución Mensual de las 3 Tareas Más Repetidas')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad de Tareas')
    plt.tick_params(axis='x', rotation=45)
    plt.legend(title='Tarea')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

def graficar_heatmap_categoria_vs_estado():
    """Heatmap: categoría vs estado para las tareas más repetidas."""
    tareas_top = df['nombre'].value_counts().head(30).index
    df_top_tareas = df[df['nombre'].isin(tareas_top)].copy()
    df_top_tareas['categoria'] = df_top_tareas['categoria'].fillna('Sin categoría')
    heatmap_data = df_top_tareas.groupby(['categoria', 'estado']).size().unstack(fill_value=0)
    fig, ax = plt.subplots()
    im = ax.imshow(heatmap_data.values, cmap='YlOrRd', aspect='auto')

    ax.set_title('Heatmap: Categoría vs Estado\n(Tareas Repetidas)')
    ax.set_xlabel('Estado')
    ax.set_ylabel('Categoría')
    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_xticklabels(heatmap_data.columns, rotation=45, ha='right')
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index)
    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            ax.text(j, i, heatmap_data.iloc[i, j], ha="center", va="center", color="black", fontweight='bold')
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout()
    plt.show()
    
limpiar_datos()
# Visualizaciones base
#grafico_barras_prioridad()
# grafico_lineas_creadas_por_dia()
# grafico_pastel_estado()
# grafico_dispersion_tiempo_vs_prioridad()
# # Evolución semanal
# grafico_lineas_semana_por_prioridad()
# Ejecutar análisis de tareas repetidas (cada gráfica puede llamarse de forma independiente)
# graficar_top_tareas_mas_repetidas()
# graficar_estado_de_top_tareas()
# graficar_evolucion_mensual_top3()
graficar_heatmap_categoria_vs_estado()