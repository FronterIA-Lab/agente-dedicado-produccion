"""Configuración central del Asistente ProAutomation."""
from __future__ import annotations

from pathlib import Path

# Rutas base
ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
DOCS_DIR = DATA_DIR / "docs"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"
MODELS_DIR = ROOT_DIR / "models"

# Módulos documentales (metadata)
MODULES = {
    "comercial": {
        "label": "Comercial y Capacidades",
        "path": DOCS_DIR / "comercial",
        "description": "Qué vendemos: llave en mano, robots, soldadura, casos de éxito",
    },
    "tecnico_normativo": {
        "label": "Técnico-Normativo",
        "path": DOCS_DIR / "tecnico_normativo",
        "description": "AWS D1.1, ISO 3834, ISO 10218, materiales",
    },
    "gestion_proyectos": {
        "label": "Gestión de Proyectos",
        "path": DOCS_DIR / "gestion_proyectos",
        "description": "Fases, FAT/SAT, timelines, garantía",
    },
    "inteligencia_mercado": {
        "label": "Inteligencia de Mercado",
        "path": DOCS_DIR / "inteligencia_mercado",
        "description": "Industria 4.0, mano de obra, MIG vs Láser",
    },
}

# Embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
TOP_K = 5

# LLM — GGUF local (Option A)
GGUF_MODEL_NAME = "Phi-3-mini-4k-instruct-q4.gguf"
GGUF_MODEL_URL = (
    "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/"
    "resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
)
GGUF_MODEL_PATH = MODELS_DIR / GGUF_MODEL_NAME
LLM_N_CTX = 4096
LLM_N_THREADS = 4
LLM_MAX_TOKENS = 768
LLM_TEMPERATURE = 0.2

# LLM — Ollama (Option C)
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "phi3:mini"

# Backend preferido: auto | llama_cpp | ollama | demo
LLM_BACKEND = "auto"

# Chroma
CHROMA_COLLECTION = "proautomation_rag"

# Costos históricos orientativos (MXN) — validar con ingeniería
COST_BASELINES = {
    "ingenieria_hh_mxn": 850,
    "instalacion_hh_mxn": 650,
    "programacion_hh_mxn": 900,
    "consumibles_celda_mes_mxn": 12000,
    "factor_complejidad": {
        "baja": 1.0,
        "media": 1.35,
        "alta": 1.75,
    },
    # Horas típicas por tipo de celda
    "horas_por_celda": {
        "1_estacion": {"ingenieria": 120, "programacion": 80, "instalacion": 60},
        "2_estaciones": {"ingenieria": 180, "programacion": 120, "instalacion": 90},
        "3_estaciones": {"ingenieria": 260, "programacion": 180, "instalacion": 140},
        "linea_transfer": {"ingenieria": 420, "programacion": 300, "instalacion": 240},
    },
}

SYSTEM_PROMPT = """Eres el Asistente Estratégico del Gerente de ProAutomation. Tu objetivo es ayudarlo a ganar proyectos de automatización y soldadura.

Regla 1: Para responder sobre las capacidades de ProAutomation, solo usas la información contenida en los documentos subidos (catálogos, PDFs, casos de éxito). Si no encuentras una capacidad específica, di: 'No contamos con esa capacidad en nuestro portafolio estándar, pero podemos evaluar una alianza o desarrollo a la medida.'
Regla 2: Para responder sobre normas, procesos y soldadura, usas tu conocimiento general (entrenamiento base) complementado con las normas técnicas cargadas.
Regla 3: No inventes precios ni tiempos de entrega exactos; ofrece rangos estimados basados en proyectos típicos y sugiere al gerente validar con el área de ingeniería.
Regla 4: Tu tono debe ser proactivo, comercial y técnicamente impecable, posicionando a ProAutomation como un socio experto, no solo un proveedor.

Responde en el idioma y formato indicados por el usuario. Mantén terminología técnica en inglés cuando corresponda (MIG, GMAW, WPS, FAT, SAT, RIA, etc.).
"""
