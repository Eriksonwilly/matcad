import streamlit as st
import numpy as np
import pandas as pd
from math import sqrt
from datetime import datetime
import hashlib
import io
import base64
import math
import tempfile
import os

# Importaciones opcionales con manejo de errores
try:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Polygon
    import matplotlib
    matplotlib.use('Agg')  # Backend no interactivo para Streamlit
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Importar sistema de pagos simple
try:
    from simple_payment_system import payment_system
    PAYMENT_SYSTEM_AVAILABLE = True
except ImportError:
    PAYMENT_SYSTEM_AVAILABLE = False

# Importaciones opcionales con manejo de errores
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# =====================
# FUNCIONES PARA GRÁFICOS DE CORTANTES Y MOMENTOS (ARTHUR H. NILSON)
# =====================

def calcular_cortantes_momentos_viga_simple(L, w, P=None, a=None):
    """
    Calcula cortantes y momentos para viga simplemente apoyada
    Según Arthur H. Nilson - Diseño de Estructuras de Concreto
    
    L: Luz de la viga (m)
    w: Carga distribuida (kg/m)
    P: Carga puntual (kg) - opcional
    a: Distancia de la carga puntual desde el apoyo izquierdo (m) - opcional
    """
    x = np.linspace(0, L, 100)
    
    # Inicializar arrays
    V = np.zeros_like(x)
    M = np.zeros_like(x)
    
    # Carga distribuida
    if w > 0:
        # Reacciones
        R_A = w * L / 2
        R_B = w * L / 2
        
        # Cortantes y momentos
        V = R_A - w * x
        M = R_A * x - w * x**2 / 2
    
    # Carga puntual
    if P is not None and a is not None:
        # Reacciones
        R_A = P * (L - a) / L
        R_B = P * a / L
        
        # Cortantes y momentos
        for i, xi in enumerate(x):
            if xi <= a:
                V[i] = R_A
                M[i] = R_A * xi
            else:
                V[i] = R_A - P
                M[i] = R_A * xi - P * (xi - a)
    
    return x, V, M

def calcular_cortantes_momentos_viga_empotrada(L, w, P=None, a=None):
    """
    Calcula cortantes y momentos para viga empotrada
    Según Arthur H. Nilson - Diseño de Estructuras de Concreto
    """
    x = np.linspace(0, L, 100)
    
    # Inicializar arrays
    V = np.zeros_like(x)
    M = np.zeros_like(x)
    
    # Carga distribuida
    if w > 0:
        # Reacciones y momentos de empotramiento
        R_A = w * L / 2
        M_A = -w * L**2 / 12
        M_B = w * L**2 / 12
        
        # Cortantes y momentos
        V = R_A - w * x
        M = M_A + R_A * x - w * x**2 / 2
    
    # Carga puntual
    if P is not None and a is not None:
        # Reacciones y momentos de empotramiento
        R_A = P * (3*L - 2*a) * (L - a) / (2*L**2)
        R_B = P * (3*L - 2*a) * a / (2*L**2)
        M_A = -P * a * (L - a)**2 / (2*L**2)
        M_B = P * a**2 * (L - a) / (2*L**2)
        
        # Cortantes y momentos
        for i, xi in enumerate(x):
            if xi <= a:
                V[i] = R_A
                M[i] = M_A + R_A * xi
            else:
                V[i] = R_A - P
                M[i] = M_A + R_A * xi - P * (xi - a)
    
    return x, V, M

def calcular_cortantes_momentos_viga_continua(L1, L2, w1, w2):
    """
    Calcula cortantes y momentos para viga continua de dos tramos
    Según Arthur H. Nilson - Diseño de Estructuras de Concreto
    """
    # Coeficientes de momento para viga continua
    # M_B = -w1*L1^2/8 - w2*L2^2/8 (aproximación)
    M_B = -(w1 * L1**2 + w2 * L2**2) / 8
    
    # Reacciones
    R_A = (w1 * L1 / 2) - (M_B / L1)
    R_B1 = (w1 * L1 / 2) + (M_B / L1)
    R_B2 = (w2 * L2 / 2) - (M_B / L2)
    R_C = (w2 * L2 / 2) + (M_B / L2)
    
    # Generar puntos para cada tramo
    x1 = np.linspace(0, L1, 50)
    x2 = np.linspace(0, L2, 50)
    
    # Cortantes y momentos para tramo 1
    V1 = R_A - w1 * x1
    M1 = R_A * x1 - w1 * x1**2 / 2
    
    # Cortantes y momentos para tramo 2
    V2 = R_B2 - w2 * x2
    M2 = R_B2 * x2 - w2 * x2**2 / 2 + M_B
    
    return x1, V1, M1, x2, V2, M2, R_A, R_B1, R_B2, R_C, M_B

def graficar_cortantes_momentos_nilson(L, w, P=None, a=None, tipo_viga="simple"):
    """
    Genera gráficos de cortantes y momentos según Arthur H. Nilson
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Backend no interactivo para Streamlit
    except ImportError:
        st.error("❌ Matplotlib no está instalado. Instale con: pip install matplotlib")
        return None
    
    if tipo_viga == "simple":
        x, V, M = calcular_cortantes_momentos_viga_simple(L, w, P, a)
    elif tipo_viga == "empotrada":
        x, V, M = calcular_cortantes_momentos_viga_empotrada(L, w, P, a)
    else:
        st.error("Tipo de viga no válido")
        return None
    
    # Crear figura con subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Gráfico de cortantes
    ax1.plot(x, V, 'r-', linewidth=2, label='Cortante (V)')
    ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=L, color='k', linestyle='-', alpha=0.3)
    ax1.fill_between(x, V, 0, alpha=0.3, color='red')
    ax1.set_title(f'Diagrama de Cortantes - Viga {tipo_viga.title()}', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Distancia (m)')
    ax1.set_ylabel('Cortante (kg)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Gráfico de momentos
    ax2.plot(x, M, 'b-', linewidth=2, label='Momento (M)')
    ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax2.axvline(x=L, color='k', linestyle='-', alpha=0.3)
    ax2.fill_between(x, M, 0, alpha=0.3, color='blue')
    ax2.set_title(f'Diagrama de Momentos - Viga {tipo_viga.title()}', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Distancia (m)')
    ax2.set_ylabel('Momento (kg·m)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    return fig

def graficar_viga_continua_nilson(L1, L2, w1, w2):
    """
    Genera gráficos de cortantes y momentos para viga continua
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Backend no interactivo para Streamlit
    except ImportError:
        st.error("❌ Matplotlib no está instalado. Instale con: pip install matplotlib")
        return None
    
    x1, V1, M1, x2, V2, M2, R_A, R_B1, R_B2, R_C, M_B = calcular_cortantes_momentos_viga_continua(L1, L2, w1, w2)
    
    # Crear figura con subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Gráfico de cortantes
    ax1.plot(x1, V1, 'r-', linewidth=2, label='Tramo 1')
    ax1.plot(x2 + L1, V2, 'r-', linewidth=2, label='Tramo 2')
    ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=L1, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=L1+L2, color='k', linestyle='-', alpha=0.3)
    ax1.fill_between(x1, V1, 0, alpha=0.3, color='red')
    ax1.fill_between(x2 + L1, V2, 0, alpha=0.3, color='red')
    ax1.set_title('Diagrama de Cortantes - Viga Continua', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Distancia (m)')
    ax1.set_ylabel('Cortante (kg)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Gráfico de momentos
    ax2.plot(x1, M1, 'b-', linewidth=2, label='Tramo 1')
    ax2.plot(x2 + L1, M2, 'b-', linewidth=2, label='Tramo 2')
    ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax2.axvline(x=L1, color='k', linestyle='-', alpha=0.3)
    ax2.axvline(x=L1+L2, color='k', linestyle='-', alpha=0.3)
    ax2.fill_between(x1, M1, 0, alpha=0.3, color='blue')
    ax2.fill_between(x2 + L1, M2, 0, alpha=0.3, color='blue')
    ax2.set_title('Diagrama de Momentos - Viga Continua', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Distancia (m)')
    ax2.set_ylabel('Momento (kg·m)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    return fig

# =====================
# FUNCIONES PARA GRÁFICOS DE CORTANTES Y MOMENTOS (JACK C. MCCORMAC)
# =====================

def calcular_cortantes_momentos_viga_simple_mccormac(L, w, P=None, a=None):
    """
    Calcula cortantes y momentos para viga simplemente apoyada
    Según Jack C. McCormac - Diseño de Estructuras de Concreto
    
    L: Luz de la viga (m)
    w: Carga distribuida (kg/m)
    P: Carga puntual (kg) - opcional
    a: Distancia de la carga puntual desde el apoyo izquierdo (m) - opcional
    """
    x = np.linspace(0, L, 100)
    
    # Inicializar arrays
    V = np.zeros_like(x)
    M = np.zeros_like(x)
    
    # Carga distribuida
    if w > 0:
        # Reacciones según McCormac
        R_A = w * L / 2
        R_B = w * L / 2
        
        # Cortantes y momentos
        V = R_A - w * x
        M = R_A * x - w * x**2 / 2
    
    # Carga puntual
    if P is not None and a is not None:
        # Reacciones según McCormac
        R_A = P * (L - a) / L
        R_B = P * a / L
        
        # Cortantes y momentos
        for i, xi in enumerate(x):
            if xi <= a:
                V[i] = R_A
                M[i] = R_A * xi
            else:
                V[i] = R_A - P
                M[i] = R_A * xi - P * (xi - a)
    
    return x, V, M

def calcular_cortantes_momentos_viga_empotrada_mccormac(L, w, P=None, a=None):
    """
    Calcula cortantes y momentos para viga empotrada
    Según Jack C. McCormac - Diseño de Estructuras de Concreto
    """
    x = np.linspace(0, L, 100)
    
    # Inicializar arrays
    V = np.zeros_like(x)
    M = np.zeros_like(x)
    
    # Carga distribuida
    if w > 0:
        # Reacciones y momentos de empotramiento según McCormac
        R_A = w * L / 2
        M_A = -w * L**2 / 12
        M_B = w * L**2 / 12
        
        # Cortantes y momentos
        V = R_A - w * x
        M = M_A + R_A * x - w * x**2 / 2
    
    # Carga puntual
    if P is not None and a is not None:
        # Reacciones y momentos de empotramiento según McCormac
        R_A = P * (3*L - 2*a) * (L - a) / (2*L**2)
        R_B = P * (3*L - 2*a) * a / (2*L**2)
        M_A = -P * a * (L - a)**2 / (2*L**2)
        M_B = P * a**2 * (L - a) / (2*L**2)
        
        # Cortantes y momentos
        for i, xi in enumerate(x):
            if xi <= a:
                V[i] = R_A
                M[i] = M_A + R_A * xi
            else:
                V[i] = R_A - P
                M[i] = M_A + R_A * xi - P * (xi - a)
    
    return x, V, M

def calcular_cortantes_momentos_viga_continua_mccormac(L1, L2, w1, w2):
    """
    Calcula cortantes y momentos para viga continua de dos tramos
    Según Jack C. McCormac - Diseño de Estructuras de Concreto
    """
    # Coeficientes de momento para viga continua según McCormac
    # M_B = -w1*L1^2/8 - w2*L2^2/8 (aproximación)
    M_B = -(w1 * L1**2 + w2 * L2**2) / 8
    
    # Reacciones
    R_A = (w1 * L1 / 2) - (M_B / L1)
    R_B1 = (w1 * L1 / 2) + (M_B / L1)
    R_B2 = (w2 * L2 / 2) - (M_B / L2)
    R_C = (w2 * L2 / 2) + (M_B / L2)
    
    # Generar puntos para cada tramo
    x1 = np.linspace(0, L1, 50)
    x2 = np.linspace(0, L2, 50)
    
    # Cortantes y momentos para tramo 1
    V1 = R_A - w1 * x1
    M1 = R_A * x1 - w1 * x1**2 / 2
    
    # Cortantes y momentos para tramo 2
    V2 = R_B2 - w2 * x2
    M2 = R_B2 * x2 - w2 * x2**2 / 2 + M_B
    
    return x1, V1, M1, x2, V2, M2, R_A, R_B1, R_B2, R_C, M_B

def graficar_cortantes_momentos_mccormac(L, w, P=None, a=None, tipo_viga="simple"):
    """
    Genera gráficos de cortantes y momentos según Jack C. McCormac
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Backend no interactivo para Streamlit
    except ImportError:
        st.error("❌ Matplotlib no está instalado. Instale con: pip install matplotlib")
        return None
    
    if tipo_viga == "simple":
        x, V, M = calcular_cortantes_momentos_viga_simple_mccormac(L, w, P, a)
    elif tipo_viga == "empotrada":
        x, V, M = calcular_cortantes_momentos_viga_empotrada_mccormac(L, w, P, a)
    else:
        st.error("Tipo de viga no válido")
        return None
    
    # Crear figura con subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Gráfico de cortantes
    ax1.plot(x, V, 'r-', linewidth=2, label='Cortante (V)')
    ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=L, color='k', linestyle='-', alpha=0.3)
    ax1.fill_between(x, V, 0, alpha=0.3, color='red')
    ax1.set_title(f'Diagrama de Cortantes - Viga {tipo_viga.title()} (McCormac)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Distancia (m)')
    ax1.set_ylabel('Cortante (kg)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Gráfico de momentos
    ax2.plot(x, M, 'b-', linewidth=2, label='Momento (M)')
    ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax2.axvline(x=L, color='k', linestyle='-', alpha=0.3)
    ax2.fill_between(x, M, 0, alpha=0.3, color='blue')
    ax2.set_title(f'Diagrama de Momentos - Viga {tipo_viga.title()} (McCormac)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Distancia (m)')
    ax2.set_ylabel('Momento (kg·m)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    return fig

def graficar_viga_continua_mccormac(L1, L2, w1, w2):
    """
    Genera gráficos de cortantes y momentos para viga continua según McCormac
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Backend no interactivo para Streamlit
    except ImportError:
        st.error("❌ Matplotlib no está instalado. Instale con: pip install matplotlib")
        return None
    
    x1, V1, M1, x2, V2, M2, R_A, R_B1, R_B2, R_C, M_B = calcular_cortantes_momentos_viga_continua_mccormac(L1, L2, w1, w2)
    
    # Crear figura con subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Gráfico de cortantes
    ax1.plot(x1, V1, 'r-', linewidth=2, label='Tramo 1')
    ax1.plot(x2 + L1, V2, 'r-', linewidth=2, label='Tramo 2')
    ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=L1, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=L1+L2, color='k', linestyle='-', alpha=0.3)
    ax1.fill_between(x1, V1, 0, alpha=0.3, color='red')
    ax1.fill_between(x2 + L1, V2, 0, alpha=0.3, color='red')
    ax1.set_title('Diagrama de Cortantes - Viga Continua (McCormac)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Distancia (m)')
    ax1.set_ylabel('Cortante (kg)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Gráfico de momentos
    ax2.plot(x1, M1, 'b-', linewidth=2, label='Tramo 1')
    ax2.plot(x2 + L1, M2, 'b-', linewidth=2, label='Tramo 2')
    ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax2.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax2.axvline(x=L1, color='k', linestyle='-', alpha=0.3)
    ax2.axvline(x=L1+L2, color='k', linestyle='-', alpha=0.3)
    ax2.fill_between(x1, M1, 0, alpha=0.3, color='blue')
    ax2.fill_between(x2 + L1, M2, 0, alpha=0.3, color='blue')
    ax2.set_title('Diagrama de Momentos - Viga Continua (McCormac)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Distancia (m)')
    ax2.set_ylabel('Momento (kg·m)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    return fig

# =====================
# SISTEMA DE LOGIN Y PLANES
# =====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    valid_users = {
        "admin": hash_password("admin123"),
        "demo": hash_password("demo123")
    }
    return username in valid_users and valid_users[username] == hash_password(password)

def get_user_plan(username):
    plan_mapping = {
        "admin": "empresarial",
        "demo": "basico"
    }
    return plan_mapping.get(username, "basico")

# Función para generar PDF del reporte
def generar_pdf_reportlab(resultados, datos_entrada, plan="premium"):
    """
    Genera un PDF profesional usando ReportLab
    """
    if not REPORTLAB_AVAILABLE:
        # Crear un archivo de texto simple como fallback
        pdf_buffer = io.BytesIO()
        reporte_texto = f"""
CONSORCIO DEJ
Ingeniería y Construcción
Reporte de Análisis Estructural - {plan.upper()}
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
    
    # Título principal
    try:
        elements.append(Paragraph("CONSORCIO DEJ", styleH))
        elements.append(Paragraph("Ingeniería y Construcción", styleN))
        elements.append(Paragraph(f"Reporte de Análisis Estructural - {plan.upper()}", styleH2))
        elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styleN))
        elements.append(Spacer(1, 20))
    except Exception as e:
        print(f"Error en título: {e}")
        elements.append(Paragraph("CONSORCIO DEJ - Reporte de Análisis Estructural", styleN))
    
    if plan == "premium":
        # Reporte premium completo
        elements.append(Paragraph("1. DATOS DE ENTRADA", styleH))
        datos_tabla = [
            ["Parámetro", "Valor", "Unidad"],
            ["Resistencia del concreto (f'c)", f"{datos_entrada.get('f_c', 0)}", "kg/cm²"],
            ["Resistencia del acero (fy)", f"{datos_entrada.get('f_y', 0)}", "kg/cm²"],
            ["Luz libre de vigas", f"{datos_entrada.get('L_viga', 0)}", "m"],
            ["Número de pisos", f"{datos_entrada.get('num_pisos', 0)}", ""],
            ["Carga Muerta", f"{datos_entrada.get('CM', 0)}", "kg/m²"],
            ["Carga Viva", f"{datos_entrada.get('CV', 0)}", "kg/m²"]
        ]
        
        tabla = Table(datos_tabla, colWidths=[200, 100, 80])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), (173/255, 216/255, 230/255)),  # light blue
            ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # black
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(tabla)
        elements.append(Spacer(1, 20))
        
        # Resultados calculados
        elements.append(Paragraph("2. RESULTADOS CALCULADOS", styleH))
        if resultados:
            resultados_tabla = [
                ["Resultado", "Valor", "Unidad"],
                ["Peso total estimado", f"{resultados.get('peso_total', 0):.1f}", "ton"],
                ["Módulo de elasticidad del concreto", f"{resultados.get('Ec', 0):.0f}", "kg/cm²"],
                ["Módulo de elasticidad del acero", f"{resultados.get('Es', 0):,}", "kg/cm²"],
                ["Espesor de losa", f"{resultados.get('h_losa', 0)*100:.0f}", "cm"],
                ["Dimensiones de viga", f"{resultados.get('b_viga', 0):.0f}×{resultados.get('d_viga', 0):.0f}", "cm"],
                ["Dimensiones de columna", f"{resultados.get('lado_columna', 0):.0f}×{resultados.get('lado_columna', 0):.0f}", "cm"]
            ]
            
            tabla_resultados = Table(resultados_tabla, colWidths=[200, 100, 80])
            tabla_resultados.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), (144/255, 238/255, 144/255)),  # light green
                ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # black
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(tabla_resultados)
        
    else:
        # Reporte básico
        elements.append(Paragraph("RESULTADOS BÁSICOS", styleH))
        if resultados:
            elements.append(Paragraph(f"Peso total estimado: {resultados.get('peso_total', 0):.1f} ton", styleN))
            elements.append(Paragraph(f"Resistencia del concreto: {datos_entrada.get('f_c', 0)} kg/cm²", styleN))
            elements.append(Paragraph(f"Resistencia del acero: {datos_entrada.get('f_y', 0)} kg/cm²", styleN))
        elements.append(Paragraph("Este es un reporte básico del plan gratuito.", styleN))
    
    # Construir PDF
    doc.build(elements)
    pdf_buffer.seek(0)
    return pdf_buffer

# =====================
# FUNCIONES DE CÁLCULO
# =====================
def calcular_propiedades_concreto(fc):
    Ec = 15000 * sqrt(fc)
    ecu = 0.003
    fr = 2 * sqrt(fc)
    if fc <= 280:
        beta1 = 0.85
    else:
        beta1 = 0.85 - 0.05 * ((fc - 280) / 70)
        beta1 = max(beta1, 0.65)
    return {'Ec': Ec, 'ecu': ecu, 'fr': fr, 'beta1': beta1}

def calcular_propiedades_acero(fy):
    Es = 2000000
    ey = fy / Es
    return {'Es': Es, 'ey': ey}

def calcular_predimensionamiento(L_viga, num_pisos, num_vanos, CM, CV, fc, fy):
    h_losa = max(L_viga / 25, 0.17)
    d_viga = L_viga * 100 / 10
    b_viga = max(0.3 * d_viga, 25)
    P_servicio = num_pisos * (CM + 0.25*CV) * (L_viga*num_vanos)**2
    P_mayorada = num_pisos * (1.2*CM + 1.6*CV) * (L_viga*num_vanos)**2
    A_col_servicio = P_servicio / (0.45*fc)
    A_col_resistencia = P_mayorada / (0.65*0.8*fc)
    A_columna = max(A_col_servicio, A_col_resistencia)
    lado_columna = sqrt(A_columna)
    return {'h_losa': h_losa, 'd_viga': d_viga, 'b_viga': b_viga, 'lado_columna': lado_columna, 'A_columna': A_columna}

def calcular_diseno_flexion(fc, fy, b, d, Mu):
    """
    Calcula el diseño por flexión según ACI 318-2025
    """
    # Calcular β1
    if fc <= 280:
        beta1 = 0.85
    else:
        beta1 = 0.85 - 0.05 * ((fc - 280) / 70)
        beta1 = max(beta1, 0.65)
    
    # Cuantía balanceada
    rho_b = 0.85 * beta1 * (fc / fy) * (6000 / (6000 + fy))
    
    # Cuantía mínima
    rho_min = max(0.8 * sqrt(fc) / fy, 14 / fy)
    
    # Cuantía máxima
    rho_max = 0.75 * rho_b
    
    # Asumir cuantía inicial (entre mínima y máxima)
    rho = (rho_min + rho_max) / 2
    
    # Calcular área de acero
    As = rho * b * d
    
    # Calcular profundidad del bloque equivalente
    a = As * fy / (0.85 * fc * b)
    
    # Calcular momento resistente
    Mn = As * fy * (d - a/2)
    phi = 0.9
    phiMn = phi * Mn
    
    return {
        'beta1': beta1,
        'rho_b': rho_b,
        'rho_min': rho_min,
        'rho_max': rho_max,
        'rho': rho,
        'As': As,
        'a': a,
        'Mn': Mn,
        'phiMn': phiMn,
        'verificacion': phiMn >= Mu
    }

def calcular_diseno_cortante(fc, fy, bw, d, Vu):
    """
    Calcula el diseño por cortante según ACI 318-2025
    """
    # Resistencia del concreto
    Vc = 0.53 * sqrt(fc) * bw * d
    
    # Factor phi para cortante
    phi = 0.75
    
    # Verificar si se necesita refuerzo
    if Vu <= phi * Vc:
        Vs_requerido = 0
        Av_s_requerido = 0
        s_max = d/2
    else:
        Vs_requerido = (Vu / phi) - Vc
        # Calcular área de estribos requerida (asumiendo estribos #3)
        Av = 0.71  # cm² para estribo #3
        s_requerido = Av * fy * d / Vs_requerido
        s_max = min(d/2, 60)  # cm
        
        if s_requerido > s_max:
            # Usar estribos más grandes o más separados
            Av_s_requerido = Vs_requerido / (fy * d)
        else:
            Av_s_requerido = Av / s_requerido
    
    return {
        'Vc': Vc,
        'Vs_requerido': Vs_requerido,
        'Av_s_requerido': Av_s_requerido,
        's_max': s_max,
        'phi': phi,
        'verificacion': Vu <= phi * (Vc + Vs_requerido) if Vs_requerido > 0 else Vu <= phi * Vc
    }

def calcular_diseno_columna(fc, fy, Ag, Ast, Pu):
    """
    Calcula el diseño de columna según ACI 318-2025
    """
    # Resistencia nominal
    Pn = 0.80 * (0.85 * fc * (Ag - Ast) + fy * Ast)
    
    # Factor phi para columnas con estribos
    phi = 0.65
    
    # Resistencia de diseño
    phiPn = phi * Pn
    
    return {
        'Pn': Pn,
        'phiPn': phiPn,
        'phi': phi,
        'verificacion': Pu <= phiPn
    }

def calcular_analisis_sismico(zona_sismica, tipo_suelo, factor_importancia, peso_total):
    """
    Calcula análisis sísmico básico según E.030
    """
    # Factores según zona sísmica
    factores_zona = {
        "Z1": 0.10,
        "Z2": 0.15, 
        "Z3": 0.25,
        "Z4": 0.35
    }
    
    # Factores según tipo de suelo
    factores_suelo = {
        "S1": 0.8,
        "S2": 1.0,
        "S3": 1.2,
        "S4": 1.4
    }
    
    Z = factores_zona.get(zona_sismica, 0.25)
    S = factores_suelo.get(tipo_suelo, 1.0)
    U = factor_importancia
    
    # Coeficiente sísmico simplificado
    C = 2.5  # Valor típico para estructuras regulares
    R = 7.0  # Factor de reducción para pórticos
    
    # Cortante basal
    V = (Z * U * C * S / R) * peso_total * 1000  # Convertir a kg
    
    return {
        'Z': Z,
        'S': S,
        'U': U,
        'C': C,
        'R': R,
        'V': V,
        'cortante_basal_ton': V / 1000
    }

# =====================
# INTERFAZ STREAMLIT
# =====================

# Configuración de la página
st.set_page_config(
    page_title="CONSORCIO DEJ - Análisis Estructural",
    page_icon="🏗️",
    layout="wide"
)

# Header con fondo amarillo
st.markdown("""
<div style="text-align: center; padding: 20px; background-color: #FFD700; color: #2F2F2F; border-radius: 10px; margin-bottom: 20px; border: 2px solid #FFA500;">
    <h1>🏗️ CONSORCIO DEJ</h1>
    <p style="font-size: 18px; font-weight: bold;">Ingeniería y Construcción</p>
    <p style="font-size: 14px;">Software de Análisis Estructural Profesional</p>
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
        st.write("❌ Sin reportes PDF")
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
        st.write("✅ Reportes PDF")
        st.write("✅ Gráficos avanzados")
        st.write("✅ Fórmulas de diseño")
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
    st.title("🏗️ CONSORCIO DEJ - Análisis Estructural")
    
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
                        else:
                            st.error("❌ " + result["message"])
    
    with tab3:
        show_pricing_page()

# Verificar estado de autenticación
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Definir opción por defecto
opcion = "🏗️ Cálculo Básico"

if not st.session_state['logged_in']:
    show_auth_page()
    st.stop()
else:
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

    # Sidebar para navegación
    st.sidebar.title("📋 Menú Principal")
    
    # Mostrar plan actual
    if st.session_state['plan'] == "gratuito":
        st.sidebar.info("🆓 Plan Gratuito - Funciones limitadas")
        st.sidebar.write("Para acceder a todas las funciones, actualiza a Premium")
        
        # Información sobre cómo acceder al plan premium
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔑 Acceso Premium")
        st.sidebar.write("**Usuario:** admin")
        st.sidebar.write("**Contraseña:** admin123")
        st.sidebar.info("Cierra sesión y vuelve a iniciar con las credenciales admin")
    else:
        st.sidebar.success("⭐ Plan Premium - Acceso completo")
        
        # Información para administradores
        st.sidebar.markdown("---")
        st.sidebar.subheader("👨‍💼 Panel de Administrador")
        st.sidebar.write("**Usuario actual:** " + st.session_state['user'])
        st.sidebar.write("**Plan:** Premium")
        st.sidebar.success("Acceso completo a todas las funciones")
    
    opcion = st.sidebar.selectbox("Selecciona una opción", 
                                 ["🏗️ Cálculo Básico", "📊 Análisis Completo", "📄 Generar Reporte", "📚 Fórmulas de Diseño Estructural", "📈 Gráficos", "ℹ️ Acerca de", "✉️ Contacto"])
    
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
    
    st.sidebar.markdown("---")
    st.sidebar.header("📋 Datos del Proyecto")
    f_c = st.sidebar.number_input("f'c (kg/cm²)", 175, 700, 210, 10)
    f_y = st.sidebar.number_input("fy (kg/cm²)", 2800, 6000, 4200, 100)
    L_viga = st.sidebar.number_input("Luz libre de vigas (m)", 3.0, 15.0, 6.0, 0.5)
    h_piso = st.sidebar.number_input("Altura de piso (m)", 2.5, 5.0, 3.0, 0.1)
    num_pisos = st.sidebar.number_input("Número de pisos", 1, 100, 15, 1)
    num_vanos = st.sidebar.number_input("Número de vanos", 1, 20, 3, 1)
    CM = st.sidebar.number_input("Carga Muerta (kg/m²)", 100, 2000, 150, 50)
    CV = st.sidebar.number_input("Carga Viva (kg/m²)", 100, 1000, 200, 50)
    zona_sismica = st.sidebar.selectbox("Zona Sísmica", ["Z1", "Z2", "Z3", "Z4"], 2)
    tipo_suelo = st.sidebar.selectbox("Tipo de Suelo", ["S1", "S2", "S3", "S4"], 1)
    tipo_estructura = st.sidebar.selectbox("Tipo de Sistema Estructural", ["Pórticos", "Muros Estructurales", "Dual"], 0)
    factor_importancia = st.sidebar.number_input("Factor de Importancia (U)", 1.0, 1.5, 1.0, 0.1)

    # =====================
    # MENÚ PRINCIPAL
    # =====================
    if opcion == "🏗️ Cálculo Básico":
        st.title("Cálculo Básico de Análisis Estructural")
        st.info("Plan gratuito: Cálculos básicos de análisis estructural")
    
    # Pestañas para diferentes tipos de cálculos
    tab1, tab2, tab3 = st.tabs(["📏 Propiedades", "🏗️ Materiales", "⚖️ Cargas"])
    
    with tab1:
        st.subheader("Propiedades del Proyecto")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Resistencia del concreto (f'c):** {f_c} kg/cm²")
            st.write(f"**Resistencia del acero (fy):** {f_y} kg/cm²")
            st.write(f"**Luz libre de vigas:** {L_viga} m")
        with col2:
            st.write(f"**Altura de piso:** {h_piso} m")
            st.write(f"**Número de pisos:** {num_pisos}")
            st.write(f"**Número de vanos:** {num_vanos}")
    
    with tab2:
        st.subheader("Propiedades de los Materiales")
        col1, col2 = st.columns(2)
        with col1:
            props_concreto = calcular_propiedades_concreto(f_c)
            st.write(f"**Módulo de elasticidad del concreto (Ec):** {props_concreto['Ec']:.0f} kg/cm²")
            st.write(f"**Deformación última del concreto (εcu):** {props_concreto['ecu']}")
            st.write(f"**Resistencia a tracción (fr):** {props_concreto['fr']:.1f} kg/cm²")
        with col2:
            props_acero = calcular_propiedades_acero(f_y)
            st.write(f"**Módulo de elasticidad del acero (Es):** {props_acero['Es']:,} kg/cm²")
            st.write(f"**Deformación de fluencia (εy):** {props_acero['ey']:.4f}")
            st.write(f"**β1:** {props_concreto['beta1']:.3f}")
    
    with tab3:
        st.subheader("Cargas y Factores de Seguridad")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Carga Muerta:** {CM} kg/m²")
            st.write(f"**Carga Viva:** {CV} kg/m²")
            st.write(f"**Zona Sísmica:** {zona_sismica}")
        with col2:
            st.write(f"**Tipo de Suelo:** {tipo_suelo}")
            st.write(f"**Tipo de Estructura:** {tipo_estructura}")
            st.write(f"**Factor de Importancia:** {factor_importancia}")
    
    # Botón para calcular
    if st.button("🚀 Calcular Análisis Básico", type="primary"):
        # Cálculos básicos
        peso_total = float(num_pisos) * float(L_viga) * float(num_vanos) * float(h_piso) * float(f_c) / 1000
        
        # Guardar resultados básicos
        st.session_state['resultados_basicos'] = {
            'peso_total': peso_total,
            'f_c': f_c,
            'f_y': f_y,
            'L_viga': L_viga,
            'num_pisos': num_pisos,
            'CM': CM,
            'CV': CV,
            'zona_sismica': zona_sismica,
            'tipo_suelo': tipo_suelo,
            'tipo_estructura': tipo_estructura,
            'Ec': props_concreto['Ec'],
            'Es': props_acero['Es'],
            'ecu': props_concreto['ecu'],
            'fr': props_concreto['fr'],
            'beta1': props_concreto['beta1'],
            'ey': props_acero['ey']
        }
        
        st.success("¡Cálculos básicos completados exitosamente!")
        st.balloons()
        
        # MOSTRAR RESULTADOS INMEDIATAMENTE DESPUÉS DEL CÁLCULO
        st.subheader("📊 Resultados del Cálculo Básico")
        
        # Mostrar resultados en columnas
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Peso Total Estimado", f"{peso_total:.1f} ton")
            st.metric("Módulo de Elasticidad del Concreto", f"{props_concreto['Ec']:.0f} kg/cm²")
            st.metric("Módulo de Elasticidad del Acero", f"{props_acero['Es']:,} kg/cm²")
            st.metric("Resistencia a Tracción", f"{props_concreto['fr']:.1f} kg/cm²")
        
        with col2:
            st.metric("Deformación Última del Concreto", f"{props_concreto['ecu']}")
            st.metric("Deformación de Fluencia", f"{props_acero['ey']:.4f}")
            st.metric("β1", f"{props_concreto['beta1']:.3f}")
            st.metric("Altura Total", f"{float(num_pisos) * float(h_piso):.1f} m")
        
        # Análisis de estabilidad
        st.subheader("🔍 Análisis de Estabilidad")
        if peso_total < 1000:
            st.success(f"✅ El peso total es aceptable (FS = {peso_total:.1f} ton < 1000 ton)")
        else:
            st.warning(f"⚠️ El peso total es alto (FS = {peso_total:.1f} ton > 1000 ton) - Revisar dimensiones")
        
        # Gráfico básico
        st.subheader("📈 Gráfico de Propiedades")
        datos = pd.DataFrame({
            'Propiedad': ['Ec (kg/cm²)', 'Es (kg/cm²)', 'fr (kg/cm²)', 'β1'],
            'Valor': [props_concreto['Ec']/1000, props_acero['Es']/1000000, props_concreto['fr'], props_concreto['beta1']]
        })
        
        # Gráfico de barras mejorado
        if PLOTLY_AVAILABLE:
            fig = px.bar(datos, x='Propiedad', y='Valor', 
                        title="Propiedades de los Materiales - Plan Gratuito",
                        color='Propiedad',
                        color_discrete_map={
                            'Ec (kg/cm²)': '#2E8B57', 
                            'Es (kg/cm²)': '#DC143C', 
                            'fr (kg/cm²)': '#4169E1',
                            'β1': '#FFD700'
                        })
            
            # Personalizar el gráfico
            fig.update_layout(
                xaxis_title="Propiedad",
                yaxis_title="Valor",
                showlegend=True,
                height=400
            )
            
            # Agregar valores en las barras
            fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Gráfico alternativo con matplotlib
            if MATPLOTLIB_AVAILABLE:
                fig, ax = plt.subplots(figsize=(10, 6))
                bars = ax.bar(datos['Propiedad'], datos['Valor'], 
                             color=['#2E8B57', '#DC143C', '#4169E1', '#FFD700'])
                ax.set_title("Propiedades de los Materiales - Plan Gratuito")
                ax.set_xlabel("Propiedad")
                ax.set_ylabel("Valor")
                
                # Agregar valores en las barras
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{height:.2f}', ha='center', va='bottom')
                
                st.pyplot(fig)
            else:
                st.info("📊 Gráfico no disponible - Matplotlib no está instalado")
                st.write("Para ver gráficos, instale matplotlib: `pip install matplotlib`")

elif opcion == "📊 Análisis Completo":
    # Verificar acceso basado en plan del usuario
    user_plan = st.session_state.get('plan', 'gratuito')
    user_email = st.session_state.get('user', '')
    
    # Verificar si es admin (acceso completo)
    is_admin = user_email == 'admin' or user_email == 'admin@consorciodej.com'
    
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
        st.title("📊 Análisis Completo de Estructuras")
        st.success("⭐ Plan Premium: Análisis completo con todas las verificaciones")
        
        # Datos de entrada completos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Propiedades del Concreto")
            st.write(f"**Resistencia del concreto (f'c):** {f_c} kg/cm²")
            st.write(f"**Resistencia del acero (fy):** {f_y} kg/cm²")
            st.write(f"**Luz libre de vigas:** {L_viga} m")
            st.write(f"**Altura de piso:** {h_piso} m")
            
            st.subheader("Dimensiones del Proyecto")
            st.write(f"**Número de pisos:** {num_pisos}")
            st.write(f"**Número de vanos:** {num_vanos}")
            st.write(f"**Carga Muerta:** {CM} kg/m²")
            st.write(f"**Carga Viva:** {CV} kg/m²")
            
        with col2:
            st.subheader("Factores de Diseño")
            st.write(f"**Zona Sísmica:** {zona_sismica}")
            st.write(f"**Tipo de Suelo:** {tipo_suelo}")
            st.write(f"**Tipo de Estructura:** {tipo_estructura}")
            st.write(f"**Factor de Importancia:** {factor_importancia}")
            
            st.subheader("Información Adicional")
            st.info("El análisis completo incluye:")
            st.write("✅ Cálculo de propiedades de materiales")
            st.write("✅ Predimensionamiento automático")
            st.write("✅ Verificaciones de estabilidad")
            st.write("✅ Gráficos interactivos")
            st.write("✅ Reportes técnicos detallados")
        
        # Botón para ejecutar análisis completo
        if st.button("🔬 Ejecutar Análisis Completo", type="primary"):
            # Cálculos completos
            props_concreto = calcular_propiedades_concreto(f_c)
            props_acero = calcular_propiedades_acero(f_y)
            predim = calcular_predimensionamiento(L_viga, num_pisos, num_vanos, CM, CV, f_c, f_y)
            
            # Calcular peso total
            peso_total = float(num_pisos) * float(L_viga) * float(num_vanos) * float(h_piso) * float(f_c) / 1000
            
            # CÁLCULOS DE DISEÑO ESTRUCTURAL SEGÚN ACI 318-2025
            
            # 1. Diseño por Flexión
            # Momento último estimado para viga típica
            Mu_estimado = (1.2 * CM + 1.6 * CV) * L_viga**2 / 8 * 1000  # kg·m
            diseno_flexion = calcular_diseno_flexion(f_c, f_y, predim['b_viga'], predim['d_viga'], Mu_estimado)
            
            # 2. Diseño por Cortante
            # Cortante último estimado
            Vu_estimado = (1.2 * CM + 1.6 * CV) * L_viga / 2 * 1000  # kg
            diseno_cortante = calcular_diseno_cortante(f_c, f_y, predim['b_viga'], predim['d_viga'], Vu_estimado)
            
            # 3. Diseño de Columna
            # Carga axial última estimada
            Pu_estimado = peso_total * 1000 / num_vanos  # kg por columna
            Ag_columna = predim['lado_columna']**2  # cm²
            Ast_columna = 0.01 * Ag_columna  # 1% de acero inicial
            diseno_columna = calcular_diseno_columna(f_c, f_y, Ag_columna, Ast_columna, Pu_estimado)
            
            # 4. Análisis Sísmico
            analisis_sismico = calcular_analisis_sismico(zona_sismica, tipo_suelo, factor_importancia, peso_total)
            
            # Guardar resultados completos
            resultados_completos = {
                'peso_total': peso_total,
                'Ec': props_concreto['Ec'],
                'Es': props_acero['Es'],
                'h_losa': predim['h_losa'],
                'b_viga': predim['b_viga'],
                'd_viga': predim['d_viga'],
                'lado_columna': predim['lado_columna'],
                'ecu': props_concreto['ecu'],
                'fr': props_concreto['fr'],
                'beta1': props_concreto['beta1'],
                'ey': props_acero['ey'],
                # Resultados de diseño estructural
                'diseno_flexion': diseno_flexion,
                'diseno_cortante': diseno_cortante,
                'diseno_columna': diseno_columna,
                'analisis_sismico': analisis_sismico,
                'Mu_estimado': Mu_estimado,
                'Vu_estimado': Vu_estimado,
                'Pu_estimado': Pu_estimado
            }
            
            # Guardar datos de entrada
            datos_entrada = {
                'f_c': f_c,
                'f_y': f_y,
                'L_viga': L_viga,
                'num_pisos': num_pisos,
                'CM': CM,
                'CV': CV,
                'zona_sismica': zona_sismica,
                'tipo_suelo': tipo_suelo,
                'tipo_estructura': tipo_estructura
            }
            
            # Guardar en session state
            st.session_state['resultados_completos'] = resultados_completos
            st.session_state['datos_entrada'] = datos_entrada
            
            st.success("¡Análisis completo ejecutado exitosamente!")
            st.balloons()
            
            # MOSTRAR RESULTADOS COMPLETOS INMEDIATAMENTE
            st.subheader("📊 Resultados del Análisis Completo")
            
            # Mostrar resultados en columnas
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Peso Total Estimado", f"{peso_total:.1f} ton")
                st.metric("Módulo de Elasticidad del Concreto", f"{props_concreto['Ec']:.0f} kg/cm²")
                st.metric("Módulo de Elasticidad del Acero", f"{props_acero['Es']:,} kg/cm²")
                st.metric("Deformación Última del Concreto", f"{props_concreto['ecu']}")
                st.metric("Resistencia a Tracción", f"{props_concreto['fr']:.1f} kg/cm²")
            
            with col2:
                st.metric("β1", f"{props_concreto['beta1']:.3f}")
                st.metric("Deformación de Fluencia", f"{props_acero['ey']:.4f}")
                st.metric("Espesor de Losa", f"{predim['h_losa']*100:.0f} cm")
                st.metric("Dimensiones de Viga", f"{predim['b_viga']:.0f}×{predim['d_viga']:.0f} cm")
                st.metric("Dimensiones de Columna", f"{predim['lado_columna']:.0f}×{predim['lado_columna']:.0f} cm")
            
            # Análisis de estabilidad
            st.subheader("🔍 Análisis de Estabilidad")
            
            # Verificaciones básicas
            if peso_total < 1000:
                st.success(f"✅ Peso total aceptable: {peso_total:.1f} ton")
            else:
                st.warning(f"⚠️ Peso total alto: {peso_total:.1f} ton - Revisar dimensiones")
            
            if props_concreto['Ec'] > 200000:
                st.success(f"✅ Módulo de elasticidad del concreto adecuado: {props_concreto['Ec']:.0f} kg/cm²")
            else:
                st.info(f"ℹ️ Módulo de elasticidad del concreto: {props_concreto['Ec']:.0f} kg/cm²")
            
            # RESULTADOS DE DISEÑO ESTRUCTURAL SEGÚN ACI 318-2025
            st.subheader("🏗️ Resultados de Diseño Estructural (ACI 318-2025)")
            
            # Pestañas para diferentes tipos de diseño
            tab1, tab2, tab3, tab4 = st.tabs(["📐 Flexión", "🔧 Cortante", "🏢 Columnas", "🌍 Sísmico"])
            
            with tab1:
                st.markdown("### 📐 Diseño por Flexión")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Momento Último (Mu)", f"{resultados_completos['Mu_estimado']:.0f} kg·m")
                    st.metric("Cuantía Balanceada (ρb)", f"{diseno_flexion['rho_b']:.4f}")
                    st.metric("Cuantía Mínima (ρmin)", f"{diseno_flexion['rho_min']:.4f}")
                    st.metric("Cuantía Máxima (ρmax)", f"{diseno_flexion['rho_max']:.4f}")
                with col2:
                    st.metric("Área de Acero (As)", f"{diseno_flexion['As']:.1f} cm²")
                    st.metric("Profundidad Bloque (a)", f"{diseno_flexion['a']:.1f} cm")
                    st.metric("Momento Resistente (φMn)", f"{diseno_flexion['phiMn']:.0f} kg·m")
                    if diseno_flexion['verificacion']:
                        st.success("✅ Verificación de flexión: CUMPLE")
                    else:
                        st.error("❌ Verificación de flexión: NO CUMPLE")
            
            with tab2:
                st.markdown("### 🔧 Diseño por Cortante")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Cortante Último (Vu)", f"{resultados_completos['Vu_estimado']:.0f} kg")
                    st.metric("Resistencia Concreto (Vc)", f"{diseno_cortante['Vc']:.0f} kg")
                    st.metric("Resistencia Acero (Vs)", f"{diseno_cortante['Vs_requerido']:.0f} kg")
                with col2:
                    st.metric("Área Estribos (Av/s)", f"{diseno_cortante['Av_s_requerido']:.3f} cm²/cm")
                    st.metric("Separación Máxima", f"{diseno_cortante['s_max']:.1f} cm")
                    if diseno_cortante['verificacion']:
                        st.success("✅ Verificación de cortante: CUMPLE")
                    else:
                        st.error("❌ Verificación de cortante: NO CUMPLE")
            
            with tab3:
                st.markdown("### 🏢 Diseño de Columnas")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Carga Axial Última (Pu)", f"{resultados_completos['Pu_estimado']:.0f} kg")
                    st.metric("Resistencia Nominal (Pn)", f"{diseno_columna['Pn']:.0f} kg")
                    st.metric("Resistencia Diseño (φPn)", f"{diseno_columna['phiPn']:.0f} kg")
                with col2:
                    st.metric("Área Total Columna", f"{Ag_columna:.0f} cm²")
                    st.metric("Área Acero Columna", f"{Ast_columna:.1f} cm²")
                    if diseno_columna['verificacion']:
                        st.success("✅ Verificación de columna: CUMPLE")
                    else:
                        st.error("❌ Verificación de columna: NO CUMPLE")
            
            with tab4:
                st.markdown("### 🌍 Análisis Sísmico (E.030)")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Factor Zona (Z)", f"{analisis_sismico['Z']:.2f}")
                    st.metric("Factor Suelo (S)", f"{analisis_sismico['S']:.1f}")
                    st.metric("Factor Importancia (U)", f"{analisis_sismico['U']:.1f}")
                with col2:
                    st.metric("Coeficiente Sísmico (C)", f"{analisis_sismico['C']:.1f}")
                    st.metric("Factor Reducción (R)", f"{analisis_sismico['R']:.1f}")
                    st.metric("Cortante Basal (V)", f"{analisis_sismico['cortante_basal_ton']:.1f} ton")
            
            # Gráfico de resultados
            if PLOTLY_AVAILABLE:
                st.subheader("📈 Gráfico de Resultados")
                datos_grafico = pd.DataFrame({
                    'Propiedad': ['Peso Total (ton)', 'Ec (kg/cm²)', 'Es (kg/cm²)', 'Espesor Losa (cm)'],
                    'Valor': [peso_total, props_concreto['Ec']/1000, props_acero['Es']/1000000, predim['h_losa']*100]
                })
                
                fig = px.bar(datos_grafico, x='Propiedad', y='Valor', 
                            title="Resultados del Análisis Completo - Plan Premium",
                            color='Propiedad',
                            color_discrete_map={
                                'Peso Total (ton)': '#2E8B57',
                                'Ec (kg/cm²)': '#4169E1',
                                'Es (kg/cm²)': '#DC143C',
                                'Espesor Losa (cm)': '#FFD700'
                            })
                
                fig.update_layout(
                    xaxis_title="Propiedad",
                    yaxis_title="Valor",
                    height=400
                )
                
                fig.update_traces(texttemplate='%{y:.1f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Gráfico alternativo con matplotlib
                st.subheader("📈 Gráfico de Resultados")
                if MATPLOTLIB_AVAILABLE:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    propiedades = ['Peso Total', 'Ec', 'Es', 'Espesor Losa']
                    valores = [peso_total, props_concreto['Ec']/1000, props_acero['Es']/1000000, predim['h_losa']*100]
                    colors = ['#2E8B57', '#4169E1', '#DC143C', '#FFD700']
                    
                    bars = ax.bar(propiedades, valores, color=colors)
                    ax.set_title("Resultados del Análisis Completo - Plan Premium")
                    ax.set_ylabel("Valor")
                    
                    # Agregar valores en las barras
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                               f'{height:.1f}', ha='center', va='bottom')
                    
                    st.pyplot(fig)
                else:
                    st.info("📊 Gráfico no disponible - Matplotlib no está instalado")
                    st.write("Para ver gráficos, instale matplotlib: `pip install matplotlib`")

elif opcion == "📄 Generar Reporte":
    st.title("📄 Generar Reporte Técnico")
    
    if st.session_state['plan'] == "gratuito":
        if 'resultados_completos' in st.session_state:
            resultados = st.session_state['resultados_completos']
            
            # Reporte básico gratuito
            reporte_basico = f"""
# REPORTE BÁSICO - ANÁLISIS ESTRUCTURAL
## CONSORCIO DEJ
### Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}

### DATOS DE ENTRADA:
- Resistencia del concreto (f'c): {st.session_state.get('datos_entrada', {}).get('f_c', 0)} kg/cm²
- Resistencia del acero (fy): {st.session_state.get('datos_entrada', {}).get('f_y', 0)} kg/cm²
- Luz libre de vigas: {st.session_state.get('datos_entrada', {}).get('L_viga', 0)} m
- Número de pisos: {st.session_state.get('datos_entrada', {}).get('num_pisos', 0)}
- Carga Muerta: {st.session_state.get('datos_entrada', {}).get('CM', 0)} kg/m²
- Carga Viva: {st.session_state.get('datos_entrada', {}).get('CV', 0)} kg/m²

### RESULTADOS DEL ANÁLISIS:
- Peso total estimado: {resultados.get('peso_total', 0):.1f} ton
- Módulo de elasticidad del concreto: {resultados.get('Ec', 0):.0f} kg/cm²
- Módulo de elasticidad del acero: {resultados.get('Es', 0):,} kg/cm²
- Espesor de losa: {resultados.get('h_losa', 0)*100:.0f} cm
- Dimensiones de viga: {resultados.get('b_viga', 0):.0f}×{resultados.get('d_viga', 0):.0f} cm
- Dimensiones de columna: {resultados.get('lado_columna', 0):.0f}×{resultados.get('lado_columna', 0):.0f} cm

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
                    file_name=f"reporte_basico_analisis_estructural_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
            
            with col2:
                # Generar PDF básico
                pdf_buffer = generar_pdf_reportlab(resultados, st.session_state.get('datos_entrada', {}), "gratuito")
                st.download_button(
                    label="📄 Descargar PDF",
                    data=pdf_buffer.getvalue(),
                    file_name=f"reporte_basico_analisis_estructural_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
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
            st.warning("⚠️ No hay resultados disponibles. Realiza primero el análisis completo.")
    else:
        # Reporte premium completo
        if 'resultados_completos' in st.session_state:
            resultados = st.session_state['resultados_completos']
            datos_entrada = st.session_state.get('datos_entrada', {})
            
            reporte_premium = f"""
# REPORTE TÉCNICO COMPLETO - ANÁLISIS ESTRUCTURAL
## CONSORCIO DEJ
### Análisis según ACI 318-2025 y E.060
### Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}

### 1. DATOS DE ENTRADA:
- Resistencia del concreto (f'c): {datos_entrada.get('f_c', 0)} kg/cm²
- Resistencia del acero (fy): {datos_entrada.get('f_y', 0)} kg/cm²
- Luz libre de vigas: {datos_entrada.get('L_viga', 0)} m
- Número de pisos: {datos_entrada.get('num_pisos', 0)}
- Carga Muerta: {datos_entrada.get('CM', 0)} kg/m²
- Carga Viva: {datos_entrada.get('CV', 0)} kg/m²
- Zona Sísmica: {datos_entrada.get('zona_sismica', 'N/A')}
- Tipo de Suelo: {datos_entrada.get('tipo_suelo', 'N/A')}
- Tipo de Estructura: {datos_entrada.get('tipo_estructura', 'N/A')}

### 2. PROPIEDADES DE LOS MATERIALES:
- Módulo de elasticidad del concreto (Ec): {resultados.get('Ec', 0):.0f} kg/cm²
- Módulo de elasticidad del acero (Es): {resultados.get('Es', 0):,} kg/cm²
- Deformación última del concreto (εcu): {resultados.get('ecu', 0)}
- Deformación de fluencia (εy): {resultados.get('ey', 0):.4f}
- Resistencia a tracción (fr): {resultados.get('fr', 0):.1f} kg/cm²
- β1: {resultados.get('beta1', 0):.3f}

### 3. DIMENSIONES CALCULADAS:
- Peso total estimado: {resultados.get('peso_total', 0):.1f} ton
- Espesor de losa: {resultados.get('h_losa', 0)*100:.0f} cm
- Dimensiones de viga: {resultados.get('b_viga', 0):.0f}×{resultados.get('d_viga', 0):.0f} cm
- Dimensiones de columna: {resultados.get('lado_columna', 0):.0f}×{resultados.get('lado_columna', 0):.0f} cm

### 4. VERIFICACIONES DE ESTABILIDAD:
- Peso total: {'✅ ACEPTABLE' if resultados.get('peso_total', 0) < 1000 else '⚠️ ALTO - Revisar dimensiones'}
- Módulo de elasticidad del concreto: {'✅ ADECUADO' if resultados.get('Ec', 0) > 200000 else 'ℹ️ NORMAL'}

### 5. RECOMENDACIONES TÉCNICAS:
- Verificar la capacidad portante del suelo en campo
- Revisar el diseño del refuerzo estructural según ACI 318-2025
- Considerar efectos sísmicos según la normativa local
- Realizar inspecciones periódicas durante la construcción
- Monitorear deformaciones durante el servicio

### 6. INFORMACIÓN DEL PROYECTO:
- Empresa: CONSORCIO DEJ
- Método de análisis: ACI 318-2025 y E.060
- Fecha de análisis: {datetime.now().strftime('%d/%m/%Y %H:%M')}
- Plan: Premium
- Software: Streamlit + Python

---
**Este reporte fue generado automáticamente por el sistema de análisis estructural de CONSORCIO DEJ.**
**Para consultas técnicas, contacte a nuestro equipo de ingeniería.**
"""
            
            st.text_area("Reporte Premium", reporte_premium, height=600)
            
            # Botones para el reporte premium
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="📥 Descargar TXT",
                    data=reporte_premium,
                    file_name=f"reporte_premium_analisis_estructural_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
            
            with col2:
                # Generar PDF premium
                if REPORTLAB_AVAILABLE:
                    try:
                        pdf_buffer = generar_pdf_reportlab(resultados, datos_entrada, "premium")
                        if pdf_buffer:
                            st.download_button(
                                label="📄 Descargar PDF Premium",
                                data=pdf_buffer.getvalue(),
                                file_name=f"reporte_premium_analisis_estructural_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                mime="application/pdf"
                            )
                        else:
                            st.error("⚠️ Error: No se pudo generar el PDF")
                    except Exception as e:
                        st.error(f"⚠️ Error generando PDF: {str(e)}")
                        st.info("🔧 Instale ReportLab: pip install reportlab")
                else:
                    st.error("⚠️ ReportLab no está instalado")
                    st.info("🔧 Para generar PDFs, instale ReportLab:")
                    st.code("pip install reportlab")
            
            with col3:
                if st.button("🖨️ Generar Reporte en Pantalla", type="primary"):
                    st.success("✅ Reporte técnico generado exitosamente")
                    st.balloons()
                    
                    # Mostrar el reporte en formato expandible
                    with st.expander("📋 VER REPORTE TÉCNICO COMPLETO", expanded=True):
                        st.markdown(reporte_premium)
        else:
            st.warning("⚠️ No hay resultados disponibles. Realiza primero el análisis completo.")

elif opcion == "📚 Fórmulas de Diseño Estructural":
    st.header("📚 Fórmulas de Diseño Estructural")
    st.info("Fórmulas clave según ACI 318-2025, E.060, Nilson, McCormac, Hibbeler y Antonio Blanco.")
    
    # Pestañas para organizar las fórmulas
    tab1, tab2, tab3, tab4 = st.tabs(["🏗️ Propiedades Materiales", "📐 Diseño por Flexión", "🔧 Diseño por Cortante", "🏢 Columnas y Losas"])
    
    with tab1:
        st.subheader("🏗️ Propiedades del Material")
        st.markdown("""
        ### Concreto (ACI 318-2025 - Capítulo 19)
        - **Resistencia a compresión (f'c):** \( f'_c \) (kg/cm²)  
          *(Valores típicos: 210, 280, 350 kg/cm²)*
        
        - **Módulo de elasticidad (Ec):** \( E_c = 15000 \sqrt{f'_c} \) (kg/cm²)
        
        - **Deformación última del concreto (εcu):** \( \varepsilon_{cu} = 0.003 \) *(Para diseño por flexión)*
        
        - **Resistencia a tracción por flexión (fr):** \( f_r = 2 \sqrt{f'_c} \) (kg/cm²)
        
        ### Acero de Refuerzo (ACI 318-2025 - Capítulo 20)
        - **Esfuerzo de fluencia (fy):** \( f_y \) (kg/cm²)  
          *(Valores típicos: 4200, 5000 kg/cm²)*
        
        - **Módulo de elasticidad (Es):** \( E_s = 2,000,000 \) (kg/cm²)
        
        - **Deformación de fluencia (εy):** \( \varepsilon_y = \frac{f_y}{E_s} \)
        """, unsafe_allow_html=True)
        
        # Fórmulas en LaTeX
        st.latex(r"E_c = 15000 \sqrt{f'_c} \text{ (kg/cm²)}")
        st.latex(r"\varepsilon_{cu} = 0.003")
        st.latex(r"f_r = 2 \sqrt{f'_c} \text{ (kg/cm²)}")
        st.latex(r"E_s = 2,000,000 \text{ (kg/cm²)}")
        st.latex(r"\varepsilon_y = \frac{f_y}{E_s}")
    
    with tab2:
        st.subheader("📐 Diseño por Flexión (ACI 318-2025 - Capítulo 9)")
        st.markdown("""
        - **Momento último (Mu):** \( M_u = 1.2M_D + 1.6M_L \) *(Combinación de carga mayorada)*
        
        - **Cuantía de acero (ρ):** \( \rho = \frac{A_s}{bd} \)
        
        - **Cuantía balanceada (ρb):** \( \rho_b = 0.85\beta_1 \frac{f'_c}{f_y} \left( \frac{6000}{6000+f_y} \right) \)  
          *(β₁ = 0.85 si f'c ≤ 280 kg/cm², disminuye 0.05 por cada 70 kg/cm² adicionales)*
        
        - **Cuantía mínima (ρmin):** \( \rho_{min} = \max\left( \frac{0.8\sqrt{f'_c}}{f_y}, \frac{14}{f_y} \right) \)
        
        - **Cuantía máxima (ρmax):** \( \rho_{max} = 0.75\rho_b \) *(Para evitar falla frágil)*
        
        - **Profundidad del bloque equivalente (a):** \( a = \frac{A_s f_y}{0.85f'_c b} \)
        
        - **Momento resistente (φMn):** \( \phi M_n = \phi A_s f_y \left(d - \frac{a}{2}\right) \)  
          *(φ = 0.9 para flexión)*
        """, unsafe_allow_html=True)
        
        # Fórmulas en LaTeX
        st.latex(r"M_u = 1.2M_D + 1.6M_L")
        st.latex(r"\rho = \frac{A_s}{bd}")
        st.latex(r"\rho_b = 0.85\beta_1 \frac{f'_c}{f_y} \left( \frac{6000}{6000+f_y} \right)")
        st.latex(r"\rho_{min} = \max\left( \frac{0.8\sqrt{f'_c}}{f_y}, \frac{14}{f_y} \right)")
        st.latex(r"\rho_{max} = 0.75\rho_b")
        st.latex(r"a = \frac{A_s f_y}{0.85f'_c b}")
        st.latex(r"\phi M_n = \phi A_s f_y \left(d - \frac{a}{2}\right)")
    
    with tab3:
        st.subheader("🔧 Diseño por Cortante (ACI 318-2025 - Capítulo 22)")
        st.markdown("""
        - **Cortante último (Vu):** \( V_u = 1.2V_D + 1.6V_L \)
        
        - **Resistencia del concreto (Vc):** \( V_c = 0.53\sqrt{f'_c} b_w d \) (kg)
        
        - **Resistencia del acero (Vs):** \( V_s = \frac{A_v f_y d}{s} \)  
          *(Av = Área de estribos, s = separación)*
        
        - **Cortante máximo (Vs máx):** \( V_{s,max} = 2.1\sqrt{f'_c} b_w d \) *(Límite superior)*
        
        - **Separación máxima de estribos (smax):** \( s_{max} = \min\left( \frac{d}{2}, 60 \text{ cm} \right) \)
        """, unsafe_allow_html=True)
        
        # Fórmulas en LaTeX
        st.latex(r"V_u = 1.2V_D + 1.6V_L")
        st.latex(r"V_c = 0.53\sqrt{f'_c} b_w d \text{ (kg)}")
        st.latex(r"V_s = \frac{A_v f_y d}{s}")
        st.latex(r"V_{s,max} = 2.1\sqrt{f'_c} b_w d")
        st.latex(r"s_{max} = \min\left( \frac{d}{2}, 60 \text{ cm} \right)")
    
    with tab4:
        st.subheader("🏢 Diseño de Columnas y Losas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Columnas (ACI 318-2025 - Capítulo 10)
            - **Carga axial última (Pu):** \( P_u = 1.2P_D + 1.6P_L \)
            
            - **Resistencia nominal (Pn):** \( P_n = 0.80[0.85f'_c(A_g - A_{st}) + f_y A_{st}] \)  
              *(φ = 0.65 para columnas con estribos, 0.75 para espirales)*
            
            - **Relación de esbeltez:** \( \frac{kL}{r} \leq 22 \) *(Para columnas arriostradas)*
            """, unsafe_allow_html=True)
            
            st.latex(r"P_u = 1.2P_D + 1.6P_L")
            st.latex(r"P_n = 0.80[0.85f'_c(A_g - A_{st}) + f_y A_{st}]")
            st.latex(r"\frac{kL}{r} \leq 22")
        
        with col2:
            st.markdown("""
            ### Losas (ACI 318-2025 - Capítulo 8 & E.060)
            - **Espesor mínimo de losa aligerada:** \( h_{min} = \frac{L}{25} \) *(No menor a 17 cm)*
            
            - **Refuerzo mínimo en losas:** \( \rho_{min} = 0.0018 \) *(Para fy = 4200 kg/cm²)*
            
            - **Separación máxima del acero:** \( s_{max} = \min(3h, 45 \text{ cm}) \)
            """, unsafe_allow_html=True)
            
            st.latex(r"h_{min} = \frac{L}{25}")
            st.latex(r"\rho_{min} = 0.0018")
            st.latex(r"s_{max} = \min(3h, 45 \text{ cm})")
    
    # Sección adicional para análisis sísmico
    st.markdown("---")
    st.subheader("🌍 Análisis Sísmico (E.030 & ACI 318-2025 - Capítulo 18)")
    st.markdown("""
    - **Cortante basal (V):** \( V = \frac{ZUCS}{R}P \)  
      *(Z = factor de zona, U = importancia, C = coeficiente sísmico, S = suelo, R = reducción)*
    
    - **Deriva máxima permitida:** \( \Delta_{max} = 0.007h \) *(Para edificios regulares)*
    """, unsafe_allow_html=True)
    
    st.latex(r"V = \frac{ZUCS}{R}P")
    st.latex(r"\Delta_{max} = 0.007h")
    
    # Conclusiones
    st.markdown("---")
    st.subheader("📋 Conclusiones")
    st.markdown("""
    - **ACI 318-2025** es más estricto en cuantías mínimas y máximas.
    - **E.060** sigue principios similares pero con ajustes para condiciones locales.
    - **McCormac y Nilson** recomiendan ductilidad en zonas sísmicas (ρ ≤ 0.025).
    - **Hibbeler** enfatiza el análisis estructural previo al diseño.
    
    Este resumen integra los conceptos clave para el diseño seguro de estructuras de concreto armado según las normas internacionales y los libros de referencia. 🏗️
    """, unsafe_allow_html=True)
    
    # Fórmulas originales (mantener compatibilidad)
    st.markdown("---")
    st.subheader("📚 Fórmulas Clásicas (ACI 318-19)")
    st.info("Fórmulas clave según ACI 318-19, Nilson, McCormac, Hibbeler y Antonio Blanco.")
    st.markdown("""
    ### 1. Propiedades del Concreto y Acero
    - **Resistencia a la compresión del concreto (f'c):** Resistencia característica a 28 días (MPa o kg/cm²).
    - **Módulo de elasticidad del concreto (Ec):**
      
      \( E_c = 4700 \sqrt{f'_c} \) (MPa)  
      (ACI 318-19, Sección 19.2.2.1)
    - **Módulo de elasticidad del acero (Es):**
      
      \( E_s = 200,000 \) MPa (o \(2 \times 10^6\) kg/cm²)
    - **Deformación máxima del concreto en compresión (εcu):**
      
      \( \varepsilon_{cu} = 0.003 \) (ACI 318-19, Sección 22.2.2.1)

    ### 2. Flexión en Vigas (Diseño por Momento)
    - **Cuantía balanceada (ρb):**
      
      \( \rho_b = \frac{0.85 \beta_1 f'_c}{f_y} \left( \frac{600}{600+f_y} \right) \)
      
      \( \beta_1 = 0.85 \) si \(f'_c \leq 28\) MPa; se reduce en 0.05 por cada 7 MPa arriba de 28 MPa.
    - **Cuantía máxima (ρmax):**
      
      \( \rho_{max} = 0.75 \rho_b \) (ACI 318-19, Sección 9.3.3)
    - **Momento resistente nominal (Mn):**
      
      \( M_n = A_s f_y (d - \frac{a}{2}) \)
    - **Profundidad del bloque equivalente de esfuerzos (a):**
      
      \( a = \frac{A_s f_y}{0.85 f'_c b} \)
    - **Momento último (Mu):**
      
      \( M_u = \phi M_n \); \(\phi = 0.90\) para flexión

    ### 3. Corte en Vigas
    - **Resistencia al corte del concreto (Vc):**
      
      \( V_c = 0.17 \sqrt{f'_c} b_w d \) (MPa) (ACI 318-19, Sección 22.5.5.1)
    - **Resistencia del acero de estribos (Vs):**
      
      \( V_s = \frac{A_v f_y d}{s} \)
    - **Corte último (Vu):**
      
      \( V_u \leq \phi (V_c + V_s) \); \(\phi = 0.75\) para corte
    - **Separación máxima de estribos:**
      
      \( s_{max} = \begin{cases} 2d & \text{si } V_s \leq 0.33 \sqrt{f'_c} b_w d \\ 4d & \text{si } V_s > 0.33 \sqrt{f'_c} b_w d \end{cases} \)

    ### 4. Columnas (Compresión y Flexo-Compresión)
    - **Carga axial nominal (Pn):**
      
      \( P_n = 0.85 f'_c (A_g - A_{st}) + f_y A_{st} \) (Columna corta)
    - **Carga axial última (Pu):**
      
      \( P_u = \phi P_n \); \(\phi = 0.65\) (con estribos), \(0.75\) (espiral)
    - **Efectos de esbeltez (Klu/r):**
      
      Si \( \frac{Kl_u}{r} > 22 \), considerar efectos de segundo orden (ACI 318-19, Sección 6.2.5).

    ### 5. Losas Armadas en una Dirección
    - **Espesor mínimo (h):**
      
      \( h = \frac{L}{20} \) (simplemente apoyada) (ACI 318-19, Tabla 7.3.1.1)
    - **Refuerzo mínimo por temperatura:**
      
      \( A_{s,min} = 0.0018 b h \) (para \(f_y = 420\) MPa)

    ### 6. Adherencia y Anclaje
    - **Longitud de desarrollo (ld) para barras en tracción:**
      
      \( l_d = \left( \frac{f_y \psi_t \psi_e}{2.1 \lambda \sqrt{f'_c}} \right) d_b \) (ACI 318-19, Sección 25.4.2)
      
      \(\psi_t, \psi_e\): Factores por ubicación y recubrimiento.

    ### 7. Servicio (Agrietamiento y Deflexión)
    - **Control de agrietamiento:**
      
      \( w = 0.076 \beta_s \frac{d_c^3}{A} \) (MPa) (ACI 318-19, Sección 24.3)
      
      \(w\): Ancho de grieta, \(d_c\): Recubrimiento, \(A\): Área de concreto alrededor de la barra.

    ---
    **Fuentes:**
    - ACI 318-19: Requisitos generales y fórmulas base.
    - McCormac & Nilson: Detalles de diseño en flexión, corte y columnas.
    - Hibbeler: Análisis estructural previo al diseño.
    - Antonio Blanco: Aplicaciones en edificaciones.
    """, unsafe_allow_html=True)
    st.latex(r"E_c = 4700 \, \sqrt{f'_c} ")
    st.latex(r"E_s = 200000 \, \text{MPa}")
    st.latex(r"\varepsilon_{cu} = 0.003")
    st.latex(r"\rho_b = \frac{0.85 \beta_1 f'_c}{f_y} \left( \frac{600}{600+f_y} \right)")
    st.latex(r"\rho_{max} = 0.75 \rho_b")
    st.latex(r"M_n = A_s f_y (d - \frac{a}{2})")
    st.latex(r"a = \frac{A_s f_y}{0.85 f'_c b}")
    st.latex(r"M_u = \phi M_n; \, \phi = 0.90")
    st.latex(r"V_c = 0.17 \sqrt{f'_c} b_w d")
    st.latex(r"V_s = \frac{A_v f_y d}{s}")
    st.latex(r"V_u \leq \phi (V_c + V_s); \, \phi = 0.75")
    st.latex(r"s_{max} = \begin{cases} 2d & V_s \leq 0.33 \sqrt{f'_c} b_w d \\ 4d & V_s > 0.33 \sqrt{f'_c} b_w d \end{cases}")
    st.latex(r"P_n = 0.85 f'_c (A_g - A_{st}) + f_y A_{st}")
    st.latex(r"P_u = \phi P_n; \, \phi = 0.65, 0.75")
    st.latex(r"h = \frac{L}{20}")
    st.latex(r"A_{s,min} = 0.0018 b h")
    st.latex(r"l_d = \left( \frac{f_y \psi_t \psi_e}{2.1 \lambda \sqrt{f'_c}} \right) d_b")
    st.latex(r"w = 0.076 \beta_s \frac{d_c^3}{A}")
    st.latex(r"E_c = 4700 \, \sqrt{f'_c} ")
    st.latex(r"E_s = 200000 \, \text{MPa}")
    st.latex(r"\varepsilon_{cu} = 0.003")
    st.latex(r"\rho_b = \frac{0.85 \beta_1 f'_c}{f_y} \left( \frac{600}{600+f_y} \right)")
    st.latex(r"\rho_{max} = 0.75 \rho_b")
    st.latex(r"M_n = A_s f_y (d - \frac{a}{2})")
    st.latex(r"a = \frac{A_s f_y}{0.85 f'_c b}")
    st.latex(r"M_u = \phi M_n; \, \phi = 0.90")
    st.latex(r"V_c = 0.17 \sqrt{f'_c} b_w d")
    st.latex(r"V_s = \frac{A_v f_y d}{s}")
    st.latex(r"V_u \leq \phi (V_c + V_s); \, \phi = 0.75")
    st.latex(r"s_{max} = \begin{cases} 2d & V_s \leq 0.33 \sqrt{f'_c} b_w d \\ 4d & V_s > 0.33 \sqrt{f'_c} b_w d \end{cases}")
    st.latex(r"P_n = 0.85 f'_c (A_g - A_{st}) + f_y A_{st}")
    st.latex(r"P_u = \phi P_n; \, \phi = 0.65, 0.75")
    st.latex(r"h = \frac{L}{20}")
    st.latex(r"A_{s,min} = 0.0018 b h")
    st.latex(r"l_d = \left( \frac{f_y \psi_t \psi_e}{2.1 \lambda \sqrt{f'_c}} \right) d_b")
    st.latex(r"w = 0.076 \beta_s \frac{d_c^3}{A}")

elif opcion == "📈 Gráficos":
    st.title("📈 Gráficos y Visualizaciones")
    
    # Pestañas para diferentes tipos de gráficos
    tab1, tab2, tab3 = st.tabs(["📊 Gráficos Básicos", "🔧 Cortantes y Momentos (Nilson)", "📈 Gráficos Avanzados"])
    
    with tab1:
        st.subheader("📊 Gráficos Básicos")
        
        if st.session_state['plan'] == "gratuito":
            st.warning("⚠️ Esta función requiere plan premium. Actualiza tu cuenta para acceder a gráficos avanzados.")
            st.info("Plan gratuito incluye: Cálculos básicos, resultados simples")
            st.info("Plan premium incluye: Gráficos interactivos, visualizaciones avanzadas")
            
            # Mostrar botón para actualizar plan
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("⭐ Actualizar a Premium", type="primary", key="upgrade_graficos"):
                    st.session_state['show_pricing'] = True
                    st.rerun()
        else:
            # Gráficos premium
            if 'resultados_completos' in st.session_state:
                resultados = st.session_state['resultados_completos']
                
                # Gráfico de propiedades
                col1, col2 = st.columns(2)
                
                with col1:
                    if PLOTLY_AVAILABLE:
                        datos_propiedades = pd.DataFrame({
                            'Propiedad': ['Ec (kg/cm²)', 'Es (kg/cm²)', 'fr (kg/cm²)', 'β1'],
                            'Valor': [resultados.get('Ec', 0)/1000, resultados.get('Es', 0)/1000000, 
                                     resultados.get('fr', 0), resultados.get('beta1', 0)]
                        })
                        
                        fig1 = px.bar(datos_propiedades, x='Propiedad', y='Valor',
                                     title="Propiedades de los Materiales - Plan Premium",
                                     color='Propiedad',
                                     color_discrete_map={
                                         'Ec (kg/cm²)': '#4169E1',
                                         'Es (kg/cm²)': '#DC143C',
                                         'fr (kg/cm²)': '#32CD32',
                                         'β1': '#FFD700'
                                     })
                        
                        fig1.update_layout(
                            xaxis_title="Propiedad",
                            yaxis_title="Valor",
                            height=400
                        )
                        
                        fig1.update_traces(texttemplate='%{y:.2f}', textposition='outside')
                        st.plotly_chart(fig1, use_container_width=True)
                    else:
                        # Gráfico alternativo con matplotlib
                        try:
                            import matplotlib.pyplot as plt
                            import matplotlib
                            matplotlib.use('Agg')  # Backend no interactivo para Streamlit
                            fig1, ax1 = plt.subplots(figsize=(8, 6))
                            propiedades = ['Ec', 'Es', 'fr', 'β1']
                            valores = [resultados.get('Ec', 0)/1000, resultados.get('Es', 0)/1000000, 
                                      resultados.get('fr', 0), resultados.get('beta1', 0)]
                            colors = ['#4169E1', '#DC143C', '#32CD32', '#FFD700']
                            bars = ax1.bar(propiedades, valores, color=colors)
                            ax1.set_title("Propiedades de los Materiales - Plan Premium")
                            ax1.set_ylabel("Valor")
                            for bar in bars:
                                height = bar.get_height()
                                ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                                       f'{height:.2f}', ha='center', va='bottom')
                            st.pyplot(fig1)
                        except ImportError:
                            st.info("📊 Gráfico no disponible - Matplotlib no está instalado")
                            st.write("Para ver gráficos, instale matplotlib: `pip install matplotlib`")
                
                with col2:
                    # Gráfico de dimensiones
                    if PLOTLY_AVAILABLE:
                        datos_dimensiones = pd.DataFrame({
                            'Dimensión': ['Peso Total (ton)', 'Espesor Losa (cm)', 'Ancho Viga (cm)', 'Alto Viga (cm)'],
                            'Valor': [resultados.get('peso_total', 0), resultados.get('h_losa', 0)*100, 
                                     resultados.get('b_viga', 0), resultados.get('d_viga', 0)]
                        })
                        
                        fig2 = px.pie(datos_dimensiones, values='Valor', names='Dimensión',
                                     title="Distribución de Dimensiones - Plan Premium",
                                     color_discrete_map={
                                         'Peso Total (ton)': '#2E8B57',
                                         'Espesor Losa (cm)': '#FF6B6B',
                                         'Ancho Viga (cm)': '#4ECDC4',
                                         'Alto Viga (cm)': '#FFD93D'
                                     })
                        
                        fig2.update_traces(textposition='inside', textinfo='percent+label+value')
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        # Gráfico alternativo con matplotlib
                        if MATPLOTLIB_AVAILABLE:
                            fig2, ax2 = plt.subplots(figsize=(8, 8))
                            dimensiones = ['Peso Total', 'Espesor Losa', 'Ancho Viga', 'Alto Viga']
                            valores = [resultados.get('peso_total', 0), resultados.get('h_losa', 0)*100, 
                                      resultados.get('b_viga', 0), resultados.get('d_viga', 0)]
                            colors = ['#2E8B57', '#FF6B6B', '#4ECDC4', '#FFD93D']
                            
                            ax2.pie(valores, labels=dimensiones, autopct='%1.1f%%', colors=colors)
                            ax2.set_title("Distribución de Dimensiones - Plan Premium")
                            st.pyplot(fig2)
                        else:
                            st.info("📊 Gráfico no disponible - Matplotlib no está instalado")
                            st.write("Para ver gráficos, instale matplotlib: `pip install matplotlib`")
            else:
                st.warning("⚠️ No hay resultados disponibles. Realiza primero el análisis completo.")
    
    with tab2:
        st.subheader("🔧 Diagramas de Cortantes y Momentos - Jack C. McCormac")
        st.info("📚 Basado en 'Diseño de Estructuras de Concreto' de Jack C. McCormac")
        
        # Verificar si matplotlib está disponible
        if not MATPLOTLIB_AVAILABLE:
            st.error("❌ Matplotlib no está instalado. Para usar esta función, instale matplotlib:")
            st.code("pip install matplotlib")
            st.info("🔧 Después de instalar matplotlib, recarga la aplicación")
        else:
            # Seleccionar tipo de viga
            tipo_viga = st.selectbox(
                "Selecciona el tipo de viga:",
                ["Viga Simplemente Apoyada", "Viga Empotrada", "Viga Continua (2 tramos)"],
                help="Según Jack C. McCormac - Diseño de Estructuras de Concreto"
            )
            
            if tipo_viga == "Viga Simplemente Apoyada":
                st.markdown("### 📐 Viga Simplemente Apoyada")
                
                col1, col2 = st.columns(2)
                with col1:
                    L = st.number_input("Luz de la viga (m)", 1.0, 20.0, 6.0, 0.5)
                    w = st.number_input("Carga distribuida (kg/m)", 0.0, 10000.0, 1000.0, 100.0)
                
                with col2:
                    usar_carga_puntual = st.checkbox("Agregar carga puntual")
                    if usar_carga_puntual:
                        P = st.number_input("Carga puntual (kg)", 0.0, 50000.0, 5000.0, 500.0)
                        a = st.number_input("Distancia desde apoyo izquierdo (m)", 0.1, L-0.1, L/2, 0.1)
                    else:
                        P = None
                        a = None
                
                if st.button("🔬 Generar Diagramas", type="primary"):
                    fig = graficar_cortantes_momentos_mccormac(L, w, P, a, "simple")
                    if fig:
                        st.pyplot(fig)
                        
                        # Mostrar valores máximos
                        x, V, M = calcular_cortantes_momentos_viga_simple_mccormac(L, w, P, a)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Cortante Máximo", f"{max(abs(V)):.1f} kg")
                        with col2:
                            st.metric("Momento Máximo", f"{max(abs(M)):.1f} kg·m")
                        with col3:
                            st.metric("Luz de la Viga", f"{L} m")
            
            elif tipo_viga == "Viga Empotrada":
                st.markdown("### 🔒 Viga Empotrada")
                
                col1, col2 = st.columns(2)
                with col1:
                    L = st.number_input("Luz de la viga (m)", 1.0, 20.0, 6.0, 0.5, key="empotrada")
                    w = st.number_input("Carga distribuida (kg/m)", 0.0, 10000.0, 1000.0, 100.0, key="w_empotrada")
                
                with col2:
                    usar_carga_puntual = st.checkbox("Agregar carga puntual", key="puntual_empotrada")
                    if usar_carga_puntual:
                        P = st.number_input("Carga puntual (kg)", 0.0, 50000.0, 5000.0, 500.0, key="P_empotrada")
                        a = st.number_input("Distancia desde apoyo izquierdo (m)", 0.1, L-0.1, L/2, 0.1, key="a_empotrada")
                    else:
                        P = None
                        a = None
                
                if st.button("🔬 Generar Diagramas", type="primary", key="btn_empotrada"):
                    fig = graficar_cortantes_momentos_mccormac(L, w, P, a, "empotrada")
                    if fig:
                        st.pyplot(fig)
                        
                        # Mostrar valores máximos
                        x, V, M = calcular_cortantes_momentos_viga_empotrada_mccormac(L, w, P, a)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Cortante Máximo", f"{max(abs(V)):.1f} kg")
                        with col2:
                            st.metric("Momento Máximo", f"{max(abs(M)):.1f} kg·m")
                        with col3:
                            st.metric("Luz de la Viga", f"{L} m")
            
            elif tipo_viga == "Viga Continua (2 tramos)":
                st.markdown("### 🔗 Viga Continua de 2 Tramos")
                
                col1, col2 = st.columns(2)
                with col1:
                    L1 = st.number_input("Luz del primer tramo (m)", 1.0, 15.0, 5.0, 0.5)
                    L2 = st.number_input("Luz del segundo tramo (m)", 1.0, 15.0, 5.0, 0.5)
                
                with col2:
                    w1 = st.number_input("Carga distribuida tramo 1 (kg/m)", 0.0, 10000.0, 1000.0, 100.0)
                    w2 = st.number_input("Carga distribuida tramo 2 (kg/m)", 0.0, 10000.0, 1000.0, 100.0)
                
                if st.button("🔬 Generar Diagramas", type="primary", key="btn_continua"):
                    fig = graficar_viga_continua_mccormac(L1, L2, w1, w2)
                    if fig:
                        st.pyplot(fig)
                        
                        # Mostrar valores máximos
                        x1, V1, M1, x2, V2, M2, R_A, R_B1, R_B2, R_C, M_B = calcular_cortantes_momentos_viga_continua_mccormac(L1, L2, w1, w2)
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Cortante Máx. Tramo 1", f"{max(abs(V1)):.1f} kg")
                        with col2:
                            st.metric("Cortante Máx. Tramo 2", f"{max(abs(V2)):.1f} kg")
                        with col3:
                            st.metric("Momento Máx. Tramo 1", f"{max(abs(M1)):.1f} kg·m")
                        with col4:
                            st.metric("Momento Máx. Tramo 2", f"{max(abs(M2)):.1f} kg·m")
                        
                        # Mostrar reacciones
                        st.subheader("📊 Reacciones Calculadas")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Reacción A", f"{R_A:.1f} kg")
                        with col2:
                            st.metric("Reacción B1", f"{R_B1:.1f} kg")
                        with col3:
                            st.metric("Reacción B2", f"{R_B2:.1f} kg")
                        with col4:
                            st.metric("Reacción C", f"{R_C:.1f} kg")
            
            # Información técnica
            st.markdown("---")
            st.subheader("📚 Información Técnica - Jack C. McCormac")
            st.markdown("""
            **Referencia:** Diseño de Estructuras de Concreto - Jack C. McCormac
            
            **Fórmulas utilizadas:**
            - **Viga simplemente apoyada:** Reacciones R = wL/2, Momento máximo M = wL²/8
            - **Viga empotrada:** Momentos de empotramiento M = ±wL²/12
            - **Viga continua:** Método de coeficientes para momentos en apoyos
            
            **Aplicaciones:**
            - Diseño de vigas de concreto armado
            - Análisis de cargas distribuidas y puntuales
            - Verificación de momentos y cortantes máximos
            - Diseño de refuerzo según ACI 318
            """)
    
    with tab3:
        st.subheader("📈 Gráficos Avanzados")
        st.info("Esta sección incluye gráficos avanzados y visualizaciones 3D (disponible en plan empresarial)")
        
        if st.session_state['plan'] == "empresarial":
            st.success("🏢 Plan Empresarial: Acceso completo a gráficos avanzados")
            # Aquí se pueden agregar gráficos 3D y visualizaciones avanzadas
            st.info("🚧 Funcionalidad en desarrollo - Próximamente gráficos 3D y visualizaciones avanzadas")
        else:
            st.warning("⚠️ Esta función requiere plan empresarial")
            st.info("Actualiza a plan empresarial para acceder a gráficos 3D y visualizaciones avanzadas")

elif opcion == "ℹ️ Acerca de":
    st.title("ℹ️ Acerca de CONSORCIO DEJ")
    st.write("""
    ### 🏗️ CONSORCIO DEJ
    **Ingeniería y Construcción Especializada**
    
    Esta aplicación fue desarrollada para facilitar el análisis y diseño estructural
    utilizando métodos reconocidos en ingeniería civil.
    
    **Características del Plan Gratuito:**
    - ✅ Cálculos básicos de análisis estructural
    - ✅ Resultados simples con gráficos básicos
    - ✅ Reporte básico descargable
    - ✅ Análisis de propiedades de materiales
    
    **Características del Plan Premium:**
    - ⭐ Análisis completo con ACI 318-2025
    - ⭐ Cálculos de predimensionamiento automáticos
    - ⭐ **Reportes técnicos en PDF** (NUEVO)
    - ⭐ **Gráficos interactivos avanzados** (NUEVO)
    - ⭐ Verificaciones de estabilidad completas
    - ⭐ Fórmulas de diseño estructural detalladas
    
    **Desarrollado con:** Python, Streamlit, Plotly
    **Normativas:** ACI 318-2025, E.060, E.030
    """)

elif opcion == "✉️ Contacto":
    st.title("✉️ Contacto")
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
    - Análisis estructural
    - Diseño de estructuras
    - Ingeniería civil
    - Construcción especializada
    """)