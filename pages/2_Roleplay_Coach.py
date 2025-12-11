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
        st.error("No se encontró la API key de OpenAI. Configurala en Streamlit Cloud (Secrets) como OPENAI_API_KEY.")
        return None
    return OpenAI(api_key=api_key)

client = get_openai_client()

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
    # cada ítem: {"role": "user"/"assistant", "content": str}
    st.session_state.rp_conversacion = []
if "rp_iniciado" not in st.session_state:
    st.session_state.rp_iniciado = False

# =========================
# HELPERS LÓGICOS
# =========================

def construir_diagnostico(brief: dict) -> str:
    """Texto profesional que lee el escenario de conversación."""
    tipo = brief["tipo_situacion"]
    objetivo = brief["objetivo"]
    emocion = brief["emocion"]
    tono = brief["tono"]
    rol_otro = brief["rol_otro"]
    que_pasa = brief["que_pasa"]

    partes = []

    partes.append(
        f"Se está preparando una conversación con **{rol_otro}** en un contexto de **{tipo.lower()}**. "
        f"El objetivo declarado es: **{objetivo}**."
    )

    if emocion in ["Bronca", "Irritación"]:
        partes.append(
            "La emoción predominante es de enojo, lo que aumenta el riesgo de que la conversación derive "
            "en descarga emocional en lugar de orden y acuerdos. Es clave cuidar el tono y los tiempos."
        )
    elif emocion in ["Ansiedad", "Confusión"]:
        partes.append(
            "La emoción predominante es de inquietud o confusión. Esto puede llevar a evitar poner el tema "
            "en palabras claras o salir de la conversación sin un acuerdo concreto."
        )
    elif emocion in ["Cansancio", "Resignación"]:
        partes.append(
            "Hay signos de cansancio o resignación. Eso suele traducirse en conversaciones donde se nombra el problema "
            "pero no se sostienen límites ni acuerdos nuevos en el tiempo."
        )
    else:
        partes.append(
            "La emocionalidad declarada está relativamente regulada, lo que aumenta la posibilidad de sostener una conversación clara y efectiva."
        )

    partes.append(
        "En esta situación, la clave no es ganar la discusión, sino ordenar el mensaje, sostener el límite que corresponde "
        "y salir de la conversación con un acuerdo claro y verificable, aunque sea incómodo."
    )

    if que_pasa.strip():
        partes.append(
            f"Resumen del caso que se quiere trabajar: {que_pasa.strip()}"
        )

    return "\n\n".join(partes)


def construir_estrategia(brief: dict) -> str:
    """Estrategia conversacional en 4 pasos."""
    tipo = brief["tipo_situacion"]
    objetivo = brief["objetivo"]
    tono = brief["tono"]
    rol_otro = brief["rol_otro"]

    estrategia = []

    estrategia.append("**1. Apertura**")
    estrategia.append(
        f"- Empezar ubicando contexto y reconocimiento: explicar en pocas palabras de qué querés hablar con {rol_otro} "
        f"y por qué es importante para el funcionamiento de la empresa, evitando reproches directos en la primera frase.\n"
        f"- El tono sugerido es: **{tono}**."
    )

    estrategia.append("**2. Cuerpo de la conversación**")
    estrategia.append(
        "- Describir hechos concretos (qué pasó, cuándo, cómo impactó) sin generalizar ni etiquetar a la persona.\n"
        "- Nombrar cómo eso afecta al equipo, al sistema y/o al cliente.\n"
        f"- Relacionar lo que está pasando con el objetivo: **{objetivo}**."
    )

    estrategia.append("**3. Pedido y acuerdo**")
    if "límite" in objetivo.lower():
        estrategia.append(
            "- Hacer un pedido claro sobre lo que a partir de ahora **no se va a seguir tolerando** y qué comportamiento se espera.\n"
            "- Acordar plazos y criterios concretos (qué cambia y desde cuándo)."
        )
    elif "feedback" in tipo.lower() or "feedback" in objetivo.lower():
        estrategia.append(
            "- Dar feedback desde la observación, no desde la acusación.\n"
            "- Preguntar al otro cómo ve la situación y qué está dispuesto a ajustar."
        )
    else:
        estrategia.append(
            "- Expresar con claridad qué esperás que cambie, qué necesitas que la otra parte vea y qué compromiso estás pidiendo.\n"
            "- Chequear si la otra persona comprende y está dispuesta a asumir ese compromiso."
        )

    estrategia.append("**4. Cierre**")
    estrategia.append(
        "- Resumir en voz alta el acuerdo o el resultado (aun si el resultado es: no hubo acuerdo, pero el límite quedó claro).\n"
        "- Agradecer la conversación sin desarmar el límite planteado.\n"
        "- Acordar un próximo punto de revisión si el tema lo requiere."
    )

    return "\n".join(estrategia)


def construir_system_prompt(brief: dict) -> str:
    """Prompt del sistema para el modelo. El modelo actúa como la otra persona, no como coach."""
    return (
        "Sos MENTORA ROLEPLAY COACH, actuando como la otra parte en una conversación real.\n"
        "NO sos terapeuta, NO sos mediador externo, NO explicás teoría.\n"
        "Tu tarea es representar con realismo a la persona con la que el usuario quiere hablar.\n\n"
        "Reglas:\n"
        "- Respondé siempre en primera persona, como si fueras esa persona.\n"
        "- Mantené un comportamiento coherente con el rol y el escenario.\n"
        "- Podés estar a la defensiva, confundido, colaborativo o resistente según la situación, pero siempre verosímil.\n"
        "- No reveles que sos una IA ni que esto es un ejercicio.\n"
        "- No des consejos al usuario, solo respondé como personaje.\n\n"
        "Cuando el usuario escriba, respondé en 1 a 5 líneas, máximo. No hagas monólogos eternos.\n\n"
        f"ESCENARIO:\n"
        f"- Tipo de situación: {brief['tipo_situacion']}\n"
        f"- Rol que representás: {brief['rol_otro']}\n"
        f"- Objetivo declarado del usuario: {brief['objetivo']}\n"
        f"- Emoción predominante del usuario: {brief['emocion']}\n"
        f"- Tono deseado de la conversación: {brief['tono']}\n"
        f"- Descripción del caso: {brief['que_pasa']}\n"
    )


def llamar_modelo_roleplay(brief: dict, conversacion: list[dict]) -> str:
    """Llama al modelo usando Responses API, armando contexto + historial."""
    if client is None:
        return "No se pudo conectar con el modelo (falta API key)."

    system_prompt = construir_system_prompt(brief)

    # Armamos el input: system + historial
    mensajes = [{"role": "system", "content": system_prompt}]
    for msg in conversacion:
        mensajes.append(
            {"role": msg["role"], "content": msg["content"]}
        )

    try:
        respuesta = client.responses.create(
            model="gpt-4.1-mini",
            input=mensajes,
        )
        # Adaptado al formato de la Responses API nueva
        texto = respuesta.output[0].content[0].text
        return texto.strip()
    except Exception as e:
        return f"Hubo un error al generar la respuesta del roleplay: {e}"


# =========================
# 1) BRIEF DEL ESCENARIO
# =========================

st.markdown("### 1️⃣ Definí el escenario de la conversación")

with st.form("rp_brief_form"):

    col1, col2 = st.columns(2)

    with col1:
        tipo_situacion = st.selectbox(
            "Tipo de situación",
            [
                "Conversación difícil con un colaborador",
                "Feedback delicado",
                "Marcar un límite",
                "Reunión con socio / dirección",
                "Coordinación entre áreas",
                "Cliente enojado",
                "Otro tipo de conversación crítica",
            ],
        )

        emocion = st.selectbox(
            "Emoción predominante en vos",
            [
                "Calma / foco",
                "Ansiedad",
                "Bronca",
                "Irritación",
                "Cansancio",
                "Resignación",
                "Confusión",
            ],
        )

    with col2:
        rol_otro = st.selectbox(
            "¿Con quién es la conversación?",
            [
                "Colaborador / empleado",
                "Jefe / superior",
                "Socio / cofundador",
                "Cliente",
                "Proveedor",
                "Familiar dentro del sistema",
                "Otro",
            ],
        )

        tono = st.selectbox(
            "Tono que querés sostener",
            [
                "Directo, pero respetuoso",
                "Formal y profesional",
                "Contenedor pero firme",
                "Empático, pero claro",
                "Muy al hueso, sin vueltas",
            ],
        )

    objetivo = st.text_input(
        "¿Qué te gustaría lograr con esta conversación? (1 frase)",
        placeholder="Ejemplo: que la persona entienda el impacto de lo que hace y se comprometa a cambiar su forma de trabajo.",
    )

    que_pasa = st.text_area(
        "Contá brevemente qué está pasando y por qué esta conversación es importante:",
        placeholder="Ejemplo: llega tarde, no cumple plazos, evita asumir errores, tensa al resto del equipo, etc.",
    )

    submitted_brief = st.form_submit_button("Generar lectura y estrategia")

if submitted_brief:
    st.session_state.rp_brief = {
        "tipo_situacion": tipo_situacion,
        "emocion": emocion,
        "rol_otro": rol_otro,
        "tono": tono,
        "objetivo": objetivo.strip() or "Ordenar la situación y lograr un acuerdo concreto.",
        "que_pasa": que_pasa.strip(),
    }

    st.session_state.rp_diagnostico = construir_diagnostico(st.session_state.rp_brief)
    st.session_state.rp_estrategia = construir_estrategia(st.session_state.rp_brief)

    # reiniciar conversación
    st.session_state.rp_conversacion = []
    st.session_state.rp_iniciado = False

# =========================
# 2) DIAGNÓSTICO + ESTRATEGIA
# =========================

if st.session_state.rp_brief:

    st.markdown("---")
    st.markdown("### 2️⃣ Lectura profesional de la conversación")

    st.write(st.session_state.rp_diagnostico)

    st.markdown("### 3️⃣ Estrategia sugerida (estructura Mentora en 4 pasos)")
    st.markdown(st.session_state.rp_estrategia)

    st.markdown("---")
    st.markdown("### 4️⃣ Roleplay en vivo")

    st.caption(
        "Ahora vas a practicar la conversación. Yo voy a representar a la otra persona. "
        "Escribí como hablarías en la vida real: directo, honesto, con el tono que elegiste."
    )

    # Inicializar primer mensaje del personaje
    if not st.session_state.rp_iniciado and client is not None:
        # primer turno: saludo / apertura del personaje
        st.session_state.rp_conversacion.append(
            {
                "role": "assistant",
                "content": "Hola, ¿qué querías hablar conmigo? Tengo un rato ahora.",
            }
        )
        st.session_state.rp_iniciado = True

    # Mostrar historial de conversación
    for msg in st.session_state.rp_conversacion:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.write(msg["content"])

    # Input del usuario
    if client is None:
        st.info("Configurá la API key de OpenAI para poder usar el roleplay en vivo.")
    else:
        user_input = st.chat_input("Escribí tu próximo mensaje en la conversación")

        if user_input:
            # agregar mensaje del usuario
            st.session_state.rp_conversacion.append(
                {"role": "user", "content": user_input.strip()}
            )

            # llamar modelo
            respuesta = llamar_modelo_roleplay(
                st.session_state.rp_brief,
                st.session_state.rp_conversacion,
            )

            st.session_state.rp_conversacion.append(
                {"role": "assistant", "content": respuesta}
            )
            st.rerun()

else:
    st.info("Primero completá el escenario de la conversación para generar la lectura y la estrategia.")
