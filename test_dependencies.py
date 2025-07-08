#!/usr/bin/env python3
"""
Script de prueba para verificar que todas las dependencias funcionen correctamente
"""

import sys
import traceback

def test_matplotlib():
    """Prueba matplotlib"""
    try:
        import matplotlib
        matplotlib.use('Agg')  # Backend no interactivo
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Crear un gráfico simple
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y, 'b-', linewidth=2, label='sin(x)')
        ax.set_title('Prueba de Matplotlib')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Guardar el gráfico
        fig.savefig('test_matplotlib.png', dpi=150, bbox_inches='tight')
        plt.close(fig)
        
        print("✅ Matplotlib funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error con Matplotlib: {e}")
        traceback.print_exc()
        return False

def test_reportlab():
    """Prueba reportlab"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        
        # Crear un PDF simple
        doc = SimpleDocTemplate("test_reportlab.pdf", pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []
        
        elements.append(Paragraph("Prueba de ReportLab", styles["Heading1"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Este es un PDF de prueba generado con ReportLab", styles["Normal"]))
        
        doc.build(elements)
        print("✅ ReportLab funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error con ReportLab: {e}")
        traceback.print_exc()
        return False

def test_plotly():
    """Prueba plotly"""
    try:
        import plotly.express as px
        import pandas as pd
        
        # Crear datos de prueba
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 1, 5, 3]
        })
        
        # Crear gráfico
        fig = px.line(df, x='x', y='y', title='Prueba de Plotly')
        fig.write_html('test_plotly.html')
        
        print("✅ Plotly funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error con Plotly: {e}")
        traceback.print_exc()
        return False

def test_streamlit():
    """Prueba streamlit"""
    try:
        import streamlit as st
        print("✅ Streamlit está disponible")
        return True
    except Exception as e:
        print(f"❌ Error con Streamlit: {e}")
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🔧 Verificando dependencias...")
    print("=" * 50)
    
    results = {}
    
    # Probar cada dependencia
    results['matplotlib'] = test_matplotlib()
    results['reportlab'] = test_reportlab()
    results['plotly'] = test_plotly()
    results['streamlit'] = test_streamlit()
    
    print("=" * 50)
    print("📊 Resumen de resultados:")
    
    all_passed = True
    for dep, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"  {dep}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 ¡Todas las dependencias funcionan correctamente!")
        print("✅ Tu aplicación Streamlit debería funcionar sin problemas")
    else:
        print("⚠️ Algunas dependencias tienen problemas")
        print("🔧 Revisa los errores arriba e instala las dependencias faltantes")
    
    return all_passed

if __name__ == "__main__":
    main() 