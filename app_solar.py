import streamlit as st

# Configuración de página centrada
st.set_page_config(page_title="Sestri Energía - Relevamiento", layout="centered")

# --- BLOQUE COMERCIAL DE INICIO ---
st.title("⚡ ¿Problemas con cortes de energía?")
st.subheader("Nosotros podemos ayudarte.")
st.write("Dejanos saber tus necesidades enviándonos la info con un simple clic. **Somos Sestri Energía.**")

# Espacio visual
st.markdown("---")

with st.form("relevamiento_sestri"):
    # --- SECCIÓN 1: OBJETIVO ---
    st.subheader("1. ¿Qué buscás resolver?")
    objetivo = st.radio(
        "Seleccioná tu prioridad:",
        ["Back-Up (Respaldo ante cortes)", "Ahorrar Energía (Autoconsumo)", "Ambas opciones"],
        index=0
    )
    
    st.divider()

    # --- SECCIÓN 2: CONSUMOS CRÍTICOS ---
    st.subheader("2. Consumos Críticos")
    st.write("Marcá qué equipos necesitás mantener encendidos siempre:")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Dispositivo**")
        eq1 = st.checkbox("Heladera / Freezer")
        eq2 = st.checkbox("Iluminación (LED)")
        eq3 = st.checkbox("Bomba de Agua")
        eq4 = st.checkbox("Internet / Cámaras / Alarmas")
        otro_nombre = st.text_input("Otro equipo específico:")
    
    with col2:
        st.write("**Uso (Horas/Día)**")
        h1 = st.number_input("H. Heladera", min_value=0, max_value=24, step=1, label_visibility="collapsed")
        h2 = st.number_input("H. Luces", min_value=0, max_value=24, step=1, label_visibility="collapsed")
        h3 = st.number_input("H. Bomba", min_value=0, max_value=24, step=1, label_visibility="collapsed")
        h4 = st.number_input("H. Internet", min_value=0, max_value=24, step=1, label_visibility="collapsed")
        h5 = st.number_input("H. Otro", min_value=0, max_value=24, step=1, label_visibility="collapsed")

    st.divider()
    
    # --- SECCIÓN 3: CONTACTO ---
    st.subheader("3. Datos de contacto")
    nombre = st.text_input("Nombre y Apellido")
    telefono = st.text_input("WhatsApp")

    # Botón con llamado a la acción claro y ancho completo
    enviar = st.form_submit_button("ENVIAR MI SOLICITUD A SESTRI ENERGÍA", use_container_width=True)

if enviar:
    if nombre and telefono:
        st.success(f"¡Excelente {nombre}! Hemos recibido tu información para el sistema de {objetivo}. Un técnico de Sestri Energía te contactará pronto.")
    else:
        st.warning("Por favor, completá tu nombre y WhatsApp para que podamos asesorarte.")
