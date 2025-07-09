#!/usr/bin/env python3
"""
Script de prueba para verificar gráficos y PDF
CONSORCIO DEJ - Análisis Estructural
"""

import sys
import os

def test_dependencies():
    """Probar que todas las dependencias estén disponibles"""
    print("🔍 Probando dependencias...")
    
    # Probar matplotlib
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        print("✅ Matplotlib - OK")
        matplotlib_ok = True
    except ImportError as e:
        print(f"❌ Matplotlib - Error: {e}")
        matplotlib_ok = False
    
    # Probar numpy
    try:
        import numpy as np
        print("✅ NumPy - OK")
        numpy_ok = True
    except ImportError as e:
        print(f"❌ NumPy - Error: {e}")
        numpy_ok = False
    
    # Probar reportlab
    try:
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        print("✅ ReportLab - OK")
        reportlab_ok = True
    except ImportError as e:
        print(f"❌ ReportLab - Error: {e}")
        reportlab_ok = False
    
    # Probar plotly
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly - OK")
        plotly_ok = True
    except ImportError as e:
        print(f"❌ Plotly - Error: {e}")
        plotly_ok = False
    
    return matplotlib_ok, numpy_ok, reportlab_ok, plotly_ok

def test_matplotlib_graphics():
    """Probar generación de gráficos con matplotlib"""
    print("\n📊 Probando gráficos de matplotlib...")
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        from io import BytesIO
        
        # Crear un gráfico simple
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y, 'b-', linewidth=2, label='sin(x)')
        ax.set_title('Gráfico de Prueba - Matplotlib')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Guardar en BytesIO
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=200)
        plt.close(fig)
        img_buffer.seek(0)
        
        print("✅ Gráfico de matplotlib generado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error generando gráfico de matplotlib: {e}")
        return False

def test_reportlab_pdf():
    """Probar generación de PDF con reportlab"""
    print("\n📄 Probando generación de PDF...")
    
    try:
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from io import BytesIO
        
        # Crear PDF simple
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=(8.5*inch, 11*inch))
        styles = getSampleStyleSheet()
        elements = []
        
        # Agregar contenido
        elements.append(Paragraph("CONSORCIO DEJ - Prueba de PDF", styles["Heading1"]))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Este es un PDF de prueba generado con ReportLab", styles["Normal"]))
        
        # Crear tabla
        data = [["Propiedad", "Valor"], ["f'c", "210 kg/cm²"], ["fy", "4200 kg/cm²"]]
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        
        # Construir PDF
        doc.build(elements)
        pdf_buffer.seek(0)
        
        print("✅ PDF generado correctamente con ReportLab")
        return True
        
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        return False

def test_app_functions():
    """Probar funciones específicas de la aplicación"""
    print("\n🏗️ Probando funciones de la aplicación...")
    
    try:
        # Importar funciones de APP.py
        from APP import calcular_propiedades_concreto, calcular_propiedades_acero
        
        # Probar cálculos
        props_concreto = calcular_propiedades_concreto(210)
        props_acero = calcular_propiedades_acero(4200)
        
        print(f"✅ Propiedades del concreto: Ec = {props_concreto['Ec']:.0f} kg/cm²")
        print(f"✅ Propiedades del acero: Es = {props_acero['Es']:,} kg/cm²")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en funciones de la aplicación: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 CONSORCIO DEJ - Pruebas de Gráficos y PDF")
    print("=" * 50)
    
    # Probar dependencias
    matplotlib_ok, numpy_ok, reportlab_ok, plotly_ok = test_dependencies()
    
    # Probar gráficos si matplotlib está disponible
    if matplotlib_ok:
        test_matplotlib_graphics()
    
    # Probar PDF si reportlab está disponible
    if reportlab_ok:
        test_reportlab_pdf()
    
    # Probar funciones de la aplicación
    test_app_functions()
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    print(f"Matplotlib: {'✅ OK' if matplotlib_ok else '❌ Error'}")
    print(f"NumPy: {'✅ OK' if numpy_ok else '❌ Error'}")
    print(f"ReportLab: {'✅ OK' if reportlab_ok else '❌ Error'}")
    print(f"Plotly: {'✅ OK' if plotly_ok else '❌ Error'}")
    
    if matplotlib_ok and reportlab_ok:
        print("\n🎉 ¡Todo está funcionando correctamente!")
        print("🚀 Puedes ejecutar la aplicación: streamlit run APP.py")
    else:
        print("\n⚠️ Algunas dependencias tienen problemas.")
        print("💡 Ejecuta: pip install -r requirements.txt")
        print("💡 O ejecuta: python install_dependencies.py")

if __name__ == "__main__":
    main() 