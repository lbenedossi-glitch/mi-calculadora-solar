import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Sestri Energía - Relevamiento", layout="centered")

# 2. CARGA DE DATOS
@st.cache_data
def cargar_datos_excel():
    nombre_archivo = 'relevamiento_enre.xlsx'
    try:
        df_excel = pd.read_excel(nombre_archivo, engine='openpyxl')
        df_excel.columns = df_excel.columns.str.strip()
        # Aseguramos que las dos primeras columnas sean nuestras etiquetas
        df_excel.rename(columns={df_excel.columns[0]: 'Artefacto', df_excel.columns[1]: 'Potencia'}, inplace=True)
        return df_excel
    except Exception as e:
        st.error(f"Error al leer el Excel: {e}")
        return None

df = cargar_datos_excel()

# --- INTERFAZ ---
st.title("⚡ Sestri Energía")
st.subheader("Calculadora de Relevamiento Fotovoltaico")

if df is not None:
    st.markdown("---")
    objetivo = st.radio("¿Qué buscás con la energía solar?", ["Ahorro en la factura", "Respaldo ante cortes (Back-up)", "Ambas"])
    
    # Selección múltiple de equipos desde el Excel
    seleccionados = st.multiselect(
        "Seleccioná los equipos que querés alimentar:", 
        options=df["Artefacto"].unique().tolist()
    )

    total_watts = 0
    resumen_mensaje = []

    if seleccionados:
        st.write("### Cantidades y Consumos:")
        
        # Iteramos sobre lo seleccionado para pedir cantidades
        for art in seleccionados:
            # Buscamos la potencia unitaria en el DataFrame
            p_unitaria = int(df[df["Artefacto"] == art]["Potencia"].iloc[0])
            
            col1, col2 = st.columns([3, 1])
            with col1:
                cant = st.number_input(f"¿Cuántos: {art}?", min_value=1, value=1, key=f"cant_{art}")
            
            subtotal = p_unitaria * cant
            total_watts += subtotal
            resumen_mensaje.append(f"{cant}x {art}")
            
            with col2:
                st.write(f"Subtotal: \n**{subtotal} W**")

        # --- RESULTADOS ---
        total_kw = total_watts / 1000
        st.divider()
        st.metric("POTENCIA TOTAL CALCULADA", f"{total_kw:.2f} kW")

        # --- FORMULARIO DE ENVÍO ---
        with st.form("envio_sestri"):
            nombre = st.text_input("Tu Nombre")
            ciudad = st.text_input("Localidad / Provincia")
            
            enviar = st.form_submit_button("PREPARAR RELEVAMIENTO PARA WHATSAPP", use_container_width=True)
            
            if enviar:
                if nombre:
                    # REEMPLAZA ESTE NÚMERO POR TU WHATSAPP REAL (con código de país)
                    tu_telefono = "5491100000000" 
                    
                    texto_ws = (f"Hola Sestri Energía, soy {nombre} de {ciudad}. "
                                f"Hice mi relevamiento: Objetivo: {objetivo}. "
                                f"Total: {total_kw:.2f}kW. Equipos: {', '.join(resumen_mensaje)}.")
                    
                    # Formatear link de WhatsApp
                    link = f"https://wa.me/{tu_telefono}?text={texto_ws.replace(' ', '%20')}"
                    
                    st.success("¡Todo listo! Hacé clic abajo para enviármelo.")
                    st.link_button("📲 ENVIAR POR WHATSAPP AHORA", link, use_container_width=True)
                else:
                    st.warning("Por favor, poné tu nombre para que sepa quién sos.")

else:
    st.warning("Esperando conexión con el archivo Excel...")
