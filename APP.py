import streamlit as st
import numpy as np
import pandas as pd
from math import sqrt
from datetime import datetime
import hashlib
import io
import base64

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

# =====================
# INTERFAZ STREAMLIT
# =====================

# Portada mejorada estilo APP1.py
st.markdown("""
<div style="text-align: center; padding: 20px; background-color: #FFD700; color: #2F2F2F; border-radius: 10px; margin-bottom: 20px; border: 2px solid #FFA500;">
    <h1>🏗️ CONSORCIO DEJ</h1>
    <p style="font-size: 18px; font-weight: bold;">Ingeniería y Construcción</p>
    <p style="font-size: 14px;">Software de Análisis Estructural Profesional</p>
</div>
""", unsafe_allow_html=True)

st.set_page_config(page_title="CONSORCIO DEJ - Análisis Estructural", page_icon="🏗️", layout="wide")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🏗️ CONSORCIO DEJ - Ingeniería y Construcción")
    st.subheader("Software de Análisis Estructural Profesional")
    st.info("ACI 318-2025 & E.060 | E.030")
    with st.form("login_form"):
        username = st.text_input("Usuario", placeholder="admin o demo")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar Sesión")
        if submitted:
            if check_credentials(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.plan = get_user_plan(username)
                st.success("¡Bienvenido!")
                st.rerun()
            else:
                st.error("Credenciales incorrectas. Usa admin/admin123 o demo/demo123.")
    st.stop()

# Sidebar de navegación y datos
with st.sidebar:
    st.header(f"👤 Usuario: {st.session_state.username.upper()}")
    plan = st.session_state.get('plan', 'basico')
    if plan == "basico":
        st.info("🆓 Plan Básico")
    else:
        st.success("🏢 Plan Empresarial")
    st.markdown("---")
    opcion = st.selectbox(
        "Menú",
        [
            "🏗️ Cálculo Básico",
            "📊 Análisis Completo",
            "📄 Reporte",
            "📚 Fórmulas de Diseño Estructural",
            "ℹ️ Acerca de"
        ],
        index=0
    )
    st.markdown("---")
    st.header("📋 Datos del Proyecto")
    f_c = st.number_input("f'c (kg/cm²)", 175, 700, 210, 10)
    f_y = st.number_input("fy (kg/cm²)", 2800, 6000, 4200, 100)
    L_viga = st.number_input("Luz libre de vigas (m)", 3.0, 15.0, 6.0, 0.5)
    h_piso = st.number_input("Altura de piso (m)", 2.5, 5.0, 3.0, 0.1)
    num_pisos = st.number_input("Número de pisos", 1, 100, 15, 1)
    num_vanos = st.number_input("Número de vanos", 1, 20, 3, 1)
    CM = st.number_input("Carga Muerta (kg/m²)", 100, 2000, 150, 50)
    CV = st.number_input("Carga Viva (kg/m²)", 100, 1000, 200, 50)
    zona_sismica = st.selectbox("Zona Sísmica", ["Z1", "Z2", "Z3", "Z4"], 2)
    tipo_suelo = st.selectbox("Tipo de Suelo", ["S1", "S2", "S3", "S4"], 1)
    tipo_estructura = st.selectbox("Tipo de Sistema Estructural", ["Pórticos", "Muros Estructurales", "Dual"], 0)
    factor_importancia = st.number_input("Factor de Importancia (U)", 1.0, 1.5, 1.0, 0.1)

# =====================
# MENÚ PRINCIPAL
# =====================
if opcion == "🏗️ Cálculo Básico":
    st.header("🏗️ Cálculo Básico de Análisis Estructural")
    peso_total = num_pisos * L_viga * num_vanos * h_piso * f_c / 1000
    st.write(f"**Peso total estimado:** {peso_total:.1f} ton")
    st.write(f"**f'c:** {f_c} kg/cm² | **fy:** {f_y} kg/cm²")
    st.write(f"**Luz libre:** {L_viga} m | **Pisos:** {num_pisos}")
    st.write(f"**Carga Muerta:** {CM} kg/m² | **Carga Viva:** {CV} kg/m²")
    st.write(f"**Zona Sísmica:** {zona_sismica} | **Tipo de Suelo:** {tipo_suelo}")
    st.write(f"**Tipo de Estructura:** {tipo_estructura}")
    st.success("Cálculo básico completado.")

elif opcion == "📊 Análisis Completo":
    st.header("📊 Análisis Completo de Estructuras")
    props_concreto = calcular_propiedades_concreto(f_c)
    props_acero = calcular_propiedades_acero(f_y)
    predim = calcular_predimensionamiento(L_viga, num_pisos, num_vanos, CM, CV, f_c, f_y)
    st.write(f"**Módulo de elasticidad del concreto (Ec):** {props_concreto['Ec']:.0f} kg/cm²")
    st.write(f"**Deformación última del concreto (εcu):** {props_concreto['ecu']}")
    st.write(f"**Resistencia a tracción (fr):** {props_concreto['fr']:.1f} kg/cm²")
    st.write(f"**β1:** {props_concreto['beta1']:.3f}")
    st.write(f"**Módulo de elasticidad del acero (Es):** {props_acero['Es']:,} kg/cm²")
    st.write(f"**Deformación de fluencia (εy):** {props_acero['ey']:.4f}")
    st.write(f"**Espesor de losa:** {predim['h_losa']*100:.0f} cm")
    st.write(f"**Dimensiones de viga:** {predim['b_viga']:.0f}×{predim['d_viga']:.0f} cm")
    st.write(f"**Dimensiones de columna:** {predim['lado_columna']:.0f}×{predim['lado_columna']:.0f} cm")
    st.success("Análisis completo realizado.")

elif opcion == "📄 Reporte":
    st.header("📄 Reporte Estructural")
    st.write("**Fecha:**", datetime.now().strftime('%d/%m/%Y %H:%M'))
    st.write(f"**Usuario:** {st.session_state.username}")
    st.write(f"**f'c:** {f_c} kg/cm² | **fy:** {f_y} kg/cm²")
    st.write(f"**Luz libre:** {L_viga} m | **Pisos:** {num_pisos}")
    st.write(f"**Zona Sísmica:** {zona_sismica} | **Tipo de Suelo:** {tipo_suelo}")
    st.write(f"**Tipo de Estructura:** {tipo_estructura}")
    
    # Calcular predimensionamiento para el reporte
    predim = calcular_predimensionamiento(L_viga, num_pisos, num_vanos, CM, CV, f_c, f_y)
    st.write(f"**Espesor de losa:** {predim['h_losa']*100:.0f} cm")
    st.write(f"**Dimensiones de viga:** {predim['b_viga']:.0f}×{predim['d_viga']:.0f} cm")
    st.write(f"**Dimensiones de columna:** {predim['lado_columna']:.0f}×{predim['lado_columna']:.0f} cm")
    st.success("Reporte generado. Copia y pega estos resultados para tu informe.")

elif opcion == "📚 Fórmulas de Diseño Estructural":
    st.header("📚 Fórmulas de Diseño Estructural")
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

elif opcion == "ℹ️ Acerca de":
    st.header("ℹ️ Acerca de CONSORCIO DEJ")
    st.write("Software profesional para análisis y diseño estructural según ACI 318-2025 y E.060.")
    st.write("Desarrollado por CONSORCIO DEJ - Ingeniería y Construcción.")
    st.write("Contacto: info@consorciodej.com | WhatsApp: +51 999 888 777")