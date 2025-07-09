#!/usr/bin/env python3
"""
VERIFICACIÓN RÁPIDA - SOLUCIÓN DEFINITIVA
CONSORCIO DEJ - Muros de Contención
"""

import json
import os
import datetime

def verificar_solucion():
    """Verificar que la solución se aplicó correctamente"""
    
    print("🔍 VERIFICACIÓN RÁPIDA - SOLUCIÓN DEFINITIVA")
    print("=" * 60)
    print()
    
    # Verificar archivos creados
    archivos_requeridos = [
        "users.json",
        "payments.json", 
        "config_pagos.json",
        "simple_payment_system.py",
        "APP.py"
    ]
    
    print("📁 VERIFICANDO ARCHIVOS:")
    archivos_ok = 0
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
            archivos_ok += 1
        else:
            print(f"❌ {archivo} - FALTANTE")
    
    print(f"\n📊 Archivos encontrados: {archivos_ok}/{len(archivos_requeridos)}")
    
    if archivos_ok < len(archivos_requeridos):
        print("⚠️ Faltan algunos archivos. Ejecuta SOLUCION_DEFINITIVA.bat nuevamente.")
        return False
    
    # Verificar contenido de usuarios
    print("\n👥 VERIFICANDO USUARIOS:")
    try:
        with open("users.json", 'r', encoding='utf-8') as f:
            users = json.load(f)
        
        usuarios_esperados = ["admin", "admin@consorciodej.com", "premium@test.com", "empresarial@test.com"]
        
        for email in usuarios_esperados:
            if email in users:
                plan = users[email]["plan"]
                print(f"✅ {email}: {plan}")
            else:
                print(f"❌ {email}: NO ENCONTRADO")
        
        print(f"\n📊 Usuarios encontrados: {len(users)}")
        
    except Exception as e:
        print(f"❌ Error leyendo usuarios: {e}")
        return False
    
    # Verificar pagos
    print("\n💰 VERIFICANDO PAGOS:")
    try:
        with open("payments.json", 'r', encoding='utf-8') as f:
            payments = json.load(f)
        
        confirmados = [p for p in payments if p["status"] == "confirmado"]
        pendientes = [p for p in payments if p["status"] == "pendiente"]
        
        print(f"✅ Pagos confirmados: {len(confirmados)}")
        print(f"⏳ Pagos pendientes: {len(pendientes)}")
        
        for payment in confirmados:
            print(f"   • {payment['email']}: {payment['plan']} - ${payment['amount']}")
        
    except Exception as e:
        print(f"❌ Error leyendo pagos: {e}")
    
    # Verificar sistema de pagos
    print("\n🔧 VERIFICANDO SISTEMA DE PAGOS:")
    try:
        from simple_payment_system import payment_system
        
        # Test login admin
        result = payment_system.login_user("admin", "admin123")
        if result["success"]:
            print(f"✅ Login admin: {result['user']['plan']}")
        else:
            print(f"❌ Login admin: {result['message']}")
        
        # Test login premium
        result = payment_system.login_user("premium@test.com", "123456")
        if result["success"]:
            print(f"✅ Login premium: {result['user']['plan']}")
        else:
            print(f"❌ Login premium: {result['message']}")
        
        # Test verificación de plan
        plan = payment_system.get_user_plan("admin")
        if plan["plan"] == "empresarial":
            print("✅ Verificación de plan admin: OK")
        else:
            print(f"❌ Verificación de plan admin: {plan['plan']}")
        
    except Exception as e:
        print(f"❌ Error en sistema de pagos: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 VERIFICACIÓN COMPLETADA")
    print("=" * 60)
    print()
    print("✅ Si todo está OK, ejecuta:")
    print("   streamlit run APP.py")
    print()
    print("🔑 Credenciales de prueba:")
    print("   admin / admin123 (Empresarial)")
    print("   premium@test.com / 123456 (Premium)")
    print("   empresarial@test.com / 123456 (Empresarial)")
    print()
    print("🚀 ¡El sistema debería funcionar correctamente ahora!")
    
    return True

def crear_usuarios_faltantes():
    """Crear usuarios si faltan"""
    
    print("🔧 CREANDO USUARIOS FALTANTES...")
    print("=" * 50)
    
    import hashlib
    
    users = {
        "admin": {
            "email": "admin",
            "password": hashlib.sha256("admin123".encode()).hexdigest(),
            "name": "Administrador",
            "plan": "empresarial",
            "created_at": datetime.datetime.now().isoformat(),
            "expires_at": None,
            "is_admin": True
        },
        "admin@consorciodej.com": {
            "email": "admin@consorciodej.com",
            "password": hashlib.sha256("admin123".encode()).hexdigest(),
            "name": "Administrador",
            "plan": "empresarial",
            "created_at": datetime.datetime.now().isoformat(),
            "expires_at": None,
            "is_admin": True
        },
        "premium@test.com": {
            "email": "premium@test.com",
            "password": hashlib.sha256("123456".encode()).hexdigest(),
            "name": "Usuario Premium",
            "plan": "premium",
            "created_at": datetime.datetime.now().isoformat(),
            "expires_at": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat(),
            "is_admin": False
        },
        "empresarial@test.com": {
            "email": "empresarial@test.com",
            "password": hashlib.sha256("123456".encode()).hexdigest(),
            "name": "Usuario Empresarial",
            "plan": "empresarial",
            "created_at": datetime.datetime.now().isoformat(),
            "expires_at": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat(),
            "is_admin": False
        }
    }
    
    with open("users.json", 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    
    print("✅ Usuarios creados exitosamente")

if __name__ == "__main__":
    print("🔍 VERIFICACIÓN RÁPIDA - CONSORCIO DEJ")
    print("=" * 50)
    print()
    print("1. Verificar solución")
    print("2. Crear usuarios faltantes")
    print("3. Salir")
    print()
    
    opcion = input("Selecciona una opción (1-3): ").strip()
    print()
    
    if opcion == "1":
        verificar_solucion()
    elif opcion == "2":
        crear_usuarios_faltantes()
    elif opcion == "3":
        print("👋 ¡Hasta luego!")
    else:
        print("❌ Opción no válida") 