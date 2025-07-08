#!/usr/bin/env python3
"""
Script de prueba para verificar gráficos en Streamlit
"""

import streamlit as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

def main():
    st.set_page_config(page_title="Prueba de Gráficos", layout="wide")
    
    st.title("🧪 Prueba de Gráficos en Streamlit")
    st.write("Verificando que matplotlib funcione correctamente en la web...")
    
    # Prueba 1: Gráfico simple
    st.subheader("1. Gráfico Simple de Línea")
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y, 'b-', linewidth=2, label='sin(x)')
        ax.set_title('Función Seno - Prueba de Matplotlib')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, alpha=0.3)
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)
        st.success("✅ Gráfico simple generado correctamente")
    except Exception as e:
        st.error(f"❌ Error en gráfico simple: {str(e)}")
    
    # Prueba 2: Gráfico de barras
    st.subheader("2. Gráfico de Barras")
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        categorias = ['Concreto', 'Acero', 'Madera', 'Aluminio']
        valores = [210, 4200, 120, 7000]  # kg/cm²
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        bars = ax.bar(categorias, valores, color=colors)
        ax.set_title('Resistencias de Materiales')
        ax.set_ylabel('Resistencia (kg/cm²)')
        
        # Agregar valores en las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                   f'{height}', ha='center', va='bottom')
        
        st.pyplot(fig)
        plt.close(fig)
        st.success("✅ Gráfico de barras generado correctamente")
    except Exception as e:
        st.error(f"❌ Error en gráfico de barras: {str(e)}")
    
    # Prueba 3: Gráfico de cortantes y momentos
    st.subheader("3. Gráfico de Cortantes y Momentos (Prueba)")
    try:
        # Datos de ejemplo
        L = 6.0  # m
        w = 1000  # kg/m
        x = np.linspace(0, L, 100)
        
        # Cálculos simples
        R_A = w * L / 2
        V = R_A - w * x
        M = R_A * x - w * x**2 / 2
        
        # Crear figura con subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Gráfico de cortantes
        ax1.plot(x, V, 'r-', linewidth=2, label='Cortante (V)')
        ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax1.fill_between(x, V, 0, alpha=0.3, color='red')
        ax1.set_title('Diagrama de Cortantes - Viga Simplemente Apoyada')
        ax1.set_xlabel('Distancia (m)')
        ax1.set_ylabel('Cortante (kg)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Gráfico de momentos
        ax2.plot(x, M, 'b-', linewidth=2, label='Momento (M)')
        ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax2.fill_between(x, M, 0, alpha=0.3, color='blue')
        ax2.set_title('Diagrama de Momentos - Viga Simplemente Apoyada')
        ax2.set_xlabel('Distancia (m)')
        ax2.set_ylabel('Momento (kg·m)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.success("✅ Gráfico de cortantes y momentos generado correctamente")
    except Exception as e:
        st.error(f"❌ Error en gráfico de cortantes/momentos: {str(e)}")
    
    # Información del sistema
    st.subheader("4. Información del Sistema")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Matplotlib", matplotlib.__version__)
    with col2:
        st.metric("NumPy", np.__version__)
    with col3:
        st.metric("Streamlit", st.__version__)
    
    # Instrucciones
    st.subheader("5. Instrucciones para la App Principal")
    st.info("""
    **Para ver gráficos en la app principal:**
    
    1. **Accede a:** http://localhost:8520
    2. **Inicia sesión como admin:**
       - Usuario: `admin`
       - Contraseña: `admin123`
    3. **Ve a "📈 Gráficos"**
    4. **Selecciona "🔧 Cortantes y Momentos (McCormac)"**
    5. **Configura los parámetros y genera diagramas**
    
    **Para el PDF Premium:**
    1. Ve a "Generar Reporte"
    2. Descarga el "PDF Premium"
    3. Verifica que incluya gráficos
    """)

if __name__ == "__main__":
    main() 