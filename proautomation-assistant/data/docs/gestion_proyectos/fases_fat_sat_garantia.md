# Gestión de Proyectos — Flujograma, FAT/SAT y Post-venta

## Fases estándar de un proyecto llave en mano ProAutomation

1. **Kick-off y definición de alcance**
   - RFQ, piezas muestra, CAD, volumen, takt time, normas
   - Matriz de riesgos y supuestos
2. **Diseño / Ingeniería**
   - Layout de celda, simulación robótica, diseño mecánico/eléctrico
   - Lista de equipos y BOM
3. **Maquinado y Fabricación**
   - Tooling, pedestales, fixtures, tableros
4. **Control y Programación**
   - PLC, HMI, robot, redes, seguridad
5. **FAT — Factory Acceptance Test**
   - Prueba en planta ProAutomation con criterios acordados
6. **Instalación en sitio**
   - Montaje, utilities, integración a línea
7. **SAT — Site Acceptance Test**
   - Aceptación en planta del cliente
8. **Puesta en marcha y ramp-up**
   - Ajuste de parámetros, capacitación, spare parts
9. **Garantía y post-venta**
   - Mantenimiento preventivo/correctivo y soporte de campo

## Timeline orientativo (celda robótica 3 estaciones)
| Fase | Duración típica | Notas |
|---|---|---|
| Kick-off + ingeniería conceptual | 2–3 semanas | Depende de claridad del RFQ |
| Diseño detalle + compras | 3–5 semanas | Lead time de robot/fuente |
| Fabricación tooling | 4–6 semanas | Paralelo con tableros |
| Integración + programación | 3–4 semanas | En taller |
| FAT | 1 semana | Con piezas del cliente |
| Instalación + SAT | 2–3 semanas | Incluye utilities |
| Ramp-up | 1–2 semanas | Capacitación operadores |
| **Total orientativo** | **16–24 semanas** | Validar con ingeniería |

Timelines más cortos (10–14 semanas) solo con alcance cerrado, equipos en stock y fixtures simples.

## Checklist FAT (Factory Acceptance Test)
- [ ] Layout vs. plano aprobado
- [ ] Ciclo de tiempo (cycle time) vs. objetivo
- [ ] Calidad de soldadura según criterios VT / cupón
- [ ] Interlocks y seguridad (e-stops, fencing, light curtains)
- [ ] Alarmas HMI y recuperación de fallas
- [ ] Trazabilidad / conteo de piezas
- [ ] Lista de pendientes (punch list) firmada

## Checklist SAT (Site Acceptance Test)
- [ ] Instalación mecánica/eléctrica conforme
- [ ] Utilities (aire, gas, potencia, extracción) verificadas
- [ ] Producción con piezas reales del cliente
- [ ] Capacitación operadores y mantenimiento firmada
- [ ] Entrega de manuales, programas backup, spare parts list
- [ ] Firma de aceptación y cierre de punch list

## Política de garantía / post-venta (marco típico)
- Garantía estándar de equipos de integración: según contrato (típicamente 12 meses desde SAT o horas equivalentes)
- Consumibles y desgaste (tips, pads, nozzles) excluidos
- Soporte remoto de programación incluido en periodo de garantía
- Contratos de mantenimiento preventivo disponibles (mensual / trimestral)
- Servicio de campo para correctivos y mejoras de productividad

## Entregables documentales al cliente
- Manual de operación
- Manual de mantenimiento preventivo
- Backup de programas PLC/robot
- Layout as-built
- Certificados de calibración relevantes
- Lista de refacciones recomendadas (12 meses)
