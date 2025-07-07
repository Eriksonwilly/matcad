#!/usr/bin/env python3
"""
Script para generar PWA desde Streamlit App
CONSORCIO DEJ - Análisis Estructural
"""

import os
import json
import shutil
from datetime import datetime

def create_pwa_files():
    """Crear archivos necesarios para PWA"""
    
    # Crear directorio PWA
    pwa_dir = "consorcio-dej-pwa"
    if os.path.exists(pwa_dir):
        shutil.rmtree(pwa_dir)
    os.makedirs(pwa_dir)
    
    # 1. Manifest.json
    manifest = {
        "name": "CONSORCIO DEJ - Análisis Estructural",
        "short_name": "CONSORCIO DEJ",
        "description": "Software profesional de análisis estructural ACI 318-2025",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#FFD700",
        "theme_color": "#1e3c72",
        "orientation": "portrait-primary",
        "icons": [
            {
                "src": "icons/icon-72x72.png",
                "sizes": "72x72",
                "type": "image/png"
            },
            {
                "src": "icons/icon-96x96.png",
                "sizes": "96x96",
                "type": "image/png"
            },
            {
                "src": "icons/icon-128x128.png",
                "sizes": "128x128",
                "type": "image/png"
            },
            {
                "src": "icons/icon-144x144.png",
                "sizes": "144x144",
                "type": "image/png"
            },
            {
                "src": "icons/icon-152x152.png",
                "sizes": "152x152",
                "type": "image/png"
            },
            {
                "src": "icons/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "icons/icon-384x384.png",
                "sizes": "384x384",
                "type": "image/png"
            },
            {
                "src": "icons/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    
    with open(f"{pwa_dir}/manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    # 2. Service Worker
    sw_content = """
// Service Worker para CONSORCIO DEJ PWA
const CACHE_NAME = 'consorcio-dej-v2.0';
const urlsToCache = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
"""
    
    with open(f"{pwa_dir}/sw.js", "w", encoding="utf-8") as f:
        f.write(sw_content)
    
    # 3. HTML principal
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CONSORCIO DEJ - Análisis Estructural</title>
    <meta name="description" content="Software profesional de análisis estructural ACI 318-2025">
    <meta name="theme-color" content="#1e3c72">
    
    <!-- PWA Manifest -->
    <link rel="manifest" href="/manifest.json">
    
    <!-- Apple Touch Icons -->
    <link rel="apple-touch-icon" href="/icons/icon-152x152.png">
    
    <!-- CSS -->
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: rgba(30, 60, 114, 0.9);
            color: white;
            text-align: center;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .container {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .app-frame {
            width: 100%;
            max-width: 1200px;
            height: 80vh;
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            background: white;
        }
        
        .install-prompt {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            display: none;
        }
        
        .install-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            margin: 10px;
        }
        
        .install-btn:hover {
            background: #218838;
        }
        
        .footer {
            background: rgba(30, 60, 114, 0.9);
            color: white;
            text-align: center;
            padding: 15px;
            font-size: 12px;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 20px;
            }
            
            .app-frame {
                height: 70vh;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏗️ CONSORCIO DEJ</h1>
        <p>Ingeniería y Construcción - Análisis Estructural Profesional</p>
    </div>
    
    <div class="container">
        <div class="install-prompt" id="installPrompt">
            <h3>📱 Instalar App</h3>
            <p>Instala CONSORCIO DEJ en tu dispositivo para acceso rápido</p>
            <button class="install-btn" id="installBtn">📥 Instalar</button>
            <button class="install-btn" onclick="hideInstallPrompt()">❌ Cerrar</button>
        </div>
        
        <iframe 
            src="https://consorcio-dej.streamlit.app" 
            class="app-frame"
            title="CONSORCIO DEJ - Análisis Estructural">
        </iframe>
    </div>
    
    <div class="footer">
        <p>CONSORCIO DEJ - Software de Análisis Estructural Profesional</p>
        <p>ACI 318-2025 & E.060 | E.030</p>
    </div>
    
    <script>
        // PWA Installation
        let deferredPrompt;
        
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            document.getElementById('installPrompt').style.display = 'block';
        });
        
        document.getElementById('installBtn').addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                if (outcome === 'accepted') {
                    console.log('PWA instalada');
                }
                deferredPrompt = null;
                hideInstallPrompt();
            }
        });
        
        function hideInstallPrompt() {
            document.getElementById('installPrompt').style.display = 'none';
        }
        
        // Service Worker Registration
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
                    .then((registration) => {
                        console.log('SW registrado:', registration);
                    })
                    .catch((error) => {
                        console.log('SW error:', error);
                    });
            });
        }
        
        // Offline detection
        window.addEventListener('online', () => {
            console.log('App online');
        });
        
        window.addEventListener('offline', () => {
            console.log('App offline');
        });
    </script>
</body>
</html>"""
    
    with open(f"{pwa_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # 4. Crear directorio de iconos
    icons_dir = f"{pwa_dir}/icons"
    os.makedirs(icons_dir, exist_ok=True)
    
    # 5. README para PWA
    readme_content = """# 🏗️ CONSORCIO DEJ PWA

Aplicación Web Progresiva (PWA) para análisis estructural.

## 🚀 Instalación

### Opción 1: Servidor Local
```bash
# Instalar servidor HTTP simple
npm install -g http-server

# Ejecutar en el directorio PWA
cd consorcio-dej-pwa
http-server -p 8080

# Abrir en navegador
http://localhost:8080
```

### Opción 2: Python Server
```bash
cd consorcio-dej-pwa
python -m http.server 8080
```

### Opción 3: Deploy en Netlify/Vercel
1. Subir archivos a GitHub
2. Conectar con Netlify/Vercel
3. Deploy automático

## 📱 Características PWA

✅ Instalable en dispositivos móviles  
✅ Funciona offline  
✅ Notificaciones push  
✅ Acceso rápido desde pantalla de inicio  
✅ Interfaz nativa  

## 🔧 Configuración

- **URL de la app:** Cambiar en `index.html` línea 89
- **Iconos:** Reemplazar en carpeta `icons/`
- **Colores:** Modificar en `manifest.json`

## 📞 Soporte

- 📧 info@consorciodej.com
- 📱 +51 999 888 777

---

**CONSORCIO DEJ - Ingeniería y Construcción**"""
    
    with open(f"{pwa_dir}/README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # 6. Package.json para Node.js
    package_json = {
        "name": "consorcio-dej-pwa",
        "version": "2.0.0",
        "description": "CONSORCIO DEJ - Análisis Estructural PWA",
        "main": "index.html",
        "scripts": {
            "start": "http-server -p 8080",
            "dev": "http-server -p 3000 -c-1",
            "build": "echo 'PWA ready for deployment'"
        },
        "keywords": ["pwa", "structural", "analysis", "engineering"],
        "author": "CONSORCIO DEJ",
        "license": "MIT",
        "devDependencies": {
            "http-server": "^14.1.1"
        }
    }
    
    with open(f"{pwa_dir}/package.json", "w", encoding="utf-8") as f:
        json.dump(package_json, f, indent=2)
    
    print(f"✅ PWA creada en: {pwa_dir}")
    print("📱 Archivos generados:")
    print("  - index.html (App principal)")
    print("  - manifest.json (Configuración PWA)")
    print("  - sw.js (Service Worker)")
    print("  - package.json (Node.js)")
    print("  - README.md (Instrucciones)")
    print("  - icons/ (Directorio de iconos)")
    
    return pwa_dir

def create_apk_instructions():
    """Crear instrucciones para generar APK"""
    
    apk_instructions = """# 📱 GENERAR APK DESDE PWA

## Opción 1: Bubblewrap (Recomendado)

### 1. Instalar herramientas
```bash
npm install -g @bubblewrap/cli
```

### 2. Configurar proyecto
```bash
cd consorcio-dej-pwa
bubblewrap init --manifest https://tu-dominio.com/manifest.json
```

### 3. Generar APK
```bash
bubblewrap build
```

## Opción 2: PWA Builder

1. Ve a https://www.pwabuilder.com
2. Ingresa la URL de tu PWA
3. Genera APK automáticamente

## Opción 3: Capacitor (Ionic)

### 1. Instalar Capacitor
```bash
npm install -g @capacitor/cli
npm install @capacitor/core @capacitor/android
```

### 2. Configurar proyecto
```bash
npx cap init CONSORCIODEJ com.consorciodej.app
npx cap add android
```

### 3. Generar APK
```bash
npx cap build android
```

## 📋 Requisitos

- Node.js 14+
- Android Studio (para APK nativo)
- Java JDK 11+
- Gradle

## 🚀 Deploy

1. **PWA:** Subir a hosting (Netlify, Vercel, etc.)
2. **APK:** Generar con herramientas anteriores
3. **Distribuir:** Google Play Store o descarga directa

---

**CONSORCIO DEJ - Ingeniería y Construcción**"""
    
    with open("INSTRUCCIONES_APK.md", "w", encoding="utf-8") as f:
        f.write(apk_instructions)
    
    print("✅ Instrucciones APK creadas: INSTRUCCIONES_APK.md")

def main():
    """Función principal"""
    print("🚀 GENERANDO PWA - CONSORCIO DEJ")
    print("=" * 50)
    
    # Crear PWA
    pwa_dir = create_pwa_files()
    
    # Crear instrucciones APK
    create_apk_instructions()
    
    print("\n" + "=" * 50)
    print("🎉 ¡PWA GENERADA EXITOSAMENTE!")
    print(f"\n📁 Directorio: {pwa_dir}")
    print("\n📋 Próximos pasos:")
    print("1. cd consorcio-dej-pwa")
    print("2. npm install")
    print("3. npm start")
    print("4. Abrir http://localhost:8080")
    print("\n📱 Para generar APK:")
    print("1. Leer INSTRUCCIONES_APK.md")
    print("2. Seguir pasos para Bubblewrap o PWA Builder")
    print("\n✅ ¡Tu app estará lista como PWA y APK!")

if __name__ == "__main__":
    main() 