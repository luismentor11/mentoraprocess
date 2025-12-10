import streamlit as st

# =========================
# CONFIGURACIÓN BÁSICA
# =========================
st.set_page_config(
    page_title="Mentora Process",
    page_icon="🧠",
    layout="centered"
)

# =========================
# INTRO MENTORA (AL HUESO)
# =========================
st.title("🧠 Mentora Process")
st.subheader("Diagnóstico del sistema humano de la empresa")
st.write(
    "Esta herramienta muestra cómo está funcionando hoy la empresa a nivel humano: "
    "liderazgo, roles, comunicación, clima interno y experiencia del cliente. "
    "El objetivo es darte un mapa claro, directo y accionable para ver qué está pasando "
    "y qué conviene ordenar primero."
)

# =========================
# CLASIFICACIÓN
# =========================
def clasificar_nivel(p):
    if p <= 2:
        return "Bajo"
    elif p <= 5:
        return "Medio"
    return "Alto"

# =========================
# FUNCIÓN PRINCIPAL
# =========================
def analizar_respuestas(r):
    familias = {
        "Poder y vínculos": 0,
        "Liderazgo y energía": 0,
        "Clima y conversaciones": 0,
        "Operación humana": 0,
        "Cliente como espejo": 0,
    }

    # --- Scoring resumido y efectivo ---
    if r["q1"] in ["Cansado pero comprometido", "Frustrado, siento que sostengo demasiado"]:
        familias["Liderazgo y energía"] += 3
    elif r["q1"] == "Ansioso, todo es urgente":
        familias["Liderazgo y energía"] += 2
        familias["Operación humana"] += 1
    elif r["q1"] == "Desconectado / a distancia":
        familias["Poder y vínculos"] += 2
        familias["Liderazgo y energía"] += 2

    if r["q3"] == "Esperás a ver si se acomoda solo":
        familias["Liderazgo y energía"] += 2
        familias["Clima y conversaciones"] += 1
    elif r["q3"] == "Buscás consenso para no quedar mal":
        familias["Poder y vínculos"] += 1
        familias["Clima y conversaciones"] += 1
    elif r["q3"] == "Te hacés cargo solo y seguís":
        familias["Liderazgo y energía"] += 2

    if r["q5"] == "Niño (reactiva)":
        familias["Clima y conversaciones"] += 2
        familias["Poder y vínculos"] += 1
    elif r["q5"] == "Adolescente (discute, desordena)":
        familias["Clima y conversaciones"] += 2
        familias["Liderazgo y energía"] += 1
    elif r["q5"] == "Adulto quemado (agotado)":
        familias["Liderazgo y energía"] += 2
        familias["Operación humana"] += 1

    if r["q6"] in ["Se habla tarde y con bronca", "Se chusmea por atrás", "No se habla, se acumula"]:
        familias["Clima y conversaciones"] += 3

    if r["q7"] in ["Yo hago lo que puedo", "No me pagan para pensar"]:
        familias["Clima y conversaciones"] += 2
        familias["Operación humana"] += 1
    if r["q7"] == "Si no estoy yo, esto no sale":
        familias["Liderazgo y energía"] += 2
        familias["Poder y vínculos"] += 1

    if r["q8"]:
        familias["Operación humana"] += 2
        familias["Clima y conversaciones"] += 1

    if r["q9"] == "Están claros, pero no se respetan":
        familias["Poder y vínculos"] += 1
        familias["Clima y conversaciones"] += 1
    elif r["q9"] in ["Son difusos", "Todos hacen un poco de todo"]:
        familias["Operación humana"] += 2

    if r["q11"] == "Buen trato, pero demoras":
        familias["Operación humana"] += 2
        familias["Cliente como espejo"] += 2
    elif r["q11"] == "Defensivo y tenso":
        familias["Cliente como espejo"] += 3
        familias["Clima y conversaciones"] += 2

    if r["q12"] == "Profesionales / técnicos":
        familias["Cliente como espejo"] += 2
        familias["Liderazgo y energía"] += 1
    elif r["q12"] == "Dirección":
        familias["Cliente como espejo"] += 1
        familias["Poder y vínculos"] += 1

    if r["q13"] == "No":
        familias["Poder y vínculos"] += 2
        familias["Operación humana"] += 1

    # CLASIFICACIÓN FINAL
    mapa = {k: clasificar_nivel(v) for k, v in familias.items()}
    dominante = max(familias, key=familias.get)

    # JUEGO HUMANO
    juegos = {
        "Poder y vínculos": "Hay decisiones que no se toman y roles que no están ordenados.",
        "Liderazgo y energía": "El liderazgo está sosteniendo demasiado, con desgaste y poca claridad.",
        "Clima y conversaciones": "Se evita hablar a tiempo y los temas se acumulan hasta explotar.",
        "Operación humana": "La empresa está en modo incendio: problemas repetidos y tiempos desordenados.",
        "Cliente como espejo": "El cliente recibe el impacto del desorden interno.",
    }
    juego = juegos[dominante]

    # ACCIONES CONCRETAS MENTORA
    focos = []

    if familias["Liderazgo y energía"] >= 3:
        focos.append("Definir las 3 decisiones que el liderazgo debe tomar en los próximos 30 días.")
    if familias["Clima y conversaciones"] >= 3:
        focos.append("Instalar un espacio semanal breve para conversaciones directas sin chisme.")
    if familias["Operación humana"] >= 3 or familias["Cliente como espejo"] >= 3:
        focos.append("Reordenar 1 punto crítico del recorrido del cliente para bajar tensión y errores.")

    if not focos:
        focos.append("Revisar acuerdos básicos y reforzar coherencia interna en tareas y comunicación.")

    # RESUMEN
    resumen = (
        "La empresa muestra tensiones que no vienen de lo técnico sino de cómo se organiza el sistema humano. "
        "Este mapa permite ver dónde se drena energía y qué ordenar primero."
    )

    return resumen, mapa, juego, focos

# =========================
# FORMULARIO
# =========================
with st.form("formulario"):

    q1 = st.selectbox("1. ¿Cómo te sentís liderando hoy?", [
        "Cansado pero comprometido",
        "Ansioso, todo es urgente",
        "Frustrado, siento que sostengo demasiado",
        "Con energía y claridad",
        "Desconectado / a distancia",
    ])

    q2 = st.text_area("2. ¿Qué decisión venís postergando?")

    q3 = st.selectbox("3. Cuando hay un problema serio:", [
        "Decidís rápido, aunque incomode",
        "Esperás a ver si se acomoda solo",
        "Buscás consenso para no quedar mal",
        "Te hacés cargo solo y seguís",
    ])

    q4 = st.text_area("4. ¿Qué comportamiento ya no deberías tolerar?")

    q5 = st.selectbox("5. Si la empresa fuera una persona, hoy sería:", [
        "Niño (reactiva)",
        "Adolescente (discute, desordena)",
        "Adulto quemado (agotado)",
        "Adulto claro (avanza)",
    ])

    q6 = st.selectbox("6. Cuando algo sale mal:", [
        "Se habla de frente y a tiempo",
        "Se habla tarde y con bronca",
        "Se chusmea por atrás",
        "No se habla, se acumula",
    ])

    q7 = st.selectbox("7. La frase más común es:", [
        "Acá siempre fue así",
        "Yo hago lo que puedo",
        "Si no estoy yo, esto no sale",
        "No me pagan para pensar",
        "Después vemos",
    ])

    q8 = st.text_input("8. ¿Quién recibe tensiones sin ser quien genera el problema?")

    q9 = st.selectbox("9. Roles y responsabilidades:", [
        "Están claros y se respetan",
        "Están claros, pero no se respetan",
        "Son difusos",
        "Todos hacen un poco de todo",
    ])

    q10 = st.text_area("10. ¿Qué tema evidente casi no se habla?")

    q11 = st.selectbox("11. En la atención al cliente se repite:", [
        "Buen trato, pero demoras",
        "Correcto, pero frío",
        "Defensivo y tenso",
        "Cálido y ordenado",
    ])

    q12 = st.selectbox("12. Cuando un cliente se queja, la bronca cae en:", [
        "Recepción / atención",
        "Área administrativa",
        "Profesionales / técnicos",
        "Dirección",
    ])

    q13 = st.selectbox("13. ¿Ese lugar genera el problema?", ["Sí", "No", "A veces"])

    q14 = st.text_area("14. Sensación que se lleva hoy el cliente:")

    q15 = st.text_area("15. Si el cliente viera la operación real, ¿qué confirmaría?")

    submit = st.form_submit_button("Generar diagnóstico")

# =========================
# RESULTADOS – FORMATO LISTO PARA ENVIAR
# =========================
if submit:
    respuestas = {
        "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5,
        "q6": q6, "q7": q7, "q8": q8, "q9": q9, "q10": q10,
        "q11": q11, "q12": q12, "q13": q13, "q14": q14, "q15": q15,
    }

    resumen, mapa, juego, focos = analizar_respuestas(respuestas)

    st.markdown("---")
    st.markdown("## 🧾 Informe Mentora Process — Listo para enviar al cliente")

    st.markdown("### 1. Lectura general")
    st.write(resumen)

    st.markdown("### 2. Mapa de dinámicas internas")
    for n, v in mapa.items():
        st.write(f"- **{n}:** {v}")

    st.markdown("### 3. Juego humano que hoy opera en la empresa")
    st.write(juego)

    st.markdown("### 4. Acciones concretas para los próximos 30 días")
    for i, foco in enumerate(focos, start=1):
        st.write(f"**{i}. {foco}**")

    st.markdown("### 5. Cierre")
    st.write(
        "Ordenar estas áreas permite mejorar coherencia interna, reducir desgaste y estabilizar la experiencia del cliente."
    )
