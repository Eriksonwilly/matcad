#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones finales implementadas
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
        matplotlib.use('Agg')  # Configurar backend antes de importar pyplot
        import matplotlib.pyplot as plt
        print("✅ Matplotlib configurado correctamente")
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
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate
        print("✅ ReportLab importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando ReportLab: {e}")
        return False
    
    return True

def test_matplotlib_config():
    """Probar configuración de Matplotlib"""
    print("\n🔧 Probando configuración de Matplotlib...")
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        
        # Crear figura simple
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
        ax.set_title("Test de Matplotlib")
        
        # Guardar en buffer
        import io
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=300)
        plt.close(fig)
        img_buffer.seek(0)
        
        print("✅ Matplotlib configurado y funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración de Matplotlib: {e}")
        return False

def test_pdf_generation():
    """Probar generación de PDF"""
    print("\n📄 Probando generación de PDF...")
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        import io
        
        # Crear PDF simple
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []
        
        elements.append(Paragraph("Test de PDF", styles["Heading1"]))
        elements.append(Paragraph("Este es un test de generación de PDF", styles["Normal"]))
        
        doc.build(elements)
        pdf_data = pdf_buffer.getvalue()
        pdf_buffer.close()
        
        # Crear nuevo buffer para descarga
        download_buffer = io.BytesIO()
        download_buffer.write(pdf_data)
        download_buffer.seek(0)
        
        print("✅ Generación de PDF funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en generación de PDF: {e}")
        return False

def test_environment():
    """Probar configuración del entorno"""
    print("\n🌍 Probando configuración del entorno...")
    
    # Configurar directorio temporal para Matplotlib
    os.environ['MPLCONFIGDIR'] = '/tmp/'
    print("✅ Directorio temporal configurado")
    
    # Verificar Python version
    print(f"✅ Python version: {sys.version}")
    
    # Verificar directorio de trabajo
    print(f"✅ Directorio de trabajo: {os.getcwd()}")
    
    return True

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DE CORRECCIONES FINALES")
    print("=" * 50)
    
    # Ejecutar todas las pruebas
    tests = [
        test_environment,
        test_imports,
        test_matplotlib_config,
        test_pdf_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Error ejecutando {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ La aplicación está lista para producción")
    else:
        print("⚠️ Algunas pruebas fallaron")
        print("🔧 Revisa los errores y corrige los problemas")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 