@echo off
echo ========================================
echo   INSTALACION COMPLETA - CONSORCIO DEJ
echo ========================================
echo.
echo Instalando dependencias y ejecutando aplicacion...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado
    echo Por favor instala Python desde: https://python.org
    pause
    exit /b 1
)

echo [1/6] Verificando Python...
python --version

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo [2/6] Creando entorno virtual...
    python -m venv venv
) else (
    echo [2/6] Entorno virtual ya existe...
)

REM Activar entorno virtual
echo [3/6] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo [4/6] Instalando dependencias...
pip install streamlit pandas numpy matplotlib plotly reportlab openpyxl

REM Verificar instalación
echo [5/6] Verificando instalación...
python -c "import streamlit; print('Streamlit instalado correctamente')"

REM Ejecutar aplicación
echo [6/6] Ejecutando aplicación...
echo.
echo ========================================
echo   CONSORCIO DEJ - MUROS DE CONTENCION
echo ========================================
echo.
echo Credenciales de prueba:
echo   admin / admin123 (Empresarial)
echo   premium@test.com / 123456 (Premium)
echo.
echo La aplicación se abrirá en tu navegador...
echo.

streamlit run APP.py

pause 