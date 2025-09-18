# Importamos las librerías necesarias para la visualización de datos
import requests  # Para hacer peticiones HTTP a APIs
import pandas as pd  # Para manipular y analizar datos estructurados
import matplotlib.pyplot as plt  # Para crear gráficos y visualizaciones

# PASO 1: CARGAR DATOS DESDE LA API
# Hacemos una petición GET a la API de nuestra aplicación Flask
resp = requests.get("http://localhost:5000/api/tareas")

# Usamos try-except para manejar posibles errores de conexión
try:
    # Convertimos la respuesta JSON en un diccionario de Python
    datos = resp.json()
    
    # Creamos un DataFrame de pandas con los datos obtenidos
    # Un DataFrame es como una tabla de Excel pero programáticamente
    df = pd.DataFrame(datos)
    
    # Mostramos información básica sobre los datos cargados
    print("Datos cargados correctamente")
    print(f"Total de tareas: {len(df)}")  # Número total de filas
    print(f"Columnas disponibles: {list(df.columns)}")  # Nombres de las columnas
except Exception as e:
    # Si hay algún error, mostramos el mensaje y una sugerencia
    print(f"Error al cargar datos: {e}")
    print("Sugerencia: Asegúrate de que la aplicación Flask esté ejecutándose en localhost:5000")
    # Creamos un DataFrame vacío para evitar errores posteriores
    df = pd.DataFrame()

def limpiar_datos():
    """
    PASO 2: LIMPIEZA DE DATOS PARA VISUALIZACIÓN
    Preparamos los datos para que las visualizaciones funcionen correctamente
    """
    print("Iniciando limpieza de datos...")

    # CONVERSIÓN DE FECHAS A DATETIME
    # Convertimos las columnas de fecha de string a datetime
    # errors='coerce' convierte valores inválidos a NaT (Not a Time)
    columnas_fecha = ['fecha_creacion','fecha_limite','completado_en', 'fecha_actualizacion', 'fecha_limite']
    for col in columnas_fecha:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    print(f"Formato de fecha corregido para: {columnas_fecha}")
    
    # NORMALIZACIÓN DE TEXTO
    # Convertimos el estado a minúsculas y eliminamos espacios extra
    # Esto evita problemas en las visualizaciones con categorías duplicadas
    df['estado'] = df['estado'].str.lower().str.strip()
    print("Texto normalizado a minúsculas en columna 'estado'")
# VISUALIZACIÓN 1: GRÁFICO DE BARRAS - COMPARAR CATEGORÍAS (PRIORIDAD)
def grafico_barras_prioridad():
    """
    VISUALIZACIÓN 1: GRÁFICO DE BARRAS POR PRIORIDAD
    Muestra la cantidad de tareas por cada nivel de prioridad
    Responde: ¿Qué categoría de prioridad domina?
    """
    # Contamos las tareas por prioridad y las ordenamos por índice
    df["prioridad"].value_counts().sort_index().plot(kind="bar")
    
    # Configuramos el título y etiquetas del gráfico
    plt.title("Tareas por prioridad")
    plt.xlabel("Prioridad")
    plt.ylabel("No de Tareas")
    
    # Configuramos la rotación de las etiquetas del eje X
    plt.xticks(rotation=0)
    
    # Agregamos una cuadrícula para facilitar la lectura
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    
    # Ajustamos el layout para evitar que se corten las etiquetas
    plt.tight_layout()
    plt.show()
# VISUALIZACIÓN 2: GRÁFICO DE LÍNEAS - EVOLUCIÓN TEMPORAL
def grafico_lineas_creadas_por_dia():
    """
    VISUALIZACIÓN 2: GRÁFICO DE LÍNEAS - EVOLUCIÓN DIARIA
    Muestra cómo cambia la cantidad de tareas creadas a lo largo del tiempo
    Responde: ¿Cómo cambia la productividad en el tiempo?
    """
    # Agrupamos las tareas por fecha de creación y contamos cuántas hay cada día
    conteo_diario = df.groupby(df["fecha_creacion"].dt.date).size()
    
    # Creamos un gráfico de líneas para mostrar la evolución temporal
    conteo_diario.plot(kind="line")
    
    # Configuramos el título y etiquetas del gráfico
    plt.title("Tareas creadas por día")
    plt.xlabel("Fecha")
    plt.ylabel("Tareas creadas")
    
    # Agregamos una cuadrícula para facilitar la lectura
    plt.grid(True, linestyle="--", alpha=0.9)
    
    # Ajustamos el layout para evitar que se corten las etiquetas
    plt.tight_layout()
    plt.show()
# VISUALIZACIÓN 3: GRÁFICO DE PASTEL - PROPORCIONES POR ESTADO
def grafico_pastel_estado():
    """
    VISUALIZACIÓN 3: GRÁFICO DE PASTEL POR ESTADO
    Muestra la distribución proporcional de tareas por estado
    Responde: ¿Qué proporción ocupa cada estado?
    """
    # Contamos las tareas por estado y creamos un gráfico de pastel
    # autopct muestra los porcentajes en cada segmento
    df["estado"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    
    # Configuramos el título del gráfico
    plt.title("Distribución por estado")
    
    # Eliminamos la etiqueta del eje Y (no es necesaria en gráficos de pastel)
    plt.ylabel("")
    
    # Ajustamos el layout para evitar que se corten las etiquetas
    plt.tight_layout()
    plt.show()
# VISUALIZACIÓN 4: GRÁFICO DE DISPERSIÓN - RELACIÓN ENTRE VARIABLES
def grafico_dispersion_tiempo_vs_prioridad():
    """
    VISUALIZACIÓN 4: GRÁFICO DE DISPERSIÓN - TIEMPO vs PRIORIDAD
    Muestra la relación entre el tiempo estimado y la prioridad de las tareas
    Responde: ¿Existe correlación entre duración y prioridad?
    """
    # Creamos un gráfico de dispersión con tiempo_estimado en X y prioridad en Y
    # alpha=0.6 hace los puntos semi-transparentes para ver superposiciones
    plt.scatter(df["tiempo_estimado"], df["prioridad"], alpha=0.6)
    
    # Configuramos el título y etiquetas del gráfico
    plt.title("Duración estimada vs Prioridad")
    plt.xlabel("Minutos estimados")
    plt.ylabel("Prioridad")
    
    # Agregamos una cuadrícula sutil para facilitar la lectura
    plt.grid(True, linestyle="--", alpha=0.3)
    
    # Ajustamos el layout para evitar que se corten las etiquetas
    plt.tight_layout()
    plt.show()
# VISUALIZACIÓN 5: GRÁFICO DE LÍNEAS MÚLTIPLES - EVOLUCIÓN SEMANAL POR PRIORIDAD
def grafico_lineas_semana_por_prioridad():
    """
    VISUALIZACIÓN 5: EVOLUCIÓN SEMANAL POR PRIORIDAD
    Muestra cómo evoluciona la creación de tareas por semana, separadas por prioridad
    Responde: ¿Cómo cambia la distribución de prioridades en el tiempo?
    """
    # Creamos una columna con la fecha de inicio de cada semana (lunes)
    # to_period('W-MON') agrupa por semana empezando en lunes
    df["semana_fecha"] = df["fecha_creacion"].dt.to_period('W-MON').apply(lambda p: p.start_time)
    
    # Agrupamos por semana y prioridad, contamos las tareas
    # unstack() convierte las prioridades en columnas separadas
    conteo = df.groupby(["semana_fecha", "prioridad"]).size().unstack(fill_value=0)
    
    # Ordenamos por fecha para que el gráfico sea cronológico
    conteo = conteo.sort_index()
    
    # Creamos un gráfico de líneas con marcadores
    conteo.plot(kind="line", marker="o")
    
    # Configuramos el título y etiquetas del gráfico
    plt.title("Tareas creadas por semana y prioridad")
    plt.xlabel("Semana (fecha de inicio)")
    plt.ylabel("Cantidad de tareas")
    
    # Agregamos cuadrícula y leyenda
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend(title="Prioridad")
    
    # Rotamos las etiquetas del eje X para mejor legibilidad
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# VISUALIZACIÓN 6: ANÁLISIS DE TAREAS MÁS REPETIDAS
def graficar_top_tareas_mas_repetidas():
    """
    VISUALIZACIÓN 6: TOP 10 TAREAS MÁS REPETIDAS
    Muestra las 10 tareas que aparecen con mayor frecuencia
    Responde: ¿Cuáles son las tareas más comunes?
    """
    # Contamos cuántas veces aparece cada nombre de tarea
    # Ordenamos de mayor a menor y tomamos las primeras 10
    tareas_repetidas = df['nombre'].value_counts().sort_values(ascending=False).head(10)
    
    # Creamos un gráfico de barras horizontal
    tareas_repetidas.plot(kind='bar')
    
    # Configuramos el título y etiquetas del gráfico
    plt.title('Top 10 Tareas Más Repetidas')
    plt.xlabel('Nombre de la Tarea')
    plt.ylabel('Frecuencia')
    
    # Rotamos las etiquetas del eje X para mejor legibilidad
    plt.tick_params(axis='x', rotation=45)
    
    # Agregamos cuadrícula vertical para facilitar la lectura
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

def graficar_estado_de_top_tareas():
    """
    VISUALIZACIÓN 7: ESTADO DE LAS TAREAS MÁS REPETIDAS
    Muestra el estado de las tareas más frecuentes en barras apiladas
    Responde: ¿En qué estado están las tareas más comunes?
    """
    # Obtenemos las 20 tareas más repetidas
    tareas_top = df['nombre'].value_counts().head(20).index
    
    # Filtramos el DataFrame para incluir solo estas tareas
    df_top_tareas = df[df['nombre'].isin(tareas_top)]
    
    # Agrupamos por nombre de tarea y estado, contamos las ocurrencias
    # unstack() convierte los estados en columnas separadas
    estado_por_tarea = df_top_tareas.groupby(['nombre', 'estado']).size().unstack(fill_value=0)
    
    # Definimos colores personalizados para cada estado
    colores = ['#ff9999', '#66b3ff', '#99ff99']
    
    # Creamos un gráfico de barras apiladas
    estado_por_tarea.plot(kind='bar', stacked=True, color=colores)
    
    # Configuramos el título y etiquetas del gráfico
    plt.title('Estado de las 5 Tareas Más Repetidas')
    plt.xlabel('Nombre de la Tarea')
    plt.ylabel('Cantidad')
    
    # Rotamos las etiquetas del eje X para mejor legibilidad
    plt.tick_params(axis='x', rotation=45)
    
    # Agregamos leyenda y cuadrícula
    plt.legend(title='Estado')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

def graficar_evolucion_mensual_top3():
    """
    VISUALIZACIÓN 8: EVOLUCIÓN MENSUAL DE LAS 3 TAREAS MÁS REPETIDAS
    Muestra cómo evolucionan las 3 tareas más frecuentes a lo largo de los meses
    Responde: ¿Cómo cambia la frecuencia de las tareas más comunes en el tiempo?
    """
    # Creamos una columna con el mes de creación
    df['mes'] = df['fecha_creacion'].dt.to_period('M')
    
    # Obtenemos las 3 tareas más repetidas
    top_3_tareas = df['nombre'].value_counts().head(3).index
    
    # Filtramos el DataFrame para incluir solo estas 3 tareas
    df_top3 = df[df['nombre'].isin(top_3_tareas)]
    
    # Agrupamos por mes y nombre de tarea, contamos las ocurrencias
    # unstack() convierte los nombres de tarea en columnas separadas
    evolucion_temporal = df_top3.groupby(['mes', 'nombre']).size().unstack(fill_value=0)
    
    # Creamos un gráfico de líneas con marcadores
    evolucion_temporal.plot(kind='line', marker='o', linewidth=2)
    
    # Configuramos el título y etiquetas del gráfico
    plt.title('Evolución Mensual de las 3 Tareas Más Repetidas')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad de Tareas')
    
    # Rotamos las etiquetas del eje X para mejor legibilidad
    plt.tick_params(axis='x', rotation=45)
    
    # Agregamos leyenda y cuadrícula
    plt.legend(title='Tarea')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

def graficar_heatmap_categoria_vs_estado():
    """
    VISUALIZACIÓN 9: HEATMAP - CATEGORÍA vs ESTADO
    Muestra la relación entre categorías y estados en un mapa de calor
    Responde: ¿Cómo se distribuyen las tareas por categoría y estado?
    """
    # Obtenemos las 30 tareas más repetidas
    tareas_top = df['nombre'].value_counts().head(30).index
    
    # Filtramos el DataFrame para incluir solo estas tareas
    df_top_tareas = df[df['nombre'].isin(tareas_top)].copy()
    
    # Rellenamos valores nulos en categoría con 'Sin categoría'
    df_top_tareas['categoria'] = df_top_tareas['categoria'].fillna('Sin categoría')
    
    # Agrupamos por categoría y estado, contamos las ocurrencias
    # unstack() convierte los estados en columnas separadas
    heatmap_data = df_top_tareas.groupby(['categoria', 'estado']).size().unstack(fill_value=0)
    
    # Creamos la figura y el eje para el heatmap
    fig, ax = plt.subplots()
    
    # Creamos el heatmap con colores que van de amarillo a rojo
    im = ax.imshow(heatmap_data.values, cmap='YlOrRd', aspect='auto')

    # Configuramos el título y etiquetas
    ax.set_title('Heatmap: Categoría vs Estado\n(Tareas Repetidas)')
    ax.set_xlabel('Estado')
    ax.set_ylabel('Categoría')
    
    # Configuramos las etiquetas de los ejes
    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_xticklabels(heatmap_data.columns, rotation=45, ha='right')
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index)
    
    # Agregamos los valores numéricos en cada celda del heatmap
    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            ax.text(j, i, heatmap_data.iloc[i, j], ha="center", va="center", 
                   color="black", fontweight='bold')
    
    # Agregamos la barra de colores (colorbar) para interpretar los valores
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout()
    plt.show()
    
# EJECUCIÓN DEL FLUJO COMPLETO DE VISUALIZACIÓN
# Ejecutamos la limpieza de datos y las visualizaciones

# Paso 1: Limpieza de datos para visualización
limpiar_datos()

# VISUALIZACIONES BÁSICAS (descomenta las que quieras ejecutar)
# Estas son las visualizaciones fundamentales para entender los datos

# grafico_barras_prioridad()  # Gráfico de barras por prioridad
# grafico_lineas_creadas_por_dia()  # Evolución temporal diaria
# grafico_pastel_estado()  # Distribución proporcional por estado
# grafico_dispersion_tiempo_vs_prioridad()  # Relación entre tiempo y prioridad

# VISUALIZACIONES AVANZADAS
# Estas visualizaciones requieren análisis más complejos

# grafico_lineas_semana_por_prioridad()  # Evolución semanal por prioridad

# ANÁLISIS DE TAREAS REPETIDAS
# Estas visualizaciones se enfocan en identificar patrones en tareas frecuentes

# graficar_top_tareas_mas_repetidas()  # Top 10 tareas más repetidas
# graficar_estado_de_top_tareas()  # Estado de las tareas más frecuentes
# graficar_evolucion_mensual_top3()  # Evolución mensual de las 3 tareas más repetidas

# VISUALIZACIÓN COMPLEJA
# Esta visualización combina múltiples dimensiones de los datos
graficar_heatmap_categoria_vs_estado()  # Heatmap categoría vs estado