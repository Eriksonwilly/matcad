# 🏗️ CONSORCIO DEJ - Análisis Estructural

## 📋 Descripción
Aplicación profesional de análisis estructural desarrollada con Streamlit, que incluye:
- Cálculos de propiedades de materiales (concreto y acero)
- Análisis completo de estructuras
- Diagramas de cortantes y momentos según Arthur H. Nilson
- Generación de reportes en PDF
- Gráficos interactivos y visualizaciones

## 🚀 Instalación Rápida

### Windows
1. Ejecuta el archivo `install_dependencies.bat` haciendo doble clic
2. O ejecuta manualmente en cmd:
```cmd
pip install streamlit numpy pandas matplotlib plotly reportlab
```

### Linux/Mac
1. Ejecuta el script de instalación:
```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```
2. O instala manualmente:
```bash
pip install streamlit numpy pandas matplotlib plotly reportlab
```

## 🎯 Ejecutar la Aplicación

```bash
streamlit run APP.py
```

## 📚 Características Principales

### 🔧 Diagramas de Cortantes y Momentos (Arthur H. Nilson)
- **Viga Simplemente Apoyada**: Cálculo de reacciones, cortantes y momentos
- **Viga Empotrada**: Análisis con momentos de empotramiento
- **Viga Continua**: Análisis de vigas de múltiples tramos
- **Fórmulas basadas en**: "Diseño de Estructuras de Concreto" de Arthur H. Nilson

### 📊 Gráficos y Visualizaciones
- Gráficos interactivos con Plotly
- Diagramas de cortantes y momentos
- Visualizaciones de propiedades de materiales
- Gráficos de distribución de dimensiones

### 📄 Generación de Reportes
- Reportes básicos en formato TXT
- Reportes premium en PDF con ReportLab
- Información técnica detallada
- Fórmulas según ACI 318-2025

## 🔑 Credenciales de Acceso

### Plan Gratuito
- **Usuario**: demo
- **Contraseña**: demo

### Plan Premium (Administrador)
- **Usuario**: admin
- **Contraseña**: admin123

## 📖 Fórmulas Incluidas

### Propiedades del Concreto (ACI 318-2025)
- Módulo de elasticidad: `Ec = 15000√f'c`
- Deformación última: `εcu = 0.003`
- Resistencia a tracción: `fr = 2√f'c`

### Diseño por Flexión
- Cuantía balanceada: `ρb = 0.85β₁(f'c/fy)(6000/(6000+fy))`
- Cuantía máxima: `ρmax = 0.75ρb`
- Momento resistente: `φMn = φAsfy(d-a/2)`

### Diseño por Cortante
- Resistencia del concreto: `Vc = 0.53√f'c bwd`
- Resistencia del acero: `Vs = Avfyd/s`

## 🛠️ Solución de Problemas

### Error: "Matplotlib no está instalado"
```bash
pip install matplotlib
```

### Error: "Plotly no está instalado"
```bash
pip install plotly
```

### Error: "ReportLab no está instalado"
```bash
pip install reportlab
```

### Error al generar PDF
1. Verifica que ReportLab esté instalado
2. Asegúrate de tener permisos de escritura
3. Ejecuta el análisis completo antes de generar el PDF

## 📞 Soporte
Para soporte técnico o consultas:
- Email: contacto@consorciodej.com
- Documentación: Incluida en la aplicación

## 📄 Licencia
Desarrollado por CONSORCIO DEJ - Ingeniería y Construcción 