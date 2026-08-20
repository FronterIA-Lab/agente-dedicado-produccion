# Catálogo de Equipos, Consumibles y Soluciones Típicas

Documento de referencia comercial para estimación y propuestas. Los precios exactos deben validarse con ingeniería y compras.

## Robots industriales típicos en celdas ProAutomation
| Aplicación | Configuración típica | Alcance / payload orientativo | Notas |
|---|---|---|---|
| Soldadura MIG / GMAW | Robot 6 ejes + fuente pulsada | 6–20 kg | Preferido para acero galvanizado / alta velocidad |
| Spot / proyección | Robot 6 ejes + pinza de resistencia | 50–150 kg | Pedestales y tooling a medida |
| Handling + soldadura | Dual process / tool changer | 10–35 kg | Cambio rápido de herramienta |
| Soldadura láser (cuando aplica) | Robot 6 ejes + cabezal láser | 10–30 kg | Alta precisión, menor distorsión |

## Fuentes de poder y procesos
- **MIG pulsado (GMAW-P):** reduce salpicadura en galvanizado; mejora estética y reduce retrabajo.
- **MIG convencional:** volumen alto en acero al carbono sin recubrimientos críticos.
- **Resistencia / Spot:** uniones de chapa automotriz, ciclos cortos.
- **Proyección:** tuercas, pernos y componentes proyectados sobre chapa.
- **Láser:** uniones de alta precisión y baja distorsión térmica.

## Consumibles habituales
- Alambre sólido ER70S-6 (diámetros 0.8 / 0.9 / 1.0 / 1.2 mm)
- Alambre tubular (flux-cored) para aplicaciones de mayor depósito
- Gas de protección: Ar/CO2 (75/25 o 90/10 según proceso)
- Boquillas, contact tips, liners, antorcha robotizada
- Electrodos / pads de pinza para spot y proyección
- Aceites anti-salpicadura, extractores de humos, cortinas y protecciones

## Arquitecturas de celda frecuentes
1. **Celda 1 estación:** 1 robot + 1 fixture fijo o posicionador simple. Ideal prototipos / bajo volumen.
2. **Celda 2 estaciones (carousel / turntable):** carga/descarga en paralelo. Alta utilización del robot.
3. **Celda 3 estaciones:** robot + 2 posicionadores + estación de inspección/buffing. Objetivo alto throughput (ej. 8,000–12,000 piezas/día según ciclo).
4. **Línea transfer:** múltiples robots en secuencia con conveyors / AGV.

## Entregables estándar llave en mano
- Concepto y layout 2D/3D
- Diseño mecánico y eléctrico
- Fabricación de tooling / pedestales
- Programación PLC + robot
- FAT (Factory Acceptance Test)
- Instalación en sitio + SAT (Site Acceptance Test)
- Capacitación de operadores y mantenimiento
- Paquete de documentación (manuales, WPS de referencia, spare parts list)

## Casos de éxito tipificados (plantilla)
- **OEM/TIER1 automotriz:** celda MIG robotizada para brackets de chasis; reducción de retrabajo por salpicadura >30% con proceso pulsado.
- **Maquiladora de autopartes:** sistema de proyección de tuercas con control de fuerza y trazabilidad.
- **Proveedor TIER2:** pedestal de soldadura personalizado + programa de mantenimiento preventivo.

## Qué NO está en el portafolio estándar
Si el cliente solicita capacidades fuera de soldadura industrial, integración robótica, PLC, tooling o llave en mano asociadas, responder:
"No contamos con esa capacidad en nuestro portafolio estándar, pero podemos evaluar una alianza o desarrollo a la medida."
