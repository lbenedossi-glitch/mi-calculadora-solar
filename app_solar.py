import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuración de página
st.set_page_config(page_title="Sestri Energía - Estimador Solar", page_icon="💡")

# Estilo para fondo y colores
st.markdown("""
    <style>
    .stApp {
        background-color: #fdfcf0;
    }
    .st-emotion-cache-1kyx0t0 {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Encabezado de la Empresa
st.write("### SESTRI ENERGÍA")
st.title("☀️ Estimador Solar Inteligente")

st.info("""
**¿Problemas con el suministro eléctrico?** Los sistemas de generación fotovoltaicos reducen tu dependencia del mismo para mantener un grado de confort.
""")

st.markdown("---")

# 3. Objetivos
st.subheader("1. ¿Cuál es su objetivo principal?")
objetivo = st.radio(
    "Seleccione una opción:",
    ["Ahorro de energía (Reducir factura)", "Backup (Protección ante cortes)", "Ambos (Ahorro + Respaldo)"],
    index=0
)

# 4. Sección de la Tabla
st.markdown("---")
st.subheader("2. Detalle de sus consumos")
st.write("Ajuste los valores o agregue aparatos nuevos al final:")

datos_base = {
    "Aparato": ["Heladera", "Lavarropas", "Aire Acondicionado", "Televisor", "Iluminación LED", "Pava eléctrica"],
    "Watts": [150, 500, 1350, 100, 150, 2000],
    "Cantidad": [1, 0, 0, 1, 10, 0],
    "Horas_Uso": [24, 1, 5, 4, 5, 0.2]
}

df_usuario = pd.DataFrame(datos_base)
tabla_editable = st.data_editor(
    df_usuario, 
    num_rows="dynamic", 
    use_container_width=True
)

# 5. Cálculos
tabla_editable["Total_Dia_Wh"] = tabla_editable["Watts"] * tabla_editable["Cantidad"] * tabla_editable["Horas_Uso"]
total_kwh_dia = tabla_editable["Total_Dia_Wh"].sum() / 1000

st.success(f"### Consumo Estimado: {total_kwh_dia:.2f} kWh/día")

# 6. Botón de WhatsApp personalizado
st.markdown("---")
st.write("#### 💡 ¿Tienes dudas?")

# --- REEMPLAZA CON TU NÚMERO ---
mi_telefono = "5491161549018" 

resumen_aparatos = ""
for index, row in tabla_editable.iterrows():
    if row["Cantidad"] > 0:
        resumen_aparatos += f"- {row['Aparato']}: {row['Cantidad']} unidad(es)\n"

mensaje_wa = (
    f"Hola Sestri Energía! He usado su estimador solar.\n\n"
    f"🎯 Objetivo: {objetivo}\n"
    f"📊 Consumo: {total_kwh_dia:.2f} kWh/día\n\n"
    f"📋 Detalle:\n{resumen_aparatos}"
)

mensaje_codificado = urllib.parse.quote(mensaje_wa)
url_whatsapp = f"https://wa.me/{mi_telefono}?text={mensaje_codificado}"

st.link_button("💡 Consultanos sin compromiso por WhatsApp", url_whatsapp, type="primary", use_container_width=True)