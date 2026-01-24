import streamlit as st
import pandas as pd

# 1. Configuración
st.set_page_config(page_title="Sestri Energía - Relevamiento", layout="centered")

# 2. Función de carga
@st.cache_data
def cargar_datos_excel():
    nombre_archivo = 'relevamiento_enre.xlsx'
    try:
        df_excel = pd.read_excel(nombre_archivo, engine='openpyxl')
        df_excel.columns = df_excel.columns.str.strip()
        return df_excel
    except Exception as e:
        st.error(f"No se pudo leer el archivo: {e}")
        return None

# 3. Ejecución
df = cargar_datos_excel()

st.title("⚡ Sestri Energía")
st.subheader("Relevamiento de Consumo")

if df is not None:
    # Renombramos internamente para que no falle por mayúsculas
    df.columns = ['Artefacto', 'Potencia'] + list(df.columns[2:])
    
    seleccionados = st.multiselect(
        "Seleccioná tus equipos:", 
        options=df["Artefacto"].unique().tolist()
    )

    if seleccionados:
        total_watts = 0
        for art in seleccionados:
            p = df[df["Artefacto"] == art]["Potencia"].iloc[0]
            total_watts += p
            st.write(f"✅ {art}: {p} W")
        
        st.divider()
        st.metric("TOTAL", f"{total_watts/1000:.2f} kW")
else:
    st.info("Subí el archivo 'relevamiento_enre.xlsx' a GitHub para empezar.")
