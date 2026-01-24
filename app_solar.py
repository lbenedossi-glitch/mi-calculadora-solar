import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sestri Energía - Relevamiento", layout="centered")

@st.cache_data
def cargar_datos_excel():
    # Asegúrate de que el nombre sea IDÉNTICO al de GitHub
    nombre_archivo = 'relevamiento_enre.xlsx'
    try:
        # Leemos la primera hoja del Excel (sheet_name=0)
        df_excel = pd.read_excel(nombre_archivo, engine='openpyxl', sheet_name=0)
        
        # Limpiamos nombres de columnas y sacamos filas vacías
        df_excel.columns = df_excel.columns.str.strip()
        df_excel = df_excel.dropna(subset=[df_excel.columns[0]])
        
        # Renombramos las dos primeras columnas para que el código funcione siempre
        df_excel.rename(columns={df_excel.columns[0]: 'Artefacto', df_excel.columns[1]: 'Potencia'}, inplace=True)
        
        # Convertimos Potencia a número por si hay errores en el Excel
        df_excel['Potencia'] = pd.to_numeric(df_excel['Potencia'], errors='coerce')
        df_excel = df_excel.dropna(subset=['Potencia'])
        
        return df_excel
    except Exception as e:
        # Esto nos dirá en pantalla el error exacto si falla
        st.error(f"Error detectado: {e}")
        return None

df = cargar_datos_excel()

st.title("⚡ Sestri Energía")
st.subheader("Relevamiento de Consumo Eléctrico")

if df is not None:
    st.success("✅ Lista de equipos cargada correctamente")
    
    seleccionados = st.multiselect(
        "Buscá y seleccioná tus artefactos:",
        options=df["Artefacto"].unique().tolist()
    )
    
    # ... (el resto del proceso de cantidades y WhatsApp que ya teníamos)
else:
    st.warning(f"⚠️ No pudimos leer el archivo. Revisá que el archivo en GitHub se llame exactamente 'relevamiento_enre.xlsx'")
¿Qué hacer ahora?
Actualizá el código con este nuevo bloque.

Si sigue saliendo el cartel rojo, intentá leer las primeras palabras (por ejemplo: FileNotFoundError o ValueError).

¿Lograste ver qué dice el error en los Logs o en el cartel rojo ahora con este nuevo código? Si me pasás el nombre del error, lo arreglamos en un minuto.
