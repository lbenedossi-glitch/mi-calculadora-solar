import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sestri Energía - Relevamiento", layout="centered")

# --- BASE DE DATOS DE TU EXCEL (ENRE) ---
data_enre = {
    "Artefacto": [
        "Aire acondicionado 2200 frigorías", "Aire acondicionado 3500 frigorías", 
        "Bomba de agua 1/2 HP", "Bomba de agua 1 HP", "Freezer", "Heladera con freezer", 
        "Lavarropas automático", "Microondas", "Televisor LED 32-50''", "Pava eléctrica",
        "Termotanque eléctrico", "Ventilador de techo", "Iluminación LED (Kit 10u)"
    ],
    "Potencia": [1013, 1613, 380, 760, 150, 200, 175, 640, 90, 2000, 1500, 60, 110]
}
df = pd.DataFrame(data_enre)

# --- INICIO DE APP ---
st.title("⚡ ¿Problemas con cortes de energía?")
st.subheader("Nosotros podemos ayudarte.")
st.write("Dejanos saber tus necesidades enviándonos la info con un simple clic. **Somos Sestri Energía.**")

st.markdown("---")

with st.form("relevamiento_sestri"):
    st.subheader("1. Prioridad")
    objetivo = st.radio("¿Qué buscás resolver?", ["Back-Up (Cortes)", "Ahorro", "Ambas"], horizontal=True)
    
    st.divider()

    st.subheader("2. Consumos Críticos")
    seleccionados = st.multiselect(
        "Buscá y seleccioná tus artefactos:",
        options=df["Artefacto"].tolist(),
        default=["Heladera con freezer"]
    )
    
    total_wh_dia = 0
    
    if seleccionados:
        st.write("---")
        # Encabezados de columna
        c_tit1, c_tit2, c_tit3 = st.columns([2, 1, 1])
        c_tit1.caption("**Artefacto**")
        c_tit2.caption("**Watts**")
        c_tit3.caption("**Horas/Día**")

        for art in seleccionados:
            # Obtener potencia fija del Excel
            potencia_fija = int(df[df["Artefacto"] == art]["Potencia"].iloc[0])
            
            # FILA ÚNICA POR ARTEFACTO
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{art}**")
            with col2:
                # Se muestra el valor fijo, no es editable para evitar errores del cliente
                st.write(f"{potencia_fija} W")
            with col3:
                # El cliente solo toca las horas
                h = st.number_input(f"Horas {art}", min_value=0, max_value=24, step=1, label_visibility="collapsed")
            
            # Suma acumulada automática
            total_wh_dia += (potencia_fija * h)

        st.markdown("---")
        # SUMA TOTAL VISIBLE ANTES DE ENVIAR
        kwh_dia = total_wh_dia / 1000
        st.subheader(f"📊 Consumo Total: {kwh_dia:.2f} kWh/día")
    
    st.divider()
    
    st.subheader("3. Contacto")
    nombre = st.text_input("Nombre")
    telefono = st.text_input("WhatsApp")

    enviar = st.form_submit_button("ENVIAR MI SOLICITUD A SESTRI ENERGÍA", use_container_width=True)

if enviar:
    if nombre and telefono:
        st.success(f"¡Gracias {nombre}! Recibimos tu relevamiento por {total_wh_dia / 1000:.2f} kWh/día.")
    else:
        st.warning("Por favor, completá nombre y WhatsApp.")
