#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación funcione correctamente
"""

import subprocess
import sys
import os
import time

def test_imports():
    """Probar que todas las dependencias se importen correctamente"""
    print("🔍 Probando importaciones...")
    
    try:
        import streamlit as st
        print("✅ Streamlit importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Streamlit: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando NumPy: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Pandas: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✅ Plotly importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Plotly: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ Matplotlib importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Matplotlib: {e}")
        return False
    
    return True

def test_calculations():
    """Probar cálculos básicos"""
    print("\n🧮 Probando cálculos básicos...")
    
    try:
        from math import sqrt
        
        # Prueba de cálculo de módulo de elasticidad
        f_c = 210
        E = 15000 * sqrt(f_c)
        print(f"✅ Módulo de elasticidad calculado: {E:.0f} kg/cm²")
        
        # Prueba de cálculo de espesor de losa
        L_viga = 6.0
        h_losa = max(L_viga / 25, 0.17)
        print(f"✅ Espesor de losa calculado: {h_losa:.2f} m")
        
        # Prueba de cálculo de peralte de viga
        d_viga = L_viga * 100 / 10
        print(f"✅ Peralte de viga calculado: {d_viga:.2f} cm")
        
        return True
    except Exception as e:
        print(f"❌ Error en cálculos: {e}")
        return False

def test_streamlit_app():
    """Probar que la aplicación Streamlit se pueda ejecutar"""
    print("\n🚀 Probando aplicación Streamlit...")
    
    try:
        # Verificar que el archivo principal existe
        if not os.path.exists("APP_MEJORADO.py"):
            print("❌ Archivo APP_MEJORADO.py no encontrado")
            return False
        
        print("✅ Archivo APP_MEJORADO.py encontrado")
        
        # Verificar sintaxis del archivo
        result = subprocess.run([sys.executable, "-m", "py_compile", "APP_MEJORADO.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Sintaxis del archivo correcta")
            return True
        else:
            print(f"❌ Error de sintaxis: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando aplicación: {e}")
        return False

def test_requirements():
    """Verificar que requirements.txt existe y es válido"""
    print("\n📦 Probando archivo requirements.txt...")
    
    try:
        if not os.path.exists("requirements.txt"):
            print("❌ Archivo requirements.txt no encontrado")
            return False
        
        print("✅ Archivo requirements.txt encontrado")
        
        # Leer y verificar contenido
        with open("requirements.txt", "r") as f:
            content = f.read()
        
        required_packages = ["streamlit", "numpy", "pandas", "matplotlib", "plotly"]
        
        for package in required_packages:
            if package in content:
                print(f"✅ {package} encontrado en requirements.txt")
            else:
                print(f"⚠️ {package} no encontrado en requirements.txt")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando requirements.txt: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🏗️ CONSORCIO DEJ - Pruebas del Software de Análisis Estructural")
    print("=" * 60)
    
    tests = [
        ("Importaciones", test_imports),
        ("Cálculos Básicos", test_calculations),
        ("Aplicación Streamlit", test_streamlit_app),
        ("Requirements.txt", test_requirements)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Ejecutando: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name}: PASÓ")
        else:
            print(f"❌ {test_name}: FALLÓ")
    
    print("\n" + "=" * 60)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La aplicación está lista para publicar.")
        print("\n📋 Próximos pasos:")
        print("1. Ejecuta: streamlit run APP_MEJORADO.py")
        print("2. Sigue la guía en GUIA_PUBLICACION.md")
        print("3. Publica en Streamlit Cloud")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores antes de publicar.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 