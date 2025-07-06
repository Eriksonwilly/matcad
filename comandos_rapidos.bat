@echo off
echo ========================================
echo CONSORCIO DEJ - Software Estructural
echo ========================================
echo.

:menu
echo Selecciona una opcion:
echo 1. Instalar dependencias
echo 2. Ejecutar pruebas
echo 3. Ejecutar aplicacion
echo 4. Salir
echo.
set /p opcion="Ingresa tu opcion (1-4): "

if "%opcion%"=="1" goto instalar
if "%opcion%"=="2" goto pruebas
if "%opcion%"=="3" goto ejecutar
if "%opcion%"=="4" goto salir
echo Opcion invalida. Intenta de nuevo.
goto menu

:instalar
echo.
echo Instalando dependencias...
python setup.py
echo.
pause
goto menu

:pruebas
echo.
echo Ejecutando pruebas...
python test_app.py
echo.
pause
goto menu

:ejecutar
echo.
echo Ejecutando aplicacion...
echo La aplicacion se abrira en tu navegador...
streamlit run APP_MEJORADO.py
echo.
pause
goto menu

:salir
echo.
echo Gracias por usar CONSORCIO DEJ!
echo.
pause
exit 