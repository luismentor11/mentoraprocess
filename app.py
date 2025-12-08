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
# ESTILOS CUSTOM (LOOK CORPORATIVO DARK)
# =========================

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Contenedor principal centrado y más angosto */
        .block-container {
            max-width: 900px !important;
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }

        /* Fondo general dark con leve gradiente */
        .stApp {
            background: radial-gradient(circle at top, #020617 0, #020617 40%, #020617 100%);
            color: #e5e7eb;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
        }

        h1, h2, h3, h4 {
            color: #e5e7eb !important;
        }

        p, label, span, div {
            font-size: 0.94rem;
        }

        /* Hero title */
        .mentora-hero-title {
            font-size: 2rem;
            font-weight: 650;
            letter-spacing: -0.03em;
            margin-bottom: 0.15rem;
        }

        .mentora-hero-subtitle {
            font-size: 0.98rem;
            color: #9ca3af;
        }

        /* Textareas & inputs */
        .stTextArea textarea {
            background-color: #020617 !important;
            color: #e5e7eb !important;
            border-radius: 0.75rem !important;
            border: 1px solid rgba(148, 163, 184, 0.6) !important;
            font-size: 0.9rem !important;
        }

        .stTextInput input {
            background-color: #020617 !important;
            color: #e5e7eb !important;
            border-radius: 999px !important;
            border: 1px solid rgba(148, 163, 184, 0.6) !important;
            font-size: 0.9rem !important;
            padding: 0.45rem 0.9rem !important;
        }

        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #020617 !important;
            border-radius: 999px !important;
            border: 1px solid rgba(148, 163, 184, 0.6) !important;
            font-size: 0.9rem !important;
        }

        .stCheckbox > label {
            color: #e5e7eb !important;
            font-size: 0.9rem;
        }

        .stRadio label {
            color: #e5e7eb !important;
            font-size: 0.9rem;
        }

        /* Botones */
        .stButton>button, .stDownloadButton>button {
            border-radius: 999px !important;
            border: 1px solid rgba(129, 140, 248, 0.9) !important;
            background: linear-gradient(90deg, #4f46e5, #a855f7) !important;
            color: white !important;
            padding: 0.45rem 1.3rem !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            box-shadow: 0 0 18px rgba(129, 140, 248, 0.4);
        }

        .stButton>button:disabled, .stDownloadButton>button:disabled {
            background: #111827 !important;
            border-color: #4b5563 !important;
            box-shadow: none !important;
            color: #6b7280 !important;
        }

        /* Cards suaves para secciones */
        .mentora-section {
            background: rgba(15, 23, 42, 0.92);
            border-radius: 1.1rem;
            border: 1px solid rgba(148, 163, 184, 0.35);
            padding: 1.1rem 1.2rem;
            margin-bottom: 1.2rem;
        }

        .mentora-section h3 {
            margin-top: 0;
        }

        /* Línea divisoria suave */
        hr {
            border: none;
            border-top: 1px solid rgba(55, 65, 81, 0.8);
            margin: 1.2rem 0;
        }

        /* Footer branding */
        .mentora-footer {
            margin-top: 1.8rem;
            font-size: 0.78rem;
            color: #6b7280;
            text-align: center;
        }

        /* Pill pequeño */
        .mentora-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.12rem 0.6rem;
            border-radius: 999px;
            border: 1px solid rgba(129, 140, 248, 0.65);
            background: rgba(15, 23, 42, 0.95);
            font-size: 0.7rem;
            color: #a5b4fc;
            margin-bottom: 0.4rem;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


inject_custom_css()

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

GENERAL_QUESTIONS = [
    "¿Cuál es hoy el principal dolor o preocupación que tenés respecto a tu empresa o equipo?",
    "Si este problema siguiera igual durante 12 meses, ¿qué impacto tendría en resultados, personas y clientes?",
    "¿Qué conversaciones difíciles sentís que se vienen pateando hace tiempo (y con quién)?",
    "¿Qué hacés normalmente cuando hay conflicto o algo sale mal? ¿Callás, explotás, culpás, te hacés cargo de todo, otra cosa?",
    "En pocas palabras, ¿qué te gustaría que sea distinto en 3 a 6 meses si este proceso funciona?",
]

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
# PROMPTS
# =========================

def build_prompt_individual(block_name, selected_issues, context_answers):
    block = BLOCKS[block_name]
    today = datetime.now().strftime("%Y-%m-%d")

    intro = textwrap.dedent(
        f"""
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
        """
    ).strip()

    issues_text = "\n".join([f"- {issue}" for issue in selected_issues])

    answers_text = "\n\nRESPUESTAS DEL USUARIO:\n"
    for label, answer in context_answers.items():
        answers_text += f"\n{label}:\n{(answer or '').strip()}\n"

    instructions = textwrap.dedent(
        """
        Estructura del informe que tenés que devolver (en español, tono ejecutivo, claro y directo):

        1. Resumen ejecutivo
        2. Patrones de liderazgo, comunicación y procesos
        3. Impacto en experiencia del cliente y en el negocio
        4. Oportunidades y focos de mejora
        5. Propuesta de trabajo con coach ejecutivo
        6. Nota de límites

        Cerrá el informe con:
        "Este informe fue generado con Mentora Process (IA) y está pensado para ser trabajado junto a
        un coach ejecutivo humano, como parte de un proceso de mejora continua."
        """
    ).strip()

    return f"{intro}\n{issues_text}\n\n{answers_text}\n\n{instructions}"


def build_prompt_team(block_name, selected_issues, team_name, team_raw_input, leader_view):
    block = BLOCKS[block_name]
    today = datetime.now().strftime("%Y-%m-%d")

    intro = textwrap.dedent(
        f"""
        Actuás como un consultor senior en cultura, procesos y liderazgo,
        especialista en empresas donde hay tensión entre áreas, personas y resultados.

        Estás usando la herramienta “Mentora Process” en MODO EQUIPO.
        Recibiste distintas versiones del mismo problema, contadas por varios integrantes de un equipo.

        Tu tarea:
        - Leer esas versiones como si fueran "capas del mismo lío".
        - Detectar patrones compartidos y contradicciones.
        - Traducir todo en un INFORME EJECUTIVO de diagnóstico de equipo.
        - Proponer focos de trabajo que luego se profundizan con el coach humano (Luis Yañez).

        FECHA DEL INFORME: {today}
        TIPO DE USO: Síntesis de equipo
        EQUIPO / ÁREA: {team_name if team_name else "No especificado"}
        BLOQUE PRINCIPAL: {block_name} – {block['description']}

        DOLENCIAS PRINCIPALES MARCADAS PARA ESTE EQUIPO:
        """
    ).strip()

    issues_text = "\n".join([f"- {issue}" for issue in selected_issues])

    team_text = textwrap.dedent(
        f"""
        VERSIONES DEL EQUIPO (copiadas tal cual o resumidas):

        {team_raw_input.strip()}

        MIRADA DEL LÍDER / DUEÑO / RESPONSABLE:

        {leader_view.strip()}
        """
    )

    instructions = textwrap.dedent(
        """
        Estructura del informe de equipo (tono ejecutivo, claro y directo):

        1. Resumen ejecutivo del conflicto / lío
        2. Patrones de equipo y juegos invisibles
        3. Impacto en resultados y en el cliente
        4. Oportunidades de mejora y focos de intervención
        5. Recomendaciones para el trabajo con el equipo
        6. Nota de límites

        Cerrá el informe con:
        "Este diagnóstico de equipo fue generado con Mentora Process (IA) a partir de las distintas versiones
        de los integrantes, y está pensado para ser trabajado junto a un coach ejecutivo humano."
        """
    ).strip()

    return f"{intro}\n{issues_text}\n\n{team_text}\n\n{instructions}"


# =========================
# LLAMADA A LA IA
# =========================

def call_llm(prompt, mode_label="MODO DEMO"):
    if not os.getenv("OPENAI_API_KEY"):
        demo_report = textwrap.dedent(
            f"""
            [{mode_label} – SIN IA CONECTADA]

            Esto es un ejemplo de cómo se vería el informe.

            Herramienta: Mentora Process.

            Acá iría el análisis ejecutivo generado por la IA.
            """
        ).strip()
        return demo_report

    try:
        import openai

        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Sos un consultor empresarial senior, claro, directo y ejecutivo.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return f"Error al llamar a la IA: {e}"


# =========================
# MODOS DE USO
# =========================

def individual_mode():
    st.markdown('<div class="mentora-section">', unsafe_allow_html=True)

    st.markdown("### 🔹 Diagnóstico individual")
    st.write(
        "Usá este modo para entender tu propio rol en el lío: cómo decidís, "
        "cómo comunicás y cómo eso impacta en tu empresa o equipo."
    )

    st.markdown("#### 1️⃣ Elegí por dónde te duele más hoy")

    block_names = list(BLOCKS.keys())
    selected_block = st.selectbox("Bloque principal", block_names, index=0, key="ind_block")

    block_data = BLOCKS[selected_block]
    st.write(f"{block_data['icon']} **{selected_block}** – {block_data['description']}")

    st.markdown("**¿Con cuáles de estas frases te sentís identificado?** (podés marcar más de una)")
    selected_issues = []
    for issue in block_data["issues"]:
        if st.checkbox(issue, key=f"ind_issue_{issue}"):
            selected_issues.append(issue)

    if not selected_issues:
        st.info("Marcá al menos una frase que se parezca a lo que pasa en tu empresa o equipo.")

    st.markdown("#### 2️⃣ Contame un poco más del contexto")

    context_answers = {}
    st.markdown("**Preguntas generales**")
    for idx, q in enumerate(GENERAL_QUESTIONS, start=1):
        ans = st.text_area(q, key=f"ind_general_q_{idx}", height=80)
        context_answers[q] = ans

    st.markdown(f"**Preguntas específicas sobre {selected_block}**")
    for idx, q in enumerate(BLOCK_SPECIFIC_QUESTIONS[selected_block], start=1):
        ans = st.text_area(q, key=f"ind_specific_{selected_block}_{idx}", height=80)
        context_answers[q] = ans

    st.markdown("#### 3️⃣ Generar informe ejecutivo")

    if st.button(
        "Generar informe individual con IA",
        type="primary",
        disabled=not selected_issues,
        key="ind_btn",
    ):
        with st.spinner("Analizando la información y generando el informe..."):
            prompt = build_prompt_individual(selected_block, selected_issues, context_answers)
            report = call_llm(prompt, mode_label="MODO INDIVIDUAL DEMO")

        st.success("Informe generado.")
        st.markdown("### 📝 Informe Mentora Process – Diagnóstico individual")
        st.write(report)

        fname = f"Informe_Mentora_Process_Individual_{selected_block.replace(' ', '_')}.txt"
        st.download_button(
            label="📥 Descargar informe en .txt",
            data=report,
            file_name=fname,
            mime="text/plain",
            key="ind_download",
        )

    st.markdown("</div>", unsafe_allow_html=True)


def team_mode():
    st.markdown('<div class="mentora-section">', unsafe_allow_html=True)

    st.markdown("### 👥 Síntesis rápida de equipo")
    st.write(
        "Usá este modo cuando varias personas del mismo equipo ya dieron su versión del problema "
        "y querés sacar un diagnóstico rápido y accionable."
    )

    team_name = st.text_input("Nombre del equipo / área (opcional)", key="team_name")

    st.markdown("#### 1️⃣ Elegí el bloque principal del problema de este equipo")

    block_names = list(BLOCKS.keys())
    selected_block = st.selectbox("Bloque principal", block_names, index=0, key="team_block")

    block_data = BLOCKS[selected_block]
    st.write(f"{block_data['icon']} **{selected_block}** – {block_data['description']}")

    st.markdown("**¿Qué frases describen mejor el lío de este equipo?** (podés marcar más de una)")
    selected_issues = []
    for issue in block_data["issues"]:
        if st.checkbox(issue, key=f"team_issue_{issue}"):
            selected_issues.append(issue)

    if not selected_issues:
        st.info("Marcá al menos una frase que se parezca a lo que pasa en este equipo.")

    st.markdown("#### 2️⃣ Pegá las versiones del equipo")

    team_raw_input = st.text_area(
        "Copiá acá las respuestas / mensajes / notas de los integrantes del equipo.\n"
        "Podés separarlas con '---' o dejando espacios entre una y otra.",
        key="team_raw",
        height=220,
    )

    leader_view = st.text_area(
        "Tu mirada como líder / dueño / responsable sobre este lío:",
        key="team_leader_view",
        height=120,
    )

    st.markdown("#### 3️⃣ Generar diagnóstico de equipo")

    disabled_btn = not (selected_issues and team_raw_input.strip())

    if st.button(
        "Generar diagnóstico de equipo con IA",
        type="primary",
        disabled=disabled_btn,
        key="team_btn",
    ):
        with st.spinner("Leyendo las versiones y generando el diagnóstico de equipo..."):
            prompt = build_prompt_team(
                selected_block,
                selected_issues,
                team_name,
                team_raw_input,
                leader_view,
            )
            report = call_llm(prompt, mode_label="MODO EQUIPO DEMO")

        st.success("Diagnóstico generado.")
        st.markdown("### 📝 Informe Mentora Process – Diagnóstico de equipo")
        st.write(report)

        fname = f"Informe_Mentora_Process_Equipo_{selected_block.replace(' ', '_')}.txt"
        st.download_button(
            label="📥 Descargar diagnóstico de equipo en .txt",
            data=report,
            file_name=fname,
            mime="text/plain",
            key="team_download",
        )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# MAIN
# =========================

def main():
    # HEADER con logo + título (sin sidebar)
    col_logo, col_text = st.columns([1, 3])

    with col_logo:
        try:
            st.image("mentora_logo.png", width=90)
        except Exception:
            st.markdown(
                "<div style='width:90px;height:90px;border-radius:999px;border:1px solid #4b5563;"
                "display:flex;align-items:center;justify-content:center;font-size:0.7rem;color:#6b7280;'>Logo Mentora</div>",
                unsafe_allow_html=True,
            )

    with col_text:
        st.markdown('<div class="mentora-pill">🧠 Herramienta de diagnóstico estratégico</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="mentora-hero-title">{APP_NAME}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="mentora-hero-subtitle">'
            'Diagnóstico de liderazgo, procesos y experiencia del cliente potenciado con IA, '
            'para conversaciones serias con dueños y gerentes.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.write("")
    st.write(
        "En pocos minutos, Mentora Process te ayuda a ordenar el caos, ponerle nombre a los patrones "
        "que se repiten y generar un informe ejecutivo listo para trabajar en sesión."
    )

    st.write("---")

    mode = st.radio(
        "¿Cómo querés usar Mentora Process hoy?",
        ["Diagnóstico individual", "Síntesis rápida de equipo"],
    )

    st.write("")

    if mode == "Diagnóstico individual":
        individual_mode()
    else:
        team_mode()

    # Branding al final
    st.markdown(
        """
        <div class="mentora-footer">
            Mentora Process · Marca de <b>Luis Yañez</b> · Desarrollado junto a IA<br/>
            Usá este informe como disparador de decisiones y conversaciones estratégicas, no como verdad absoluta.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
