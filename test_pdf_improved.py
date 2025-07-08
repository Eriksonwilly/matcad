#!/usr/bin/env python3
"""
Script de prueba mejorado para verificar la generación de PDF
"""

import io
import sys
from datetime import datetime

# Agregar el directorio actual al path para importar APP
sys.path.append('.')

# Importar la función de generación de PDF
try:
    from APP import generar_pdf_reportlab
    print("✅ Función importada correctamente")
except ImportError as e:
    print(f"❌ Error importando: {e}")
    exit(1)

# Datos de prueba mejorados
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

def test_pdf_generation():
    """Prueba la generación de PDF"""
    print("🔬 Probando generación de PDF...")
    
    try:
        # Generar PDF premium
        pdf_buffer = generar_pdf_reportlab(resultados_prueba, datos_entrada_prueba, "premium")
        
        if pdf_buffer:
            # Verificar que el buffer contiene datos
            pdf_data = pdf_buffer.getvalue()
            print(f"✅ PDF generado exitosamente - Tamaño: {len(pdf_data)} bytes")
            
            # Verificar que es un PDF válido
            if pdf_data.startswith(b'%PDF'):
                print("✅ El archivo es un PDF válido")
                
                # Guardar el PDF de prueba
                with open("test_pdf_improved.pdf", "wb") as f:
                    f.write(pdf_data)
                print("✅ PDF guardado como 'test_pdf_improved.pdf'")
                
                # Mostrar información del PDF
                print(f"📄 Tamaño del archivo: {len(pdf_data)} bytes")
                print(f"📅 Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                
                return True
            else:
                print("⚠️ El archivo no parece ser un PDF válido")
                print(f"Primeros bytes: {pdf_data[:50]}")
                return False
        else:
            print("❌ No se pudo generar el PDF")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la generación: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_pdf():
    """Prueba la generación de PDF básico"""
    print("\n🔬 Probando generación de PDF básico...")
    
    try:
        # Generar PDF básico
        pdf_buffer = generar_pdf_reportlab(resultados_prueba, datos_entrada_prueba, "gratuito")
        
        if pdf_buffer:
            pdf_data = pdf_buffer.getvalue()
            print(f"✅ PDF básico generado - Tamaño: {len(pdf_data)} bytes")
            
            with open("test_pdf_basic.pdf", "wb") as f:
                f.write(pdf_data)
            print("✅ PDF básico guardado como 'test_pdf_basic.pdf'")
            return True
        else:
            print("❌ No se pudo generar el PDF básico")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la generación básica: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de generación de PDF...")
    print("=" * 50)
    
    # Probar PDF premium
    success_premium = test_pdf_generation()
    
    # Probar PDF básico
    success_basic = test_basic_pdf()
    
    print("=" * 50)
    if success_premium and success_basic:
        print("🎉 ¡Todas las pruebas exitosas! Los PDFs se generaron correctamente.")
        print("📁 Archivos generados:")
        print("   - test_pdf_improved.pdf (Premium)")
        print("   - test_pdf_basic.pdf (Básico)")
    else:
        print("💥 Algunas pruebas fallaron. Revisar errores arriba.") 