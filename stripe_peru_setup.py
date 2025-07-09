#!/usr/bin/env python3
"""
Guía para configurar Stripe desde Perú
CONSORCIO DEJ - Configuración Internacional
"""

import webbrowser

def show_stripe_peru_guide():
    """Mostrar guía para configurar Stripe desde Perú"""
    print("🇵🇪 CONFIGURACIÓN DE STRIPE DESDE PERÚ")
    print("=" * 50)
    
    print("\n📋 PROBLEMA: Stripe no aparece Perú en el registro")
    print("✅ SOLUCIÓN: Usar VPN o método alternativo")
    
    print("\n🚀 MÉTODOS PARA REGISTRARSE EN STRIPE:")
    
    methods = [
        ("1️⃣", "Usar VPN", "Conectar VPN a Estados Unidos y registrar"),
        ("2️⃣", "Registro con datos de EE.UU.", "Usar dirección de EE.UU. temporal"),
        ("3️⃣", "Contactar soporte", "Solicitar activación para Perú"),
        ("4️⃣", "Usar PayPal", "Alternativa más fácil para Perú")
    ]
    
    for emoji, method, description in methods:
        print(f"{emoji} {method}")
        print(f"   📝 {description}")
        print()

def show_vpn_method():
    """Mostrar método con VPN"""
    print("🔒 MÉTODO VPN (Recomendado):")
    print("=" * 30)
    
    steps = [
        "1. Descargar VPN gratuito (ProtonVPN, Windscribe)",
        "2. Conectar a servidor de Estados Unidos",
        "3. Ir a https://stripe.com",
        "4. Seleccionar 'Estados Unidos' como país",
        "5. Completar registro con tus datos reales",
        "6. Usar dirección de EE.UU. temporal",
        "7. Verificar cuenta con pasaporte/DNI"
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")
    
    print("\n🌐 VPNs gratuitos recomendados:")
    print("   • ProtonVPN (https://protonvpn.com)")
    print("   • Windscribe (https://windscribe.com)")
    print("   • TunnelBear (https://tunnelbear.com)")

def show_paypal_alternative():
    """Mostrar alternativa con PayPal"""
    print("💳 ALTERNATIVA CON PAYPAL:")
    print("=" * 30)
    
    print("PayPal es más fácil de configurar desde Perú:")
    print("✅ Disponible en Perú")
    print("✅ Sin restricciones geográficas")
    print("✅ Integración más simple")
    print("✅ Comisiones similares")
    
    print("\n📋 Pasos para PayPal:")
    steps = [
        "1. Crear cuenta en PayPal.com",
        "2. Verificar cuenta con tarjeta bancaria",
        "3. Configurar PayPal en la aplicación",
        "4. Procesar pagos directamente"
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")

def main():
    """Función principal"""
    print("🏗️ CONSORCIO DEJ - Configuración de Pagos desde Perú")
    print("=" * 60)
    
    show_stripe_peru_guide()
    
    print("🎯 ¿QUÉ MÉTODO PREFIERES?")
    print("1. Configurar Stripe con VPN")
    print("2. Usar PayPal como alternativa")
    print("3. Ver ambos métodos")
    
    choice = input("\nSelecciona una opción (1-3): ")
    
    if choice == "1":
        show_vpn_method()
        print("\n🌐 Abriendo Stripe...")
        webbrowser.open("https://stripe.com")
    elif choice == "2":
        show_paypal_alternative()
        print("\n🌐 Abriendo PayPal...")
        webbrowser.open("https://paypal.com")
    else:
        show_vpn_method()
        print("\n" + "="*50)
        show_paypal_alternative()

if __name__ == "__main__":
    main() 