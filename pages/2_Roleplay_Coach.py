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

# ==============================
