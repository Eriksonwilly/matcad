#!/usr/bin/env python3
"""
Script de prueba para verificar que matplotlib y la generación de PDF funcionen correctamente
"""

import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

def test_matplotlib():
    """Prueba que matplotlib funcione correctamente"""
    try:
        # Crear un gráfico simple
        fig, ax = plt.subplots(figsize=(8, 6))
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y, 'b-', linewidth=2, label='sin(x)')
        ax.set_title('Prueba de Matplotlib')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Guardar en buffer
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
        buffer.seek(0)
        plt.close(fig)
        
        return buffer, "✅ Matplotlib funcionando correctamente"
    except Exception as e:
        return None, f"❌ Error en matplotlib: {str(e)}"

def test_pdf_generation():
    """Prueba la generación de PDF"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        
        # Crear PDF de prueba
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []
        
        elements.append(Paragraph("Prueba de Generación de PDF", styles["Heading1"]))
        elements.append(Paragraph("Este es un PDF de prueba generado con ReportLab", styles["Normal"]))
        
        doc.build(elements)
        buffer.seek(0)
        
        return buffer, "✅ PDF generado correctamente"
    except Exception as e:
        return None, f"❌ Error en PDF: {str(e)}"

def main():
    st.title("🧪 Pruebas de Funcionalidad")
    st.write("Verificando que matplotlib y PDF funcionen correctamente...")
    
    # Prueba matplotlib
    st.subheader("1. Prueba de Matplotlib")
    buffer, message = test_matplotlib()
    st.write(message)
    
    if buffer:
        st.image(buffer, caption="Gráfico de prueba generado con matplotlib", use_column_width=True)
    else:
        st.error("No se pudo generar el gráfico")
    
    # Prueba PDF
    st.subheader("2. Prueba de Generación de PDF")
    pdf_buffer, pdf_message = test_pdf_generation()
    st.write(pdf_message)
    
    if pdf_buffer:
        st.download_button(
            label="📄 Descargar PDF de Prueba",
            data=pdf_buffer.getvalue(),
            file_name="test_pdf.pdf",
            mime="application/pdf"
        )
    else:
        st.error("No se pudo generar el PDF")
    
    # Información del sistema
    st.subheader("3. Información del Sistema")
    st.write(f"**Matplotlib version:** {matplotlib.__version__}")
    st.write(f"**NumPy version:** {np.__version__}")
    
    try:
        import reportlab
        st.write(f"**ReportLab version:** {reportlab.Version}")
    except:
        st.write("**ReportLab:** No disponible")

if __name__ == "__main__":
    main() 