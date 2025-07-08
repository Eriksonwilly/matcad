#!/usr/bin/env python3
"""
Script para ejecutar la aplicación Streamlit y probar la funcionalidad
"""

import subprocess
import time
import sys
import os

def run_streamlit_app():
    """Ejecuta la aplicación Streamlit"""
    print("🚀 Iniciando aplicación Streamlit...")
    
    try:
        # Ejecutar la aplicación en segundo plano
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "APP.py",
            "--server.port", "8506",
            "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Aplicación iniciada en puerto 8506")
        print("🌐 URL: http://localhost:8506")
        print("⏳ Esperando 5 segundos para que la aplicación se inicie...")
        
        time.sleep(5)
        
        # Verificar que la aplicación está corriendo
        import requests
        try:
            response = requests.get("http://localhost:8506", timeout=10)
            if response.status_code == 200:
                print("✅ Aplicación funcionando correctamente")
                print("📋 Instrucciones para probar:")
                print("   1. Abre http://localhost:8506 en tu navegador")
                print("   2. Inicia sesión con admin/admin123")
                print("   3. Ve a '📊 Análisis Completo'")
                print("   4. Ejecuta el análisis")
                print("   5. Ve a '📄 Generar Reporte'")
                print("   6. Haz clic en '📄 Generar PDF Premium'")
                print("   7. Descarga el PDF generado")
            else:
                print(f"⚠️ Aplicación respondió con código: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ No se pudo conectar a la aplicación: {e}")
        
        print("\n🔄 Presiona Ctrl+C para detener la aplicación")
        
        # Mantener la aplicación corriendo
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo aplicación...")
            process.terminate()
            process.wait()
            print("✅ Aplicación detenida")
            
    except Exception as e:
        print(f"❌ Error ejecutando la aplicación: {e}")

if __name__ == "__main__":
    print("🔧 Verificando dependencias...")
    
    # Verificar que ReportLab está instalado
    try:
        import reportlab
        print(f"✅ ReportLab instalado: {reportlab.__version__}")
    except ImportError:
        print("❌ ReportLab no está instalado")
        print("💡 Instala con: pip install reportlab")
        exit(1)
    
    # Verificar que Streamlit está instalado
    try:
        import streamlit
        print(f"✅ Streamlit instalado: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit no está instalado")
        print("💡 Instala con: pip install streamlit")
        exit(1)
    
    print("✅ Todas las dependencias están instaladas")
    print("=" * 50)
    
    # Ejecutar la aplicación
    run_streamlit_app() 