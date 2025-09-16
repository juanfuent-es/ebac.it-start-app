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
    
    columnas_fecha = ['fecha_creacion', 'fecha_limite', 'completado_en']
    for col in columnas_fecha:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            print(f"Formato de fecha corregido para: {col}")
    
    if 'estado' in df.columns:
        df['estado'] = df['estado'].str.lower()
        print("Texto normalizado a minúsculas en columna 'estado'")
    
    if 'prioridad' in df.columns:
        mapeo_prioridad = {
            'Alta': 'alta',
            'Media': 'media', 
            'Baja': 'baja',
            'HIGH': 'alta',
            'MEDIUM': 'media',
            'LOW': 'baja'
        }
        df['prioridad'] = df['prioridad'].replace(mapeo_prioridad)
        df['prioridad'] = df['prioridad'].str.lower().str.strip()
        print("Valores de prioridad unificados")
    
    print(f"Limpieza completada: {filas_iniciales - filas_despues_nulos} filas eliminadas")
    return df

def detectar_outliers():
    print("Detectando outliers y valores inconsistentes...")
    outliers = {}
    
    if 'tiempo_estimado' in df.columns:
        tiempos_negativos = df[df['tiempo_estimado'] < 0]
        outliers['tiempos_negativos'] = {
            'cantidad': len(tiempos_negativos),
            'registros': tiempos_negativos
        }
        print(f"Tiempos estimados negativos: {len(tiempos_negativos)} casos")
    
    if 'fecha_creacion' in df.columns and 'completado_en' in df.columns:
        fechas_incorrectas = df[df['completado_en'] < df['fecha_creacion']]
        outliers['fechas_incorrectas'] = {
            'cantidad': len(fechas_incorrectas),
            'registros': fechas_incorrectas
        }
        print(f"Fechas incorrectas: {len(fechas_incorrectas)} casos")
    
    if 'prioridad' in df.columns:
        prioridades_unicas = df['prioridad'].value_counts()
        outliers['prioridades_inconsistentes'] = {
            'valores_unicos': prioridades_unicas,
            'cantidad_unicos': len(prioridades_unicas)
        }
        print(f"Valores únicos en prioridad: {len(prioridades_unicas)}")
        print("Valores encontrados:", prioridades_unicas.index.tolist())
    
    return outliers

def crear_columnas_derivadas():
    print("Creando columnas derivadas...")
    
    if 'completado_en' in df.columns and 'fecha_limite' in df.columns:
        df['atrasada'] = df['completado_en'] > df['fecha_limite']
        print("Columna 'atrasada' creada")
    
    if 'fecha_creacion' in df.columns:
        df['mes'] = df['fecha_creacion'].dt.month
        print("Columna 'mes' creada")
    
    if 'completado_en' in df.columns and 'fecha_creacion' in df.columns:
        df['dias_entre_creacion_y_entrega'] = (df['completado_en'] - df['fecha_creacion']).dt.days
        print("Columna 'dias_entre_creacion_y_entrega' creada")
    
    if 'completado_en' in df.columns and 'fecha_creacion' in df.columns:
        df['duracion_real'] = (df['completado_en'] - df['fecha_creacion']).dt.days
        print("Columna 'duracion_real' creada")
    
    if 'completado_en' in df.columns and 'fecha_limite' in df.columns:
        df['cumplimiento'] = df['completado_en'] <= df['fecha_limite']
        print("Columna 'cumplimiento' creada")
    
    if 'tiempo_estimado' in df.columns:
        df['tiempo_estimado_horas'] = df['tiempo_estimado'] / 60
        print("Columna 'tiempo_estimado_horas' creada")
    
    return df

def analizar_rendimiento():
    print("Analizando rendimiento del equipo...")
    
    if 'a_tiempo' not in df.columns:
        df['a_tiempo'] = df['completado_en'] <= df['fecha_limite']
    
    if 'dias_retraso' not in df.columns:
        df['dias_retraso'] = (df['completado_en'] - df['fecha_limite']).dt.days
    
    porcentaje_cumplimiento = df['a_tiempo'].mean() * 100
    print(f"Porcentaje de cumplimiento: {porcentaje_cumplimiento:.2f}%")
    
    retrasadas = df[df['dias_retraso'] > 0]
    print(f"Tareas entregadas fuera de plazo: {len(retrasadas)}")
    
    if len(retrasadas) > 0:
        promedio_retraso = retrasadas['dias_retraso'].mean()
        print(f"Promedio de días de retraso: {promedio_retraso:.2f}")
    
    return {
        'porcentaje_cumplimiento': porcentaje_cumplimiento,
        'tareas_retrasadas': len(retrasadas),
        'promedio_retraso': retrasadas['dias_retraso'].mean() if len(retrasadas) > 0 else 0
    }

def agrupar_por_prioridad():
    print("Agrupando por prioridad...")
    
    if 'tiempo_estimado' in df.columns and 'prioridad' in df.columns:
        tiempo_promedio = df.groupby('prioridad')['tiempo_estimado'].mean()
        print("Tiempo promedio estimado por prioridad:")
        print(tiempo_promedio)
    
    if 'prioridad' in df.columns and 'completado_en' in df.columns:
        completadas = df[df['completado_en'].notnull()]
        completadas_por_prioridad = completadas.groupby('prioridad').size()
        print("Tareas completadas por prioridad:")
        print(completadas_por_prioridad)
    
    return {
        'tiempo_promedio': tiempo_promedio if 'tiempo_estimado' in df.columns else None,
        'completadas_por_prioridad': completadas_por_prioridad if 'prioridad' in df.columns else None
    }

def analizar_por_mes():
    print("Analizando por mes de creación...")
    
    if 'fecha_creacion' in df.columns:
        if 'mes' not in df.columns:
            df['mes'] = df['fecha_creacion'].dt.month
        
        tareas_por_mes = df.groupby('mes').size()
        print("Tareas creadas por mes:")
        print(tareas_por_mes)
        
        return tareas_por_mes
    
    return None

def analizar_por_semana():
    print("Analizando por semana...")
    
    if 'completado_en' in df.columns:
        df['semana'] = df['completado_en'].dt.isocalendar().week
        tareas_por_semana = df.groupby('semana').size()
        print("Tareas completadas por semana:")
        print(tareas_por_semana)
        
        return tareas_por_semana
    
    return None

def estadisticas_descriptivas():
    print("Calculando estadísticas descriptivas...")
    
    estadisticas = {}
    
    if 'tiempo_estimado' in df.columns:
        promedio_duracion = df['tiempo_estimado'].mean()
        estadisticas['promedio_duracion'] = round(promedio_duracion, 2)
        print(f"Promedio de duración estimada: {promedio_duracion:.2f} minutos")
    
    if 'fecha_creacion' in df.columns:
        tareas_por_dia = df.groupby(df['fecha_creacion'].dt.date).size()
        estadisticas['tareas_por_dia'] = tareas_por_dia
        print("Tareas creadas por día (últimos 5 días):")
        print(tareas_por_dia.tail())
    
    if 'cumplimiento' in df.columns:
        porcentaje_cumplimiento = df['cumplimiento'].mean() * 100
        estadisticas['porcentaje_cumplimiento'] = round(porcentaje_cumplimiento, 2)
        print(f"Porcentaje de cumplimiento: {porcentaje_cumplimiento:.2f}%")
    
    return estadisticas

def mostrar_resumen():
    print("\n" + "="*50)
    print("RESUMEN DEL DATASET PROCESADO")
    print("="*50)
    print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
    print(f"Columnas: {list(df.columns)}")
    
    if 'prioridad' in df.columns:
        print(f"\nDistribución por prioridad:")
        print(df['prioridad'].value_counts())
    
    if 'estado' in df.columns:
        print(f"\nDistribución por estado:")
        print(df['estado'].value_counts())
    
    print("="*50)

def procesar_dataset_completo():
    print("Iniciando procesamiento completo del dataset...")
    
    limpiar_datos_basicos()
    outliers = detectar_outliers()
    crear_columnas_derivadas()
    rendimiento = analizar_rendimiento()
    agrupacion_prioridad = agrupar_por_prioridad()
    analisis_mes = analizar_por_mes()
    estadisticas = estadisticas_descriptivas()
    mostrar_resumen()
    
    print("\nProcesamiento completo finalizado!")
    
    return df

if __name__ == "__main__":
    print("Procesamiento de datos con pandas")
    print("-" * 40)
    
    procesar_dataset_completo()
