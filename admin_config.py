#!/usr/bin/env python3
"""
Configuración del Administrador - CONSORCIO DEJ
Credenciales y configuración del sistema
"""

# Credenciales del administrador
ADMIN_CREDENTIALS = {
    "usuario": "admin",
    "clave": "admin123"
}

# Credenciales demo (para modo sin sistema de pagos)
DEMO_CREDENTIALS = {
    "usuario": "demo",
    "clave": "demo"
}

# Configuración de planes
PLANS_CONFIG = {
    "gratuito": {
        "precio": 0.0,
        "duracion_dias": None,
        "caracteristicas": [
            "Cálculos básicos",
            "Análisis simple",
            "Reportes básicos"
        ]
    },
    "premium": {
        "precio": 29.99,
        "duracion_dias": 30,
        "caracteristicas": [
            "Todo del plan gratuito",
            "Análisis completo",
            "Diseño del fuste",
            "Gráficos avanzados",
            "Reportes PDF"
        ]
    },
    "empresarial": {
        "precio": 99.99,
        "duracion_dias": 30,
        "caracteristicas": [
            "Todo del plan premium",
            "Soporte prioritario",
            "Múltiples proyectos",
            "Reportes personalizados",
            "Capacitación incluida",
            "API de integración"
        ]
    }
}

# Configuración de pagos
PAYMENT_CONFIG = {
    "paypal": {
        "email": "consorciodej@gmail.com",
        "link": "https://paypal.me/consorciodej"
    },
    "transferencia": {
        "banco": "BCP",
        "cuenta": "193-12345678-0-12",
        "cci": "002-193-001234567890-12",
        "titular": "CONSORCIO DEJ SAC"
    },
    "efectivo": {
        "oficina": "Av. Arequipa 123, Lima",
        "contacto": "+51 999 888 777"
    }
}

def get_admin_credentials():
    """Obtener credenciales del administrador"""
    return ADMIN_CREDENTIALS

def get_demo_credentials():
    """Obtener credenciales demo"""
    return DEMO_CREDENTIALS

def get_plan_config(plan_name):
    """Obtener configuración de un plan"""
    return PLANS_CONFIG.get(plan_name, {})

def get_payment_config(payment_method):
    """Obtener configuración de método de pago"""
    return PAYMENT_CONFIG.get(payment_method, {})

def validate_admin_login(username, password):
    """Validar login de administrador"""
    return (username == ADMIN_CREDENTIALS["usuario"] and 
            password == ADMIN_CREDENTIALS["clave"])

def validate_demo_login(username, password):
    """Validar login demo"""
    return (username == DEMO_CREDENTIALS["usuario"] and 
            password == DEMO_CREDENTIALS["clave"])

if __name__ == "__main__":
    print("🔧 CONFIGURACIÓN DEL ADMINISTRADOR")
    print("=" * 40)
    print(f"Usuario admin: {ADMIN_CREDENTIALS['usuario']}")
    print(f"Clave admin: {ADMIN_CREDENTIALS['clave']}")
    print()
    print("🧪 CREDENCIALES DEMO")
    print(f"Usuario demo: {DEMO_CREDENTIALS['usuario']}")
    print(f"Clave demo: {DEMO_CREDENTIALS['clave']}")
    print()
    print("💰 CONFIGURACIÓN DE PLANES")
    for plan, config in PLANS_CONFIG.items():
        print(f"{plan.title()}: ${config['precio']}/mes") 