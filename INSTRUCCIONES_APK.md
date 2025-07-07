# 📱 GENERAR APK DESDE PWA

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

**CONSORCIO DEJ - Ingeniería y Construcción**