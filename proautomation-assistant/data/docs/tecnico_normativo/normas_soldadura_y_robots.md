# Módulo Técnico-Normativo — Resumen operativo para propuestas

**Aviso:** Este documento es una guía de referencia práctica para argumentación comercial-técnica. No sustituye la compra ni la aplicación oficial de normas AWS, ISO u OEM. El gerente debe validar requisitos contractuales con ingeniería y calidad.

## AWS D1.1 — Structural Welding Code (acero)
Aplicación típica: estructuras y ensambles de acero al carbono / baja aleación.

Puntos clave para propuestas:
- **WPS / PQR / WPQ:** Calificar el procedimiento de soldadura (Welding Procedure Specification), el Procedure Qualification Record y soldadores/operadores.
- Variables esenciales: proceso (SMAW, GMAW, FCAW, etc.), material base, espesor, posición, precalentamiento, consumible y gas.
- Inspección visual (VT) como mínimo; NDT adicionales (UT, MT, PT, RT) según criticidad del cliente.
- Acero galvanizado: riesgo de porosidad por zinc vaporizado; requiere limpieza, ventilación/extracción de humos y ajuste de parámetros (a menudo GMAW pulsado).

Frase útil para el gerente:
"Para cumplir con AWS D1.1 debemos calificar el WPS con muestras del material del cliente y definir el plan de inspección antes del FAT."

## ISO 3834 — Requisitos de calidad en soldadura por fusión
Niveles: 3834-2 (completo), 3834-3 (estándar), 3834-4 (elemental).

Elementos a mencionar en propuestas de calidad:
- Revisión de requisitos contractuales de soldadura
- Personal calificado (coordinador de soldadura, soldadores)
- Equipos calibrados y mantenimiento
- Trazabilidad de consumibles y materiales
- Documentación de WPS y registros de producción
- Tratamiento de no conformidades

## ISO 10218 / RIA — Seguridad en robots industriales
- Evaluación de riesgos de la celda (ISO 12100 / ISO 10218-2 para sistemas integrados)
- Resguardo perimetral, cortinas de luz, escáneres, interlocks
- Velocidad colaborativa solo si aplica cobots certificados; la mayoría de celdas ProAutomation son industriales con fencing
- Validación de distancias de seguridad y paradas de emergencia
- Documentación de integración segura para SAT

## Resistencia de materiales y diseño de uniones
- Selección de proceso según espesor, recubrimiento y ciclo de producción
- Control de distorsión térmica (secuencia de soldadura, fixtures rígidos, láser cuando justifique)
- Criterios de aceptación dimensional del cliente (GD&T / tolerancias de junta)
- Sobre acero galvanizado / AHSS: validar metalurgia y posibles defectos (porosidad, splash, soft zones)

## Comparativa rápida de procesos (referencia técnica)
| Proceso | Ventaja | Limitación | Uso típico ProAutomation |
|---|---|---|---|
| MIG / GMAW | Versátil, buen costo | Salpicadura / humos | Brackets, estructuras, galvanizado con pulso |
| Spot | Ciclo muy corto | Acceso a ambos lados | Chapa automotriz |
| Proyección | Ideal tuercas/pernos | Tooling específico | Fasteners sobre panel |
| Láser | Precisión, baja distorsión | Mayor inversión | Uniones estéticas / AHSS selectivo |

## Checklist normativo mínimo antes de cotizar
1. Material base y recubrimiento (galvanizado, e-coat, AHSS grade)
2. Norma de soldadura exigida (AWS D1.1, ISO, OEM specific)
3. Nivel de inspección / NDT
4. Requisitos de seguridad de celda (ISO 10218)
5. Trazabilidad y nivel ISO 3834 solicitado
6. Muestras para WPS disponibles sí/no
