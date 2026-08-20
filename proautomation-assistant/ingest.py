#!/usr/bin/env python3
"""Ingesta de documentos → embeddings → ChromaDB."""
from __future__ import annotations

import argparse
import sys

from rag_engine import rebuild_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconstruye el índice vectorial ProAutomation")
    parser.parse_args()
    print("Reconstruyendo índice RAG (esto puede tardar la primera vez al bajar embeddings)...")
    n = rebuild_index()
    print(f"Listo. Fragmentos indexados: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
