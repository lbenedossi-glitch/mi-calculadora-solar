import streamlit as st
import pandas as pd

# Configuración de Sestri Energía
st.set_page_config(page_title="Sestri Energía - Relevamiento", layout="centered")

# --- BASE DE DATOS (Watts fijos del ENRE) ---
data_enre = {
    "Artefacto": [
        "Aire acondicionado 2200 frigorías", "Aire acondicionado 3500 frigorías", 
        "Bomba de agua 1/2 HP", "Bomba de agua 1 HP", "Freezer", "Heladera con freezer", 
        "Lavarropas automático", "Microondas", "Pava eléctrica", "Termotanque eléctrico",
        "Televisor LED 32-50''", "Ventilador de techo", "Iluminación LED (Kit 10u)"
    ],
    "Potencia": [1013, 1613, 380, 760, 150, 200, 175, 640, 2000, 1500, 90, 60, 110]
}
df = pd.DataFrame(data_enre)

# --- TU NUEVO ENCABEZADO PERSONALIZADO ---
st.title("⚡ Sestri Energía")
st.subheader("¿Problemas con los cortes o el costo? Generar tu propia energía es la solución. Te podemos ayudar.")
st.write("Dejanos conocer tus necesidades con unos simples clics.")

st.markdown("---")

# 1. OPCIÓN DE OBJETIVO
objetivo = st.radio(
    "¿Qué buscás resolver principalmente?",
    ["Back-Up (Respaldo ante cortes)", "Ahorrar energía (Autoconsumo)", "Ambas opciones"],
    horizontal=False
)

st.divider()

# 2. SELECCIÓN DE ARTEFACTOS
seleccionados = st.multiselect(
    "Seleccioná los equipos que querés incluir en tu sistema:",
    options=df["Artefacto"].tolist()
)

if seleccionados:
    total_watts = 0
    st.write("**Resumen de equipos:**")
    
    for art in seleccionados:
        p = int(df[df["Artefacto"] == art]["Potencia"].iloc[0])
        total_watts += p
        st.write(f"✅ {art} ({p} W)")

    total_kw = total_watts / 1000
    st.divider()
    st.metric("Potencia Total Instalada", f"{total_kw:.2f} kW")

    # 3. FORMULARIO DE CONTACTO E IDENTIFICACIÓN
    with st.form("contacto_sestri"):
        st.write("### Datos para tu presupuesto")
        nombre = st.text_input("Nombre y Apellido")
        tel_cliente = st.text_input("Tu WhatsApp (con código de área)")
        
        confirmar = st.form_submit_button("PREPARAR ENVÍO", use_container_width=True)
        
        if confirmar:
            if nombre and tel_cliente:
                # --- TU NÚMERO DE WHATSAPP ---
                tu_telefono = "5491161549018" # <--- CAMBIAR POR EL TUYO
                
                lista_txt = ", ".join(seleccionados)
