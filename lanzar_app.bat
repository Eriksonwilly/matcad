@echo off
title CONSORCIO DEJ - Análisis Estructural
color 0A

echo ========================================
echo    CONSORCIO DEJ - Análisis Estructural
echo ========================================
echo.
echo Verificando dependencias...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está disponible
    echo Por favor, instala Python 3.11 o verifica el PATH
    pause
    exit /b 1
)

REM Verificar Streamlit
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Instalando Streamlit...
    pip install streamlit
)

REM Verificar Matplotlib
python -c "import matplotlib" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Instalando Matplotlib...
    pip install matplotlib
)

REM Verificar ReportLab
python -c "import reportlab" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Instalando ReportLab...
    pip install reportlab
)

echo.
echo ✅ Todas las dependencias verificadas
echo.
echo 🚀 Iniciando aplicación...
echo.
echo 📱 URL Local: http://localhost:8520
echo 🌐 URL Red: http://192.168.139.127:8520
echo.
echo 💡 Para detener la app, presiona Ctrl+C
echo.

REM Cambiar al directorio del proyecto
cd /d "C:\Users\selec\Desktop\PROGRAMACION DIGITAL\CONCRETO ARMADO"

REM Lanzar la app
python -m streamlit run APP.py --server.port 8520

echo.
echo Aplicación detenida.
pause 