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

# --- BLOQUE COMERCIAL DE INICIO ---
st.title("⚡ SESTRI ENERGIA")
st.subheader("Si los cortes de luz o el costo de la factura son un problema. Nosotros podemos ayudarte.")
st.write("Dejanos saber tus necesidades enviándonos la info con un simple clic. **Somos Sestri Energía.**")

st.markdown("---")

# 1. SELECCIÓN DE ARTEFACTOS
seleccionados = st.multiselect(
    "Buscá y marcá tus equipos de la lista:",
    options=df["Artefacto"].tolist()
)

if seleccionados:
    total_watts = 0
    st.write("**Equipos seleccionados:**")
    
    for art in seleccionados:
        p = int(df[df["Artefacto"] == art]["Potencia"].iloc[0])
        total_watts += p
        st.write(f"✅ {art} ({p} W)")

    total_kw = total_watts / 1000
    st.divider()
    st.metric("Potencia Total Estimada", f"{total_kw:.2f} kW")

    # 2. FORMULARIO DE CONTACTO E IDENTIFICACIÓN
    with st.form("contacto_sestri"):
        st.write("### Datos de contacto")
        nombre = st.text_input("Nombre y Apellido")
        tel_cliente = st.text_input("WhatsApp de contacto (con código de área)")
        
        confirmar = st.form_submit_button("PREPARAR ENVÍO", use_container_width=True)
        
        if confirmar:
            if nombre and tel_cliente and seleccionados:
                # --- CONFIGURACIÓN DE TU WHATSAPP ---
                # PONÉ TU NÚMERO AQUÍ (Ej: 54911XXXXXXXX)
                tu_telefono = "5491100000000" 
                
                lista_txt = ", ".join(seleccionados)
                # El mensaje ahora incluye el teléfono para que te quede registrado en el texto
                mensaje_wa = (
                    f"Hola Sestri Energía! Mi nombre es {nombre}. "
                    f"Mi WhatsApp de contacto es {tel_cliente}. "
                    f"Mi relevamiento dio un total de {total_kw:.2f} kW. "
                    f"Equipos: {lista_txt}."
                )
                
                url_wa = f"https://wa.me/{tu_telefono}?text={mensaje_wa.replace(' ', '%20')}"
                
                st.success(f"¡Gracias {nombre}! Para enviarnos la información, hacé clic en el botón de abajo.")
                st.link_button("📲 ENVIAR RELEVAMIENTO A WHATSAPP", url_wa, use_container_width=True)
            else:
                st.warning("Por favor, completá tu nombre y teléfono para poder identificarte.")

else:
    st.info("Elegí tus artefactos arriba para calcular la potencia total.")
