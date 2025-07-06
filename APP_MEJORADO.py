import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from math import sqrt
from datetime import datetime
import io
import tempfile
import os

# Configuración de la página con diseño profesional
st.set_page_config(
    page_title="CONSORCIO DEJ - Análisis Estructural Avanzado",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar el diseño
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #FFD700, #FFA500);
        color: #2F2F2F;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 2px solid #FFA500;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #FFD700;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header profesional
st.markdown("""
<div class="main-header">
    <h1>🏗️ CONSORCIO DEJ</h1>
    <p style="font-size: 18px; font-weight: bold;">Ingeniería y Construcción</p>
    <p style="font-size: 14px;">Software de Análisis Estructural Avanzado (ACI 318-2025 & E.060)</p>
</div>
""", unsafe_allow_html=True)

# Sistema de navegación con pestañas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Datos de Entrada", 
    "🔧 Predimensionamiento", 
    "🌎 Análisis Sísmico", 
    "🛠️ Diseño Estructural", 
    "📝 Reporte Final"
])

with tab1:
    st.header("📊 Datos de Entrada del Proyecto")
    
    # Sidebar mejorado
    with st.sidebar:
        st.header("🏗️ CONSORCIO DEJ")
        st.info("Software de Análisis Estructural")
        
        # Materiales
        st.subheader("📌 Materiales")
        f_c = st.number_input("Resistencia del concreto f'c (kg/cm²)", 
                             min_value=175, max_value=700, value=210, step=10)
        f_y = st.number_input("Esfuerzo de fluencia del acero fy (kg/cm²)", 
                             min_value=2800, max_value=6000, value=4200, step=100)
        E = 15000*sqrt(f_c)  # Módulo de elasticidad del concreto (kg/cm²)
        
        # Geometría
        st.subheader("📐 Geometría")
        L_viga = st.number_input("Luz libre de vigas (m)", 
                                min_value=3.0, max_value=12.0, value=6.0, step=0.5)
        h_piso = st.number_input("Altura de piso (m)", 
                                min_value=2.5, max_value=4.5, value=3.0, step=0.1)
        num_pisos = st.number_input("Número de pisos", 
                                   min_value=1, max_value=50, value=15, step=1)
        num_vanos = st.number_input("Número de vanos en dirección X", 
                                   min_value=1, max_value=10, value=3, step=1)
        
        # Cargas
        st.subheader("⚖️ Cargas")
        CM = st.number_input("Carga Muerta (kg/m²)", 
                            min_value=100, max_value=1000, value=150, step=50)
        CV = st.number_input("Carga Viva (kg/m²)", 
                            min_value=100, max_value=500, value=200, step=50)
        
        # Datos sísmicos (E.030)
        st.subheader("🌎 Parámetros Sísmicos")
        zona_sismica = st.selectbox("Zona Sísmica", ["Z1", "Z2", "Z3", "Z4"], index=2)
        tipo_suelo = st.selectbox("Tipo de Suelo", ["S1", "S2", "S3", "S4"], index=1)
        tipo_estructura = st.selectbox("Tipo de Sistema Estructural", 
                                      ["Pórticos", "Muros Estructurales", "Dual"], index=0)
        factor_importancia = st.number_input("Factor de Importancia (U)", 
                                           min_value=1.0, max_value=1.5, value=1.0, step=0.1)
    
    # Mostrar datos de entrada en el área principal
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Resumen de Datos de Entrada")
        
        # Crear DataFrame para mostrar datos
        datos_entrada = {
            "Parámetro": [
                "Resistencia del concreto (f'c)",
                "Esfuerzo de fluencia (fy)",
                "Módulo de elasticidad (E)",
                "Luz libre de vigas",
                "Altura de piso",
                "Número de pisos",
                "Número de vanos"
            ],
            "Valor": [
                f"{f_c} kg/cm²",
                f"{f_y} kg/cm²",
                f"{E:.0f} kg/cm²",
                f"{L_viga} m",
                f"{h_piso} m",
                f"{num_pisos}",
                f"{num_vanos}"
            ]
        }
        
        df_datos = pd.DataFrame(datos_entrada)
        st.dataframe(df_datos, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("🌎 Parámetros Sísmicos")
        
        # Factores de zona según E.030
        factores_Z = {"Z1": 0.10, "Z2": 0.20, "Z3": 0.30, "Z4": 0.45}
        Z = factores_Z[zona_sismica]
        
        # Coeficientes de reducción según E.030
        factores_R = {
            "Pórticos": 8.0,
            "Muros Estructurales": 6.0,
            "Dual": 7.0
        }
        R = factores_R[tipo_estructura]
        
        # Factores de suelo según E.030
        factores_S = {"S1": 1.0, "S2": 1.2, "S3": 1.4, "S4": 1.6}
        S = factores_S[tipo_suelo]
        
        datos_sismicos = {
            "Parámetro": ["Zona Sísmica", "Factor Z", "Tipo de Suelo", "Factor S", 
                         "Tipo de Estructura", "Factor R", "Factor de Importancia"],
            "Valor": [zona_sismica, f"{Z:.2f}", tipo_suelo, f"{S:.1f}", 
                     tipo_estructura, f"{R:.1f}", f"{factor_importancia:.1f}"]
        }
        
        df_sismicos = pd.DataFrame(datos_sismicos)
        st.dataframe(df_sismicos, use_container_width=True, hide_index=True)

with tab2:
    st.header("🔧 Predimensionamiento Estructural")
    
    # 2.1 Losas Aligeradas (E.060)
    h_losa = max(L_viga / 25, 0.17)  # Espesor mínimo (17 cm mínimo)
    rho_min_losa = 0.0018  # Cuantía mínima para losas
    
    st.subheader("🏗️ Losas Aligeradas")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Espesor mínimo (h)", f"{h_losa:.2f} m", f"{h_losa*100:.0f} cm")
        st.metric("Cuantía mínima (ρ)", f"{rho_min_losa:.4f}")
    
    with col2:
        # Gráfico de espesor de losa
        fig_losa = px.bar(x=["Espesor Mínimo"], y=[h_losa*100], 
                         title="Espesor de Losa Aligerada",
                         color_discrete_sequence=['#FFD700'])
        fig_losa.update_layout(yaxis_title="Espesor (cm)", height=300)
        st.plotly_chart(fig_losa, use_container_width=True)
    
    # 2.2 Vigas (ACI 318-2025)
    d_viga = L_viga * 100 / 10  # Peralte efectivo (cm)
    b_viga = max(0.3 * d_viga, 25)  # Ancho mínimo (25 cm mínimo)
    rho_min_viga = max(0.8 * sqrt(f_c) / f_y, 14 / f_y)
    rho_max_viga = 0.025  # Para zonas sísmicas
    
    st.subheader("🏗️ Vigas Principales")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Peralte efectivo (d)", f"{d_viga:.2f} cm")
        st.metric("Ancho mínimo (b)", f"{b_viga:.2f} cm")
        st.metric("Cuantía mínima (ρ_min)", f"{rho_min_viga:.4f}")
        st.metric("Cuantía máxima (ρ_max)", f"{rho_max_viga:.4f}")
    
    with col2:
        # Gráfico de dimensiones de viga
        fig_viga = px.bar(x=["Peralte (d)", "Ancho (b)"], 
                         y=[d_viga, b_viga],
                         title="Dimensiones de Viga Principal",
                         color_discrete_sequence=['#4169E1'])
        fig_viga.update_layout(yaxis_title="Dimensión (cm)", height=300)
        st.plotly_chart(fig_viga, use_container_width=True)
    
    # 2.3 Columnas (ACI 318-2025)
    P_servicio = num_pisos * (CM + 0.25*CV) * (L_viga*num_vanos)**2  # Carga axial estimada (kg)
    P_mayorada = num_pisos * (1.2*CM + 1.6*CV) * (L_viga*num_vanos)**2  # Carga mayorada (kg)
    
    # Área mínima para compresión
    A_columna_servicio = (P_servicio) / (0.45*f_c)  # cm²
    A_columna_mayorada = (P_mayorada) / (0.65*0.8*f_c)  # cm² (φ=0.65)
    
    # Tomar el mayor valor
    A_columna = max(A_columna_servicio, A_columna_mayorada)
    lado_columna = sqrt(A_columna)  # Lado para columna cuadrada (cm)
    
    # Verificación de esbeltez
    k = 1.0  # Factor de longitud efectiva (conservador)
    r = 0.3 * lado_columna  # Radio de giro
    relacion_esbeltez = (k * h_piso * 100) / r
    
    st.subheader("🏗️ Columnas")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Área bruta requerida (A_g)", f"{A_columna:.2f} cm²")
        st.metric("Lado mínimo (columna cuadrada)", f"{lado_columna:.2f} cm")
        st.metric("Relación de esbeltez (kLu/r)", f"{relacion_esbeltez:.2f}")
    
    with col2:
        # Verificación de esbeltez
        if relacion_esbeltez <= 22:
            st.success("✅ OK - Esbeltez dentro del límite (≤ 22)")
        else:
            st.warning("⚠️ Requiere análisis de efectos de segundo orden")
        
        # Gráfico de área de columna
        fig_columna = px.bar(x=["Área Bruta"], y=[A_columna],
                           title="Área de Columna Requerida",
                           color_discrete_sequence=['#32CD32'])
        fig_columna.update_layout(yaxis_title="Área (cm²)", height=300)
        st.plotly_chart(fig_columna, use_container_width=True)

with tab3:
    st.header("🌎 Análisis Sísmico (E.030)")
    
    # Peso total del edificio
    P_edificio = num_pisos * (CM + 0.25*CV) * (L_viga*num_vanos)**2  # kg
    
    # Coeficiente sísmico
    T = 0.1 * num_pisos  # Período fundamental aproximado (segundos)
    if tipo_suelo == "S1":
        C = 2.5 * (1.0/T)**0.8
    else:
        C = 2.5 * (1.0/T)  # Simplificado
    
    # Cortante basal
    V = (Z * factor_importancia * C * S * P_edificio) / R  # kg
    
    # Distribución vertical de fuerzas
    Fx = []
    sum_h = sum([i*h_piso for i in range(1, num_pisos+1)])
    for i in range(1, num_pisos+1):
        Fx.append(V * (i*h_piso)/sum_h)
    
    st.subheader("📊 Resultados del Análisis Sísmico")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Peso total del edificio", f"{P_edificio/1000:.2f} ton")
        st.metric("Coeficiente sísmico (C)", f"{C:.3f}")
        st.metric("Cortante basal (V)", f"{V/1000:.2f} ton")
        st.metric("Período fundamental (T)", f"{T:.2f} s")
    
    with col2:
        st.subheader("📈 Distribución de Fuerzas Sísmicas")
        
        # Crear DataFrame para la distribución
        distribucion_data = {
            "Piso": list(range(1, num_pisos+1)),
            "Fuerza Sísmica (ton)": [f/1000 for f in Fx]
        }
        df_distribucion = pd.DataFrame(distribucion_data)
        st.dataframe(df_distribucion, use_container_width=True, hide_index=True)
    
    # Gráfico de distribución de fuerzas sísmicas
    st.subheader("📊 Visualización de Fuerzas Sísmicas")
    
    fig_sismo = px.bar(x=list(range(1, num_pisos+1)), 
                      y=[f/1000 for f in Fx],
                      title="Distribución de Fuerzas Sísmicas por Piso",
                      labels={'x': 'Nivel', 'y': 'Fuerza Sísmica (ton)'},
                      color_discrete_sequence=['#FF6B6B'])
    
    fig_sismo.update_layout(
        xaxis_title="Nivel",
        yaxis_title="Fuerza Sísmica (ton)",
        height=400,
        showlegend=False
    )
    
    # Agregar valores en las barras
    fig_sismo.update_traces(texttemplate='%{y:.2f}', textposition='outside')
    
    st.plotly_chart(fig_sismo, use_container_width=True)

with tab4:
    st.header("🛠️ Diseño de Elementos Estructurales")
    
    # 4.1 Diseño de Vigas
    M_u = (1.2*CM + 1.6*CV) * L_viga**2 / 8 * 100  # Momento mayorado (kgf*cm)
    phi = 0.9
    d_viga_cm = d_viga - 4  # d = h - recubrimiento (4 cm estimado)
    
    # Iteración para encontrar As
    a_estimado = d_viga_cm / 5
    A_s = (M_u) / (phi * f_y * (d_viga_cm - a_estimado/2))
    a_real = (A_s * f_y) / (0.85 * f_c * b_viga)
    A_s_corr = (M_u) / (phi * f_y * (d_viga_cm - a_real/2))
    
    # Verificación de cuantías
    rho_provisto = A_s_corr / (b_viga * d_viga_cm)
    cumple_cuantia = rho_min_viga <= rho_provisto <= rho_max_viga
    
    st.subheader("🏗️ Viga Principal - Flexión")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Momento mayorado (Mu)", f"{M_u/100:.2f} kgf·m")
        st.metric("Acero requerido (As)", f"{A_s_corr:.2f} cm²")
        st.metric("ρ provisto", f"{rho_provisto:.4f}")
    
    with col2:
        st.metric("ρ mínimo", f"{rho_min_viga:.4f}")
        st.metric("ρ máximo", f"{rho_max_viga:.4f}")
        
        if cumple_cuantia:
            st.success("✅ CUMPLE cuantías")
        else:
            st.error("⚠️ NO CUMPLE cuantías")
    
    # 4.2 Diseño por Cortante
    V_u = (1.2*CM + 1.6*CV) * L_viga / 2  # Cortante mayorado (kg)
    phi_v = 0.75
    V_c = 0.53 * sqrt(f_c) * b_viga * d_viga_cm  # kgf
    V_s_max = 2.1 * sqrt(f_c) * b_viga * d_viga_cm  # Límite ACI 318-25
    
    st.subheader("🏗️ Viga Principal - Cortante")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Cortante mayorado (Vu)", f"{V_u:.2f} kgf")
        st.metric("Resistencia del concreto (Vc)", f"{V_c:.2f} kgf")
    
    with col2:
        if V_u > phi_v * V_c:
            V_s = (V_u / phi_v) - V_c
            if V_s > V_s_max:
                st.error("⚠️ Sección insuficiente para resistir cortante!")
                st.info("💡 Aumentar dimensiones de la viga")
            else:
                # Diseño de estribos
                diam_estribo = 0.95  # 3/8"
                Av = 2 * 0.71  # 2 ramas de estribo #3 (cm²)
                s_max = min(d_viga_cm/2, 60)  # cm (ACI 318-25 9.7.6.2)
                s_req = (Av * f_y * d_viga_cm) / V_s  # cm
                
                st.metric("Acero requerido (Vs)", f"{V_s:.2f} kgf")
                st.metric("Separación estribos ϕ3/8", f"{min(s_req, s_max):.2f} cm")
        else:
            st.success("✅ El concreto resiste el cortante")
            st.info("📏 Colocar estribos mínimos")
            st.metric("Separación máxima", f"{min(d_viga_cm/2, 60):.0f} cm")
    
    # 4.3 Diseño de Columnas
    st.subheader("🏗️ Columnas - Diseño a Compresión")
    
    P_u = P_mayorada  # kg (ya calculado)
    phi = 0.65  # Para columnas con estribos
    A_g = lado_columna**2  # cm²
    As_min = 0.01 * A_g  # Acero mínimo (1%)
    As_max = 0.06 * A_g  # Acero máximo (6%)
    
    # Resistencia nominal
    Pn = P_u / phi
    P0 = 0.85*f_c*(A_g - As_min) + f_y*As_min  # kg
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Carga axial mayorada (Pu)", f"{P_u/1000:.2f} ton")
        st.metric("Área de concreto (Ag)", f"{A_g:.2f} cm²")
        st.metric("Acero longitudinal mínimo", f"{As_min:.2f} cm² (1%)")
    
    with col2:
        st.metric("Acero longitudinal máximo", f"{As_max:.2f} cm² (6%)")
        st.metric("Resistencia nominal (Pn)", f"{Pn/1000:.2f} ton")
        st.metric("Resistencia máxima (P0)", f"{P0/1000:.2f} ton")
    
    if Pn <= P0:
        st.success("✅ La columna resiste la carga axial")
    else:
        st.error("⚠️ Aumentar dimensiones de columna o resistencia del concreto")

with tab5:
    st.header("📝 Reporte Estructural Completo")
    
    # Resumen de diseño
    st.subheader("📋 Resumen de Diseño")
    
    elementos = {
        "Elemento": ["Losa Aligerada", "Viga Principal", "Columna"],
        "Dimensión": [f"{h_losa*100:.0f} cm", f"{b_viga:.0f}x{d_viga:.0f} cm", f"{lado_columna:.0f}x{lado_columna:.0f} cm"],
        "Acero Longitudinal": ["-", f"{A_s_corr:.2f} cm²", f"{As_min:.2f}-{As_max:.2f} cm² (1%-6%)"],
        "Refuerzo Transversal": ["Malla ϕ4@25cm", 
                                f"Estribos ϕ3/8@{min(s_req, s_max):.0f}cm" if 's_req' in locals() else f"Estribos ϕ3/8@{d_viga_cm/2:.0f}cm", 
                                "Estribos ϕ3/8@30cm"]
    }
    
    df_elementos = pd.DataFrame(elementos)
    st.dataframe(df_elementos, use_container_width=True, hide_index=True)
    
    # Gráfico de comparación de elementos
    st.subheader("📊 Comparación de Elementos Estructurales")
    
    # Datos para el gráfico
    elementos_grafico = {
        "Elemento": ["Losa", "Viga", "Columna"],
        "Altura (cm)": [h_losa*100, d_viga, lado_columna],
        "Ancho (cm)": [0, b_viga, lado_columna]
    }
    
    fig_comparacion = px.bar(
        elementos_grafico, 
        x="Elemento", 
        y=["Altura (cm)", "Ancho (cm)"],
        title="Dimensiones de Elementos Estructurales",
        barmode='group',
        color_discrete_map={"Altura (cm)": "#FFD700", "Ancho (cm)": "#4169E1"}
    )
    
    fig_comparacion.update_layout(
        xaxis_title="Elemento",
        yaxis_title="Dimensión (cm)",
        height=400
    )
    
    st.plotly_chart(fig_comparacion, use_container_width=True)
    
    # Información adicional
    st.subheader("ℹ️ Información del Proyecto")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Datos del Proyecto:**")
        st.write(f"• Fecha de análisis: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        st.write(f"• Empresa: CONSORCIO DEJ")
        st.write(f"• Software: Streamlit + Python")
        st.write(f"• Normativa: ACI 318-2025 & E.060")
    
    with col2:
        st.info("**Recomendaciones:**")
        st.write("• Verificar todos los cálculos con software especializado")
        st.write("• Consultar con ingeniero estructural certificado")
        st.write("• Revisar detalles constructivos")
        st.write("• Considerar efectos sísmicos adicionales")
    
    # Botón para generar reporte
    if st.button("📄 Generar Reporte PDF", type="primary"):
        st.success("✅ Reporte generado exitosamente")
        st.balloons()
        
        # Aquí se podría implementar la generación de PDF
        st.info("📋 Funcionalidad de PDF en desarrollo")

# Footer profesional
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;">
    <p style="font-weight: bold; color: #2F2F2F;">🏗️ CONSORCIO DEJ - Ingeniería y Construcción</p>
    <p style="color: #666;">Software de Análisis Estructural Avanzado</p>
    <p style="font-size: 12px; color: #999;">Desarrollado con Python, Streamlit y Plotly</p>
</div>
""", unsafe_allow_html=True) 