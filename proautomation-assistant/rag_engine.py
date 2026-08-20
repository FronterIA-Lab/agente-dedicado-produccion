"""Motor RAG: ingesta, embeddings, Chroma y consulta."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config import (
    CHROMA_COLLECTION,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DOCS_DIR,
    EMBEDDING_MODEL,
    GGUF_MODEL_PATH,
    LLM_BACKEND,
    LLM_MAX_TOKENS,
    LLM_N_CTX,
    LLM_N_THREADS,
    LLM_TEMPERATURE,
    MODULES,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    TOP_K,
    VECTOR_STORE_DIR,
)
from prompts import build_rag_prompt

logger = logging.getLogger(__name__)


@dataclass
class SourceHit:
    content: str
    module: str
    source: str
    score: float | None = None


@dataclass
class RAGResult:
    answer: str
    sources: list[SourceHit]
    backend: str
    unsupported_capability: bool = False


def _load_documents() -> list[dict[str, Any]]:
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    docs: list = []
    for module_id, meta in MODULES.items():
        folder: Path = meta["path"]
        if not folder.exists():
            continue
        for path in sorted(folder.rglob("*")):
            if path.suffix.lower() not in {".pdf", ".md", ".txt"}:
                continue
            try:
                if path.suffix.lower() == ".pdf":
                    loaded = PyPDFLoader(str(path)).load()
                else:
                    loaded = TextLoader(str(path), encoding="utf-8").load()
                for d in loaded:
                    d.metadata["module"] = module_id
                    d.metadata["module_label"] = meta["label"]
                    d.metadata["source"] = path.name
                docs.extend(loaded)
            except Exception as exc:  # noqa: BLE001
                logger.warning("No se pudo cargar %s: %s", path, exc)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(docs)


def get_embeddings():
    from langchain_community.embeddings import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vectorstore(create_if_missing: bool = True):
    import chromadb
    from langchain_community.vectorstores import Chroma

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    embeddings = get_embeddings()
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))

    existing = [c.name for c in client.list_collections()]
    if CHROMA_COLLECTION not in existing:
        if not create_if_missing:
            raise RuntimeError("Vector store vacío. Ejecuta: python ingest.py")
        chunks = _load_documents()
        if not chunks:
            raise RuntimeError(f"No hay documentos en {DOCS_DIR}")
        vs = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=CHROMA_COLLECTION,
            persist_directory=str(VECTOR_STORE_DIR),
            client=client,
        )
        logger.info("Índice creado con %s fragmentos", len(chunks))
        return vs

    return Chroma(
        collection_name=CHROMA_COLLECTION,
        embedding_function=embeddings,
        persist_directory=str(VECTOR_STORE_DIR),
        client=client,
    )


def rebuild_index() -> int:
    import chromadb
    from langchain_community.vectorstores import Chroma

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(VECTOR_STORE_DIR))
    existing = [c.name for c in client.list_collections()]
    if CHROMA_COLLECTION in existing:
        client.delete_collection(CHROMA_COLLECTION)

    chunks = _load_documents()
    if not chunks:
        raise RuntimeError(f"No hay documentos en {DOCS_DIR}")
    embeddings = get_embeddings()
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=CHROMA_COLLECTION,
        persist_directory=str(VECTOR_STORE_DIR),
        client=client,
    )
    return len(chunks)


class LLMClient:
    """Wrapper multi-backend: llama.cpp GGUF, Ollama o demo."""

    def __init__(self, backend: str | None = None):
        self.backend = backend or self._detect_backend()
        self._llm = None
        if self.backend == "llama_cpp":
            self._init_llama_cpp()
        elif self.backend == "ollama":
            self._init_ollama()

    @staticmethod
    def _ollama_available() -> bool:
        try:
            import urllib.request

            with urllib.request.urlopen(f"{OLLAMA_BASE_URL}/api/tags", timeout=1.5) as resp:
                return resp.status == 200
        except Exception:  # noqa: BLE001
            return False

    @classmethod
    def _detect_backend(cls) -> str:
        preferred = (LLM_BACKEND or "auto").lower()
        if preferred in {"llama_cpp", "ollama", "demo"}:
            if preferred == "llama_cpp" and not GGUF_MODEL_PATH.exists():
                return "demo"
            if preferred == "ollama" and not cls._ollama_available():
                return "demo"
            return preferred
        if GGUF_MODEL_PATH.exists():
            try:
                import llama_cpp  # noqa: F401

                return "llama_cpp"
            except ImportError:
                pass
        if cls._ollama_available():
            return "ollama"
        return "demo"

    def _init_llama_cpp(self) -> None:
        from langchain_community.llms import LlamaCpp

        self._llm = LlamaCpp(
            model_path=str(GGUF_MODEL_PATH),
            n_ctx=LLM_N_CTX,
            n_threads=LLM_N_THREADS,
            max_tokens=LLM_MAX_TOKENS,
            temperature=LLM_TEMPERATURE,
            verbose=False,
        )

    def _init_ollama(self) -> None:
        from langchain_community.llms import Ollama

        self._llm = Ollama(
            base_url=OLLAMA_BASE_URL,
            model=OLLAMA_MODEL,
            temperature=LLM_TEMPERATURE,
        )

    def generate(self, prompt: str) -> str:
        if self.backend == "demo":
            return self._demo_generate(prompt)
        return self._llm.invoke(prompt)

    @staticmethod
    def _demo_generate(prompt: str) -> str:
        """Modo demo sin LLM: respuesta estructurada basada en el contexto recuperado."""
        # Extrae bloque de contexto si existe
        ctx = ""
        if "CONTEXTO RECUPERADO" in prompt:
            try:
                ctx = prompt.split("CONTEXTO RECUPERADO", 1)[1]
                ctx = ctx.split("Pregunta del gerente:", 1)[0]
            except Exception:  # noqa: BLE001
                ctx = prompt[-2000:]
        snippets = [ln.strip(" -") for ln in ctx.splitlines() if len(ln.strip()) > 40][:6]
        body = "\n".join(f"- {s[:220]}" for s in snippets) or "- (Sin fragmentos recuperados)"
        return (
            "**[Modo demo — sin LLM local]** Se recuperó contexto de la base RAG. "
            "Instala el modelo GGUF (`python scripts/download_models.py`) u Ollama "
            "(`ollama pull phi3:mini`) para respuestas generativas completas.\n\n"
            "Hallazgos relevantes del conocimiento ProAutomation:\n"
            f"{body}\n\n"
            "Siguiente paso sugerido: valida alcance con ingeniería y solicita piezas muestra "
            "para calificar WPS antes del FAT."
        )


class RAGEngine:
    def __init__(self):
        self.vs = get_vectorstore(create_if_missing=True)
        self.llm = LLMClient()

    @property
    def backend(self) -> str:
        return self.llm.backend

    def retrieve(
        self,
        query: str,
        *,
        module_filter: str | None = None,
        k: int = TOP_K,
    ) -> list[SourceHit]:
        filt = {"module": module_filter} if module_filter and module_filter != "todos" else None
        try:
            pairs = self.vs.similarity_search_with_relevance_scores(query, k=k, filter=filt)
        except Exception:  # noqa: BLE001
            docs = self.vs.similarity_search(query, k=k, filter=filt)
            pairs = [(d, None) for d in docs]

        hits: list[SourceHit] = []
        for doc, score in pairs:
            hits.append(
                SourceHit(
                    content=doc.page_content,
                    module=doc.metadata.get("module", "desconocido"),
                    source=doc.metadata.get("source", "desconocido"),
                    score=float(score) if score is not None else None,
                )
            )
        return hits

    def query(
        self,
        question: str,
        *,
        module_filter: str | None = None,
        output_format: str = "ejecutivo",
        language: str = "es",
        session_context: str = "",
        mcc_addon: str = "",
        k: int = TOP_K,
    ) -> RAGResult:
        hits = self.retrieve(question, module_filter=module_filter, k=k)
        context = "\n\n".join(
            f"[{h.module} | {h.source}]\n{h.content}" for h in hits
        ) or "(Sin contexto recuperado)"
        prompt = build_rag_prompt(
            question,
            context,
            output_format=output_format,
            language=language,
            session_context=session_context,
            mcc_addon=mcc_addon,
        )
        answer = self.llm.generate(prompt)
        unsupported = "no contamos con esa capacidad" in answer.lower()
        return RAGResult(
            answer=answer,
            sources=hits,
            backend=self.backend,
            unsupported_capability=unsupported,
        )
