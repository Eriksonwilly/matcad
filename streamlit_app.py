import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from math import sqrt
from datetime import datetime
import hashlib
import io
import base64
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ===== CONFIGURACIÓN PARA MÓVIL/APK =====
st.set_page_config(
    page_title="CONSORCIO DEJ - Análisis Estructural",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://consorciodej.com/help',
        'Report a bug': 'https://consorciodej.com/bug',
        'About': 'CONSORCIO DEJ v2.0 - Análisis Estructural Profesional'
    }
)

# CSS optimizado para móvil
st.markdown("""
<style>
    @media (max-width: 768px) {
        .main-header {
            padding: 15px !important;
            font-size: 18px !important;
        }
        .metric-card {
            padding: 15px !important;
            margin: 10px 0 !important;
        }
        .calculate-button {
            padding: 15px !important;
            margin: 20px 0 !important;
        }
    }
    
    .main-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #2F2F2F;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
    }
    .error-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 2px solid #dc3545;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
    }
    .calculate-button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    .section-header {
        background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ===== FUNCIONES DE CÁLCULO ACI 318-2025 =====
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

def calcular_cuantias_balanceada(fc, fy, beta1):
    rho_b = 0.85 * beta1 * (fc / fy) * (6000 / (6000 + fy))
    rho_min = max(0.8 * sqrt(fc) / fy, 14 / fy)
    rho_max = 0.75 * rho_b
    rho_max_mccormac = 0.025
    return {'rho_b': rho_b, 'rho_min': rho_min, 'rho_max': rho_max, 'rho_max_mccormac': rho_max_mccormac}

def calcular_diseno_flexion(Mu, b, d, fc, fy, beta1):
    phi = 0.9
    cuantias = calcular_cuantias_balanceada(fc, fy, beta1)
    a_estimado = d / 5
    As_estimado = Mu / (phi * fy * (d - a_estimado/2))
    a_real = (As_estimado * fy) / (0.85 * fc * b)
    As_corregido = Mu / (phi * fy * (d - a_real/2))
    rho_provisto = As_corregido / (b * d)
    cumple_cuantia_min = rho_provisto >= cuantias['rho_min']
    cumple_cuantia_max = rho_provisto <= cuantias['rho_max']
    cumple_mccormac = rho_provisto <= cuantias['rho_max_mccormac']
    Mn = As_corregido * fy * (d - a_real/2)
    phiMn = phi * Mn
    return {
        'As': As_corregido, 'a': a_real, 'rho_provisto': rho_provisto,
        'cumple_cuantia_min': cumple_cuantia_min, 'cumple_cuantia_max': cumple_cuantia_max,
        'cumple_mccormac': cumple_mccormac, 'Mn': Mn, 'phiMn': phiMn, 'cuantias': cuantias
    }

def calcular_diseno_cortante(Vu, b, d, fc, fy):
    phi_v = 0.75
    Vc = 0.53 * sqrt(fc) * b * d
    Vs_max = 2.1 * sqrt(fc) * b * d
    s_max = min(d/2, 60)
    requiere_acero = Vu > phi_v * Vc
    if requiere_acero:
        Vs_requerido = (Vu / phi_v) - Vc
        requiere_rediseno = Vs_requerido > Vs_max
    else:
        Vs_requerido = 0
        requiere_rediseno = False
    return {
        'Vc': Vc, 'Vs_max': Vs_max, 's_max': s_max, 'requiere_acero': requiere_acero,
        'Vs_requerido': Vs_requerido, 'requiere_rediseno': requiere_rediseno, 'phi_v': phi_v
    }

def calcular_diseno_columna(Pu, fc, fy, Ag, Ast=0):
    phi_col = 0.65
    rho_min_col = 0.01
    rho_max_col = 0.06
    As_min_col = rho_min_col * Ag
    As_max_col = rho_max_col * Ag
    Pn = 0.80 * (0.85 * fc * (Ag - Ast) + fy * Ast)
    phiPn = phi_col * Pn
    cumple_capacidad = Pu <= phiPn
    return {
        'Pn': Pn, 'phiPn': phiPn, 'As_min_col': As_min_col, 'As_max_col': As_max_col,
        'cumple_capacidad': cumple_capacidad, 'phi_col': phi_col
    }

def calcular_analisis_sismico(P_edificio, num_pisos, h_piso, zona_sismica, tipo_suelo, tipo_estructura, factor_importancia):
    factores_Z = {"Z1": 0.10, "Z2": 0.20, "Z3": 0.30, "Z4": 0.45}
    Z = factores_Z[zona_sismica]
    factores_R = {"Pórticos": 8.0, "Muros Estructurales": 6.0, "Dual": 7.0}
    R = factores_R[tipo_estructura]
    factores_S = {"S1": 1.0, "S2": 1.2, "S3": 1.4, "S4": 1.6}
    S = factores_S[tipo_suelo]
    T = 0.1 * num_pisos
    if tipo_suelo == "S1":
        C = 2.5 * (1.0/T)**0.8
    else:
        C = 2.5 * (1.0/T)
    V = (Z * factor_importancia * C * S * P_edificio) / R
    Fx = []
    sum_h = sum([i*h_piso for i in range(1, num_pisos+1)])
    for i in range(1, num_pisos+1):
        Fx.append(V * (i*h_piso)/sum_h)
    deriva_max = 0.007 * h_piso
    return {'T': T, 'C': C, 'V': V, 'Fx': Fx, 'deriva_max': deriva_max, 'Z': Z, 'R': R, 'S': S}

# ===== APLICACIÓN PRINCIPAL =====
def main():
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ CONSORCIO DEJ</h1>
        <p style="font-size: 20px; font-weight: bold;">Ingeniería y Construcción</p>
        <p style="font-size: 16px;">Software de Análisis Estructural Profesional</p>
        <p style="font-size: 14px;">ACI 318-2025 & E.060 | E.030</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar simplificado para móvil
    with st.sidebar:
        st.header("📊 Datos del Proyecto")
        
        # Materiales
        st.subheader("🏗️ Materiales")
        f_c = st.number_input("f'c (kg/cm²)", min_value=175, max_value=700, value=210, step=10)
        f_y = st.number_input("fy (kg/cm²)", min_value=2800, max_value=6000, value=4200, step=100)
        
        # Geometría
        st.subheader("📐 Geometría")
        L_viga = st.number_input("Luz libre (m)", min_value=3.0, max_value=15.0, value=6.0, step=0.5)
        h_piso = st.number_input("Altura piso (m)", min_value=2.5, max_value=5.0, value=3.0, step=0.1)
        num_pisos = st.number_input("Número de pisos", min_value=1, max_value=100, value=15, step=1)
        num_vanos = st.number_input("Número de vanos", min_value=1, max_value=20, value=3, step=1)
        
        # Cargas
        st.subheader("⚖️ Cargas")
        CM = st.number_input("Carga Muerta (kg/m²)", min_value=100, max_value=2000, value=150, step=50)
        CV = st.number_input("Carga Viva (kg/m²)", min_value=100, max_value=1000, value=200, step=50)
        
        # Parámetros sísmicos
        st.subheader("🌎 Sísmicos")
        zona_sismica = st.selectbox("Zona Sísmica", ["Z1", "Z2", "Z3", "Z4"], index=2)
        tipo_suelo = st.selectbox("Tipo de Suelo", ["S1", "S2", "S3", "S4"], index=1)
        tipo_estructura = st.selectbox("Sistema Estructural", ["Pórticos", "Muros Estructurales", "Dual"], index=0)
        factor_importancia = st.number_input("Factor de Importancia", min_value=1.0, max_value=1.5, value=1.0, step=0.1)
    
    # Área principal
    st.title("📊 Análisis Estructural Completo")
    
    # Botón de cálculo principal
    st.markdown("""
    <div class="calculate-button">
        <h2>🚀 CALCULAR TODO EL PROYECTO</h2>
        <p>Predimensionamiento • Análisis Sísmico • Diseño Estructural • Gráficas</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⚡ EJECUTAR ANÁLISIS COMPLETO", type="primary", use_container_width=True):
        with st.spinner('Calculando análisis estructural...'):
            # Calcular propiedades de materiales
            props_concreto = calcular_propiedades_concreto(f_c)
            props_acero = calcular_propiedades_acero(f_y)
            
            # Predimensionamiento
            h_losa = max(L_viga / 25, 0.17)
            d_viga = L_viga * 100 / 10
            b_viga = max(0.3 * d_viga, 25)
            P_servicio = num_pisos * (CM + 0.25*CV) * (L_viga*num_vanos)**2
            P_mayorada = num_pisos * (1.2*CM + 1.6*CV) * (L_viga*num_vanos)**2
            A_columna = max(P_servicio / (0.45*f_c), P_mayorada / (0.65*0.8*f_c))
            lado_columna = sqrt(A_columna)
            
            # Análisis sísmico
            P_edificio = num_pisos * (CM + 0.25*CV) * (L_viga*num_vanos)**2
            sismo = calcular_analisis_sismico(P_edificio, num_pisos, h_piso, zona_sismica, tipo_suelo, tipo_estructura, factor_importancia)
            
            # Diseño estructural
            M_u = (1.2*CM + 1.6*CV) * L_viga**2 / 8 * 100
            d_viga_cm = d_viga - 4
            diseno_flexion = calcular_diseno_flexion(M_u, b_viga, d_viga_cm, f_c, f_y, props_concreto['beta1'])
            
            V_u = (1.2*CM + 1.6*CV) * L_viga / 2
            diseno_cortante = calcular_diseno_cortante(V_u, b_viga, d_viga_cm, f_c, f_y)
            
            diseno_columna = calcular_diseno_columna(P_mayorada, f_c, f_y, A_columna)
            
            # Mostrar resultados
            st.success("✅ ¡Análisis completado exitosamente!")
            
            # Resultados principales
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <h4>📐 Dimensiones</h4>
                    <p><strong>Losa:</strong> """ + f"{h_losa*100:.0f}" + """ cm</p>
                    <p><strong>Viga:</strong> """ + f"{b_viga:.0f}" + """×""" + f"{d_viga:.0f}" + """ cm</p>
                    <p><strong>Columna:</strong> """ + f"{lado_columna:.0f}" + """×""" + f"{lado_columna:.0f}" + """ cm</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-card">
                    <h4>🌎 Sísmico</h4>
                    <p><strong>Cortante basal:</strong> """ + f"{sismo['V']/1000:.1f}" + """ ton</p>
                    <p><strong>Período:</strong> """ + f"{sismo['T']:.2f}" + """ s</p>
                    <p><strong>Coeficiente:</strong> """ + f"{sismo['C']:.3f}" + """</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráfico de fuerzas sísmicas
            fig_sismo = go.Figure()
            fig_sismo.add_trace(go.Bar(
                x=list(range(1, num_pisos+1)),
                y=[f/1000 for f in sismo['Fx']],
                name='Fuerza Sísmica',
                marker_color='#dc3545'
            ))
            fig_sismo.update_layout(
                title="Distribución de Fuerzas Sísmicas",
                xaxis_title="Nivel",
                yaxis_title="Fuerza (ton)",
                height=400
            )
            st.plotly_chart(fig_sismo, use_container_width=True)
            
            st.balloons()

if __name__ == "__main__":
    main() 