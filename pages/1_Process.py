import streamlit as st

st.set_page_config(
    page_title="Mentora Process",
    page_icon="🔍",
    layout="centered"
)

# ------------------------------------------
# -----------  ESTILO VISUAL ---------------
# ------------------------------------------

# CSS elegante y seguro para Streamlit
st.markdown("""
<style>
/* Fondo general */
.main {
    background-color: #f5f6fa;
}

/* Contenedor tipo tarjeta */
.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* Títulos principales */
h1 {
    color: #4F46E5; /* Indigo Mentora */
    font-weight: 900 !important;
}

/* Subtítulos */
h3, h2 {
    color: #4338CA; 
    font-weight: 700 !important;
}

/* Texto general */
p, label, textarea {
    font-size: 1.05rem !important;
}

/* Botón principal */
.stButton>button {
    background-color: #4F46E5;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    font-size: 1.05rem;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #3730A3;
}

/* Link */
a {
    color: #4F46E5 !important;
    text-decoration: none !important;
}
</style>
""", unsa
