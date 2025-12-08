import os
import streamlit as st
from openai import OpenAI

# ---------------- CONFIGURACIÓN BÁSICA ----------------
st.set_page_config(
    page_title="Mentora Roleplay Coach",
    page_icon="🎭",
    layout="centered"
)

st.title("🎭 Mentora Roleplay Coach")
st.caption("Simulación inteligente de conversaciones profesionales")

st.markdown("""
Este módulo te ayuda a practicar conversaciones importantes:
- Dar feedback difícil  
- Negociar con clientes  
- Manejar conversaciones con tu jefe  
- Resolver conflictos con tu equipo  

Primero entendemos tu contexto y luego simulamos la conversación en vivo.
""")

# ---------------- API KEY ----------------
api_key = st.text_input(
    "Colocá tu OpenAI API Key",
    type="password",
    help="También podés configurar la variable de entorno OPENAI_API_KEY."
)

if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.warning("⚠️ Falta la API Key. Ingresala arriba para continuar.")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------------- ESTADO DE SESIÓN ----------------
if "roleplay_messages" not in st.session_state:
    st.session_state.roleplay_messages = [
        {
            "role": "system",
            "content": """
Sos **Mentora Roleplay Coach**, experto en conversaciones difíciles,
negociación, liderazgo, ventas y comunicación profesional.

SEGUIDO ESTE FLUJO SIEMPRE:

FASE 1 — DIAGNÓSTICO
Hacé entre 3 y 5 preguntas (una por mensaje):
- ¿Cuál es tu rol? (líder, vendedor, empleado, socio…)
- ¿Con quién querés practicar? (jefe, cliente, colaborador…)
- ¿Qué conversación puntual querés entrenar?
- ¿Qué te incomoda o te da miedo de esta situación?
- ¿Qué resultado concreto querés lograr?

Cuando tengas claridad, decí:
“Listo, ya tengo el escenario claro. Ahora lo resumo y después arrancamos la simulación.”

FASE 2 — DISEÑO DEL ESCENARIO
Resumí en 4–6 líneas:
- contexto
- roles (vos y el personaje)
- objetivo de la conversación
- tono (suave / realista / brutal honesto)

Luego preguntá:
“¿Querés comenzar la simulación?”

FASE 3 — ROLEPLAY (simulación)
- Entrá EN PERSONAJE.
- Respuestas cortas, naturales.
- Usá lenguaje argentino si el usuario lo usa.
- No aclares que sos IA.

FASE 4 — FEEDBACK
Si el usuario dice “pausa”, “feedback” o “cerrar”:
- Salí del personaje.
- Resumí:
  - 3 fortalezas
  - 3 áreas de mejora
  - 3 recomendaciones prácticas
Preguntá si quiere repetir con más dificultad o crear un escenario nuevo.
"""
        },
        {
            "role": "assistant",
            "content": "Hola, soy Mentora Roleplay Coach 🎭. ¿Qué conversación te gustaría practicar hoy?"
        }
    ]

# ---------------- MOSTRAR HISTORIAL ----------------
for msg in st.session_state.roleplay_messages:
    if msg["role"] == "system":
        continue
    with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
        st.markdown(msg["content"])

# ---------------- INPUT DEL USUARIO ----------------
user_input = st.chat_input("Escribí acá para hablar con el coach...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.roleplay_messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Procesando..."):
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=st.session_state.roleplay_messages,
                temperature=0.8
            )
            reply = response.choices[0].message.content

            st.markdown(reply)
            st.session_state.roleplay_messages.append(
                {"role": "assistant", "content": reply}
            )

# ---------------- SIDEBAR ----------------
st.sidebar.subheader("⚙️ Controles")

if st.sidebar.button("🔄 Reiniciar roleplay"):
    st.session_state.roleplay_messages = [
        st.session_state.roleplay_messages[0],
        {"role": "assistant", "content": "Reiniciamos. ¿Qué conversación querés practicar ahora?"}
    ]
    st.experimental_rerun()
