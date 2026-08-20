"""Prompts del sistema y modos de salida."""
from __future__ import annotations

from config import SYSTEM_PROMPT


FORMAT_INSTRUCTIONS = {
    "ejecutivo": (
        "Formato EJECUTIVO: responde en máximo 3 párrafos cortos, listos para junta directiva. "
        "Sin relleno. Incluye recomendación clara y siguiente paso."
    ),
    "tecnico": (
        "Formato TÉCNICO: incluye detalle de proceso, normas aplicables y al menos una tabla "
        "comparativa en Markdown cuando sea útil (ventajas, riesgos, alternativas)."
    ),
}

LANGUAGE_INSTRUCTIONS = {
    "es": "Responde en español. Conserva términos técnicos en inglés (MIG, GMAW, WPS, FAT, SAT, etc.).",
    "en": "Respond in English. Keep welding/automation terminology precise.",
    "dual": (
        "Responde en español para el cliente local, pero incluye entre paréntesis o en tablas "
        "la terminología técnica en inglés clave (MIG/GMAW, WPS, FAT/SAT, ISO 10218, etc.)."
    ),
}


def build_rag_prompt(
    question: str,
    context: str,
    *,
    output_format: str = "ejecutivo",
    language: str = "es",
    session_context: str = "",
    mcc_addon: str = "",
) -> str:
    fmt = FORMAT_INSTRUCTIONS.get(output_format, FORMAT_INSTRUCTIONS["ejecutivo"])
    lang = LANGUAGE_INSTRUCTIONS.get(language, LANGUAGE_INSTRUCTIONS["es"])
    session_block = f"\nContexto de sesión del cliente:\n{session_context}\n" if session_context else ""
    mcc_block = f"\nInstrucciones MCC activas:\n{mcc_addon}\n" if mcc_addon else ""

    return f"""{SYSTEM_PROMPT}

{fmt}
{lang}
{session_block}{mcc_block}
---
CONTEXTO RECUPERADO DE LA BASE DE CONOCIMIENTO (cita estas fuentes cuando afirmes capacidades):
{context}
---

Pregunta del gerente:
{question}

Si una afirmación de capacidad no está respaldada por el contexto, indícalo explícitamente.
Respuesta:
"""


PPT_STRUCTURE_PROMPT = """A partir del siguiente concepto, genera una estructura de presentación PowerPoint
lista para que el gerente la arme. Usa este formato:

# Título de la presentación
## Slide N — Título
- Bullet 1
- Bullet 2
- Nota del orador: ...

Concepto:
{concept}

Contexto disponible:
{context}
"""
