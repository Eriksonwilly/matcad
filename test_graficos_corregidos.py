#!/usr/bin/env python3
"""
Script de prueba para verificar que los gráficos funcionen correctamente
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo para Streamlit

# Configuración de la página
st.set_page_config(
    page_title="Test Gráficos - CONSORCIO DEJ",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Test de Gráficos - CONSORCIO DEJ")
st.info("Este script prueba que los gráficos funcionen correctamente")

# Función para calcular cortantes y momentos (simplificada)
def calcular_cortantes_momentos_viga_simple(L, w):
    """Calcula cortantes y momentos para viga simplemente apoyada"""
    x = np.linspace(0, L, 100)
    R_A = w * L / 2
    V = R_A - w * x
    M = R_A * x - w * x**2 / 2
    return x, V, M

# Función para graficar (simplificada)
def graficar_cortantes_momentos(L, w):
    """Genera gráficos de cortantes y momentos"""
    x, V, M = calcular_cortantes_momentos_viga_simple(L, w)
    
    # Crear figura con subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Gráfico de cortantes
    ax1.plot(x, V, 'r-', linewidth=2, label='Cortante (V)')
    ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=L, color='k', linestyle='-', alpha=0.3)
    ax1.fill_between(x, V, 0, alpha=0.3, color='red')
    ax1.set_title('Diagrama de Cortantes - Viga Simplemente Apoyada', fontsize=14, fontweight='bold')
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
    ax2.set_title('Diagrama de Momentos - Viga Simplemente Apoyada', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Distancia (m)')
    ax2.set_ylabel('Momento (kg·m)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    return fig

# Interfaz de prueba
st.subheader("🔧 Test de Gráficos de Cortantes y Momentos")

col1, col2 = st.columns(2)
with col1:
    L = st.number_input("Luz de la viga (m)", 1.0, 20.0, 6.0, 0.5)
    w = st.number_input("Carga distribuida (kg/m)", 0.0, 10000.0, 1000.0, 100.0)

with col2:
    st.write("**Parámetros de entrada:**")
    st.write(f"- Luz de la viga: {L} m")
    st.write(f"- Carga distribuida: {w} kg/m")
    st.write(f"- Reacción en apoyos: {w * L / 2:.1f} kg")
    st.write(f"- Momento máximo: {w * L**2 / 8:.1f} kg·m")

if st.button("🔬 Generar Gráficos de Prueba", type="primary"):
    try:
        # Generar gráfico
        fig = graficar_cortantes_momentos(L, w)
        
        # Mostrar gráfico
        st.pyplot(fig)
        
        # Calcular valores máximos
        x, V, M = calcular_cortantes_momentos_viga_simple(L, w)
        
        # Mostrar métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Cortante Máximo", f"{max(abs(V)):.1f} kg")
        with col2:
            st.metric("Momento Máximo", f"{max(abs(M)):.1f} kg·m")
        with col3:
            st.metric("Luz de la Viga", f"{L} m")
        
        st.success("✅ Gráficos generados exitosamente!")
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ Error generando gráficos: {str(e)}")
        st.info("Verifica que matplotlib esté instalado correctamente")

# Información adicional
st.markdown("---")
st.subheader("📚 Información Técnica")
st.markdown("""
**Fórmulas utilizadas:**
- **Reacciones:** R = wL/2
- **Cortante:** V(x) = R - wx
- **Momento:** M(x) = Rx - wx²/2
- **Momento máximo:** M_max = wL²/8 (en el centro)

**Verificaciones:**
- ✅ Matplotlib importado correctamente
- ✅ Backend 'Agg' configurado para Streamlit
- ✅ Funciones de cálculo implementadas
- ✅ Gráficos con subplots funcionando
""")

# Test de importaciones
st.subheader("🔍 Verificación de Importaciones")
try:
    import matplotlib
    st.success(f"✅ Matplotlib versión: {matplotlib.__version__}")
except ImportError:
    st.error("❌ Matplotlib no está instalado")

try:
    import numpy
    st.success(f"✅ NumPy versión: {numpy.__version__}")
except ImportError:
    st.error("❌ NumPy no está instalado")

try:
    import streamlit
    st.success(f"✅ Streamlit versión: {streamlit.__version__}")
except ImportError:
    st.error("❌ Streamlit no está instalado") 