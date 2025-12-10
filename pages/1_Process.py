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
st.subheader("Diagnóstico del sistema humano de la empresa")
st.write(
    "Esta herramienta te ayuda a ver cómo está funcionando hoy la empresa a nivel humano: "
    "energía, vínculos, organización interna y experiencia del cliente. "
    "El objetivo es darte un mapa claro y acciones concretas para los próximos 30 días."
)

# =========================
# HELPERS
# =========================

def clasificar_nivel_bloque(p):
    if p <= 2:
        return "Bajo"
    elif p <= 5:
        return "Medio"
    return "Alto"


def clasificar_madurez(niveles):
    altos = sum(1 for n in niveles.values() if n == "Alto")
    medios = sum(1 for n in niveles.values() if n == "Medio")
    bajos = sum(1 for n in niveles.values() if n == "Bajo")

    if altos >= 3:
        nivel = "Nivel 1 – Sobrevivencia"
        descripcion = (
            "La empresa está funcionando en modo sobrevivencia. El sistema humano está saturado, "
            "los temas se apagan a último momento y hay poco espacio real para pensar y ordenar."
        )
    elif altos == 2 and medios >= 2:
        nivel = "Nivel 2 – Dependencia"
        descripcion = (
            "La empresa depende demasiado de pocas personas clave. El resto del sistema se adapta, "
            "pero con desgaste, confusión y tensiones crecientes."
        )
    elif altos <= 2 and medios >= 2:
        nivel = "Nivel 3 – Caos funcional"
        descripcion = (
            "La empresa funciona, pero con esfuerzo extra, repitiendo errores y sosteniendo tensiones "
            "que se podrían evitar si se ordenan algunas bases."
        )
    elif altos == 0 and medios >= 1:
        nivel = "Nivel 4 – Orden creciente"
        descripcion = (
            "La empresa está en un proceso de orden. Hay temas por trabajar, pero el sistema humano tiene "
            "base para sostener cambios y mejoras."
        )
    else:
        nivel = "Nivel 5 – Madurez humana"
        descripcion = (
            "La empresa muestra un nivel de madurez humana alto: se puede hablar, decidir y ordenar sin "
            "entrar en modo crisis permanente."
        )

    return nivel, descripcion


def generar_acciones(bloques_puntaje, niveles_bloque, nivel_madurez):
    acciones = []

    # bloque con más tensión
    bloque_mayor_tension = max(bloques_puntaje, key=bloques_puntaje.get)

    if bloque_mayor_tension == "Energía del sistema":
        acciones.append(
            "Definir y comunicar claramente qué temas NO se van a tomar en los próximos 30 días para bajar carga y recuperar energía."
        )
        acciones.append(
            "Acordar con el equipo 1 espacio fijo por semana (30 a 45 minutos) para revisar prioridades y sacar temas de la cabeza al papel."
        )
    elif bloque_mayor_tension == "Vínculos y comunicación":
        acciones.append(
            "Elegir 2 conversaciones pendientes importantes y ponerles fecha, formato y responsables para tenerlas en los próximos 30 días."
        )
        acciones.append(
            "Definir una regla básica de comunicación interna (por ejemplo: lo que se habla de alguien, se habla con esa persona)."
        )
    elif bloque_mayor_tension == "Organización y claridad":
        acciones.append(
            "Definir por escrito qué corresponde y qué no corresponde a cada rol clave, y revisarlo con las personas involucradas."
        )
        acciones.append(
            "Detectar 1 error repetido en la operación y documentar un paso a paso simple para reducirlo o evitarlo."
        )
    else:  # Cliente como espejo
        acciones.append(
            "Mapear 1 recorrido típico del cliente (desde que entra en contacto hasta que se va) y marcar dónde se genera más fricción o demora."
        )
        acciones.append(
            "Acordar una respuesta estándar clara y simple para las quejas más frecuentes de los clientes."
        )

    # acción extra si la madurez es baja
    if "Nivel 1" in nivel_madurez or "Nivel 2" in nivel_madurez:
        acciones.append(
            "Poner en agenda una reunión de revisión general del sistema humano (no de números), para ordenar decisiones y prioridades."
        )

    return acciones


# =========================
# FORMULARIO
# =========================

with st.form("diagnostico_mentora_process"):

    st.markdown("### 1️⃣ Punto de partida")

    rol = st.selectbox(
        "¿Cuál es tu rol principal en la empresa?",
        [
            "Dirección / Socio / Gerencia",
            "Liderazgo intermedio / Coordinación",
            "Equipo operativo / Administrativo",
            "Atención al cliente / Recepción",
            "Profesional / Técnico",
            "Otro",
        ],
    )

    puerta = st.selectbox(
        "¿Qué describe mejor lo que está pasando hoy?",
        [
            "Desgaste / cansancio en quienes sostienen la empresa",
            "Tensión interna / roces / conversaciones pendientes",
            "Operación pesada / lenta / desordenada",
            "Clientes incómodos / quejas / mala experiencia",
            "No tengo claro qué pasa, pero algo está trabado",
        ],
    )

    ejemplo_situacion = st.text_area(
        "Contá brevemente una situación concreta que para vos represente lo que está pasando:",
        placeholder="Ejemplo: discusiones entre socios, quejas en recepción, tareas que siempre se hacen a último momento, etc.",
    )

    st.markdown("### 2️⃣ Energía del sistema")

    q_ene_1 = st.selectbox(
        "¿Cómo describirías la energía general de la empresa en el día a día?",
        [
            "Liviana y ordenada",
            "Cambia según el día",
            "Pesada, con cansancio acumulado",
            "Tensa, todo es urgente",
        ],
    )

    q_ene_2 = st.selectbox(
        "En relación a decisiones importantes:",
        [
            "Se toman a tiempo y se comunican",
            "Se demoran un poco, pero salen",
            "Se estiran hasta que explota algo",
            "Se patean o se evitan",
        ],
    )

    st.markdown("### 3️⃣ Vínculos y comunicación interna")

    q_vin_1 = st.selectbox(
        "Cuando hay un conflicto o algo molesta:",
        [
            "Se habla directo y a tiempo",
            "Se habla, pero tarde",
            "Se comenta por atrás",
            "No se habla, se acumula",
        ],
    )

    q_vin_2 = st.selectbox(
        "En el equipo, lo que más se ve es:",
        [
            "Colaboración y apoyo",
            "Buen trato, pero con chistes o comentarios irónicos",
            "Grupos separados o bandos",
            "Personas que trabajan aisladas o a la defensiva",
        ],
    )

    st.markdown("### 4️⃣ Organización y claridad")

    q_org_1 = st.selectbox(
        "Respecto a roles y responsabilidades:",
        [
            "Están claros y se respetan",
            "Están claros, pero no siempre se respetan",
            "Hay zonas grises, no está tan claro",
            "Cada uno hace un poco de todo para apagar incendios",
        ],
    )

    q_org_2 = st.selectbox(
        "Sobre errores y problemas que se repiten:",
        [
            "Son pocos y se corrigen rápido",
            "Aparecen cada tanto",
            "Se repiten seguido",
            "Ya son parte del funcionamiento normal",
        ],
    )

    st.markdown("### 5️⃣ Cliente como espejo del sistema")

    q_cli_1 = st.selectbox(
        "La experiencia típica del cliente hoy es:",
        [
            "Fluida y ordenada",
            "Buena, pero con demoras o desprolijidades",
            "Correcta, pero fría o distante",
            "Irregular, con quejas o enojos frecuentes",
        ],
    )

    q_cli_2 = st.selectbox(
        "Cuando un cliente se queja o se enoja:",
        [
            "Es algo puntual y se resuelve",
            "Pasa cada tanto y genera tensión",
            "Pasa seguido y desgasta al equipo",
            "Se volvió algo normal en el día a día",
        ],
    )

    submit = st.form_submit_button("Generar diagnóstico Mentora Process")

# =========================
# PROCESAMIENTO
# =========================

if submit:
    bloques_puntaje = {
        "Energía del sistema": 0,
        "Vínculos y comunicación": 0,
        "Organización y claridad": 0,
        "Cliente como espejo": 0,
    }

    # puerta / síntoma
    if puerta == "Desgaste / cansancio en quienes sostienen la empresa":
        bloques_puntaje["Energía del sistema"] += 2
    elif puerta == "Tensión interna / roces / conversaciones pendientes":
        bloques_puntaje["Vínculos y comunicación"] += 2
    elif puerta == "Operación pesada / lenta / desordenada":
        bloques_puntaje["Organización y claridad"] += 2
    elif puerta == "Clientes incómodos / quejas / mala experiencia":
        bloques_puntaje["Cliente como espejo"] += 2
    else:
        bloques_puntaje["Energía del sistema"] += 1
        bloques_puntaje["Vínculos y comunicación"] += 1
        bloques_puntaje["Organización y claridad"] += 1
        bloques_puntaje["Cliente como espejo"] += 1

    # energía
    if q_ene_1 == "Liviana y ordenada":
        bloques_puntaje["Energía del sistema"] += 0
    elif q_ene_1 == "Cambia según el día":
        bloques_puntaje["Energía del sistema"] += 1
    elif q_ene_1 == "Pesada, con cansancio acumulado":
        bloques_puntaje["Energía del sistema"] += 2
    else:
        bloques_puntaje["Energía del sistema"] += 3

    if q_ene_2 == "Se toman a tiempo y se comunican":
        bloques_puntaje["Energía del sistema"] += 0
    elif q_ene_2 == "Se demoran un poco, pero salen":
        bloques_puntaje["Energía del sistema"] += 1
    elif q_ene_2 == "Se estiran hasta que explota algo":
        bloques_puntaje["Energía del sistema"] += 2
    else:
        bloques_puntaje["Energía del sistema"] += 3

    # vínculos
    if q_vin_1 == "Se habla directo y a tiempo":
        bloques_puntaje["Vínculos y comunicación"] += 0
    elif q_vin_1 == "Se habla, pero tarde":
        bloques_puntaje["Vínculos y comunicación"] += 1
    elif q_vin_1 == "Se comenta por atrás":
        bloques_puntaje["Vínculos y comunicación"] += 2
    else:
        bloques_puntaje["Vínculos y comunicación"] += 3

    if q_vin_2 == "Colaboración y apoyo":
        bloques_puntaje["Vínculos y comunicación"] += 0
    elif q_vin_2 == "Buen trato, pero con chistes o comentarios irónicos":
        bloques_puntaje["Vínculos y comunicación"] += 1
    elif q_vin_2 == "Grupos separados o bandos":
        bloques_puntaje["Vínculos y comunicación"] += 2
    else:
        bloques_puntaje["Vínculos y comunicación"] += 3

    # organización
    if q_org_1 == "Están claros y se respetan":
        bloques_puntaje["Organización y claridad"] += 0
    elif q_org_1 == "Están claros, pero no siempre se respetan":
        bloques_puntaje["Organización y claridad"] += 1
    elif q_org_1 == "Hay zonas grises, no está tan claro":
        bloques_puntaje["Organización y claridad"] += 2
    else:
        bloques_puntaje["Organización y claridad"] += 3

    if q_org_2 == "Son pocos y se corrigen rápido":
        bloques_puntaje["Organización y claridad"] += 0
    elif q_org_2 == "Aparecen cada tanto":
        bloques_puntaje["Organización y claridad"] += 1
    elif q_org_2 == "Se repiten seguido":
        bloques_puntaje["Organización y claridad"] += 2
    else:
        bloques_puntaje["Organización y claridad"] += 3

    # cliente
    if q_cli_1 == "Fluida y ordenada":
        bloques_puntaje["Cliente como espejo"] += 0
    elif q_cli_1 == "Buena, pero con demoras o desprolijidades":
        bloques_puntaje["Cliente como espejo"] += 1
    elif q_cli_1 == "Correcta, pero fría o distante":
        bloques_puntaje["Cliente como espejo"] += 2
    else:
        bloques_puntaje["Cliente como espejo"] += 3

    if q_cli_2 == "Es algo puntual y se resuelve":
        bloques_puntaje["Cliente como espejo"] += 0
    elif q_cli_2 == "Pasa cada tanto y genera tensión":
        bloques_puntaje["Cliente como espejo"] += 1
    elif q_cli_2 == "Pasa seguido y desgasta al equipo":
        bloques_puntaje["Cliente como espejo"] += 2
    else:
        bloques_puntaje["Cliente como espejo"] += 3

    # niveles por bloque
    niveles_bloque = {
        nombre: clasificar_nivel_bloque(p) for nombre, p in bloques_puntaje.items()
    }

    # nivel de madurez
    nivel_madurez, descripcion_madurez = clasificar_madurez(niveles_bloque)

    resumen_global = (
        "La lectura se hace sobre el sistema humano de la empresa, no sobre personas aisladas. "
        "Los resultados muestran en qué áreas se concentra hoy la tensión y qué conviene ordenar primero."
    )

    acciones = generar_acciones(bloques_puntaje, niveles_bloque, nivel_madurez)

    # =========================
    # INFORME
    # =========================
    st.markdown("---")
    st.markdown("## 🧾 Informe Mentora Process – Versión beta")

    st.markdown("### 1. Datos de contexto")
    st.write(f"- Rol de quien responde: **{rol}**")
    st.write(f"- Puerta de entrada al diagnóstico: **{puerta}**")
    if ejemplo_situacion.strip():
        st.write("Situación representativa:")
        st.write(f"“{ejemplo_situacion.strip()}”")

    st.markdown("### 2. Lectura general del sistema humano")
    st.write(resumen_global)

    st.markdown("### 3. Mapa por bloques")
    for nombre, nivel in niveles_bloque.items():
        st.write(f"- **{nombre}:** {nivel}")

    st.markdown("### 4. Nivel de madurez humana de la empresa")
    st.write(f"**{nivel_madurez}**")
    st.write(descripcion_madurez)

    st.markdown("### 5. Acciones sugeridas para los próximos 30 días")
    for i, accion in enumerate(acciones, start=1):
        st.write(f"{i}. {accion}")

    st.markdown("### 6. Nota para el consultor")
    st.caption(
        "Este informe es una base de lectura. Las sesiones y encuentros se diseñan aparte, "
        "a partir de la realidad específica de la empresa."
    )
