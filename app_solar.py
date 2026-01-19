import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuración obligatoria (esto hace que se vea bien en celulares)
st.set_page_config(page_title="Calculadora Solar", page_icon="☀️")

# 2. Título y Objetivos
st.title("☀️ Estimador Solar")

st.subheader("1. ¿Cuál es su objetivo principal?")
objetivo = st.radio(
    "Seleccione una opción:",
    ["Ahorro de energía (Reducir factura)", "Backup (Protección ante cortes)", "Ambos (Ahorro + Respaldo)"],
    index=0
)

# 3. Sección de la Tabla
st.markdown("---")
st.subheader("2. Detalle de sus consumos")
st.write("Puede modificar los valores o agregar aparatos nuevos al final de la lista:")

datos_base = {
    "Aparato": ["Heladera", "Lavarropas", "Aire Acondicionado", "Televisor", "Iluminación LED", "Pava eléctrica"],
    "Watts": [150, 500, 1350, 100, 150, 2000],
    "Cantidad": [1, 0, 0, 1, 10, 0],
    "Horas_Uso": [24, 1, 5, 4, 5, 0.2]
}

df_usuario = pd.DataFrame(datos_base)
# Aquí está la tabla que mencionas
tabla_editable = st.data_editor(
    df_usuario, 
    num_rows="dynamic", 
    use_container_width=True
)

# 4. Cálculos automáticos
tabla_editable["Total_Dia_Wh"] = tabla_editable["Watts"] * tabla_editable["Cantidad"] * tabla_editable["Horas_Uso"]
total_kwh_dia = tabla_editable["Total_Dia_Wh"].sum() / 1000

st.info(f"Consumo Total: **{total_kwh_dia:.2f} kWh/día** | Objetivo: **{objetivo}**")

# 5. Botón de WhatsApp
st.markdown("---")
# --- REEMPLAZA LAS X CON TU NÚMERO ---
mi_telefono = "54911XXXXXXXX" 

resumen_aparatos = ""
for index, row in tabla_editable.iterrows():
    if row["Cantidad"] > 0:
        resumen_aparatos += f"- {row['Aparato']}: {row['Cantidad']} unidad(es)\n"

mensaje_wa = (
    f"Hola! He usado tu calculadora solar.\n\n"
    f"🎯 Objetivo: {objetivo}\n"
    f"📊 Consumo: {total_kwh_dia:.2f} kWh/día\n\n"
    f"📋 Detalle:\n{resumen_aparatos}"
)

mensaje_codificado = urllib.parse.quote(mensaje_wa)
url_whatsapp = f"https://wa.me/{mi_telefono}?text={mensaje_codificado}"

st.link_button("🚀 Enviar consulta por WhatsApp", url_whatsapp)