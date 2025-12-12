import streamlit as st

st.set_page_config(
    page_title="Mentora Process & Roleplay Coach",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Mentora Process & Roleplay Coach")
st.caption("Plataforma de entrenamiento para conversaciones difíciles, liderazgo y decisiones empresariales.")

st.markdown("""
### ¿Qué es esta plataforma?

**Mentora Process & Roleplay Coach** es una herramienta de entrenamiento para empresas, líderes y equipos que necesitan:

- Tomar mejores decisiones bajo presión  
- Entrenar conversaciones difíciles (clientes, jefes, colaboradores)  
- Bajar el estrés en situaciones de conflicto o negociación  
- Practicar en un entorno seguro, pero realista

---

### Módulos incluidos en esta demo

1. **[Diagnóstico / Process](./?page=1_Process)**  
   Espacio para analizar el contexto, los puntos ciegos y los desafíos actuales.

2. **🎭 Mentora Roleplay Coach (voz + texto)**  
   Un simulador que permite practicar conversaciones reales, con tres estilos:
   - Modo estándar  
   - Modo cliente difícil  
   - Modo brutal honesto (modo samurái)  

3. **Informe verbal inmediato**  
   Al finalizar el roleplay, el coach puede dar feedback con:
   - Fortalezas  
   - Áreas de mejora  
   - Recomendaciones concretas para la próxima conversación  

---

### Cómo usar esta demo en una reunión con la empresa

1. Explicá en 1 minuto el objetivo:  
   > “Nuestra idea es que sus líderes y equipos puedan practicar conversaciones importantes antes de tenerlas en la vida real.”

2. Mostrá el menú lateral y entrá a **“Mentora Roleplay Coach”**.  
3. Pedí que alguien traiga una situación real (cliente conflictivo, empleado, jefe, etc.).  
4. Hacé el roleplay en vivo.  
5. Cerrá mostrando el feedback del coach y cómo se podría usar en un programa de capacitación.

---

📌 Para continuar, usá el menú lateral de Streamlit y entrá a **“Mentora Roleplay Coach”**.
""")
import streamlit as st
from modules.roleplay import load_system_prompt, load_roleplay_payload

st.divider()
st.header("🧠 Mentora Roleplay Coach – Test interno")

if st.button("Cargar Prompt System"):
    prompt = load_system_prompt()
    st.success("Prompt cargado correctamente")
    st.text_area("Prompt System", prompt, height=300)

if st.button("Cargar Roleplay JSON (mock)"):
    payload = load_roleplay_payload("data/sample_roleplay_input.json")
    st.success("Payload cargado correctamente")
    st.json(payload)
