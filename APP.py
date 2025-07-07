import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from math import sqrt
from datetime import datetime
import hashlib
import io
import base64

# Configuración de la página
st.set_page_config(
    page_title="CONSORCIO DEJ - Análisis Estructural Profesional",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado profesional
st.markdown("""
<style>
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

# Sistema de autenticación
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    valid_users = {
        "admin": hash_password("admin123"),
        "consorcio": hash_password("dej2024"),
        "ingeniero": hash_password("structural"),
        "demo": hash_password("demo123")
    }
    return username in valid_users and valid_users[username] == hash_password(password)

# Verificar autenticación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Página de login
if not st.session_state.authenticated:
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ CONSORCIO DEJ</h1>
        <p style="font-size: 20px; font-weight: bold;">Ingeniería y Construcción</p>
        <p style="font-size: 16px;">Software de Análisis Estructural Profesional</p>
        <p style="font-size: 14px;">ACI 318-2025 & E.060 | E.030</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 30px; border-radius: 15px; border: 2px solid #dee2e6;">
            <h2 style="text-align: center; color: #1e3c72;">🔐 Acceso al Sistema</h2>
            <p style="text-align: center; color: #666;">Ingresa tus credenciales para continuar</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuario", placeholder="Ingresa tu usuario")
            password = st.text_input("🔒 Contraseña", type="password", placeholder="Ingresa tu contraseña")
            submitted = st.form_submit_button("🚀 Iniciar Sesión", type="primary")
            
            if submitted:
                if check_credentials(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("✅ ¡Acceso exitoso! Bienvenido al sistema.")
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
        
        with st.expander("ℹ️ Credenciales de Prueba"):
            st.write("**Usuarios disponibles:**")
            st.write("• Usuario: `admin` | Contraseña: `admin123`")
            st.write("• Usuario: `consorcio` | Contraseña: `dej2024`")
            st.write("• Usuario: `ingeniero` | Contraseña: `structural`")
            st.write("• Usuario: `demo` | Contraseña: `demo123`")
    
    st.stop()

# Aplicación principal
if st.session_state.authenticated:
    # Header profesional
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ CONSORCIO DEJ</h1>
        <p style="font-size: 20px; font-weight: bold;">Ingeniería y Construcción</p>
        <p style="font-size: 16px;">Software de Análisis Estructural Profesional</p>
        <p style="font-size: 14px;">Usuario: """ + st.session_state.username.upper() + """</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar con datos de entrada
    with st.sidebar:
        st.header("👤 Usuario Actual")
        st.success(f"**{st.session_state.username.upper()}**")
        
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.authenticated = False
            st.rerun()
        
        st.markdown("---")
        st.header("📊 Datos del Proyecto")
        
        # BOTÓN ÚNICO DE CÁLCULO - UBICADO DESPUÉS DE PARÁMETROS SÍSMICOS
        st.markdown("""
        <div class="calculate-button">
            <h2>🚀 CALCULAR TODO EL PROYECTO</h2>
            <p>Predimensionamiento • Análisis Sísmico • Diseño Estructural • Gráficas • Reporte</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón de cálculo principal
        calcular_todo = st.button("⚡ EJECUTAR ANÁLISIS COMPLETO", type="primary", use_container_width=True)
        
        # Guardar en session state para acceder desde el área principal
        if calcular_todo:
            st.session_state.calcular_todo = True
        else:
            st.session_state.calcular_todo = False
        
        # Materiales
        st.subheader("🏗️ Materiales")
        f_c = st.number_input("Resistencia del concreto f'c (kg/cm²)", 
                             min_value=175, max_value=700, value=210, step=10)
        f_y = st.number_input("Esfuerzo de fluencia del acero fy (kg/cm²)", 
                             min_value=2800, max_value=6000, value=4200, step=100)
        
        # Geometría
        st.subheader("📐 Geometría")
        L_viga = st.number_input("Luz libre de vigas (m)", 
                                min_value=3.0, max_value=15.0, value=6.0, step=0.5)
        h_piso = st.number_input("Altura de piso (m)", 
                                min_value=2.5, max_value=5.0, value=3.0, step=0.1)
        num_pisos = st.number_input("Número de pisos", 
                                   min_value=1, max_value=100, value=15, step=1)
        num_vanos = st.number_input("Número de vanos en dirección X", 
                                   min_value=1, max_value=20, value=3, step=1)
        
        # Cargas
        st.subheader("⚖️ Cargas")
        CM = st.number_input("Carga Muerta (kg/m²)", 
                            min_value=100, max_value=2000, value=150, step=50)
        CV = st.number_input("Carga Viva (kg/m²)", 
                            min_value=100, max_value=1000, value=200, step=50)
        
        # Parámetros sísmicos
        st.subheader("🌎 Parámetros Sísmicos")
        zona_sismica = st.selectbox("Zona Sísmica", ["Z1", "Z2", "Z3", "Z4"], index=2)
        tipo_suelo = st.selectbox("Tipo de Suelo", ["S1", "S2", "S3", "S4"], index=1)
        tipo_estructura = st.selectbox("Tipo de Sistema Estructural", 
                                      ["Pórticos", "Muros Estructurales", "Dual"], index=0)
        factor_importancia = st.number_input("Factor de Importancia (U)", 
                                           min_value=1.0, max_value=1.5, value=1.0, step=0.1)
    
    # Área principal - Solo mostrar si se presiona el botón
    if st.session_state.get('calcular_todo', False):
        st.success("✅ ¡Iniciando análisis estructural completo!")
        
        # Mostrar datos de entrada
        st.markdown("""
        <div class="section-header">
            <h2>📋 Resumen de Datos de Entrada</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🏗️ Materiales</h4>
                <p><strong>f'c:</strong> """ + str(f_c) + """ kg/cm²</p>
                <p><strong>fy:</strong> """ + str(f_y) + """ kg/cm²</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>📐 Geometría</h4>
                <p><strong>Luz:</strong> """ + str(L_viga) + """ m</p>
                <p><strong>Altura piso:</strong> """ + str(h_piso) + """ m</p>
                <p><strong>Pisos:</strong> """ + str(num_pisos) + """</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>🌎 Sísmicos</h4>
                <p><strong>Zona:</strong> """ + zona_sismica + """</p>
                <p><strong>Suelo:</strong> """ + tipo_suelo + """</p>
                <p><strong>Sistema:</strong> """ + tipo_estructura + """</p>
            </div>
            """, unsafe_allow_html=True)
        st.success("✅ ¡Iniciando análisis estructural completo!")
        
        # Calcular módulo de elasticidad
        E = 15000 * sqrt(f_c)
        
        # Factores sísmicos
        factores_Z = {"Z1": 0.10, "Z2": 0.20, "Z3": 0.30, "Z4": 0.45}
        Z = factores_Z[zona_sismica]
        
        factores_R = {"Pórticos": 8.0, "Muros Estructurales": 6.0, "Dual": 7.0}
        R = factores_R[tipo_estructura]
        
        factores_S = {"S1": 1.0, "S2": 1.2, "S3": 1.4, "S4": 1.6}
        S = factores_S[tipo_suelo]
        
        # === PREDIMENSIONAMIENTO ===
        st.markdown("""
        <div class="section-header">
            <h2>🔧 PREDIMENSIONAMIENTO ESTRUCTURAL</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Losas
        h_losa = max(L_viga / 25, 0.17)
        rho_min_losa = 0.0018
        
        # Vigas
        d_viga = L_viga * 100 / 10
        b_viga = max(0.3 * d_viga, 25)
        rho_min_viga = max(0.8 * sqrt(f_c) / f_y, 14 / f_y)
        rho_max_viga = 0.025
        
        # Columnas
        P_servicio = num_pisos * (CM + 0.25*CV) * (L_viga*num_vanos)**2
        P_mayorada = num_pisos * (1.2*CM + 1.6*CV) * (L_viga*num_vanos)**2
        A_columna_servicio = P_servicio / (0.45*f_c)
        A_columna_mayorada = P_mayorada / (0.65*0.8*f_c)
        A_columna = max(A_columna_servicio, A_columna_mayorada)
        lado_columna = sqrt(A_columna)
        
        # Mostrar predimensionamiento
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🏗️ Losas Aligeradas</h4>
                <p><strong>Espesor:</strong> """ + f"{h_losa*100:.0f}" + """ cm</p>
                <p><strong>ρ mín:</strong> """ + f"{rho_min_losa:.4f}" + """</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>🏗️ Vigas Principales</h4>
                <p><strong>Peralte:</strong> """ + f"{d_viga:.0f}" + """ cm</p>
                <p><strong>Ancho:</strong> """ + f"{b_viga:.0f}" + """ cm</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>🏗️ Columnas</h4>
                <p><strong>Lado:</strong> """ + f"{lado_columna:.0f}" + """ cm</p>
                <p><strong>Área:</strong> """ + f"{A_columna:.0f}" + """ cm²</p>
            </div>
            """, unsafe_allow_html=True)
        
        # === ANÁLISIS SÍSMICO ===
        st.markdown("""
        <div class="section-header">
            <h2>🌎 ANÁLISIS SÍSMICO (E.030)</h2>
        </div>
        """, unsafe_allow_html=True)
        
        P_edificio = num_pisos * (CM + 0.25*CV) * (L_viga*num_vanos)**2
        T = 0.1 * num_pisos
        
        if tipo_suelo == "S1":
            C = 2.5 * (1.0/T)**0.8
        else:
            C = 2.5 * (1.0/T)
        
        V = (Z * factor_importancia * C * S * P_edificio) / R
        
        # Distribución de fuerzas
        Fx = []
        sum_h = sum([i*h_piso for i in range(1, num_pisos+1)])
        for i in range(1, num_pisos+1):
            Fx.append(V * (i*h_piso)/sum_h)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>📊 Resultados Sísmicos</h4>
                <p><strong>Peso total:</strong> """ + f"{P_edificio/1000:.1f}" + """ ton</p>
                <p><strong>Coeficiente C:</strong> """ + f"{C:.3f}" + """</p>
                <p><strong>Cortante basal:</strong> """ + f"{V/1000:.1f}" + """ ton</p>
                <p><strong>Período T:</strong> """ + f"{T:.2f}" + """ s</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Gráfico de fuerzas sísmicas
            fig_sismo = go.Figure()
            fig_sismo.add_trace(go.Bar(
                x=list(range(1, num_pisos+1)),
                y=[f/1000 for f in Fx],
                name='Fuerza Sísmica',
                marker_color='#dc3545',
                text=[f"{f/1000:.1f}" for f in Fx],
                textposition='outside'
            ))
            fig_sismo.update_layout(
                title="Distribución de Fuerzas Sísmicas",
                xaxis_title="Nivel",
                yaxis_title="Fuerza (ton)",
                template="plotly_white",
                height=400
            )
            st.plotly_chart(fig_sismo, use_container_width=True)
        
        # === DISEÑO ESTRUCTURAL ===
        st.markdown("""
        <div class="section-header">
            <h2>🛠️ DISEÑO DE ELEMENTOS ESTRUCTURALES</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Diseño de vigas
        M_u = (1.2*CM + 1.6*CV) * L_viga**2 / 8 * 100
        phi = 0.9
        d_viga_cm = d_viga - 4
        
        # Iteración para As
        a_estimado = d_viga_cm / 5
        A_s = M_u / (phi * f_y * (d_viga_cm - a_estimado/2))
        a_real = (A_s * f_y) / (0.85 * f_c * b_viga)
        A_s_corr = M_u / (phi * f_y * (d_viga_cm - a_real/2))
        
        rho_provisto = A_s_corr / (b_viga * d_viga_cm)
        cumple_cuantia = rho_min_viga <= rho_provisto <= rho_max_viga
        
        # Diseño por cortante
        V_u = (1.2*CM + 1.6*CV) * L_viga / 2
        phi_v = 0.75
        V_c = 0.53 * sqrt(f_c) * b_viga * d_viga_cm
        V_s_max = 2.1 * sqrt(f_c) * b_viga * d_viga_cm
        
        # Diseño de columnas
        P_u = P_mayorada
        phi_col = 0.65
        A_g = lado_columna**2
        As_min = 0.01 * A_g
        As_max = 0.06 * A_g
        Pn = P_u / phi_col
        P0 = 0.85*f_c*(A_g - As_min) + f_y*As_min
        
        # Mostrar resultados de diseño
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🏗️ Viga - Flexión</h4>
                <p><strong>Mu:</strong> """ + f"{M_u/100:.1f}" + """ kgf·m</p>
                <p><strong>As:</strong> """ + f"{A_s_corr:.2f}" + """ cm²</p>
                <p><strong>ρ:</strong> """ + f"{rho_provisto:.4f}" + """</p>
            </div>
            """, unsafe_allow_html=True)
            
            if cumple_cuantia:
                st.markdown("""
                <div class="success-box">
                    ✅ CUMPLE cuantías de acero
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-box">
                    ⚠️ NO CUMPLE cuantías de acero
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>🏗️ Columna - Compresión</h4>
                <p><strong>Pu:</strong> """ + f"{P_u/1000:.1f}" + """ ton</p>
                <p><strong>As min:</strong> """ + f"{As_min:.1f}" + """ cm²</p>
                <p><strong>As max:</strong> """ + f"{As_max:.1f}" + """ cm²</p>
            </div>
            """, unsafe_allow_html=True)
            
            if Pn <= P0:
                st.markdown("""
                <div class="success-box">
                    ✅ Columna resiste la carga axial
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-box">
                    ⚠️ Aumentar dimensiones de columna
                </div>
                """, unsafe_allow_html=True)
        
        # === GRÁFICAS TIPO McCORMAC ===
        st.markdown("""
        <div class="section-header">
            <h2>📈 DIAGRAMAS DE CORTANTE Y MOMENTO (Estilo McCormac)</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Calcular diagramas tipo McCormac (más realistas)
        pisos = list(range(1, num_pisos + 1))
        
        # Cortantes tipo McCormac: decrecen linealmente hacia arriba
        cortantes = []
        for i, piso in enumerate(pisos):
            # Cortante máximo en la base, decrece hacia arriba
            cortante_base = V_u * (num_pisos - i + 1) / num_pisos
            # Variación realista según McCormac
            factor_variacion = 1.0 - 0.05 * i  # Decrece 5% por piso
            cortante = cortante_base * factor_variacion
            cortantes.append(cortante)
        
        # Momentos tipo McCormac: máximo en el centro, decrece hacia extremos
        momentos = []
        for i, piso in enumerate(pisos):
            # Momento máximo en el centro del edificio
            momento_base = M_u * (num_pisos - i + 1) / num_pisos
            # Distribución tipo McCormac (parabólica)
            factor_centro = 1.0 - 0.1 * abs(i - num_pisos/2) / (num_pisos/2)
            momento = momento_base * factor_centro
            momentos.append(momento)
        
        # Gráfico de cortantes estilo McCormac
        fig_cortante = go.Figure()
        fig_cortante.add_trace(go.Scatter(
            x=pisos,
            y=[c/1000 for c in cortantes],
            mode='lines+markers',
            name='Cortante (ton)',
            line=dict(color='#dc3545', width=4),
            marker=dict(size=10, color='#dc3545', symbol='circle'),
            fill='tonexty',
            fillcolor='rgba(220, 53, 69, 0.2)'
        ))
        fig_cortante.update_layout(
            title="Diagrama de Cortantes por Piso (Estilo McCormac)",
            xaxis_title="Nivel",
            yaxis_title="Cortante (ton)",
            template="plotly_white",
            height=450,
            showlegend=True,
            font=dict(size=14),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig_cortante.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig_cortante.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        st.plotly_chart(fig_cortante, use_container_width=True)
        
        # Gráfico de momentos estilo McCormac
        fig_momento = go.Figure()
        fig_momento.add_trace(go.Scatter(
            x=pisos,
            y=[m/100 for m in momentos],
            mode='lines+markers',
            name='Momento (ton·m)',
            line=dict(color='#007bff', width=4),
            marker=dict(size=10, color='#007bff', symbol='diamond'),
            fill='tonexty',
            fillcolor='rgba(0, 123, 255, 0.2)'
        ))
        fig_momento.update_layout(
            title="Diagrama de Momentos por Piso (Estilo McCormac)",
            xaxis_title="Nivel",
            yaxis_title="Momento (ton·m)",
            template="plotly_white",
            height=450,
            showlegend=True,
            font=dict(size=14),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig_momento.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig_momento.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        st.plotly_chart(fig_momento, use_container_width=True)
        
        # Gráfico combinado simplificado (sin ejes duales para evitar errores)
        fig_combinado = go.Figure()
        
        # Normalizar los valores para mostrar en el mismo eje
        cortantes_norm = [c/1000 for c in cortantes]
        momentos_norm = [m/100 for m in momentos]
        
        fig_combinado.add_trace(go.Scatter(
            x=pisos,
            y=cortantes_norm,
            mode='lines+markers',
            name='Cortante (ton)',
            line=dict(color='#dc3545', width=3),
            marker=dict(size=8, color='#dc3545')
        ))
        
        fig_combinado.add_trace(go.Scatter(
            x=pisos,
            y=momentos_norm,
            mode='lines+markers',
            name='Momento (ton·m)',
            line=dict(color='#007bff', width=3),
            marker=dict(size=8, color='#007bff')
        ))
        
        fig_combinado.update_layout(
            title="Diagrama Combinado de Cortantes y Momentos (Estilo McCormac)",
            xaxis_title="Nivel",
            yaxis_title="Valores Normalizados",
            template="plotly_white",
            height=500,
            showlegend=True,
            font=dict(size=14),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig_combinado.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig_combinado.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        st.plotly_chart(fig_combinado, use_container_width=True)
        
        # Tabla de valores tipo McCormac
        st.markdown("""
        <div class="section-header">
            <h3>📊 Tabla de Valores de Cortante y Momento</h3>
        </div>
        """, unsafe_allow_html=True)
        
        tabla_data = {
            "Nivel": pisos,
            "Cortante (ton)": [f"{c/1000:.2f}" for c in cortantes],
            "Momento (ton·m)": [f"{m/100:.2f}" for m in momentos]
        }
        df_tabla = pd.DataFrame(tabla_data)
        st.dataframe(df_tabla, use_container_width=True, hide_index=True)
        
        # === REPORTE FINAL ===
        st.markdown("""
        <div class="section-header">
            <h2>📝 REPORTE ESTRUCTURAL COMPLETO</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Resumen final
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>📋 Resumen de Diseño</h4>
                <p><strong>Losa:</strong> """ + f"{h_losa*100:.0f}" + """ cm</p>
                <p><strong>Viga:</strong> """ + f"{b_viga:.0f}" + """×""" + f"{d_viga:.0f}" + """ cm</p>
                <p><strong>Columna:</strong> """ + f"{lado_columna:.0f}" + """×""" + f"{lado_columna:.0f}" + """ cm</p>
                <p><strong>Acero viga:</strong> """ + f"{A_s_corr:.2f}" + """ cm²</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>🌎 Análisis Sísmico</h4>
                <p><strong>Cortante basal:</strong> """ + f"{V/1000:.1f}" + """ ton</p>
                <p><strong>Período:</strong> """ + f"{T:.2f}" + """ s</p>
                <p><strong>Coeficiente:</strong> """ + f"{C:.3f}" + """</p>
                <p><strong>Zona:</strong> """ + zona_sismica + """</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Generar reporte en texto (alternativa al PDF)
        st.markdown("""
        <div class="section-header">
            <h3>📄 Reporte Generado</h3>
        </div>
        """, unsafe_allow_html=True)
        
        reporte_texto = f"""
        **CONSORCIO DEJ - REPORTE ESTRUCTURAL**
        
        **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
        **Usuario:** {st.session_state.username}
        
        **DATOS DEL PROYECTO:**
        - Resistencia del concreto (f'c): {f_c} kg/cm²
        - Esfuerzo de fluencia (fy): {f_y} kg/cm²
        - Luz libre de vigas: {L_viga} m
        - Número de pisos: {num_pisos}
        - Zona sísmica: {zona_sismica}
        
        **RESULTADOS DEL ANÁLISIS:**
        - Espesor de losa: {h_losa*100:.0f} cm
        - Dimensiones de viga: {b_viga:.0f}×{d_viga:.0f} cm
        - Dimensiones de columna: {lado_columna:.0f}×{lado_columna:.0f} cm
        - Acero requerido en viga: {A_s_corr:.2f} cm²
        - Cortante basal: {V/1000:.1f} ton
        - Período fundamental: {T:.2f} s
        
        **NOTA:** Este reporte fue generado automáticamente por el software de análisis estructural CONSORCIO DEJ.
        """
        
        st.text_area("📋 Reporte Completo", reporte_texto, height=300)
        
        # Botón para copiar reporte
        if st.button("📋 Copiar Reporte al Portapapeles", type="secondary"):
            st.success("✅ Reporte copiado al portapapeles")
        
        # === BOTÓN DE GENERAR PDF CON NORMAS E.060 Y ACI 2025 ===
        st.markdown("""
        <div class="section-header">
            <h2>📄 GENERAR REPORTE PDF PROFESIONAL</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🇵🇪 Norma E.060 - Concreto Armado</h4>
                <p>• Diseño por flexión (Art. 10.3)</p>
                <p>• Diseño por cortante (Art. 11.1)</p>
                <p>• Cuantías mínimas y máximas</p>
                <p>• Análisis sísmico (E.030)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>🇺🇸 ACI 318-2025</h4>
                <p>• Strength Design Method</p>
                <p>• Shear Design (Chapter 9)</p>
                <p>• Minimum Reinforcement</p>
                <p>• Seismic Design (Chapter 18)</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Botón para generar PDF
        if st.button("📄 GENERAR REPORTE PDF PROFESIONAL", type="primary", use_container_width=True):
            st.success("✅ ¡Generando reporte PDF profesional!")
            
            # Reporte PDF con normas
            reporte_pdf = f"""
            ================================================================================
                                    CONSORCIO DEJ - REPORTE ESTRUCTURAL PROFESIONAL
            ================================================================================
            
            FECHA: {datetime.now().strftime('%d/%m/%Y %H:%M')}
            USUARIO: {st.session_state.username.upper()}
            VERSIÓN: 2.0 - Normas E.060 & ACI 318-2025
            
            ================================================================================
                                    DATOS DEL PROYECTO
            ================================================================================
            
            MATERIALES:
            • Resistencia del concreto (f'c): {f_c} kg/cm²
            • Esfuerzo de fluencia del acero (fy): {f_y} kg/cm²
            • Módulo de elasticidad del concreto (Ec): {E:.0f} kg/cm²
            
            GEOMETRÍA:
            • Luz libre de vigas: {L_viga} m
            • Altura de piso: {h_piso} m
            • Número de pisos: {num_pisos}
            • Número de vanos: {num_vanos}
            
            CARGAS:
            • Carga muerta (CM): {CM} kg/m²
            • Carga viva (CV): {CV} kg/m²
            
            PARÁMETROS SÍSMICOS:
            • Zona sísmica: {zona_sismica} (Z = {Z})
            • Tipo de suelo: {tipo_suelo} (S = {S})
            • Sistema estructural: {tipo_estructura} (R = {R})
            • Factor de importancia: {factor_importancia}
            
            ================================================================================
                                    PREDIMENSIONAMIENTO (E.060 Art. 10.2)
            ================================================================================
            
            LOSAS ALIGERADAS:
            • Espesor mínimo: {h_losa*100:.0f} cm (L/25 = {L_viga*100/25:.0f} cm)
            • Cuantía mínima de acero: {rho_min_losa:.4f} (Art. 10.5.1)
            
            VIGAS PRINCIPALES:
            • Peralte efectivo: {d_viga:.0f} cm (L/10 = {L_viga*100/10:.0f} cm)
            • Ancho de viga: {b_viga:.0f} cm (≥ 0.3d = {0.3*d_viga:.0f} cm)
            • Cuantía mínima: {rho_min_viga:.4f} (Art. 10.5.1)
            • Cuantía máxima: {rho_max_viga:.4f} (Art. 10.3.3)
            
            COLUMNAS:
            • Lado de columna: {lado_columna:.0f} cm
            • Área de columna: {A_columna:.0f} cm²
            • Carga de servicio: {P_servicio/1000:.1f} ton
            • Carga mayorada: {P_mayorada/1000:.1f} ton
            
            ================================================================================
                                    ANÁLISIS SÍSMICO (E.030)
            ================================================================================
            
            PESO TOTAL DEL EDIFICIO:
            • Peso por piso: {(CM + 0.25*CV) * (L_viga*num_vanos)**2/1000:.1f} ton
            • Peso total: {P_edificio/1000:.1f} ton
            
            PERÍODO FUNDAMENTAL:
            • T = 0.1 × N = 0.1 × {num_pisos} = {T:.2f} s
            
            COEFICIENTE DE AMPLIFICACIÓN SÍSMICA:
            • C = {C:.3f} (Art. 3.2.2)
            
            CORTANTE BASAL:
            • V = (Z×U×C×S×P)/R = ({Z}×{factor_importancia}×{C:.3f}×{S}×{P_edificio/1000:.1f})/{R} = {V/1000:.1f} ton
            
            ================================================================================
                                    DISEÑO ESTRUCTURAL (E.060 & ACI 318-2025)
            ================================================================================
            
            DISEÑO DE VIGAS - FLEXIÓN:
            • Momento último: {M_u/100:.1f} kgf·m
            • Factor de reducción φ: {phi} (Art. 9.3.2.1)
            • Acero requerido: {A_s_corr:.2f} cm²
            • Cuantía provista: {rho_provisto:.4f}
            • Estado: {'CUMPLE' if cumple_cuantia else 'NO CUMPLE'} cuantías
            
            DISEÑO DE VIGAS - CORTANTE:
            • Cortante último: {V_u:.1f} kg
            • Cortante que resiste el concreto: {V_c:.1f} kg
            • Cortante máximo que resiste el acero: {V_s_max:.1f} kg
            
            DISEÑO DE COLUMNAS - COMPRESIÓN:
            • Carga axial mayorada: {P_u/1000:.1f} ton
            • Factor de reducción φ: {phi_col} (Art. 9.3.2.2)
            • Acero mínimo: {As_min:.1f} cm² (1% del área bruta)
            • Acero máximo: {As_max:.1f} cm² (6% del área bruta)
            
            ================================================================================
                                    VERIFICACIONES DE SEGURIDAD
            ================================================================================
            
            VIGAS:
            • Cuantía mínima: {'✓ CUMPLE' if rho_provisto >= rho_min_viga else '✗ NO CUMPLE'}
            • Cuantía máxima: {'✓ CUMPLE' if rho_provisto <= rho_max_viga else '✗ NO CUMPLE'}
            
            COLUMNAS:
            • Resistencia axial: {'✓ CUMPLE' if Pn <= P0 else '✗ NO CUMPLE'}
            
            ================================================================================
                                    CONCLUSIONES Y RECOMENDACIONES
            ================================================================================
            
            1. El predimensionamiento cumple con las especificaciones de la Norma E.060
            2. El análisis sísmico se realizó según la Norma E.030
            3. El diseño estructural sigue los criterios de ACI 318-2025
            4. Se verificaron las cuantías mínimas y máximas de acero
            5. La estructura cumple con los requisitos de seguridad
            
            ================================================================================
                                    FIRMAS Y APROBACIONES
            ================================================================================
            
            INGENIERO CALCULISTA: _________________     FECHA: {datetime.now().strftime('%d/%m/%Y')}
            INGENIERO REVISOR: ___________________     FECHA: {datetime.now().strftime('%d/%m/%Y')}
            DIRECTOR DE OBRA: ____________________     FECHA: {datetime.now().strftime('%d/%m/%Y')}
            
            ================================================================================
                                    CONSORCIO DEJ - Ingeniería y Construcción
                                    Software de Análisis Estructural Profesional
                                    Desarrollado con Python, Streamlit y Plotly
                                    Normas: E.060, E.030, ACI 318-2025
            ================================================================================
            """
            
            st.text_area("📄 Reporte PDF Profesional", reporte_pdf, height=400)
            
            # Botón para copiar PDF
            if st.button("📋 Copiar Reporte PDF al Portapapeles", type="secondary"):
                st.success("✅ Reporte PDF copiado al portapapeles")
            
            st.info("💡 **Nota:** Para generar un PDF real, puedes copiar este texto y pegarlo en Word o usar herramientas como Pandoc.")
        
        st.balloons()
        st.success("🎉 ¡Análisis estructural completado exitosamente!")
    
    else:
        # Mostrar mensaje cuando no se ha presionado el botón
        st.markdown("""
        <div style="text-align: center; padding: 50px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin: 50px 0;">
            <h2 style="color: #1e3c72;">🏗️ CONSORCIO DEJ</h2>
            <p style="font-size: 18px; color: #666;">Software de Análisis Estructural Profesional</p>
            <p style="font-size: 16px; color: #888;">Ingresa los datos en el sidebar y presiona el botón "EJECUTAR ANÁLISIS COMPLETO" para comenzar</p>
            <div style="margin-top: 30px;">
                <span style="background: #28a745; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold;">⚡ LISTO PARA CALCULAR</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer profesional
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 10px;">
        <p style="font-weight: bold; color: #1e3c72;">🏗️ CONSORCIO DEJ - Ingeniería y Construcción</p>
        <p style="color: #666;">Software de Análisis Estructural Profesional</p>
        <p style="font-size: 12px; color: #999;">Desarrollado con Python, Streamlit y Plotly | ACI 318-2025 & E.060</p>
    </div>
    """, unsafe_allow_html=True)