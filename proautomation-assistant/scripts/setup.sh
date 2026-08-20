#!/usr/bin/env bash
# Setup completo para el gerente (macOS/Linux)
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python scripts/download_models.py --skip-gguf || true
python ingest.py
echo ""
echo "Listo. Ejecuta: source .venv/bin/activate && streamlit run app.py"
