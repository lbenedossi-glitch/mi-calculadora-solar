import streamlit as st
import urllib.parse

# Configuración básica
st.set_page_config(page_title="Asesor Solar Modular", layout="centered")

st.title("☀️ Calculadora Solar Modular")
st.write("Selecciona tus equipos para diseñar tu sistema a medida.")

# --- DATOS DE EQUIPOS ---
equipos = [
    {"nombre": "Refrigerador", "w": 250, "h": 24},
    {"nombre": "Iluminación LED", "w": 100, "h": 5},
    {"nombre": "Televisor", "w": 120, "h": 4},
    {"nombre": "Módem Wi-Fi", "w": 20, "h": 24},
    {"nombre": "Lavarropas", "w": 500, "h": 1},
    {"nombre": "Aire Acondicionado", "w": 1500, "h": 5}
]

# --- LÓGICA DE LA APP ---
objetivo = st.radio("¿Cuál es tu prioridad?", ["Ahorrar Energía", "Tener Backup", "Ambos"])

st.subheader("Selecciona tus dispositivos:")
seleccionados = []
for e in equipos:
    if st.checkbox(f"{e['nombre']} ({e['w']}W)"):
        seleccionados.append(e)

if seleccionados:
    total_w = sum(item['w'] for item in seleccionados)
    total_kwh = sum(item['w'] * item['h'] for item in seleccionados) / 1000
    
    st.divider()
    st.markdown(f"### 📊 Resumen de Consumo")
    st.write(f"**Potencia Pico:** {total_w} W")
    st.write(f"**Consumo Diario:** {total_kwh:.2f} kWh/día")

    if "Ahorrar" in objetivo:
        st.info("💡 Puedes empezar sin baterías e instalarlas después.")
    elif "Backup" in objetivo:
        st.warning("🔋 Puedes empezar con baterías y añadir paneles después.")

    import streamlit as st
import urllib.parse

# --- AQUÍ DEBES PONER TU NÚMERO ---
# Ejemplo: "5491161549018" (Sin el +, sin espacios, con código de país)
mi_numero = "TU_NUMERO_AQUI" 

st.markdown("---")
st.subheader("📲 ¿Listo para avanzar?")

# Creamos el link de WhatsApp
texto_mensaje = "Hola, quiero recibir asesoramiento sobre mi consumo solar estimado."
texto_codificado = urllib.parse.quote(texto_mensaje)
url_final = f"https://wa.me/{mi_numero}?text={texto_codificado}"

# Este botón sí funciona en la nube
st.link_button("Contactar por WhatsApp", url_final)