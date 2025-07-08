@echo off
echo ========================================
echo    CONSORCIO DEJ - Instalador
echo ========================================
echo.
echo Instalando dependencias para la aplicacion...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.8 o superior desde python.org
    pause
    exit /b 1
)

echo ✅ Python detectado
python --version

echo.
echo 📦 Instalando dependencias desde requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ ERROR: No se pudieron instalar algunas dependencias
    echo Intentando instalar dependencias individualmente...
    
    echo.
    echo Instalando Streamlit...
    pip install streamlit>=1.28.0
    
    echo.
    echo Instalando Pandas...
    pip install pandas>=2.0.0
    
    echo.
    echo Instalando NumPy...
    pip install numpy>=1.24.0
    
    echo.
    echo Instalando Matplotlib...
    pip install matplotlib>=3.7.0
    
    echo.
    echo Instalando Plotly...
    pip install plotly>=5.15.0
    
    echo.
    echo Instalando ReportLab...
    pip install reportlab>=4.0.0
    
    echo.
    echo Instalando otras dependencias...
    pip install openpyxl>=3.1.0
    pip install Pillow>=10.0.0
    pip install streamlit-authenticator>=0.2.0
    pip install streamlit-option-menu>=0.3.0
)

echo.
echo 🔧 Verificando instalación...
python test_dependencies.py

if errorlevel 1 (
    echo.
    echo ⚠️ Algunas dependencias pueden tener problemas
    echo Revisa los errores arriba
) else (
    echo.
    echo ✅ Todas las dependencias instaladas correctamente
)

echo.
echo 🚀 Para ejecutar la aplicación:
echo    python -m streamlit run APP.py --server.port 8520
echo.
echo 📁 O usa el script: lanzar_app.bat
echo.
pause 