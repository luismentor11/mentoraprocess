import streamlit as st

# =========================
# CONFIGURACIÓN BÁSICA
# =========================
st.set_page_config(
    page_title="Mentora Process",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Mentora Process")
st.subheader("Diagnóstico de quilombos humanos en empresas que ya funcionan")
st.write(
    "Este diagnóstico NO analiza ventas, marketing ni sistemas. "
    "Se enfoca exclusivamente en liderazgo, vínculos, clima, conversaciones, "
    "operación humana y experiencia del cliente."
)

# =========================
# SYSTEM PROMPT (para usar con IA si querés luego)
# =========================
SYSTEM_PROMPT = (
    "Sos MENTORA PROCESS, un sistema de diagnóstico humano y sistémico para empresas que ya funcionan.\n"
    "\n"
    "Tu rol NO es:\n"
    "- analizar ventas,\n"
    "- proponer marketing,\n"
    "- evaluar facturación,\n"
    "- diseñar sistemas técnicos.\n"
    "\n"
    "Tu rol ES:\n"
    "- detectar patrones humanos dentro de la empresa,\n"
    "- identificar dónde nace el conflicto real aunque explote en otro lugar,\n"
    "- leer liderazgo, vínculos, clima emocional, conversaciones y experiencia humana del cliente.\n"
    "\n"
    "Trabajás siempre desde el enfoque Mentora:\n"
    "- coaching ontológico,\n"
    "- lectura sistémica,\n"
    "- responsabilidad individual y organizacional,\n"
    "- lenguaje claro y directo, sin eufemismos ni humo.\n"
    "\n"
    "Utilizás como marco las 5 familias de quilombos humanos:\n"
    "1. Poder y vínculos de base\n"
    "2. Liderazgo y energía\n"
    "3. Cultura, clima y conversaciones\n"
    "4. Operación humana y gestión del tiempo\n"
    "5. Cliente como espejo del sistema interno\n"
    "\n"
    "Reglas obligatorias:\n"
    "- Nunca hables de ventas, marketing, facturación ni tecnología.\n"
    "- No des soluciones técnicas.\n"
    "- No culpes personas: señalá roles y patrones.\n"
    "- Señalá el origen real del quilombo, aunque sea incómodo.\n"
    "- Usá lenguaje claro, firme y respetuoso.\n"
    "\n"
    "La salida del diagnóstico debe incluir siempre:\n"
    "1. Lectura global del sistema.\n"
    "2. Clasificación de las 5 familias (Bajo / Medio / Alto).\n"
    "3. Identificación del juego oculto que está operando.\n"
    "4. Propuesta de 2 o 3 focos de trabajo Mentora.\n"
    "\n"
    "Tu objetivo no es agradar.\n"
    "Tu objetivo es ordenar conciencia y responsabilidad.\n"
)

# =========================
# FUNCIÓN DE CLASIFICACIÓN
# =========================

def clasificar_nivel(puntaje: int) -> str:
    """Convierte un puntaje numérico en Bajo / Medio / Alto."""
    if puntaje <= 2:
        return "Bajo"
    elif puntaje <= 5:
        return "Medio"
    else:
        return "Alto"


# =========================
# FUNCIÓN PRINCIPAL DE ANÁLISIS
# =========================

def analizar_respuestas(r):
    familias = {
        "Poder y vínculos de base": 0,
        "Liderazgo y energía": 0,
        "Cultura, clima y conversaciones": 0,
        "Operación humana y tiempo": 0,
        "Cliente como espejo": 0,
    }

    # === REGLAS HEURÍSTICAS (scoring) ===

    # Pregunta 1
    if r["q1"] in ["Cansado pero comprometido", "Frustrado, siento que sostengo demasiado"]:
        familias["Liderazgo y energía"] += 3
    elif r["q1"] == "Ansioso, todo es urgente":
        familias["Liderazgo y energía"] += 2
        familias["Operación humana y tiempo"] += 1
    elif r["q1"] == "Desconectado / a distancia":
        familias["Poder y vínculos de base"] += 2
        familias["Liderazgo y energía"] += 2
    elif r["q1"] == "Con energía y claridad":
        familias["Liderazgo y energía"] += 1

    # Pregunta 3
    if r["q3"] == "Decidís rápido, aunque incomode":
        familias["Liderazgo y energía"] += 1
    elif r["q3"] == "Esperás a ver si se acomoda solo":
        familias["Liderazgo y energía"] += 2
        familias["Cultura, clima y conversaciones"] += 1
    elif r["q3"] == "Buscás consenso para no quedar mal":
        familias["Poder y vínculos de base"] += 1
        familias["Cultura, clima y conversaciones"] += 1
    elif r["q3"] == "Te hacés cargo solo y seguís":
        familias["Liderazgo y energía"] += 2

    # Pregunta 5
    if r["q5"] == "Niño (reactiva, se queja, depende)":
        familias["Cultura, clima y conversaciones"] += 2
        familias["Poder y vínculos de base"] += 1
    elif r["q5"] == "Adolescente (discute, se rebela, desordena)":
        familias["Cultura, clima y conversaciones"] += 2
        familias["Liderazgo y energía"] += 1
    elif r["q5"] == "Adulto quemado (funciona, pero agotado)":
        familias["Liderazgo y energía"] += 2
        familias["Operación humana y tiempo"] += 1
    elif r["q5"] == "Adulto claro (decide y avanza)":
        familias["Liderazgo y energía"] += 1

    # Pregunta 6
    if r["q6"] == "Se habla de frente y a tiempo":
        familias["Cultura, clima y conversaciones"] += 1
    elif r["q6"] in ["Se habla tarde y con bronca", "Se chusmea por atrás", "No se habla, se acumula"]:
        familias["Cultura, clima y conversaciones"] += 3

    # Pregunta 7
    if r["q7"] in ["Acá siempre fue así", "Después vemos"]:
        familias["Cultura, clima y conversaciones"] += 2
    if r["q7"] in ["Yo hago lo que puedo", "No me pagan para pensar"]:
        familias["Cultura, clima y conversaciones"] += 2
        familias["Operación humana y tiempo"] += 1
    if r["q7"] == "Si no estoy yo, esto no sale":
        familias["Liderazgo y energía"] += 2
        familias["Poder y vínculos de base"] += 1

    # Pregunta 8
    if r["q8"]:
        familias["Operación humana y tiempo"] += 2
        familias["Cultura, clima y conversaciones"] += 1

    # Pregunta 9
    if r["q9"] == "Están claros, pero no se respetan":
        familias["Poder y vínculos de base"] += 1
        familias["Cultura, clima y conversaciones"] += 1
    elif r["q9"] == "Son difusos":
        familias["Operación humana y tiempo"] += 2
    elif r["q9"] == "Todos hacen un poco de todo":
        familias["Operación humana y tiempo"] += 2
        familias["Liderazgo y energía"] += 1

    # Pregunta 11
    if r["q11"] == "Buen trato, pero demoras":
        familias["Operación humana y tiempo"] += 2
        familias["Cliente como espejo"] += 2
    elif r["q11"] == "Correcto, pero frío":
        familias["Cliente como espejo"] += 2
        familias["Cultura, clima y conversaciones"] += 1
    elif r["q11"] == "Defensivo y tenso":
        familias["Cliente como espejo"] += 3
        familias["Cultura, clima y conversaciones"] += 2
    elif r["q11"] == "Cálido y ordenado":
        familias["Cliente como espejo"] += 1

    # Pregunta 12
    if r["q12"] == "Recepción / atención":
        familias["Cliente como espejo"] += 2
        familias["Operación humana y tiempo"] += 1
    elif r["q12"] == "Área administrativa":
        familias["Cliente como espejo"] += 2
    elif r["q12"] == "Profesionales / técnicos":
        familias["Cliente como espejo"] += 2
        familias["Liderazgo y energía"] += 1
    elif r["q12"] == "Dirección":
        familias["Cliente como espejo"] += 1
        familias["Poder y vínculos de base"] += 1

    # Pregunta 13
    if r["q13"] == "No":
        familias["Poder y vínculos de base"] += 2
        familias["Operación humana y tiempo"] += 1

    # === CLASIFICACIÓN ===
    mapa_clasificado = {nombre: clasificar_nivel(p) for nombre, p in familias.items()}
    familia_predominante = max(familias, key=familias.get)

    # === JUEGO OCULTO ===
    if familia_predominante == "Poder y vínculos de base":
        juego_oculto = (
            "Las reglas reales de poder y los vínculos de base no están ordenados. "
            "Hay decisiones que se patean o se negocian por debajo, y el sistema "
            "prefiere evitar conflictos antes que ordenar responsabilidades."
        )
    elif familia_predominante == "Liderazgo y energía":
        juego_oculto = (
            "El liderazgo está sosteniendo desde el cansancio, la ansiedad o la sobrecarga. "
            "Se toman decisiones tarde, se toleran comportamientos que ya no cierran y "
            "el mensaje implícito es 'aguantemos como se pueda'."
        )
    elif familia_predominante == "Cultura, clima y conversaciones":
        juego_oculto = (
            "La cultura permite chisme, descarga y evasión en lugar de conversaciones directas. "
            "Lo que todos ven no se nombra a tiempo, y las emociones se acumulan hasta explotar."
        )
    elif familia_predominante == "Operación humana y tiempo":
        juego_oculto = (
            "La operación humana vive en modo incendio: roles difusos, tiempos desordenados "
            "y acuerdos que no se sostienen. El sistema gestiona tarde, corriendo detrás de los problemas."
        )
    else:
        juego_oculto = (
            "La experiencia del cliente está recibiendo el impacto del desorden interno. "
            "La bronca y el desgaste se descargan en la atención, y el cliente siente "
            "la incoherencia entre lo que se promete y lo que se vive."
        )

    # === FOCOS DE TRABAJO ===
    focos = []

    if familias["Liderazgo y energía"] >= 3:
        focos.append(
            "Ordenar el juego interno del liderazgo: definir qué ya no se va a tolerar, "
            "qué decisiones se van a tomar en los próximos 30 días y cómo se va a sostener esa coherencia."
        )

    if familias["Cultura, clima y conversaciones"] >= 3:
        focos.append(
            "Crear un espacio fijo para conversaciones francas (sin chisme): "
            "nombrar lo que todos ven, trabajar acuerdos nuevos y revisar compromisos."
        )

    if familias["Operación humana y tiempo"] >= 3 or familias["Cliente como espejo"] >= 3:
        focos.append(
            "Mapear 1 o 2 momentos críticos del recorrido del cliente (como recepción o esperas) "
            "y alinear tiempos, límites y forma de comunicar para que la bronca no caiga siempre en el lugar equivocado."
        )

    if not focos:
        focos.append(
            "Consolidar lo que ya funciona: mantener espacios de conversación, cuidar la energía del liderazgo "
            "y reforzar la coherencia entre cómo se tratan internamente y cómo tratan al cliente."
        )

    resumen_global = (
        "Este diagnóstico no habla de ventas ni de marketing. "
        "Muestra cómo está hoy el juego humano dentro de la empresa y cómo ese juego "
        "impacta en el equipo y en la experiencia del cliente."
    )

    return resumen_global, mapa_clasificado, juego_oculto, focos



# =========================
# FORMULARIO EN STREAMLIT
# =========================

with st.form("diagnostico_mentora_process"):
    st.markdown("### 1️⃣ Líder / Dirección")

    q1 = st.selectbox(
        "1. Hoy, ¿cómo te sentís liderando la empresa?",
        [
            "Cansado pero comprometido",
            "Ansioso, todo es urgente",
            "Frustrado, siento que sostengo demasiado",
            "Con energía y claridad",
            "Desconectado / a distancia",
        ],
    )

    q2 = st.text_area(
        "2. ¿Qué decisión importante sabés que deberías tomar y venís postergando?",
        placeholder="Personas, límites, estructura, responsabilidades, tiempos…",
    )

    q3 = st.selectbox(
        "3. Cuando hay un problema serio, normalmente vos:",
        [
            "Decidís rápido, aunque incomode",
            "Esperás a ver si se acomoda solo",
            "Buscás consenso para no quedar mal",
            "Te hacés cargo solo y seguís",
        ],
    )

    q4 = st.text_area(
        "4. ¿Qué comportamiento dentro de la empresa ya sabés que no debería seguir tolerándose?",
        placeholder="Ejemplo: impuntualidad crónica, malos tratos, falta de compromiso…",
    )

    q5 = st.selectbox(
        "5. Si la empresa fuera una persona, hoy estaría en modo:",
        [
            "Niño (reactiva, se queja, depende)",
            "Adolescente (discute, se rebela, desordena)",
            "Adulto quemado (funciona, pero agotado)",
            "Adulto claro (decide y avanza)",
        ],
    )

    st.markdown("### 2️⃣ Equipo / Sistema interno")

    q6 = st.selectbox(
        "6. Cuando algo sale mal en el equipo, lo que suele pasar primero es:",
        [
            "Se habla de frente y a tiempo",
            "Se habla tarde y con bronca",
            "Se chusmea por atrás",
            "No se habla, se acumula",
        ],
    )

    q7 = st.selectbox(
        "7. ¿Qué frase escuchás más seguido en el día a día?",
        [
            "Acá siempre fue así",
            "Yo hago lo que puedo",
            "Si no estoy yo, esto no sale",
            "No me pagan para pensar",
            "Después vemos",
        ],
    )

    q8 = st.text_input(
        "8. ¿Quién es la persona o área que más recibe quejas o tensiones sin ser quien genera el problema?",
        placeholder="Ejemplo: recepción, administración…",
    )

    q9 = st.selectbox(
        "9. Respecto a los roles y responsabilidades:",
        [
            "Están claros y se respetan",
            "Están claros, pero no se respetan",
            "Son difusos",
            "Todos hacen un poco de todo",
        ],
    )

    q10 = st.text_area(
        "10. ¿Qué tema es evidente para todos pero casi nunca se habla en serio?",
        placeholder="Ejemplo: un socio que no aporta, alguien intocable, un problema crónico…",
    )

    st.markdown("### 3️⃣ Cliente / Experiencia humana")

    q11 = st.selectbox(
        "11. En la atención al cliente, lo que más se repite hoy es:",
        [
            "Buen trato, pero demoras",
            "Correcto, pero frío",
            "Defensivo y tenso",
            "Cálido y ordenado",
        ],
    )

    q12 = st.selectbox(
        "12. Cuando un cliente se enoja o se queja, generalmente la bronca cae en:",
        [
            "Recepción / atención",
            "Área administrativa",
            "Profesionales / técnicos",
            "Dirección",
        ],
    )

    q13 = st.selectbox(
        "13. ¿Ese lugar que recibe la bronca es también el que genera el problema?",
        [
            "Sí",
            "No",
            "A veces",
        ],
    )

    q14 = st.text_area(
        "14. ¿Qué sensación creés que el cliente se lleva hoy después de interactuar con la empresa?",
        placeholder="Ejemplo: cuidado, estrés, desorden, calidez, desconfianza…",
    )

    q15 = st.text_area(
        "15. Si el cliente pudiera ver un día de trabajo puertas adentro, ¿se sorprendería o confirmaría lo que ya siente?",
        placeholder="¿Qué vería? ¿Qué confirmaría?",
    )

    submitted = st.form_submit_button("Generar diagnóstico Mentora Process")

if submitted:
    respuestas = {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q4": q4,
        "q5": q5,
        "q6": q6,
        "q7": q7,
        "q8": q8,
        "q9": q9,
        "q10": q10,
        "q11": q11,
        "q12": q12,
        "q13": q13,
        "q14": q14,
        "q15": q15,
    }

    resumen_global, mapa_familias, juego_oculto, focos = analizar_respuestas(respuestas)

    st.markdown("---")
    st.markdown("## 🧾 Resultado del diagnóstico")

    st.write(resumen_global)

    st.markdown("### 🔍 Mapa Mentora – Familias de quilombos")
    for nombre, nivel in mapa_familias.items():
        st.write(f"- **{nombre}:** {nivel}")

    st.markdown("### 🎭 Juego oculto que está operando")
    st.write(juego_oculto)

    st.markdown("### 🎯 Focos de trabajo Mentora sugeridos")
    for i, foco in enumerate(focos, start=1):
        st.write(f"{i}. {foco}")

    st.markdown("—")
    st.caption(
        "Este resultado no reemplaza una conversación profunda. "
        "Es un mapa inicial para decidir por dónde empezar a ordenar el juego humano."
    )
