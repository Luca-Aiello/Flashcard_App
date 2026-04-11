import streamlit as st
import pandas as pd
import random
import os

st.set_page_config(page_title="PatoRepaso Pro", layout="wide")

# Función para cargar el CSV generado
@st.cache_data
def cargar_datos():
    if os.path.exists('datos_patologia.csv'):
        return pd.read_csv('datos_patologia.csv')
    return None

df = cargar_datos()

if df is None:
    st.error("Aún no tienes el archivo 'datos_patologia.csv'. Ejecuta primero el script de limpieza.")
else:
    st.sidebar.title("Navegación")
    modo = st.sidebar.radio("Ir a:", ["Modo Estudio (Todos)", "Modo Examen (Flashcards)"])

    if modo == "Modo Estudio (Todos)":
        st.title("📚 Galería de Muestras")
        # Buscador
        busqueda = st.text_input("Buscar patógeno...")
        df_filtrado = df[df['Descripcion'].str.contains(busqueda, case=False)]
        
        # Mostrar en cuadrícula (grid)
        cols = st.columns(3)
        for i, row in df_filtrado.iterrows():
            with cols[i % 3]:
                path_foto = os.path.join("fotos", row['Imagen'])
                if os.path.exists(path_foto):
                    st.image(path_foto, caption=row['Descripcion'])
                else:
                    st.warning(f"No falta la foto: {row['Imagen']}")

    else:
        st.title("🧪 Modo Flashcard")
        st.write("Identifica la muestra y luego presiona el botón para verificar.")

        if 'indice' not in st.session_state:
            st.session_state.indice = random.randint(0, len(df)-1)

        fila = df.iloc[st.session_state.indice]
        path_foto = os.path.join("fotos", fila['Imagen'])

        if os.path.exists(path_foto):
            st.image(path_foto, width=500)
            
            if st.button("REVELAR RESPUESTA"):
                st.info(f"**Identificación:** {fila['Descripcion']}")
            
            if st.button("Siguiente muestra ➡️"):
                st.session_state.indice = random.randint(0, len(df)-1)
                st.rerun()
        else:
            st.error(f"Error: No se encuentra la foto {fila['Imagen']}")