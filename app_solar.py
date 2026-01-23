import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Sestri Energía - Relevamiento", layout="centered")

# --- BASE DE DATOS INTERNA (Misma de tu Excel) ---
# Separamos Artefacto de Potencia para que la matemática funcione
data_enre = {
    "Artefacto": [
        "Aire acondicionado 2200 frigorías", "Aire acondicionado 3500 frigorías", 
        "Bomba de agua 1/2 HP", "Bomba de agua 1 HP", "Heladera con freezer", 
        "Lavarropas automático", "Microondas", "Televisor LED 32-50''", 
        "Pava eléctrica", "Ventilador de techo", "Iluminación LED (Kit 10u)"
    ],
    "Potencia": [1013, 1613, 380, 760, 200, 175, 640, 90, 2000, 60, 110]
}
df = pd.DataFrame(data_enre)

# --- ENCABEZADO ---
st.title("⚡ Sestri Energía")
st.subheader("Calculadora de Relevamiento Fotovoltaico")
st.write("Seleccioná los equipos para calcular tu demanda diaria en kWh.")

st.markdown("---")

with st.form("formulario_sestri"):
    # 1. OBJETIVO
    objetivo = st.radio("Prioridad del sistema:", ["Back-Up", "Ahorro", "Ambas"], horizontal=True)
    
    st.divider()

    # 2. SELECCIÓN DINÁMICA
    st.write("**Buscá y agregá tus artefactos de la lista:**")
    seleccionados = st.multiselect(
        "Hacé clic aquí para buscar:",
        options=df["Artefacto"].tolist(),
        help="Podés escribir el nombre del aparato para encontrarlo rápido."
    )
    
    total_energia_dia = 0
    
    if seleccionados:
        st.write("---")
        # Encabezados de tabla
        col_t1, col_t2, col_t3 = st.columns([2, 1, 1])
        col_t1.caption("**Artefacto**")
        col_t2.caption("**Watts (ENRE)**")
        col_t3.caption("**Horas de uso**")

        for art in seleccionados:
            # Extraemos el valor numérico de la potencia de forma limpia
            valor_watts = int(df[df["Artefacto"] == art]["Potencia"].iloc[0])
            
            # Mostramos la fila alineada
            c1, c2, c3 = st.columns([2, 1, 1])
            
            with c1:
                st.write(art)
            with c2:
                # Se muestra como texto, NO como input. El cliente no lo carga.
                st.write(f"{valor_watts} W")
            with c3:
                # Único dato que el cliente ingresa manualmente
                h = st.number_input(f"Horas para {art}", min_value=0, max_value=24, step=1, label_visibility="collapsed")
            
            # MATEMÁTICA: Aquí se hace el cálculo real
            total_energia_dia += (valor_watts * h)

        st.markdown("---")
        # RESULTADO FINAL VISIBLE
        kwh_final = total_energia_dia / 1000
        st.metric("DEMANDA TOTAL ESTIMADA", f"{kwh_final:.2f} kWh/día")
        st.caption("Este valor es fundamental para dimensionar tus paneles y baterías.")
    
    st.divider()
    
    # 3. CONTACTO
    nombre = st.text_input("Tu Nombre")
    whatsapp = st.text_input("Tu WhatsApp")

    enviar = st.form_submit_button("ENVIAR RELEVAMIENTO A SESTRI ENERGÍA", use_container_width=True)

if enviar:
    if nombre and whatsapp:
        st.success(f"¡Excelente {nombre}! Hemos recibido tu relevamiento por {total_energia_dia / 1000:.2f} kWh/día.")
    else:
        st.warning("Por favor, completá tu nombre y contacto para que podamos asesorarte.")
