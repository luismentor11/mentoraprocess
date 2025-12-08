import os
import textwrap
from datetime import datetime

import streamlit as st

# =========================
# CONFIG BÁSICA DE LA APP
# =========================

APP_NAME = "Mentora Process"
PAGE_TITLE = f"{APP_NAME} – Diagnóstico de Liderazgo, Procesos y Cliente"
PAGE_ICON = "🧠"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered")


# =========================
# ESTILOS (FONDO CLARO, LOOK CORPORATIVO)
# =========================

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Contenedor principal centrado */
        .block-container {
            max-width: 900px !important;
