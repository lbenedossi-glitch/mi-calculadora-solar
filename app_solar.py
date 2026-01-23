import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sestri Energía - Relevamiento", layout="centered")

# --- DATOS DEL ENRE ---
data_enre = {
    "Artefacto": [
        "Aire acondicionado 2200 frig", "Aire acondicionado 3500 frig", 
        "Bomba de agua 1/2 HP", "Bomba de agua 1 HP", "Heladera con freezer", 
        "Lavarropas automático", "Microondas", "Televisor LED 32-50''", 
        "Pava eléctrica", "Ventilador de techo", "Iluminación LED (Kit 10u)"
    ],
    "Potencia": [1013, 1613, 380, 760, 200, 175, 640, 90, 2000, 60, 110]
}
df = pd.DataFrame(data_enre)

# --- INICIO ---
st.title("⚡ Sestri Energía")
st.subheader("Calculadora de Consumos Críticos")
st.write("Seleccioná tus equipos y definí las horas de uso.")

st.markdown("---")

with st.form("relevamiento_sestri"):
    # 1. OBJETIVO
    objetivo = st.radio("Prioridad:", ["Back-Up", "Ahorro", "Ambas"], horizontal=True)
    
    st.divider()

    # 2. SELECCIÓN DE ARTEFACTOS
    seleccionados = st.multiselect(
        "Buscá y agregá tus artefactos:",
        options=df["Artefacto"].tolist()
    )
    
    total_wh_dia = 0
    
    if seleccionados:
        st.write("---")
        # Encabezados
        col_t1, col_t2, col_t3 = st.columns([2, 1, 1])
        col_t1.caption("**Artefacto**")
        col_t2.caption("**Watts**")
        col_t3.caption("**Horas/Día**")

        for art in seleccionados:
            # Traemos la potencia fija del "Excel" (DataFrame)
            potencia_fija = int(df[df["Artefacto"] == art]["Potencia"].iloc[0])
            
            # FILA ÚNICA
            c1, c2, c3 = st.columns([2, 1, 1])
            
            with c1:
                st.write(f"{art}")
            with c2:
                # AQUÍ ESTÁ LA CLAVE: st.write NO requiere carga manual
                st.write(f"**{potencia_fija} W**")
            with c3:
                # El único cuadro de carga es este
                h = st.number_input(f"h_{art}", min_value=0, max_value=24, step=1, label_visibility="collapsed")
            
            # Calculamos energía
            total_wh_dia += (potencia_fija * h)

        st.markdown("---")
        # SUMATORIA TOTAL
        kwh_dia = total_wh_dia / 1000
        st.metric("Total Acumulado", f"{kwh_dia:.2f} kWh/día")
    
    st.divider()
    
    # 3. CONTACTO
    nombre = st.text_input("Nombre")
    telefono = st.text_input("WhatsApp")

    enviar = st.form_submit_button("ENVIAR A SESTRI ENERGÍA", use_container_width=True)

if enviar:
    if nombre and telefono:
        st.success(f"¡Gracias {nombre}! Recibimos tu demanda de {total_wh_dia / 1000:.2f} kWh/día.")
    else:
        st.warning("Completá tus datos de contacto.")
