#!/usr/bin/env python3
"""
Script para deployment en Windows - CONSORCIO DEJ
"""

import os
import subprocess
import sys

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    
    print("✅ Versión de Python compatible")
    return True

def install_requirements():
    """Instalar dependencias básicas"""
    print("📦 Instalando dependencias...")
    
    try:
        # Instalar streamlit
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit==1.28.1"])
        print("✅ Streamlit instalado")
        
        # Instalar numpy
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy==1.24.3"])
        print("✅ NumPy instalado")
        
        # Instalar pandas
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas==2.0.3"])
        print("✅ Pandas instalado")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def run_streamlit():
    """Ejecutar aplicación Streamlit"""
    print("🚀 Iniciando CONSORCIO DEJ...")
    
    try:
        # Ejecutar streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "APP.py", "--server.port=8501"])
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando Streamlit: {e}")

def main():
    """Función principal"""
    print("🏗️ CONSORCIO DEJ - Setup para Windows")
    print("=" * 50)
    
    # Verificar Python
    if not check_python_version():
        return
    
    # Instalar dependencias
    if not install_requirements():
        print("❌ No se pudieron instalar las dependencias")
        return
    
    print("\n✅ Setup completado exitosamente!")
    print("🌐 La aplicación se abrirá en tu navegador")
    print("📱 URL: http://localhost:8501")
    print("\n💡 Para cerrar la aplicación, presiona Ctrl+C")
    
    # Ejecutar aplicación
    run_streamlit()

if __name__ == "__main__":
    main() 