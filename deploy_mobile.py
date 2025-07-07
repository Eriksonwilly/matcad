#!/usr/bin/env python3
"""
🚀 Script de Automatización para Deploy Mobile - CONSORCIO DEJ
Genera automáticamente una app móvil desde tu aplicación Streamlit
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

def print_banner():
    """Imprime el banner de la aplicación"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🏗️ CONSORCIO DEJ                          ║
    ║              🚀 Generador de App Móvil                       ║
    ║                                                              ║
    ║  Análisis Estructural Profesional - ACI 318-2025            ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        'streamlit', 'numpy', 'pandas', 'plotly', 'reportlab'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - FALTANTE")
    
    if missing_packages:
        print(f"\n⚠️  Instalando paquetes faltantes: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Paquetes instalados correctamente")
        except subprocess.CalledProcessError:
            print("❌ Error al instalar paquetes")
            return False
    
    return True

def create_mobile_directory():
    """Crea el directorio para la app móvil"""
    print("\n📁 Creando directorio para app móvil...")
    
    mobile_dir = Path("consorcio-dej-mobile")
    if mobile_dir.exists():
        shutil.rmtree(mobile_dir)
    
    mobile_dir.mkdir()
    
    # Crear subdirectorios
    (mobile_dir / ".streamlit").mkdir()
    (mobile_dir / "assets").mkdir()
    
    print("✅ Directorio creado: consorcio-dej-mobile/")
    return mobile_dir

def copy_files(mobile_dir):
    """Copia los archivos necesarios"""
    print("\n📋 Copiando archivos...")
    
    # Archivos principales
    files_to_copy = [
        ("streamlit_app.py", "streamlit_app.py"),
        ("requirements.txt", "requirements.txt"),
        (".streamlit/config.toml", ".streamlit/config.toml"),
        ("README_APK.md", "README.md")
    ]
    
    for src, dst in files_to_copy:
        src_path = Path(src)
        dst_path = mobile_dir / dst
        
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            print(f"✅ {src} → {dst}")
        else:
            print(f"⚠️  {src} no encontrado")
    
    return True

def create_manifest(mobile_dir):
    """Crea el manifest.json para PWA"""
    print("\n📱 Creando manifest.json para PWA...")
    
    manifest_content = {
        "name": "CONSORCIO DEJ - Análisis Estructural",
        "short_name": "CONSORCIO DEJ",
        "description": "Software de Análisis Estructural Profesional",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#FFD700",
        "theme_color": "#FFA500",
        "icons": [
            {
                "src": "assets/icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "assets/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    
    import json
    manifest_path = mobile_dir / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_content, f, indent=2, ensure_ascii=False)
    
    print("✅ manifest.json creado")
    return True

def create_service_worker(mobile_dir):
    """Crea el service worker para PWA"""
    print("\n⚙️  Creando service worker...")
    
    sw_content = """
// Service Worker para CONSORCIO DEJ
const CACHE_NAME = 'consorcio-dej-v2.0';
const urlsToCache = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
"""
    
    sw_path = mobile_dir / "sw.js"
    with open(sw_path, 'w', encoding='utf-8') as f:
        f.write(sw_content)
    
    print("✅ Service worker creado")
    return True

def create_deployment_script(mobile_dir):
    """Crea script de deployment"""
    print("\n🚀 Creando script de deployment...")
    
    deploy_script = """#!/bin/bash
# Script de deployment para CONSORCIO DEJ Mobile

echo "🚀 Iniciando deployment de CONSORCIO DEJ Mobile..."

# Verificar que estamos en el directorio correcto
if [ ! -f "streamlit_app.py" ]; then
    echo "❌ Error: No se encontró streamlit_app.py"
    exit 1
fi

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Probar la aplicación localmente
echo "🧪 Probando aplicación..."
streamlit run streamlit_app.py --server.headless true --server.port 8501 &

# Esperar a que la app esté lista
sleep 5

echo "✅ Aplicación lista en http://localhost:8501"
echo ""
echo "📱 Para deploy en Streamlit Cloud:"
echo "1. Sube este directorio a GitHub"
echo "2. Ve a https://share.streamlit.io"
echo "3. Conecta tu repositorio"
echo "4. Deploy automático"
echo ""
echo "🔗 Tu app estará disponible en:"
echo "https://tu-usuario-consorcio-dej.streamlit.app"
"""
    
    deploy_path = mobile_dir / "deploy.sh"
    with open(deploy_path, 'w', encoding='utf-8') as f:
        f.write(deploy_script)
    
    # Hacer ejecutable en Unix
    if os.name != 'nt':  # No Windows
        os.chmod(deploy_path, 0o755)
    
    print("✅ Script de deployment creado")
    return True

def create_gitignore(mobile_dir):
    """Crea .gitignore"""
    print("\n📝 Creando .gitignore...")
    
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Streamlit
.streamlit/secrets.toml

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
"""
    
    gitignore_path = mobile_dir / ".gitignore"
    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore creado")
    return True

def show_next_steps(mobile_dir):
    """Muestra los siguientes pasos"""
    print("\n" + "="*60)
    print("🎉 ¡APP MÓVIL CREADA EXITOSAMENTE!")
    print("="*60)
    
    print(f"\n📁 Directorio creado: {mobile_dir.absolute()}")
    
    print("\n📋 Archivos generados:")
    for file_path in mobile_dir.rglob("*"):
        if file_path.is_file():
            rel_path = file_path.relative_to(mobile_dir)
            print(f"   ✅ {rel_path}")
    
    print("\n🚀 PRÓXIMOS PASOS:")
    print("1. 📱 Probar la app:")
    print(f"   cd {mobile_dir}")
    print("   streamlit run streamlit_app.py")
    
    print("\n2. 📤 Subir a GitHub:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'CONSORCIO DEJ Mobile App'")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/tuusuario/consorcio-dej-mobile.git")
    print("   git push -u origin main")
    
    print("\n3. 🌐 Deploy en Streamlit Cloud:")
    print("   • Ve a https://share.streamlit.io")
    print("   • Conecta tu cuenta de GitHub")
    print("   • Selecciona el repositorio")
    print("   • Deploy automático")
    
    print("\n4. 📱 Compartir:")
    print("   • Envía el enlace de Streamlit Cloud")
    print("   • Los usuarios pueden acceder desde móviles")
    print("   • Funciona como una app nativa")
    
    print("\n" + "="*60)
    print("🎯 ¡Tu app estará lista en menos de 10 minutos!")
    print("="*60)

def main():
    """Función principal"""
    print_banner()
    
    # Verificar dependencias
    if not check_dependencies():
        print("❌ Error: No se pudieron instalar las dependencias")
        return
    
    # Crear directorio
    mobile_dir = create_mobile_directory()
    
    # Copiar archivos
    if not copy_files(mobile_dir):
        print("❌ Error: No se pudieron copiar los archivos")
        return
    
    # Crear archivos adicionales
    create_manifest(mobile_dir)
    create_service_worker(mobile_dir)
    create_deployment_script(mobile_dir)
    create_gitignore(mobile_dir)
    
    # Mostrar próximos pasos
    show_next_steps(mobile_dir)

if __name__ == "__main__":
    main() 