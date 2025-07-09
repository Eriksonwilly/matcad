@echo off
echo ========================================
echo   INSTALACION COMPLETA - CONSORCIO DEJ
echo ========================================
echo.
echo Instalando todas las dependencias y verificando funcionamiento...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado
    echo Por favor instala Python desde: https://python.org
    pause
    exit /b 1
)

echo ✅ Python detectado
python --version
echo.

echo [1/5] Actualizando pip...
python -m pip install --upgrade pip
echo.

echo [2/5] Instalando dependencias principales...
pip install streamlit>=1.28.0
pip install pandas>=2.0.0
pip install numpy>=1.24.0
pip install matplotlib>=3.7.0
pip install plotly>=5.15.0
pip install reportlab>=4.0.0
echo.

echo [3/5] Instalando dependencias adicionales...
pip install openpyxl>=3.1.0
pip install stripe>=7.0.0
pip install streamlit-authenticator>=0.2.0
pip install streamlit-option-menu>=0.3.0
pip install Pillow>=10.0.0
pip install scipy>=1.10.0
pip install seaborn>=0.12.0
echo.

echo [4/5] Verificando instalación...
python test_graficos_pdf.py
echo.

echo [5/5] Ejecutando aplicación...
echo.
echo ========================================
echo   CONSORCIO DEJ - ANALISIS ESTRUCTURAL
echo ========================================
echo.
echo Credenciales de prueba:
echo   admin / admin123 (Empresarial)
echo   demo / demo (Gratuito)
echo.
echo La aplicación se abrirá en tu navegador...
echo.

streamlit run APP.py

pause 