import streamlit as st

from modules.roleplay import load_system_prompt, load_roleplay_payload
from modules.voice import speech_to_text, text_to_speech
from modules.roleplay_engine import run_roleplay


# -------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------
st.set_page_config(
    page_title="Mentora Process & Roleplay Coach",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Mentora Process & Roleplay Coach")
st.caption(
    "Plataforma de entrenamiento para conversaciones difíciles, liderazgo y decisiones empresariales."
)

# -------------------------------------------------
# CONTENIDO INTRODUCTORIO
# -------------------------------------------------
st.markdown("""
### ¿Qué es esta plataforma?

**Mentora Process & Roleplay Coach** es una herramienta de entrenamiento para empresas, líderes y equipos que necesitan:

- Tomar mejores decisiones bajo presión  
- Entrenar conversaciones difíciles (clientes, jefes, colaboradores)  
- Bajar el estrés en situaciones de conflicto o negociación  
- Practicar en un entorno seguro, pero realista  

---

### Módulos incluidos en esta demo

1. **Diagnóstico / Process**  
   Espacio para analizar el contexto, los puntos ciegos y los desafíos actuales.

2. **🎭 Mentora Roleplay Coach (voz + texto)**  
   Un simulador que permite practicar conversaciones reales.

3. **Informe verbal inmediato**  
   Feedback claro y accionable al finalizar cada roleplay.

---

### Cómo usar esta demo en una reunión con la empresa

1. Explicá en 1 minuto el objetivo:  
   > “Nuestra idea es que sus líderes y equipos puedan practicar conversaciones importantes antes de tenerlas en la vida real.”

2. Pedí una situación real.  
3. Hacé el roleplay en vivo.  
4. Mostrá el feedback.  

---
""")

# -------------------------------------------------
# TEST INTERNO – CARGA DE CONFIGURACIÓN
# -------------------------------------------------
st.divider()
st.header("🧪 Test interno – Configuración")

if st.button("Cargar Prompt System"):
    prompt = load_system_prompt()
    st.success("Prompt cargado correctamente")
    st.text_area("Prompt System", prompt, height=250)

if st.button("Cargar Roleplay JSON (mock)"):
    payload = load_roleplay_payloa
