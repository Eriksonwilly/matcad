# 🚀 GENERACIÓN DE APK PARA CONSORCIO DEJ

## 📱 **OPCIÓN 1: STREAMLIT MOBILE (RECOMENDADA)**

### **Paso 1: Preparar el proyecto**
```bash
# Crear directorio del proyecto
mkdir consorcio-dej-mobile
cd consorcio-dej-mobile

# Copiar archivos
cp streamlit_app.py .
cp requirements.txt .
cp -r .streamlit .
```

### **Paso 2: Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **Paso 3: Probar la aplicación**
```bash
streamlit run streamlit_app.py
```

### **Paso 4: Generar APK con Streamlit Mobile**

#### **Opción A: Usando Streamlit Cloud + PWA**
1. **Subir a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/tuusuario/consorcio-dej-mobile.git
   git push -u origin main
   ```

2. **Deploy en Streamlit Cloud:**
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Conecta tu cuenta de GitHub
   - Selecciona el repositorio
   - Deploy automático

3. **Convertir a PWA (Progressive Web App):**
   - La app será accesible desde móviles
   - Los usuarios pueden "instalar" la app en su pantalla de inicio
   - Funciona offline parcialmente

#### **Opción B: Usando Streamlit Mobile Builder**
1. **Instalar Streamlit Mobile:**
   ```bash
   pip install streamlit-mobile
   ```

2. **Generar APK:**
   ```bash
   streamlit-mobile build --app streamlit_app.py --output consorcio-dej.apk
   ```

---

## 📱 **OPCIÓN 2: KIVY + PYTHON (ALTERNATIVA)**

### **Paso 1: Instalar Buildozer**
```bash
pip install buildozer
```

### **Paso 2: Crear buildozer.spec**
```ini
[app]
title = CONSORCIO DEJ
package.name = consorciodej
package.domain = org.consorciodej
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 2.0

requirements = python3,kivy,streamlit,numpy,pandas,plotly,reportlab

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
android.api = 29
android.minapi = 21
android.ndk = 23b
android.sdk = 29
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
```

### **Paso 3: Generar APK**
```bash
buildozer android debug
```

---

## 📱 **OPCIÓN 3: FLUTTER + STREAMLIT (AVANZADA)**

### **Paso 1: Crear app Flutter**
```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() {
  runApp(ConsorcioDejApp());
}

class ConsorcioDejApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CONSORCIO DEJ',
      theme: ThemeData(
        primarySwatch: Colors.orange,
      ),
      home: StreamlitWebView(),
    );
  }
}

class StreamlitWebView extends StatefulWidget {
  @override
  _StreamlitWebViewState createState() => _StreamlitWebViewState();
}

class _StreamlitWebViewState extends State<StreamlitWebView> {
  late WebViewController _controller;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('CONSORCIO DEJ - Análisis Estructural'),
      ),
      body: WebView(
        initialUrl: 'https://tu-app.streamlit.app',
        javascriptMode: JavascriptMode.unrestricted,
        onWebViewCreated: (WebViewController webViewController) {
          _controller = webViewController;
        },
      ),
    );
  }
}
```

### **Paso 2: Configurar pubspec.yaml**
```yaml
name: consorcio_dej
description: Análisis Estructural Profesional

environment:
  sdk: ">=2.12.0 <3.0.0"

dependencies:
  flutter:
    sdk: flutter
  webview_flutter: ^3.0.0
  cupertino_icons: ^1.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^1.0.0
```

### **Paso 3: Generar APK**
```bash
flutter build apk --release
```

---

## 🔗 **ENLACES ÚTILES:**

### **Streamlit Mobile:**
- 📱 [Streamlit Mobile Documentation](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- 🚀 [Streamlit Cloud](https://share.streamlit.io)
- 📋 [PWA Guidelines](https://web.dev/progressive-web-apps/)

### **Buildozer:**
- 🛠️ [Buildozer Documentation](https://buildozer.readthedocs.io/)
- 📱 [Kivy Android](https://kivy.org/doc/stable/installation/installation-android.html)

### **Flutter:**
- 🎯 [Flutter Documentation](https://flutter.dev/docs)
- 📱 [Flutter Android](https://flutter.dev/docs/deployment/android)

---

## ⚡ **MÉTODO RÁPIDO (RECOMENDADO):**

### **1. Subir a Streamlit Cloud (5 minutos):**
```bash
# Crear repositorio en GitHub
# Subir archivos
git add .
git commit -m "Mobile app ready"
git push

# Deploy en Streamlit Cloud
# URL: https://share.streamlit.io
```

### **2. Convertir a PWA (2 minutos):**
- La app será accesible desde móviles
- Los usuarios pueden "instalar" la app
- Funciona como una app nativa

### **3. Compartir enlace:**
- Enviar el enlace de Streamlit Cloud
- Los usuarios pueden acceder desde cualquier dispositivo
- No requiere instalación de APK

---

## 📋 **ARCHIVOS NECESARIOS:**

```
consorcio-dej-mobile/
├── streamlit_app.py          # App principal optimizada
├── requirements.txt          # Dependencias
├── .streamlit/
│   └── config.toml          # Configuración Streamlit
├── README_APK.md            # Este archivo
└── assets/                  # Imágenes y recursos
    ├── icon.png
    └── logo.png
```

---

## 🎯 **RESULTADO FINAL:**

✅ **App web optimizada para móviles**
✅ **Accesible desde cualquier dispositivo**
✅ **Interfaz responsive y profesional**
✅ **Cálculos ACI 318-2025 completos**
✅ **Gráficos interactivos**
✅ **Sin necesidad de instalación**

---

## 📞 **SOPORTE:**

- 📧 Email: info@consorciodej.com
- 📱 WhatsApp: +51 999 888 777
- 🌐 Web: https://consorciodej.com

**¡Tu app estará lista en menos de 10 minutos!** 🚀 