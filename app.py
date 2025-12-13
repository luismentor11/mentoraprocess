import streamlit as st

# =========================
# CONFIG BÁSICA
# =========================
st.set_page_config(
    page_title="Mentora",
    page_icon="🧠",
    layout="centered",
)

# =========================
# HOME
# =========================
st.title("🧠 Mentora")
st.subheader("Entrenamiento para conversaciones críticas y toma de decisiones.")

st.write(
    "Mentora es un sistema de entrenamiento profesional para líderes, equipos y empresas "
    "que necesitan claridad, firmeza y mejores resultados en conversaciones clave."
)

st.markdown("---")

# =========================
# OPCIONES PRINCIPALES
# =========================
st.markdown("## Elegí por dónde empezar")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔍 Process")
    st.write(
        "Diagnóstico estratégico para entender:\n"
        "- dónde está el problema real\n"
        "- qué decisiones están trabadas\n"
        "- qué conversaciones no se están dando"
    )
    st.markdown("*Ideal para ordenar antes de actuar.*")

with col2:
    st.markdown("### 🎭 Roleplay Coach (voz)")
    st.write(
        "Entrenamiento práctico por voz para:\n"
        "- conversaciones difíciles\n"
        "- negociación\n"
        "- liderazgo y límites"
    )
    st.markdown(
        "Simulás la conversación, recibís feedback y entrenás antes de ir a la realidad.\n\n"
        "*Ideal para practicar y mejorar ejecución.*"
    )

st.markdown("---")

# =========================
# FLUJO RECOMENDADO
# =========================
st.markdown("## Uso típico en empresas")

st.write(
    "1. **Process** para diagnóstico\n"
    "2. **Roleplay Coach** para entrenar\n"
    "3. **Feedback y práctica concreta** para mejorar resultados"
)

st.markdown("---")

st.info("Seleccioná un módulo desde el menú lateral para comenzar.")
