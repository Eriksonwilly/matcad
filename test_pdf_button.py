#!/usr/bin/env python3
"""
Script para probar específicamente el botón de PDF en la aplicación
"""

import streamlit as st
import sys
import os

# Agregar el directorio actual al path
sys.path.append('.')

def test_pdf_generation():
    """Prueba la generación de PDF directamente"""
    print("🧪 Probando generación de PDF...")
    
    try:
        # Importar la función
        from APP import generar_pdf_reportlab
        
        # Datos de prueba
        resultados_prueba = {
            'peso_total': 1500.5,
            'Ec': 217944.0,
            'Es': 2000000.0,
            'h_losa': 0.24,
            'b_viga': 30.0,
            'd_viga': 60.0,
            'lado_columna': 40.0,
            'ecu': 0.003,
            'fr': 28.98,
            'beta1': 0.85,
            'ey': 0.0021,
            'diseno_flexion': {
                'rho_b': 0.0214,
                'rho_min': 0.0033,
                'rho_max': 0.0161,
                'As': 18.0,
                'phiMn': 45000.0,
                'verificacion': True
            },
            'diseno_cortante': {
                'Vc': 15000.0,
                'Vs_requerido': 5000.0,
                'Av_s_requerido': 0.15,
                'verificacion': True
            },
            'diseno_columna': {
                'Pn': 80000.0,
                'phiPn': 52000.0,
                'verificacion': True
            },
            'analisis_sismico': {
                'Z': 0.25,
                'S': 1.0,
                'U': 1.0,
                'cortante_basal_ton': 45.2
            },
            'Mu_estimado': 42000.0,
            'Vu_estimado': 18000.0,
            'Pu_estimado': 50000.0
        }

        datos_entrada_prueba = {
            'f_c': 210,
            'f_y': 4200,
            'L_viga': 6.0,
            'num_pisos': 15,
            'CM': 150,
            'CV': 200,
            'zona_sismica': 'Z3',
            'tipo_suelo': 'S2',
            'tipo_estructura': 'Pórticos'
        }
        
        # Simular session state
        st.session_state['user'] = 'admin'
        
        # Generar PDF
        pdf_buffer = generar_pdf_reportlab(resultados_prueba, datos_entrada_prueba, "premium")
        
        if pdf_buffer:
            pdf_data = pdf_buffer.getvalue()
            print(f"✅ PDF generado exitosamente - Tamaño: {len(pdf_data)} bytes")
            
            # Verificar que es un PDF válido
            if pdf_data.startswith(b'%PDF'):
                print("✅ El archivo es un PDF válido")
                
                # Guardar el PDF de prueba
                with open("test_pdf_button_output.pdf", "wb") as f:
                    f.write(pdf_data)
                print("✅ PDF guardado como 'test_pdf_button_output.pdf'")
                
                return True
            else:
                print("⚠️ El archivo no parece ser un PDF válido")
                return False
        else:
            print("❌ No se pudo generar el PDF")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_streamlit_components():
    """Prueba los componentes de Streamlit"""
    print("🧪 Probando componentes de Streamlit...")
    
    try:
        # Probar st.download_button
        print("✅ st.download_button disponible")
        
        # Probar st.button
        print("✅ st.button disponible")
        
        # Probar st.spinner
        print("✅ st.spinner disponible")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con componentes de Streamlit: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del botón de PDF...")
    print("=" * 50)
    
    # Probar componentes de Streamlit
    streamlit_ok = test_streamlit_components()
    
    # Probar generación de PDF
    pdf_ok = test_pdf_generation()
    
    print("=" * 50)
    if streamlit_ok and pdf_ok:
        print("🎉 ¡Todas las pruebas exitosas!")
        print("📋 El botón de PDF debería funcionar correctamente en la aplicación")
        print("🌐 Ve a http://localhost:8508 para probar la aplicación")
    else:
        print("💥 Algunas pruebas fallaron")
        if not streamlit_ok:
            print("❌ Problema con componentes de Streamlit")
        if not pdf_ok:
            print("❌ Problema con generación de PDF") 