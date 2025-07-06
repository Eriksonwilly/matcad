#!/bin/bash

echo "========================================"
echo "CONSORCIO DEJ - Software Estructural"
echo "========================================"
echo

while true; do
    echo "Selecciona una opcion:"
    echo "1. Instalar dependencias"
    echo "2. Ejecutar pruebas"
    echo "3. Ejecutar aplicacion"
    echo "4. Salir"
    echo
    read -p "Ingresa tu opcion (1-4): " opcion

    case $opcion in
        1)
            echo
            echo "Instalando dependencias..."
            python3 setup.py
            echo
            read -p "Presiona Enter para continuar..."
            ;;
        2)
            echo
            echo "Ejecutando pruebas..."
            python3 test_app.py
            echo
            read -p "Presiona Enter para continuar..."
            ;;
        3)
            echo
            echo "Ejecutando aplicacion..."
            echo "La aplicacion se abrira en tu navegador..."
            streamlit run APP_MEJORADO.py
            echo
            read -p "Presiona Enter para continuar..."
            ;;
        4)
            echo
            echo "Gracias por usar CONSORCIO DEJ!"
            echo
            exit 0
            ;;
        *)
            echo "Opcion invalida. Intenta de nuevo."
            ;;
    esac
done 