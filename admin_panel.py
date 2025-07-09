#!/usr/bin/env python3
"""
Panel de Administración - CONSORCIO DEJ
Gestión de usuarios, pagos y configuración
"""

import streamlit as st
import json
import os
from datetime import datetime
from simple_payment_system import payment_system
from admin_config import validate_admin_login, get_plan_config, get_payment_config

def show_admin_login():
    """Mostrar login de administrador"""
    st.title("🔧 Panel de Administración")
    st.subheader("Acceso de Administrador")
    
    with st.form("admin_login"):
        username = st.text_input("Usuario Administrador")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Acceder")
        
        if submitted:
            if validate_admin_login(username, password):
                st.session_state['admin_logged_in'] = True
                st.success("✅ Acceso concedido")
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas")
    
    # Mostrar credenciales de ayuda
    with st.expander("ℹ️ Credenciales de ayuda"):
        st.info("""
        **Credenciales del administrador:**
        - Usuario: admin
        - Contraseña: admin123
        
        **Credenciales demo:**
        - Usuario: demo
        - Contraseña: demo
        """)

def show_admin_dashboard():
    """Mostrar dashboard de administrador"""
    st.title("🔧 Panel de Administración - CONSORCIO DEJ")
    
    # Sidebar para navegación
    st.sidebar.title("📋 Menú Administrativo")
    admin_option = st.sidebar.selectbox(
        "Seleccionar opción",
        ["📊 Dashboard", "👥 Usuarios", "💳 Pagos", "⚙️ Configuración", "📈 Estadísticas"]
    )
    
    # Botón para cerrar sesión
    if st.sidebar.button("🚪 Cerrar Sesión Admin"):
        st.session_state['admin_logged_in'] = False
        st.rerun()
    
    if admin_option == "📊 Dashboard":
        show_dashboard()
    elif admin_option == "👥 Usuarios":
        show_users_management()
    elif admin_option == "💳 Pagos":
        show_payments_management()
    elif admin_option == "⚙️ Configuración":
        show_configuration()
    elif admin_option == "📈 Estadísticas":
        show_statistics()

def show_dashboard():
    """Mostrar dashboard principal"""
    st.subheader("📊 Dashboard General")
    
    # Estadísticas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = len(payment_system.users)
        st.metric("👥 Total Usuarios", total_users)
    
    with col2:
        pending_payments = len(payment_system.get_pending_payments())
        st.metric("⏳ Pagos Pendientes", pending_payments)
    
    with col3:
        premium_users = sum(1 for user in payment_system.users.values() 
                          if user.get('plan') == 'premium')
        st.metric("⭐ Usuarios Premium", premium_users)
    
    with col4:
        business_users = sum(1 for user in payment_system.users.values() 
                           if user.get('plan') == 'empresarial')
        st.metric("🏢 Usuarios Empresarial", business_users)
    
    # Pagos pendientes recientes
    st.subheader("⏳ Pagos Pendientes Recientes")
    pending_payments = payment_system.get_pending_payments()
    
    if pending_payments:
        for payment in pending_payments[-5:]:  # Últimos 5 pagos
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"**{payment['email']}** - {payment['plan'].title()}")
                
                with col2:
                    st.write(f"${payment['amount']:.2f}")
                
                with col3:
                    st.write(payment['payment_method'])
                
                with col4:
                    if st.button(f"✅ Confirmar", key=f"confirm_{payment['id']}"):
                        result = payment_system.confirm_payment(payment['id'])
                        if result["success"]:
                            st.success("Pago confirmado")
                            st.rerun()
                        else:
                            st.error(result["message"])
    else:
        st.info("No hay pagos pendientes")

def show_users_management():
    """Gestionar usuarios"""
    st.subheader("👥 Gestión de Usuarios")
    
    # Buscar usuario
    search_email = st.text_input("🔍 Buscar usuario por email")
    
    if search_email:
        if search_email in payment_system.users:
            user = payment_system.users[search_email]
            show_user_details(user)
        else:
            st.warning("Usuario no encontrado")
    
    # Lista de usuarios
    st.subheader("📋 Lista de Usuarios")
    
    for email, user in payment_system.users.items():
        with st.expander(f"{email} - {user.get('plan', 'gratuito').title()}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Nombre:** {user.get('name', 'N/A')}")
                st.write(f"**Plan:** {user.get('plan', 'gratuito').title()}")
                st.write(f"**Registrado:** {user.get('created_at', 'N/A')}")
                if user.get('expires_at'):
                    st.write(f"**Expira:** {user.get('expires_at', 'N/A')}")
            
            with col2:
                if st.button("🗑️ Eliminar", key=f"delete_{email}"):
                    del payment_system.users[email]
                    payment_system.save_data()
                    st.success("Usuario eliminado")
                    st.rerun()

def show_user_details(user):
    """Mostrar detalles de un usuario"""
    st.subheader("👤 Detalles del Usuario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Email:** {user.get('email', 'N/A')}")
        st.write(f"**Nombre:** {user.get('name', 'N/A')}")
        st.write(f"**Plan actual:** {user.get('plan', 'gratuito').title()}")
    
    with col2:
        st.write(f"**Registrado:** {user.get('created_at', 'N/A')}")
        if user.get('expires_at'):
            st.write(f"**Expira:** {user.get('expires_at', 'N/A')}")
        if user.get('payment_pending'):
            st.write(f"**Pago pendiente:** {user.get('payment_pending')}")
    
    # Cambiar plan
    st.subheader("🔄 Cambiar Plan")
    new_plan = st.selectbox("Nuevo plan", ["gratuito", "premium", "empresarial"])
    
    if st.button("Actualizar Plan"):
        user['plan'] = new_plan
        user['payment_pending'] = None
        payment_system.save_data()
        st.success(f"Plan actualizado a {new_plan.title()}")

def show_payments_management():
    """Gestionar pagos"""
    st.subheader("💳 Gestión de Pagos")
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.selectbox("Filtrar por estado", ["Todos", "pendiente", "confirmado"])
    
    with col2:
        plan_filter = st.selectbox("Filtrar por plan", ["Todos", "premium", "empresarial"])
    
    # Lista de pagos
    payments = payment_system.payments
    
    # Aplicar filtros
    if status_filter != "Todos":
        payments = [p for p in payments if p['status'] == status_filter]
    
    if plan_filter != "Todos":
        payments = [p for p in payments if p['plan'] == plan_filter]
    
    st.subheader(f"📋 Pagos ({len(payments)})")
    
    for payment in payments:
        with st.expander(f"{payment['id']} - {payment['email']} - {payment['plan'].title()}"):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"**Email:** {payment['email']}")
                st.write(f"**Plan:** {payment['plan'].title()}")
                st.write(f"**Método:** {payment['payment_method']}")
            
            with col2:
                st.write(f"**Monto:** ${payment['amount']:.2f}")
                st.write(f"**Estado:** {payment['status']}")
            
            with col3:
                st.write(f"**Fecha:** {payment['created_at']}")
                if payment.get('confirmed_at'):
                    st.write(f"**Confirmado:** {payment['confirmed_at']}")
            
            with col4:
                if payment['status'] == 'pendiente':
                    if st.button("✅ Confirmar", key=f"confirm_payment_{payment['id']}"):
                        result = payment_system.confirm_payment(payment['id'])
                        if result["success"]:
                            st.success("Pago confirmado")
                            st.rerun()
                        else:
                            st.error(result["message"])
                else:
                    st.success("✅ Confirmado")

def show_configuration():
    """Mostrar configuración"""
    st.subheader("⚙️ Configuración del Sistema")
    
    # Configuración de planes
    st.subheader("💰 Configuración de Planes")
    
    for plan_name, config in get_plan_config().items():
        with st.expander(f"Plan {plan_name.title()}"):
            st.write(f"**Precio:** ${config['precio']:.2f}")
            st.write(f"**Duración:** {config['duracion_dias']} días" if config['duracion_dias'] else "**Duración:** Ilimitado")
            st.write("**Características:**")
            for feature in config['caracteristicas']:
                st.write(f"• {feature}")
    
    # Configuración de pagos
    st.subheader("💳 Configuración de Pagos")
    
    for method, config in get_payment_config().items():
        with st.expander(f"Método: {method.title()}"):
            for key, value in config.items():
                st.write(f"**{key.title()}:** {value}")

def show_statistics():
    """Mostrar estadísticas"""
    st.subheader("📈 Estadísticas del Sistema")
    
    # Gráficos de usuarios por plan
    import pandas as pd
    
    plan_counts = {}
    for user in payment_system.users.values():
        plan = user.get('plan', 'gratuito')
        plan_counts[plan] = plan_counts.get(plan, 0) + 1
    
    if plan_counts:
        df_plans = pd.DataFrame(list(plan_counts.items()), columns=['Plan', 'Usuarios'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👥 Usuarios por Plan")
            st.bar_chart(df_plans.set_index('Plan'))
        
        with col2:
            st.subheader("📊 Distribución de Planes")
            st.dataframe(df_plans)
    
    # Estadísticas de pagos
    st.subheader("💳 Estadísticas de Pagos")
    
    if payment_system.payments:
        df_payments = pd.DataFrame(payment_system.payments)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Pagos por estado:**")
            status_counts = df_payments['status'].value_counts()
            st.bar_chart(status_counts)
        
        with col2:
            st.write("**Pagos por plan:**")
            plan_counts = df_payments['plan'].value_counts()
            st.bar_chart(plan_counts)
    else:
        st.info("No hay datos de pagos disponibles")

def main():
    """Función principal del panel de administración"""
    st.set_page_config(
        page_title="Panel Admin - CONSORCIO DEJ",
        page_icon="🔧",
        layout="wide"
    )
    
    # Verificar si el admin está logueado
    if 'admin_logged_in' not in st.session_state:
        st.session_state['admin_logged_in'] = False
    
    if not st.session_state['admin_logged_in']:
        show_admin_login()
    else:
        show_admin_dashboard()

if __name__ == "__main__":
    main() 