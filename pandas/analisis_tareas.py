import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# CARGA Y PREPARACIÓN DE DATOS
# =============================================================================

def cargar_datos_tareas():
    """
    Carga datos de tareas desde la API y simula columnas adicionales para análisis.
    Retorna un DataFrame con columnas enriquecidas para análisis de datos.
    """
    url = "http://localhost:5000/api/tareas"
    resp = requests.get(url)
    datos = resp.json()
    df = pd.DataFrame(datos)
    
    if df.empty:
        print("No hay datos de tareas disponibles")
        return pd.DataFrame()
    
    # Mapear columnas existentes a nombres más descriptivos
    df = df.rename(columns={
        'created_at': 'fecha_creacion',
        'updated_at': 'fecha_actualizacion'
    })
    
    # Simular datos adicionales para análisis (basado en datos reales)
    np.random.seed(42)  # Para reproducibilidad
    n_tareas = len(df)
    
    # Simular fechas límite (entre 1-30 días después de creación)
    df['fecha_limite'] = pd.to_datetime(df['fecha_creacion']) + pd.to_timedelta(
        np.random.randint(1, 31, n_tareas), unit='D'
    )
    
    # Simular prioridades
    prioridades = ['baja', 'media', 'alta', 'urgente']
    df['prioridad'] = np.random.choice(prioridades, n_tareas, p=[0.3, 0.4, 0.25, 0.05])
    
    # Simular tiempo estimado (en horas)
    df['tiempo_estimado'] = np.random.lognormal(mean=1.5, sigma=0.8, size=n_tareas).round(1)
    
    # Simular fecha de completado (solo para tareas completadas)
    df['completado_en'] = None
    completadas = df['estado'] == 'completada'
    if completadas.any():
        fechas_completado = []
        for idx, row in df[completadas].iterrows():
            inicio = pd.to_datetime(row['fecha_creacion'])
            limite = pd.to_datetime(row['fecha_limite'])
            # Completado entre creación y límite (80% de las veces)
            if np.random.random() < 0.8:
                dias_diff = (limite - inicio).days
                completado = inicio + timedelta(days=np.random.randint(0, max(1, dias_diff)))
            else:
                # 20% se completan después del límite
                completado = limite + timedelta(days=np.random.randint(1, 5))
            fechas_completado.append(completado)
        
        df.loc[completadas, 'completado_en'] = fechas_completado
    
    # Convertir columnas de fecha
    columnas_fecha = ['fecha_creacion', 'fecha_actualizacion', 'fecha_limite', 'completado_en']
    for col in columnas_fecha:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Convertir tiempo estimado a numérico
    df['tiempo_estimado'] = pd.to_numeric(df['tiempo_estimado'], errors='coerce')
    
    return df

# =============================================================================
# FUNCIONES DE ANÁLISIS TEMPORAL
# =============================================================================

def analisis_creacion_tareas(df):
    """
    Analiza cuándo se crean más tareas.
    Retorna estadísticas y visualizaciones sobre patrones de creación.
    """
    if df.empty or 'fecha_creacion' not in df.columns:
        print("No hay datos de fecha de creación disponibles")
        return None
    
    # Agregar columnas derivadas para análisis temporal
    df['hora_creacion'] = df['fecha_creacion'].dt.hour
    df['dia_semana'] = df['fecha_creacion'].dt.day_name()
    df['mes'] = df['fecha_creacion'].dt.month_name()
    df['dia_mes'] = df['fecha_creacion'].dt.day
    
    print("=== ANÁLISIS: ¿CUÁNDO SE CREAN MÁS TAREAS? ===")
    
    # Por hora del día
    print("\n📊 Distribución por hora del día:")
    por_hora = df['hora_creacion'].value_counts().sort_index()
    print(por_hora)
    
    # Por día de la semana
    print("\n📅 Distribución por día de la semana:")
    orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    por_dia = df['dia_semana'].value_counts().reindex(orden_dias, fill_value=0)
    print(por_dia)
    
    # Por mes
    print("\n🗓️ Distribución por mes:")
    por_mes = df['mes'].value_counts()
    print(por_mes)
    
    # Estadísticas resumidas
    stats = {
        'hora_pico': por_hora.idxmax(),
        'dia_pico': por_dia.idxmax(),
        'mes_pico': por_mes.idxmax(),
        'total_tareas': len(df),
        'promedio_por_dia': len(df) / df['fecha_creacion'].dt.date.nunique() if not df.empty else 0
    }
    
    print(f"\n📈 RESUMEN:")
    print(f"• Hora pico: {stats['hora_pico']}:00")
    print(f"• Día pico: {stats['dia_pico']}")
    print(f"• Mes pico: {stats['mes_pico']}")
    print(f"• Promedio tareas/día: {stats['promedio_por_dia']:.1f}")
    
    return stats

def analisis_vencimientos(df):
    """
    Analiza cuándo suelen vencer las tareas y patrones de vencimiento.
    """
    if df.empty or 'fecha_limite' not in df.columns:
        print("No hay datos de fecha límite disponibles")
        return None
    
    print("\n=== ANÁLISIS: ¿CUÁNDO SUELEN VENCER LAS TAREAS? ===")
    
    # Tiempo hasta vencimiento desde creación
    df['dias_hasta_vencimiento'] = (df['fecha_limite'] - df['fecha_creacion']).dt.days
    
    # Análisis de vencimientos por día de la semana
    df['dia_vencimiento'] = df['fecha_limite'].dt.day_name()
    
    print("\n⏰ Distribución de plazos (días hasta vencimiento):")
    print(df['dias_hasta_vencimiento'].describe())
    
    print("\n📅 Día de la semana más común para vencimientos:")
    orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    por_dia_venc = df['dia_vencimiento'].value_counts().reindex(orden_dias, fill_value=0)
    print(por_dia_venc)
    
    # Tareas que ya vencieron
    hoy = datetime.now()
    vencidas = df[df['fecha_limite'] < hoy]
    print(f"\n⚠️ Tareas vencidas: {len(vencidas)} de {len(df)} ({len(vencidas)/len(df)*100:.1f}%)")
    
    return {
        'promedio_dias_limite': df['dias_hasta_vencimiento'].mean(),
        'mediana_dias_limite': df['dias_hasta_vencimiento'].median(),
        'dia_vencimiento_comun': por_dia_venc.idxmax(),
        'tareas_vencidas': len(vencidas),
        'porcentaje_vencidas': len(vencidas)/len(df)*100 if len(df) > 0 else 0
    }

# =============================================================================
# FUNCIONES DE ANÁLISIS DE PRIORIDADES
# =============================================================================

def analisis_prioridades(df):
    """
    Analiza qué urgencias se atienden más y patrones de priorización.
    """
    if df.empty or 'prioridad' not in df.columns:
        print("No hay datos de prioridad disponibles")
        return None
    
    print("\n=== ANÁLISIS: ¿QUÉ URGENCIAS SE ATIENDEN MÁS? ===")
    
    # Distribución de prioridades
    print("\n🎯 Distribución de prioridades:")
    dist_prioridades = df['prioridad'].value_counts()
    print(dist_prioridades)
    print(f"Porcentajes: {(dist_prioridades / len(df) * 100).round(1)}")
    
    # Prioridades por estado
    print("\n📊 Prioridades por estado:")
    crosstab = pd.crosstab(df['prioridad'], df['estado'], margins=True)
    print(crosstab)
    
    # Tasa de completitud por prioridad
    if 'estado' in df.columns:
        completitud = df.groupby('prioridad')['estado'].apply(
            lambda x: (x == 'completada').sum() / len(x) * 100
        ).round(1)
        print("\n✅ Tasa de completitud por prioridad (%):")
        print(completitud)
    
    return {
        'prioridad_mas_comun': dist_prioridades.idxmax(),
        'distribucion_prioridades': dist_prioridades.to_dict(),
        'tasa_completitud_por_prioridad': completitud.to_dict() if 'completitud' in locals() else {}
    }

# =============================================================================
# FUNCIONES DE ANÁLISIS DE DURACIÓN
# =============================================================================

def analisis_duracion(df):
    """
    Analiza cuánto duran las tareas y patrones de estimación vs realidad.
    """
    if df.empty or 'tiempo_estimado' not in df.columns:
        print("No hay datos de tiempo estimado disponibles")
        return None
    
    print("\n=== ANÁLISIS: ¿CUÁNTO DURAN LAS TAREAS? ===")
    
    # Estadísticas de tiempo estimado
    print("\n⏱️ Estadísticas de tiempo estimado (horas):")
    print(df['tiempo_estimado'].describe())
    
    # Distribución por rangos
    df['rango_tiempo'] = pd.cut(
        df['tiempo_estimado'], 
        bins=[0, 1, 4, 8, 16, float('inf')], 
        labels=['Muy corta (<1h)', 'Corta (1-4h)', 'Media (4-8h)', 'Larga (8-16h)', 'Muy larga (>16h)']
    )
    
    print("\n📊 Distribución por rangos de duración:")
    print(df['rango_tiempo'].value_counts())
    
    # Tiempo por prioridad
    if 'prioridad' in df.columns:
        print("\n🎯 Tiempo promedio por prioridad:")
        tiempo_por_prioridad = df.groupby('prioridad')['tiempo_estimado'].agg(['mean', 'median']).round(1)
        print(tiempo_por_prioridad)
    
    return {
        'tiempo_promedio': df['tiempo_estimado'].mean(),
        'tiempo_mediano': df['tiempo_estimado'].median(),
        'rango_mas_comun': df['rango_tiempo'].mode()[0] if not df['rango_tiempo'].mode().empty else None
    }

# =============================================================================
# FUNCIONES DE ANÁLISIS DE COMPLETITUD
# =============================================================================

def analisis_completitud(df):
    """
    Analiza qué tareas se completan, cuándo y patrones de rendimiento.
    """
    if df.empty:
        print("No hay datos disponibles")
        return None
    
    print("\n=== ANÁLISIS: ¿QUÉ TAREAS SE COMPLETAN Y CUÁNDO? ===")
    
    # Distribución de estados
    print("\n📊 Distribución de estados:")
    dist_estados = df['estado'].value_counts()
    print(dist_estados)
    print(f"Porcentajes: {(dist_estados / len(df) * 100).round(1)}")
    
    # Análisis de tareas completadas
    completadas = df[df['estado'] == 'completada'].copy()
    
    if len(completadas) > 0 and 'completado_en' in df.columns:
        # Tiempo real de ejecución
        completadas['tiempo_real'] = (
            completadas['completado_en'] - completadas['fecha_creacion']
        ).dt.days
        
        print(f"\n✅ Análisis de {len(completadas)} tareas completadas:")
        print(f"• Tiempo promedio de completado: {completadas['tiempo_real'].mean():.1f} días")
        print(f"• Tiempo mediano de completado: {completadas['tiempo_real'].median():.1f} días")
        
        # Completadas a tiempo vs retrasadas
        if 'fecha_limite' in df.columns:
            a_tiempo = completadas['completado_en'] <= completadas['fecha_limite']
            print(f"• Completadas a tiempo: {a_tiempo.sum()} ({a_tiempo.sum()/len(completadas)*100:.1f}%)")
            print(f"• Completadas con retraso: {(~a_tiempo).sum()} ({(~a_tiempo).sum()/len(completadas)*100:.1f}%)")
        
        # Día de la semana de completado
        completadas['dia_completado'] = completadas['completado_en'].dt.day_name()
        print("\n📅 Día más común para completar tareas:")
        print(completadas['dia_completado'].value_counts().head())
    
    return {
        'tasa_completitud': len(completadas) / len(df) * 100 if len(df) > 0 else 0,
        'distribucion_estados': dist_estados.to_dict(),
        'tiempo_promedio_completado': completadas['tiempo_real'].mean() if len(completadas) > 0 and 'tiempo_real' in completadas.columns else None
    }

# =============================================================================
# FUNCIONES DE RESUMEN Y MÉTRICAS GENERALES
# =============================================================================

def generar_reporte_completo(df):
    """
    Genera un reporte completo con todas las métricas y análisis.
    """
    print("🚀 GENERANDO REPORTE COMPLETO DE ANÁLISIS DE TAREAS")
    print("=" * 60)
    
    # Ejecutar todos los análisis
    stats_creacion = analisis_creacion_tareas(df)
    stats_vencimientos = analisis_vencimientos(df)
    stats_prioridades = analisis_prioridades(df)
    stats_duracion = analisis_duracion(df)
    stats_completitud = analisis_completitud(df)
    
    # Resumen ejecutivo
    print("\n" + "="*60)
    print("📋 RESUMEN EJECUTIVO")
    print("="*60)
    
    if stats_creacion:
        print(f"🕐 Hora pico de creación: {stats_creacion['hora_pico']}:00")
        print(f"📅 Día pico de creación: {stats_creacion['dia_pico']}")
    
    if stats_prioridades:
        print(f"🎯 Prioridad más común: {stats_prioridades['prioridad_mas_comun']}")
    
    if stats_duracion:
        print(f"⏱️ Duración promedio: {stats_duracion['tiempo_promedio']:.1f} horas")
    
    if stats_completitud:
        print(f"✅ Tasa de completitud: {stats_completitud['tasa_completitud']:.1f}%")
    
    if stats_vencimientos:
        print(f"⚠️ Tareas vencidas: {stats_vencimientos['porcentaje_vencidas']:.1f}%")
    
    return {
        'creacion': stats_creacion,
        'vencimientos': stats_vencimientos,
        'prioridades': stats_prioridades,
        'duracion': stats_duracion,
        'completitud': stats_completitud
    }

def exportar_analisis(df, filename='tareas_analizadas.csv'):
    """
    Exporta el DataFrame con análisis adicionales a CSV.
    """
    # Agregar columnas derivadas útiles
    if 'fecha_creacion' in df.columns:
        df['mes_creacion'] = df['fecha_creacion'].dt.month_name()
        df['dia_semana_creacion'] = df['fecha_creacion'].dt.day_name()
        df['hora_creacion'] = df['fecha_creacion'].dt.hour
    
    if 'fecha_limite' in df.columns and 'fecha_creacion' in df.columns:
        df['dias_plazo'] = (df['fecha_limite'] - df['fecha_creacion']).dt.days
    
    if 'completado_en' in df.columns and 'fecha_creacion' in df.columns:
        df['dias_ejecucion'] = (df['completado_en'] - df['fecha_creacion']).dt.days
    
    # Exportar
    df.to_csv(filename, index=False)
    print(f"📁 Datos exportados a: {filename}")
    print(f"📊 Columnas incluidas: {', '.join(df.columns)}")

# =============================================================================
# FUNCIONES DE VISUALIZACIÓN
# =============================================================================

def crear_visualizaciones(df):
    """
    Crea visualizaciones útiles para el análisis de tareas.
    """
    if df.empty:
        print("No hay datos para visualizar")
        return
    
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Dashboard de Análisis de Tareas', fontsize=16, fontweight='bold')
    
    # 1. Distribución de estados
    if 'estado' in df.columns:
        df['estado'].value_counts().plot(kind='pie', ax=axes[0,0], autopct='%1.1f%%')
        axes[0,0].set_title('Distribución de Estados')
        axes[0,0].set_ylabel('')
    
    # 2. Tareas por prioridad
    if 'prioridad' in df.columns:
        df['prioridad'].value_counts().plot(kind='bar', ax=axes[0,1], color='skyblue')
        axes[0,1].set_title('Tareas por Prioridad')
        axes[0,1].tick_params(axis='x', rotation=45)
    
    # 3. Tiempo estimado por rango
    if 'tiempo_estimado' in df.columns:
        df['tiempo_estimado'].hist(bins=20, ax=axes[1,0], color='lightgreen', alpha=0.7)
        axes[1,0].set_title('Distribución de Tiempo Estimado (horas)')
        axes[1,0].set_xlabel('Horas')
        axes[1,0].set_ylabel('Frecuencia')
    
    # 4. Creación por día de la semana
    if 'fecha_creacion' in df.columns:
        dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df_dias = df['fecha_creacion'].dt.day_name().value_counts().reindex(dias_orden, fill_value=0)
        df_dias.plot(kind='bar', ax=axes[1,1], color='coral')
        axes[1,1].set_title('Creación de Tareas por Día')
        axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('analisis_tareas_dashboard.png', dpi=300, bbox_inches='tight')
    print("📊 Dashboard guardado como 'analisis_tareas_dashboard.png'")
    plt.show()

# =============================================================================
# SCRIPT PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    # Cargar datos
    df = cargar_datos_tareas()
    
    if not df.empty:
        # Ejecutar análisis completo
        reporte = generar_reporte_completo(df)
        
        # Crear visualizaciones
        try:
            crear_visualizaciones(df)
        except Exception as e:
            print(f"⚠️ No se pudieron crear visualizaciones: {e}")
        
        # Exportar resultados
        exportar_analisis(df)
        
        print("\n🎉 ¡Análisis completo finalizado!")
        print("💡 Usa las funciones individuales para análisis específicos:")
        print("   - analisis_creacion_tareas(df)")
        print("   - analisis_vencimientos(df)")
        print("   - analisis_prioridades(df)")
        print("   - analisis_duracion(df)")
        print("   - analisis_completitud(df)")
    else:
        print("❌ No se pudieron cargar datos para análisis")