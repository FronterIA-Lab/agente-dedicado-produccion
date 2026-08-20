#!/usr/bin/env python3
"""Prueba rápida sin UI: retrieval + calculador."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag_engine import RAGEngine
from tools import calcular_costo


def main() -> None:
    engine = RAGEngine()
    q = "sistema de soldadura por proyección piezas automotrices"
    hits = engine.retrieve(q, module_filter="comercial", k=3)
    assert hits, "Se esperaban resultados del módulo comercial"
    assert any("proyec" in h.content.lower() or "soldadura" in h.content.lower() for h in hits)
    cost = calcular_costo("3_estaciones", "media")
    assert "rango_estimado_mxn" in cost["detalle"]
    print(f"backend={engine.backend} hits={len(hits)} OK")
    for h in hits:
        print(f" - [{h.module}] {h.source}")


if __name__ == "__main__":
    main()
