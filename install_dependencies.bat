@echo off
echo ========================================
echo INSTALANDO DEPENDENCIAS - CONSORCIO DEJ
echo ========================================
echo.

echo Instalando dependencias basicas...
pip install streamlit numpy pandas

echo.
echo Instalando matplotlib para graficos...
pip install matplotlib

echo.
echo Instalando plotly para graficos interactivos...
pip install plotly

echo.
echo Instalando reportlab para PDFs...
pip install reportlab

echo.
echo ========================================
echo INSTALACION COMPLETADA
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo streamlit run APP.py
echo.
pause 