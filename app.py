import os
import textwrap
from datetime import datetime

import streamlit as st

# =========================
# CONFIG BÁSICA DE LA APP
# =========================

APP_NAME = "Mentora Process"
PAGE_TITLE = f"{APP_NAME} – Diagnóstico de Liderazgo, Procesos y Cliente"
PAGE_ICON = "🧠"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered")

# =========================
# DATA: BLOQUES Y DOLORES
# =========================

BLOCKS = {
    "Orden & Crecimiento": {
        "icon": "🧩",
        "description": "Cuando la empresa crece, pero el orden no acompaña.",
        "issues": [
            "Estamos creciendo y esto es un caos",
            "Cada área hace lo que quiere",
            "El dueño está en todo",
            "Queremos vender la empresa / atraer inversores",
            "Queremos automatizar, pero primero ordenar",
        ],
    },
    "Personas & Productividad": {
        "icon": "👥",
        "description": "Personas clave, equipos saturados y productividad real.",
        "issues": [
            "Dependo de 2 personas clave y si se van, me fundo",
            "Tengo gente ocupada pero no productiva",
            "Cada vez que entra alguien nuevo es un parto",
        ],
    },
    "Experiencia del Cliente & Calidad": {
        "icon": "⭐",
        "description": "Clientes que se van, errores y calidad de servicio.",
        "issues": [
            "Perdemos clientes y no sabemos por qué",
            "Cumplimos mal, tarde o con errores",
        ],
    },
    "Tecnología & Automatización": {
        "icon": "💻",
        "description": "Sistemas, herramientas y automatización que funcionen de verdad.",
        "issues": [
            "Quiero escalar sin contratar más gente",
            "Tenemos software pero no lo usamos bien",
        ],
    },
}

# Preguntas generales tipo "Juego Oculto" pero en lenguaje empresa
GENERAL_QUESTIONS = [
    "¿Cuál es hoy el principal dolor o preocupación que tenés respecto a tu empresa o equipo?",
    "Si este problema siguiera igual durante 12 meses, ¿qué impacto tendría en resultados, personas y clientes?",
    "¿Qué conversaciones difíciles sentís que se vienen pateando hace tiempo (y con quién)?",
    "¿Qué hacés normalmente cuando hay conflicto o algo sale mal? ¿Callás, explotás, culpás, te hacés cargo de todo, otra cosa?",
    "En pocas palabras, ¿qué te gustaría que sea distinto en 3 a 6 meses si este proceso funciona?",
]

# Preguntas adicionales por bloque (afinando el diagnóstico individual)
BLOCK_SPECIFIC_QUESTIONS = {
    "Orden & Crecimiento": [
        "¿En qué parte sentís más el caos hoy? (ej: coordinación entre áreas, prioridades, decisiones, reuniones, etc.)",
        "¿Qué cosas hoy dependen sí o sí del dueño o de 1–2 personas clave?",
    ],
    "Personas & Productividad": [
        "¿Qué comportamientos ves en tu equipo que te hacen sentir que están ocupados pero no necesariamente produciendo?",
        "¿Cómo es hoy el proceso de incorporar a alguien nuevo? Contá brevemente los pasos y dónde se traba.",
    ],
    "Experiencia del Cliente & Calidad": [
        "¿En qué momentos se rompen más las cosas con el cliente? (inicio, entregas, postventa, reclamos, etc.)",
        "Si le preguntáramos a tus mejores clientes qué los frustra de tu empresa, ¿qué creés que dirían?",
    ],
    "Tecnología & Automatización": [
        "¿Qué herramientas o sistemas usan hoy (nombre y para qué)?",
        "¿Cuál es la mayor bronca que tenés hoy con la tecnología en tu empresa?",
    ],
}

# =========================
# FUNCIÓN PARA ARMAR PROMPT INDIVIDUAL
# =========================

def build_prompt_individual(block_name, selected_issues, context_answers):
    block = BLOCKS[block_name]
    today = datetime.now().strftime("%Y-%m-%d")

    intro = textwrap.dedent(f"""
    Actuás como un consultor senior en mejora de procesos, liderazgo y experiencia del cliente,
    especialista en pymes y empresas en crecimiento. Tenés un enfoque claro, directo y ejecutivo.

    El contexto es la herramienta llamada “Mentora Process”, que combina diagnóstico de procesos
    visibles con lectura de patrones invisibles en la forma de dirigir, decidir y conversar en la empresa.

    Tu tarea:
    - Analizar la situación de la empresa/líder desde esta mirada individual.
    - Detectar patrones de liderazgo, comunicación y procesos.
    - Traducir esto a un INFORME EJECUTIVO claro y accionable.
    - Incluir una propuesta de trabajo a abordar con un coach ejecutivo humano (Luis Yañez).

    FECHA DEL INFORME: {today}
    TIPO DE USO: Diagnóstico individual
    BLOQUE PRINCIPAL: {block_name} – {block['description']}

    DOLENCIAS PRINCIPALES QUE LA PERSONA MARCÓ:
    """).strip()

    issues_text = "\n".join([f"- {issue}" for issue in selected_issues])

    answers_text = "\n\nRESPUESTAS DEL USUARIO:\n"
    for label, answer in context_answers.items():
        answers_text += f"\n{label}:\n{answer.strip()}\n"

    instructions = textwrap.dedent("""
    Estructura del informe que tenés que devolver (en español, tono ejecutivo, claro y directo):

    1. Resumen ejecutivo
       - 3 a 5 bullet points con los hallazgos clave.
       - Nivel de riesgo percibido en comunicación y procesos (bajo / medio / alto) y por qué.

    2. Patrones de liderazgo, comunicación y procesos
       - Describir los patrones que observás (ej: dependencia del dueño, caos por crecimiento, tolerancia a la informalidad, evitar conflicto, etc.).
       - Explicar cómo estos patrones impactan en resultados, equipo y cliente.

    3. Impacto en experiencia del cliente y en el negocio
       - Cómo se traduce esto en la experiencia del cliente (consistencia, tiempos, errores, etc.).
       - Riesgos: legales, operativos, de rotación, de pérdida de clientes, etc.

    4. Oportunidades y focos de mejora
       - 3 a 5 focos concretos (ej: clarificar rol del dueño, ordenar procesos entre áreas, estructurar onboarding, usar mejor el software, etc.).
       - Explicar brevemente cada foco (qué cambiaría y qué beneficio traería).

    5. Propuesta de trabajo con coach ejecutivo
       - Proponer entre 3 y 6 encuentros/sesiones con objetivo por sesión.
       - Aclarar que este informe es un punto de partida y que el proceso se profundiza con acompañamiento humano.

    6. Nota de límites
       - Aclarar que esto no reemplaza asesoría legal, contable ni procesos terapéuticos.

    Cerrá SIEMPRE el informe con algo como:
    "Este informe fue generado con Mentora Process (IA) y está pensado para ser trabajado junto a
    un coach ejecutivo humano, como parte de un proceso de mejora continua."
    """).strip()

    full_prompt = f"{intro}\n{issues_text}\n\n{answers_text}\n\n{instructions}"
    return full_prompt

# =========================
# FUNCIÓN PARA ARMAR PROMPT EQUIPO
# =========================

def build_prompt_team(block_name, selected_issues, team_name, team_raw_input, leader_view):
    block = BLOCKS[block_name]
    today = datetime.now().strftime("%Y-%m-%d")

    intro = textwrap.dedent(f"""
    Actuás como un consultor senior en cultura, procesos y liderazgo,
    especialista en empresas donde hay tensión entre áreas, personas y resultados.

    Estás usando la herramienta “Mentora Process” en MODO EQUIPO.
    Recibiste distintas versiones del mismo problema, contadas por varios integrantes de un equipo.

    Tu tarea:
    - Leer esas versiones como si fueran "capas del mismo lío".
    - Detectar patrones compartidos y contradicciones.
    - Identificar juegos de poder, silencios, culpas y puntos ciegos (sin usar lenguaje terapéutico).
    - Traducir todo en un INFORME EJECUTIVO de diagnóstico de equipo.
    - Proponer focos de trabajo que luego se profundizan con el coach humano (Luis Yañez).

    FECHA DEL INFORME: {today}
    TIPO DE USO: Síntesis de equipo
    EQUIPO / ÁREA: {team_name if team_name else "No especificado"}
    BLOQUE PRINCIPAL: {block_name} – {block['description']}

    DOLENCIAS PRINCIPALES MARCADAS PARA ESTE EQUIPO:
    """).strip()

    issues_text = "\n".join([f"- {issue}" for issue in selected_issues])

    team_text = textwrap.dedent(f"""
    VERSIONES DEL EQUIPO (copiadas tal cual o resumidas):

    {team_raw_input.strip()}

    MIRADA DEL LÍDER / DUEÑO / RESPONSABLE:

    {leader_view.strip()}
    """)

    instructions = textwrap.dedent("""
    Estructura del informe de equipo (en español, tono ejecutivo, claro y directo):

    1. Resumen ejecutivo del conflicto / lío
       - 3 a 7 bullets que expliquen qué está pasando en el equipo.
       - Incluir dónde se traba, qué se repite y qué emoción predomina (sin psicologismo barato).

    2. Patrones de equipo y juegos invisibles
       - Describir patrones colectivos (ej: todos culpan a otro área, nadie asume, dependencia del dueño, comunicación pasivo-agresiva, etc.).
       - Marcar contradicciones entre versiones y qué revelan sobre la cultura.

    3. Impacto en resultados y en el cliente
       - Cómo este lío afecta a tiempos, calidad, errores, experiencia del cliente, clima interno.

    4. Oportunidades de mejora y focos de intervención
       - 3 a 6 focos claros (ej: acordar reglas de juego entre áreas, definir quién decide qué, ordenar el flujo de información, entrenar conversaciones difíciles, etc.).
       - Explicar brevemente cada foco con lenguaje concreto.

    5. Recomendaciones para el trabajo con el equipo
       - Proponer dinámicas o tipos de conversaciones a trabajar (sin detallar dinámicas complejas).
       - Sugerir si conviene empezar por el dueño, por los líderes intermedios o por todo el equipo junto.

    6. Nota de límites
       - Aclarar que este informe es una lectura a partir de percepciones y no reemplaza auditorías legales, contables ni procesos terapéuticos.

    Cerrá el informe con algo como:
    "Este diagnóstico de equipo fue generado con Mentora Process (IA) a partir de las distintas versiones
    de los integrantes, y está pensado para ser trabajado junto a un coach ejecutivo humano."
    """).strip()

    full_prompt = f"{intro}\n{issues_text}\n\n{team_text}\n\n{instructions}"
    return full_prompt

# =========================
# GENERAR INFORME (COMÚN)
# =========================

def call_llm(prompt, mode_label="MODO DEMO"):
    """
    Abstrae la llamada a la IA.
    Si no hay API key, devuelve modo demo.
    """
    if not os.getenv("OPENAI_API_KEY"):
        demo_report = textwrap.dedent(f"""
        [{mode_label} – SIN IA CONECTADA]

        Esto es un ejemplo de cómo se vería el informe.

        Acá iría el análisis ejecutivo generado por la IA, con:
        - Resumen ejecutivo
        - Patrones
        - Impacto en cliente y negocio
        - Focos de mejora
        - Propuesta de trabajo con coach

        Para activar la IA:
        1) Instalá openai: `pip install openai`
        2) Seteá la variable de entorno OPENAI_API_KEY
        3) Reemplazá la lógica de demo por la llamada real a la API.
        """).strip()
        return demo_report

    try:
        import openai

        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini",  # Cambiá por el modelo que quieras usar
            messages=[
                {
                    "role": "system",
                    "content": "Sos un consultor empresarial senior, claro, directo y ejecutivo.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )

        report_text = response.choices[0].message["content"]
        return report_text

    except Exception as e:
        return f"Error al llamar a la IA: {e}"

# =========================
# UI: MODO INDIVIDUAL
# =========================

def individual_mode():
    st.subheader("🔹 Diagnóstico individual")

    st.markdown(
        """
        Usá este modo cuando querés entender **tu propio rol** en el lío:
        cómo decidís, cómo comunicás y cómo eso impacta en tu empresa o equipo.
        """
    )

    st.divider()

    # 1) Elegir bloque principal
    st.markdown("### 1️⃣ Elegí por dónde te duele más hoy")

    block_names = list(BLOCKS.keys())
    selected_block = st.selectbox("Bloque principal", block_names, index=0, key="ind_block")

    block_data = BLOCKS[selected_block]
    st.markdown(f"**{block_data['icon']} {selected_block}** – {block_data['description']}")

    st.markdown("**¿Con cuáles de estas frases te sentís identificado?** (podés marcar más de una)")

    selected_issues = []
    for issue in block_data["issues"]:
        checked = st.checkbox(issue, value=False, key=f"ind_issue_{issue}")
        if checked:
            selected_issues.append(issue)

    if not selected_issues:
        st.info("Marcá al menos una frase que se parezca a lo que pasa en tu empresa o equipo.")

    st.divider()

    # 2) Preguntas de contexto
    st.markdown("### 2️⃣ Contame un poco más del contexto")

    context_answers = {}

    st.markdown("**Preguntas generales**")
    for idx, q in enumerate(GENERAL_QUESTIONS, start=1):
        answer = st.text_area(q, key=f"ind_general_q_{idx}", height=80)
        context_answers[q] = answer

    st.markdown(f"**Preguntas específicas sobre {selected_block}**")
    for idx, q in enumerate(BLOCK_SPECIFIC_QUESTIONS[selected_block], start=1):
        answer = st.text_area(q, key=f"ind_specific_{selected_block}_{idx}", height=80)
        context_answers[q] = answer

    st.divider()

    # 3) Generar informe
    st.markdown("### 3️⃣ Generar informe ejecutivo")

    if st.button("Generar informe individual con IA", type="primary", disabled=not selected_issues, key="ind_btn"):
        with st.spinner("Analizando la información y generando el informe..."):
            prompt = build_prompt_individual(selected_block, selected_issues, context_answers)
            report = call_llm(prompt, mode_label="MODO INDIVIDUAL DEMO")

        st.success("Informe generado.")
        st.markdown("### 📝 Informe Mentora Process – Diagnóstico individual")
        st.write(report)

        file_name = f"Informe_Mentora_Process_Individual_{selected_block.replace(' ', '_')}.txt"
        st.download_button(
            label="📥 Descargar informe en .txt",
            data=report,
            file_name=file_name,
            mime="text/plain",
            key="ind_download",
        )

# =========================
# UI: MODO EQUIPO
# =========================

def team_mode():
    st.subheader("👥 Síntesis rápida de equipo")

    st.markdown(
        """
        Usá este modo cuando **varias personas del mismo equipo** ya dieron su versión
        del problema (por escrito, por WhatsApp, por formulario, etc.) y querés sacar
        un **diagnóstico del lío** al toque.

        👉 Paso práctico:
        - Le pedís a cada integrante que responda un formulario o que te mande su versión.
        - Copiás todas las versiones en el campo de abajo (separadas por líneas o guiones).
        - Agregás tu mirada como líder / dueño.
        - Mentora Process te devuelve un diagnóstico de equipo para trabajar en sesión.
        """
    )

    st.divider()

    team_name = st.text_input("Nombre del equipo / área (opcional)", key="team_name")

    st.markdown("### 1️⃣ Elegí el bloque principal del problema de este equipo")

    block_names = list(BLOCKS.keys())
    selected_block = st.selectbox("Bloque principal", block_names, index=0, key="team_block")

    block_data = BLOCKS[selected_block]
    st.markdown(f"**{block_data['icon']} {selected_block}** – {block_data['description']}")

    st.markdown("**¿Qué frases describen mejor el lío de este equipo?** (podés marcar más de una)")

    selected_issues = []
    for issue in block_data["issues"]:
        checked = st.checkbox(issue, value=False, key=f"team_issue_{issue}")
        if checked:
            selected_issues.append(issue)

    if not selected_issues:
        st.info("Marcá al menos una frase que se parezca a lo que pasa en este equipo.")

    st.divider()

    st.markdown("### 2️⃣ Pegá las versiones del equipo")

    team_raw_input = st.text_area(
        "Copiá acá las respuestas / mensajes / notas de los integrantes del equipo.\n"
        "Podés separarlas con líneas como '---' o dejando espacios entre una y otra.",
        key="team_raw",
        height=220,
    )

    leader_view = st.text_area(
        "Tu mirada como líder / dueño / responsable sobre este lío:",
        key="team_leader_view",
        height=120,
    )

    st.divider()

    st.markdown("### 3️⃣ Generar diagnóstico de equipo")

    disabled_btn = not (selected_issues and team_raw_input.strip())

    if st.button("Generar diagnóstico de equipo con IA", type="primary", disabled=disabled_btn, key="team_btn"):
        with st.spinner("Leyendo las versiones y generando el diagnóstico de equipo..."):
            prompt = build_prompt_team(
                block_name=selected_block,
                selected_issues=selected_issues,
                team_name=team_name,
                team_raw_input=team_raw_input,
                leader_view=leader_view,
            )
            report = call_llm(prompt, mode_label="MODO EQUIPO DEMO")

        st.success("Diagnóstico generado.")
        st.markdown("### 📝 Informe Mentora Process – Diagnóstico de equipo")
        st.write(report)

        file_name = f"Informe_Mentora_Process_Equipo_{selected_block.replace(' ', '_')}.txt"
        st.download_button(
            label="📥 Descargar diagnóstico de equipo en .txt",
            data=report,
            file_name=file_name,
            mime="text/plain",
            key="team_download",
        )

# =========================
# MAIN
# =========================

def main():
    st.title(APP_NAME)
    st.caption(
        "Mentora Process: diagnóstico de liderazgo, procesos y experiencia del cliente potenciado con IA."
    )

    st.markdown(
        """
        Esta herramienta te ayuda a **poner en palabras el caos**, detectar patrones invisibles
        en la forma en que dirigís, decidís y coordinás tu empresa, y traducirlo en un
        **informe ejecutivo** para trabajar con un coach.
        """
    )

    st.divider()

    mode = st.radio(
        "¿Cómo querés usar Mentora Process hoy?",
        ["Diagnóstico individual", "Síntesis rápida de equipo"],
        horizontal=True,
    )

    st.divider()

    if mode == "Diagnóstico individual":
        individual_mode()
    else:
        team_mode()


if __name__ == "__main__":
    main()
