# agente-dedicado-produccion
agente asistente gerencia producción planta industrial


Tu objetivo es crear un sistema RAG quequede empaquetado, listo para enviar.
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
Te deajré algunos pdfs en documentos. 

Esta arquitectura convierte al asistente en un **Multiplicador de Fuerza Comercial**, permitiendo que el gerente responda RFQs complejos en minutos, se anticipe a objeciones técnicas y presente una imagen de ultra-especialización, todo sin pisar el piso de producción del cliente.
