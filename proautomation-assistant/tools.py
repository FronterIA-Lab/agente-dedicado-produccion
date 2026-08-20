"""Herramientas de negocio para el gerente de ProAutomation."""
from __future__ import annotations

from typing import TYPE_CHECKING

from config import COST_BASELINES
from prompts import PPT_STRUCTURE_PROMPT

if TYPE_CHECKING:
    from rag_engine import RAGEngine


def generar_propuesta(rag: "RAGEngine", cliente_info: str, output_format: str = "tecnico") -> dict:
    """RFQ Responder: cruza requisitos con módulo comercial + gestión."""
    question = (
        "Genera un BORRADOR de propuesta técnico-económica (RFQ response) con: "
        "1) Resumen ejecutivo del entendimiento, 2) Solución técnica recomendada "
        "(arquitectura de celda / proceso de soldadura), 3) Entregables, "
        "4) Fases del proyecto y timeline orientativo, 5) Normas a mencionar, "
        "6) Supuestos y exclusiones, 7) Siguiente paso comercial.\n\n"
        f"Información del RFQ / cliente:\n{cliente_info}"
    )
    # Recupera de comercial y gestión prioritariamente mezclando consultas
    r1 = rag.retrieve(cliente_info, module_filter="comercial", k=4)
    r2 = rag.retrieve(cliente_info + " timeline FAT SAT", module_filter="gestion_proyectos", k=3)
    r3 = rag.retrieve(cliente_info + " normas WPS", module_filter="tecnico_normativo", k=3)
    hits = r1 + r2 + r3
    context = "\n\n".join(f"[{h.module} | {h.source}]\n{h.content}" for h in hits)
    from prompts import build_rag_prompt

    prompt = build_rag_prompt(
        question,
        context,
        output_format=output_format,
        language="dual",
    )
    answer = rag.llm.generate(prompt)
    return {"answer": answer, "sources": hits, "tool": "generar_propuesta"}


def calcular_costo(
    tipo_celda: str = "3_estaciones",
    complejidad: str = "media",
    estaciones: int | None = None,
) -> dict:
    """Estimador por regla de 3 / baselines históricos. Rangos, no precio firme."""
    baselines = COST_BASELINES
    key = tipo_celda if tipo_celda in baselines["horas_por_celda"] else "3_estaciones"
    if estaciones == 1:
        key = "1_estacion"
    elif estaciones == 2:
        key = "2_estaciones"
    elif estaciones == 3:
        key = "3_estaciones"

    horas = baselines["horas_por_celda"][key]
    factor = baselines["factor_complejidad"].get(complejidad, 1.35)

    ing = horas["ingenieria"] * factor * baselines["ingenieria_hh_mxn"]
    prog = horas["programacion"] * factor * baselines["programacion_hh_mxn"]
    inst = horas["instalacion"] * factor * baselines["instalacion_hh_mxn"]
    cons_3m = baselines["consumibles_celda_mes_mxn"] * 3

    subtotal = ing + prog + inst + cons_3m
    # Rango ±20%
    low = int(subtotal * 0.8)
    high = int(subtotal * 1.2)

    detalle = {
        "tipo_celda": key,
        "complejidad": complejidad,
        "factor": factor,
        "horas_ajustadas": {k: round(v * factor, 1) for k, v in horas.items()},
        "ingenieria_mxn": int(ing),
        "programacion_mxn": int(prog),
        "instalacion_mxn": int(inst),
        "consumibles_3_meses_mxn": int(cons_3m),
        "rango_estimado_mxn": {"min": low, "max": high},
        "aviso": (
            "Estimación orientativa basada en proyectos típicos. "
            "No incluye robot/fuente/hardware de terceros ni margen comercial. "
            "Validar con ingeniería y compras antes de cotizar."
        ),
    }

    md = f"""### Estimación de costos (orientativa)

| Concepto | Horas (ajustadas) | MXN |
|---|---:|---:|
| Ingeniería | {detalle['horas_ajustadas']['ingenieria']} | ${detalle['ingenieria_mxn']:,} |
| Programación PLC/Robot | {detalle['horas_ajustadas']['programacion']} | ${detalle['programacion_mxn']:,} |
| Instalación | {detalle['horas_ajustadas']['instalacion']} | ${detalle['instalacion_mxn']:,} |
| Consumibles (3 meses) | — | ${detalle['consumibles_3_meses_mxn']:,} |

**Rango estimado de servicios ProAutomation:** ${low:,} – ${high:,} MXN

> {detalle['aviso']}
"""
    return {"answer": md, "detalle": detalle, "sources": [], "tool": "calcular_costo"}


def generar_preguntas(rag: "RAGEngine", industria: str, contexto: str = "") -> dict:
    """Lista de preguntas técnicas clave antes de una reunión."""
    question = (
        f"Genera un listado de 10–15 preguntas técnicas y comerciales clave "
        f"que el gerente de ProAutomation debe hacer a un cliente de la industria: {industria}. "
        "Organiza en bloques: Proceso/Material, Volumen/Calidad, Planta/Utilities, "
        "Normativa, Comercial. Incluye por qué importa cada pregunta.\n"
        f"Contexto adicional: {contexto or 'N/A'}"
    )
    result = rag.query(
        question,
        module_filter=None,
        output_format="tecnico",
        language="dual",
    )
    return {
        "answer": result.answer,
        "sources": result.sources,
        "tool": "generar_preguntas",
    }


def redactar_manual(rag: "RAGEngine", tipo: str, equipo: str) -> dict:
    """Borrador de plan de mantenimiento o manual de operación."""
    tipo_norm = tipo.lower().strip()
    if "manten" in tipo_norm:
        focus = "plan de mantenimiento preventivo (diario/semanal/mensual/trimestral)"
    else:
        focus = "manual de operación para operadores (arranque, ciclo, alarmas, parada segura)"

    question = (
        f"Redacta un borrador de {focus} para: {equipo}. "
        "Incluye secciones claras, checklist y advertencias de seguridad ISO 10218. "
        "Indica que es borrador a validar con ingeniería."
    )
    result = rag.query(
        question,
        module_filter=None,
        output_format="tecnico",
        language="dual",
    )
    return {
        "answer": result.answer,
        "sources": result.sources,
        "tool": "redactar_manual",
    }


def generar_ppt(rag: "RAGEngine", concept: str) -> dict:
    """Estructura de diapositivas a partir de un concepto."""
    hits = rag.retrieve(concept, k=5)
    context = "\n\n".join(f"[{h.module} | {h.source}]\n{h.content}" for h in hits)
    prompt = PPT_STRUCTURE_PROMPT.format(concept=concept, context=context)
    answer = rag.llm.generate(prompt)
    return {"answer": answer, "sources": hits, "tool": "generar_ppt"}
