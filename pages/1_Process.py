import streamlit as st

st.set_page_config(page_title="Mentora Process", page_icon="🔍")

st.title("🔍 Mentora Process — Diagnóstico Estratégico")
st.markdown("""
Este módulo te permite analizar tu situación actual, detectar nudos, puntos ciegos y oportunidades de mejora en tu proceso interno o empresarial.

A continuación completá el diagnóstico para ayudarte a entender:

- Cómo estás trabajando hoy  
- Qué bloqueos aparecen  
- Qué objetivos concretos buscás  
- Qué hábitos y entornos influyen  
""")

st.subheader("📘 Diagnóstico Rápido")

pregunta1 = st.text_area("1. ¿Cuál es tu objetivo principal hoy?")
pregunta2 = st.text_area("2. ¿Qué es lo que más te está frenando ahora?")
pregunta3 = st.text_area("3. ¿Qué decisiones estás evitando?")
pregunta4 = st.text_area("4. ¿Qué resultados querés ver en 30 días?")
pregunta5 = st.text_area("5. ¿Qué hábitos o conductas repetís y te generan ruido?")

if st.button("Guardar diagnóstico"):
    st.success("Diagnóstico registrado. Podés continuar con el Roleplay para entrenar conversaciones relacionadas con estos puntos.")
