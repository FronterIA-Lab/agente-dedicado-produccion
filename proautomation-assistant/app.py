"""
Asistente Estratégico ProAutomation — interfaz Streamlit.
Ejecutar: streamlit run app.py
"""
from __future__ import annotations

import streamlit as st

from config import MODULES, SYSTEM_PROMPT
from mcc_handler import MCCState, SessionContext
from rag_engine import RAGEngine
from tools import (
    calcular_costo,
    generar_ppt,
    generar_preguntas,
    generar_propuesta,
    redactar_manual,
)


st.set_page_config(
    page_title="ProAutomation Assistant",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner="Cargando motor RAG (primera vez puede tardar)...")
def load_engine() -> RAGEngine:
    return RAGEngine()


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "mcc" not in st.session_state:
        st.session_state.mcc = MCCState()
    if "awaiting_context" not in st.session_state:
        st.session_state.awaiting_context = True


def sidebar(engine: RAGEngine) -> dict:
    st.sidebar.title("ProAutomation")
    st.sidebar.caption("Asistente del Gerente de Producción")
    st.sidebar.markdown(f"**LLM backend:** `{engine.backend}`")

    st.sidebar.subheader("Formato de salida")
    output_format = st.sidebar.radio(
        "Modo",
        options=["ejecutivo", "tecnico"],
        format_func=lambda x: "Ejecutivo (≤3 párrafos)" if x == "ejecutivo" else "Técnico (tablas)",
        horizontal=False,
    )
    language = st.sidebar.selectbox(
        "Idioma",
        options=["es", "dual", "en"],
        format_func=lambda x: {
            "es": "Español",
            "dual": "Español + términos EN",
            "en": "English",
        }[x],
    )
    module_filter = st.sidebar.selectbox(
        "Filtrar módulo RAG",
        options=["todos", *MODULES.keys()],
        format_func=lambda x: "Todos los módulos" if x == "todos" else MODULES[x]["label"],
    )

    st.sidebar.subheader("MCC — capas activas")
    mcc: MCCState = st.session_state.mcc
    mcc.bifurcation = st.sidebar.selectbox(
        "Bifurcación de output",
        options=["ninguno", "dos_enfoques", "contra_argumentacion"],
        format_func=lambda x: {
            "ninguno": "Ninguna",
            "dos_enfoques": "Óptimo vs menor inversión",
            "contra_argumentacion": "Contra-argumentación cliente",
        }[x],
    )
    mcc.certainty = st.sidebar.checkbox("Verificación de certeza", value=True)
    mcc.framework = st.sidebar.checkbox("Marco de decisión (framework)", value=False)
    mcc.known_probe = st.sidebar.checkbox("KNOWN_PROBE (calibración)", value=False)

    with st.sidebar.expander("Capa 1 — Contexto del cliente", expanded=mcc.session.is_empty()):
        st.caption(mcc.session.onboarding_question())
        mcc.session.industria = st.text_input("Industria", mcc.session.industria)
        mcc.session.volumen = st.text_input("Volumen", mcc.session.volumen)
        mcc.session.restricciones = st.text_input("Restricciones técnicas", mcc.session.restricciones)
        mcc.session.plazo = st.text_input("Plazo", mcc.session.plazo)
        mcc.session.presupuesto = st.text_input("Presupuesto aprox.", mcc.session.presupuesto)
        mcc.session.notas = st.text_area("Notas", mcc.session.notas, height=80)
        if st.button("Guardar contexto"):
            st.session_state.awaiting_context = False
            st.sidebar.success("Contexto de sesión guardado")

    st.sidebar.divider()
    st.sidebar.subheader("Herramientas")
    tool = st.sidebar.selectbox(
        "Acción rápida",
        options=[
            "chat",
            "propuesta",
            "costos",
            "preguntas",
            "manual",
            "ppt",
        ],
        format_func=lambda x: {
            "chat": "Chat libre",
            "propuesta": "Generador de Propuesta (RFQ)",
            "costos": "Calculador de Costos",
            "preguntas": "Preguntas para el cliente",
            "manual": "Manual / Protocolo",
            "ppt": "Estructura PPT",
        }[x],
    )

    with st.sidebar.expander("System Prompt (ADN)", expanded=False):
        st.code(SYSTEM_PROMPT, language=None)

    if st.sidebar.button("Limpiar conversación"):
        st.session_state.messages = []
        st.rerun()

    return {
        "output_format": output_format,
        "language": language,
        "module_filter": None if module_filter == "todos" else module_filter,
        "tool": tool,
    }


def render_sources(sources) -> None:
    if not sources:
        return
    with st.expander("Fuentes RAG", expanded=False):
        for i, s in enumerate(sources, 1):
            score = f" · score={s.score:.3f}" if s.score is not None else ""
            st.markdown(f"**{i}. [{s.module}] {s.source}**{score}")
            st.caption(s.content[:400] + ("…" if len(s.content) > 400 else ""))


def tool_panels(engine: RAGEngine, opts: dict) -> None:
    tool = opts["tool"]
    if tool == "chat":
        return

    st.subheader("Herramienta seleccionada")
    if tool == "propuesta":
        rfq = st.text_area(
            "Pega el RFQ o requisitos del cliente",
            height=160,
            placeholder="Ej: Maquiladora autopartes, 10,000 pzas/día acero galvanizado...",
        )
        if st.button("Generar propuesta", type="primary") and rfq.strip():
            with st.spinner("Cruzando RFQ con capacidades y gestión de proyectos..."):
                out = generar_propuesta(engine, rfq, output_format=opts["output_format"])
            st.markdown(out["answer"])
            render_sources(out["sources"])

    elif tool == "costos":
        c1, c2 = st.columns(2)
        tipo = c1.selectbox(
            "Tipo de celda",
            ["1_estacion", "2_estaciones", "3_estaciones", "linea_transfer"],
        )
        comp = c2.selectbox("Complejidad", ["baja", "media", "alta"])
        if st.button("Calcular estimación", type="primary"):
            out = calcular_costo(tipo_celda=tipo, complejidad=comp)
            st.markdown(out["answer"])

    elif tool == "preguntas":
        industria = st.text_input("Industria del cliente", "automotriz TIER1")
        extra = st.text_input("Contexto adicional", "")
        if st.button("Generar preguntas", type="primary"):
            with st.spinner("Analizando industria y base de conocimiento..."):
                out = generar_preguntas(engine, industria, extra)
            st.markdown(out["answer"])
            render_sources(out["sources"])

    elif tool == "manual":
        tipo = st.selectbox("Tipo", ["mantenimiento preventivo", "manual de operación"])
        equipo = st.text_input("Equipo / celda", "Celda robótica MIG 2 estaciones")
        if st.button("Redactar borrador", type="primary"):
            with st.spinner("Redactando protocolo..."):
                out = redactar_manual(engine, tipo, equipo)
            st.markdown(out["answer"])
            render_sources(out["sources"])

    elif tool == "ppt":
        concept = st.text_area("Concepto de la presentación", height=120)
        if st.button("Generar estructura PPT", type="primary") and concept.strip():
            with st.spinner("Armando diapositivas..."):
                out = generar_ppt(engine, concept)
            st.markdown(out["answer"])
            render_sources(out["sources"])


def chat_panel(engine: RAGEngine, opts: dict) -> None:
    st.subheader("Chat con el Asistente Estratégico")
    mcc: MCCState = st.session_state.mcc

    if st.session_state.awaiting_context and mcc.session.is_empty():
        st.info(mcc.session.onboarding_question() + " — completa el panel lateral para mejores respuestas.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                render_sources(msg["sources"])

    if prompt := st.chat_input("Escribe tu consulta comercial-técnica..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consultando RAG..."):
                result = engine.query(
                    prompt,
                    module_filter=opts["module_filter"],
                    output_format=opts["output_format"],
                    language=opts["language"],
                    session_context=mcc.session.as_text(),
                    mcc_addon=mcc.prompt_addon(),
                )
                answer = mcc.tag_unsupported_claims(
                    result.answer,
                    [s.content for s in result.sources],
                )
            st.markdown(answer)
            render_sources(result.sources)
            st.caption(f"Backend: {result.backend}")

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": result.sources,
            }
        )


def main() -> None:
    init_state()
    st.title("Asistente Estratégico ProAutomation")
    st.caption(
        "RAG local · Capacidades · Normas · Gestión de proyectos · Inteligencia de mercado"
    )

    try:
        engine = load_engine()
    except Exception as exc:  # noqa: BLE001
        st.error(
            f"No se pudo iniciar el motor RAG: {exc}\n\n"
            "Ejecuta primero:\n"
            "```bash\npip install -r requirements.txt\n"
            "python scripts/download_models.py --skip-gguf\n"
            "python ingest.py\n```"
        )
        st.stop()

    opts = sidebar(engine)
    if opts["tool"] != "chat":
        tool_panels(engine, opts)
        st.divider()
    chat_panel(engine, opts)


if __name__ == "__main__":
    main()
