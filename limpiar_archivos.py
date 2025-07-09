#!/usr/bin/env python3
"""
Script para limpiar archivos innecesarios antes de subir a GitHub
CONSORCIO DEJ - Muros de Contención
"""

import os
import shutil
import glob

def limpiar_archivos():
    """Limpiar archivos y carpetas innecesarios"""
    
    print("=" * 60)
    print("   CONSORCIO DEJ - LIMPIEZA DE ARCHIVOS")
    print("=" * 60)
    print()
    
    # Lista de carpetas y archivos a eliminar
    carpetas_a_eliminar = [
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".cache",
        "build",
        "dist",
        "*.egg-info",
        "*.dist-info"
    ]
    
    # Carpetas de versiones específicas
    versiones = [
        "1.28.0", "2.0.0", "3.7.0", "1.24.0", "5.15.0", "4.0.0", "3.1.0",
        "1.17.1", "1.5.1", "0.4.6", "1.3.2", "45.0.4", "0.8.0", "0.12.1",
        "2.9.0.post0", "1.1.0", "6.0.2", "4.58.4", "1.1", "3.10", "1.4.8",
        "5.4.0", "3.10.3", "2.3.0", "1.3.0", "25.0", "11.2.1", "25.1.1",
        "2.22", "0.27.0", "0.29.0", "5.6.0", "6.4.2.2.3", "6.4.3", "13.10.2",
        "6.4.2.3.3", "6.4.2", "6.9.1", "0.6.6", "2025.6.15", "5.2.0", "3.4.2",
        "8.2.1", "2025.2", "5.3.1", "5.0.0", "2.4.0", "0.5.1", "0.2.17"
    ]
    
    # Archivos a eliminar
    archivos_a_eliminar = [
        "*.pyc",
        "*.pyo",
        "*.pyd",
        "*.so",
        "*.egg",
        "*.log",
        ".DS_Store",
        "Thumbs.db"
    ]
    
    total_eliminados = 0
    
    print("🧹 Limpiando archivos innecesarios...")
    print()
    
    # Eliminar carpetas de versiones
    for version in versiones:
        if os.path.exists(version):
            try:
                shutil.rmtree(version)
                print(f"✅ Eliminada carpeta: {version}")
                total_eliminados += 1
            except Exception as e:
                print(f"⚠️ Error eliminando {version}: {e}")
    
    # Eliminar carpetas generales
    for carpeta in carpetas_a_eliminar:
        if os.path.exists(carpeta):
            try:
                shutil.rmtree(carpeta)
                print(f"✅ Eliminada carpeta: {carpeta}")
                total_eliminados += 1
            except Exception as e:
                print(f"⚠️ Error eliminando {carpeta}: {e}")
    
    # Eliminar archivos específicos
    for patron in archivos_a_eliminar:
        archivos = glob.glob(patron)
        for archivo in archivos:
            try:
                os.remove(archivo)
                print(f"✅ Eliminado archivo: {archivo}")
                total_eliminados += 1
            except Exception as e:
                print(f"⚠️ Error eliminando {archivo}: {e}")
    
    # Buscar carpetas __pycache__ recursivamente
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                try:
                    shutil.rmtree(os.path.join(root, dir_name))
                    print(f"✅ Eliminada carpeta: {os.path.join(root, dir_name)}")
                    total_eliminados += 1
                except Exception as e:
                    print(f"⚠️ Error eliminando {dir_name}: {e}")
    
    print()
    print("=" * 60)
    print(f"   LIMPIEZA COMPLETADA: {total_eliminados} elementos eliminados")
    print("=" * 60)
    print()
    
    # Mostrar archivos importantes que SÍ deben subirse
    print("📁 Archivos importantes que SÍ debes subir a GitHub:")
    print()
    
    archivos_importantes = [
        "APP.py",
        "requirements.txt",
        ".gitignore",
        "README.md",
        "*.bat",
        "*.ps1",
        "ejecutar_app.py",
        "SOLUCION_RAPIDA_ADMIN.py"
    ]
    
    for archivo in archivos_importantes:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            archivos_glob = glob.glob(archivo)
            for archivo_glob in archivos_glob:
                print(f"✅ {archivo_glob}")
    
    print()
    print("🚀 Ahora puedes subir tu proyecto a GitHub de manera segura!")
    print()
    print("Comandos para GitHub:")
    print("git add .")
    print("git commit -m 'CONSORCIO DEJ - Muros de Contención'")
    print("git push origin main")

if __name__ == "__main__":
    limpiar_archivos() 