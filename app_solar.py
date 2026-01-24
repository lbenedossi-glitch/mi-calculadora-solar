import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Sestri Energía - Relevamiento", layout="centered")

# 2. CARGA DE DATOS DESDE TU EXCEL SUBIDO
@st.cache_data
def cargar_datos_excel():
    try:
        # AQUÍ: Poné el nombre exacto de tu archivo en GitHub
        nombre_archivo = 'relevamiento_enre.xlsx' 
        df_excel = pd.read_excel(nombre_archivo)
        
        # Limpiamos nombres de columnas
        df_excel.columns = df_excel.columns.str.strip()
        return df_excel
    except Exception as e:
        st.error(f"Error al leer el Excel: {e}")
        return None

df = cargar_datos_excel()

# --- INTERFAZ ---
st.title("⚡ Sestri Energía")
st.subheader("Generar tu propia energía es la solución. Te podemos ayudar.")

if df is not None:
    st.markdown("---")
    objetivo = st.radio("¿Qué buscás resolver?", ["Back-Up (Cortes)", "Ahorro", "Ambas"])
    st.divider()

    # Selección múltiple basada en el EXCEL
    seleccionados = st.multiselect(
        "Seleccioná tus equipos (datos cargados desde tu Excel):", 
        options=df["Artefacto"].unique().tolist()
    )

    total_watts = 0
    equipos_resumen = []

    if seleccionados:
        st.write("### Ajustá las cantidades:")
        col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
        col_h1.caption("**Equipo**")
        col_h2.caption("**Cant.**")
        col_h3.caption("**Subtotal**")

        for art in seleccionados:
            # Buscamos la potencia en el Excel
            p_unitaria = int(df[df["Artefacto"] == art]["Potencia"].iloc[0])
            
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.write(art)
            with c2:
                # El "key" asegura que cada selector sea único
                cant = st.number_input(f"Cant_{art}", min_value=1, max_value=100, value=1, label_visibility="collapsed", key=f"input_{art}")
            
            subtotal = p_unitaria * cant
            total_watts += subtotal
            equipos_resumen.append(f"{cant}x {art} ({subtotal}W)")
            
            with c3:
                st.write(f"**{subtotal} W**")

        # --- CÁLCULO Y ENVÍO ---
        total_kw = total_watts / 1000
        st.divider()
        st.metric("POTENCIA TOTAL RELEVADA", f"{total_kw:.2f} kW")

        with st.form("contacto"):
            nombre = st.text_input("Nombre y Apellido")
            tel = st.text_input("WhatsApp de contacto")
            
            if st.form_submit_button("PREPARAR ENVÍO A SESTRI ENERGÍA", use_container_width=True):
                if nombre and tel:
                    # RECUERDA: Poné tu número real aquí
                    tu_num = "5491161549018" 
                    msg = f"Sestri Energía: Relevamiento de {nombre} ({tel}). Objetivo: {objetivo}. Total: {total_kw:.2f}kW. Detalle: {', '.join(equipos_resumen)}."
                    url = f"https://wa.me/{tu_num}?text={msg.replace(' ', '%20')}"
                    st.link_button("📲 ENVIAR POR WHATSAPP", url, use_container_width=True)
                else:
                    st.warning("Por favor, completá tus datos.")
else:
    st.info("Asegurate de que el archivo Excel esté en el repositorio de GitHub y que el nombre en el código coincida.")
