@echo off
echo ========================================
echo   CONSORCIO DEJ - LIMPIEZA PARA GITHUB
echo ========================================
echo.
echo Limpiando archivos innecesarios...
echo.

python limpiar_archivos.py

echo.
echo ========================================
echo   ARCHIVOS LISTOS PARA GITHUB
echo ========================================
echo.
echo ✅ Archivos importantes que SÍ subir:
echo - APP.py
echo - requirements.txt
echo - .gitignore
echo - *.bat
echo - *.ps1
echo - ejecutar_app.py
echo.
echo ❌ Archivos que NO subir (ya eliminados):
echo - venv/
echo - __pycache__/
echo - Carpetas de versiones (1.28.0, 2.0.0, etc.)
echo - Metadatos de paquetes
echo.
echo 🚀 Ahora puedes subir a GitHub de manera segura!
echo.
pause 