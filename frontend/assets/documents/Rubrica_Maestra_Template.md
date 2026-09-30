# Rúbrica maestra para el reto de registro de pedidos

**Centro de Gestión Agroempresarial del Oriente (CGAO)**  
**Subsede Vélez · Regional Santander**  
**Programa:** Análisis y Desarrollo de Software  
**Uso:** ejemplo formativo para el reto de registro de pedidos de productos veleños

Esta rúbrica evalúa la aplicación local que registra pedidos, consulta su estado y calcula el valor entregado. Sus criterios, puntajes y evidencias coinciden con el reto y la plantilla de evaluación en Excel. Es un ejemplo formativo; el instructor debe confirmar el tiempo y las condiciones antes de usarlo en una competencia.

La distribución de 69 puntos M, 23 J y 8 P corresponde a este reto de ADSO. La guía técnica define rangos generales para diseñar otras pruebas, no una distribución única.

## Distribución de los puntajes

| Módulo | Alcance | Puntaje | Proporción |
|---|---|---:|---:|
| A | Planeación y fundamentos | 15 | 15 % |
| B | Construcción de la aplicación | 60 | 60 % |
| C | Ordenamiento con tiempo limitado | 15 | 15 % |
| D | Cierre responsable y proceso | 10 | 10 % |
| **Total** |  | **100** | **100 %** |

| Tipo | Aplicación | Puntaje | Proporción |
|---|---|---:|---:|
| M | Medición objetiva | 69 | 69 % |
| J | Juicio técnico | 23 | 23 % |
| P | Proceso y seguridad | 8 | 8 % |
| **Total** |  | **100** | **100 %** |

La distribución cumple la regla M-J-P: M suma al menos 60 puntos, J no supera 30 puntos y P no supera 10 puntos.

## Criterios de evaluación

| ID | Módulo | Criterio | Tipo | Puntos | Evidencia para asignar el puntaje |
|---|---|---|:---:|---:|---|
| M1 | A | Reglas y cálculo del pedido | M | 7 | Alias de 2 a 40 caracteres; producto del catálogo; cantidad entera entre 1 y 100; subtotal igual a cantidad por precio unitario. Se asignan los 7 puntos si pasan todos los casos; en otro caso, 0. |
| M2 | B | Registro del pedido | M | 15 | Crea código consecutivo y guarda los campos correctos. Dos bocadillos deben sumar $15.000 y tres panelitas deben sumar $15.000. |
| M3 | B | Validación de datos | M | 12 | Rechaza alias vacío o fuera del rango y cantidad no entera o fuera del rango. El catálogo solo ofrece los dos productos del reto. Muestra un mensaje y no crea el pedido inválido. |
| M4 | B | Consulta de pedidos | M | 10 | Muestra los campos, busca alias sin distinguir mayúsculas y filtra por estado. Los resultados coinciden con los pedidos guardados. |
| M5 | B | Estado, resumen y persistencia | M | 13 | Cambia el estado, muestra la cantidad y el valor de pedidos entregados, y conserva pedidos y estados en el almacenamiento local al recargar. Los resultados coinciden con los casos de prueba. |
| M6 | C | Ordenamiento por subtotal | M | 10 | En 30 minutos ordena en orden descendente, de mayor a menor subtotal y, en empate, muestra primero el código menor. |
| M7 | D | Cierre y uso eficiente de la estación | M | 2 | Asigna 2 puntos si cierra los programas que ya no necesita, retira los archivos temporales de prueba creados para el reto y apaga el monitor o el equipo si no se va a usar de inmediato; en otro caso, 0. |
| J1 | A | Planeación técnica | J | 8 | 0: sin evidencia. 1: flujo parcial. 2: incluye las acciones requeridas. 3: flujo completo y fácil de seguir. |
| J2 | B | Interfaz de la aplicación | J | 10 | 0: inoperable. 1: fallas que dificultan el uso. 2: permite completar las tareas con claridad. 3: facilita las tareas y comunica los errores con claridad. |
| J3 | C | Explicación de la comprobación | J | 5 | 0: no explica o presenta información incorrecta. 1: menciona el resultado. 2: describe las pruebas. 3: explica las pruebas y el resultado observado. |
| P1 | D | Ergonomía y orden del puesto | P | 4 | Asigna 4 puntos si durante el reto mantiene una postura adecuada, ordena los elementos de trabajo y deja despejada la estación; en otro caso, 0. |
| P2 | D | Separación de residuos | P | 4 | Asigna 4 puntos si clasifica cada residuo en el recipiente identificado por color: blanco para aprovechables limpios y secos, verde para orgánicos aprovechables y negro para no aprovechables. Si no genera residuos, deja la estación limpia; en otro caso, 0. |

## Registro de puntajes

- En criterios **M** y **P**, registra 0 o el puntaje máximo del criterio.
- En criterios **J**, registra un nivel entero de 0 a 3. La plantilla convierte ese nivel a puntos con la fórmula `nivel ÷ 3 × puntaje máximo`.
- Anota las observaciones en la plantilla Excel y conserva las capturas o registros de los casos comprobados como evidencia de la entrega.

La plantilla de evaluación consolida automáticamente los subtotales M, J y P y calcula el resultado sobre 100 puntos.
