import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sestri Energía - Relevamiento Completo", layout="centered")

# --- BASE DE DATOS COMPLETA SEGÚN TU EXCEL ---
# He cargado la mayor cantidad de datos de tu tabla para que no falte nada
data_enre = {
    "Artefacto": [
        "Afeitadora eléctrica", "Aire acondicionado 2200 frig. F/C", "Aire acondicionado 3500 frig. F/C", 
        "Aire acondicionado 4500 frig. F/C", "Anafes (2 hornallas)", "Aspiradora", "Batidora de mano", 
        "Bomba de agua 1/2 HP", "Bomba de agua 1 HP", "Bomba de pileta", "Cafetera eléctrica", 
        "Calefactor eléctrico", "Computadora (CPU + Monitor)", "Depiladora", "Enceradora", 
        "Extractor de aire", "Freezer", "Heladera con freezer", "Heladera sin freezer", 
        "Horno eléctrico", "Iluminación (Kit 10 lámparas LED)", "Lavarropas automático (frío)", 
        "Lavarropas automático (caliente)", "Lavavajillas", "Microondas", "Pancha", 
        "Pava eléctrica", "Notebook/Laptop", "Radio", "Reproductor de DVD", "Secador de pelo", 
        "Secarropas centrífugo", "Secarropas por calor", "Soldador eléctrico", "Televisor LED 32-50''", 
        "Termotanque eléctrico", "Tostadora", "Ventilador de pared", "Ventilador de pie", 
        "Ventilador de techo"
    ],
    "Potencia": [
        15, 1013, 1613, 2150, 2000, 750, 200, 380, 760, 600, 900, 1500, 200, 15, 600, 
        25, 150, 200, 150, 2500, 110, 175, 2000, 1500, 640, 1000, 2000, 50, 30, 30, 
        500, 400, 2500, 60, 90, 1500, 800, 80, 80, 60
    ]
}
df = pd.DataFrame(data_enre)

# --- ENCABEZADO ---
st.title("⚡ Sestri Energía")
st.subheader("¿Problemas con los cortes o el costo? Generar tu propia energía es la solución.")
st.write("Seleccioná tus equipos. Si no encontrás alguno, podés agregarlo manualmente al final.")

st.markdown("---")

# 1. OBJETIVO
objetivo = st.radio("¿Cuál es tu prioridad?", ["Back-Up (Cortes)", "Ahorro", "Ambas"])

st.divider()

# 2. SELECCIÓN DE ARTEFACTOS (Lista ENRE completa)
seleccionados = st.multiselect(
    "Buscá y marcá tus equipos (podés escribir para filtrar):",
    options=df["Artefacto"].tolist()
)

total_watts = 0
equipos_finales = []

if seleccionados:
    st.write("**Resumen de potencia seleccionada:**")
    for art in seleccionados:
        p = int(df[df["Artefacto"] == art]["Potencia"].iloc[0])
        total_watts += p
        equipos_finales.append(f"{art} ({p}W)")
        st.write(f"✅ {art} — **{p} W**")

# 3. AGREGAR PERSONALIZADOS
st.write("---")
with st.expander("➕ ¿No encontraste un equipo? Agregalo acá"):
    c1, c2 = st.columns([2, 1])
    extra_nom = c1.text_input("Nombre del equipo")
    extra_wat = c2.number_input("Watts", min_value=0, step=50)
    if extra_nom and extra_wat > 0:
        total_watts += extra_wat
        equipos_finales.append(f"{extra_nom} ({extra_wat}W)")
        st.info(f"Agregado: {extra_nom}")

# CÁLCULO Y ENVÍO
if total_watts > 0:
    total_kw = total_watts / 1000
    st.metric("POTENCIA TOTAL RELEVADA", f"{total_kw:.2f} kW")

    with st.form("contacto_sestri"):
        st.write("### Envianos tu relevamiento")
        nombre = st.text_input("Nombre y Apellido")
        tel_cliente = st.text_input("WhatsApp de contacto")
        
        if st.form_submit_button("PREPARAR MENSAJE PARA WHATSAPP", use_container_width=True):
            if nombre and tel_cliente:
                tu_num = "5491161549018" # <-- CAMBIAR POR EL TUYO
                msg = (f"Hola Sestri Energía! Soy {nombre} ({tel_cliente}). "
                       f"Busco: {objetivo}. Potencia: {total_kw:.2f}kW. "
                       f"Equipos: {', '.join(equipos_finales)}.")
                url = f"https://wa.me/{tu_num}?text={msg.replace(' ', '%20')}"
                st.success("¡Datos listos!")
                st.link_button("📲 ENVIAR POR WHATSAPP", url, use_container_width=True)
