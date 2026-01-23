import streamlit as st
import pandas as pd

# Configuración de Sestri Energía
st.set_page_config(page_title="Sestri Energía - Relevamiento", layout="centered")

# --- CARGA DE DATOS (Mapeado exacto de tu Excel) ---
# He incluido una muestra representativa de tu lista de 50+ artefactos
data_enre = {
    "Artefacto": [
        "Aire acondicionado de 2200 frigorías F/C", "Aire acondicionado de 3500 frigorías F/C", 
        "Bomba de agua de 1/2 HP", "Bomba de agua 1 HP", "Heladera con freezer", 
        "Lavarropas automático de 5 kg", "Microondas", "Televisor LED 32'' a 50''", 
        "Pava eléctrica", "Ventilador de techo", "Iluminación LED (11 W)"
    ],
    "Watts": [1013, 1613, 380, 760, 200, 175, 640, 90, 2000, 60, 11]
}
df = pd.DataFrame(data_enre)

# --- ENCABEZADO COMERCIAL ---
st.title("⚡ ¿Problemas con cortes de energía?")
st.subheader("Nosotros podemos ayudarte.")
st.write("Dejanos saber tus necesidades enviándonos la info con un simple clic. **Somos Sestri Energía.**")

st.markdown("---")

with st.form("relevamiento_sestri"):
    # 1. OBJETIVO
    st.subheader("1. ¿Qué buscás resolver?")
    objetivo = st.radio("Prioridad:", ["Back-Up (Cortes)", "Ahorro", "Ambas"], horizontal=True)
    
    st.divider()

    # 2. CONSUMOS (Selección y Columnas)
    st.subheader("2. Consumos Críticos")
    st.write("Elegí tus equipos (los Watts se cargan solos):")
    
    seleccionados = st.multiselect(
        "Buscador de artefactos:",
        options=df["Artefacto"].tolist(),
        default=["Heladera con freezer", "Iluminación LED (11 W)"]
    )
    
    total_wh_dia = 0
    
    if seleccionados:
        st.write("---")
        # ENCABEZADOS DE COLUMNA (Para que se vea como una tabla)
        c_tit1, c_tit2, c_tit3 = st.columns([2, 1, 1])
        c_tit1.caption("**Artefacto**")
        c_tit2.caption("**Potencia**")
        c_tit3.caption("**Horas/Día**")

        for art in seleccionados:
            # Obtener los watts fijos de tu Excel
            potencia_fija = int(df[df["Artefacto"] == art]["Watts"].iloc[0])
            
            # FILA ÚNICA: Artefacto | Watts | Horas
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{art}**")
            with col2:
                # Aquí mostramos el texto, ya no es un casillero de carga
                st.write(f"{potencia_fija} W")
            with col3:
                # El único dato que carga el cliente son las horas
                h = st.number_input(f"h_{art}", min_value=0, max_value=24, step=1, label_visibility="collapsed")
            
            total_wh_dia += (potencia_fija * h)

        # SUMATORIA TOTAL AUTOMÁTICA
        st.markdown("---")
        kwh_dia = total_wh_dia / 1000
        st.subheader(f"📊 Consumo Total: {kwh_dia:.2f} kWh/día")
    
    st.divider()
    
    # 3. CONTACTO
    st.subheader("3. Datos de contacto")
    nombre = st.text_input("Nombre")
    telefono = st.text_input("WhatsApp")

    enviar = st.form_submit_button("ENVIAR A SESTRI ENERGÍA", use_container_width=True)

if enviar:
    if nombre and telefono:
        st.success(f"¡Excelente {nombre}! Hemos recibido tu demanda de {total_wh_dia / 1000:.2f} kWh/día.")
    else:
        st.warning("Por favor, completá nombre y WhatsApp.")
