import os
import base64
import tempfile
import streamlit as st
from openai import OpenAI

# ------------- API KEY -------------
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ No se encontró OPENAI_API_KEY en Secrets ni en variables de entorno.")
    st.stop()

client = OpenAI(api_key=api_key)

# ------------- ESTADO INICIAL -------------
if "roleplay_messages" not in st.session_state:
    st.session_state.roleplay_messages = []

if "simulation_mode" not in st.session_state:
    st.session_state.simulation_mode = "Estándar"


# ------------- CONFIGURACIÓN DE MODOS -------------
MODOS = {
    "Estándar": """
Modo estándar: tono profesional, empático y claro.
Simulás a una persona razonable, firme pero abierta al diálogo.
""",
    "Cliente difícil": """
Modo cliente difícil: persona exigente, impaciente, algo irritada.
Interrumpe, desconfía, cuestiona el precio o el valor, pero sin ser totalmente irracional.
""",
    "Brutal honesto (modo samurái)": """
Modo brutal honesto: decís lo que muchos piensan y nadie se anima a decir.
Sin maquillaje, directo, frontal, poniendo presión en la conversación.
Nunca faltás el respeto, pero no suavizás nada.
"""
}


def build_system_prompt(mode: str) -> str:
    return f"""
Sos **Mentora Roleplay Coach**, un simulador de conversaciones difíciles para contextos de empresa,
ventas, liderazgo y trabajo en equipo.

Te manejás en tres modos:
- Estándar: profesional, empático, equilibrado.
- Cliente difícil: más exigente, crítico y emocional.
- Brutal honesto: directo, frontal, sin anestesia pero con respeto.

MODO ACTUAL: {mode.upper()}

FLUJO DE TRABAJO:

FASE 1 — DIAGNÓSTICO
- Hacés 3 a 5 preguntas CORTAS, una por mensaje:
  - ¿Cuál es tu rol?
  - ¿Con quién querés practicar? (jefe, cliente, colaborador...)
  - ¿Qué conversación concreta querés entrenar?
  - ¿Qué te incomoda o te da miedo de esta situación?
  - ¿Qué resultado te gustaría lograr?

FASE 2 — RESUMEN DEL ESCENARIO
- Resumís en 4–6 líneas:
  - contexto
  - roles (quién es el usuario y quién sos vos en el roleplay)
  - objetivo de la conversación
  - cómo se va a sentir aproximadamente el otro según el modo elegido

FASE 3 — ROLEPLAY
- Entrás en personaje.
- Respondés como una persona real en esa situación.
- Respuestas cortas, naturales, como en una charla real.
- Usás lenguaje argentino si el usuario escribe así.
- No aclarás que sos una IA mientras estás en personaje.

FASE 4 — FEEDBACK
Si el usuario dice “pausa”, “feedback” o “cerrar”:
- Salís del personaje.
- Dás:
  - 3 fortalezas
  - 3 áreas de mejora
  - 3 recomendaciones concretas para la próxima conversación.
Preguntás si quiere repetir con más dificultad o cambiar de escenario.
"""


def reset_conversation():
    st.session_state.roleplay_messages = [
        {
            "role": "system",
            "content": build_system_prompt(st.session_state.simulation_mode)
        },
        {
            "role": "assistant",
            "content": "Soy Mentora Roleplay Coach 🎭. Contame brevemente qué conversación te gustaría practicar hoy."
        }
    ]


# Si todavía no inicializamos con el modo actual:
if not st.session_state.roleplay_messages:
    reset_conversation()

# ------------- UI PRINCIPAL -------------
st.title("🎭 Mentora Roleplay Coach")
st.caption("Simulador de conversaciones difíciles con modos configurables para empresas.")

st.markdown("""
Elegí un escenario y practicá una conversación importante en un entorno seguro y controlado.

Podés usar **voz** (micrófono) o **texto**.
""")

# ----- Selector de modo -----
st.subheader("🎚️ Modo de simulación")

nuevo_modo = st.selectbox(
    "Elegí el estilo del roleplay:",
    list(MODOS.keys()),
    index=list(MODOS.keys()).index(st.session_state.simulation_mode)
)

st.markdown(f"**Descripción del modo:** {MODOS[nuevo_modo]}")

c1, c2 = st.columns(2)
with c1:
    if st.button("Aplicar este modo"):
        if nuevo_modo != st.session_state.simulation_mode:
            st.session_state.simulation_mode = nuevo_modo
            reset_conversation()
            st.success(f"Modo actualizado a: {nuevo_modo}")
with c2:
    if st.button("Reiniciar conversación"):
        reset_conversation()
        st.info("Conversación reiniciada con el modo actual.")


# ------------- FUNCIONES AUDIO / TTS -------------
def play_audio_from_bytes(audio_bytes: bytes):
    b64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
        <audio controls autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


def tts(text: str) -> bytes:
    """Texto a voz con OpenAI."""
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    return response.read()


def transcribe(file_path: str) -> str:
    """Voz a texto con Whisper."""
    with open(file_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text


# ------------- HISTORIAL EN PANTALLA -------------
st.subheader("💬 Conversación")

for msg in st.session_state.roleplay_messages:
    if msg["role"] == "system":
        continue
    with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
        st.markdown(msg["content"])


# ------------- INPUT POR VOZ -------------
st.subheader("🎤 Hablar con el coach (opcional)")

audio = st.audio_input("Grabá un mensaje de voz para el coach")

if audio is not None:
    st.write("⏳ Procesando audio...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio.read())
        audio_path = tmp.name

    # Transcribir audio
    user_text = transcribe(audio_path)

    st.session_state.roleplay_messages.append({"role": "user", "content": user_text})
    st.chat_message("user").markdown(f"🎤 **Vos dijiste (voz):** {user_text}")

    # Respuesta del coach
    with st.chat_message("assistant"):
        with st.spinner("Pensando la mejor respuesta..."):
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=st.session_state.roleplay_messages,
                temperature=0.8,
            )
            ai_text = response.choices[0].message.content

            st.markdown(ai_text)
            st.session_state.roleplay_messages.append(
                {"role": "assistant", "content": ai_text}
            )

            # Generar voz
            try:
                audio_bytes = tts(ai_text)
                play_audio_from_bytes(audio_bytes)
            except Exception:
                st.warning("No se pudo generar audio, pero el texto está listo.")


# ------------- INPUT POR TEXTO -------------
text_input = st.chat_input("O escribí acá para practicar por chat...")

if text_input:
    st.session_state.roleplay_messages.append({"role": "user", "content": text_input})
    st.chat_message("user").markdown(text_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando la mejor respuesta..."):
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=st.session_state.roleplay_messages,
                temperature=0.8,
            )
            ai_text = response.choices[0].message.content

            st.markdown(ai_text)
            st.session_state.roleplay_messages.append(
                {"role": "assistant", "content": ai_text}
            )

            # Voz opcional
            try:
                audio_bytes = tts(ai_text)
                play_audio_from_bytes(audio_bytes)
            except Exception:
                pass

# ------------- SIDEBAR INFO -------------
st.sidebar.title("Mentora Roleplay Coach")
st.sidebar.markdown("""
Esta demo está pensada para empresas que quieren:

- Entrenar líderes y mandos medios  
- Practicar conversaciones difíciles antes de tenerlas  
- Reducir errores en comunicación y decisiones  

Usá los **modos de simulación** para mostrar cómo cambia la conversación según el contexto.
""")
