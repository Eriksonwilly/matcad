#!/usr/bin/env python3
"""
Verificación de archivos para deployment en Streamlit Cloud
"""

import os
import sys

def check_files():
    """Verificar que todos los archivos necesarios estén presentes"""
    required_files = [
        'APP.py',
        'requirements.txt',
        'packages.txt',
        '.streamlit/config.toml',
        'setup.sh',
        'README.md',
        '.gitignore'
    ]
    
    missing_files = []
    
    print("🔍 Verificando archivos para deployment...")
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - FALTANTE")
            missing_files.append(file_path)
    
    return missing_files

def check_requirements():
    """Verificar archivo requirements.txt"""
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt no encontrado")
        return False
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    required_packages = [
        'streamlit',
        'numpy',
        'pandas'
    ]
    
    optional_packages = [
        'plotly',
        'reportlab'
    ]
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        if package not in content:
            missing_required.append(package)
    
    for package in optional_packages:
        if package not in content:
            missing_optional.append(package)
    
    if missing_required:
        print(f"❌ Paquetes requeridos faltantes en requirements.txt: {', '.join(missing_required)}")
        return False
    
    if missing_optional:
        print(f"ℹ️ Paquetes opcionales no incluidos: {', '.join(missing_optional)}")
    
    print("✅ requirements.txt verificado")
    return True

def check_config():
    """Verificar configuración de Streamlit"""
    config_path = '.streamlit/config.toml'
    
    if not os.path.exists(config_path):
        print("❌ .streamlit/config.toml no encontrado")
        return False
    
    with open(config_path, 'r') as f:
        content = f.read()
    
    required_configs = [
        'headless = true',
        'port = 8501'
    ]
    
    missing_configs = []
    
    for config in required_configs:
        if config not in content:
            missing_configs.append(config)
    
    if missing_configs:
        print(f"⚠️ Configuraciones faltantes: {', '.join(missing_configs)}")
        return False
    
    print("✅ Configuración de Streamlit verificada")
    return True

def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN DE DEPLOYMENT - CONSORCIO DEJ")
    print("=" * 50)
    
    # Verificar archivos
    missing_files = check_files()
    
    # Verificar requirements
    requirements_ok = check_requirements()
    
    # Verificar configuración
    config_ok = check_config()
    
    print("\n" + "=" * 50)
    
    if not missing_files and requirements_ok and config_ok:
        print("🎉 ¡TODOS LOS ARCHIVOS ESTÁN LISTOS PARA DEPLOYMENT!")
        print("\n📋 Próximos pasos:")
        print("1. git add .")
        print("2. git commit -m 'CONSORCIO DEJ v2.0 - Ready for deployment'")
        print("3. git push origin main")
        print("4. Ve a https://share.streamlit.io")
        print("5. Conecta tu repositorio")
        print("6. Deploy automático")
        print("\n✅ Tu app estará lista en minutos!")
        
        print("\n🖥️ Para ejecutar localmente en Windows:")
        print("1. Doble clic en 'run_app.bat'")
        print("2. O ejecuta: python deploy_windows.py")
        print("3. O ejecuta: streamlit run APP.py")
    else:
        print("⚠️ Hay problemas que deben corregirse antes del deployment:")
        
        if missing_files:
            print(f"• Archivos faltantes: {', '.join(missing_files)}")
        
        if not requirements_ok:
            print("• Problemas en requirements.txt")
        
        if not config_ok:
            print("• Problemas en configuración de Streamlit")
        
        print("\n🔧 Corrige estos problemas y ejecuta la verificación nuevamente")

if __name__ == "__main__":
    main() 