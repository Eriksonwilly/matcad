import hashlib
import json
import os
from datetime import datetime, timedelta
import random

class SimplePaymentSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.payments_file = "payments.json"
        self.load_data()
    
    def load_data(self):
        """Cargar datos de usuarios y pagos"""
        # Cargar usuarios
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {
                "admin@consorciodej.com": {
                    "email": "admin@consorciodej.com",
                    "password": hashlib.sha256("admin123".encode()).hexdigest(),
                    "name": "Administrador",
                    "plan": "empresarial",
                    "created_at": datetime.now().isoformat()
                },
                "demo@consorciodej.com": {
                    "email": "demo@consorciodej.com", 
                    "password": hashlib.sha256("demo123".encode()).hexdigest(),
                    "name": "Usuario Demo",
                    "plan": "basico",
                    "created_at": datetime.now().isoformat()
                }
            }
            self.save_users()
        
        # Cargar pagos
        if os.path.exists(self.payments_file):
            with open(self.payments_file, 'r') as f:
                self.payments = json.load(f)
        else:
            self.payments = []
            self.save_payments()
    
    def save_users(self):
        """Guardar datos de usuarios"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def save_payments(self):
        """Guardar datos de pagos"""
        with open(self.payments_file, 'w') as f:
            json.dump(self.payments, f, indent=2)
    
    def register_user(self, email, password, name):
        """Registrar nuevo usuario"""
        if email in self.users:
            return {"success": False, "message": "El email ya está registrado"}
        
        if len(password) < 6:
            return {"success": False, "message": "La contraseña debe tener al menos 6 caracteres"}
        
        self.users[email] = {
            "email": email,
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "name": name,
            "plan": "basico",
            "created_at": datetime.now().isoformat()
        }
        
        self.save_users()
        return {"success": True, "message": "Usuario registrado exitosamente"}
    
    def login_user(self, email, password):
        """Iniciar sesión de usuario"""
        if email not in self.users:
            return {"success": False, "message": "Email o contraseña incorrectos"}
        
        user = self.users[email]
        if user["password"] != hashlib.sha256(password.encode()).hexdigest():
            return {"success": False, "message": "Email o contraseña incorrectos"}
        
        return {
            "success": True, 
            "user": user,
            "message": f"Bienvenido, {user['name']}"
        }
    
    def get_user_plan(self, email):
        """Obtener plan del usuario"""
        if email in self.users:
            return self.users[email]
        return {"plan": "basico"}
    
    def upgrade_plan(self, email, plan, payment_method):
        """Actualizar plan del usuario"""
        if email not in self.users:
            return {"success": False, "message": "Usuario no encontrado"}
        
        # Precios de los planes
        prices = {
            "premium": 29.99,
            "empresarial": 99.99
        }
        
        if plan not in prices:
            return {"success": False, "message": "Plan no válido"}
        
        # Generar instrucciones de pago según el método
        payment_instructions = self.get_payment_instructions(plan, payment_method, prices[plan])
        
        # Simular procesamiento de pago (en un sistema real, aquí iría la integración con pasarela de pagos)
        payment_id = f"PAY-{random.randint(10000, 99999)}"
        
        # Registrar el pago
        payment_record = {
            "payment_id": payment_id,
            "email": email,
            "plan": plan,
            "amount": prices[plan],
            "payment_method": payment_method,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "instructions": payment_instructions
        }
        
        self.payments.append(payment_record)
        self.save_payments()
        
        # Simular confirmación automática para algunos métodos
        auto_confirmed = payment_method in ["yape", "plin"]
        
        if auto_confirmed:
            # Actualizar plan inmediatamente
            self.users[email]["plan"] = plan
            self.save_users()
            
            return {
                "success": True,
                "message": "Pago confirmado automáticamente",
                "instructions": payment_instructions,
                "auto_confirmed": True,
                "payment_id": payment_id
            }
        else:
            return {
                "success": True,
                "message": "Pago procesado correctamente",
                "instructions": payment_instructions,
                "auto_confirmed": False,
                "payment_id": payment_id
            }
    
    def get_payment_instructions(self, plan, payment_method, amount):
        """Generar instrucciones de pago según el método"""
        instructions = {
            "yape": f"""
📱 PAGO CON YAPE - Plan {plan.upper()}
💰 Monto: S/ {amount:.2f}

1. Abre Yape en tu celular
2. Escanea el código QR o envía a: 999 888 777
3. Concepto: "CONSORCIO DEJ - {plan.upper()}"
4. Envía el comprobante a WhatsApp: +51 999 888 777
5. Tu plan será activado en 5 minutos

✅ Activación automática disponible
            """,
            
            "plin": f"""
📱 PAGO CON PLIN - Plan {plan.upper()}
💰 Monto: S/ {amount:.2f}

1. Abre PLIN en tu celular
2. Envía a: 999 888 777
3. Concepto: "CONSORCIO DEJ - {plan.upper()}"
4. Envía el comprobante a WhatsApp: +51 999 888 777
5. Tu plan será activado en 5 minutos

✅ Activación automática disponible
            """,
            
            "paypal": f"""
💳 PAGO CON PAYPAL - Plan {plan.upper()}
💰 Monto: ${amount:.2f} USD

1. Ve a: paypal.me/consorciodej
2. Ingresa el monto: ${amount:.2f}
3. Concepto: "CONSORCIO DEJ - {plan.upper()}"
4. Envía el comprobante a: pagos@consorciodej.com
5. Tu plan será activado en 2 horas

⏰ Activación manual (2 horas máximo)
            """,
            
            "transferencia": f"""
🏦 TRANSFERENCIA BANCÁRIA - Plan {plan.upper()}
💰 Monto: S/ {amount:.2f}

Banco: BANCO DE CRÉDITO DEL PERÚ
Cuenta: 193-12345678-0-12
CCI: 002-193-001234567890-12
Titular: CONSORCIO DEJ SAC
Concepto: "CONSORCIO DEJ - {plan.upper()}"

1. Realiza la transferencia
2. Envía el comprobante a: pagos@consorciodej.com
3. Tu plan será activado en 2 horas

⏰ Activación manual (2 horas máximo)
            """,
            
            "efectivo": f"""
💵 PAGO EN EFECTIVO - Plan {plan.upper()}
💰 Monto: S/ {amount:.2f}

1. Acércate a nuestras oficinas:
   📍 Av. Principal 123, Lima
   📞 Tel: (01) 123-4567
   
2. Horarios de atención:
   📅 Lunes a Viernes: 9:00 AM - 6:00 PM
   📅 Sábados: 9:00 AM - 1:00 PM

3. Tu plan será activado inmediatamente

✅ Activación inmediata
            """
        }
        
        return instructions.get(payment_method, "Método de pago no disponible")
    
    def confirm_payment(self, payment_id):
        """Confirmar pago manualmente (para administradores)"""
        for payment in self.payments:
            if payment["payment_id"] == payment_id and payment["status"] == "pending":
                payment["status"] = "confirmed"
                payment["confirmed_at"] = datetime.now().isoformat()
                
                # Actualizar plan del usuario
                email = payment["email"]
                plan = payment["plan"]
                if email in self.users:
                    self.users[email]["plan"] = plan
                
                self.save_payments()
                self.save_users()
                
                return {"success": True, "message": "Pago confirmado exitosamente"}
        
        return {"success": False, "message": "Pago no encontrado o ya confirmado"}

# Instancia global del sistema de pagos
payment_system = SimplePaymentSystem() 