#!/usr/bin/env python3
"""
Script para instalar dependencias y ejecutar la aplicación
CONSORCIO DEJ - Muros de Contención
"""

import subprocess
import sys
import os

def ejecutar_comando(comando, descripcion):
    """Ejecutar un comando y mostrar el resultado"""
    print(f"[INFO] {descripcion}...")
    try:
        resultado = subprocess.run(comando, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {descripcion} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {descripcion}: {e}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("   CONSORCIO DEJ - INSTALACION COMPLETA")
    print("=" * 60)
    print()
    
    # Verificar Python
    print(f"[INFO] Verificando Python...")
    try:
        version = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python: {version.stdout.strip()}")
    except Exception as e:
        print(f"❌ Error verificando Python: {e}")
        return
    
    # Verificar si streamlit está instalado
    try:
        import streamlit
        print("✅ Streamlit ya está instalado")
        streamlit_instalado = True
    except ImportError:
        print("❌ Streamlit no está instalado")
        streamlit_instalado = False
    
    # Instalar streamlit si no está instalado
    if not streamlit_instalado:
        print("[INFO] Instalando Streamlit...")
        if not ejecutar_comando(f"{sys.executable} -m pip install streamlit", "Instalación de Streamlit"):
            print("❌ No se pudo instalar Streamlit")
            return
        
        # Instalar otras dependencias
        dependencias = ["pandas", "numpy", "matplotlib", "plotly", "reportlab", "openpyxl"]
        for dep in dependencias:
            ejecutar_comando(f"{sys.executable} -m pip install {dep}", f"Instalación de {dep}")
    
    # Verificar que APP.py existe
    if not os.path.exists("APP.py"):
        print("❌ ERROR: No se encontró APP.py")
        print("Asegúrate de estar en el directorio correcto")
        return
    
    print()
    print("=" * 60)
    print("   EJECUTANDO APLICACION")
    print("=" * 60)
    print()
    print("🔑 Credenciales de prueba:")
    print("   admin / admin123 (Empresarial)")
    print("   premium@test.com / 123456 (Premium)")
    print("   empresarial@test.com / 123456 (Empresarial)")
    print()
    print("🌐 La aplicación se abrirá en tu navegador...")
    print()
    
    # Ejecutar la aplicación
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "APP.py"])
    except KeyboardInterrupt:
        print("\n👋 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando la aplicación: {e}")

if __name__ == "__main__":
    main() 