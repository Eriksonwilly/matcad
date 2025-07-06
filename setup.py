#!/usr/bin/env python3
"""
Script de instalación para CONSORCIO DEJ - Software de Análisis Estructural
"""

import subprocess
import sys
import os

def install_requirements():
    """Instalar dependencias del proyecto"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al instalar dependencias")
        return False

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def main():
    """Función principal"""
    print("🏗️ CONSORCIO DEJ - Instalador del Software de Análisis Estructural")
    print("=" * 60)
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependencias
    if not install_requirements():
        sys.exit(1)
    
    print("\n🎉 Instalación completada exitosamente!")
    print("\n📋 Para ejecutar la aplicación:")
    print("   streamlit run APP_MEJORADO.py")
    print("\n🌐 Para publicar en Streamlit Cloud:")
    print("   1. Sube el código a GitHub")
    print("   2. Ve a share.streamlit.io")
    print("   3. Conecta tu repositorio")
    print("   4. Deploy!")

if __name__ == "__main__":
    main() 