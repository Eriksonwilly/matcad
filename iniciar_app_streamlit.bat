@echo off
echo ========================================
echo    CONSORCIO DEJ - Análisis Estructural
echo ========================================
echo.
echo Iniciando aplicacion Streamlit...
echo.

REM Cambia la ruta a la carpeta de tu proyecto
cd /d "C:\Users\selec\Desktop\PROGRAMACION DIGITAL\CONCRETO ARMADO"

REM Verifica que Python esté disponible
python --version
if errorlevel 1 (
    echo ERROR: Python no está disponible en el PATH
    echo Por favor, verifica la instalación de Python
    pause
    exit /b 1
)

REM Verifica que Streamlit esté instalado
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
if errorlevel 1 (
    echo Instalando Streamlit...
    pip install streamlit
)

echo.
echo Lanzando aplicacion en puerto 8520...
echo.
echo Cuando aparezca la URL, abre tu navegador en:
echo http://localhost:8520
echo.
echo Para detener la aplicacion, presiona Ctrl+C
echo.

REM Lanza la app con el Python correcto
python -m streamlit run APP.py --server.port 8520

echo.
echo Aplicacion detenida.
pause 