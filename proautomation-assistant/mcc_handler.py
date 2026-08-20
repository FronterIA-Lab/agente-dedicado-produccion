"""MCC — Metodología de interacción en 4 capas."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SessionContext:
    """Capa 1 — Declaración de contexto del cliente."""

    industria: str = ""
    volumen: str = ""
    restricciones: str = ""
    plazo: str = ""
    presupuesto: str = ""
    notas: str = ""

    def is_empty(self) -> bool:
        return not any(
            [
                self.industria,
                self.volumen,
                self.restricciones,
                self.plazo,
                self.presupuesto,
                self.notas,
            ]
        )

    def as_text(self) -> str:
        if self.is_empty():
            return ""
        parts = [
            f"Industria: {self.industria or 'N/D'}",
            f"Volumen: {self.volumen or 'N/D'}",
            f"Restricciones técnicas: {self.restricciones or 'N/D'}",
            f"Plazo: {self.plazo or 'N/D'}",
            f"Presupuesto aproximado: {self.presupuesto or 'N/D'}",
        ]
        if self.notas:
            parts.append(f"Notas: {self.notas}")
        return "\n".join(parts)

    def onboarding_question(self) -> str:
        return (
            "¿Cuál es la situación de este cliente? "
            "(industria, volumen, restricciones técnicas, plazo, presupuesto aproximado)"
        )


# Capa 2 — Bifurcación de output
BIFURCATION_MODES = {
    "ninguno": "",
    "dos_enfoques": (
        "BIFURCACIÓN: entrega DOS enfoques en paralelo: "
        "(A) técnico-óptimo y (B) menor inversión inicial. Compara trade-offs."
    ),
    "contra_argumentacion": (
        "BIFURCACIÓN: además de tu recomendación, incluye la contra-argumentación "
        "probable del cliente y cómo rebatirla con datos técnicos/comerciales."
    ),
}

# Capa 3 — Verificación de certeza
CERTAINTY_ADDON = (
    "VERIFICACIÓN DE CERTEZA: al final, lista las afirmaciones que NO están "
    "respaldadas por los documentos recuperados bajo el encabezado "
    "'Afirmaciones a validar'. Si todo está respaldado, indícalo."
)

KNOWN_PROBE_PROMPT = (
    "KNOWN_PROBE (calibración): hazme 3 preguntas cuya respuesta YA debería "
    "estar en la base de conocimiento de ProAutomation (capacidades, fases FAT/SAT "
    "o normas de referencia). Espera mis respuestas para calibrar confianza."
)

# Capa 4 — Extracción de frameworks
FRAMEWORK_ADDON = (
    "FRAMEWORK: no des solo la solución cerrada. Transforma la respuesta en un "
    "marco de decisión con 5 criterios, preguntas clave y variables a evaluar "
    "con el cliente para definir la celda/proceso."
)


@dataclass
class MCCState:
    session: SessionContext = field(default_factory=SessionContext)
    bifurcation: str = "ninguno"
    certainty: bool = True
    framework: bool = False
    known_probe: bool = False

    def prompt_addon(self) -> str:
        parts: list[str] = []
        bif = BIFURCATION_MODES.get(self.bifurcation, "")
        if bif:
            parts.append(bif)
        if self.certainty:
            parts.append(CERTAINTY_ADDON)
        if self.framework:
            parts.append(FRAMEWORK_ADDON)
        if self.known_probe:
            parts.append(KNOWN_PROBE_PROMPT)
        return "\n".join(parts)

    def tag_unsupported_claims(self, answer: str, source_texts: list[str]) -> str:
        """Etiqueta simple de certeza: recuerda al usuario revisar citas."""
        if not self.certainty:
            return answer
        joined = "\n".join(source_texts).lower()
        markers = []
        for token in ["precio firme", "garantizamos", "único proveedor", "certificados iso"]:
            if token in answer.lower() and token not in joined:
                markers.append(token)
        if not markers:
            return answer + (
                "\n\n---\n**Certeza:** Revisa las fuentes citadas. "
                "Las capacidades de ProAutomation deben basarse solo en documentos cargados."
            )
        return (
            answer
            + "\n\n---\n**Afirmaciones a validar (no claras en documentos):** "
            + ", ".join(markers)
        )
