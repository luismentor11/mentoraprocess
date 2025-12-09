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
.roleplay-btn {
    background: #4F46E5; 
    padding: 8px 15px; 
    border-radius: 10px; 
    color: white; 
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
# ----------- CLASIFICADOR AUTOMÁTICO -------
# ------------------------------------------

def clasificar_conflicto(texto):
    if not texto:
        return "General", []

    t = texto.lower()

    # Liderazgo / empleados
    if any(x in t for x in ["empleado", "equipo", "personal", "trabajador", "colaborador"]):
        return "Liderazgo y Gestión de Personas", [
            "Charla de alineación y expectativas",
            "Feedback correctivo claro y firme",
            "Cortar patrón repetitivo y reestablecer autoridad"
        ]

    # Socios
    if any(x in t for x in ["socio", "sociedad", "decisiones", "acuerdos"]):
        return "Socios y Negociación Estratégica", [
            "Definición de roles y toma de decisiones",
            "Alineación de visión del negocio",
            "Negociación de responsabilidades"
        ]

    # Clientes / ventas
    if any(x in t for x in ["cliente", "venta", "presupuesto", "queja"]):
        return "Clientes y Manejo Comercial", [
            "Negociación de precio / objeciones",
            "Conversación de reclamo difícil",
            "Cierre comercial con presión"
        ]

    # Productividad / burnout / emocional
    if any(x in t for x in ["cans", "agot", "estres", "tiempo", "anquietud", "ansiedad"]):
        return "Gestión Emocional y Productividad", [
            "Pedido de ayuda / redistribución de carga",
            "Poner límites sin culpa",
            "Reestructurar tiempos y prioridades"
        ]

    return "Conversación General", [
        "Clarificación de expectativas",
        "Expresión honesta sin conflicto",
        "Negociación simple"
    ]

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
# ----------- CLASIFICACIÓN AUTOMÁTICA ------
# ------------------------------------------

if tema:
    categoria, escenarios = clasificar_conflicto(tema)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧭 Tipo de conversación detectada automáticamente")
    st.success(categoria)

    st.markdown("### Escenarios recomendados:")
    for i, esc in enumerate(escenarios, 1):
        st.markdown(f"**{i}. {esc}**")

    st.markdown("</div>", unsafe_allow_html=True)


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
# ----------- CHAT ROLEPLAY -----------------
# ------------------------------------------

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("💬 Chat de Roleplay")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Mostrar historial
for m in st.session_state["messages"]:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# ------------------------------------------
# ----------- GENERAR RESPUESTA IA ----------
# ------------------------------------------

if prompt := st.chat_input("Escribí tu mensaje para iniciar o continuar el roleplay..."):

    st.session_state["messages"].append({"role": "user", "content": prompt})

    system_prompt = f"""
    Estás actuando como un simulador conversacional profesional llamado Mentora Roleplay Coach.

    Tema principal: {tema}
    Categoría detectada: {categoria}
    Escenarios recomendados: {escenarios}
    Modo seleccionado: {modo}

    Reglas:
    - Respondé como la contraparte real en esa conversación.
    - Ajustate al modo elegido (suave, directo o brutalidad productiva).
    - Ayudá a profundizar con preguntas.
    - No sermonees, no des monólogos.
    - La conversación debe avanzar hacia claridad y resolución.
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
        st.error("Error generando respuesta. Revisá tu API key o el modelo.")
        st.stop()

st.markdown('</div>', unsafe_allow_html=True)
