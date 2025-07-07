@echo off
echo 🏗️ CONSORCIO DEJ - Análisis Estructural
echo ================================================

echo 🐍 Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo 💡 Instala Python desde https://python.org
    pause
    exit /b 1
)

echo 📦 Instalando dependencias...
pip install streamlit==1.28.1 numpy==1.24.3 pandas==2.0.3
if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo 🚀 Iniciando aplicación...
echo 🌐 La aplicación se abrirá en tu navegador
echo 📱 URL: http://localhost:8501
echo.
echo 💡 Para cerrar la aplicación, presiona Ctrl+C
echo.

streamlit run APP.py --server.port=8501

pause 