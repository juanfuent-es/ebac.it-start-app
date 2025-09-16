import requests
import pandas as pd

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

def limpiar_datos_basicos():
    print("Iniciando limpieza básica de datos...")
    
    filas_iniciales = len(df)
    print(f"Estado inicial: {filas_iniciales} filas")
    
    df.dropna(inplace=True)
    filas_despues_nulos = len(df)
    print(f"Después de eliminar nulos: {filas_despues_nulos} filas")

    # Solo convertir columnas de fecha a datetime
    columnas_fecha = ['fecha_creacion','fecha_limite','completado_en', 'fecha_actualizacion', 'fecha_limite']
    for col in columnas_fecha:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    print(f"Formato de fecha corregido para: {columnas_fecha}")
    # 
    df['estado'] = df['estado'].str.lower().str.strip()
    print("Texto normalizado a minúsculas en columna 'estado'")
    print(f"Limpieza completada: {filas_iniciales - filas_despues_nulos} filas eliminadas")

def detectar_outliers():
    print("Detectando outliers y valores inconsistentes...")    
    tiempos_negativos = df[df['tiempo_estimado'] < 0]
    print(f"Tiempos estimados negativos: {len(tiempos_negativos)} casos")

    fechas_incorrectas = df[df['completado_en'] < df['fecha_creacion']]
    print(f"Fechas incorrectas: {len(fechas_incorrectas)} casos")

    prioridades_unicas = df['prioridad'].value_counts()
    print(f"Valores únicos en prioridad: {len(prioridades_unicas)}")
    print("Valores encontrados:", prioridades_unicas.index.tolist())

def crear_columnas_derivadas():
    print("Creando columnas derivadas...")
    
    df['atrasada'] = df['completado_en'] > df['fecha_limite']
    print(f"Columna 'atrasada' creada: {df['atrasada']}")
    df['mes'] = df['fecha_creacion'].dt.month
    print(f"Columna 'mes' creada: {df['mes']}")
    df['semana'] = df['completado_en'].dt.isocalendar().week
    
    df['dias_entre_creacion_y_entrega'] = (df['completado_en'] - df['fecha_creacion']).dt.days
    print(f"Columna 'dias_entre_creacion_y_entrega' creada: {df['dias_entre_creacion_y_entrega']}")
    
    df['duracion_real'] = (df['completado_en'] - df['fecha_creacion']).dt.days
    print(f"Columna 'duracion_real' creada: {df['duracion_real']}")
    
    df['cumplimiento'] = df['completado_en'] <= df['fecha_limite']
    print(f"Columna 'cumplimiento' creada: {df['cumplimiento']}")
    
    df['tiempo_estimado_horas'] = df['tiempo_estimado'] / 60
    print(f"Columna 'tiempo_estimado_horas' creada: {df['tiempo_estimado_horas']}")

def analizar_rendimiento():
    print("Analizando rendimiento del equipo...")

    porcentaje_cumplimiento = df['cumplimiento'].mean() * 100
    print(f"Porcentaje de cumplimiento: {porcentaje_cumplimiento:.2f}%")
    
    df['dias_retraso'] = (df['completado_en'] - df['fecha_limite']).dt.days
    retrasadas = df[df['dias_retraso'] > 0]
    print(f"Tareas entregadas fuera de plazo: {len(retrasadas)}")
    
    if len(retrasadas) > 0:
        promedio_retraso = retrasadas['dias_retraso'].mean()
        print(f"Promedio de días de retraso: {promedio_retraso:.2f}")

def agrupar_por_prioridad():
    print("Agrupando por prioridad...")
    tiempo_promedio = df.groupby('prioridad')['tiempo_estimado'].mean()
    print("Tiempo promedio estimado por prioridad:")
    print(tiempo_promedio)
    
    completadas = df[df['completado_en'].notnull()]
    completadas_por_prioridad = completadas.groupby('prioridad').size()
    print("Tareas completadas por prioridad:")
    print(completadas_por_prioridad)

def analizar_por_mes():
    print("Analizando por mes de creación...")
    tareas_por_mes = df.groupby('mes').size()
    print(f"Tareas creadas por mes: {tareas_por_mes}")

def analizar_por_semana():
    print("Analizando por semana...")
    tareas_por_semana = df.groupby('semana').size()
    print(f"Tareas completadas por semana: {tareas_por_semana}")
    
def estadisticas_descriptivas():
    print("Calculando estadísticas descriptivas...")
    
    promedio_duracion = df['tiempo_estimado'].mean()
    print(f"Promedio de duración estimada: {promedio_duracion:.2f} minutos")
    
    tareas_por_dia = df.groupby(df['fecha_creacion'].dt.date).size()
    print(f"Tareas creadas por día (últimos 10 días): {tareas_por_dia.tail(5)}")
    
    porcentaje_cumplimiento = df['cumplimiento'].mean() * 100
    print(f"Porcentaje de cumplimiento: {porcentaje_cumplimiento:.2f}%")

limpiar_datos_basicos()
detectar_outliers()
crear_columnas_derivadas()
analizar_rendimiento()
agrupar_por_prioridad()
analizar_por_mes()
analizar_por_semana()
estadisticas_descriptivas()