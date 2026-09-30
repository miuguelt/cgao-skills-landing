# Mapa del proyecto CGAO Skills

La imagen Docker publica la carpeta `frontend/` de la raíz del repositorio. Esa carpeta contiene el sitio que se debe mantener.

## Fuentes de contenido

- `frontend/index.html` contiene la página y los enlaces a sus recursos.
- `frontend/css/styles.css` define el diseño adaptable y los estados de foco.
- `frontend/assets/documents/` contiene el reto formativo, el Excel y las fuentes editables de la rúbrica y las guías.
- `frontend/assets/generated_docs/` contiene los PDF descargables y una copia sincronizada del Excel.
- `scripts/generar_excel_evaluacion.py` genera la planilla desde los criterios del reto.
- `scripts/generate_docs.py` genera los PDF desde las fuentes vigentes.
- `tests/` comprueba la página, los puntajes, las copias publicadas y la correspondencia entre el Word y la rúbrica.

## Rúbrica de ADSO

El reto de registro de pedidos es un ejemplo formativo. Sus 100 puntos se distribuyen en M = 69, J = 23 y P = 8; el módulo D suma 10 puntos e incluye cierre eficiente de recursos digitales, ergonomía, orden y separación de residuos. La guía técnica define rangos generales para diseñar otras pruebas.

El Excel sirve para tres participantes. Las celdas amarillas se completan a mano y el libro calcula los subtotales y el puntaje final. Los documentos publicados se conservan centralizados en `frontend/assets/documents/` y `frontend/assets/generated_docs/`.

## Validación local

- `npm test`
- `python -m unittest discover -s tests -v`
- `python scripts/generate_docs.py`
