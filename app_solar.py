import streamlit as st
import pandas as pd

# Configuración de página
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

# --- INTERFAZ ---
st.title("⚡ Sestri Energía")
st.subheader("Relevamiento de Equipamiento Eléctrico")
st.write("¿Problemas con los cortes de energía?, ¿El costo de la energía es muy alto?"
        "La energía autogenerada es la solución". Con tan solo unos pocos clics te 
         podemos ayudar")

st.markdown("---")

# 1. SELECCIÓN DE ARTEFACTOS
# El usuario solo elige de la lista, no carga horas ni watts.
seleccionados = st.multiselect(
    "Buscá y marcá tus equipos:",
    options=df["Artefacto"].tolist(),
    help="Podés seleccionar varios de la lista."
)

st.divider()

if seleccionados:
    total_watts = 0
    
    # Mostramos un resumen de lo seleccionado con sus watts fijos
    st.write("**Resumen de Potencia Instalada:**")
    
    for art in seleccionados:
        # Buscamos la potencia automáticamente
        p = int(df[df["Artefacto"] == art]["Potencia"].iloc[0])
        total_watts += p
        # Formato simple: Nombre - Watts
        st.write(f"✅ {art}: **{p} W**")

    st.divider()
    
    # CÁLCULO FINAL EN kW
    total_kw = total_watts / 1000
    
    col1, col2 = st.columns(2)
    col1.metric("Potencia Total (W)", f"{total_watts} W")
    col2.metric("Potencia Total (kW)", f"{total_kw:.2f} kW")
    
    st.info("Esta es la potencia máxima que el sistema debería soportar si todos los equipos encendieran a la vez.")

    # 2. FORMULARIO DE CONTACTO
    with st.form("contacto_sestri"):
        st.write("### Envianos tu consulta")
        nombre = st.text_input("Nombre y Apellido")
        whatsapp = st.text_input("WhatsApp")
        
        if st.form_submit_button("ENVIAR A SESTRI ENERGÍA", use_container_width=True):
            if nombre and whatsapp:
                st.success(f"¡Gracias {nombre}! Recibimos tu listado con un total de {total_kw:.2f} kW.")
            else:
                st.warning("Por favor, completá tus datos de contacto.")

else:
    st.info("Elegí tus artefactos arriba para ver el total de potencia.")

