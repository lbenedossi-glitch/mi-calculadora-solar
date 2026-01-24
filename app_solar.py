import streamlit as st
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Sestri Energía - Relevamiento", layout="wide")

# 2. CARGA DE DATOS
@st.cache_data
def cargar_datos_excel():
    nombre_archivo = 'relevamiento_enre.xlsx'
    try:
        df_excel = pd.read_excel(nombre_archivo, engine='openpyxl')
        df_excel.columns = df_excel.columns.str.strip()
        df_excel.rename(columns={df_excel.columns[0]: 'Artefacto', df_excel.columns[1]: 'Potencia'}, inplace=True)
        return df_excel
    except Exception as e:
        st.error(f"Error al leer el Excel: {e}")
        return None

df = cargar_datos_excel()

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stNumberInput {width: 80px !important;}
    .main {background-color: #f5f7f9;}
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Sestri Energía")
st.subheader("Calculadora de Relevamiento Fotovoltaico")

if df is not None:
    st.info("Paso 1: Definí tu objetivo y elegí tus equipos")
    
    col_a, col_b = st.columns(2)
    with col_a:
        objetivo = st.selectbox("¿Qué buscás resolver?", ["Ahorro", "Back-up (Cortes)", "Ambas"])
    with col_b:
        seleccionados = st.multiselect(
            "Elegí tus equipos de la lista:", 
            options=df["Artefacto"].unique().tolist()
        )

    total_watts = 0
    resumen_mensaje = []

    if seleccionados:
        st.markdown("---")
        st.markdown("#### Paso 2: Ajustá cantidades")
        
        # Encabezados de tabla simples
        h1, h2, h3 = st.columns([3, 1, 1])
        h1.caption("**Artefacto**")
        h2.caption("**Cant.**")
        h3.caption("**Subtotal**")

        for art in seleccionados:
            p_unitaria = int(df[df["Artefacto"] == art]["Potencia"].iloc[0])
            
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                st.write(f"🔹 {art}")
            with c2:
                # Usamos label_visibility="collapsed" para que no ocupe espacio el texto "¿Cuántos?"
                cant = st.number_input("", min_value=1, value=1, key=f"c_{art}", label_visibility="collapsed")
            
            subtotal = p_unitaria * cant
            total_watts += subtotal
            resumen_mensaje.append(f"{cant}x {art}")
            
            with c3:
                st.write(f"**{subtotal} W**")

        # --- RESULTADOS ---
        total_kw = total_watts / 1000
        st.divider()
        
        # Usamos una métrica grande para el total
        st.metric("POTENCIA TOTAL RELEVADA", f"{total_kw:.2f} kW")

        # --- PASO FINAL ---
        st.markdown("#### Paso 3: Envíanos tu consulta")
        with st.form("envio_sestri"):
            c_nom, c_loc = st.columns(2)
            nombre = c_nom.text_input("Nombre y Apellido")
            ciudad = c_loc.text_input("Localidad")
            
            enviar = st.form_submit_button("PREPARAR WHATSAPP PARA SESTRI ENERGÍA", use_container_width=True)
            
            if enviar:
                if nombre:
                    tu_telefono = "5491136453664" # Tu número de Sestri Energía
                    texto_ws = (f"Sestri Energía: Relevamiento de {nombre} ({ciudad}). "
                                f"Objetivo: {objetivo}. Total: {total_kw:.2f}kW. "
                                f"Detalle: {', '.join(resumen_mensaje)}.")
                    
                    link = f"https://wa.me/{tu_telefono}?text={texto_ws.replace(' ', '%20')}"
                    st.success("✅ ¡Presupuesto calculado! Hacé clic en el botón de abajo.")
                    st.link_button("📲 ENVIAR AHORA POR WHATSAPP", link, use_container_width=True)
                else:
                    st.warning("Completá tu nombre para continuar.")
else:
    st.warning("Verificando conexión con los datos de Sestri Energía...")
