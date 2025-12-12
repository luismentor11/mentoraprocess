import os
import streamlit as st
from openai import OpenAI

# =========================
# CONFIG BÁSICA
# =========================
st.set_page_config(
    page_title="Mentora Roleplay Coach",
    page_icon="🎭",
    layout="centered",
)

st.title("🎭 Mentora Roleplay Coach")
st.subheader("Entrenamiento de conversaciones difíciles en contexto real")

st.write(
    "Esta herramienta te permite practicar conversaciones importantes de la vida real "
    "(colaboradores, socios, clientes, mandos medios) con un roleplay guiado. "
    "Primero definís el escenario, luego ves una lectura profesional de la situación, "
    "una estrategia sugerida y finalmente practicás la conversación en vivo."
)

# =========================
# CONFIG OPENAI
# =========================
def get_openai_client() -> OpenAI | None:
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)
    if not api_key:
        st.error(
            "No se encontró la API key de OpenAI. "
            "Configurala en Streamlit Cloud (Secrets) como OPENAI_API_KEY."
        )
        return None
    return OpenAI(api_key=api_key)

client = get_openai_client()

# =========================
# VOZ (STT + TTS)
# =========================
def voz_a_texto(audio_bytes: bytes) -> str:
    try:
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_bytes)

        with open("temp_audio.wav", "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text.strip()
    except Exception as e:
        return f"[Error STT: {e}]"


def texto_a_voz(texto: str):
    try:
        respuesta = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=texto
        )
        return respuesta
    except Exception:
        return None

# =========================
# SESSION STATE
# =========================
if "rp_brief" not in st.session_state:
    st.session_state.rp_brief = None

if "rp_diagnostico" not in st.session_state:
    st.session_state.rp_diagnostico = ""
if "rp_estrategia" not in st.session_state:
    st.session_state.rp_estrategia = ""
if "rp_conversacion" not in st.session_state:
    st.session_state.rp_conversacion = []
if "rp_iniciado" not in st.session_state:
    st.session_state.rp_iniciado = False

# =========================
# LÓGICA DE NEGOCIO
# =========================
def construir_diagnostico(brief: dict) -> str:
    return (
        f"Se está preparando una conversación con **{brief['rol_otro']}**.\n\n"
        f"Objetivo: **{brief['objetivo']}**.\n\n"
        "La clave no es ganar la discusión, sino ordenar el mensaje, "
        "sostener el límite y salir con un acuerdo concreto."
    )


def construir_estrategia(brief: dict) -> str:
    return (
        "**1. Apertura**\n"
        "- Ubicar el tema sin reproche.\n\n"
        "
