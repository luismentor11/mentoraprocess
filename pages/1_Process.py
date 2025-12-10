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
    "Herramienta de diagnóstico profesional para leer el sistema humano de la empresa: "
    "liderazgo, vínculos, clima emocional, operación real y experiencia del cliente. "
    "El objetivo es obtener un mapa claro y accionable sobre qué está pasando y qué conviene ordenar primero."
)

# =========================
# HELPERS
# =========================

def nivel_bajo_medio_alto(score: int) -> str:
    if score <= 3:
        return "Bajo"
    elif score <= 6:
        return "Medio"
    return "Alto"


def calcular_madurez(niveles: dict) -> tuple[str, str]:
    altos = sum(1 for n in niveles.values() if n == "Alto")
    medios = sum(1 for n in niveles.values() if n == "Medio")
    bajos = sum(1 for n in niveles.values() if n == "Bajo")

    if altos >= 3:
        nivel = "Nivel 1 – Sobrevivencia"
        desc = (
            "La empresa está operando en modo sobrevivencia. El sistema humano sostiene el día a día con mucha tensión, "
            "poco margen para pensar y alta probabilidad de desgaste o roturas importantes si no se interviene."
        )
    elif altos == 2 and medios >= 2:
        nivel = "Nivel 2 – Dependencia"
        desc = (
            "La empresa depende en exceso de pocas personas o vínculos clave. El sistema funciona, pero se apoya en "
            "estructuras frágiles: si una pieza se cae o se satura, todo el resto se resiente."
        )
    elif altos <= 2 and medios >= 2:
        nivel = "Nivel 3 – Caos funcional"
        desc = (
            "La empresa funciona, pero con esfuerzo extra, errores repetidos y temas que se arrastran. Hay base para ordenar, "
            "pero el sistema todavía responde más a la urgencia que a decisiones conscientes."
        )
    elif altos == 0 and medios >= 1:
        nivel = "Nivel 4 – Orden en construcción"
        desc = (
            "La empresa muestra intención de orden y ciertas bases sólidas. Siguen existiendo zonas de tensión, "
            "pero el sistema tiene recursos humanos para sostener cambios y mejoras reales."
        )
    else:
        nivel = "Nivel 5 – Madurez humana"
        desc = (
            "El sistema humano de la empresa tiene un buen nivel de madurez: hay conversaciones, responsabilidad compartida "
            "y capacidad de ajustar sin entrar en crisis permanente. Las intervenciones pueden ser finas y estratégicas."
        )

    return nivel, desc


def definir_juego_oculto(scores: dict) -> str:
    dominante = max(scores, key=scores.get)

    if dominante == "Poder y vínculos":
        return (
            "El juego oculto principal está en el poder y los vínculos. Hay decisiones que no se terminan de tomar, "
            "personas o temas intocables y responsabilidades que se desplazan sin nombrarlas con claridad."
        )
    if dominante == "Liderazgo y energía":
        return (
            "El juego oculto está en el estado del liderazgo. Quienes sostienen la empresa cargan con demasiado, "
            "postergan decisiones clave o funcionan con un nivel de desgaste que termina impactando en todo el sistema."
        )
    if dominante == "Cultura emocional y conversaciones":
        return (
            "El juego oculto vive en la cultura emocional. Hay cosas que se saben pero no se hablan de frente, "
            "las emociones se acumulan y los conflictos vuelven en forma de comentarios, chistes o tensión crónica."
        )
    if dominante == "Operación humana y claridad":
        return (
            "El juego oculto está en la operación humana. Roles difusos, errores repetidos y una organización que parece "
            "funcionar a base de apagar incendios más que de acordar cómo se quiere trabajar."
        )
    # Cliente como espejo
    return (
        "El juego oculto se ve reflejado en el cliente. La experiencia que vive el cliente confirma el desorden interno: "
        "quejas, fricciones o trato desigual según quién atienda y en qué momento."
    )


def generar_acciones(scores: dict, niveles: dict, nivel_madurez: str) -> list[str]:
    acciones: list[str] = []

    # Ordenamos patrones por tensión
    orden_patrones = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    patrones_top = [p[0] for p in orden_patrones[:2]]

    for patron in patrones_top:
        if patron == "Poder y vínculos":
            acciones.append(
                "Redibujar el mapa real de poder y vínculos: identificar quién decide qué, "
                "qué temas están prohibidos de nombrar y qué roles están sobredimensionados o subutilizados."
            )
            acciones.append(
                "Poner por escrito 3 decisiones de fondo que hoy se evitan (personas, límites o estructura) "
                "y definir fecha máxima para tomarlas, aunque incomoden."
            )
        elif patron == "Liderazgo y energía":
            acciones.append(
                "Revisar agenda y foco del liderazgo: definir qué tareas tienen que salir de la cabeza del líder "
                "y pasar a sistema, equipo o terceros en los próximos 30 días."
            )
            acciones.append(
                "Acordar con el liderazgo 1 espacio semanal sin operación (30–45 minutos) para revisar decisiones, "
                "prioridades y límites, sin apagar incendios."
            )
        elif patron == "Cultura emocional y conversaciones":
            acciones.append(
                "Identificar 2 conversaciones que todos saben que faltan y ponerles fecha, participantes y objetivo claro "
                "para tenerlas en los próximos 30 días."
            )
            acciones.append(
                "Definir una regla simple de comunicación interna (por ejemplo: lo que se habla de alguien, se habla con esa persona) "
                "y sostenerla explícitamente desde la dirección."
            )
        elif patron == "Operación humana y claridad":
            acciones.append(
                "Elegir 1 proceso o circuito crítico (por ejemplo: ingreso de clientes, turnos, pedidos, cobros) y "
                "mapearlo paso a paso, marcando quién hace qué y en qué orden."
            )
            acciones.append(
                "Revisar 3 tareas que hoy hace alguien que no debería hacerlas y reasignarlas o eliminarlas de forma consciente."
            )
        elif patron == "Cliente como espejo":
            acciones.append(
                "Registrar durante 15 días las quejas o fricciones más frecuentes de los clientes y agruparlas por tipo "
                "(demora, trato, errores, comunicación, organización)."
            )
            acciones.append(
                "Diseñar una respuesta estándar clara y respetuosa para cada tipo de queja, alineada entre recepción, administración "
                "y dirección, para bajar la tensión en quienes atienden."
            )

    if "Nivel 1" in nivel_madurez or "Nivel 2" in nivel_madurez:
        acciones.append(
            "Programar una reunión específica para revisar el sistema humano (no números ni ventas): "
            "roles, conversaciones pendientes, límites y decisiones postergadas."
        )

    # eliminar duplicadas manteniendo orden
    acciones_unicas: list[str] = []
    for acc in acciones:
        if acc not in acciones_unicas:
            acciones_unicas.append(acc)

    return acciones_unicas


def armar_reporte_texto(
    contexto: dict,
    patrones_scores: dict,
    patrones_niveles: dict,
    nivel_madurez: str,
    desc_madurez: str,
    juego_oculto: str,
    acciones: list[str],
) -> str:
    lineas: list[str] = []

    lineas.append("INFORME MENTORA PROCESS")
    lineas.append("")
    lineas.append("1. DATOS DE CONTEXTO")
    lineas.append(f"- Tipo de empresa: {contexto['tipo_empresa']}")
    lineas.append(f"- Tamaño aproximado del equipo: {contexto['tam_equipo']} personas")
    lineas.append(f"- Áreas principales: {contexto['areas'] or 'No especificado'}")
    lineas.append(f"- Antigüedad del equipo: {contexto['antiguedad']}")
    lineas.append(f"- Rol de quien responde: {contexto['rol']}")
    lineas.append(f"- Relación con el conflicto: {contexto['relacion_conflicto']}")
    lineas.append(f"- Síntoma principal que se observa: {contexto['sintoma']}")
    lineas.append(f"- Costo de seguir así: {contexto['costo'] or 'No especificado'}")
    lineas.append("")
    if contexto["caso"]:
        lineas.append("Caso representativo:")
        lineas.append(f"{contexto['caso']}")
        lineas.append("")

    lineas.append("2. LECTURA GENERAL DEL SISTEMA HUMANO")
    lineas.append(
        "La lectura se enfoca en el sistema humano, no en personas aisladas. "
        "A partir de las respuestas, se observa cómo se combinan poder, liderazgo, conversaciones, "
        "organización y experiencia del cliente."
    )
    lineas.append("")

    lineas.append("3. MAPA DE PATRONES INTERNOS")
    for nombre in [
        "Poder y vínculos",
        "Liderazgo y energía",
        "Cultura emocional y conversaciones",
        "Operación humana y claridad",
        "Cliente como espejo",
    ]:
        nivel = patrones_niveles[nombre]
        score = patrones_scores[nombre]
        lineas.append(f"- {nombre}: {nivel} (intensidad {score})")
    lineas.append("")

    lineas.append("4. JUEGO OCULTO QUE HOY ESTÁ OPERANDO")
    lineas.append(juego_oculto)
    lineas.append("")

    lineas.append("5. NIVEL DE MADUREZ HUMANA DE LA EMPRESA")
    lineas.append(nivel_madurez)
    lineas.append(desc_madurez)
    lineas.append("")

    lineas.append("6. ACCIONES PRIORITARIAS PARA LOS PRÓXIMOS 30–60 DÍAS")
    for i, accion in enumerate(acciones, start=1):
        lineas.append(f"{i}. {accion}")
    lineas.append("")

    lineas.append(
        "Este informe es un punto de partida. La profundidad real se trabaja en conversación, "
        "pero el mapa permite decidir por dónde conviene empezar a intervenir."
    )

    return "\n".join(lineas)


# =========================
# FORMULARIO
# =========================

with st.form("diagnostico_mentora_process"):

    st.markdown("### 1️⃣ Contexto de la empresa")

    tipo_empresa = st.selectbox(
        "Tipo de empresa",
        [
            "Empresa familiar",
            "Servicios profesionales",
            "Comercio / Atención directa",
            "Salud / Educación",
            "Startup / Equipo joven",
            "Otra",
        ],
    )

    tam_equipo = st.number_input(
        "Cantidad aproximada de personas que trabajan hoy en la empresa",
        min_value=1,
        max_value=1000,
        value=10,
        step=1,
    )

    areas = st.text_input(
        "Áreas o sectores principales (separadas por coma)",
        placeholder="Ejemplo: Administración, Ventas, Recepción, Producción, Dirección",
    )

    antiguedad_equipo = st.selectbox(
        "Antigüedad promedio del equipo",
        [
            "Menos de 1 año",
            "Entre 1 y 3 años",
            "Entre 3 y 7 años",
            "Más de 7 años",
            "Muy mezclada (gente nueva y muy antigua)",
        ],
    )

    rol = st.selectbox(
        "Tu rol principal en la empresa",
        [
            "Socio / Dirección",
            "Gerencia / Encargado",
            "Equipo operativo / Administrativo",
            "Atención al cliente / Recepción",
            "Profesional / Técnico",
            "Otro",
        ],
    )

    relacion_conflicto = st.selectbox(
        "Respecto al conflicto que ves, sentís que:",
        [
            "Sos parte de quienes lo generan",
            "Recibís el impacto, pero no lo generás",
            "Lo observás desde afuera",
            "Estás en el medio de varias partes",
            "No tenés claro qué pasa, pero te afecta igual",
        ],
    )

    sintoma_principal = st.selectbox(
        "Si tuvieras que elegir un síntoma principal hoy, sería:",
        [
            "Desgaste / cansancio en quienes sostienen la empresa",
            "Tensiones internas / roces / conversaciones pendientes",
            "Operación pesada / lenta / desordenada",
            "Clientes incómodos / quejas / mala experiencia",
            "No está claro qué pasa, pero algo está trabado",
        ],
    )

    caso_representativo = st.text_area(
        "Contá un caso concreto que represente lo que está pasando:",
        placeholder="Ejemplo: discusión entre socios, queja fuerte de un cliente, error repetido, renuncia, cruce entre áreas, etc.",
    )

    costo_seguir = st.multiselect(
        "¿Qué costo tiene seguir así para la empresa?",
        [
            "Dinero",
            "Clientes",
            "Personas clave",
            "Tiempo",
            "Energía emocional",
            "Reputación",
            "Otro",
        ],
    )

    costo_otro = ""
    if "Otro" in costo_seguir:
        costo_otro = st.text_input("¿Qué otro costo importante identificás?")

    st.markdown("### 2️⃣ Patrones profundos del sistema humano")

    st.markdown("#### Poder y vínculos invisibles")
    poder_tema_taboo = st.selectbox(
        "Sentís que hay temas que nadie quiere nombrar:",
        [
            "Casi nunca",
            "A veces",
            "Seguido",
            "Todo el tiempo",
        ],
    )
    poder_intocables = st.selectbox(
        "En la empresa hay personas o temas 'intocables':",
        [
            "No, en general se puede hablar de todo",
            "Un poco, pero se puede abordar",
            "Sí, claro y se evita tocarlos",
        ],
    )
    poder_responsabilidad = st.selectbox(
        "Cuando algo importante sale mal, la responsabilidad:",
        [
            "Se asume y se corrige",
            "Se comparte y se revisa",
            "Se baja hacia niveles más bajos",
            "Se diluye o se patea sin que nadie se haga cargo",
        ],
    )
    poder_tema_no_nombrado = st.text_area(
        "Si pudieras nombrar un tema que casi nunca se habla, pero sabés que está:",
        placeholder="Ejemplo: un socio que no aporta, alguien que maltrata, favoritismos, roles desbalanceados…",
    )

    st.markdown("#### Liderazgo y energía")
    lid_energia = st.selectbox(
        "La energía del liderazgo hoy está:",
        [
            "Clara y con buena energía",
            "Con cierto desgaste, pero manejable",
            "Cansada / saturada",
            "Ausente o muy reactiva",
        ],
    )
    lid_decisiones = st.selectbox(
        "Respecto a decisiones importantes:",
        [
            "Se toman a tiempo y se comunican",
            "Se demoran, pero llegan",
            "Se estiran hasta que explota algo",
            "Directamente se evitan",
        ],
    )
    lid_limites = st.selectbox(
        "Cuando alguien marca un límite sano (tiempos, tareas, respeto):",
        [
            "Se respeta y se ajusta",
            "Se escucha, pero no siempre se sostiene",
            "Genera molestia o resistencia",
            "Se castiga sutilmente o se deslegitima",
        ],
    )
    lid_comportamiento_tolerado = st.text_area(
        "¿Qué comportamiento sabés que se está tolerando y ya no cierra?",
        placeholder="Ejemplo: impuntualidad crónica, malos tratos, incumplimiento de acuerdos, baja responsabilidad…",
    )

    st.markdown("#### Cultura emocional y conversaciones")
    cult_conflicto = st.selectbox(
        "Cuando algo molesta o hay conflicto:",
        [
            "Se habla de frente y a tiempo",
            "Se habla, pero tarde",
            "Se comenta por atrás",
            "No se habla y se acumula",
        ],
    )
    cult_emocion = st.selectbox(
        "La emoción que más aparece en el día a día es:",
        [
            "Calma / foco",
            "Cansancio",
            "Irritación",
            "Resignación",
        ],
    )
    cult_conflicto_recurrente = st.text_area(
        "¿Qué conflicto o situación sentís que se repite una y otra vez?",
        placeholder="Ejemplo: las mismas discusiones, quejas entre áreas, peleas silenciosas…",
    )

    st.markdown("#### Operación humana y claridad")
    op_errores = st.selectbox(
        "Errores o problemas que se repiten:",
        [
            "Son pocos y se corrigen rápido",
            "Aparecen cada tanto",
            "Se repiten seguido",
            "Ya son parte del funcionamiento normal",
        ],
    )
    op_modo_trabajo = st.selectbox(
        "El modo de trabajo del día a día es más parecido a:",
        [
            "Planificado y previsible",
            "Una mezcla entre plan y urgencia",
            "Resolver sobre la marcha casi siempre",
            "Apagar incendios todo el tiempo",
        ],
    )
    op_saturacion = st.selectbox(
        "Respecto a la saturación de personas o áreas:",
        [
            "No se ve saturación importante",
            "A veces alguna persona o área se satura",
            "Siempre las mismas personas o áreas están saturadas",
            "La saturación es constante y generalizada",
        ],
    )
    op_tarea_fuera_lugar = st.text_area(
        "Mencioná una tarea importante que hoy hace alguien que no debería hacerla:",
        placeholder="Ejemplo: un dueño haciendo tareas operativas, recepción resolviendo problemas de dirección, etc.",
    )

    st.markdown("#### Cliente como espejo del sistema")
    cli_experiencia = st.selectbox(
        "La experiencia típica del cliente hoy es:",
        [
            "Fluida y ordenada",
            "Buena, pero con demoras o desprolijidades",
            "Correcta, pero fría o distante",
            "Irregular, con quejas o enojos frecuentes",
        ],
    )
    cli_quejas_frecuencia = st.selectbox(
        "Quejas o enojos de clientes:",
        [
            "Son raros y puntuales",
            "Pasan cada tanto",
            "Pasan seguido",
            "Son parte del día a día",
        ],
    )
    cli_puerta = st.selectbox(
        "Cuando un cliente se queja fuerte, la bronca suele caer en:",
        [
            "Recepción / Atención",
            "Administración",
            "Profesionales / Técnicos",
            "Dirección / Socios",
            "Depende del día y de quién esté",
        ],
    )
    cli_si_viera = st.text_area(
        "Si un cliente pudiera ver un día de trabajo puertas adentro, ¿qué confirmaría de lo que ya siente?",
        placeholder="Ejemplo: desorden, buena voluntad pero caos, trato desigual, coordinación, cuidado real, etc.",
    )

    submit = st.form_submit_button("Generar informe Mentora Process")

# =========================
# PROCESAMIENTO
# =========================

if submit:
    # Scores por patrón
    patrones_scores = {
        "Poder y vínculos": 0,
        "Liderazgo y energía": 0,
        "Cultura emocional y conversaciones": 0,
        "Operación humana y claridad": 0,
        "Cliente como espejo": 0,
    }

    # síntoma principal
    if sintoma_principal == "Desgaste / cansancio en quienes sostienen la empresa":
        patrones_scores["Liderazgo y energía"] += 3
    elif sintoma_principal == "Tensiones internas / roces / conversaciones pendientes":
        patrones_scores["Cultura emocional y conversaciones"] += 3
        patrones_scores["Poder y vínculos"] += 1
    elif sintoma_principal == "Operación pesada / lenta / desordenada":
        patrones_scores["Operación humana y claridad"] += 3
    elif sintoma_principal == "Clientes incómodos / quejas / mala experiencia":
        patrones_scores["Cliente como espejo"] += 3
    else:
        patrones_scores["Poder y vínculos"] += 1
        patrones_scores["Liderazgo y energía"] += 1
        patrones_scores["Cultura emocional y conversaciones"] += 1
        patrones_scores["Operación humana y claridad"] += 1
        patrones_scores["Cliente como espejo"] += 1

    # Poder y vínculos
    map_poder_tema = {
        "Casi nunca": 0,
        "A veces": 1,
        "Seguido": 2,
        "Todo el tiempo": 3,
    }
    patrones_scores["Poder y vínculos"] += map_poder_tema[poder_tema_taboo]

    map_poder_intocables = {
        "No, en general se puede hablar de todo": 0,
        "Un poco, pero se puede abordar": 1,
        "Sí, claro y se evita tocarlos": 3,
    }
    patrones_scores["Poder y vínculos"] += map_poder_intocables[poder_intocables]

    map_poder_resp = {
        "Se asume y se corrige": 0,
        "Se comparte y se revisa": 1,
        "Se baja hacia niveles más bajos": 2,
        "Se diluye o se patea sin que nadie se haga cargo": 3,
    }
    patrones_scores["Poder y vínculos"] += map_poder_resp[poder_responsabilidad]

    # Liderazgo y energía
    map_lid_energia = {
        "Clara y con buena energía": 0,
        "Con cierto desgaste, pero manejable": 1,
        "Cansada / saturada": 2,
        "Ausente o muy reactiva": 3,
    }
    patrones_scores["Liderazgo y energía"] += map_lid_energia[lid_energia]

    map_lid_decisiones = {
        "Se toman a tiempo y se comunican": 0,
        "Se demoran, pero llegan": 1,
        "Se estiran hasta que explota algo": 2,
        "Directamente se evitan": 3,
    }
    patrones_scores["Liderazgo y energía"] += map_lid_decisiones[lid_decisiones]

    map_lid_limites = {
        "Se respeta y se ajusta": 0,
        "Se escucha, pero no siempre se sostiene": 1,
        "Genera molestia o resistencia": 2,
        "Se castiga sutilmente o se deslegitima": 3,
    }
    patrones_scores["Liderazgo y energía"] += map_lid_limites[lid_limites]

    # Cultura emocional y conversaciones
    map_cult_conflicto = {
        "Se habla de frente y a tiempo": 0,
        "Se habla, pero tarde": 1,
        "Se comenta por atrás": 2,
        "No se habla y se acumula": 3,
    }
    patrones_scores["Cultura emocional y conversaciones"] += map_cult_conflicto[cult_conflicto]

    map_cult_emocion = {
        "Calma / foco": 0,
        "Cansancio": 1,
        "Irritación": 2,
        "Resignación": 3,
    }
    patrones_scores["Cultura emocional y conversaciones"] += map_cult_emocion[cult_emocion]

    # Operación humana y claridad
    map_op_errores = {
        "Son pocos y se corrigen rápido": 0,
        "Aparecen cada tanto": 1,
        "Se repiten seguido": 2,
        "Ya son parte del funcionamiento normal": 3,
    }
    patrones_scores["Operación humana y claridad"] += map_op_errores[op_errores]

    map_op_modo = {
        "Planificado y previsible": 0,
        "Una mezcla entre plan y urgencia": 1,
        "Resolver sobre la marcha casi siempre": 2,
        "Apagar incendios todo el tiempo": 3,
    }
    patrones_scores["Operación humana y claridad"] += map_op_modo[op_modo_trabajo]

    map_op_saturacion = {
        "No se ve saturación importante": 0,
        "A veces alguna persona o área se satura": 1,
        "Siempre las mismas personas o áreas están saturadas": 2,
        "La saturación es constante y generalizada": 3,
    }
    patrones_scores["Operación humana y claridad"] += map_op_saturacion[op_saturacion]

    # Cliente como espejo
    map_cli_exp = {
        "Fluida y ordenada": 0,
        "Buena, pero con demoras o desprolijidades": 1,
        "Correcta, pero fría o distante": 2,
        "Irregular, con quejas o enojos frecuentes": 3,
    }
    patrones_scores["Cliente como espejo"] += map_cli_exp[cli_experiencia]

    map_cli_quejas = {
        "Son raros y puntuales": 0,
        "Pasan cada tanto": 1,
        "Pasan seguido": 2,
        "Son parte del día a día": 3,
    }
    patrones_scores["Cliente como espejo"] += map_cli_quejas[cli_quejas_frecuencia]

    if cli_puerta in ["Recepción / Atención", "Administración"]:
        patrones_scores["Cliente como espejo"] += 1
        patrones_scores["Operación humana y claridad"] += 1
    elif cli_puerta == "Profesionales / Técnicos":
        patrones_scores["Cliente como espejo"] += 2
        patrones_scores["Liderazgo y energía"] += 1
    elif cli_puerta == "Dirección / Socios":
        patrones_scores["Cliente como espejo"] += 1
        patrones_scores["Poder y vínculos"] += 1
    else:  # depende
        patrones_scores["Cliente como espejo"] += 1

    # Niveles por patrón
    patrones_niveles = {
        nombre: nivel_bajo_medio_alto(score)
        for nombre, score in patrones_scores.items()
    }

    # Madurez
    nivel_madurez, desc_madurez = calcular_madurez(patrones_niveles)

    # Acciones sugeridas
    acciones = generar_acciones(patrones_scores, patrones_niveles, nivel_madurez)

    # Contexto para reporte
    costo_descripcion = ", ".join([c for c in costo_seguir if c != "Otro"])
    if "Otro" in costo_seguir and costo_otro:
        if costo_descripcion:
            costo_descripcion += f", Otro: {costo_otro}"
        else:
            costo_descripcion = f"Otro: {costo_otro}"

    contexto = {
        "tipo_empresa": tipo_empresa,
        "tam_equipo": tam_equipo,
        "areas": areas,
        "antiguedad": antiguedad_equipo,
        "rol": rol,
        "relacion_conflicto": relacion_conflicto,
        "sintoma": sintoma_principal,
        "caso": caso_representativo,
        "costo": costo_descripcion,
    }

    juego_oculto = definir_juego_oculto(patrones_scores)

    reporte_texto = armar_reporte_texto(
        contexto,
        patrones_scores,
        patrones_niveles,
        nivel_madurez,
        desc_madurez,
        juego_oculto,
        acciones,
    )

    # =========================
    # MOSTRAR INFORME EN PANTALLA
    # =========================
    st.markdown("---")
    st.markdown("## 🧾 Informe Mentora Process – Versión beta profesional")

    st.markdown("### 1. Datos de contexto")
    st.write(f"- Tipo de empresa: **{tipo_empresa}**")
    st.write(f"- Tamaño aproximado del equipo: **{tam_equipo} personas**")
    st.write(f"- Áreas principales: **{areas or 'No especificado'}**")
    st.write(f"- Antigüedad del equipo: **{antiguedad_equipo}**")
    st.write(f"- Rol de quien responde: **{rol}**")
    st.write(f"- Relación con el conflicto: **{relacion_conflicto}**")
    st.write(f"- Síntoma principal: **{sintoma_principal}**")
    st.write(f"- Costo de seguir así: **{costo_descripcion or 'No especificado'}**")

    if caso_representativo.strip():
        st.markdown("**Caso representativo:**")
        st.write(caso_representativo.strip())

    st.markdown("### 2. Mapa de patrones internos")
    for nombre in patrones_scores.keys():
        st.write(
            f"- **{nombre}:** {patrones_niveles[nombre]} "
            f"(intensidad {patrones_scores[nombre]})"
        )

    st.markdown("### 3. Juego oculto que hoy está operando")
    st.write(juego_oculto)

    st.markdown("### 4. Nivel de madurez humana de la empresa")
    st.write(f"**{nivel_madurez}**")
    st.write(desc_madurez)

    st.markdown("### 5. Acciones sugeridas para los próximos 30–60 días")
    for i, acc in enumerate(acciones, start=1):
        st.write(f"{i}. {acc}")

    st.markdown("### 6. Informe completo en texto")
    st.text_area(
        "Podés copiar y pegar este informe para enviarlo al cliente:",
        value=reporte_texto,
        height=350,
    )

    st.download_button(
        label="⬇️ Descargar informe en texto (.txt)",
        data=reporte_texto,
        file_name="informe_mentora_process.txt",
        mime="text/plain",
    )
