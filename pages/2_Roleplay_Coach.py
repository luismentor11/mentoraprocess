import os
import streamlit as st
from openai import OpenAI

# ======================================================
# CONFIG BÁSICA
# ======================================================
st.set_page_config(
    page_title="Mentora Roleplay Coach",
    page_icon="🎭",
    layout="centered",
)

st.title("🎭 Mentora Roleplay Coach")
st.subheader("Entrenamiento real de conversaciones por voz")

# ======================================================
# OPENAI
# ======================================================
def get_client():
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        st.error("Falta OPENAI_API_KEY en Secrets.")
        st.stop()
    return OpenAI(api_key=api_key)

client = get_client()

# ======================================================
# STT — VOZ A TEXTO (ROBUSTO)
# ======================================================
def voz_a_texto(audio_file):
    try:
        audio_bytes = audio_file.read()
        with open("input_audio.wav", "wb") as f:
            f.write(audio_bytes)

        with open("input_audio.wav", "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )

        return transcript.text.strip()

    except Exception as e:
        return f"[ERROR STT: {e}]"

# ======================================================
# TTS — TEXTO A VOZ (ARCHIVO REAL)
# ======================================================
def texto_a_voz(texto):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "mp3"},
            input=texto
        )

        audio_data = response.output[0].content[0].audio
        audio_bytes = audio_data.get("data")

        if not audio_bytes:
            return None

        with open("respuesta.mp3", "wb") as f:
            f.write(audio_bytes)

        return "respuesta.mp3"

    except Exception as e:
        return None

# ======================================================
# SESSION STATE
# ======================================================
if "conversacion" not in st.session_state:
    st.session_state.conversacion = []

# ======================================================
# SYSTEM PROMPT (SIMPLE Y REALISTA)
# ======================================================
SYSTEM_PROMPT = (
    "Sos la otra persona en una conversación real.\n"
    "Respondés como humano, no como coach.\n"
    "Frases cortas, tono natural.\n"
)

# ======================================================
# LLAMADA AL MODELO (TEXTO)
# ======================================================
def responder(mensajes):
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    msgs.extend(mensajes)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=msgs
    )

    return response.output[0].content[0].text.strip()

# ======================================================
# UI
# ======================================================
st.markdown("### Conversación")

for msg in st.session_state.conversacion:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

col1, col2 = st.columns([2, 1])

with col1:
    texto = st.chat_input("Escribí tu mensaje")

with col2:
    audio = st.audio_input("🎤 Hablar")

# ======================================================
# TEXTO
# ======================================================
if texto:
    st.session_state.conversacion.append(
        {"role": "user", "content": texto}
    )

    reply = responder(st.session_state.conversacion)

    st.session_state.conversacion.append(
        {"role": "assistant", "content": reply}
    )

    audio_path = texto_a_voz(reply)
    if audio_path:
        st.audio(audio_path, format="audio/mp3")

    st.rerun()

# ======================================================
# VOZ
# ======================================================
if audio:
    texto_usuario = voz_a_texto(audio)

    st.session_state.conversacion.append(
        {"role": "user", "content": texto_usuario}
    )

    reply = responder(st.session_state.conversacion)

    st.session_state.conversacion.append(
        {"role": "assistant", "content": reply}
    )

    audio_path = texto_a_voz(reply)
    if audio_path:
        st.audio(audio_path, format="audio/mp3")

    st.rerun()
