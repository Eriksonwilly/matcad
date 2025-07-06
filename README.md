# 🏗️ CONSORCIO DEJ - Software de Análisis Estructural Avanzado

## 📋 Descripción

Software profesional para análisis estructural de edificios de concreto armado según las normativas ACI 318-2025 y E.060 (Perú). Desarrollado con Python y Streamlit.

## 🚀 Características Principales

### ✅ Funcionalidades Incluidas:
- **Predimensionamiento Estructural**: Losas, vigas y columnas
- **Análisis Sísmico**: Según E.030 (Norma Peruana)
- **Diseño Estructural**: Flexión, cortante y compresión
- **Visualizaciones Interactivas**: Gráficos con Plotly
- **Reportes Técnicos**: Generación automática de resultados
- **Interfaz Profesional**: Diseño moderno y responsivo

### 📊 Módulos del Software:
1. **📊 Datos de Entrada**: Materiales, geometría y cargas
2. **🔧 Predimensionamiento**: Dimensiones automáticas
3. **🌎 Análisis Sísmico**: Cálculos según E.030
4. **🛠️ Diseño Estructural**: Acero y verificaciones
5. **📝 Reporte Final**: Resumen completo

## 🛠️ Instalación y Uso

### Requisitos Previos:
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación:

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tu-usuario/consorcio-dej-estructural.git
cd consorcio-dej-estructural
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación:**
```bash
streamlit run APP_MEJORADO.py
```

4. **Abrir en navegador:**
La aplicación se abrirá automáticamente en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
consorcio-dej-estructural/
├── APP_MEJORADO.py          # Aplicación principal mejorada
├── APP.py                   # Aplicación original
├── APP1.py                  # Referencia de diseño
├── requirements.txt         # Dependencias del proyecto
├── README.md               # Este archivo
└── .gitignore              # Archivos a ignorar en Git
```

## 🌐 Publicación en Streamlit Cloud

### Pasos para Publicar:

1. **Crear cuenta en GitHub:**
   - Ve a [github.com](https://github.com)
   - Crea una cuenta gratuita
   - Crea un nuevo repositorio

2. **Subir código a GitHub:**
```bash
git init
git add .
git commit -m "Primera versión del software estructural"
git branch -M main
git remote add origin https://github.com/tu-usuario/tu-repositorio.git
git push -u origin main
```

3. **Publicar en Streamlit Cloud:**
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Inicia sesión con tu cuenta de GitHub
   - Haz clic en "New app"
   - Selecciona tu repositorio
   - Archivo principal: `APP_MEJORADO.py`
   - Haz clic en "Deploy"

## 📋 Uso del Software

### 1. Datos de Entrada
- Ingresa las propiedades de los materiales (f'c, fy)
- Define la geometría del edificio
- Especifica las cargas (muerta, viva)
- Configura parámetros sísmicos

### 2. Predimensionamiento
- El software calcula automáticamente:
  - Espesor de losas aligeradas
  - Dimensiones de vigas principales
  - Tamaño de columnas

### 3. Análisis Sísmico
- Cálculo del cortante basal
- Distribución de fuerzas sísmicas
- Verificación de parámetros E.030

### 4. Diseño Estructural
- Diseño por flexión de vigas
- Diseño por cortante
- Diseño de columnas a compresión
- Verificación de cuantías

### 5. Reporte Final
- Resumen completo de resultados
- Gráficos interactivos
- Recomendaciones técnicas

## 🔧 Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **Streamlit**: Framework web
- **Plotly**: Gráficos interactivos
- **Pandas**: Manipulación de datos
- **NumPy**: Cálculos numéricos
- **Matplotlib**: Gráficos estáticos

## 📚 Normativas Aplicadas

- **ACI 318-2025**: Código de construcción de concreto
- **E.030**: Norma de diseño sismorresistente (Perú)
- **E.060**: Norma de concreto armado (Perú)

## 👨‍💼 Desarrollado por

**CONSORCIO DEJ** - Ingeniería y Construcción
- Especialistas en análisis estructural
- Desarrollo de software técnico
- Consultoría en construcción

## 📞 Contacto

- **Email**: contacto@consorciodej.com
- **Teléfono**: +51 XXX XXX XXX
- **Web**: www.consorciodej.com

## 📄 Licencia

Este software está desarrollado para uso educativo y profesional. Se recomienda validar todos los cálculos con software especializado y consultar con ingenieros estructurales certificados.

## ⚠️ Descargo de Responsabilidad

Este software proporciona resultados preliminares para análisis estructural. Los usuarios deben:
- Validar todos los cálculos con software especializado
- Consultar con ingenieros estructurales certificados
- Verificar el cumplimiento de normativas locales
- Realizar inspecciones y pruebas en campo

---

**🏗️ CONSORCIO DEJ - Ingeniería y Construcción**
*Software de Análisis Estructural Avanzado*