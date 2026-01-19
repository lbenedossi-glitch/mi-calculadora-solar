import streamlit as st
import pandas as pd
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Calculadora Solar Pro", page_icon="☀️")

st.title("☀️ Estimador de Consumo Solar")
st.write("Modifica la tabla con tus artefactos. Puedes cambiar los Watts, las horas o agregar nuevos aparatos al final.")

# 1. Definimos la lista base
datos_base = {
    "Aparato": ["Heladera", "Lavarropas", "Aire Acondicionado", "Televisor", "Microondas", "Pava eléctrica", "Iluminación LED"],
    "Watts": [150, 500, 1350, 100, 1200, 2000, 150],
    "Cantidad": [1, 0, 0, 1, 0, 0, 10],
    "Horas_Uso": [24, 1, 5, 4, 0.2, 0.2, 5]
}

# 2. Tabla Interactiva
df_usuario = pd.DataFrame(datos_base)
tabla_editable = st.data_editor(
    df_usuario, 
    num_rows="dynamic", 
    use_container_width=True
)

# 3. Cálculos
tabla_editable["Total_Dia_Wh"] = tabla_editable["Watts"] * tabla_editable["Cantidad"] * tabla_editable["Horas_Uso"]
total_kwh_dia = tabla_editable["Total_Dia_Wh"].sum() / 1000

st.metric("Consumo Total Estimado", f"{total_kwh_dia:.2f} kWh/día")

# 4. Lógica de WhatsApp personalizada
st.markdown("---")
st.subheader("📩 ¿Quieres un presupuesto detallado?")

# --- PON TU NÚMERO AQUÍ ---
mi_telefono = "5491161549018" # Reemplaza con tu número real

# Creamos un resumen de texto de la tabla para el mensaje
resumen_aparatos = ""
for index, row in tabla_editable.iterrows():
    if row["Cantidad"] > 0:
        resumen_aparatos += f"- {row['Aparato']}: {row['Cantidad']} unidad(es)\n"

mensaje_wa = (
    f"Hola! He usado tu calculadora solar.\n\n"
    f"📍 *Resumen de consumo:* {total_kwh_dia:.2f} kWh/día\n"
    f"📍 *Detalle de equipos:*\n{resumen_aparatos}\n"
    f"¿Podrías enviarme un presupuesto para cubrir este consumo?"
)

mensaje_codificado = urllib.parse.quote(mensaje_wa)
url_whatsapp = f"https://wa.me/{mi_telefono}?text={mensaje_codificado}"

st.link_button("🚀 Enviar detalle por WhatsApp", url_whatsapp)