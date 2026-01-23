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
st.subheader("¿Problemas por cortes de luz o alto costo en la factura?. Nosotros podemos ayudarte.")
st.write("Dejanos saber tus necesidades enviándonos la info con unos simples clics.")

st.markdown("---")

# 1. SELECCIÓN DE ARTEFACTOS
seleccionados = st.multiselect(
    "Buscá y marcá tus equipos de la lista:",
    options=df["Artefacto"].tolist(),
    help="Podés seleccionar todos los que necesites."
)

st.divider()

if seleccionados:
    total_watts = 0
    st.write("**Resumen de equipos seleccionados:**")
    
    # Listado simple para el cliente
    for art in seleccionados:
        p = int(df[df["Artefacto"] == art]["Potencia"].iloc[0])
        total_watts += p
        st.write(f"✅ {art} (**{p} W**)")

    # Cálculo en kW
    total_kw = total_watts / 1000
    
    st.divider()
    st.metric("Potencia Total Estimada", f"{total_kw:.2f} kW")

    # 2. FORMULARIO DE CONTACTO Y BOTÓN WHATSAPP
    with st.form("contacto_sestri"):
        st.write("### Envianos tu consulta")
        nombre = st.text_input("Nombre y Apellido")
        
        # El botón del formulario procesa los datos
        confirmar = st.form_submit_button("PREPARAR MENSAJE DE WHATSAPP", use_container_width=True)
        
        if confirmar:
            if nombre and seleccionados:
                # --- CONFIGURACIÓN DE WHATSAPP ---
                # AQUÍ: Poné tu número (ej: 5491161234567) sin símbolos
                tu_telefono = "5491161549018" 
                
                lista_txt = ", ".join(seleccionados)
                mensaje_wa = f"Hola Sestri Energía! Mi nombre es {nombre}. Mi relevamiento dio un total de {total_kw:.2f} kW. Equipos: {lista_txt}."
                
                # Codificamos el mensaje para la URL
                url_wa = f"https://wa.me/{tu_telefono}?text={mensaje_wa.replace(' ', '%20')}"
                
                st.success(f"¡Todo listo, {nombre}!")
                # Botón final que abre WhatsApp
                st.link_button("📲 ENVIAR AHORA POR WHATSAPP", url_wa, use_container_width=True)
            else:
                st.warning("Por favor, ingresá tu nombre antes de enviar.")

else:
    st.info("Elegí tus artefactos arriba para calcular la potencia total.")



