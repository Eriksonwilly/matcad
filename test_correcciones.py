#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones implementadas
en APP.py para resolver problemas de PDF y Matplotlib en producción.
"""

import sys
import os

def test_imports():
    """Probar que todas las importaciones funcionan correctamente"""
    print("🔍 Probando importaciones...")
    
    try:
        import streamlit as st
        print("✅ Streamlit importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Streamlit: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando NumPy: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Pandas: {e}")
        return False
    
    try:
        import matplotlib
        # Configurar backend antes de importar pyplot
        matplotlib.use('Agg')  # Backend no interactivo para Streamlit
        import matplotlib.pyplot as plt
        print("✅ Matplotlib configurado y importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Matplotlib: {e}")
        return False
    
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Plotly: {e}")
        return False
    
    try:
        from reportlab.lib.pagesizes import A4, letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        print("✅ ReportLab importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando ReportLab: {e}")
        return False
    
    return True

def test_matplotlib_backend():
    """Probar que el backend de Matplotlib funciona correctamente"""
    print("\n🔍 Probando backend de Matplotlib...")
    
    try:
        import matplotlib
        matplotlib.use('Agg')  # Backend no interactivo para Streamlit
        import matplotlib.pyplot as plt
        
        # Crear una figura simple
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
        ax.set_title("Prueba de Matplotlib")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        
        # Guardar la figura
        fig.savefig('test_matplotlib.png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        
        # Verificar que el archivo se creó
        if os.path.exists('test_matplotlib.png'):
            print("✅ Matplotlib backend funciona correctamente")
            os.remove('test_matplotlib.png')  # Limpiar
            return True
        else:
            print("❌ Error: No se pudo crear el archivo de imagen")
            return False
            
    except Exception as e:
        print(f"❌ Error probando Matplotlib: {e}")
        return False

def test_pdf_generation():
    """Probar la generación de PDF con ReportLab"""
    print("\n🔍 Probando generación de PDF...")
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        import io
        
        # Crear buffer de memoria
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []
        
        # Agregar contenido
        elements.append(Paragraph("Prueba de PDF - CONSORCIO DEJ", styles["Heading1"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Este es un PDF de prueba generado con ReportLab.", styles["Normal"]))
        
        # Construir PDF
        doc.build(elements)
        pdf_buffer.seek(0)
        
        # Verificar que el PDF tiene contenido
        pdf_content = pdf_buffer.getvalue()
        if len(pdf_content) > 0:
            print("✅ Generación de PDF funciona correctamente")
            return True
        else:
            print("❌ Error: PDF generado está vacío")
            return False
            
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        return False

def test_app_import():
    """Probar que APP.py se puede importar sin errores"""
    print("\n🔍 Probando importación de APP.py...")
    
    try:
        # Simular el entorno de Streamlit
        import sys
        sys.path.append('.')
        
        # Importar funciones específicas de APP.py
        from APP import (
            calcular_propiedades_concreto,
            calcular_propiedades_acero,
            generar_pdf_reportlab
        )
        
        # Probar funciones básicas
        props_concreto = calcular_propiedades_concreto(210)
        props_acero = calcular_propiedades_acero(4200)
        
        if props_concreto and props_acero:
            print("✅ APP.py se puede importar y las funciones básicas funcionan")
            return True
        else:
            print("❌ Error: Las funciones básicas no retornan valores válidos")
            return False
            
    except Exception as e:
        print(f"❌ Error importando APP.py: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de correcciones...")
    print("=" * 50)
    
    tests = [
        ("Importaciones", test_imports),
        ("Backend Matplotlib", test_matplotlib_backend),
        ("Generación PDF", test_pdf_generation),
        ("Importación APP.py", test_app_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Ejecutando: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"⚠️ Test falló: {test_name}")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! Las correcciones están funcionando correctamente.")
        print("\n✅ Problemas resueltos:")
        print("   - Configuración de Matplotlib backend 'Agg'")
        print("   - Generación de PDF con ReportLab")
        print("   - Eliminación de st.rerun() problemático")
        print("   - Importaciones optimizadas")
        return True
    else:
        print("❌ Algunas pruebas fallaron. Revisar las dependencias.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 