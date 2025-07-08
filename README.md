# 🏗️ CONSORCIO DEJ - Análisis Estructural

Aplicación web profesional para análisis y diseño estructural de concreto armado, desarrollada con Streamlit y Python.

## 🚀 Instalación Rápida

### Windows
```bash
# Opción 1: Script automático (Recomendado)
install_dependencies.bat

# Opción 2: Manual
pip install -r requirements.txt
python test_dependencies.py
```

### Linux/Mac
```bash
# Opción 1: Script automático
chmod +x install_dependencies.sh
./install_dependencies.sh

# Opción 2: Manual
pip install -r requirements.txt
python test_dependencies.py
```

## 🎯 Ejecutar la Aplicación

### Opción 1: Script Automático (Recomendado)
```bash
# Windows
lanzar_app.bat

# Linux/Mac
./lanzar_app.sh
```

### Opción 2: Comando Manual
```bash
python -m streamlit run APP.py --server.port 8520
```

### Opción 3: Puerto Alternativo (si 8520 está ocupado)
```bash
python -m streamlit run APP.py --server.port 8530
```

## 🔧 Solución de Problemas

### Error: "Matplotlib no está instalado"
```bash
# Reinstalar matplotlib
pip uninstall matplotlib
pip install matplotlib>=3.7.0

# Verificar instalación
python test_dependencies.py
```

### Error: "ReportLab no está instalado"
```bash
# Reinstalar reportlab
pip uninstall reportlab
pip install reportlab>=4.0.0

# Verificar instalación
python test_dependencies.py
```

### Error: Puerto ocupado
```bash
# Usar puerto alternativo
python -m streamlit run APP.py --server.port 8530

# O matar procesos en el puerto (Windows)
netstat -ano | findstr :8520
taskkill /PID [PID_NUMBER] /F
```

## 📋 Características

### Plan Gratuito
- ✅ Cálculos básicos de análisis estructural
- ✅ Resultados simples con gráficos básicos
- ✅ Reporte básico descargable
- ✅ Análisis de propiedades de materiales

### Plan Premium
- ⭐ Análisis completo con ACI 318-2025
- ⭐ Cálculos de predimensionamiento automáticos
- ⭐ **Reportes técnicos en PDF** (NUEVO)
- ⭐ **Gráficos interactivos avanzados** (NUEVO)
- ⭐ Verificaciones de estabilidad completas
- ⭐ Fórmulas de diseño estructural detalladas
- ⭐ Diagramas de cortantes y momentos (Nilson/McCormac)

## 🔑 Acceso

### Credenciales de Prueba
- **Usuario:** admin
- **Contraseña:** admin123
- **Plan:** Empresarial (acceso completo)

### Credenciales Demo
- **Usuario:** demo
- **Contraseña:** demo
- **Plan:** Gratuito (funciones limitadas)

## 📚 Dependencias Principales

- **Streamlit** >= 1.28.0 - Interfaz web
- **Matplotlib** >= 3.7.0 - Gráficos y diagramas
- **ReportLab** >= 4.0.0 - Generación de PDFs
- **Plotly** >= 5.15.0 - Gráficos interactivos
- **NumPy** >= 1.24.0 - Cálculos numéricos
- **Pandas** >= 2.0.0 - Manipulación de datos

## 🏗️ Normativas Implementadas

- **ACI 318-2025** - Building Code Requirements for Structural Concrete
- **RNE E.060** - Norma de Concreto Armado (Perú)
- **RNE E.030** - Norma de Diseño Sismorresistente (Perú)
- **Referencias:** Nilson, McCormac, Hibbeler, Blanco Blasco

## 📞 Soporte

- 📧 Email: contacto@consorciodej.com
- 📱 WhatsApp: +51 999 888 777
- 🌐 Web: www.consorciodej.com

---

**CONSORCIO DEJ - Ingeniería y Construcción Especializada**