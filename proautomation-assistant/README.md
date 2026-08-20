# ProAutomation Assistant

Asistente estratégico con **RAG local** para el Gerente de Producción de **ProAutomation S.A. de C.V.**  
Ayuda a responder RFQs, estimar costos, preparar reuniones y argumentar con normas y capacidades reales de la empresa.

Todo corre en tu computadora (CPU). Los datos no salen de tu equipo una vez descargados los modelos.

---

## Requisitos de hardware

| Recurso | Mínimo | Recomendado |
|--------|--------|-------------|
| CPU | Intel i5 / Ryzen 5 | i7 / Ryzen 7 |
| RAM | 8 GB | 16 GB |
| Disco | 10 GB libres | 12 GB+ |
| GPU | No requerida | — |
| SO | Windows 10/11, macOS, Linux | — |

---

## Instalación rápida (Opción A)

```bash
cd proautomation-assistant

# 1) Entorno virtual
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 2) Dependencias
pip install -r requirements.txt

# 3) Modelos (embeddings + opcional Phi-3 GGUF ~2.3 GB)
python scripts/download_models.py

# Si la descarga GGUF falla o quieres ir más ligero:
python scripts/download_models.py --skip-gguf

# 4) Indexar documentos (4 módulos)
python ingest.py

# 5) Abrir la interfaz
streamlit run app.py
```

Abre el navegador en: **http://localhost:8501**

---

## Alternativa con Ollama (Opción C)

Si `llama-cpp-python` o el GGUF dan problemas:

1. Instala [Ollama](https://ollama.com)
2. Ejecuta: `ollama pull phi3:mini`
3. Deja Ollama corriendo
4. Arranca la app: `streamlit run app.py`

El asistente detecta Ollama automáticamente.

---

## Primera ejecución

- La primera vez descargará embeddings (`all-MiniLM-L6-v2`, ~80 MB) y construirá el índice Chroma.
- Con LLM local, las respuestas tardan unos segundos en CPU.
- Sin LLM (modo **demo**), igual puedes buscar en la base RAG y usar el calculador de costos; las respuestas generativas serán limitadas hasta instalar Phi-3 u Ollama.

---

## Qué incluye

### 4 módulos RAG (metadata)

1. **Comercial y Capacidades** — PDFs de ProAutomation + catálogo de servicios
2. **Técnico-Normativo** — AWS D1.1, ISO 3834, ISO 10218 (guía operativa)
3. **Gestión de Proyectos** — fases, FAT/SAT, timelines, garantía
4. **Inteligencia de Mercado** — Industria 4.0, mano de obra, MIG vs Láser

### Herramientas

- Generador de propuestas (RFQ)
- Calculador de costos estimados (rangos)
- Generador de preguntas para el cliente
- Redactor de manuales / protocolos
- Estructura de presentaciones (PPT)

### MCC (capas de interacción)

1. Declaración de contexto del cliente  
2. Bifurcación de output (óptimo vs menor inversión / contra-argumentación)  
3. Verificación de certeza + KNOWN_PROBE  
4. Extracción de frameworks de decisión  

### Formatos

- Ejecutivo (máx. 3 párrafos) o Técnico (tablas)
- Español / dual (ES + términos EN) / English

---

## Estructura

```
proautomation-assistant/
├── app.py                 # Interfaz Streamlit
├── rag_engine.py          # RAG + LLM
├── tools.py               # Herramientas de negocio
├── mcc_handler.py         # Capas MCC
├── config.py              # Rutas, modelos, system prompt
├── prompts.py
├── ingest.py              # Reindexar documentos
├── requirements.txt
├── scripts/download_models.py
├── data/docs/             # 4 módulos documentales
├── data/vector_store/     # Índice Chroma (auto)
└── models/                # GGUF (descargado)
```

---

## Agregar más documentos

1. Copia PDFs o Markdown en la carpeta del módulo correspondiente bajo `data/docs/`
2. Ejecuta `python ingest.py`
3. Reinicia Streamlit

---

## Gobernanza (System Prompt)

El agente **solo** afirma capacidades de ProAutomation si están en los documentos.  
No inventa precios ni plazos exactos: da rangos y pide validar con ingeniería.

---

## Soporte interno

Empresa: ProAutomation S.A. de C.V. — Hermosillo, Sonora  
Tel: +52 (662) 262 7005
