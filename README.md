# agente-dedicado-produccion
agente asistente gerencia producción planta industrial


Tu objetivo es crear un sistema RAG quequede empaquetado, listo para enviar.
Es para el gerente de producción de la empresa Pro-Automation
Este es el objetivo:
**Arquitectura de Agente RAG** diseñada específicamente para este contexto:

---

### 1. Capa de Conocimiento (El "Cerebro" RAG)
La base de datos vectorial debe estar dividida en **4 módulos documentales** claramente etiquetados (metadata):

- **Módulo Comercial y de Capacidades (¿Qué vendemos?):**
  - Contenido: El PDF ("llave-en-mano"), catálogos de robots, fichas técnicas de soldadoras MIG/de resistencia, lista de consumibles, y casos de éxito anteriores.
  - *Uso:* El gerente pregunta *"¿Podemos hacer un sistema de soldadura por proyección para piezas automotrices?"* y el RAG extrae exactamente qué servicios y equipos ofrece la empresa.

- **Módulo Técnico-Normativo (Estándares de la industria):**
  - Contenido: Normas AWS (American Welding Society) D1.1, ISO 3834 (Requisitos de calidad en soldadura), ISO 10218 (Seguridad en robots), y estándares de resistencia de materiales.
  - *Uso:* Fundamentar técnicamente las propuestas, asegurando que el diseño cumple con la reglamentación internacional.

- **Módulo de Gestión de Proyectos (¿Cómo lo ejecutamos?):**
  - Contenido: Flujogramas de las fases del proyecto (Diseño → Maquinado → Control → Instalación → Puesta en Marcha), checklists de FAT (Factory Acceptance Test) y SAT (Site Acceptance Test), y políticas de garantía/post-venta.
  - *Uso:* El gerente pide *"Dame un timeline estándar para una celda robótica de 3 estaciones"* y el agente genera el cronograma base.

- **Módulo de Inteligencia de Mercado (El contexto externo):**
  - Contenido: Tendencias en Industria 4.0, escasez de mano de obra calificada en soldadura, y comparativas teóricas entre soldadura MIG vs. Láser.
  - *Uso:* Ayudar al gerente a argumentar por qué el cliente *necesita* automatizar ahora.

---

### 2. Capa de Herramientas (Actions / MCP - Model Context Protocol)
Para que el asistente no solo "hable", sino que **produzca valor tangible** para el gerente, debe tener estas funciones:

- **Generador de Propuestas Técnico-Económicas (RFQ Responder):** El gerente sube una solicitud de cotización (RFQ) del cliente. El agente lee los requisitos, los cruza con el Módulo de Capacidades, y genera un borrador de propuesta con la solución técnica adecuada, los entregables y las fases del proyecto.
- **Calculador de Costos Estimados (Regla de 3 simple):** Basado en datos históricos generales cargados en el RAG, puede estimar horas-hombre de ingeniería, costos de consumibles y tiempos de instalación para dar un precio aproximado al gerente.
- **Generador de Preguntas para el Cliente:** Antes de una reunión, el agente analiza la industria del cliente y genera un listado de preguntas técnicas clave que el gerente debe hacer para no tener sorpresas (ej. *"¿Qué tipo de recubrimiento tiene la pieza? ¿Cuál es la tolerancia de la junta?"*).
- **Redactor de Manuales y Protocolos:** Genera borradores de planes de mantenimiento preventivo y manuales de operación para entregar al cliente final en la etapa de post-venta.

---

### 3. Capa de Interacción y Formato (Output)
El gerente necesita respuestas rápidas y listas para usar en juntas directivas o con clientes. El agente debe poder:

- **Responder en formato ejecutivo:** Resúmenes de máximo 3 párrafos.
- **Responder en formato técnico:** Con tablas comparativas (ej. *Ventajas de nuestro robot vs. competencia genérica*).
- **Generar presentaciones (PPT):** Crear una estructura de diapositivas a partir de un concepto.
- **Idioma dual:** Español para el cliente local, pero con terminología técnica en inglés (MIG, GMAW, RIA, etc.) para proyectos con ingenieros extranjeros.

---

### 4. Gobernanza y Prompt de Sistema (El "ADN" del Agente)

Debes configurar el *System Prompt* de la siguiente manera para evitar riesgos:

> *"Eres el Asistente Estratégico del Gerente de ProAutomation. Tu objetivo es ayudarlo a ganar proyectos de automatización y soldadura.*  
> **Regla 1:** Para responder sobre las capacidades de ProAutomation, **solo** usas la información contenida en los documentos subidos (catálogos, PDFs, casos de éxito). Si no encuentras una capacidad específica, di: 'No contamos con esa capacidad en nuestro portafolio estándar, pero podemos evaluar una alianza o desarrollo a la medida.'  
> **Regla 2:** Para responder sobre normas, procesos y soldadura, usas tu conocimiento general (entrenamiento base) complementado con las normas técnicas cargadas.  
> **Regla 3:** No inventes precios ni tiempos de entrega exactos; ofrece rangos estimados basados en proyectos típicos y sugiere al gerente validar con el área de ingeniería.  
> **Regla 4:** Tu tono debe ser proactivo, comercial y técnicamente impecable, posicionando a ProAutomation como un socio experto, no solo un proveedor."*

---

### Ejemplo de Flujo de Trabajo (Caso Práctico)

1. **Entrada del Gerente:** *"Tengo una reunión mañana con una maquiladora de autopartes. Necesitan soldar 10,000 piezas/día de acero galvanizado. ¿Qué arquitectura de celda les proponemos y qué normativa debo mencionar?"*
2. **Acción del RAG:**
   - Busca en el Módulo de Capacidades qué robots y fuentes de poder maneja ProAutomation para acero galvanizado (soldadura MIG con pulsos).
   - Busca en el Módulo Normativo las especificaciones de soldadura sobre acero galvanizado (riesgo de porosidad, necesidad de extracción de humos).
   - Busca en el Módulo de Gestión un layout típico de celda robotizada con 2 posicionadores para alcanzar esa producción.
3. **Salida del Asistente:**
   - *"Propongo una celda robótica con brazo de 6 ejes, fuente de poder pulsada (para minimizar salpicadura en galvanizado), y un sistema de enganche rápido de herramienta. Para cumplir con la AWS D1.1, debemos calificar el procedimiento de soldadura (WPS) con las muestras de su material. Adjunto un borrador de carta de presentación con estos argumentos y un cronograma tentativo de 16 semanas para entrega llave en mano. ¿Quieres que ajuste los tiempos?"*

---

Esta es mi propuesta de arquitectura.
🧩 Arquitectura RAG para ProAutomation – Versión Ligera (CPU)

1. Requisitos de Hardware Mínimos (para el gerente)

CPU: Intel Core i5 / AMD Ryzen 5 (o equivalente)
RAM: 8 GB (16 GB recomendado)
Almacenamiento: 10 GB libres (para modelos y documentos)
No se necesita GPU.
Sistema operativo: Windows 10/11, macOS o Linux (usaremos herramientas multiplataforma).
2. Componentes Técnicos

🧠 Modelo de Lenguaje (LLM) – CPU nativo

Usaremos modelos cuantizados en formato GGUF que corren eficientemente en CPU gracias a la librería llama-cpp-python.

Recomendado: Phi-3-mini-4k-instruct.Q4_K_M.gguf (3.8B parámetros, ~2.5 GB) – muy bueno en razonamiento y seguimiento de instrucciones.
Alternativa: Qwen2-1.5B-Instruct.Q4_K_M.gguf (más ligero, ~1 GB) si el hardware es justo.
Embeddings: all-MiniLM-L6-v2 (modelo de Hugging Face, 384 dimensiones, ~80 MB) – ligero y rápido.
🗄️ Base de Datos Vectorial – en memoria / local

Usaremos ChromaDB en modo persistente (guarda en disco) o FAISS con índice plano. Chroma es más fácil de manejar para el gerente.

🧩 Framework de Orquestación

LangChain con integración con llama-cpp-python para el LLM y Chroma para la base vectorial. Es flexible y permite implementar fácilmente las herramientas del asistente.

📦 Empaquetado e Instalación

Opción A (más sencilla): Crear un script Python que instale las dependencias y descargue los modelos automáticamente. El gerente solo ejecuta pip install -r requirements.txt y luego python app.py.
Opción B (más profesional): Empaquetar con PyInstaller un solo ejecutable (.exe para Windows). Esto oculta la complejidad pero puede hacer el archivo más pesado.
Opción C: Usar Ollama (instalador simple) y configurar el RAG para que se conecte a la API local de Ollama, mientras el código de la aplicación maneja la base vectorial y las herramientas. Esto da una instalación en dos pasos.
🖥️ Interfaz de Usuario

Streamlit – genera una interfaz web local (accesible desde el navegador) con apenas unas líneas de código. El gerente solo abre http://localhost:8501 después de ejecutar el script.
Alternativa: Gradio (similar) o una interfaz CLI para los más técnicos.
3. Integración del MCC en el Flujo del Asistente

El MCC no es solo un "prompt", sino una metodología de interacción. Implementaremos sus cuatro capas como pasos guiados que el asistente ejecuta o sugiere al gerente.

🔹 Capa 1 – Declaración de Contexto

En el sistema: Al iniciar una conversación, el asistente preguntará al gerente:
"¿Cuál es la situación de este cliente? (industria, volumen, restricciones técnicas, plazo, presupuesto aproximado)"
Estas respuestas se almacenan como metadatos de la sesión y se inyectan en cada consulta posterior.
🔹 Capa 2 – Bifurcación de Output

Herramienta: el asistente puede ofrecer botones/opciones:
"Dame dos enfoques: uno técnico-óptimo y otro con menor inversión inicial"
"Muestra la contra-argumentación que podría hacer el cliente"
Esto se implementa como funciones que generan múltiples respuestas divergentes y las presenta en paralelo.
🔹 Capa 3 – Verificación de Certeza

Integración: Después de dar una respuesta, el asistente etiqueta automáticamente las afirmaciones que no están respaldadas por los documentos cargados (usando un sistema de citas). Además, puede activar un modo "Pregúntame algo que ya sepas para calibrar mi confianza" (KNOWN_PROBE) como parte del onboarding.
🔹 Capa 4 – Extracción de Frameworks

Herramienta: El asistente puede, a petición, transformar su respuesta en un marco de decisión (lista de criterios, preguntas clave, variables a evaluar) en lugar de una solución cerrada. Por ejemplo:
"En lugar de darte la celda final, te doy los 5 criterios que debes evaluar con el cliente para definirla".
⚙️ Implementación Técnica

Estas capas se implementan como componentes del prompt que se añaden dinámicamente según el modo seleccionado por el gerente (a través de la interfaz).
Las herramientas (Generador de Propuestas, Calculador de Costos, etc.) se programan como funciones Python que el asistente puede invocar (usando @tool de LangChain) cuando el contexto lo requiere.
4. Estructura de Archivos para la Aplicación

text
proautomation-assistant/
├── app.py               # Punto de entrada (Streamlit)
├── rag_engine.py        # Lógica de RAG (carga de documentos, embeddings, búsqueda)
├── tools.py             # Herramientas (propuestas, costos, preguntas, manuales)
├── mcc_handler.py       # Lógica de los pasos del MCC
├── config.py            # Configuración (rutas, modelos, etc.)
├── requirements.txt     # Dependencias
├── data/
│   ├── docs/            # PDFs y documentos de los 4 módulos (se incluyen pre-procesados)
│   └── vector_store/    # Donde Chroma guarda los índices (creado automáticamente)
├── models/
│   └── phi-3-mini.Q4_K_M.gguf   # (descargado automáticamente o incluido)
└── README.md            # Instrucciones para el gerente
5. Pasos Concretos para Construir el Sistema

Preparar los documentos:

Tomar los PDFs de los cuatro módulos y convertirlos a texto (o usar pypdf para cargarlos directamente).
Crear un script de ingesta que divida en fragmentos (chunks), genere embeddings con all-MiniLM-L6-v2 y los guarde en Chroma con metadatos (módulo, tipo, etc.).
Configurar el LLM local:

Instalar llama-cpp-python y descargar el modelo GGUF de Hugging Face (con un script que lo haga automáticamente).
Crear un wrapper para que LangChain pueda usarlo.
Desarrollar el motor RAG:

Función query(query_text, metadata_filter=None) que:

Recupera los fragmentos más relevantes de Chroma (usando el filtro de metadatos si se especifica).
Construye un prompt con el contexto y la pregunta.
Llama al LLM y devuelve la respuesta + las fuentes.
Implementar las herramientas del MCC y las funciones de negocio:

generar_propuesta(cliente_info): usa RAG para extraer capacidades, luego genera el borrador.
calcular_costo(especificaciones): reglas simples + datos históricos.
generar_preguntas(industria): prompt específico.
etc.
Construir la interfaz en Streamlit:

Un chat con opciones laterales para cambiar el "modo" (ejecutivo/técnico, idioma, capa MCC activa).
Botones para invocar las herramientas directamente.
Visualización de fuentes y citas.
Empaquetar y documentar:

Escribir un README.md con instrucciones claras: instalar Python, crear entorno virtual, ejecutar pip install -r requirements.txt, luego streamlit run app.py.
Opcional: usar pyinstaller para generar un .exe que incluya todo.
6. Consideraciones para el Gerente (usuario final)

La primera ejecución tardará unos minutos en descargar los modelos (si no están incluidos) y construir el índice vectorial.
Después, la respuesta será casi instantánea (1-3 segundos en CPU moderna).
Todo funciona sin Internet una vez descargados los modelos y documentos.
El sistema es seguro porque los datos nunca salen de su computadora.

----------------

Te deajré algunos pdfs en documentos. 

Esta arquitectura convierte al asistente en un **Multiplicador de Fuerza Comercial**, permitiendo que el gerente responda RFQs complejos en minutos, se anticipe a objeciones técnicas y presente una imagen de ultra-especialización, todo sin pisar el piso de producción del cliente.
