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
def get_openai_client():
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
def voz_a_texto(audio_bytes):
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


def texto_a_voz(texto):
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
if "rp_feedback" not in st.session_state:
    st.session_state.rp_feedback = None
if "rp_patron" not in st.session_state:
    st.session_state.rp_patron = None

# =========================
# LÓGICA MENTORA
# =========================
def construir_diagnostico(brief):
    return (
        f"Se está preparando una conversación con **{brief['rol_otro']}**.\n\n"
        f"Objetivo: **{brief['objetivo']}**.\n\n"
        "La clave no es ganar la discusión, sino ordenar el mensaje, "
        "sostener el límite y salir con un acuerdo concreto."
    )


def construir_estrategia(brief):
    return (
        "**1. Apertura**\n"
        "- Ubicar el tema sin reproche.\n\n"
        "**2. Desarrollo**\n"
        "- Describir hechos concretos.\n\n"
        "**3. Pedido**\n"
        "- Pedido claro y verificable.\n\n"
        "**4. Cierre**\n"
        "- Acordar próximo paso."
    )


def construir_system_prompt(brief):
    return (
        "Sos MENTORA ROLEPLAY COACH.\n"
        "Actuás como la OTRA PERSONA de la conversación.\n"
        "No explicás teoría. No sos coach.\n\n"
        "Respondé como humano real.\n"
        "1 a 5 líneas máximo.\n\n"
        f"ROL QUE REPRESENTÁS: {brief['rol_otro']}\n"
        f"OBJETIVO DEL USUARIO: {brief['objetivo']}\n"
        f"CONTEXTO: {brief['que_pasa']}\n"
        f"EMOCIÓN DEL USUARIO: {brief['emocion']}\n"
        f"TONO BUSCADO: {brief['tono']}\n"
    )


def llamar_modelo_roleplay(brief, conversacion):
    if client is None:
        return "No se pudo conectar con el modelo."

    system_prompt = construir_system_prompt(brief)
    mensajes = [{"role": "system", "content": system_prompt}]
    mensajes.extend(conversacion)

    respuesta = client.responses.create(
        model="gpt-4.1-mini",
        input=mensajes,
    )

    return respuesta.output[0].content[0].text.strip()


def detectar_patron_humano(conversacion):
    if client is None:
        return "No se pudo detectar patrón."

    prompt = (
        "Analizás una conversación real desde coaching ontológico.\n"
        "Detectás el PATRÓN HUMANO DOMINANTE del usuario.\n\n"
        "Patrones posibles:\n"
        "- Evitación del conflicto\n"
        "- Necesidad de aprobación\n"
        "- Rigidez / control\n"
        "- Confusión / dispersión\n\n"
        "Respondé SOLO con este formato:\n"
        "PATRON:\n"
        "- <nombre del patrón>\n\n"
        "LECTURA:\n"
        "- explicación breve (2 a 3 líneas)\n"
    )

    mensajes = [{"role": "system", "content": prompt}]
    mensajes.extend(conversacion)

    respuesta = client.responses.create(
        model="gpt-4.1-mini",
        input=mensajes,
    )

    return respuesta.output[0].content[0].text.strip()


def generar_feedback_ontologico(brief, conversacion):
    if client is None:
        return "No se pudo generar feedback."

    prompt = (
        "Actuás como un coach ontológico senior de Mentora.\n"
        "Leés una conversación real y das feedback breve, claro y accionable.\n\n"
        "Formato de salida EXACTO:\n"
        "FORTALEZAS:\n"
        "- ...\n"
        "- ...\n"
        "- ...\n\n"
        "A MEJORAR:\n"
        "- ...\n"
        "- ...\n\n"
        "PRACTICA CLAVE:\n"
        "- ...\n\n"
        f"Objetivo: {brief['objetivo']}\n"
        f"Emoción: {brief['emocion']}\n"
        f"Tono: {brief['tono']}\n"
    )

    mensajes = [{"role": "system", "content": prompt}]
    mensajes.extend(conversacion)

    respuesta = client.responses.create(
        model="gpt-4.1-mini",
        input=mensajes,
    )

    return respuesta.output[0].content[0].text.strip()

# =========================
# 1) BRIEF
# =========================
st.markdown("### 1️⃣ Definí el escenario")

with st.form("rp_form"):
    tipo_situacion = st.selectbox(
        "Tipo de situación",
        [
            "Conversación difícil",
            "Feedback",
            "Marcar un límite",
            "Reunión con socio",
            "Cliente enojado",
        ],
    )

    rol_otro = st.selectbox(
        "¿Con quién hablás?",
        ["Colaborador", "Jefe", "Socio", "Cliente"],
    )

    emocion = st.selectbox(
        "Emoción predominante",
        ["Calma", "Ansiedad", "Bronca", "Cansancio"],
    )

    tono = st.selectbox(
        "Tono buscado",
        ["Directo", "Empático", "Firme", "Muy al hueso"],
    )

    objetivo = st.text_input("Objetivo concreto")
    que_pasa = st.text_area("¿Qué está pasando?")

    submitted = st.form_submit_button("Generar estrategia")

if submitted:
    st.session_state.rp_brief = {
        "tipo_situacion": tipo_situacion,
        "rol_otro": rol_otro,
        "emocion": emocion,
        "tono": tono,
        "objetivo": objetivo or "Ordenar la situación",
        "que_pasa": que_pasa,
    }

    st.session_state.rp_diagnostico = construir_diagnostico(st.session_state.rp_brief)
    st.session_state.rp_estrategia = construir_estrategia(st.session_state.rp_brief)
    st.session_state.rp_conversacion = []
    st.session_state.rp_iniciado = False
    st.session_state.rp_feedback = None
    st.session_state.rp_patron = None

# =========================
# 2) ROLEPLAY
# =========================
if st.session_state.rp_brief:

    st.markdown("---")
    st.markdown("### 2️⃣ Lectura profesional")
    st.write(st.session_state.rp_diagnostico)

    st.markdown("### 3️⃣ Estrategia sugerida")
    st.markdown(st.session_state.rp_estrategia)

    st.markdown("### 4️⃣ Roleplay en vivo")

    if not st.session_state.rp_iniciado:
        st.session_state.rp_conversacion.append(
            {"role": "assistant", "content": "Hola, ¿qué querías hablar conmigo?"}
        )
        st.session_state.rp_iniciado = True

    for msg in st.session_state.rp_conversacion:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if client:
        col_txt, col_voice = st.columns([2, 1])

        with col_txt:
            user_text = st.chat_input("Escribí tu mensaje")

        with col_voice:
            audio = st.audio_input("🎤 Hablar")

        if user_text:
            st.session_state.rp_conversacion.append(
                {"role": "user", "content": user_text}
            )
            reply = llamar_modelo_roleplay(
                st.session_state.rp_brief,
                st.session_state.rp_conversacion,
            )
            st.session_state.rp_conversacion.append(
                {"role": "assistant", "content": reply}
            )
            st.rerun()

        if audio:
            texto_usuario = voz_a_texto(audio.getvalue())
            st.session_state.rp_conversacion.append(
                {"role": "user", "content": texto_usuario}
            )
            reply = llamar_modelo_roleplay(
                st.session_state.rp_brief,
                st.session_state.rp_conversacion,
            )
            st.session_state.rp_conversacion.append(
                {"role": "assistant", "content": reply}
            )

            audio_resp = texto_a_voz(reply)
            if audio_resp:
                st.audio(audio_resp, format="audio/mp3")

            st.rerun()

    st.markdown("---")
    if st.button("🧠 Cerrar sesión y ver análisis"):
        st.session_state.rp_patron = detectar_patron_humano(
            st.session_state.rp_conversacion
        )
        st.session_state.rp_feedback = generar_feedback_ontologico(
            st.session_state.rp_brief,
            st.session_state.rp_conversacion,
        )

# =========================
# 3) CIERRE + PATRÓN
# =========================
if st.session_state.rp_patron:
    st.markdown("## 🔍 Patrón humano detectado")
    st.markdown(st.session_state.rp_patron)

if st.session_state.rp_feedback:
    st.markdown("## 🧠 Feedback Mentora")
    st.markdown(st.session_state.rp_feedback)
