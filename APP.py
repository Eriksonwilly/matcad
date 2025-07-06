import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt

# Configuración de la página
st.set_page_config(page_title="Análisis Estructural Avanzado", layout="wide", page_icon="🏗️")

# Título
st.title("🏗️ Software de Análisis Estructural Avanzado (ACI 318-2025 & E.060)")
st.markdown("---")

# --- 1. DATOS DE ENTRADA ---
st.sidebar.header("📌 Datos Básicos del Proyecto")

# Materiales
f_c = st.sidebar.number_input("Resistencia del concreto f'c (kg/cm²)", min_value=175, max_value=700, value=210)
f_y = st.sidebar.number_input("Esfuerzo de fluencia del acero fy (kg/cm²)", min_value=2800, max_value=6000, value=4200)
E = 15000*sqrt(f_c)  # Módulo de elasticidad del concreto (kg/cm²)

# Geometría
L_viga = st.sidebar.number_input("Luz libre de vigas (m)", min_value=3.0, max_value=12.0, value=6.0)
h_piso = st.sidebar.number_input("Altura de piso (m)", min_value=2.5, max_value=4.5, value=3.0)
num_pisos = st.sidebar.number_input("Número de pisos", min_value=1, max_value=50, value=15)
num_vanos = st.sidebar.number_input("Número de vanos en dirección X", min_value=1, max_value=10, value=3)

# Cargas
CM = st.sidebar.number_input("Carga Muerta (kg/m²)", min_value=100, max_value=1000, value=150)
CV = st.sidebar.number_input("Carga Viva (kg/m²)", min_value=100, max_value=500, value=200)

# Datos sísmicos (E.030)
st.sidebar.header("📌 Parámetros Sísmicos")
zona_sismica = st.sidebar.selectbox("Zona Sísmica", ["Z1", "Z2", "Z3", "Z4"], index=2)
tipo_suelo = st.sidebar.selectbox("Tipo de Suelo", ["S1", "S2", "S3", "S4"], index=1)
tipo_estructura = st.sidebar.selectbox("Tipo de Sistema Estructural", 
                                      ["Pórticos", "Muros Estructurales", "Dual"], index=0)
factor_importancia = st.sidebar.number_input("Factor de Importancia (U)", min_value=1.0, max_value=1.5, value=1.0)

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

# --- 2. PREDIMENSIONAMIENTO ---
st.header("🔧 Predimensionamiento Estructural")

# 2.1 Losas Aligeradas (E.060)
h_losa = max(L_viga / 25, 0.17)  # Espesor mínimo (17 cm mínimo)
rho_min_losa = 0.0018  # Cuantía mínima para losas

st.subheader("Losas Aligeradas")
col1, col2 = st.columns(2)
with col1:
    st.write(f"Espesor mínimo (h): {h_losa:.2f} m")
    st.write(f"Cuantía mínima (ρ): {rho_min_losa:.4f}")

# 2.2 Vigas (ACI 318-2025)
d_viga = L_viga * 100 / 10  # Peralte efectivo (cm)
b_viga = max(0.3 * d_viga, 25)  # Ancho mínimo (25 cm mínimo)
rho_min_viga = max(0.8 * sqrt(f_c) / f_y, 14 / f_y)
rho_max_viga = 0.025  # Para zonas sísmicas

st.subheader("Vigas Principales")
col1, col2 = st.columns(2)
with col1:
    st.write(f"Peralte efectivo (d): {d_viga:.2f} cm")
    st.write(f"Ancho mínimo (b): {b_viga:.2f} cm")
with col2:
    st.write(f"Cuantía mínima (ρ_min): {rho_min_viga:.4f}")
    st.write(f"Cuantía máxima (ρ_max): {rho_max_viga:.4f}")

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

st.subheader("Columnas")
col1, col2 = st.columns(2)
with col1:
    st.write(f"Área bruta requerida (A_g): {A_columna:.2f} cm²")
    st.write(f"Lado mínimo (columna cuadrada): {lado_columna:.2f} cm")
with col2:
    st.write(f"Relación de esbeltez (kLu/r): {relacion_esbeltez:.2f}")
    st.write("✔️ OK (Debe ser < 22 para pórticos arriostrados)" if relacion_esbeltez <= 22 else "⚠️ Requiere análisis de efectos de segundo orden")

# --- 3. ANÁLISIS SÍSMICO ---
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

st.subheader("Resultados del Análisis Sísmico")
col1, col2 = st.columns(2)
with col1:
    st.write(f"Peso total del edificio: {P_edificio/1000:.2f} ton")
    st.write(f"Coeficiente sísmico (C): {C:.3f}")
    st.write(f"Cortante basal (V): {V/1000:.2f} ton")
with col2:
    st.write("**Distribución de fuerzas sísmicas por piso:**")
    for i, fuerza in enumerate(Fx, 1):
        st.write(f"Piso {i}: {fuerza/1000:.2f} ton")

# --- 4. DISEÑO DE ELEMENTOS ---
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

st.subheader("Viga Principal - Flexión")
col1, col2 = st.columns(2)
with col1:
    st.write(f"Momento mayorado (Mu): {M_u/100:.2f} kgf·m")
    st.write(f"Acero requerido (As): {A_s_corr:.2f} cm²")
    st.write(f"ρ provisto: {rho_provisto:.4f}")
with col2:
    st.write(f"ρ mínimo: {rho_min_viga:.4f}")
    st.write(f"ρ máximo: {rho_max_viga:.4f}")
    st.write("✔️ CUMPLE cuantías" if cumple_cuantia else "⚠️ NO CUMPLE cuantías")

# 4.2 Diseño por Cortante
V_u = (1.2*CM + 1.6*CV) * L_viga / 2  # Cortante mayorado (kg)
phi_v = 0.75
V_c = 0.53 * sqrt(f_c) * b_viga * d_viga_cm  # kgf
V_s_max = 2.1 * sqrt(f_c) * b_viga * d_viga_cm  # Límite ACI 318-25

if V_u > phi_v * V_c:
    V_s = (V_u / phi_v) - V_c
    if V_s > V_s_max:
        st.error("¡Sección insuficiente para resistir cortante! Aumentar dimensiones")
    else:
        # Diseño de estribos
        diam_estribo = 0.95  # 3/8"
        Av = 2 * 0.71  # 2 ramas de estribo #3 (cm²)
        s_max = min(d_viga_cm/2, 60)  # cm (ACI 318-25 9.7.6.2)
        s_req = (Av * f_y * d_viga_cm) / V_s  # cm
        
        st.subheader("Viga Principal - Cortante")
        st.write(f"Cortante mayorado (Vu): {V_u:.2f} kgf")
        st.write(f"Resistencia del concreto (Vc): {V_c:.2f} kgf")
        st.write(f"Acero requerido (Vs): {V_s:.2f} kgf")
        st.write(f"Separación de estribos ϕ3/8: {min(s_req, s_max):.2f} cm")
else:
    st.subheader("Viga Principal - Cortante")
    st.write("✔️ El concreto resiste el cortante. Colocar estribos mínimos")
    st.write(f"Separación máxima: {min(d_viga_cm/2, 60):.0f} cm")

# 4.3 Diseño de Columnas
st.subheader("Columnas - Diseño a Compresión")
P_u = P_mayorada  # kg (ya calculado)
phi = 0.65  # Para columnas con estribos
A_g = lado_columna**2  # cm²
As_min = 0.01 * A_g  # Acero mínimo (1%)
As_max = 0.06 * A_g  # Acero máximo (6%)

# Resistencia nominal
Pn = P_u / phi
P0 = 0.85*f_c*(A_g - As_min) + f_y*As_min  # kg

st.write(f"Carga axial mayorada (Pu): {P_u/1000:.2f} ton")
st.write(f"Área de concreto (Ag): {A_g:.2f} cm²")
st.write(f"Acero longitudinal mínimo: {As_min:.2f} cm² (1%)")
st.write(f"Acero longitudinal máximo: {As_max:.2f} cm² (6%)")
st.write(f"Resistencia nominal (Pn): {Pn/1000:.2f} ton")
st.write(f"Resistencia máxima (P0): {P0/1000:.2f} ton")

if Pn <= P0:
    st.success("✔️ La columna resiste la carga axial")
else:
    st.error("⚠️ Aumentar dimensiones de columna o resistencia del concreto")

# --- 5. REPORTE FINAL ---
st.header("📝 Reporte Estructural Completo")

# Resumen de diseño
elementos = {
    "Elemento": ["Losa Aligerada", "Viga Principal", "Columna"],
    "Dimensión": [f"{h_losa*100:.0f} cm", f"{b_viga:.0f}x{d_viga:.0f} cm", f"{lado_columna:.0f}x{lado_columna:.0f} cm"],
    "Acero Longitudinal": ["-", f"{A_s_corr:.2f} cm²", f"{As_min:.2f}-{As_max:.2f} cm² (1%-6%)"],
    "Refuerzo Transversal": ["Malla ϕ4@25cm", "Estribos ϕ3/8@{0:.0f}cm".format(min(s_req, s_max) if 's_req' in locals() else d_viga_cm/2), "Estribos ϕ3/8@30cm"]
}

df = pd.DataFrame(elementos)
st.table(df)

# Gráficos
st.subheader("📊 Visualización de Resultados")

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(range(1, num_pisos+1), [f/1000 for f in Fx], color='steelblue')
ax.set_title("Distribución de Fuerzas Sísmicas por Piso")
ax.set_xlabel("Nivel")
ax.set_ylabel("Fuerza Sísmica (ton)")
ax.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig)

# --- INSTRU@CCIONES FINALES ---
st.markdown("---")
st.success("✅ Análisis estructural completado satisfactoriamente")
st.warning("⚠️ **Nota importante:** Este software proporciona resultados preliminares. Se recomienda validar todos los cálculos con un ingeniero estructural certificado y realizar modelos detallados con software especializado (ETABS, SAP2000, etc.)")