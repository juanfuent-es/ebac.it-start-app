#!/usr/bin/env python3
"""
DEMO: Análisis de Tareas con Pandas
===================================

Este script demuestra cómo usar las funciones de análisis de tareas
para obtener insights valiosos de los datos.

Autor: Asistente IA
Fecha: 2025
"""

from analisis_tareas import *

def demo_basico():
    """
    Demostración básica: cargar datos y ejecutar análisis individuales.
    """
    print("🚀 DEMO BÁSICO: Análisis Individual de Tareas")
    print("=" * 50)
    
    # 1. Cargar datos
    print("📥 Cargando datos de tareas...")
    df = cargar_datos_tareas()
    
    if df.empty:
        print("❌ No hay datos disponibles. Asegúrate de que el servidor esté corriendo.")
        return
    
    print(f"✅ Datos cargados: {len(df)} tareas")
    print(f"📊 Columnas disponibles: {', '.join(df.columns)}")
    
    # 2. Análisis temporal
    print("\n" + "="*50)
    stats_tiempo = analisis_creacion_tareas(df)
    
    # 3. Análisis de prioridades
    print("\n" + "="*50)
    stats_prioridad = analisis_prioridades(df)
    
    # 4. Análisis de duración
    print("\n" + "="*50)
    stats_duracion = analisis_duracion(df)
    
    # 5. Análisis de completitud
    print("\n" + "="*50)
    stats_completitud = analisis_completitud(df)
    
    return df

def demo_avanzado():
    """
    Demostración avanzada: análisis completo con visualizaciones.
    """
    print("\n🎯 DEMO AVANZADO: Análisis Completo")
    print("=" * 50)
    
    # Cargar datos
    df = cargar_datos_tareas()
    
    if df.empty:
        print("❌ No hay datos disponibles.")
        return
    
    # Generar reporte completo
    reporte = generar_reporte_completo(df)
    
    # Crear visualizaciones
    print("\n📊 Generando visualizaciones...")
    try:
        crear_visualizaciones(df)
    except Exception as e:
        print(f"⚠️ Error en visualizaciones: {e}")
    
    # Exportar datos
    print("\n💾 Exportando datos analizados...")
    exportar_analisis(df, 'demo_tareas_analizadas.csv')
    
    return df, reporte

def demo_casos_uso():
    """
    Demostración de casos de uso específicos.
    """
    print("\n💡 DEMO: Casos de Uso Específicos")
    print("=" * 50)
    
    df = cargar_datos_tareas()
    
    if df.empty:
        return
    
    print("📋 CASO 1: Identificar patrones de productividad")
    print("-" * 40)
    
    # ¿En qué horario se crean más tareas?
    if 'fecha_creacion' in df.columns:
        df['hora'] = df['fecha_creacion'].dt.hour
        horas_pico = df['hora'].value_counts().sort_index()
        print("🕐 Horas con más creación de tareas:")
        for hora, count in horas_pico.head().items():
            print(f"   {hora}:00 - {count} tareas")
    
    print("\n📋 CASO 2: Análisis de eficiencia por prioridad")
    print("-" * 40)
    
    if 'prioridad' in df.columns and 'estado' in df.columns:
        eficiencia = df.groupby('prioridad')['estado'].apply(
            lambda x: (x == 'completada').mean() * 100
        ).round(1)
        print("✅ Tasa de completitud por prioridad:")
        for prioridad, tasa in eficiencia.items():
            print(f"   {prioridad.capitalize()}: {tasa}%")
    
    print("\n📋 CASO 3: Predicción de retrasos")
    print("-" * 40)
    
    if 'tiempo_estimado' in df.columns and 'prioridad' in df.columns:
        tiempo_por_prioridad = df.groupby('prioridad')['tiempo_estimado'].mean().round(1)
        print("⏱️ Tiempo promedio por prioridad (horas):")
        for prioridad, tiempo in tiempo_por_prioridad.items():
            print(f"   {prioridad.capitalize()}: {tiempo}h")
    
    print("\n📋 CASO 4: Identificar cuellos de botella")
    print("-" * 40)
    
    pendientes = df[df['estado'] == 'pendiente']
    if len(pendientes) > 0:
        print(f"⚠️ Tareas pendientes: {len(pendientes)}")
        if 'prioridad' in pendientes.columns:
            print("🎯 Distribución de prioridades en pendientes:")
            dist = pendientes['prioridad'].value_counts()
            for prioridad, count in dist.items():
                print(f"   {prioridad.capitalize()}: {count}")

def demo_interactivo():
    """
    Demostración interactiva donde el usuario puede elegir qué análisis ejecutar.
    """
    print("\n🎮 DEMO INTERACTIVO")
    print("=" * 50)
    
    df = cargar_datos_tareas()
    
    if df.empty:
        print("❌ No hay datos disponibles.")
        return
    
    opciones = {
        '1': ('Análisis temporal', lambda: analisis_creacion_tareas(df)),
        '2': ('Análisis de vencimientos', lambda: analisis_vencimientos(df)),
        '3': ('Análisis de prioridades', lambda: analisis_prioridades(df)),
        '4': ('Análisis de duración', lambda: analisis_duracion(df)),
        '5': ('Análisis de completitud', lambda: analisis_completitud(df)),
        '6': ('Reporte completo', lambda: generar_reporte_completo(df)),
        '7': ('Crear visualizaciones', lambda: crear_visualizaciones(df)),
        '8': ('Exportar datos', lambda: exportar_analisis(df))
    }
    
    print("Selecciona el análisis que quieres ejecutar:")
    for key, (nombre, _) in opciones.items():
        print(f"  {key}. {nombre}")
    
    # Para demo automática, ejecutamos algunas opciones
    print("\n🤖 Ejecutando automáticamente algunas opciones...")
    
    # Ejecutar análisis temporal
    print("\n➡️ Ejecutando opción 1: Análisis temporal")
    opciones['1'][1]()
    
    # Ejecutar análisis de prioridades
    print("\n➡️ Ejecutando opción 3: Análisis de prioridades")
    opciones['3'][1]()

def main():
    """
    Función principal que ejecuta todas las demostraciones.
    """
    print("🎉 BIENVENIDO AL DEMO DE ANÁLISIS DE TAREAS")
    print("=" * 60)
    print("Este script demuestra el poder del análisis de datos con Pandas")
    print("aplicado a la gestión de tareas.")
    print()
    
    try:
        # Demo básico
        df = demo_basico()
        
        if df is not None and not df.empty:
            # Demo avanzado
            demo_avanzado()
            
            # Casos de uso
            demo_casos_uso()
            
            # Demo interactivo
            demo_interactivo()
            
            print("\n🎊 ¡DEMO COMPLETADO!")
            print("=" * 60)
            print("💡 PRÓXIMOS PASOS:")
            print("   1. Modifica las funciones según tus necesidades")
            print("   2. Agrega nuevas métricas o visualizaciones")
            print("   3. Integra con sistemas de alertas o dashboards")
            print("   4. Programa ejecuciones automáticas para reportes periódicos")
            print("\n📚 RECURSOS:")
            print("   - Documentación de Pandas: https://pandas.pydata.org/docs/")
            print("   - Matplotlib para visualizaciones: https://matplotlib.org/")
            print("   - Seaborn para gráficos estadísticos: https://seaborn.pydata.org/")
        
    except Exception as e:
        print(f"❌ Error durante la demostración: {e}")
        print("💡 Asegúrate de que:")
        print("   1. El servidor Flask esté corriendo en localhost:5000")
        print("   2. Tengas datos de tareas en la base de datos")
        print("   3. Las dependencias estén instaladas (pandas, requests, matplotlib, seaborn)")

if __name__ == "__main__":
    main()