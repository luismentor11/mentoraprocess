import os
import streamlit as st
from openai import OpenAI
import tempfile
import base64

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Mentora Roleplay Coach",
    page_icon="🎭",
    layout="centered"
)

st.title("🎭 Mentora Roleplay Coach — Versión con Voz")
st.caption("Hablá con el coach. Conversación en tiempo real, simulación realista.")

st.markdown("""
### Podés usar:
- 🎤 **Voz** (recomendado)  
- ⌨️ **Texto tradicional**

Cuando hables, el coach entiende tu intención y responde con voz y texto.
""")

# ---------------- API KEY ----------------
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ Falta la API Key. Cargala en *Secrets* de Streamlit Cloud.")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------------- ESTADO ----------------
if "roleplay_messages" not in st.session_state:
    st.session_state.roleplay_messages = [
        {
            "role": "system",
            "content": """
Sos Mentora Roleplay Coach. Trabajás con voice + texto.
Sos directo, empático, brutal honesto, estilo argentino.

FLUJO:
1. Diagnóstico con preguntas cortas.
2. Resumen del escenario.
3. Simulación realista (modo personaje).
4. Feedback cuando el usuario diga: pausa / feedback / cerrar.

Respondé SIEMPRE en texto + un mensaje breve para TTS.
"""
        },
        {
            "role": "assistant",
            "content": "Hola, ¿qué conversación querés practicar hoy?"
        }
    ]


# ---------------- FUNCIONES DE AUDIO ----------------

def play_audio_from_bytes(audio_bytes):
    """Reproduce audio en Streamlit desde bytes sin archivos externos."""
    b64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
        <audio controls autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


def tts(text):
    """Convierte texto en audio (voz natural OpenAI)."""
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    return response.read()


def transcribe(audio_file):
    """Convierte voz a texto (Whisper)."""
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript.text


# ---------------- HISTORIAL ----------------
st.subheader("💬 Conversación")

for msg in st.session_state.roleplay_messages:
    if msg["role"] == "system":
        continue
    with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
        st.markdown(msg["content"])


# ---------------- INPUT DE VOZ ----------------
st.subheader("🎤 Hablar con el Coach")

audio = st.audio_input("Apretá para grabar")

if audio is not None:
    st.write("⏳ Procesando audio...")
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(audio.read())
        audio_path = tmp.name

    # transcribir
    user_text = transcribe(audio_path)

    st.session_state.roleplay_messages.append({"role": "user", "content": user_text})
    st.chat_message("user").markdown(f"🎤 **Vos dijiste:** {user_text}")

    # responder
    with st.chat_message("assistant"):
        with st.spinner("Pensando respuesta..."):
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=st.session_state.roleplay_messages,
                temperature=0.8
            )

            ai_text = response.choices[0].message.content
            st.markdown(ai_text)

            st.session_state.roleplay_messages.append(
                {"role": "assistant", "content": ai_text}
            )

            # generar voz
            audio_bytes = tts(ai_text)
            play_audio_from_bytes(audio_bytes)


# ---------------- INPUT DE TEXTO ----------------
text_input = st.chat_input("O escribí acá la respuesta...")

if text_input:
    st.session_state.roleplay_messages.append({"role": "user", "content": text_input})
    st.chat_message("user").markdown(text_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando respuesta..."):
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=st.session_state.roleplay_messages,
                temperature=0.8
            )

            ai_text = response.choices[0].message.content
            st.markdown(ai_text)

            st.session_state.roleplay_messages.append(
                {"role": "assistant", "content": ai_text}
            )

            # voz
            audio_bytes = tts(ai_text)
            play_audio_from_bytes(audio_bytes)


# ---------------- SIDEBAR ----------------
st.sidebar.subheader("⚙️ Opciones")
if st.sidebar.button("🔄 Reiniciar conversación"):
    st.session_state.roleplay_messages = [
        st.session_state.roleplay_messages[0],
        {"role": "assistant", "content": "Reiniciamos. ¿Qué conversación querés practicar ahora?"}
    ]
    st.rerun()
