import streamlit as st

from modules.encuesta import mostrar_registro
from modules.recomendaciones import mostrar_directorio

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Chokoi",
    page_icon="🍫",
    layout="wide"
)

# =====================================================
# HEADER
# =====================================================

st.title("Chokoi")

st.subheader(
    "Directorio de productores de cacao y chocolate mexicano"
)

st.write(
    """
    Chokoi busca conectar productores,
    emprendimientos y consumidores interesados
    en cacao mexicano y comercio justo.
    """
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Navegación")

modo = st.sidebar.selectbox(
    "Selecciona una sección",
    [
        "Inicio",
        "Registrar productor",
        "Explorar productores"
    ]
)

# =====================================================
# INICIO
# =====================================================

if modo == "Inicio":

    st.header("¿Qué es Chokoi?")

    st.write(
        """
        Chokoi es un directorio digital enfocado
        en visibilizar productores mexicanos
        de cacao y chocolate artesanal.
        """
    )

    st.markdown(
        """
        ### Objetivos

        - Fortalecer la visibilidad de productores

        - Facilitar conexión comercial

        - Generar datos para análisis territorial

        - Impulsar el cacao mexicano
        """
    )

# =====================================================
# REGISTRO
# =====================================================

elif modo == "Registrar productor":

    mostrar_registro()

# =====================================================
# DIRECTORIO
# =====================================================

elif modo == "Explorar productores":

    mostrar_directorio()

