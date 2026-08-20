#!/usr/bin/env python3
"""Descarga el modelo GGUF Phi-3-mini y verifica embeddings."""
from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

# Permite ejecutar desde la carpeta del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import EMBEDDING_MODEL, GGUF_MODEL_PATH, GGUF_MODEL_URL, MODELS_DIR


def download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1_000_000:
        print(f"Ya existe: {dest} ({dest.stat().st_size / 1e9:.2f} GB)")
        return

    print(f"Descargando:\n  {url}\n→ {dest}")
    print("Esto puede tomar varios minutos (~2.3 GB)...")

    def _progress(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            pct = min(100, downloaded * 100 / total_size)
            mb = downloaded / 1e6
            total_mb = total_size / 1e6
            print(f"\r  {pct:5.1f}%  {mb:.0f}/{total_mb:.0f} MB", end="", flush=True)

    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        urllib.request.urlretrieve(url, tmp, reporthook=_progress)
        print()
        tmp.replace(dest)
        print(f"OK: {dest}")
    except Exception as exc:  # noqa: BLE001
        if tmp.exists():
            tmp.unlink(missing_ok=True)
        print(f"\nError al descargar modelo GGUF: {exc}")
        print(
            "Alternativa: instala Ollama (https://ollama.com) y ejecuta:\n"
            "  ollama pull phi3:mini"
        )
        raise


def warm_embeddings() -> None:
    print(f"Precargando embeddings: {EMBEDDING_MODEL}")
    from langchain_community.embeddings import HuggingFaceEmbeddings

    emb = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    _ = emb.embed_query("soldadura MIG robotizada ProAutomation")
    print("Embeddings listos.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-gguf", action="store_true", help="Solo embeddings")
    parser.add_argument("--skip-embeddings", action="store_true", help="Solo GGUF")
    args = parser.parse_args()

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    if not args.skip_gguf:
        try:
            download_file(GGUF_MODEL_URL, GGUF_MODEL_PATH)
        except Exception:  # noqa: BLE001
            print("Continuando sin GGUF (puedes usar Ollama o modo demo).")
    if not args.skip_embeddings:
        warm_embeddings()
    print("Descarga completada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
