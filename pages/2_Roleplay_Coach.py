import streamlit as st
from urllib.parse import unquote
import openai

st.set_page_config(
    page_title="Mentora Roleplay Coach",
    page_icon="🎭",
    layout="centered"
)

# ------------------------------------------
# ----------- ESTILO VISUAL -----------------
# ------------------------------------------

st.markdown("""
<style>
.card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}
h1 {
    color: #4F46E5;
    font-weight: 900 !important;
}
.stButton>button {
    background-color: #4F46E5 !important;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    font-size: 1.05rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------
# ----------- LEER PARAMETROS ---------------
# ------------------------------------------

params = st.query_params

conflicto_recibido = None
if "conflicto" in params:
    conflicto_recibido = unquote(params["conflicto"])

# ------------------------------------------
# ----------- HEADER -------------------------
# ------------------------------------------

st.markdown('<div class="card">', unsafe_allow_html=True)
st.title("🎭 Mentora Roleplay Coach")
st.caption("Simulá conversaciones difíciles con un coach interactivo que se adapta a tu estilo y objetivo.")
st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# ----------- DEFINIR TEMA ------------------
# ------------------------------------------

st.markdown('<div class="card">', unsafe_allow_html=True)

if conflicto_recibido:
    st.subheader("🧩 Conversación detectada desde Mentora Process")
    st.info(conflicto_recibido)
    tema = st.text_area("¿Querés ajustar o modificar el enfoque de la conversación?", conflicto_recibido)
else:
    tema = st.text_area("¿Sobre qué conversación querés entrenar hoy?")

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# ----------- ELEGIR ESTILO -----------------
# ------------------------------------------

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🎚 Seleccioná el estilo del roleplay")

modo = st.radio(
    "Elegí el tipo de interacción:",
    [
        "Suave — Acompañamiento y contención",
        "Directo — Comunicación clara y neutral",
        "Brutalidad Productiva — Sin filtros, foco en resultados"
    ]
)
st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# ----------- ROLEPLAY ----------------------
# ------------------------------------------

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💬 Chat de Roleplay")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Mostrar mensajes anteriores
for m in st.session_state["messages"]:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# ------------------------------------------
# ----------- GENERAR RESPUESTA -------------
# ------------------------------------------

if prompt := st.chat_input("Escribí tu mensaje para iniciar o continuar el roleplay..."):

    st.session_state["messages"].append({"role": "user", "content": prompt})

    system_prompt = f"""
    Estás actuando como un simulador de conversaciones profesionales llamado Mentora Roleplay Coach.

    Tema de la conversación: {tema}

    Modo seleccionado: {modo}

    Reglas:
    - Respondé como la contraparte real en esa conversación.
    - Adaptate al tono del modo elegido.
    - Si el usuario se traba, ofrecé alternativas.
    - No des discursos largos; mantené agilidad conversacional.
    - Siempre devolvé una pregunta que haga avanzar el roleplay.
    """

    try:
        respuesta = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state["messages"]
            ]
        )

        bot_reply = respuesta.choices[0].message["content"]

        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

        with st.chat_message("assistant"):
            st.write(bot_reply)

    except Exception as e:
        st.error("Error generando respuesta. Revisá tu API Key o el modelo seleccionado.")
        st.stop()

st.markdown('</div>', unsafe_allow_html=True)
