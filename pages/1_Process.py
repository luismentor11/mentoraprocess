import streamlit as st

st.set_page_config(
    page_title="Mentora Process",
    page_icon="🔍",
    layout="centered"
)

# ------------------ HEADER ------------------

st.title("🔍 Mentora Process — Diagnóstico Estratégico Profundo")
st.caption("Un análisis profesional para entender tu situación actual, identificar bloqueos y diseñar un camino claro hacia tus resultados.")

st.markdown("""
Este módulo está diseñado para empresas, equipos y líderes que buscan claridad estratégica.

A través de preguntas poderosas, exploramos:

- 🎯 **Objetivos reales**
- 🧱 **Bloqueos y tensiones**
- 🔁 **Patrones que se repiten**
- ⚡ **Fortalezas disponibles**
- 🚀 **Próximos movimientos posibles**

Tomate tu tiempo. Las respuestas no tienen que ser perfectas; solo tienen que ser **honestas**.
""")


# ------------------ FORMULARIO ------------------

st.subheader("📝 Diagnóstico Guiado")

preg1 = st.text_area("1. ¿Cuál es hoy tu objetivo más importante dentro del área o proyecto?", height=80)

preg2 = st.text_area("2. ¿Qué situaciones o problemas se repiten y parecen no resolverse?", height=80)

preg3 = st.text_area("3. ¿Qué conversaciones estás evitando (con un cliente, jefe, colega o socio)?", height=80)

preg4 = st.text_area("4. ¿Qué emoción domina tu día a día laboral (ansiedad, enojo, claridad, motivación, desgaste)? ¿Qué te está diciendo esa emoción?", height=80)

preg5 = st.text_area("5. Si pudieras cambiar una sola cosa HOY que mejoraría todo lo demás, ¿qué sería?", height=80)

preg6 = st.text_area("6. ¿Qué fortalezas personales o del equipo no están siendo aprovechadas?", height=80)

preg7 = st.text_area("7. ¿Qué decisión venís posponiendo que ya sabés que deberías tomar?", height=80)


# ------------------ PROCESAR RESULTADOS ------------------

if st.button("📌 Generar análisis"):
    if not any([preg1, preg2, preg3, preg4, preg5, preg6, preg7]):
        st.warning("Necesito al menos una respuesta para generar el análisis.")
    else:
        st.success("Diagnóstico generado con éxito.")

        st.markdown("### 📊 Análisis de Tu Situación (Mentora Insights)")
        st.markdown("""
A continuación, un análisis general basado en tus respuestas:

- **Tu objetivo clave:**  
  _{}_

- **Los bloqueos que aparecen:**  
  _{}_

- **La conversación pendiente más determinante:**  
  _{}_

- **El estado emocional predominante:**  
  _{}_

- **El cambio inmediato con mayor impacto:**  
  _{}_

- **Fortalezas no utilizadas:**  
  _{}_

- **La decisión postergada que mueve la aguja:**  
  _{}_
        """.format(
            preg1 or "*No definido*",
            preg2 or "*No especificado*",
            preg3 or "*No declarado*",
            preg4 or "*No declarado*",
            preg5 or "*No definido*",
            preg6 or "*No especificado*",
            preg7 or "*No declarado*"
        ))

        st.info("Este diagnóstico te prepara para entrenar conversaciones concretas en el **Mentora Roleplay Coach**.")

        st.markdown("👉 [Ir al simulador de conversaciones](./?page=2_Roleplay_Coach)")


# ------------------ SIDEBAR ------------------

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
