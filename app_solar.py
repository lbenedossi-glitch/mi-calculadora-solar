import streamlit as st

# Mantenemos el diseño centrado para que no se desborde en el móvil
st.set_page_config(page_title="Relevamiento GST", layout="centered")

st.title("☀️ Relevamiento de Consumos Críticos")
st.write("Complete los equipos que desea mantener funcionando ante un corte o con energía solar.")

with st.form("relevamiento_tecnico"):
    st.subheader("Equipos de Respaldo")
    
    # Lista de equipos comunes para que el cliente solo complete horas o Watts
    # Usamos columnas que se apilan solas en el celular
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Dispositivo Crítico**")
        eq1 = st.checkbox("Heladera / Freezer")
        eq2 = st.checkbox("Iluminación (LED)")
        eq3 = st.checkbox("Bomba de Agua")
        eq4 = st.checkbox("Internet / Cámaras")
        otro_nombre = st.text_input("Otro equipo:")
    
    with col2:
        st.write("**Uso (Horas/Día)**")
        h1 = st.number_input("Horas Heladera", min_value=0, max_value=24, step=1, label_visibility="collapsed")
        h2 = st.number_input("Horas Luces", min_value=0, max_value=24, step=1, label_visibility="collapsed")
        h3 = st.number_input("Horas Bomba", min_value=0, max_value=24, step=1, label_visibility="collapsed")
        h4 = st.number_input("Horas Internet", min_value=0, max_value=24, step=1, label_visibility="collapsed")
        h5 = st.number_input("Horas Otro", min_value=0, max_value=24, step=1, label_visibility="collapsed")

    st.divider()
    
    # Datos de contacto para que te llegue el informe
    nombre = st.text_input("Tu Nombre")
    telefono = st.text_input("WhatsApp de contacto")

    # Botón de envío que ocupa todo el ancho del celular
    enviar = st.form_submit_button("Enviar datos para configuración", use_container_width=True)

if enviar:
    st.success(f"¡Gracias {nombre}! Recibimos tus datos. En breve configuraremos tu sistema a medida.")
    # Aquí podrías agregar el botón de WhatsApp que ya teníamos para que te mande el resumen
