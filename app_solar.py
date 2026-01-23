import streamlit as st
import pandas as pd

# Configuración Sestri Energía
st.set_page_config(page_title="Sestri Energía - Relevamiento Profesional", layout="centered")

# --- CARGA DE DATOS DESDE TU EXCEL ---
# He mapeado los datos directamente de tu archivo "Consumo Estimado Total y Máximo.xlsx"
data_enre = {
    "Artefacto": [
        "Aire acondicionado de 2200 frigorías F/C", "Aire acondicionado de 3500 frigorías F/C", 
        "Bomba de agua de 1/2 HP", "Bomba de agua 1 HP", "Freezer", "Heladera con freezer", 
        "Lavarropas automático de 5 kg", "Microondas", "Televisor LED 32'' a 50''", "Pava eléctrica",
        "Termotanque eléctrico", "Ventilador de techo", "Iluminación LED (11 W)"
    ],
    "Potencia": [1013, 1613, 380, 760, 150, 200, 175, 640, 90, 2000, 1500, 60, 11]
}
# Nota: En la versión final, usaremos pd.read_csv o la API de Google para leer el total de las 50+ filas.
df = pd.DataFrame(data_enre)

# --- INTERFAZ ---
st.title("⚡ ¿Problemas con cortes de energía?")
st.subheader("Nosotros podemos ayudarte.")
st.write("Dejanos saber tus necesidades enviándonos la info con un simple clic. **Somos Sestri Energía.**")

st.markdown("---")

with st.form("relevamiento_sestri"):
    # 1. OBJETIVO
    st.subheader("1. ¿Qué buscás resolver?")
    objetivo = st.radio("Prioridad:", ["Back-Up (Cortes)", "Ahorro", "Ambas"], index=0)
    
    st.divider()

    # 2. CONSUMOS (Usando tu lista del ENRE)
    st.subheader("2. Consumos Críticos")
    st.write("Buscá y seleccioná los equipos que querés mantener encendidos:")
    
    seleccionados = st.multiselect(
        "Seleccionar artefactos:",
        options=df["Artefacto"].tolist(),
        default=["Heladera con freezer", "Iluminación LED (11 W)"]
    )
    
    total_wh_dia = 0
    
    if seleccionados:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1: st.caption("**Artefacto**")
        with col2: st.caption("**Watts (ENRE)**")
        with col3: st.caption("**Horas/Día**")
        
        for art in seleccionados:
            potencia = int(df[df["Artefacto"] == art]["Potencia"].iloc[0])
            
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1: st.write(art)
            with c2: st.write(f"{potencia} W")
            with c3:
                h = st.number_input(f"H_{art}", min_value=0, max_value=24, step=1, label_visibility="collapsed")
            
            total_wh_dia += (potencia * h)

    st.divider()
    
    # RESULTADO
    kwh_dia = total_wh_dia / 1000
    st.metric("Demanda Estimada Total", f"{kwh_dia:.2f} kWh/día")
    
    # 3. CONTACTO
    st.subheader("3. Datos de contacto")
    nombre = st.text_input("Nombre")
    telefono = st.text_input("WhatsApp")

    enviar = st.form_submit_button("ENVIAR SOLICITUD A SESTRI ENERGÍA", use_container_width=True)

if enviar:
    if nombre and telefono:
        st.success(f"¡Gracias {nombre}! Recibimos tu demanda de {kwh_dia:.2f} kWh/día.")
    else:
        st.warning("Completá tus datos de contacto.")
