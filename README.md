# agente-dedicado-produccion

Agente asistente para la gerencia de producción de **ProAutomation**.

## Entrega lista para usar

El sistema RAG empaquetado está en:

**[`proautomation-assistant/`](./proautomation-assistant/)**

Ahí encontrarás:
- Motor RAG (Chroma + embeddings CPU)
- 4 módulos documentales
- Herramientas (RFQ, costos, preguntas, manuales, PPT)
- Capas MCC
- Interfaz Streamlit
- Instrucciones de instalación para el gerente

```bash
cd proautomation-assistant
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/download_models.py --skip-gguf
python ingest.py
streamlit run app.py
```

Documentación detallada: [`proautomation-assistant/README.md`](./proautomation-assistant/README.md)

## Documentos de empresa incluidos

- `Proautomation-nosotros.pdf`
- `proAutomation-llave-en-mano.pdf`

(también copiados en `proautomation-assistant/data/docs/comercial/`)
