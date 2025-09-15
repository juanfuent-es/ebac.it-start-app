#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Seed para Poblar Base de Datos
=====================================

Este script lee el archivo tareas.csv y pobla la base de datos SQLite
con las categorías y tareas correspondientes.

Autor: Sistema de Seed de Tareas
Fecha: 2025
"""

import pandas as pd
import sqlite3
from datetime import datetime
from database import init_db, connect_db, execute
from models.categoria import Categoria
from models.tarea import Tarea

class DatabaseSeeder:
    """Clase para poblar la base de datos con datos del CSV"""
    
    def __init__(self, csv_file='tareas.csv'):
        self.csv_file = csv_file
        self.df = None
        self.categoria_mapping = {}  # Mapeo de nombre de categoría a ID
        
    def load_csv_data(self):
        """Cargar y procesar los datos del archivo CSV"""
        print("📊 Cargando datos del archivo CSV...")
        
        try:
            # Cargar el archivo CSV
            self.df = pd.read_csv(self.csv_file)
            
            # Convertir columnas de fecha
            date_columns = ['fecha_creacion', 'fecha_limite', 'fecha_completado', 'fecha_actualizacion']
            for col in date_columns:
                if col in self.df.columns:
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
            
            print(f"✅ Datos cargados: {len(self.df)} registros")
            print(f"📋 Columnas: {list(self.df.columns)}")
            
            # Mostrar categorías únicas
            if 'categoria' in self.df.columns:
                categorias_unicas = self.df['categoria'].unique()
                print(f"🏷️ Categorías encontradas: {len(categorias_unicas)}")
                for cat in sorted(categorias_unicas):
                    count = len(self.df[self.df['categoria'] == cat])
                    print(f"   - {cat}: {count} tareas")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al cargar CSV: {e}")
            return False
    
    def seed_categorias(self):
        """Crear categorías en la base de datos"""
        print("\n🏷️ POBLANDO CATEGORÍAS...")
        
        if 'categoria' not in self.df.columns:
            print("❌ No se encontró la columna 'categoria' en el CSV")
            return False
        
        categorias_unicas = self.df['categoria'].unique()
        categorias_creadas = 0
        
        for categoria_nombre in sorted(categorias_unicas):
            if pd.isna(categoria_nombre) or categoria_nombre.strip() == "":
                continue
                
            try:
                # Usar get_or_create para evitar duplicados
                categoria_id = Categoria.get_or_create(categoria_nombre.strip())
                self.categoria_mapping[categoria_nombre] = categoria_id
                categorias_creadas += 1
                print(f"   ✅ Categoría '{categoria_nombre}' -> ID {categoria_id}")
                
            except Exception as e:
                print(f"   ❌ Error al crear categoría '{categoria_nombre}': {e}")
        
        print(f"✅ Categorías procesadas: {categorias_creadas}/{len(categorias_unicas)}")
        return True
    
    def seed_tareas(self):
        """Crear tareas en la base de datos"""
        print("\n📋 POBLANDO TAREAS...")
        
        tareas_creadas = 0
        tareas_con_error = 0
        
        for index, row in self.df.iterrows():
            try:
                # Validar que tenga categoría
                categoria_nombre = row['categoria']
                if pd.isna(categoria_nombre) or categoria_nombre not in self.categoria_mapping:
                    print(f"   ⚠️ Fila {index + 1}: Categoría inválida '{categoria_nombre}'")
                    tareas_con_error += 1
                    continue
                
                # Preparar datos de la tarea
                nombre = str(row['nombre']).strip()
                if not nombre or nombre == 'nan':
                    print(f"   ⚠️ Fila {index + 1}: Nombre de tarea vacío")
                    tareas_con_error += 1
                    continue
                
                # Estado
                estado = str(row['estado']).strip().lower()
                if estado not in ['pendiente', 'completada', 'en_progreso']:
                    estado = 'pendiente'  # Valor por defecto
                
                # Prioridad
                prioridad = str(row['prioridad']).strip().lower()
                if prioridad not in ['baja', 'media', 'alta']:
                    prioridad = 'media'  # Valor por defecto
                
                # Fecha límite
                fecha_limite = None
                if not pd.isna(row['fecha_limite']):
                    try:
                        fecha_limite = pd.to_datetime(row['fecha_limite'])
                        fecha_limite = fecha_limite.strftime('%Y-%m-%dT%H:%M')
                    except:
                        fecha_limite = None
                
                # Tiempo estimado
                tiempo_estimado = None
                if not pd.isna(row['tiempo_estimado']):
                    try:
                        tiempo_estimado = int(row['tiempo_estimado'])
                    except:
                        tiempo_estimado = None
                
                # Crear la tarea usando el modelo
                categoria_id = self.categoria_mapping[categoria_nombre]
                
                tarea_id = Tarea.create(
                    nombre=nombre,
                    id_categoria=categoria_id,
                    estado=estado,
                    fecha_limite=fecha_limite,
                    prioridad=prioridad,
                    tiempo_estimado=tiempo_estimado
                )
                
                # Si la tarea está completada, actualizar la fecha de completado
                if estado == 'completada' and not pd.isna(row['fecha_completado']):
                    try:
                        fecha_completado = pd.to_datetime(row['fecha_completado'])
                        fecha_completado_str = fecha_completado.strftime('%Y-%m-%d %H:%M:%S')
                        
                        # Actualizar la fecha de completado directamente en la base de datos
                        conn = connect_db()
                        conn.execute(
                            "UPDATE tareas SET completado_en = ? WHERE id = ?",
                            (fecha_completado_str, tarea_id)
                        )
                        conn.commit()
                        conn.close()
                        
                    except Exception as e:
                        print(f"   ⚠️ Error al actualizar fecha completado para tarea {tarea_id}: {e}")
                
                tareas_creadas += 1
                
                # Mostrar progreso cada 100 tareas
                if tareas_creadas % 100 == 0:
                    print(f"   📊 Progreso: {tareas_creadas} tareas creadas...")
                
            except Exception as e:
                print(f"   ❌ Error en fila {index + 1}: {e}")
                tareas_con_error += 1
        
        print(f"✅ Tareas procesadas: {tareas_creadas} creadas, {tareas_con_error} con errores")
        return True
    
    def verify_seed_data(self):
        """Verificar que los datos se insertaron correctamente"""
        print("\n🔍 VERIFICANDO DATOS INSERTADOS...")
        
        try:
            # Verificar categorías
            categorias = Categoria.get_all()
            print(f"📊 Categorías en BD: {len(categorias)}")
            for cat in categorias:
                print(f"   - ID {cat['id']}: {cat['nombre']}")
            
            # Verificar tareas
            tareas = Tarea.get_all()
            print(f"📊 Tareas en BD: {len(tareas)}")
            
            # Estadísticas por estado
            if tareas:
                estados = {}
                for tarea in tareas:
                    estado = tarea['estado']
                    estados[estado] = estados.get(estado, 0) + 1
                
                print("📈 Distribución por estado:")
                for estado, count in estados.items():
                    print(f"   - {estado}: {count} tareas")
            
            # Estadísticas por categoría
            conn = connect_db()
            stats_cat = conn.execute("""
                SELECT c.nombre, COUNT(t.id) as total
                FROM categorias c
                LEFT JOIN tareas t ON c.id = t.id_categoria
                GROUP BY c.id, c.nombre
                ORDER BY total DESC
            """).fetchall()
            conn.close()
            
            print("📊 Tareas por categoría:")
            for stat in stats_cat:
                print(f"   - {stat['nombre']}: {stat['total']} tareas")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al verificar datos: {e}")
            return False
    
    def run_seed(self):
        """Ejecutar el proceso completo de seed"""
        print("🌱 INICIANDO PROCESO DE SEED")
        print("="*60)
        
        # 1. Inicializar base de datos
        print("🗄️ Inicializando base de datos...")
        init_db()
        
        # 2. Cargar datos del CSV
        if not self.load_csv_data():
            return False
        
        # 3. Poblar categorías
        if not self.seed_categorias():
            return False
        
        # 4. Poblar tareas
        if not self.seed_tareas():
            return False
        
        # 5. Verificar datos
        if not self.verify_seed_data():
            return False
        
        print("\n" + "="*60)
        print("✅ PROCESO DE SEED COMPLETADO EXITOSAMENTE")
        print("="*60)
        print("🎯 Resumen:")
        print(f"   - Categorías creadas: {len(self.categoria_mapping)}")
        print(f"   - Tareas procesadas: {len(self.df)}")
        print(f"   - Base de datos lista para usar")
        
        return True


def main():
    """Función principal"""
    print("🌱 GENERADOR DE SEED PARA BASE DE DATOS")
    print("="*60)
    
    # Crear instancia del seeder
    seeder = DatabaseSeeder('tareas.csv')
    
    # Ejecutar seed
    success = seeder.run_seed()
    
    if success:
        print("\n🎉 ¡Base de datos poblada exitosamente!")
        print("💡 Puedes ejecutar tu aplicación Flask ahora")
    else:
        print("\n❌ Error en el proceso de seed")
        print("🔍 Revisa los mensajes de error anteriores")


if __name__ == "__main__":
    main()
