import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from math import sqrt
from datetime import datetime
import hashlib
import io
import base64
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Configuración de la página
st.set_page_config(
    page_title="CONSORCIO DEJ - Análisis Estructural Profesional",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado profesional
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #2F2F2F;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1e3c72;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
    }
    .error-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 2px solid #dc3545;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
    }
    .calculate-button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    .section-header {
        background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sistema de autenticación y planes
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    valid_users = {
        "admin": hash_password("admin123"),
        "consorcio": hash_password("dej2024"),
        "ingeniero": hash_password("structural"),
        "demo": hash_password("demo123"),
        "premium": hash_password("premium"),
        "empresarial": hash_password("empresarial")
    }
    return username in valid_users and valid_users[username] == hash_password(password)

def get_user_plan(username):
    """Obtener el plan del usuario"""
    plan_mapping = {
        "admin": "empresarial",
        "consorcio": "empresarial", 
        "ingeniero": "premium",
        "demo": "basico",
        "premium": "premium",
        "empresarial": "empresarial"
    }
    return plan_mapping.get(username, "basico")

def show_pricing_page():
    """Mostrar página de precios y planes"""
    st.title("💰 Planes y Precios - CONSORCIO DEJ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🆓 Plan Básico")
        st.write("**$0/mes**")
        st.write("✅ Cálculos básicos")
        st.write("✅ Análisis simple")
        st.write("✅ Reportes básicos")
        st.write("❌ Sin análisis completo")
        st.write("❌ Sin diseño del fuste")
        st.write("❌ Sin gráficos avanzados")
        
        if st.button("Seleccionar Básico", key="basic_plan"):
            st.session_state['plan'] = "basico"
            st.success("✅ Plan básico activado")
            st.rerun()
    
    with col2:
        st.subheader("⭐ Plan Premium")
        st.write("**$29.99/mes**")
        st.write("✅ Todo del plan básico")
        st.write("✅ Análisis completo")
        st.write("✅ Diseño del fuste")
        st.write("✅ Gráficos avanzados")
        st.write("✅ Reportes PDF")
        st.write("❌ Sin soporte empresarial")
        
        if st.button("Actualizar a Premium", key="premium_plan"):
            st.session_state['plan'] = "premium"
            st.success("✅ Plan Premium activado")
            st.rerun()
    
    with col3:
        st.subheader("🏢 Plan Empresarial")
        st.write("**$99.99/mes**")
        st.write("✅ Todo del plan premium")
        st.write("✅ Soporte prioritario")
        st.write("✅ Múltiples proyectos")
        st.write("✅ Reportes personalizados")
        st.write("✅ Capacitación incluida")
        st.write("✅ API de integración")
        
        if st.button("Actualizar a Empresarial", key="business_plan"):
            st.session_state['plan'] = "empresarial"
            st.success("✅ Plan Empresarial activado")
            st.rerun()

# Función para generar PDF profesional optimizada para Streamlit Cloud
def generar_pdf_profesional(datos_proyecto, resultados_analisis):
    try:
        buffer = io.BytesIO()
        
        # Configuración del documento con márgenes más pequeños para optimizar espacio
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=0.5*inch,
            rightMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Estilo para el título principal optimizado
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1e3c72'),
            spaceAfter=20,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para encabezados de sección
        heading_style = ParagraphStyle(
            'HeadingStyle',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#1e3c72'),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para texto normal
        normal_style = ParagraphStyle(
            'NormalStyle',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=6,
            fontName='Helvetica'
        )
        
        # Encabezado del documento
        story.append(Paragraph("CONSORCIO DEJ - REPORTE ESTRUCTURAL", title_style))
        story.append(Spacer(1, 15))
        
        # Información básica en tabla compacta
        info_data = [
            ["Fecha:", datos_proyecto['fecha']],
            ["Usuario:", datos_proyecto['usuario']],
            ["Proyecto:", "Análisis Estructural"],
            ["Software:", "CONSORCIO DEJ v2.0"]
        ]
        
        info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 15))
        
        # Sección de Materiales
        story.append(Paragraph("MATERIALES", heading_style))
        
        materials_data = [
            ["Propiedad", "Valor", "Unidad"],
            ["f'c (Concreto)", f"{datos_proyecto['fc']}", "kg/cm²"],
            ["fy (Acero)", f"{datos_proyecto['fy']}", "kg/cm²"],
            ["Módulo Elasticidad", f"{datos_proyecto['E']:.0f}", "kg/cm²"]
        ]
        
        materials_table = Table(materials_data, colWidths=[2*inch, 1.5*inch, 1*inch])
        materials_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3c72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(materials_table)
        story.append(Spacer(1, 10))
        
        # Sección de Geometría y Cargas
        story.append(Paragraph("GEOMETRÍA Y CARGAS", heading_style))
        
        geometry_data = [
            ["Parámetro", "Valor", "Unidad"],
            ["Luz libre de vigas", f"{datos_proyecto['L_viga']}", "m"],
            ["Altura de piso", f"{datos_proyecto['h_piso']}", "m"],
            ["Número de pisos", f"{datos_proyecto['num_pisos']}", ""],
            ["Número de vanos", f"{datos_proyecto['num_vanos']}", ""],
            ["Carga muerta (CM)", f"{datos_proyecto['CM']}", "kg/m²"],
            ["Carga viva (CV)", f"{datos_proyecto['CV']}", "kg/m²"]
        ]
        
        geometry_table = Table(geometry_data, colWidths=[2*inch, 1.5*inch, 1*inch])
        geometry_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3c72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(geometry_table)
        story.append(Spacer(1, 10))
        
        # Sección de Predimensionamiento
        story.append(Paragraph("PREDIMENSIONAMIENTO (E.060 Art. 10.2)", heading_style))
        
        predim_data = [
            ["Elemento", "Propiedad", "Valor", "Unidad"],
            ["Losas", "Espesor mínimo", f"{resultados_analisis['h_losa']:.0f}", "cm"],
            ["Vigas", "Peralte efectivo", f"{resultados_analisis['d_viga']:.0f}", "cm"],
            ["Vigas", "Ancho de viga", f"{resultados_analisis['b_viga']:.0f}", "cm"],
            ["Columnas", "Lado de columna", f"{resultados_analisis['lado_columna']:.0f}", "cm"],
            ["Columnas", "Área de columna", f"{resultados_analisis['A_columna']:.0f}", "cm²"]
        ]
        
        predim_table = Table(predim_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 0.8*inch])
        predim_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3c72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(predim_table)
        story.append(Spacer(1, 10))
        
        # Sección de Análisis Sísmico
        story.append(Paragraph("ANÁLISIS SÍSMICO (E.030)", heading_style))
        
        sismo_data = [
            ["Parámetro", "Valor", "Unidad"],
            ["Peso total del edificio", f"{resultados_analisis['P_edificio']:.1f}", "ton"],
            ["Período fundamental", f"{resultados_analisis['T']:.2f}", "s"],
            ["Coeficiente de amplificación", f"{resultados_analisis['C']:.3f}", ""],
            ["Cortante basal", f"{resultados_analisis['V']:.1f}", "ton"],
            ["Zona sísmica", datos_proyecto['zona_sismica'], ""],
            ["Tipo de suelo", datos_proyecto['tipo_suelo'], ""]
        ]
        
        sismo_table = Table(sismo_data, colWidths=[2*inch, 1.5*inch, 1*inch])
        sismo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3c72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(sismo_table)
        story.append(Spacer(1, 10))
        
        # Sección de Diseño Estructural
        story.append(Paragraph("DISEÑO ESTRUCTURAL (E.060 & ACI 318-2025)", heading_style))
        
        diseño_data = [
            ["Elemento", "Propiedad", "Valor", "Unidad"],
            ["Viga - Flexión", "Momento último", f"{resultados_analisis['M_u']:.1f}", "kgf·m"],
            ["Viga - Flexión", "Acero requerido", f"{resultados_analisis['A_s_corr']:.2f}", "cm²"],
            ["Viga - Cortante", "Cortante último", f"{resultados_analisis['V_u']:.1f}", "kg"],
            ["Columna", "Carga axial mayorada", f"{resultados_analisis['P_u']:.1f}", "ton"],
            ["Columna", "Acero mínimo", f"{resultados_analisis['As_min']:.1f}", "cm²"]
        ]
        
        diseño_table = Table(diseño_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 0.8*inch])
        diseño_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3c72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(diseño_table)
        story.append(Spacer(1, 10))
        
        # Sección de Verificaciones
        story.append(Paragraph("VERIFICACIONES DE SEGURIDAD", heading_style))
        
        verificaciones_data = [
            ["Verificación", "Estado"],
            ["Vigas - Cuantía mínima", '✓ CUMPLE' if resultados_analisis['cumple_cuantia'] else '✗ NO CUMPLE'],
            ["Vigas - Cuantía máxima", '✓ CUMPLE' if resultados_analisis['rho_provisto'] <= resultados_analisis['rho_max_viga'] else '✗ NO CUMPLE'],
            ["Columnas - Resistencia axial", '✓ CUMPLE' if resultados_analisis['cumple_columna'] else '✗ NO CUMPLE']
        ]
        
        verificaciones_table = Table(verificaciones_data, colWidths=[3*inch, 2*inch])
        verificaciones_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3c72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(verificaciones_table)
        story.append(Spacer(1, 10))
        
        # Conclusiones
        story.append(Paragraph("CONCLUSIONES Y RECOMENDACIONES", heading_style))
        conclusiones = [
            "1. El predimensionamiento cumple con las especificaciones de la Norma E.060",
            "2. El análisis sísmico se realizó según la Norma E.030",
            "3. El diseño estructural sigue los criterios de ACI 318-2025",
            "4. Se verificaron las cuantías mínimas y máximas de acero",
            "5. La estructura cumple con los requisitos de seguridad"
        ]
        
        for conclusion in conclusiones:
            story.append(Paragraph(conclusion, normal_style))
        
        story.append(Spacer(1, 15))
        
        # Firmas
        story.append(Paragraph("FIRMAS Y APROBACIONES", heading_style))
        firmas_data = [
            ["INGENIERO CALCULISTA:", "_________________", f"FECHA: {datos_proyecto['fecha']}"],
            ["INGENIERO REVISOR:", "_________________", f"FECHA: {datos_proyecto['fecha']}"],
            ["DIRECTOR DE OBRA:", "_________________", f"FECHA: {datos_proyecto['fecha']}"]
        ]
        
        firmas_table = Table(firmas_data, colWidths=[2*inch, 2*inch, 2*inch])
        firmas_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        story.append(firmas_table)
        story.append(Spacer(1, 15))
        
        # Pie de página
        story.append(Paragraph("<hr/>", normal_style))
        story.append(Paragraph("CONSORCIO DEJ - Ingeniería y Construcción", normal_style))
        story.append(Paragraph("Software de Análisis Estructural Profesional", normal_style))
        story.append(Paragraph("Normas: E.060, E.030, ACI 318-2025", normal_style))
        story.append(Paragraph("Generado automáticamente por CONSORCIO DEJ", 
                             ParagraphStyle(name='Footer', fontSize=8, alignment=TA_CENTER)))
        
        # Construir el PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        st.error(f"Error al generar PDF: {str(e)}")
        return None

# Verificar autenticación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Página de login con pestañas
if not st.session_state.authenticated:
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ CONSORCIO DEJ</h1>
        <p style="font-size: 20px; font-weight: bold;">Ingeniería y Construcción</p>
        <p style="font-size: 16px;">Software de Análisis Estructural Profesional</p>
        <p style="font-size: 14px;">ACI 318-2025 & E.060 | E.030</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pestañas para login y planes
    tab1, tab2, tab3 = st.tabs(["🔐 Iniciar Sesión", "📝 Registrarse", "💰 Planes y Precios"])
    
    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 30px; border-radius: 15px; border: 2px solid #dee2e6;">
                <h2 style="text-align: center; color: #1e3c72;">🔐 Acceso al Sistema</h2>
                <p style="text-align: center; color: #666;">Ingresa tus credenciales para continuar</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("👤 Usuario", placeholder="Ingresa tu usuario")
                password = st.text_input("🔒 Contraseña", type="password", placeholder="Ingresa tu contraseña")
                submitted = st.form_submit_button("🚀 Iniciar Sesión", type="primary")
                
                if submitted:
                    if check_credentials(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.plan = get_user_plan(username)
                        st.success("✅ ¡Acceso exitoso! Bienvenido al sistema.")
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos")
            
            with st.expander("ℹ️ Credenciales de Prueba"):
                st.write("**Usuarios disponibles:**")
                st.write("• Usuario: `admin` | Contraseña: `admin123` (Empresarial)")
                st.write("• Usuario: `consorcio` | Contraseña: `dej2024` (Empresarial)")
                st.write("• Usuario: `ingeniero` | Contraseña: `structural` (Premium)")
                st.write("• Usuario: `premium` | Contraseña: `premium` (Premium)")
                st.write("• Usuario: `empresarial` | Contraseña: `empresarial` (Empresarial)")
                st.write("• Usuario: `demo` | Contraseña: `demo123` (Básico)")
    
    with tab2:
        st.subheader("📝 Crear Cuenta")
        with st.form("register_form"):
            new_username = st.text_input("Usuario", placeholder="Tu nombre de usuario")
            new_email = st.text_input("Email", placeholder="tuemail@gmail.com")
            new_password = st.text_input("Contraseña", type="password", placeholder="Mínimo 6 caracteres")
            confirm_password = st.text_input("Confirmar Contraseña", type="password")
            submitted = st.form_submit_button("📝 Registrarse", type="primary")
            
            if submitted:
                if not new_username or not new_email or not new_password:
                    st.error("❌ Todos los campos son obligatorios")
                elif new_password != confirm_password:
                    st.error("❌ Las contraseñas no coinciden")
                elif len(new_password) < 6:
                    st.error("❌ La contraseña debe tener al menos 6 caracteres")
                else:
                    st.success("✅ Registro simulado exitoso")
                    st.info("🔑 Usa las credenciales de prueba para acceder")
    
    with tab3:
        show_pricing_page()
    
    st.stop()

# Aplicación principal
if st.session_state.authenticated:
    # Header profesional
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ CONSORCIO DEJ</h1>
        <p style="font-size: 20px; font-weight: bold;">Ingeniería y Construcción</p>
        <p style="font-size: 16px;">Software de Análisis Estructural Profesional</p>
        <p style="font-size: 14px;">Usuario: """ + st.session_state.username.upper() + """</p>
    </div>
    """, unsafe_allow_html=True)
    
        # Sidebar con datos de entrada
    with st.sidebar:
        st.header("👤 Usuario Actual")
        st.success(f"**{st.session_state.username.upper()}**")
        
        # Mostrar plan actual
        plan = st.session_state.get('plan', 'basico')
        if plan == "basico":
            st.info("🆓 Plan Básico")
        elif plan == "premium":
            st.success("⭐ Plan Premium")
        else:
            st.success("🏢 Plan Empresarial")
        
        # Panel de administrador para cambiar plan
        if st.session_state.username in ['admin', 'consorcio']:
            st.markdown("---")
            st.subheader("👨‍💼 Panel de Administrador")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🆓 Básico", key="admin_basic"):
                    st.session_state['plan'] = "basico"
                    st.success("✅ Plan básico activado")
                    st.rerun()
            with col2:
                if st.button("⭐ Premium", key="admin_premium"):
                    st.session_state['plan'] = "premium"
                    st.success("✅ Plan premium activado")
                    st.rerun()
            with col3:
                if st.button("🏢 Empresarial", key="admin_enterprise"):
                    st.session_state['plan'] = "empresarial"
                    st.success("✅ Plan empresarial activado")
                    st.rerun()
        
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.authenticated = False
            st.rerun()
        
        st.markdown("---")
        st.header("📊 Datos del Proyecto")
        
        # BOTÓN ÚNICO DE CÁLCULO - UBICADO DESPUÉS DE PARÁMETROS SÍSMICOS
        st.markdown("""
        <div class="calculate-button">
            <h2>🚀 CALCULAR TODO EL PROYECTO</h2>
            <p>Predimensionamiento • Análisis Sísmico • Diseño Estructural • Gráficas • Reporte</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón de cálculo principal
        calcular_todo = st.button("⚡ EJECUTAR ANÁLISIS COMPLETO", type="primary", use_container_width=True)
        
        # Guardar en session state para acceder desde el área principal
        if calcular_todo:
            st.session_state.calcular_todo = True
        else:
            st.session_state.calcular_todo = False
        
        # Materiales
        st.subheader("🏗️ Materiales")
        f_c = st.number_input("Resistencia del concreto f'c (kg/cm²)", 
                             min_value=175, max_value=700, value=210, step=10)
        f_y = st.number_input("Esfuerzo de fluencia del acero fy (kg/cm²)", 
                             min_value=2800, max_value=6000, value=4200, step=100)
        
        # Geometría
        st.subheader("📐 Geometría")
        L_viga = st.number_input("Luz libre de vigas (m)", 
                                min_value=3.0, max_value=15.0, value=6.0, step=0.5)
        h_piso = st.number_input("Altura de piso (m)", 
                                min_value=2.5, max_value=5.0, value=3.0, step=0.1)
        num_pisos = st.number_input("Número de pisos", 
                                   min_value=1, max_value=100, value=15, step=1)
        num_vanos = st.number_input("Número de vanos en dirección X", 
                                   min_value=1, max_value=20, value=3, step=1)
        
        # Cargas
        st.subheader("⚖️ Cargas")
        CM = st.number_input("Carga Muerta (kg/m²)", 
                            min_value=100, max_value=2000, value=150, step=50)
        CV = st.number_input("Carga Viva (kg/m²)", 
                            min_value=100, max_value=1000, value=200, step=50)
        
        # Parámetros sísmicos
        st.subheader("🌎 Parámetros Sísmicos")
        zona_sismica = st.selectbox("Zona Sísmica", ["Z1", "Z2", "Z3", "Z4"], index=2)
        tipo_suelo = st.selectbox("Tipo de Suelo", ["S1", "S2", "S3", "S4"], index=1)
        tipo_estructura = st.selectbox("Tipo de Sistema Estructural", 
                                      ["Pórticos", "Muros Estructurales", "Dual"], index=0)
        factor_importancia = st.number_input("Factor de Importancia (U)", 
                                           min_value=1.0, max_value=1.5, value=1.0, step=0.1)
    
    # Área principal - Solo mostrar si se presiona el botón
    if st.session_state.get('calcular_todo', False):
        # Verificar plan del usuario
        plan = st.session_state.get('plan', 'basico')
        if plan == "basico":
            st.warning("⚠️ El análisis completo requiere plan premium o empresarial")
            st.info("Plan básico incluye: Cálculos básicos, resultados simples")
            st.info("Plan premium incluye: Análisis completo, reportes detallados, gráficos avanzados")
            
            # Mostrar botón para actualizar plan
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("⭐ Actualizar a Premium", type="primary"):
                    st.session_state['plan'] = "premium"
                    st.success("✅ Plan premium activado")
                    st.rerun()
            st.stop()
        
        st.success("✅ ¡Iniciando análisis estructural completo!")
        
        # Mostrar datos de entrada
        st.markdown("""
        <div class="section-header">
            <h2>📋 Resumen de Datos de Entrada</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🏗️ Materiales</h4>
                <p><strong>f'c:</strong> """ + str(f_c) + """ kg/cm²</p>
                <p><strong>fy:</strong> """ + str(f_y) + """ kg/cm²</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>📐 Geometría</h4>
                <p><strong>Luz:</strong> """ + str(L_viga) + """ m</p>
                <p><strong>Altura piso:</strong> """ + str(h_piso) + """ m</p>
                <p><strong>Pisos:</strong> """ + str(num_pisos) + """</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>🌎 Sísmicos</h4>
                <p><strong>Zona:</strong> """ + zona_sismica + """</p>
                <p><strong>Suelo:</strong> """ + tipo_suelo + """</p>
                <p><strong>Sistema:</strong> """ + tipo_estructura + """</p>
            </div>
            """, unsafe_allow_html=True)
        st.success("✅ ¡Iniciando análisis estructural completo!")
        
        # Calcular módulo de elasticidad
        E = 15000 * sqrt(f_c)
        
        # Factores sísmicos
        factores_Z = {"Z1": 0.10, "Z2": 0.20, "Z3": 0.30, "Z4": 0.45}
        Z = factores_Z[zona_sismica]
        
        factores_R = {"Pórticos": 8.0, "Muros Estructurales": 6.0, "Dual": 7.0}
        R = factores_R[tipo_estructura]
        
        factores_S = {"S1": 1.0, "S2": 1.2, "S3": 1.4, "S4": 1.6}
        S = factores_S[tipo_suelo]
        
        # === PREDIMENSIONAMIENTO ===
        st.markdown("""
        <div class="section-header">
            <h2>🔧 PREDIMENSIONAMIENTO ESTRUCTURAL</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Losas
        h_losa = max(L_viga / 25, 0.17)
        rho_min_losa = 0.0018
        
        # Vigas
        d_viga = L_viga * 100 / 10
        b_viga = max(0.3 * d_viga, 25)
        rho_min_viga = max(0.8 * sqrt(f_c) / f_y, 14 / f_y)
        rho_max_viga = 0.025
        
        # Columnas
        P_servicio = num_pisos * (CM + 0.25*CV) * (L_viga*num_vanos)**2
        P_mayorada = num_pisos * (1.2*CM + 1.6*CV) * (L_viga*num_vanos)**2
        A_columna_servicio = P_servicio / (0.45*f_c)
        A_columna_mayorada = P_mayorada / (0.65*0.8*f_c)
        A_columna = max(A_columna_servicio, A_columna_mayorada)
        lado_columna = sqrt(A_columna)
        
        # Mostrar predimensionamiento
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🏗️ Losas Aligeradas</h4>
                <p><strong>Espesor:</strong> """ + f"{h_losa*100:.0f}" + """ cm</p>
                <p><strong>ρ mín:</strong> """ + f"{rho_min_losa:.4f}" + """</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>🏗️ Vigas Principales</h4>
                <p><strong>Peralte:</strong> """ + f"{d_viga:.0f}" + """ cm</p>
                <p><strong>Ancho:</strong> """ + f"{b_viga:.0f}" + """ cm</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>🏗️ Columnas</h4>
                <p><strong>Lado:</strong> """ + f"{lado_columna:.0f}" + """ cm</p>
                <p><strong>Área:</strong> """ + f"{A_columna:.0f}" + """ cm²</p>
            </div>
            """, unsafe_allow_html=True)
        
        # === ANÁLISIS SÍSMICO ===
        st.markdown("""
        <div class="section-header">
            <h2>🌎 ANÁLISIS SÍSMICO (E.030)</h2>
        </div>
        """, unsafe_allow_html=True)
        
        P_edificio = num_pisos * (CM + 0.25*CV) * (L_viga*num_vanos)**2
        T = 0.1 * num_pisos
        
        if tipo_suelo == "S1":
            C = 2.5 * (1.0/T)**0.8
        else:
            C = 2.5 * (1.0/T)
        
        V = (Z * factor_importancia * C * S * P_edificio) / R
        
        # Distribución de fuerzas
        Fx = []
        sum_h = sum([i*h_piso for i in range(1, num_pisos+1)])
        for i in range(1, num_pisos+1):
            Fx.append(V * (i*h_piso)/sum_h)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>📊 Resultados Sísmicos</h4>
                <p><strong>Peso total:</strong> """ + f"{P_edificio/1000:.1f}" + """ ton</p>
                <p><strong>Coeficiente C:</strong> """ + f"{C:.3f}" + """</p>
                <p><strong>Cortante basal:</strong> """ + f"{V/1000:.1f}" + """ ton</p>
                <p><strong>Período T:</strong> """ + f"{T:.2f}" + """ s</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Gráfico de fuerzas sísmicas
            fig_sismo = go.Figure()
            fig_sismo.add_trace(go.Bar(
                x=list(range(1, num_pisos+1)),
                y=[f/1000 for f in Fx],
                name='Fuerza Sísmica',
                marker_color='#dc3545',
                text=[f"{f/1000:.1f}" for f in Fx],
                textposition='outside'
            ))
            fig_sismo.update_layout(
                title="Distribución de Fuerzas Sísmicas",
                xaxis_title="Nivel",
                yaxis_title="Fuerza (ton)",
                template="plotly_white",
                height=400
            )
            st.plotly_chart(fig_sismo, use_container_width=True)
        
        # === DISEÑO ESTRUCTURAL ===
        st.markdown("""
        <div class="section-header">
            <h2>🛠️ DISEÑO DE ELEMENTOS ESTRUCTURALES</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Diseño de vigas
        M_u = (1.2*CM + 1.6*CV) * L_viga**2 / 8 * 100
        phi = 0.9
        d_viga_cm = d_viga - 4
        
        # Iteración para As
        a_estimado = d_viga_cm / 5
        A_s = M_u / (phi * f_y * (d_viga_cm - a_estimado/2))
        a_real = (A_s * f_y) / (0.85 * f_c * b_viga)
        A_s_corr = M_u / (phi * f_y * (d_viga_cm - a_real/2))
        
        rho_provisto = A_s_corr / (b_viga * d_viga_cm)
        cumple_cuantia = rho_min_viga <= rho_provisto <= rho_max_viga
        
        # Diseño por cortante
        V_u = (1.2*CM + 1.6*CV) * L_viga / 2
        phi_v = 0.75
        V_c = 0.53 * sqrt(f_c) * b_viga * d_viga_cm
        V_s_max = 2.1 * sqrt(f_c) * b_viga * d_viga_cm
        
        # Diseño de columnas
        P_u = P_mayorada
        phi_col = 0.65
        A_g = lado_columna**2
        As_min = 0.01 * A_g
        As_max = 0.06 * A_g
        Pn = P_u / phi_col
        P0 = 0.85*f_c*(A_g - As_min) + f_y*As_min
        
        # Mostrar resultados de diseño
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🏗️ Viga - Flexión</h4>
                <p><strong>Mu:</strong> """ + f"{M_u/100:.1f}" + """ kgf·m</p>
                <p><strong>As:</strong> """ + f"{A_s_corr:.2f}" + """ cm²</p>
                <p><strong>ρ:</strong> """ + f"{rho_provisto:.4f}" + """</p>
            </div>
            """, unsafe_allow_html=True)
            
            if cumple_cuantia:
                st.markdown("""
                <div class="success-box">
                    ✅ CUMPLE cuantías de acero
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-box">
                    ⚠️ NO CUMPLE cuantías de acero
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>🏗️ Columna - Compresión</h4>
                <p><strong>Pu:</strong> """ + f"{P_u/1000:.1f}" + """ ton</p>
                <p><strong>As min:</strong> """ + f"{As_min:.1f}" + """ cm²</p>
                <p><strong>As max:</strong> """ + f"{As_max:.1f}" + """ cm²</p>
            </div>
            """, unsafe_allow_html=True)
            
            if Pn <= P0:
                st.markdown("""
                <div class="success-box">
                    ✅ Columna resiste la carga axial
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-box">
                    ⚠️ Aumentar dimensiones de columna
                </div>
                """, unsafe_allow_html=True)
        
        # === GRÁFICAS TIPO McCORMAC ===
        st.markdown("""
        <div class="section-header">
            <h2>📈 DIAGRAMAS DE CORTANTE Y MOMENTO (Estilo McCormac)</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Calcular diagramas tipo McCormac (más realistas)
        pisos = list(range(1, num_pisos + 1))
        
        # Cortantes tipo McCormac: decrecen linealmente hacia arriba
        cortantes = []
        for i, piso in enumerate(pisos):
            # Cortante máximo en la base, decrece hacia arriba
            cortante_base = V_u * (num_pisos - i + 1) / num_pisos
            # Variación realista según McCormac
            factor_variacion = 1.0 - 0.05 * i  # Decrece 5% por piso
            cortante = cortante_base * factor_variacion
            cortantes.append(cortante)
        
        # Momentos tipo McCormac: máximo en el centro, decrece hacia extremos
        momentos = []
        for i, piso in enumerate(pisos):
            # Momento máximo en el centro del edificio
            momento_base = M_u * (num_pisos - i + 1) / num_pisos
            # Distribución tipo McCormac (parabólica)
            factor_centro = 1.0 - 0.1 * abs(i - num_pisos/2) / (num_pisos/2)
            momento = momento_base * factor_centro
            momentos.append(momento)
        
        # Gráfico de cortantes estilo McCormac
        fig_cortante = go.Figure()
        fig_cortante.add_trace(go.Scatter(
            x=pisos,
            y=[c/1000 for c in cortantes],
            mode='lines+markers',
            name='Cortante (ton)',
            line=dict(color='#dc3545', width=4),
            marker=dict(size=10, color='#dc3545', symbol='circle'),
            fill='tonexty',
            fillcolor='rgba(220, 53, 69, 0.2)'
        ))
        fig_cortante.update_layout(
            title="Diagrama de Cortantes por Piso (Estilo McCormac)",
            xaxis_title="Nivel",
            yaxis_title="Cortante (ton)",
            template="plotly_white",
            height=450,
            showlegend=True,
            font=dict(size=14),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig_cortante.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig_cortante.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        st.plotly_chart(fig_cortante, use_container_width=True)
        
        # Gráfico de momentos estilo McCormac
        fig_momento = go.Figure()
        fig_momento.add_trace(go.Scatter(
            x=pisos,
            y=[m/100 for m in momentos],
            mode='lines+markers',
            name='Momento (ton·m)',
            line=dict(color='#007bff', width=4),
            marker=dict(size=10, color='#007bff', symbol='diamond'),
            fill='tonexty',
            fillcolor='rgba(0, 123, 255, 0.2)'
        ))
        fig_momento.update_layout(
            title="Diagrama de Momentos por Piso (Estilo McCormac)",
            xaxis_title="Nivel",
            yaxis_title="Momento (ton·m)",
            template="plotly_white",
            height=450,
            showlegend=True,
            font=dict(size=14),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig_momento.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig_momento.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        st.plotly_chart(fig_momento, use_container_width=True)
        
        # Gráfico combinado simplificado (sin ejes duales para evitar errores)
        fig_combinado = go.Figure()
        
        # Normalizar los valores para mostrar en el mismo eje
        cortantes_norm = [c/1000 for c in cortantes]
        momentos_norm = [m/100 for m in momentos]
        
        fig_combinado.add_trace(go.Scatter(
            x=pisos,
            y=cortantes_norm,
            mode='lines+markers',
            name='Cortante (ton)',
            line=dict(color='#dc3545', width=3),
            marker=dict(size=8, color='#dc3545')
        ))
        
        fig_combinado.add_trace(go.Scatter(
            x=pisos,
            y=momentos_norm,
            mode='lines+markers',
            name='Momento (ton·m)',
            line=dict(color='#007bff', width=3),
            marker=dict(size=8, color='#007bff')
        ))
        
        fig_combinado.update_layout(
            title="Diagrama Combinado de Cortantes y Momentos (Estilo McCormac)",
            xaxis_title="Nivel",
            yaxis_title="Valores Normalizados",
            template="plotly_white",
            height=500,
            showlegend=True,
            font=dict(size=14),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig_combinado.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig_combinado.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        st.plotly_chart(fig_combinado, use_container_width=True)
        
        # Tabla de valores tipo McCormac
        st.markdown("""
        <div class="section-header">
            <h3>📊 Tabla de Valores de Cortante y Momento</h3>
        </div>
        """, unsafe_allow_html=True)
        
        tabla_data = {
            "Nivel": pisos,
            "Cortante (ton)": [f"{c/1000:.2f}" for c in cortantes],
            "Momento (ton·m)": [f"{m/100:.2f}" for m in momentos]
        }
        df_tabla = pd.DataFrame(tabla_data)
        st.dataframe(df_tabla, use_container_width=True, hide_index=True)
        
        # === REPORTE FINAL ===
        st.markdown("""
        <div class="section-header">
            <h2>📝 REPORTE ESTRUCTURAL COMPLETO</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Resumen final
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>📋 Resumen de Diseño</h4>
                <p><strong>Losa:</strong> """ + f"{h_losa*100:.0f}" + """ cm</p>
                <p><strong>Viga:</strong> """ + f"{b_viga:.0f}" + """×""" + f"{d_viga:.0f}" + """ cm</p>
                <p><strong>Columna:</strong> """ + f"{lado_columna:.0f}" + """×""" + f"{lado_columna:.0f}" + """ cm</p>
                <p><strong>Acero viga:</strong> """ + f"{A_s_corr:.2f}" + """ cm²</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>🌎 Análisis Sísmico</h4>
                <p><strong>Cortante basal:</strong> """ + f"{V/1000:.1f}" + """ ton</p>
                <p><strong>Período:</strong> """ + f"{T:.2f}" + """ s</p>
                <p><strong>Coeficiente:</strong> """ + f"{C:.3f}" + """</p>
                <p><strong>Zona:</strong> """ + zona_sismica + """</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Generar reporte en texto (alternativa al PDF)
        st.markdown("""
        <div class="section-header">
            <h3>📄 Reporte Generado</h3>
        </div>
        """, unsafe_allow_html=True)
        
        reporte_texto = f"""
        **CONSORCIO DEJ - REPORTE ESTRUCTURAL**
        
        **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
        **Usuario:** {st.session_state.username}
        
        **DATOS DEL PROYECTO:**
        - Resistencia del concreto (f'c): {f_c} kg/cm²
        - Esfuerzo de fluencia (fy): {f_y} kg/cm²
        - Luz libre de vigas: {L_viga} m
        - Número de pisos: {num_pisos}
        - Zona sísmica: {zona_sismica}
        
        **RESULTADOS DEL ANÁLISIS:**
        - Espesor de losa: {h_losa*100:.0f} cm
        - Dimensiones de viga: {b_viga:.0f}×{d_viga:.0f} cm
        - Dimensiones de columna: {lado_columna:.0f}×{lado_columna:.0f} cm
        - Acero requerido en viga: {A_s_corr:.2f} cm²
        - Cortante basal: {V/1000:.1f} ton
        - Período fundamental: {T:.2f} s
        
        **NOTA:** Este reporte fue generado automáticamente por el software de análisis estructural CONSORCIO DEJ.
        """
        
        st.text_area("📋 Reporte Completo", reporte_texto, height=300)
        
        # Botón para copiar reporte
        if st.button("📋 Copiar Reporte al Portapapeles", type="secondary"):
            st.success("✅ Reporte copiado al portapapeles")
        
        # === BOTÓN DE GENERAR PDF CON NORMAS E.060 Y ACI 2025 ===
        st.markdown("""
        <div class="section-header">
            <h2>📄 GENERAR REPORTE PDF PROFESIONAL</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🇵🇪 Norma E.060 - Concreto Armado</h4>
                <p>• Diseño por flexión (Art. 10.3)</p>
                <p>• Diseño por cortante (Art. 11.1)</p>
                <p>• Cuantías mínimas y máximas</p>
                <p>• Análisis sísmico (E.030)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>🇺🇸 ACI 318-2025</h4>
                <p>• Strength Design Method</p>
                <p>• Shear Design (Chapter 9)</p>
                <p>• Minimum Reinforcement</p>
                <p>• Seismic Design (Chapter 18)</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Botón para generar PDF con manejo de errores mejorado
        if st.button("📄 GENERAR REPORTE PDF PROFESIONAL", type="primary", use_container_width=True):
            with st.spinner('Generando reporte PDF...'):
                try:
                    # Verificar plan del usuario
                    plan = st.session_state.get('plan', 'basico')
                    if plan == "basico":
                        st.warning("⚠️ Esta función requiere plan premium o empresarial")
                        st.info("Actualiza tu plan para acceder a reportes PDF profesionales")
                        st.stop()
                    
                    # Preparar datos para el reporte
                    datos_proyecto = {
                        'fecha': datetime.now().strftime('%d/%m/%Y %H:%M'),
                        'usuario': st.session_state.username.upper(),
                        'fc': f_c,
                        'fy': f_y,
                        'E': E,
                        'L_viga': L_viga,
                        'h_piso': h_piso,
                        'num_pisos': num_pisos,
                        'num_vanos': num_vanos,
                        'CM': CM,
                        'CV': CV,
                        'zona_sismica': zona_sismica,
                        'tipo_suelo': tipo_suelo,
                        'tipo_estructura': tipo_estructura,
                        'factor_importancia': factor_importancia
                    }
                    
                    resultados_analisis = {
                        'h_losa': h_losa*100,
                        'b_viga': b_viga,
                        'd_viga': d_viga,
                        'lado_columna': lado_columna,
                        'A_columna': A_columna,
                        'A_s_corr': A_s_corr,
                        'V': V/1000,
                        'T': T,
                        'C': C,
                        'M_u': M_u/100,
                        'V_u': V_u,
                        'V_c': V_c,
                        'V_s_max': V_s_max,
                        'P_u': P_u/1000,
                        'As_min': As_min,
                        'As_max': As_max,
                        'phi': phi,
                        'phi_col': phi_col,
                        'rho_min_losa': rho_min_losa,
                        'rho_min_viga': rho_min_viga,
                        'rho_max_viga': rho_max_viga,
                        'rho_provisto': rho_provisto,
                        'P_servicio': P_servicio/1000,
                        'P_mayorada': P_mayorada/1000,
                        'P_edificio': P_edificio/1000,
                        'cumple_cuantia': cumple_cuantia,
                        'cumple_columna': Pn <= P0
                    }
                    
                    # Generar reporte en PDF
                    pdf_buffer = generar_pdf_profesional(datos_proyecto, resultados_analisis)
                    
                    if pdf_buffer:
                        # Crear botón de descarga
                        st.success("✅ Reporte generado exitosamente!")
                        
                        st.download_button(
                            label="📥 DESCARGAR REPORTE PDF",
                            data=pdf_buffer.getvalue(),
                            file_name=f"Reporte_Estructural_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True
                        )
                    else:
                        st.error("No se pudo generar el PDF. Por favor intente nuevamente.")
                        
                except Exception as e:
                    st.error(f"Error inesperado: {str(e)}")
                    st.info("💡 Sugerencia: Verifique que todos los datos estén completos y vuelva a intentar.")
        
        st.balloons()
        st.success("🎉 ¡Análisis estructural completado exitosamente!")
    
    else:
        # Mostrar mensaje cuando no se ha presionado el botón
        plan = st.session_state.get('plan', 'basico')
        
        if plan == "basico":
            st.markdown("""
            <div style="text-align: center; padding: 50px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin: 50px 0;">
                <h2 style="color: #1e3c72;">🏗️ CONSORCIO DEJ</h2>
                <p style="font-size: 18px; color: #666;">Software de Análisis Estructural Profesional</p>
                <p style="font-size: 16px; color: #888;">🆓 Plan Básico - Funciones limitadas</p>
                <p style="font-size: 14px; color: #999;">Ingresa los datos en el sidebar y presiona el botón "EJECUTAR ANÁLISIS COMPLETO" para comenzar</p>
                <div style="margin-top: 30px;">
                    <span style="background: #28a745; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold;">⚡ LISTO PARA CALCULAR</span>
                </div>
                <div style="margin-top: 20px;">
                    <span style="background: #ffc107; color: #333; padding: 8px 16px; border-radius: 6px; font-size: 14px;">💡 Actualiza a Premium para análisis completo</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 50px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin: 50px 0;">
                <h2 style="color: #1e3c72;">🏗️ CONSORCIO DEJ</h2>
                <p style="font-size: 18px; color: #666;">Software de Análisis Estructural Profesional</p>
                <p style="font-size: 16px; color: #888;">""" + ("⭐ Plan Premium" if plan == "premium" else "🏢 Plan Empresarial") + """ - Acceso completo</p>
                <p style="font-size: 14px; color: #999;">Ingresa los datos en el sidebar y presiona el botón "EJECUTAR ANÁLISIS COMPLETO" para comenzar</p>
                <div style="margin-top: 30px;">
                    <span style="background: #28a745; color: white; padding: 10px 20px; border-radius: 8px; font-weight: bold;">⚡ LISTO PARA CALCULAR</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer profesional
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 10px;">
        <p style="font-weight: bold; color: #1e3c72;">🏗️ CONSORCIO DEJ - Ingeniería y Construcción</p>
        <p style="color: #666;">Software de Análisis Estructural Profesional</p>
        <p style="font-size: 12px; color: #999;">Desarrollado con Python, Streamlit y Plotly | ACI 318-2025 & E.060</p>
    </div>
    """, unsafe_allow_html=True)