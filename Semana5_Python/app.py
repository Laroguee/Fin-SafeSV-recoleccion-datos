"""
FinSafe SV: Diagnóstico y Monitoreo del Riesgo Crediticio en El Salvador
Entrega 5: Aplicación Web Interactiva en Streamlit (app.py)
"""
import sys
import os

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

from app import *
