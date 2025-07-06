import streamlit as st
import math
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import io
import tempfile
import os

# Importar sistema de pagos simple
try:
    from simple_payment_system import payment_system
    PAYMENT_SYSTEM_AVAILABLE = True
except ImportError:
    PAYMENT_SYSTEM_AVAILABLE = False
    st.warning("⚠️ Sistema de pagos no disponible. Usando modo demo.")

# Importaciones opcionales con manejo de errores
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("⚠️ Plotly no está instalado. Los gráficos interactivos no estarán disponibles.")

try:
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    st.warning("⚠️ ReportLab no está instalado. La generación de PDFs no estará disponible.")

# Función para calcular diseño del fuste del muro
def calcular_diseno_fuste(resultados, datos_entrada):
    """
    Calcula el diseño y verificación del fuste del muro según PARTE 2.2.py
    """
    # Datos del fuste
    h1 = datos_entrada['h1']
    gamma_relleno = datos_entrada['gamma_relleno']
    phi_relleno = datos_entrada['phi_relleno']
    cohesion = datos_entrada['cohesion']
    Df = datos_entrada['Df']
    fc = datos_entrada['fc']
    fy = datos_entrada['fy']
    b = resultados['b']
    
    # 1. Cálculo del coeficiente pasivo
    phi_rad = math.radians(phi_relleno)
    kp = (1 + math.sin(phi_rad)) / (1 - math.sin(phi_rad))
    
    # 2. Empuje pasivo en el intradós
    Ep = 0.5 * kp * (gamma_relleno/1000) * Df**2 + 2 * cohesion * Df * math.sqrt(kp)
    Ep_kg_m = Ep * 1000  # Convertir a kg/m
    
    # 3. Altura de aplicación del empuje pasivo
    yt = Df / 3
    
    # 4. Momentos volcadores y estabilizadores
    # Empuje activo total
    ka = resultados['ka']
    Ea_relleno = 0.5 * ka * (gamma_relleno/1000) * h1**2
    Ea_sobrecarga = ka * (datos_entrada['qsc']/1000) * h1
    Ea_total = Ea_relleno + Ea_sobrecarga
    
    # Momentos volcadores
    Mvol_relleno = Ea_relleno * h1 / 3
    Mvol_sobrecarga = Ea_sobrecarga * h1 / 2
    Mvol_total = Mvol_relleno + Mvol_sobrecarga
    
    # Momentos estabilizadores (simplificado)
    W_muro = b * h1 * (datos_entrada['gamma_concreto']/1000)
    W_zapata = resultados['Bz'] * resultados['hz'] * (datos_entrada['gamma_concreto']/1000)
    W_relleno = resultados['t'] * h1 * (gamma_relleno/1000)
    
    # Brazos de momento
    x_muro = resultados['r'] + b/2
    x_zapata = resultados['Bz']/2
    x_relleno = resultados['r'] + b + resultados['t']/2
    
    Mr_muro = W_muro * x_muro
    Mr_zapata = W_zapata * x_zapata
    Mr_relleno = W_relleno * x_relleno
    Mr_pasivo = Ep * yt
    Mesta_total = Mr_muro + Mr_zapata + Mr_relleno + Mr_pasivo
    
    # 5. Factores de seguridad
    FSv = Mesta_total / Mvol_total
    FSd = (math.tan(phi_rad) * (W_muro + W_zapata + W_relleno) + Ep) / Ea_total
    
    # 6. Ubicación de la resultante y excentricidad
    W_total = W_muro + W_zapata + W_relleno
    sum_momentos = Mr_muro + Mr_zapata + Mr_relleno
    x_barra = sum_momentos / W_total
    e = abs(x_barra - resultados['Bz']/2)
    
    # 7. Cálculo del peralte efectivo
    # Momento de diseño
    Mu = 1.4 * Mvol_total  # Factor de carga
    
    # Resistencia del concreto
    fc_kg_cm2 = fc
    fy_kg_cm2 = fy
    
    # Peralte efectivo requerido
    dreq = math.sqrt(Mu * 100000 / (0.9 * 0.85 * fc_kg_cm2 * b * 100 * 0.59))
    hreq = dreq + 9  # Recubrimiento + diámetro de barra
    dreal = resultados['hz'] * 100 - 9  # Peralte real en cm
    
    # 8. Área de acero
    As = Mu * 100000 / (0.9 * fy_kg_cm2 * dreal)
    Asmin = 0.0033 * b * 100 * dreal  # Cuantía mínima
    
    # 9. Distribución del acero
    # Usar barras de 5/8" (1.98 cm²)
    area_barra = 1.98
    num_barras = math.ceil(As / area_barra)
    As_proporcionado = num_barras * area_barra
    separacion = (b * 100 - 6) / (num_barras - 1)  # 3cm de recubrimiento
    
    # 10. Verificación de cuantías
    rho_real = As_proporcionado / (b * 100 * dreal)
    rho_min = 0.0033
    rho_max = 0.0163
    
    # 11. Acero por retracción y temperatura
    As_retraccion = 0.002 * b * 100 * resultados['hz'] * 100
    num_barras_retraccion = math.ceil(As_retraccion / 1.27)  # Barras de 1/2"
    As_retraccion_proporcionado = num_barras_retraccion * 1.27
    
    return {
        'kp': kp,
        'Ep_kg_m': Ep_kg_m,
        'yt': yt,
        'Mvol_total': Mvol_total,
        'Mesta_total': Mesta_total,
        'FSv': FSv,
        'FSd': FSd,
        'x_barra': x_barra,
        'e': e,
        'dreq': dreq,
        'hreq': hreq,
        'dreal': dreal,
        'As': As,
        'Asmin': Asmin,
        'num_barras': num_barras,
        'As_proporcionado': As_proporcionado,
        'separacion': separacion,
        'rho_real': rho_real,
        'As_retraccion': As_retraccion,
        'num_barras_retraccion': num_barras_retraccion,
        'As_retraccion_proporcionado': As_retraccion_proporcionado
    }

# Función para generar PDF del reporte
def generar_pdf_reportlab(resultados, datos_entrada, diseno_fuste, plan="premium"):
    """
    Genera un PDF profesional usando ReportLab
    """
    if not REPORTLAB_AVAILABLE:
        # Crear un archivo de texto simple como fallback
        pdf_buffer = io.BytesIO()
        reporte_texto = f"""
CONSORCIO DEJ
Ingeniería y Construcción
Reporte de Muro de Contención - {plan.upper()}
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Este es un reporte básico. Para reportes en PDF, instale ReportLab:
pip install reportlab

---
Generado por: CONSORCIO DEJ
        """
        pdf_buffer.write(reporte_texto.encode('utf-8'))
        pdf_buffer.seek(0)
        return pdf_buffer
    
    # Crear archivo temporal
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleH = styles["Heading1"]
    styleH2 = styles["Heading2"]
    elements = []
    
    # Función auxiliar para agregar elementos de forma segura
    def add_element(element):
        try:
            elements.append(element)
        except Exception as e:
            print(f"Error agregando elemento: {e}")
            # Agregar elemento de texto simple como fallback
            elements.append(Paragraph(str(element), styleN))
    
    # Título principal
    try:
        elements.append(Paragraph("CONSORCIO DEJ", styleH))
        elements.append(Paragraph("Ingeniería y Construcción", styleN))
        elements.append(Paragraph(f"Reporte de Muro de Contención - {plan.upper()}", styleH2))
        elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styleN))
        elements.append(Spacer(1, 20))
    except Exception as e:
        print(f"Error en título: {e}")
        elements.append(Paragraph("CONSORCIO DEJ - Reporte de Muro de Contención", styleN))
    
    if plan == "premium":
        # Reporte premium completo
        elements.append(Paragraph("1. DATOS DE ENTRADA", styleH))
        datos_tabla = [
            ["Parámetro", "Valor", "Unidad"],
            ["Altura del talud (h1)", f"{datos_entrada['h1']:.2f}", "m"],
            ["Densidad del relleno", f"{datos_entrada['gamma_relleno']}", "kg/m³"],
            ["Ángulo de fricción del relleno", f"{datos_entrada['phi_relleno']}", "°"],
            ["Profundidad de desplante (Df)", f"{datos_entrada['Df']:.2f}", "m"],
            ["Sobrecarga (qsc)", f"{datos_entrada['qsc']}", "kg/m²"],
            ["Resistencia del concreto (fc)", f"{datos_entrada['fc']}", "kg/cm²"],
            ["Resistencia del acero (fy)", f"{datos_entrada['fy']}", "kg/cm²"]
        ]
        
        tabla = Table(datos_tabla, colWidths=[200, 100, 80])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(tabla)
        elements.append(Spacer(1, 20))
        
        # Dimensiones calculadas
        elements.append(Paragraph("2. DIMENSIONES CALCULADAS", styleH))
        dim_tabla = [
            ["Dimensión", "Valor", "Unidad"],
            ["Ancho de zapata (Bz)", f"{resultados['Bz']:.2f}", "m"],
            ["Peralte de zapata (hz)", f"{resultados['hz']:.2f}", "m"],
            ["Espesor del muro (b)", f"{resultados['b']:.2f}", "m"],
            ["Longitud de puntera (r)", f"{resultados['r']:.2f}", "m"],
            ["Longitud de talón (t)", f"{resultados['t']:.2f}", "m"],
            ["Altura de coronación (hm)", f"{resultados['hm']:.2f}", "m"]
        ]
        
        tabla_dim = Table(dim_tabla, colWidths=[200, 100, 80])
        tabla_dim.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(tabla_dim)
        elements.append(Spacer(1, 20))
        
        # Diseño del fuste
        elements.append(Paragraph("3. DISEÑO Y VERIFICACIÓN DEL FUSTE", styleH))
        fuste_tabla = [
            ["Parámetro", "Valor", "Unidad"],
            ["Coeficiente pasivo (kp)", f"{diseno_fuste['kp']:.2f}", ""],
            ["Empuje pasivo", f"{diseno_fuste['Ep_kg_m']:.0f}", "kg/m"],
            ["Factor de seguridad volcamiento", f"{diseno_fuste['FSv']:.2f}", ""],
            ["Factor de seguridad deslizamiento", f"{diseno_fuste['FSd']:.2f}", ""],
            ["Peralte efectivo requerido", f"{diseno_fuste['dreq']:.2f}", "cm"],
            ["Peralte efectivo real", f"{diseno_fuste['dreal']:.2f}", "cm"],
            ["Área de acero requerida", f"{diseno_fuste['As']:.2f}", "cm²"],
            ["Área de acero mínima", f"{diseno_fuste['Asmin']:.2f}", "cm²"],
            ["Número de barras 5/8\"", f"{diseno_fuste['num_barras']}", ""],
            ["Separación entre barras", f"{diseno_fuste['separacion']:.1f}", "cm"]
        ]
        
        tabla_fuste = Table(fuste_tabla, colWidths=[200, 100, 80])
        tabla_fuste.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(tabla_fuste)
        elements.append(Spacer(1, 20))
        
        # Verificaciones de estabilidad
        elements.append(Paragraph("4. VERIFICACIONES DE ESTABILIDAD", styleH))
        verificaciones = []
        
        if diseno_fuste['FSv'] >= 2.0:
            verificaciones.append(["Volcamiento", "CUMPLE", f"FS = {diseno_fuste['FSv']:.2f} ≥ 2.0"])
        else:
            verificaciones.append(["Volcamiento", "NO CUMPLE", f"FS = {diseno_fuste['FSv']:.2f} < 2.0"])
            
        if diseno_fuste['FSd'] >= 1.5:
            verificaciones.append(["Deslizamiento", "CUMPLE", f"FS = {diseno_fuste['FSd']:.2f} ≥ 1.5"])
        else:
            verificaciones.append(["Deslizamiento", "NO CUMPLE", f"FS = {diseno_fuste['FSd']:.2f} < 1.5"])
            
        if diseno_fuste['dreal'] >= diseno_fuste['dreq']:
            verificaciones.append(["Peralte efectivo", "CUMPLE", f"dreal = {diseno_fuste['dreal']:.2f} ≥ {diseno_fuste['dreq']:.2f}"])
        else:
            verificaciones.append(["Peralte efectivo", "NO CUMPLE", f"dreal = {diseno_fuste['dreal']:.2f} < {diseno_fuste['dreq']:.2f}"])
            
        if diseno_fuste['As_proporcionado'] >= diseno_fuste['As']:
            verificaciones.append(["Área de acero", "CUMPLE", f"As = {diseno_fuste['As_proporcionado']:.2f} ≥ {diseno_fuste['As']:.2f}"])
        else:
            verificaciones.append(["Área de acero", "NO CUMPLE", f"As = {diseno_fuste['As_proporcionado']:.2f} < {diseno_fuste['As']:.2f}"])
        
        verif_tabla = [["Verificación", "Estado", "Detalle"]] + verificaciones
        tabla_verif = Table(verif_tabla, colWidths=[150, 100, 150])
        tabla_verif.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightcoral),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(tabla_verif)
        
    else:
        # Reporte básico
        elements.append(Paragraph("RESULTADOS BÁSICOS", styleH))
        elements.append(Paragraph(f"Peso del muro: {resultados.get('peso_muro', 0):.2f} kN", styleN))
        elements.append(Paragraph(f"Empuje del suelo: {resultados.get('empuje_suelo', 0):.2f} kN", styleN))
        elements.append(Paragraph(f"Factor de seguridad: {resultados.get('fs_volcamiento', 0):.2f}", styleN))
        elements.append(Paragraph("Este es un reporte básico del plan gratuito.", styleN))
    
    # Construir PDF
    doc.build(elements)
    pdf_buffer.seek(0)
    return pdf_buffer

# Función para dibujar el muro de contención
def dibujar_muro_streamlit(dimensiones, h1, Df, qsc):
    """
    Dibuja el muro de contención con las dimensiones calculadas para Streamlit.
    
    Parámetros:
    -----------
    dimensiones : dict
        Diccionario con las dimensiones calculadas del muro
    h1 : float
        Altura del talud (m)
    Df : float
        Profundidad de desplante (m)
    qsc : float
        Sobrecarga (kg/m²)
    
    Retorna:
    --------
    matplotlib.figure.Figure
        Figura con el dibujo del muro
    """
    # Configurar estilo profesional
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Extraer dimensiones
    Bz = dimensiones['Bz']
    hz = dimensiones['hz']
    b = dimensiones['b']
    r = dimensiones['r']
    t = dimensiones['t']
    hm = dimensiones['hm']
    
    # Colores profesionales mejorados
    color_zapata = '#4FC3F7'  # Azul claro profesional
    color_muro = '#FF5722'    # Naranja vibrante
    color_relleno = '#FFC107' # Amarillo dorado
    color_suelo = '#8D6E63'   # Marrón tierra
    color_agua = '#81C784'    # Verde agua
    color_acero = '#607D8B'   # Gris acero
    
    # Dibujar suelo de cimentación con gradiente
    suelo_gradient = np.linspace(0.3, 0.8, 50)
    for i, alpha in enumerate(suelo_gradient):
        y_pos = -Df + (i * Df / 50)
        ax.add_patch(Rectangle((-1, y_pos), Bz+2, Df/50, 
                              facecolor=color_suelo, edgecolor='none', alpha=alpha))
    
    # Dibujar zapata con efecto 3D
    ax.add_patch(Rectangle((0, 0), Bz, hz, facecolor=color_zapata, 
                          edgecolor='#1565C0', linewidth=3))
    
    # Dibujar muro principal con gradiente
    for i in range(10):
        alpha = 0.7 + (i * 0.03)
        ax.add_patch(Rectangle((r, hz + i*h1/10), b, h1/10, 
                              facecolor=color_muro, edgecolor='#D84315', 
                              linewidth=1, alpha=alpha))
    
    # Dibujar parte superior del muro
    ax.add_patch(Rectangle((r, hz + h1), b, hm, facecolor=color_muro, 
                          edgecolor='#D84315', linewidth=3))
    
    # Dibujar relleno con patrón
    relleno_pts = [(r+b, hz), (Bz, hz), (Bz, hz+h1+hm), (r+b, hz+h1+hm)]
    ax.add_patch(Polygon(relleno_pts, facecolor=color_relleno, 
                        edgecolor='#F57F17', linewidth=2, alpha=0.8))
    
    # Agregar patrón de relleno (puntos)
    for i in range(20):
        x = r + b + (i * t / 20) + np.random.normal(0, 0.02)
        y = hz + np.random.uniform(0, h1+hm)
        if x < Bz and y < hz+h1+hm:
            ax.scatter(x, y, c='#F57F17', s=15, alpha=0.6)
    
    # Dibujar sobrecarga con flechas mejoradas y profesionales
    flechas_x = np.linspace(r+b+0.1, Bz-0.1, 15)
    for i, x in enumerate(flechas_x):
        color_flecha = '#D32F2F' if i % 3 == 0 else '#F44336' if i % 3 == 1 else '#E53935'
        ax.arrow(x, hz+h1+hm+0.7, 0, -0.5, head_width=0.1, head_length=0.2, 
                fc=color_flecha, ec=color_flecha, linewidth=4, alpha=0.9)
    
    # Texto de sobrecarga con fondo profesional (más pequeño)
    ax.text(Bz/2, hz+h1+hm+0.8, f'SOBRECARGA: {qsc} kg/m²', 
            ha='center', fontsize=10, fontweight='bold', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#FFEBEE', 
                     edgecolor='#D32F2F', linewidth=2, alpha=0.9))
    
    # Agregar línea de nivel del terreno
    ax.axhline(y=hz, color='#795548', linewidth=2, linestyle='-', alpha=0.8)
    ax.text(Bz+0.2, hz, 'NIVEL TERRENO', fontsize=8, fontweight='bold', 
            color='#795548', rotation=90, va='center')
    
    # Añadir dimensiones con estilo profesional (más pequeñas)
    dimension_style = dict(arrowstyle='<->', color='#1976D2', linewidth=2)
    
    # Dimensiones horizontales
    ax.annotate('', xy=(0, hz/2), xytext=(r, hz/2), arrowprops=dimension_style)
    ax.text(r/2, hz/2-0.1, f'r={r}m', ha='center', fontsize=8, fontweight='bold', 
            color='#1976D2', bbox=dict(boxstyle="round,pad=0.1", facecolor='white', 
                                      edgecolor='#1976D2', alpha=0.8))
    
    ax.annotate('', xy=(r, hz/2), xytext=(r+b, hz/2), arrowprops=dimension_style)
    ax.text(r+b/2, hz/2-0.1, f'b={b}m', ha='center', fontsize=8, fontweight='bold', 
            color='#1976D2', bbox=dict(boxstyle="round,pad=0.1", facecolor='white', 
                                      edgecolor='#1976D2', alpha=0.8))
    
    ax.annotate('', xy=(r+b, hz/2), xytext=(Bz, hz/2), arrowprops=dimension_style)
    ax.text(r+b+t/2, hz/2-0.1, f't={t}m', ha='center', fontsize=8, fontweight='bold', 
            color='#1976D2', bbox=dict(boxstyle="round,pad=0.1", facecolor='white', 
                                      edgecolor='#1976D2', alpha=0.8))
    
    # Dimensiones verticales
    ax.annotate('', xy=(r+b/2, hz), xytext=(r+b/2, hz+h1), arrowprops=dimension_style)
    ax.text(r+b/2-0.15, hz+h1/2, f'h1={h1}m', ha='right', fontsize=8, fontweight='bold', 
            color='#1976D2', bbox=dict(boxstyle="round,pad=0.1", facecolor='white', 
                                      edgecolor='#1976D2', alpha=0.8))
    
    ax.annotate('', xy=(r+b/2, hz+h1), xytext=(r+b/2, hz+h1+hm), arrowprops=dimension_style)
    ax.text(r+b/2-0.15, hz+h1+hm/2, f'hm={hm}m', ha='right', fontsize=8, fontweight='bold', 
            color='#1976D2', bbox=dict(boxstyle="round,pad=0.1", facecolor='white', 
                                      edgecolor='#1976D2', alpha=0.8))
    
    ax.annotate('', xy=(r+b/2, 0), xytext=(r+b/2, -Df), arrowprops=dimension_style)
    ax.text(r+b/2-0.15, -Df/2, f'Df={Df}m', ha='right', fontsize=8, fontweight='bold', 
            color='#1976D2', bbox=dict(boxstyle="round,pad=0.1", facecolor='white', 
                                      edgecolor='#1976D2', alpha=0.8))
    
    ax.annotate('', xy=(0, 0), xytext=(0, hz), arrowprops=dimension_style)
    ax.text(-0.15, hz/2, f'hz={hz}m', ha='right', fontsize=8, fontweight='bold', 
            color='#1976D2', bbox=dict(boxstyle="round,pad=0.1", facecolor='white', 
                                      edgecolor='#1976D2', alpha=0.8))
    
    ax.annotate('', xy=(0, 0), xytext=(Bz, 0), arrowprops=dimension_style)
    ax.text(Bz/2, -0.2, f'Bz={Bz}m', ha='center', fontsize=8, fontweight='bold', 
            color='#1976D2', bbox=dict(boxstyle="round,pad=0.1", facecolor='white', 
                                      edgecolor='#1976D2', alpha=0.8))
    
    # Ajustar límites del gráfico para mejor visualización
    ax.set_xlim(-1.0, Bz+1.0)
    ax.set_ylim(-Df-0.5, hz+h1+hm+1.0)
    
    # Configurar aspecto y títulos profesionales
    ax.set_aspect('equal')
    ax.set_title('DISEÑO PROFESIONAL DE MURO DE CONTENCIÓN\nCONSORCIO DEJ - Ingeniería y Construcción', 
                fontsize=16, fontweight='bold', pad=20, color='#1565C0')
    ax.set_xlabel('Distancia (metros)', fontsize=12, fontweight='bold', color='#424242')
    ax.set_ylabel('Altura (metros)', fontsize=12, fontweight='bold', color='#424242')
    
    # Agregar leyenda profesional (más pequeña y posicionada para no obstruir)
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=color_zapata, edgecolor='#1565C0', label='ZAPATA'),
        Patch(facecolor=color_muro, edgecolor='#D84315', label='MURO'),
        Patch(facecolor=color_relleno, edgecolor='#F57F17', label='RELLENO'),
        Patch(facecolor=color_suelo, edgecolor='#5D4037', label='SUELO')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=8, 
             frameon=True, fancybox=True, shadow=True, 
             title='ELEMENTOS', title_fontsize=9, bbox_to_anchor=(0.02, 0.98))
    
    # Agregar grid sutil
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    
    # Configurar fondo
    ax.set_facecolor('#FAFAFA')
    fig.patch.set_facecolor('white')
    
    plt.tight_layout()
    return fig

# Configuración de la página
st.set_page_config(
    page_title="CONSORCIO DEJ - Muros de Contención",
    page_icon="🏗️",
    layout="wide"
)

# Header con fondo amarillo
st.markdown("""
<div style="text-align: center; padding: 20px; background-color: #FFD700; color: #2F2F2F; border-radius: 10px; margin-bottom: 20px; border: 2px solid #FFA500;">
    <h1>🏗️ CONSORCIO DEJ</h1>
    <p style="font-size: 18px; font-weight: bold;">Ingeniería y Construcción</p>
    <p style="font-size: 14px;">Diseño y Análisis de Muros de Contención</p>
</div>
""", unsafe_allow_html=True)

# Sistema de autenticación y pagos
def show_pricing_page():
    """Mostrar página de precios y planes"""
    st.title("💰 Planes y Precios - CONSORCIO DEJ")
    
    # Verificar si es administrador
    is_admin = st.session_state.get('user') == 'admin'
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🆓 Plan Gratuito")
        st.write("**$0/mes**")
        st.write("✅ Cálculos básicos")
        st.write("✅ Análisis simple")
        st.write("✅ Reportes básicos")
        st.write("❌ Sin análisis completo")
        st.write("❌ Sin diseño del fuste")
        st.write("❌ Sin gráficos avanzados")
        
        if st.button("Seleccionar Gratuito", key="free_plan"):
            if is_admin:
                st.session_state['plan'] = "gratuito"
                if 'user_data' in st.session_state:
                    st.session_state['user_data']['plan'] = "gratuito"
                st.success("✅ Plan gratuito activado para administrador")
                st.rerun()
            else:
                st.info("Ya tienes acceso al plan gratuito")
    
    with col2:
        st.subheader("⭐ Plan Premium")
        st.write("**$29.99/mes**")
        st.write("✅ Todo del plan gratuito")
        st.write("✅ Análisis completo")
        st.write("✅ Diseño del fuste")
        st.write("✅ Gráficos avanzados")
        st.write("✅ Reportes PDF")
        st.write("❌ Sin soporte empresarial")
        
        if st.button("Actualizar a Premium", key="premium_plan"):
            if is_admin:
                # Acceso directo para administrador
                st.session_state['plan'] = "premium"
                if 'user_data' in st.session_state:
                    st.session_state['user_data']['plan'] = "premium"
                st.success("✅ Plan Premium activado para administrador")
                st.rerun()
            elif PAYMENT_SYSTEM_AVAILABLE:
                show_payment_form("premium")
            else:
                st.info("Sistema de pagos no disponible en modo demo")
    
    with col3:
        st.subheader("🏢 Plan Empresarial")
        st.write("**$99.99/mes**")
        st.write("✅ Todo del plan premium")
        st.write("✅ Soporte prioritario")
        st.write("✅ Múltiples proyectos")
        st.write("✅ Reportes personalizados")
        st.write("✅ Capacitación incluida")
        st.write("✅ API de integración")
        
        if st.button("Actualizar a Empresarial", key="business_plan"):
            if is_admin:
                # Acceso directo para administrador
                st.session_state['plan'] = "empresarial"
                if 'user_data' in st.session_state:
                    st.session_state['user_data']['plan'] = "empresarial"
                st.success("✅ Plan Empresarial activado para administrador")
                st.rerun()
            elif PAYMENT_SYSTEM_AVAILABLE:
                show_payment_form("empresarial")
            else:
                st.info("Sistema de pagos no disponible en modo demo")
    
    # Panel especial para administrador
    if is_admin:
        st.markdown("---")
        st.subheader("👨‍💼 Panel de Administrador")
        st.info("Como administrador, puedes cambiar tu plan directamente sin pasar por el sistema de pagos.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🆓 Activar Plan Gratuito", key="admin_free"):
                st.session_state['plan'] = "gratuito"
                if 'user_data' in st.session_state:
                    st.session_state['user_data']['plan'] = "gratuito"
                st.success("✅ Plan gratuito activado")
                st.rerun()
        
        with col2:
            if st.button("⭐ Activar Plan Premium", key="admin_premium"):
                st.session_state['plan'] = "premium"
                if 'user_data' in st.session_state:
                    st.session_state['user_data']['plan'] = "premium"
                st.success("✅ Plan premium activado")
                st.rerun()
        
        with col3:
            if st.button("🏢 Activar Plan Empresarial", key="admin_enterprise"):
                st.session_state['plan'] = "empresarial"
                if 'user_data' in st.session_state:
                    st.session_state['user_data']['plan'] = "empresarial"
                st.success("✅ Plan empresarial activado")
                st.rerun()

def show_payment_form(plan):
    """Mostrar formulario de pago"""
    st.subheader(f"💳 Pago - Plan {plan.title()}")
    
    # Verificar si hay usuario logueado
    if 'user' not in st.session_state:
        st.warning("⚠️ Debes iniciar sesión o registrarte primero")
        st.info("📝 Ve a la pestaña 'Registrarse' para crear una cuenta")
        return
    
    payment_method = st.selectbox(
        "Método de pago",
        ["yape", "plin", "paypal", "transferencia", "efectivo"],
        format_func=lambda x: {
            "yape": "📱 Yape (Más Rápido)",
            "plin": "📱 PLIN",
            "paypal": "💳 PayPal",
            "transferencia": "🏦 Transferencia Bancaria", 
            "efectivo": "💵 Pago en Efectivo"
        }[x]
    )
    
    if st.button("Procesar Pago", type="primary"):
        if PAYMENT_SYSTEM_AVAILABLE:
            try:
                result = payment_system.upgrade_plan(
                    st.session_state['user'], 
                    plan, 
                    payment_method
                )
                
                if result["success"]:
                    # Verificar si es acceso directo de admin
                    if result.get("admin_access"):
                        st.success("✅ " + result["message"])
                        st.info("🎉 Acceso completo activado para administrador")
                        
                        # Actualizar plan en session state
                        st.session_state['plan'] = plan
                        if 'user_data' in st.session_state:
                            st.session_state['user_data']['plan'] = plan
                        
                        # Botón para continuar
                        if st.button("🚀 Continuar con Acceso Completo", key="continue_full_access"):
                            st.rerun()
                    else:
                        st.success("✅ Pago procesado correctamente")
                        st.info("📋 Instrucciones de pago:")
                        st.text(result["instructions"])
                        
                        # Mostrar información adicional
                        st.info("📱 Envía el comprobante de pago a WhatsApp: +51 999 888 777")
                        
                        # Verificar si fue confirmado automáticamente
                        if result.get("auto_confirmed"):
                            st.success("🎉 ¡Plan activado inmediatamente!")
                            st.info("✅ Pago confirmado automáticamente")
                            
                            # Actualizar plan en session state
                            st.session_state['plan'] = plan
                            if 'user_data' in st.session_state:
                                st.session_state['user_data']['plan'] = plan
                            
                            # Botón para continuar con acceso completo
                            if st.button("🚀 Continuar con Acceso Completo", key="continue_full_access"):
                                st.rerun()
                        else:
                            st.info("⏰ Activación en 2 horas máximo")
                            st.info("🔄 Recarga la página después de 2 horas")
                else:
                    st.error(f"❌ Error: {result['message']}")
            except Exception as e:
                st.error(f"❌ Error en el sistema de pagos: {str(e)}")
                st.info("🔄 Intenta nuevamente o contacta soporte")
        else:
            st.error("❌ Sistema de pagos no disponible")
            st.info("🔧 Contacta al administrador para activar el sistema")

def show_auth_page():
    st.title("🏗️ CONSORCIO DEJ - Muros de Contención")
    
    # Pestañas para login/registro
    tab1, tab2, tab3 = st.tabs(["🔐 Iniciar Sesión", "📝 Registrarse", "💰 Planes y Precios"])
    
    with tab1:
        st.subheader("Iniciar Sesión")
        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Entrar")
            
            if submitted:
                # Verificar credenciales especiales primero
                if username == "admin" and password == "admin123":
                    st.session_state['logged_in'] = True
                    st.session_state['user_data'] = {"username": "admin", "plan": "empresarial", "name": "Administrador"}
                    st.session_state['user'] = "admin"
                    st.session_state['plan'] = "empresarial"
                    st.success("¡Bienvenido Administrador!")
                    st.rerun()
                elif username == "demo" and password == "demo":
                    st.session_state['logged_in'] = True
                    st.session_state['user_data'] = {"username": "demo", "plan": "gratuito", "name": "Usuario Demo"}
                    st.session_state['user'] = "demo"
                    st.session_state['plan'] = "gratuito"
                    st.success("¡Bienvenido al modo demo!")
                    st.rerun()
                elif not PAYMENT_SYSTEM_AVAILABLE:
                    st.error("Credenciales disponibles: admin/admin123 o demo/demo")
                else:
                    # Sistema real
                    result = payment_system.login_user(username, password)
                    if result["success"]:
                        st.session_state['logged_in'] = True
                        st.session_state['user_data'] = result["user"]
                        st.session_state['user'] = result["user"]["email"]
                        st.session_state['plan'] = result["user"]["plan"]
                        st.success(f"¡Bienvenido, {result['user']['name']}!")
                        st.rerun()
                    else:
                        st.error(result["message"])
    
    with tab2:
        st.subheader("Crear Cuenta")
        with st.form("register_form"):
            new_username = st.text_input("Usuario", placeholder="Tu nombre de usuario")
            new_email = st.text_input("Email", placeholder="tuemail@gmail.com")
            new_password = st.text_input("Contraseña", type="password", placeholder="Mínimo 6 caracteres")
            confirm_password = st.text_input("Confirmar Contraseña", type="password")
            submitted = st.form_submit_button("📝 Registrarse", type="primary")
            
            if submitted:
                if not new_username or not new_email or not new_password:
                    st.error("❌ Todos los campos son obligatorios")
                elif new_password != confirm_password:
                    st.error("❌ Las contraseñas no coinciden")
                elif len(new_password) < 6:
                    st.error("❌ La contraseña debe tener al menos 6 caracteres")
                else:
                    if not PAYMENT_SYSTEM_AVAILABLE:
                        st.success("✅ Modo demo: Registro simulado exitoso")
                        st.info("🔑 Credenciales: demo / demo")
                    else:
                        result = payment_system.register_user(new_email, new_password, new_username)
                        if result["success"]:
                            st.success("✅ " + result["message"])
                            st.info("🔐 Ahora puedes iniciar sesión y actualizar tu plan")
                            
                            # Auto-login después del registro
                            login_result = payment_system.login_user(new_email, new_password)
                            if login_result["success"]:
                                st.session_state['logged_in'] = True
                                st.session_state['user_data'] = login_result["user"]
                                st.session_state['user'] = login_result["user"]["email"]
                                st.session_state['plan'] = login_result["user"]["plan"]
                                st.success(f"🎉 ¡Bienvenido, {login_result['user']['name']}!")
                                st.info("💰 Ve a 'Planes y Precios' para actualizar tu plan")
                                st.rerun()
                        else:
                            st.error("❌ " + result["message"])
    
    with tab3:
        show_pricing_page()

# Verificar estado de autenticación
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Función para actualizar plan del usuario
def update_user_plan():
    """Actualizar plan del usuario desde el sistema de pagos"""
    if PAYMENT_SYSTEM_AVAILABLE and 'user' in st.session_state:
        try:
            user_email = st.session_state['user']
            if user_email and user_email not in ['admin', 'demo']:
                real_plan = payment_system.get_user_plan(user_email)
                current_plan = real_plan.get('plan', 'gratuito')
                
                # Actualizar session state si el plan cambió
                if st.session_state.get('plan') != current_plan:
                    st.session_state['plan'] = current_plan
                    if 'user_data' in st.session_state:
                        st.session_state['user_data']['plan'] = current_plan
                    return True
        except Exception as e:
            pass
    return False

if not st.session_state['logged_in']:
    show_auth_page()
else:
    # Actualizar plan del usuario automáticamente
    plan_updated = update_user_plan()
    if plan_updated:
        st.success("🎉 ¡Tu plan ha sido actualizado!")
        st.rerun()
    # Mostrar información del usuario
    user_data = st.session_state.get('user_data', {})
    plan = user_data.get('plan', 'gratuito')
    
    # Header con información del plan
    if plan == "gratuito":
        st.sidebar.info("🆓 Plan Gratuito")
    elif plan == "premium":
        st.sidebar.success("⭐ Plan Premium")
    else:
        st.sidebar.success("🏢 Plan Empresarial")
    
    st.sidebar.write(f"Usuario: {st.session_state['user']}")
    st.sidebar.write(f"Plan: {plan}")
    
    # Botón para cerrar sesión
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state['logged_in'] = False
        st.session_state['user_data'] = None
        st.session_state['user'] = None
        st.session_state['plan'] = None
        st.rerun()
    
    # Panel especial para administrador
    is_admin = st.session_state.get('user') == 'admin'
    if is_admin:
        st.sidebar.markdown("---")
        st.sidebar.subheader("👨‍💼 Panel de Administrador")
        st.sidebar.info("Acceso directo a todos los planes")
        
        col1, col2, col3 = st.sidebar.columns(3)
        with col1:
            if st.button("🆓 Gratuito", key="sidebar_free"):
                st.session_state['plan'] = "gratuito"
                if 'user_data' in st.session_state:
                    st.session_state['user_data']['plan'] = "gratuito"
                st.success("✅ Plan gratuito activado")
                st.rerun()
        
        with col2:
            if st.button("⭐ Premium", key="sidebar_premium"):
                st.session_state['plan'] = "premium"
                if 'user_data' in st.session_state:
                    st.session_state['user_data']['plan'] = "premium"
                st.success("✅ Plan premium activado")
                st.rerun()
        
        with col3:
            if st.button("🏢 Empresarial", key="sidebar_enterprise"):
                st.session_state['plan'] = "empresarial"
                if 'user_data' in st.session_state:
                    st.session_state['user_data']['plan'] = "empresarial"
                st.success("✅ Plan empresarial activado")
                st.rerun()
    
    # Mostrar página de precios si se solicita
    if st.session_state.get('show_pricing', False):
        show_pricing_page()
        
        # Botón para volver
        if st.button("← Volver a la aplicación"):
            st.session_state['show_pricing'] = False
            st.rerun()
    else:
        # Sidebar para navegación
        st.sidebar.title("📋 Menú Principal")
    
    # Mostrar plan actual
    if st.session_state['plan'] == "gratuito":
        st.sidebar.info("🆓 Plan Gratuito")
    else:
        st.sidebar.success("⭐ Plan Premium")
    
    opcion = st.sidebar.selectbox("Selecciona una opción", 
                                 ["🏗️ Cálculo Básico", "📊 Análisis Completo", "🏗️ Diseño del Fuste", "📄 Generar Reporte", "📈 Gráficos", "ℹ️ Acerca de", "✉️ Contacto"])

    if opcion == "🏗️ Cálculo Básico":
        st.title("Cálculo Básico de Muro de Contención")
        st.info("Plan gratuito: Cálculos básicos de estabilidad")
        
        # Pestañas para diferentes tipos de cálculos
        tab1, tab2, tab3 = st.tabs(["📏 Dimensiones", "🏗️ Materiales", "⚖️ Cargas"])
        
        with tab1:
            st.subheader("Dimensiones del Muro")
            col1, col2 = st.columns(2)
            with col1:
                altura = st.number_input("Altura del muro (m)", min_value=1.0, max_value=15.0, value=3.0, step=0.1)
                base = st.number_input("Base del muro (m)", min_value=0.5, max_value=8.0, value=1.0, step=0.1)
            with col2:
                espesor = st.number_input("Espesor del muro (m)", min_value=0.2, max_value=2.0, value=0.3, step=0.05)
                longitud = st.number_input("Longitud del muro (m)", min_value=1.0, max_value=100.0, value=10.0, step=0.5)
        
        with tab2:
            st.subheader("Propiedades de los Materiales")
            col1, col2 = st.columns(2)
            with col1:
                peso_especifico = st.number_input("Peso específico del hormigón (kN/m³)", min_value=20.0, max_value=30.0, value=24.0, step=0.5)
                resistencia_concreto = st.number_input("Resistencia del hormigón (MPa)", min_value=15.0, max_value=50.0, value=25.0, step=1.0)
            with col2:
                peso_suelo = st.number_input("Peso específico del suelo (kN/m³)", min_value=15.0, max_value=22.0, value=18.0, step=0.5)
                angulo_friccion = st.number_input("Ángulo de fricción del suelo (°)", min_value=20.0, max_value=45.0, value=30.0, step=1.0)
        
        with tab3:
            st.subheader("Cargas y Factores de Seguridad")
            col1, col2 = st.columns(2)
            with col1:
                sobrecarga = st.number_input("Sobrecarga (kN/m²)", min_value=0.0, max_value=50.0, value=10.0, step=1.0)
                factor_seguridad = st.number_input("Factor de seguridad", min_value=1.2, max_value=3.0, value=1.5, step=0.1)
            with col2:
                sismo = st.checkbox("Considerar sismo")
                viento = st.checkbox("Considerar viento")
        
        # Botón para calcular
        if st.button("🚀 Calcular Muro de Contención", type="primary"):
            # Cálculos básicos
            volumen = altura * base * espesor * longitud
            peso_muro = volumen * peso_especifico
            
            # Cálculo del empuje del suelo
            angulo_rad = math.radians(angulo_friccion)
            ka = math.tan(math.radians(45 - angulo_friccion/2))**2  # Coeficiente de empuje activo
            empuje_suelo = 0.5 * peso_suelo * altura**2 * ka * longitud
            
            # Cálculo del momento volcador
            momento_volcador = empuje_suelo * altura / 3
            
            # Cálculo del momento estabilizador
            momento_estabilizador = peso_muro * base / 2
            
            # Factor de seguridad al volcamiento
            fs_volcamiento = momento_estabilizador / momento_volcador
            
            # Guardar resultados en session state
            st.session_state['resultados_basicos'] = {
                'altura': altura,
                'base': base,
                'espesor': espesor,
                'longitud': longitud,
                'peso_muro': peso_muro,
                'empuje_suelo': empuje_suelo,
                'fs_volcamiento': fs_volcamiento,
                'volumen': volumen,
                'ka': ka,
                'momento_volcador': momento_volcador,
                'momento_estabilizador': momento_estabilizador
            }
            
            st.success("¡Cálculos básicos completados exitosamente!")
            st.balloons()
            
            # MOSTRAR RESULTADOS INMEDIATAMENTE DESPUÉS DEL CÁLCULO
            st.subheader("📊 Resultados del Cálculo Básico")
            
            # Mostrar resultados en columnas
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Peso del Muro", f"{peso_muro:.2f} kN")
                st.metric("Empuje del Suelo", f"{empuje_suelo:.2f} kN")
                st.metric("Volumen", f"{volumen:.2f} m³")
                st.metric("Coeficiente Ka", f"{ka:.3f}")
            
            with col2:
                st.metric("Factor de Seguridad", f"{fs_volcamiento:.2f}")
                st.metric("Momento Volcador", f"{momento_volcador:.2f} kN·m")
                st.metric("Momento Estabilizador", f"{momento_estabilizador:.2f} kN·m")
                st.metric("Altura", f"{altura:.1f} m")
            
            # Análisis de estabilidad
            st.subheader("🔍 Análisis de Estabilidad")
            if fs_volcamiento > 1.5:
                st.success(f"✅ El muro es estable al volcamiento (FS = {fs_volcamiento:.2f} > 1.5)")
            else:
                st.error(f"⚠️ El muro requiere revisión de estabilidad (FS = {fs_volcamiento:.2f} < 1.5)")
            
            # Gráfico básico
            st.subheader("📈 Gráfico de Fuerzas")
            datos = pd.DataFrame({
                'Fuerza': ['Peso Muro', 'Empuje Suelo'],
                'Valor (kN)': [peso_muro, empuje_suelo]
            })
            
            # Gráfico de barras mejorado
            if PLOTLY_AVAILABLE:
                fig = px.bar(datos, x='Fuerza', y='Valor (kN)', 
                            title="Comparación de Fuerzas - Plan Gratuito",
                            color='Fuerza',
                            color_discrete_map={'Peso Muro': '#2E8B57', 'Empuje Suelo': '#DC143C'})
                
                # Personalizar el gráfico
                fig.update_layout(
                    xaxis_title="Tipo de Fuerza",
                    yaxis_title="Valor (kN)",
                    showlegend=True,
                    height=400
                )
                
                # Agregar valores en las barras
                fig.update_traces(texttemplate='%{y:.1f}', textposition='outside')
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Gráfico alternativo con matplotlib
                fig, ax = plt.subplots(figsize=(10, 6))
                bars = ax.bar(datos['Fuerza'], datos['Valor (kN)'], 
                             color=['#2E8B57', '#DC143C'])
                ax.set_title("Comparación de Fuerzas - Plan Gratuito")
                ax.set_xlabel("Tipo de Fuerza")
                ax.set_ylabel("Valor (kN)")
                
                # Agregar valores en las barras
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{height:.1f}', ha='center', va='bottom')
                
                st.pyplot(fig)
            
            # Gráfico de momentos
            st.subheader("📊 Gráfico de Momentos")
            datos_momentos = pd.DataFrame({
                'Momento': ['Volcador', 'Estabilizador'],
                'Valor (kN·m)': [momento_volcador, momento_estabilizador]
            })
            
            if PLOTLY_AVAILABLE:
                fig2 = px.pie(datos_momentos, values='Valor (kN·m)', names='Momento',
                             title="Distribución de Momentos - Plan Gratuito",
                             color_discrete_map={'Volcador': '#FF6B6B', 'Estabilizador': '#4ECDC4'})
                
                fig2.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig2, use_container_width=True)
            else:
                # Gráfico alternativo con matplotlib
                fig2, ax2 = plt.subplots(figsize=(8, 8))
                ax2.pie(datos_momentos['Valor (kN·m)'], labels=datos_momentos['Momento'], 
                       autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4'])
                ax2.set_title("Distribución de Momentos - Plan Gratuito")
                st.pyplot(fig2)

    elif opcion == "📊 Análisis Completo":
        # Verificar acceso basado en plan del usuario
        user_plan = st.session_state.get('plan', 'gratuito')
        user_email = st.session_state.get('user', '')
        
        # Verificar si es admin (acceso completo)
        is_admin = user_email == 'admin' or user_email == 'admin@consorciodej.com'
        
        # Para usuarios normales, verificar plan real en el sistema de pagos
        if PAYMENT_SYSTEM_AVAILABLE and user_email and not is_admin:
            try:
                real_plan = payment_system.get_user_plan(user_email)
                current_plan = real_plan.get('plan', 'gratuito')
                
                # Actualizar session state si el plan cambió
                if st.session_state.get('plan') != current_plan:
                    st.session_state['plan'] = current_plan
                    if 'user_data' in st.session_state:
                        st.session_state['user_data']['plan'] = current_plan
                    user_plan = current_plan
            except Exception as e:
                # Si hay error, usar el plan de session state
                pass
        
        if user_plan == "gratuito" and not is_admin:
            st.warning("⚠️ Esta función requiere plan premium. Actualiza tu cuenta para acceder a análisis completos.")
            st.info("Plan gratuito incluye: Cálculos básicos, resultados simples")
            st.info("Plan premium incluye: Análisis completo, reportes detallados, gráficos avanzados")
            
            # Mostrar botón para actualizar plan
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("⭐ Actualizar a Premium", type="primary"):
                    st.session_state['show_pricing'] = True
                    st.rerun()
        else:
            st.title("Análisis Completo de Muro de Contención")
            st.success("⭐ Plan Premium: Análisis completo con teoría de Rankine")
            
            # Datos de entrada completos
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Dimensiones")
                h1 = st.number_input("Altura del talud (m)", value=2.8, step=0.1)
                Df = st.number_input("Profundidad de desplante (m)", value=1.2, step=0.1)
                hm = st.number_input("Altura de coronación (m)", value=1.2, step=0.1, help="Según TAREA_DE_PROGRAMACION2.py, altura recomendada para mejor estabilidad")
                
                st.subheader("Materiales")
                gamma_relleno = st.number_input("Densidad del relleno (kg/m³)", value=1800, step=50)
                phi_relleno = st.number_input("Ángulo de fricción del relleno (°)", value=30, step=1)
                gamma_concreto = st.number_input("Peso específico del concreto (kg/m³)", value=2400, step=50)
                
            with col2:
                st.subheader("Propiedades del Suelo")
                gamma_cimentacion = st.number_input("Densidad del suelo de cimentación (kg/m³)", value=1700, step=50)
                phi_cimentacion = st.number_input("Ángulo de fricción del suelo (°)", value=25, step=1)
                cohesion = st.number_input("Cohesión del suelo (t/m²)", value=1.0, step=0.1)
                sigma_adm = st.number_input("Capacidad portante del suelo (kg/cm²)", value=2.5, step=0.1)
                
                st.subheader("Cargas")
                qsc = st.number_input("Sobrecarga (kg/m²)", value=1000, step=100)
                fc = st.number_input("Resistencia del concreto (kg/cm²)", value=210, step=10)
                fy = st.number_input("Resistencia del acero (kg/cm²)", value=4200, step=100)
            
            if st.button("🔬 Ejecutar Análisis Completo", type="primary"):
                # Cálculos completos basados en TAREA_DE_PROGRAMACION2.py
                
                # Coeficiente de empuje activo (fórmula correcta de Rankine)
                phi_relleno_rad = math.radians(phi_relleno)
                ka = math.tan(math.radians(45 - phi_relleno/2))**2
                
                # Altura equivalente por sobrecarga
                hs = qsc / gamma_relleno
                
                # Factor kc para concreto
                kc = 14.28  # Para fc = 210 kg/cm²
                
                # Dimensiones calculadas
                Bz = (h1 + Df) * (1 + hs/(h1 + Df)) * math.sqrt(ka)
                Bz = round(Bz, 2)
                
                hz = math.sqrt(((h1 + Df)**2 * (1 + hs/(h1 + Df))) / (9 * kc))
                hz = round(hz * 100) / 100
                hz = max(0.4, hz)
                
                b = math.sqrt(((h1 + hm)**2 * (1 + hs/(h1 + hm))) / (10 * kc))
                b = round(b * 100) / 100
                b = max(0.35, b)
                
                r = (2 * Bz - 3 * b) / 6
                r = round(r * 100) / 100
                r = max(0.7, r)
                
                t = Bz - r - b
                t = round(t * 100) / 100
                
                # Cálculos de estabilidad completos (basados en AVANCE2.PY)
                
                # 1. Empujes activos
                Ea_relleno = 0.5 * ka * (gamma_relleno/1000) * h1**2
                Ea_sobrecarga = ka * (qsc/1000) * h1  # Convertir kg/m² a tn/m²
                Ea_total = Ea_relleno + Ea_sobrecarga
                
                # 2. Empuje pasivo (si aplica)
                phi_cimentacion_rad = math.radians(phi_cimentacion)
                kp = math.tan(math.radians(45 + phi_cimentacion/2))**2
                Ep = 0.5 * kp * (gamma_cimentacion/1000) * Df**2
                
                # 3. Pesos de cada elemento
                W_muro = b * h1 * (gamma_concreto/1000)
                W_zapata = Bz * hz * (gamma_concreto/1000)
                W_relleno = t * h1 * (gamma_relleno/1000)
                
                # 4. Posiciones de los pesos (brazos de momento)
                x_muro = r + b/2
                x_zapata = Bz/2
                x_relleno = r + b + t/2
                
                # 5. Momentos estabilizadores
                Mr_muro = W_muro * x_muro
                Mr_zapata = W_zapata * x_zapata
                Mr_relleno = W_relleno * x_relleno
                Mr_pasivo = Ep * Df/3
                M_estabilizador = Mr_muro + Mr_zapata + Mr_relleno + Mr_pasivo
                
                # 6. Momentos volcadores
                Mv_relleno = Ea_relleno * h1/3
                Mv_sobrecarga = Ea_sobrecarga * h1/2
                M_volcador = Mv_relleno + Mv_sobrecarga
                
                # 7. Factor de seguridad al volcamiento
                FS_volcamiento = M_estabilizador / M_volcador
                
                # 8. Verificación al deslizamiento
                mu = math.tan(phi_cimentacion_rad)  # Coeficiente de fricción
                Fr_friccion = mu * (W_muro + W_zapata + W_relleno)
                Fr_pasivo = Ep
                Fr_total = Fr_friccion + Fr_pasivo
                Fd_total = Ea_total
                FS_deslizamiento = Fr_total / Fd_total
                
                # 9. Verificación de presiones sobre el suelo
                W_total = W_muro + W_zapata + W_relleno
                
                # Posición de la resultante vertical
                sum_momentos_verticales = Mr_muro + Mr_zapata + Mr_relleno
                x_barra = sum_momentos_verticales / W_total
                
                # Excentricidad
                e = abs(x_barra - Bz/2)
                
                # Presiones máxima y mínima
                q_max = (W_total / Bz) * (1 + 6*e/Bz)
                q_min = (W_total / Bz) * (1 - 6*e/Bz)
                
                # Verificar si hay tensiones
                tension = q_min < 0
                
                # Convertir a kg/cm²
                q_max_kg_cm2 = q_max * 0.1  # tn/m² a kg/cm²
                q_min_kg_cm2 = q_min * 0.1
                
                # Crear diccionario con datos de entrada para el diseño del fuste
                datos_entrada = {
                    'h1': h1,
                    'gamma_relleno': gamma_relleno,
                    'phi_relleno': phi_relleno,
                    'gamma_cimentacion': gamma_cimentacion,
                    'phi_cimentacion': phi_cimentacion,
                    'cohesion': cohesion,
                    'Df': Df,
                    'sigma_adm': sigma_adm,
                    'gamma_concreto': gamma_concreto,
                    'fc': fc,
                    'fy': fy,
                    'qsc': qsc,
                    'hm': hm
                }
                
                # Calcular diseño del fuste
                resultados_completos = {
                    'ka': ka,
                    'kp': kp,
                    'hs': hs,
                    'Bz': Bz,
                    'hz': hz,
                    'b': b,
                    'r': r,
                    't': t,
                    'hm': hm,
                    'h1': h1,
                    'Df': Df,
                    'qsc': qsc,
                    'Ea_relleno': Ea_relleno,
                    'Ea_sobrecarga': Ea_sobrecarga,
                    'Ea_total': Ea_total,
                    'Ep': Ep,
                    'W_muro': W_muro,
                    'W_zapata': W_zapata,
                    'W_relleno': W_relleno,
                    'W_total': W_total,
                    'M_volcador': M_volcador,
                    'M_estabilizador': M_estabilizador,
                    'FS_volcamiento': FS_volcamiento,
                    'FS_deslizamiento': FS_deslizamiento,
                    'q_max_kg_cm2': q_max_kg_cm2,
                    'q_min_kg_cm2': q_min_kg_cm2,
                    'e': e,
                    'tension': tension
                }
                
                diseno_fuste = calcular_diseno_fuste(resultados_completos, datos_entrada)
                
                # Guardar resultados completos
                st.session_state['resultados_completos'] = {
                    'ka': ka,
                    'kp': kp,
                    'hs': hs,
                    'Bz': Bz,
                    'hz': hz,
                    'b': b,
                    'r': r,
                    't': t,
                    'hm': hm,
                    'h1': h1,
                    'Df': Df,
                    'qsc': qsc,
                    'Ea_relleno': Ea_relleno,
                    'Ea_sobrecarga': Ea_sobrecarga,
                    'Ea_total': Ea_total,
                    'Ep': Ep,
                    'W_muro': W_muro,
                    'W_zapata': W_zapata,
                    'W_relleno': W_relleno,
                    'W_total': W_total,
                    'M_volcador': M_volcador,
                    'M_estabilizador': M_estabilizador,
                    'FS_volcamiento': FS_volcamiento,
                    'FS_deslizamiento': FS_deslizamiento,
                    'q_max_kg_cm2': q_max_kg_cm2,
                    'q_min_kg_cm2': q_min_kg_cm2,
                    'e': e,
                    'tension': tension
                }
                
                # Guardar datos de entrada y diseño del fuste
                st.session_state['datos_entrada'] = datos_entrada
                st.session_state['diseno_fuste'] = diseno_fuste
                
                st.success("¡Análisis completo ejecutado exitosamente!")
                st.balloons()
                
                # MOSTRAR RESULTADOS COMPLETOS INMEDIATAMENTE
                st.subheader("📊 Resultados del Análisis Completo")
                
                # Mostrar resultados en columnas
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Coeficiente Ka", f"{ka:.3f}")
                    st.metric("Ancho de Zapata (Bz)", f"{Bz:.2f} m")
                    st.metric("Peralte de Zapata (hz)", f"{hz:.2f} m")
                    st.metric("Espesor del Muro (b)", f"{b:.2f} m")
                    st.metric("Longitud de Puntera (r)", f"{r:.2f} m")
                    st.metric("Longitud de Talón (t)", f"{t:.2f} m")
                
                with col2:
                    st.metric("Empuje Activo Total", f"{Ea_total:.2f} tn/m")
                    st.metric("Empuje Pasivo", f"{Ep:.2f} tn/m")
                    st.metric("Peso Total", f"{W_total:.2f} tn/m")
                    st.metric("FS Deslizamiento", f"{FS_deslizamiento:.2f}")
                    st.metric("Presión Máxima", f"{q_max_kg_cm2:.2f} kg/cm²")
                    st.metric("Excentricidad", f"{e:.3f} m")
                
                # Análisis de estabilidad completo
                st.subheader("🔍 Análisis de Estabilidad Completo")
                
                # Verificación al volcamiento
                col1, col2 = st.columns(2)
                with col1:
                    if FS_volcamiento >= 2.0:
                        st.success(f"✅ **Volcamiento:** CUMPLE (FS = {FS_volcamiento:.2f} ≥ 2.0)")
                    else:
                        st.error(f"⚠️ **Volcamiento:** NO CUMPLE (FS = {FS_volcamiento:.2f} < 2.0)")
                
                with col2:
                    if FS_deslizamiento >= 1.5:
                        st.success(f"✅ **Deslizamiento:** CUMPLE (FS = {FS_deslizamiento:.2f} ≥ 1.5)")
                    else:
                        st.error(f"⚠️ **Deslizamiento:** NO CUMPLE (FS = {FS_deslizamiento:.2f} < 1.5)")
                
                # Verificación de presiones
                st.subheader("📊 Verificación de Presiones sobre el Suelo")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Presión Máxima", f"{q_max_kg_cm2:.2f} kg/cm²")
                    if q_max_kg_cm2 <= sigma_adm:
                        st.success(f"✅ ≤ {sigma_adm} kg/cm²")
                    else:
                        st.error(f"⚠️ > {sigma_adm} kg/cm²")
                
                with col2:
                    st.metric("Presión Mínima", f"{q_min_kg_cm2:.2f} kg/cm²")
                    if not tension:
                        st.success("✅ Sin tensiones")
                    else:
                        st.error("⚠️ Hay tensiones")
                
                with col3:
                    st.metric("Excentricidad", f"{e:.3f} m")
                    e_limite = Bz / 6
                    if e <= e_limite:
                        st.success(f"✅ ≤ B/6 ({e_limite:.3f} m)")
                    else:
                        st.error(f"⚠️ > B/6 ({e_limite:.3f} m)")
                
                # Diseño del fuste
                st.subheader("🏗️ Diseño y Verificación del Fuste del Muro")
                st.info("Análisis estructural del fuste según PARTE 2.2.py")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Coeficiente Pasivo (kp)", f"{diseno_fuste['kp']:.2f}")
                    st.metric("Empuje Pasivo", f"{diseno_fuste['Ep_kg_m']:.0f} kg/m")
                    st.metric("Peralte Efectivo Req.", f"{diseno_fuste['dreq']:.2f} cm")
                    st.metric("Peralte Efectivo Real", f"{diseno_fuste['dreal']:.2f} cm")
                    st.metric("Área de Acero Req.", f"{diseno_fuste['As']:.2f} cm²")
                
                with col2:
                    st.metric("Área de Acero Mín.", f"{diseno_fuste['Asmin']:.2f} cm²")
                    st.metric("Número de Barras 5/8\"", f"{diseno_fuste['num_barras']}")
                    st.metric("Separación Barras", f"{diseno_fuste['separacion']:.1f} cm")
                    st.metric("Acero Retracción", f"{diseno_fuste['As_retraccion']:.2f} cm²")
                    st.metric("Barras Retracción 1/2\"", f"{diseno_fuste['num_barras_retraccion']}")
                
                # Verificaciones del fuste
                st.subheader("🔍 Verificaciones del Fuste")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if diseno_fuste['dreal'] >= diseno_fuste['dreq']:
                        st.success(f"✅ **Peralte:** CUMPLE (dreal = {diseno_fuste['dreal']:.2f} ≥ {diseno_fuste['dreq']:.2f} cm)")
                    else:
                        st.error(f"⚠️ **Peralte:** NO CUMPLE (dreal = {diseno_fuste['dreal']:.2f} < {diseno_fuste['dreq']:.2f} cm)")
                
                with col2:
                    if diseno_fuste['As_proporcionado'] >= diseno_fuste['As']:
                        st.success(f"✅ **Acero:** CUMPLE (As = {diseno_fuste['As_proporcionado']:.2f} ≥ {diseno_fuste['As']:.2f} cm²)")
                    else:
                        st.error(f"⚠️ **Acero:** NO CUMPLE (As = {diseno_fuste['As_proporcionado']:.2f} < {diseno_fuste['As']:.2f} cm²)")
                
                with col3:
                    if diseno_fuste['As_proporcionado'] >= diseno_fuste['Asmin']:
                        st.success(f"✅ **Acero Mín:** CUMPLE (As = {diseno_fuste['As_proporcionado']:.2f} ≥ {diseno_fuste['Asmin']:.2f} cm²)")
                    else:
                        st.error(f"⚠️ **Acero Mín:** NO CUMPLE (As = {diseno_fuste['As_proporcionado']:.2f} < {diseno_fuste['Asmin']:.2f} cm²)")
                
                # Resumen final
                cumple_todo = (FS_volcamiento >= 2.0 and FS_deslizamiento >= 1.5 and 
                              q_max_kg_cm2 <= sigma_adm and not tension and e <= e_limite and
                              diseno_fuste['dreal'] >= diseno_fuste['dreq'] and 
                              diseno_fuste['As_proporcionado'] >= diseno_fuste['As'])
                
                if cumple_todo:
                    st.success("🎉 **RESULTADO FINAL:** El muro CUMPLE con todos los requisitos de estabilidad y diseño estructural")
                else:
                    st.error("⚠️ **RESULTADO FINAL:** El muro NO CUMPLE con todos los requisitos. Se recomienda revisar dimensiones.")
                
                # Gráfico del muro de contención
                st.subheader("🏗️ Visualización del Muro de Contención")
                st.info("Gráfico detallado del muro con todas las dimensiones calculadas")
                
                # Crear dimensiones para el gráfico
                dimensiones_grafico = {
                    'Bz': Bz,
                    'hz': hz,
                    'b': b,
                    'r': r,
                    't': t,
                    'hm': hm
                }
                
                # Generar el gráfico del muro
                fig_muro = dibujar_muro_streamlit(dimensiones_grafico, h1, Df, qsc)
                
                # Mostrar el gráfico en Streamlit
                st.pyplot(fig_muro)
                
                # Información adicional sobre el gráfico
                st.markdown("""
                **Leyenda del Gráfico:**
                - 🔵 **Zapata (Azul claro):** Base de cimentación del muro
                - 🔴 **Muro (Rosa):** Estructura principal de contención
                - 🟡 **Relleno (Amarillo):** Material de relleno detrás del muro
                - 🟤 **Suelo (Marrón):** Suelo de cimentación
                - 🔴 **Flechas rojas:** Sobrecarga aplicada (qsc)
                - 🔵 **Dimensiones en azul:** Medidas calculadas del muro
                """)
                
                # Mostrar información del diseño del fuste si está disponible
                if 'diseno_fuste' in st.session_state:
                    st.subheader("🏗️ Información del Diseño del Fuste")
                    diseno_fuste = st.session_state['diseno_fuste']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.info("**Diseño Estructural:**")
                        st.write(f"• Peralte efectivo requerido: {diseno_fuste['dreq']:.2f} cm")
                        st.write(f"• Peralte efectivo real: {diseno_fuste['dreal']:.2f} cm")
                        st.write(f"• Área de acero requerida: {diseno_fuste['As']:.2f} cm²")
                        st.write(f"• Área de acero mínima: {diseno_fuste['Asmin']:.2f} cm²")
                    
                    with col2:
                        st.info("**Distribución del Acero:**")
                        st.write(f"• Número de barras 5/8\": {diseno_fuste['num_barras']}")
                        st.write(f"• Separación entre barras: {diseno_fuste['separacion']:.1f} cm")
                        st.write(f"• Acero por retracción: {diseno_fuste['As_retraccion']:.2f} cm²")
                        st.write(f"• Barras retracción 1/2\": {diseno_fuste['num_barras_retraccion']}")

    elif opcion == "🏗️ Diseño del Fuste":
        st.title("Diseño y Verificación del Fuste del Muro")
        
        # Verificar acceso basado en plan del usuario
        user_plan = st.session_state.get('plan', 'gratuito')
        user_email = st.session_state.get('user', '')
        
        # Verificar si es admin (acceso completo)
        is_admin = user_email == 'admin' or user_email == 'admin@consorciodej.com'
        
        # Para usuarios normales, verificar plan real en el sistema de pagos
        if PAYMENT_SYSTEM_AVAILABLE and user_email and not is_admin:
            try:
                real_plan = payment_system.get_user_plan(user_email)
                current_plan = real_plan.get('plan', 'gratuito')
                
                # Actualizar session state si el plan cambió
                if st.session_state.get('plan') != current_plan:
                    st.session_state['plan'] = current_plan
                    if 'user_data' in st.session_state:
                        st.session_state['user_data']['plan'] = current_plan
                    user_plan = current_plan
            except Exception as e:
                # Si hay error, usar el plan de session state
                pass
        
        if user_plan == "gratuito" and not is_admin:
            st.warning("⚠️ Esta función requiere plan premium. Actualiza tu cuenta para acceder al diseño estructural.")
            st.info("Plan gratuito incluye: Cálculos básicos, resultados simples")
            st.info("Plan premium incluye: Diseño del fuste, cálculo de refuerzo, reportes detallados")
            
            # Mostrar botón para actualizar plan
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("⭐ Actualizar a Premium", type="primary", key="upgrade_diseno"):
                    st.session_state['show_pricing'] = True
                    st.rerun()
        else:
            st.success("⭐ Plan Premium: Diseño estructural completo del fuste")
            
            if 'diseno_fuste' in st.session_state and 'datos_entrada' in st.session_state:
                diseno_fuste = st.session_state['diseno_fuste']
                datos_entrada = st.session_state['datos_entrada']
                
                # Mostrar información del diseño del fuste
                st.subheader("📊 Resultados del Diseño del Fuste")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Coeficiente Pasivo (kp)", f"{diseno_fuste['kp']:.2f}")
                    st.metric("Empuje Pasivo", f"{diseno_fuste['Ep_kg_m']:.0f} kg/m")
                    st.metric("Altura de Aplicación", f"{diseno_fuste['yt']:.2f} m")
                    st.metric("Momento Volcador Total", f"{diseno_fuste['Mvol_total']:.2f} tn·m/m")
                    st.metric("Momento Estabilizador Total", f"{diseno_fuste['Mesta_total']:.2f} tn·m/m")
                
                with col2:
                    st.metric("Factor Seguridad Volcamiento", f"{diseno_fuste['FSv']:.2f}")
                    st.metric("Factor Seguridad Deslizamiento", f"{diseno_fuste['FSd']:.2f}")
                    st.metric("Ubicación Resultante (x̄)", f"{diseno_fuste['x_barra']:.3f} m")
                    st.metric("Excentricidad (e)", f"{diseno_fuste['e']:.3f} m")
                    st.metric("Cuantía Real (ρ)", f"{diseno_fuste['rho_real']:.4f}")
                
                # Diseño estructural
                st.subheader("🏗️ Diseño Estructural")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info("**Peralte Efectivo:**")
                    st.write(f"• Requerido: {diseno_fuste['dreq']:.2f} cm")
                    st.write(f"• Real: {diseno_fuste['dreal']:.2f} cm")
                    if diseno_fuste['dreal'] >= diseno_fuste['dreq']:
                        st.success("✅ CUMPLE")
                    else:
                        st.error("⚠️ NO CUMPLE")
                
                with col2:
                    st.info("**Área de Acero:**")
                    st.write(f"• Requerida: {diseno_fuste['As']:.2f} cm²")
                    st.write(f"• Mínima: {diseno_fuste['Asmin']:.2f} cm²")
                    st.write(f"• Proporcionada: {diseno_fuste['As_proporcionado']:.2f} cm²")
                    if diseno_fuste['As_proporcionado'] >= diseno_fuste['As']:
                        st.success("✅ CUMPLE")
                    else:
                        st.error("⚠️ NO CUMPLE")
                
                with col3:
                    st.info("**Distribución:**")
                    st.write(f"• Barras 5/8\": {diseno_fuste['num_barras']}")
                    st.write(f"• Separación: {diseno_fuste['separacion']:.1f} cm")
                    st.write(f"• Barras retracción: {diseno_fuste['num_barras_retraccion']}")
                    st.write(f"• Acero retracción: {diseno_fuste['As_retraccion_proporcionado']:.2f} cm²")
                
                # Tabla de propiedades del acero
                st.subheader("📋 Propiedades del Acero Corrugado")
                acero_data = {
                    'Barra N°': ['3', '4', '5', '6', '7'],
                    'Diámetro (pulg)': ['3/8', '1/2', '5/8', '3/4', '7/8'],
                    'Diámetro (cm)': [0.98, 1.27, 1.59, 1.91, 2.22],
                    'Peso (kg/m)': [0.559, 0.993, 1.552, 2.235, 3.042],
                    'Área (cm²)': [0.71, 1.27, 1.98, 2.85, 3.85],
                    'Perímetro (cm)': [2.99, 3.99, 4.99, 5.98, 6.98]
                }
                
                df_acero = pd.DataFrame(acero_data)
                st.dataframe(df_acero, use_container_width=True)
                
                # Verificaciones de estabilidad
                st.subheader("🔍 Verificaciones de Estabilidad del Fuste")
                
                verificaciones = []
                
                # Verificación al volcamiento
                if diseno_fuste['FSv'] >= 2.0:
                    verificaciones.append(["Volcamiento", "✅ CUMPLE", f"FS = {diseno_fuste['FSv']:.2f} ≥ 2.0"])
                else:
                    verificaciones.append(["Volcamiento", "⚠️ NO CUMPLE", f"FS = {diseno_fuste['FSv']:.2f} < 2.0"])
                
                # Verificación al deslizamiento
                if diseno_fuste['FSd'] >= 1.5:
                    verificaciones.append(["Deslizamiento", "✅ CUMPLE", f"FS = {diseno_fuste['FSd']:.2f} ≥ 1.5"])
                else:
                    verificaciones.append(["Deslizamiento", "⚠️ NO CUMPLE", f"FS = {diseno_fuste['FSd']:.2f} < 1.5"])
                
                # Verificación de peralte
                if diseno_fuste['dreal'] >= diseno_fuste['dreq']:
                    verificaciones.append(["Peralte Efectivo", "✅ CUMPLE", f"dreal = {diseno_fuste['dreal']:.2f} ≥ {diseno_fuste['dreq']:.2f}"])
                else:
                    verificaciones.append(["Peralte Efectivo", "⚠️ NO CUMPLE", f"dreal = {diseno_fuste['dreal']:.2f} < {diseno_fuste['dreq']:.2f}"])
                
                # Verificación de acero
                if diseno_fuste['As_proporcionado'] >= diseno_fuste['As']:
                    verificaciones.append(["Área de Acero", "✅ CUMPLE", f"As = {diseno_fuste['As_proporcionado']:.2f} ≥ {diseno_fuste['As']:.2f}"])
                else:
                    verificaciones.append(["Área de Acero", "⚠️ NO CUMPLE", f"As = {diseno_fuste['As_proporcionado']:.2f} < {diseno_fuste['As']:.2f}"])
                
                # Verificación de cuantía mínima
                if diseno_fuste['rho_real'] >= 0.0033:
                    verificaciones.append(["Cuantía Mínima", "✅ CUMPLE", f"ρ = {diseno_fuste['rho_real']:.4f} ≥ 0.0033"])
                else:
                    verificaciones.append(["Cuantía Mínima", "⚠️ NO CUMPLE", f"ρ = {diseno_fuste['rho_real']:.4f} < 0.0033"])
                
                # Mostrar tabla de verificaciones
                df_verif = pd.DataFrame(verificaciones)
                df_verif.columns = ['Verificación', 'Estado', 'Detalle']
                st.dataframe(df_verif, use_container_width=True, hide_index=True)
                
                # Resumen final
                cumple_todo = (diseno_fuste['FSv'] >= 2.0 and diseno_fuste['FSd'] >= 1.5 and 
                              diseno_fuste['dreal'] >= diseno_fuste['dreq'] and 
                              diseno_fuste['As_proporcionado'] >= diseno_fuste['As'] and
                              diseno_fuste['rho_real'] >= 0.0033)
                
                if cumple_todo:
                    st.success("🎉 **RESULTADO FINAL:** El fuste del muro CUMPLE con todos los requisitos de diseño estructural")
                else:
                    st.error("⚠️ **RESULTADO FINAL:** El fuste del muro NO CUMPLE con todos los requisitos. Se recomienda revisar el diseño.")
                
            else:
                st.warning("⚠️ No hay datos de diseño del fuste disponibles. Ejecuta primero el análisis completo.")

    elif opcion == "📄 Generar Reporte":
        st.title("Generar Reporte Técnico")
        
        if st.session_state['plan'] == "gratuito":
            if 'resultados_basicos' in st.session_state:
                resultados = st.session_state['resultados_basicos']
                
                # Reporte básico gratuito
                reporte_basico = f"""
# REPORTE BÁSICO - MURO DE CONTENCIÓN
## CONSORCIO DEJ
### Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}

### DATOS DE ENTRADA:
- Altura del muro: {resultados['altura']:.2f} m
- Base del muro: {resultados['base']:.2f} m
- Espesor del muro: {resultados['espesor']:.2f} m
- Longitud del muro: {resultados['longitud']:.2f} m
- Peso específico del hormigón: 24.0 kN/m³
- Peso específico del suelo: 18.0 kN/m³
- Ángulo de fricción del suelo: 30.0°

### RESULTADOS DEL CÁLCULO:
- Peso del muro: {resultados['peso_muro']:.2f} kN
- Empuje del suelo: {resultados['empuje_suelo']:.2f} kN
- Factor de seguridad al volcamiento: {resultados['fs_volcamiento']:.2f}
- Volumen de hormigón: {resultados['volumen']:.2f} m³
- Coeficiente de empuje activo (Ka): {resultados['ka']:.3f}
- Momento volcador: {resultados['momento_volcador']:.2f} kN·m
- Momento estabilizador: {resultados['momento_estabilizador']:.2f} kN·m

### ANÁLISIS DE ESTABILIDAD:
"""
                
                if resultados['fs_volcamiento'] > 1.5:
                    reporte_basico += "✅ El muro es estable al volcamiento (FS > 1.5)"
                else:
                    reporte_basico += "⚠️ El muro requiere revisión de estabilidad (FS < 1.5)"
                
                reporte_basico += f"""

### CONCLUSIONES:
El análisis básico indica que el muro de contención {'cumple' if resultados['fs_volcamiento'] > 1.5 else 'no cumple'} con los requisitos mínimos de estabilidad al volcamiento.

### NOTA:
Este es un reporte básico del plan gratuito. Para análisis más detallados, considere actualizar al plan premium.

---
Generado por: CONSORCIO DEJ
Plan: Gratuito
"""
                
                st.text_area("Reporte Básico", reporte_basico, height=500)
                
                # Botones para el reporte básico
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        label="📥 Descargar TXT",
                        data=reporte_basico,
                        file_name=f"reporte_basico_muro_contencion_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    # Generar PDF básico
                    pdf_buffer = generar_pdf_reportlab(resultados, {}, {}, "gratuito")
                    st.download_button(
                        label="📄 Descargar PDF",
                        data=pdf_buffer.getvalue(),
                        file_name=f"reporte_basico_muro_contencion_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf"
                    )
                
                with col3:
                    if st.button("🖨️ Generar Reporte en Pantalla", type="primary"):
                        st.success("✅ Reporte básico generado exitosamente")
                        st.balloons()
                        
                        # Mostrar el reporte en formato expandible
                        with st.expander("📋 VER REPORTE BÁSICO COMPLETO", expanded=True):
                            st.markdown(reporte_basico)
            else:
                st.warning("⚠️ No hay resultados disponibles. Realiza primero los cálculos básicos.")
        else:
            # Reporte premium completo
            if 'resultados_completos' in st.session_state:
                resultados = st.session_state['resultados_completos']
                
                reporte_premium = f"""
# REPORTE TÉCNICO COMPLETO - MURO DE CONTENCIÓN
## CONSORCIO DEJ
### Análisis según Teoría de Rankine
### Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}

### 1. COEFICIENTES DE PRESIÓN:
- Coeficiente de empuje activo (Ka): {resultados['ka']:.3f}
- Coeficiente de empuje pasivo (Kp): {resultados['kp']:.3f}
- Altura equivalente por sobrecarga (hs): {resultados['hs']:.3f} m

### 2. DIMENSIONES CALCULADAS:
- Ancho de zapata (Bz): {resultados['Bz']:.2f} m
- Peralte de zapata (hz): {resultados['hz']:.2f} m
- Espesor del muro (b): {resultados['b']:.2f} m
- Longitud de puntera (r): {resultados['r']:.2f} m
- Longitud de talón (t): {resultados['t']:.2f} m
- Altura del talud (h1): {resultados['h1']:.2f} m
- Profundidad de desplante (Df): {resultados['Df']:.2f} m

### 3. ANÁLISIS DE EMPUJES:
- Empuje activo por relleno: {resultados['Ea_relleno']:.2f} tn/m
- Empuje activo por sobrecarga: {resultados['Ea_sobrecarga']:.2f} tn/m
- Empuje activo total: {resultados['Ea_total']:.2f} tn/m
- Empuje pasivo: {resultados['Ep']:.2f} tn/m

### 4. ANÁLISIS DE PESOS:
- Peso del muro: {resultados['W_muro']:.2f} tn/m
- Peso de la zapata: {resultados['W_zapata']:.2f} tn/m
- Peso del relleno: {resultados['W_relleno']:.2f} tn/m
- Peso total: {resultados['W_total']:.2f} tn/m

### 5. MOMENTOS Y FACTORES DE SEGURIDAD:
- Momento volcador: {resultados['M_volcador']:.2f} tn·m/m
- Momento estabilizador: {resultados['M_estabilizador']:.2f} tn·m/m
- Factor de seguridad al volcamiento: {resultados['FS_volcamiento']:.2f}
- Factor de seguridad al deslizamiento: {resultados['FS_deslizamiento']:.2f}

### 6. VERIFICACIÓN DE PRESIONES:
- Presión máxima: {resultados['q_max_kg_cm2']:.2f} kg/cm²
- Presión mínima: {resultados['q_min_kg_cm2']:.2f} kg/cm²
- Excentricidad: {resultados['e']:.3f} m
- Hay tensiones: {'Sí' if resultados['tension'] else 'No'}

### 7. VERIFICACIONES DE ESTABILIDAD:
"""
                
                # Verificaciones de estabilidad
                cumple_volcamiento = resultados['FS_volcamiento'] >= 2.0
                cumple_deslizamiento = resultados['FS_deslizamiento'] >= 1.5
                cumple_presion = resultados['q_max_kg_cm2'] <= 2.5  # Asumiendo q_adm = 2.5 kg/cm²
                cumple_excentricidad = resultados['e'] <= resultados['Bz'] / 6
                sin_tensiones = not resultados['tension']
                
                reporte_premium += f"""
**Verificación al Volcamiento:**
- Factor de seguridad calculado: {resultados['FS_volcamiento']:.2f}
- Factor mínimo requerido: 2.0
- Estado: {'✅ CUMPLE' if cumple_volcamiento else '⚠️ NO CUMPLE'}

**Verificación al Deslizamiento:**
- Factor de seguridad calculado: {resultados['FS_deslizamiento']:.2f}
- Factor mínimo requerido: 1.5
- Estado: {'✅ CUMPLE' if cumple_deslizamiento else '⚠️ NO CUMPLE'}

**Verificación de Presiones:**
- Presión máxima: {resultados['q_max_kg_cm2']:.2f} kg/cm²
- Presión admisible: 2.5 kg/cm²
- Estado: {'✅ CUMPLE' if cumple_presion else '⚠️ NO CUMPLE'}

**Verificación de Excentricidad:**
- Excentricidad calculada: {resultados['e']:.3f} m
- Límite (B/6): {resultados['Bz']/6:.3f} m
- Estado: {'✅ CUMPLE' if cumple_excentricidad else '⚠️ NO CUMPLE'}

**Verificación de Tensiones:**
- Hay tensiones: {'Sí' if resultados['tension'] else 'No'}
- Estado: {'✅ CUMPLE' if sin_tensiones else '⚠️ NO CUMPLE'}

### 8. RESULTADO FINAL:
"""
                
                cumple_todo = cumple_volcamiento and cumple_deslizamiento and cumple_presion and cumple_excentricidad and sin_tensiones
                
                if cumple_todo:
                    reporte_premium += """
🎉 **EL MURO CUMPLE CON TODOS LOS REQUISITOS DE ESTABILIDAD**

El análisis completo según la teoría de Rankine indica que el muro de contención 
es estructuralmente seguro y cumple con todas las verificaciones requeridas.
"""
                else:
                    reporte_premium += """
⚠️ **EL MURO NO CUMPLE CON TODOS LOS REQUISITOS**

Se recomienda revisar las dimensiones del muro o las propiedades del suelo 
para mejorar los factores de seguridad y cumplir con las especificaciones.
"""

                # Agregar información del diseño del fuste si está disponible
                if 'diseno_fuste' in st.session_state and st.session_state['diseno_fuste']:
                    diseno_fuste = st.session_state['diseno_fuste']
                    reporte_premium += f"""

### 9. DISEÑO Y VERIFICACIÓN DEL FUSTE DEL MURO:
**9.1 Coeficiente Pasivo y Empuje:**
- Coeficiente pasivo (kp): {diseno_fuste['kp']:.2f}
- Empuje pasivo: {diseno_fuste['Ep_kg_m']:.0f} kg/m
- Altura de aplicación: {diseno_fuste['yt']:.2f} m

**9.2 Momentos y Factores de Seguridad:**
- Momento volcador total: {diseno_fuste['Mvol_total']:.2f} tn·m/m
- Momento estabilizador total: {diseno_fuste['Mesta_total']:.2f} tn·m/m
- Factor de seguridad al volcamiento: {diseno_fuste['FSv']:.2f}
- Factor de seguridad al deslizamiento: {diseno_fuste['FSd']:.2f}

**9.3 Diseño Estructural:**
- Peralte efectivo requerido: {diseno_fuste['dreq']:.2f} cm
- Peralte efectivo real: {diseno_fuste['dreal']:.2f} cm
- Área de acero requerida: {diseno_fuste['As']:.2f} cm²
- Área de acero mínima: {diseno_fuste['Asmin']:.2f} cm²
- Área de acero proporcionada: {diseno_fuste['As_proporcionado']:.2f} cm²

**9.4 Distribución del Acero:**
- Número de barras 5/8\": {diseno_fuste['num_barras']}
- Separación entre barras: {diseno_fuste['separacion']:.1f} cm
- Acero por retracción y temperatura: {diseno_fuste['As_retraccion']:.2f} cm²
- Barras de retracción 1/2\": {diseno_fuste['num_barras_retraccion']}

**9.5 Verificaciones del Fuste:**
- Peralte efectivo: {'✅ CUMPLE' if diseno_fuste['dreal'] >= diseno_fuste['dreq'] else '⚠️ NO CUMPLE'}
- Área de acero: {'✅ CUMPLE' if diseno_fuste['As_proporcionado'] >= diseno_fuste['As'] else '⚠️ NO CUMPLE'}
- Cuantía mínima: {'✅ CUMPLE' if diseno_fuste['rho_real'] >= 0.0033 else '⚠️ NO CUMPLE'}

### 10. RECOMENDACIONES TÉCNICAS:
- Verificar la capacidad portante del suelo en campo
- Revisar el diseño del refuerzo estructural según ACI 318
- Considerar efectos sísmicos según la normativa local
- Realizar inspecciones periódicas durante la construcción
- Monitorear deformaciones durante el servicio
- Verificar drenaje del relleno para evitar presiones hidrostáticas
- **NUEVO:** Verificar la colocación del acero según el diseño calculado
- **NUEVO:** Controlar la calidad del concreto durante la construcción

### 11. INFORMACIÓN DEL PROYECTO:
- Empresa: CONSORCIO DEJ
- Método de análisis: Teoría de Rankine
- Diseño estructural: Según PARTE 2.2.py
- Fecha de análisis: {datetime.now().strftime('%d/%m/%Y %H:%M')}
- Plan: Premium
- Software: Streamlit + Python

---
**Este reporte fue generado automáticamente por el sistema de análisis de muros de contención de CONSORCIO DEJ.**
**Para consultas técnicas, contacte a nuestro equipo de ingeniería.**
"""
                else:
                    reporte_premium += f"""

### 9. RECOMENDACIONES TÉCNICAS:
- Verificar la capacidad portante del suelo en campo
- Revisar el diseño del refuerzo estructural según ACI 318
- Considerar efectos sísmicos según la normativa local
- Realizar inspecciones periódicas durante la construcción
- Monitorear deformaciones durante el servicio
- Verificar drenaje del relleno para evitar presiones hidrostáticas

### 10. INFORMACIÓN DEL PROYECTO:
- Empresa: CONSORCIO DEJ
- Método de análisis: Teoría de Rankine
- Fecha de análisis: {datetime.now().strftime('%d/%m/%Y %H:%M')}
- Plan: Premium
- Software: Streamlit + Python

---
**Este reporte fue generado automáticamente por el sistema de análisis de muros de contención de CONSORCIO DEJ.**
**Para consultas técnicas, contacte a nuestro equipo de ingeniería.**
"""
                
                st.text_area("Reporte Premium", reporte_premium, height=600)
                
                # Botones para el reporte premium
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        label="📥 Descargar TXT",
                        data=reporte_premium,
                        file_name=f"reporte_premium_muro_contencion_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    # Generar PDF premium con diseño del fuste
                    if 'datos_entrada' in st.session_state and 'diseno_fuste' in st.session_state:
                        try:
                            pdf_buffer = generar_pdf_reportlab(
                                st.session_state['resultados_completos'], 
                                st.session_state['datos_entrada'], 
                                st.session_state['diseno_fuste'], 
                                "premium"
                            )
                            st.download_button(
                                label="📄 Descargar PDF Premium",
                                data=pdf_buffer.getvalue(),
                                file_name=f"reporte_premium_muro_contencion_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                mime="application/pdf"
                            )
                        except Exception as e:
                            st.error(f"⚠️ Error generando PDF: {str(e)}")
                            st.info("Intenta ejecutar el análisis completo nuevamente")
                    else:
                        st.warning("⚠️ Ejecuta primero el análisis completo")
                
                with col3:
                    if st.button("🖨️ Generar Reporte en Pantalla", type="primary"):
                        st.success("✅ Reporte técnico generado exitosamente")
                        st.balloons()
                        
                        # Mostrar el reporte en formato expandible
                        with st.expander("📋 VER REPORTE TÉCNICO COMPLETO", expanded=True):
                            st.markdown(reporte_premium)
            else:
                st.warning("⚠️ No hay resultados disponibles. Realiza primero el análisis completo.")

    elif opcion == "📈 Gráficos":
        st.title("Gráficos y Visualizaciones")
        
        if st.session_state['plan'] == "gratuito":
            if 'resultados_basicos' in st.session_state:
                resultados = st.session_state['resultados_basicos']
                
                # Gráfico básico gratuito
                datos = pd.DataFrame({
                    'Fuerza': ['Peso Muro', 'Empuje Suelo'],
                    'Valor (kN)': [resultados['peso_muro'], resultados['empuje_suelo']]
                })
                
                fig = px.bar(datos, x='Fuerza', y='Valor (kN)', 
                            title="Comparación de Fuerzas - Plan Gratuito",
                            color='Fuerza',
                            color_discrete_map={'Peso Muro': '#2E8B57', 'Empuje Suelo': '#DC143C'})
                
                fig.update_layout(
                    xaxis_title="Tipo de Fuerza",
                    yaxis_title="Valor (kN)",
                    height=400
                )
                
                fig.update_traces(texttemplate='%{y:.1f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
                
                # Gráfico de momentos
                datos_momentos = pd.DataFrame({
                    'Momento': ['Volcador', 'Estabilizador'],
                    'Valor (kN·m)': [resultados['momento_volcador'], resultados['momento_estabilizador']]
                })
                
                fig2 = px.pie(datos_momentos, values='Valor (kN·m)', names='Momento',
                             title="Distribución de Momentos - Plan Gratuito",
                             color_discrete_map={'Volcador': '#FF6B6B', 'Estabilizador': '#4ECDC4'})
                
                fig2.update_traces(textposition='inside', textinfo='percent+label+value')
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("⚠️ No hay resultados disponibles. Realiza primero los cálculos básicos.")
        else:
            # Gráficos premium
            if 'resultados_completos' in st.session_state:
                resultados = st.session_state['resultados_completos']
                
                # Gráfico de fuerzas
                col1, col2 = st.columns(2)
                
                with col1:
                    datos_fuerzas = pd.DataFrame({
                        'Fuerza': ['Empuje Activo', 'Empuje Pasivo', 'Peso Total'],
                        'Valor (tn/m)': [resultados['Ea_total'], resultados['Ep'], 
                                        resultados['W_total']]
                    })
                    
                    fig1 = px.bar(datos_fuerzas, x='Fuerza', y='Valor (tn/m)',
                                 title="Análisis de Fuerzas - Plan Premium",
                                 color='Fuerza',
                                 color_discrete_map={
                                     'Empuje Activo': '#DC143C',
                                     'Empuje Pasivo': '#2E8B57',
                                     'Peso Total': '#4169E1'
                                 })
                    
                    fig1.update_layout(
                        xaxis_title="Tipo de Fuerza",
                        yaxis_title="Valor (tn/m)",
                        height=400
                    )
                    
                    fig1.update_traces(texttemplate='%{y:.2f}', textposition='outside')
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Gráfico de momentos
                    datos_momentos = pd.DataFrame({
                        'Momento': ['Volcador', 'Estabilizador'],
                        'Valor (tn·m/m)': [resultados['M_volcador'], resultados['M_estabilizador']]
                    })
                    
                    fig2 = px.pie(datos_momentos, values='Valor (tn·m/m)', names='Momento',
                                 title="Distribución de Momentos - Plan Premium",
                                 color_discrete_map={'Volcador': '#FF6B6B', 'Estabilizador': '#4ECDC4'})
                    
                    fig2.update_traces(textposition='inside', textinfo='percent+label+value')
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Gráfico de dimensiones
                st.subheader("📏 Dimensiones del Muro")
                dimensiones = {
                    'Dimensión': ['Bz', 'hz', 'b', 'r', 't'],
                    'Valor (m)': [resultados['Bz'], resultados['hz'], resultados['b'], 
                                 resultados['r'], resultados['t']]
                }
                
                fig3 = px.bar(pd.DataFrame(dimensiones), x='Dimensión', y='Valor (m)',
                             title="Dimensiones Calculadas del Muro - Plan Premium",
                             color='Dimensión',
                             color_discrete_map={
                                 'Bz': '#FF1493',
                                 'hz': '#00CED1',
                                 'b': '#32CD32',
                                 'r': '#FFD700',
                                 't': '#FF6347'
                             })
                
                fig3.update_layout(
                    xaxis_title="Dimensión",
                    yaxis_title="Valor (m)",
                    height=400
                )
                
                fig3.update_traces(texttemplate='%{y:.2f}', textposition='outside')
                st.plotly_chart(fig3, use_container_width=True)
                
                # Gráfico del muro de contención
                st.subheader("🏗️ Visualización del Muro de Contención")
                st.info("Representación gráfica detallada del muro diseñado")
                
                # Crear dimensiones para el gráfico
                dimensiones_grafico = {
                    'Bz': resultados['Bz'],
                    'hz': resultados['hz'],
                    'b': resultados['b'],
                    'r': resultados['r'],
                    't': resultados['t'],
                    'hm': resultados['hm']
                }
                
                # Generar el gráfico del muro con valores reales
                fig_muro = dibujar_muro_streamlit(dimensiones_grafico, resultados['h1'], resultados['Df'], resultados['qsc'])
                
                # Mostrar el gráfico en Streamlit
                st.pyplot(fig_muro)
                
                # Información adicional sobre el gráfico
                st.markdown("""
                **Leyenda del Gráfico:**
                - 🔵 **Zapata (Azul claro):** Base de cimentación del muro
                - 🔴 **Muro (Rosa):** Estructura principal de contención
                - 🟡 **Relleno (Amarillo):** Material de relleno detrás del muro
                - 🟤 **Suelo (Marrón):** Suelo de cimentación
                - 🔴 **Flechas rojas:** Sobrecarga aplicada (qsc)
                - 🔵 **Dimensiones en azul:** Medidas calculadas del muro
                """)
            else:
                st.warning("⚠️ No hay resultados disponibles. Realiza primero el análisis completo.")

    elif opcion == "ℹ️ Acerca de":
        st.title("Acerca de CONSORCIO DEJ")
        st.write("""
        ### 🏗️ CONSORCIO DEJ
        **Ingeniería y Construcción Especializada**
        
        Esta aplicación fue desarrollada para facilitar el cálculo y diseño de muros de contención
        utilizando métodos reconocidos en ingeniería geotécnica.
        
        **Características del Plan Gratuito:**
        - ✅ Cálculos básicos de estabilidad
        - ✅ Resultados simples con gráficos
        - ✅ Reporte básico descargable
        - ✅ Análisis de factor de seguridad
        
        **Características del Plan Premium:**
        - ⭐ Análisis completo con teoría de Rankine
        - ⭐ Cálculos de dimensiones automáticos
        - ⭐ **Diseño y verificación del fuste del muro** (NUEVO)
        - ⭐ **Cálculo de refuerzo estructural** (NUEVO)
        - ⭐ **Reportes técnicos en PDF** (NUEVO)
        - ⭐ Gráficos avanzados y visualizaciones
        - ⭐ Verificaciones de estabilidad completas
        - ⭐ **Altura de coronación optimizada** (NUEVO)
        
        **Desarrollado con:** Python, Streamlit, Plotly
        **Normativas:** Aplicación de la teoría de Rankine para muros de contención
        """)

    elif opcion == "✉️ Contacto":
        st.title("Contacto")
        st.write("""
        ### 🏗️ CONSORCIO DEJ
        **Información de Contacto:**
        
        📧 Email: contacto@consorciodej.com  
        📱 Teléfono: +123 456 7890  
        🌐 Web: www.consorciodej.com  
        📍 Dirección: [Tu dirección aquí]
        
        **Horarios de Atención:**
        Lunes a Viernes: 8:00 AM - 6:00 PM
        
        **Servicios:**
        - Diseño de muros de contención
        - Análisis geotécnico
        - Ingeniería estructural
        - Construcción especializada
        """)

    # Mostrar plan actual en sidebar
    if st.session_state['plan'] == "gratuito":
        st.sidebar.info("🆓 Plan Gratuito - Funciones limitadas")
        st.sidebar.write("Para acceder a todas las funciones, actualiza a Premium")
        
        # Información sobre cómo acceder al plan premium
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔑 Acceso Premium")
        st.sidebar.write("**Usuario:** premium")
        st.sidebar.write("**Contraseña:** premium")
        st.sidebar.info("Cierra sesión y vuelve a iniciar con las credenciales premium")
    else:
        st.sidebar.success("⭐ Plan Premium - Acceso completo")
        
        # Información para administradores
        st.sidebar.markdown("---")
        st.sidebar.subheader("👨‍💼 Panel de Administrador")
        st.sidebar.write("**Usuario actual:** " + st.session_state['user'])
        st.sidebar.write("**Plan:** Premium")
        st.sidebar.success("Acceso completo a todas las funciones")