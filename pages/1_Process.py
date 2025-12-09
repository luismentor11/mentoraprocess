import streamlit as st
from reportlab.pdfgen import canvas
from io import BytesIO

st.set_page_config(
    page_title="Mentora Process",
    page_icon="🔍",
    layout="centered"
)

# ------------------------------------------
# -----------  ESTILO VISUAL ---------------
# ------------------------------------------

st.markdown("""
<style>
/* Fondo general */
.main {
    background-color: #f5f6fa;
}

/* Contenedor tipo tarjeta */
.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* Títulos principales */
h1 {
    color: #4F46E5;
    font-weight: 900 !important;
}

/* Subtítulos */
h3, h2 {
    color: #4338CA;
    font-weight: 700 !important;
}

/* Texto general */
p, label, textarea {
    font-size: 1.05rem !important;
}

/* Botón principal */
.stButton>button {
    background-color: #4F46E5;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
    font-size: 1.05rem;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #3730A3;
}

/* Link */
a {
    color: #4F46E5 !important;
    text-decoration: none !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------
# ------------ FUNCIÓN PDF -----------------
# ------------------------------------------

def generar_pdf(respuestas):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, 800, "Informe Mentora Process")

    c.setFont("Helvetica", 11)
    y = 770

    for titulo, texto in respuestas.items():
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, titulo)
        y -= 18

        c.setFont("Helvetica", 10)
        for linea in texto.split("\n"):
            c.drawString(50, y, linea)
            y -= 15

        y -= 10

        if y < 60:  # salto de página
            c.showPage()
            y = 800

    c.save()
    buffer.seek(0)
    return buffer


# ------------------------------------------
# -------------- HEADER ---------------------
# ------------------------------------------

st.markdown('<div class="card">', unsafe_allow_html=True)
st.title("🔍 Mentora Process — Diagnóstico Estratégico Profundo")
st.caption("Un análisis profesional para líderes, equipos y organizaciones en búsqueda de claridad, foco y decisiones reales.")

st.markdown("""
Este módulo está diseñado para empresas, equipos y líderes que buscan claridad estratégica.

A través de preguntas poderosas, exploramos:

- 🎯 **Objetivos reales**
- 🧱 **Bloqueos y tensiones**
- 🔁 **Patrones que se repiten**
- ⚡ **Fortalezas disponibles**
- 🚀 **Próximos movimientos posibles**
""")
st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# ----------- FORMULARIO --------------------
# ------------------------------------------

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📝 Diagnóstico Guiado")

preg1 = st.text_area("1. ¿Cuál es hoy tu objetivo más importante dentro del área o proyecto?", height=80)
preg2 = st.text_area("2. ¿Qué situaciones o problemas se repiten y parecen no resolverse?", height=80)
preg3 = st.text_area("3. ¿Qué conversaciones estás evitando (con un cliente, jefe, colega o socio)?", height=80)
preg4 = st.text_area("4. ¿Qué emoción domina tu día a día laboral? ¿Qué te está diciendo esa emoción?", height=80)
preg5 = st.text_area("5. Si pudieras cambiar una sola cosa HOY que mejoraría todo lo demás, ¿qué sería?", height=80)
preg6 = st.text_area("6. ¿Qué fortalezas personales o del equipo no están siendo aprovechadas?", height=80)
preg7 = st.text_area("7. ¿Qué decisión venís posponiendo que ya sabés que deberías tomar?", height=80)

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# ----------- ANÁLISIS + DEEP INSIGHTS + PDF
# ------------------------------------------

st.markdown('<div class="card">', unsafe_allow_html=True)

if st.button("📌 Generar análisis"):
    if not any([preg1, preg2, preg3, preg4, preg5, preg6, preg7]):
        st.warning("Necesito al menos una respuesta para generar el análisis.")
    else:
        st.success("Diagnóstico generado con éxito.")

        # ----- ANÁLISIS BÁSICO -----
        st.markdown("### 📊 Análisis de Tu Situación (Mentora Insights)")
        st.markdown(f"""
**🎯 Objetivo:**  
{preg1 or "*No definido*"}

**🧱 Bloqueos o problemas recurrentes:**  
{preg2 or "*No especificado*"}

**💬 Conversación pendiente clave:**  
{preg3 or "*No declarado*"}

**🎭 Emoción predominante y su mensaje:**  
{preg4 or "*No declarado*"}

**⚡ Cambio inmediato con mayor impacto:**  
{preg5 or "*No definido*"}

**💎 Fortalezas no utilizadas:**  
{preg6 or "*No especificado*"}

**🔑 Decisión postergada que mueve la aguja:**  
{preg7 or "*No declarado*"}
        """)

        # ----- DEEP INSIGHTS -----
        st.markdown("### 🧠 Deep Insights — Lectura Ontológica")

        insights = []

        # 1 — Objetivo
        if preg1 and len(preg1) < 30:
            insights.append("Tu objetivo aparece poco definido. Cuando la meta es ambigua, la acción se vuelve dispersa.")
        elif preg1:
            insights.append("Tu objetivo tiene estructura. Falta alinear conversaciones y acciones para sostenerlo.")

        # 2 — Bloqueos
        if preg2 and ("siempre" in preg2.lower() or "repite" in preg2.lower()):
            insights.append("Detecto un patrón repetitivo. Los patrones no se rompen con esfuerzo sino con nuevas conversaciones.")
        elif preg2:
            insights.append("El bloqueo parece situacional, no estructural. Con una intervención precisa puede resolverse rápido.")

        # 3 — Conversación evitada
        if preg3:
            insights.append("La conversación que evitás es el eje real del conflicto. Lo que no se conversa, se cronifica.")
        else:
            insights.append("La ausencia de una conversación clara indica que el problema aún no tomó forma lingüística.")

        # 4 — Emoción predominante
        if preg4:
            lower = preg4.lower()
            if "ans" in lower:
                insights.append("La ansiedad muestra exceso de futuro y falta de estructura en el presente.")
            elif "eno" in lower:
                insights.append("El enojo revela vulneración de límites personales no expresados.")
            elif "cans" in lower or "agot" in lower:
                insights.append("El cansancio indica acumulación de decisiones no tomadas.")
            else:
                insights.append("Tu emoción es un mensaje del sistema: escucharlo ordena la acción.")

        # 5 — Cambio clave
        if preg5:
            insights.append("El cambio clave que nombrás es un movimiento de alto retorno. Si se ejecuta, reorganiza todo el sistema.")

        # 6 — Fortalezas
        if preg6:
            insights.append("Tus fortalezas están subutilizadas. Cuando no se activan, aparece frustración o estancamiento.")

        # 7 — Decisión postergada
        if preg7:
            insights.append("La decisión postergada es el punto de quiebre. Lo evitado hoy se convierte en costo mañana.")

        # Mostrar insights
        for insight in insights:
            st.markdown(f"🔹 {insight}")

        # ----- PDF -----
        respuestas = {
            "🎯 Objetivo": preg1 or "No definido",
            "🧱 Bloqueos": preg2 or "No especificado",
            "💬 Conversación pendiente": preg3 or "No declarado",
            "🎭 Emoción predominante": preg4 or "No declarado",
            "⚡ Cambio clave": preg5 or "No definido",
            "💎 Fortalezas": preg6 or "No especificado",
            "🔑 Decisión postergada": preg7 or "No declarado"
        }

        pdf_buffer = generar_pdf(respuestas)

        st.download_button(
            label="📄 Descargar Informe PDF",
            data=pdf_buffer,
            file_name="mentora_process_informe.pdf",
            mime="application/pdf"
        )

        st.info("Este diagnóstico te prepara para entrenar conversaciones reales en el **Mentora Roleplay Coach**.")
        st.markdown("👉 [Ir al simulador de conversaciones](./?page=2_Roleplay_Coach)")

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# ----------- SIDEBAR -----------------------
# ------------------------------------------

st.sidebar.title("Mentora Process")
st.sidebar.markdown("""
Este módulo está diseñado para:

- Líderes  
- Equipos comerciales  
- Mandos medios  
- Emprendedores  
- RRHH y capacitación  

Usalo para preparar conversaciones difíciles antes de ejecutarlas en la vida real.
""")
