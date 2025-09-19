#!/usr/bin/env python3
"""
Archivo WSGI para deploy en Render.com
Este archivo permite que Render ejecute la aplicación Flask
"""

# Importar la aplicación Flask desde app.py
from app import app

# Render necesita que la variable se llame 'application'
application = app