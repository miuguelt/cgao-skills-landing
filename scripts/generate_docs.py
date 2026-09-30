import os
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Robust paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "frontend", "assets")
DOCS_DIR = os.path.join(ASSETS_DIR, "documents")
SVG_DIR = os.path.join(ASSETS_DIR, "svg")
OUTPUT_DIR = os.path.join(ASSETS_DIR, "generated_docs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# SVG support check
try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    HAS_SVGLIB = True
except ImportError:
    HAS_SVGLIB = False

# Colors
DARK_BLUE = colors.HexColor("#0f172a")
DARK_SLATE = colors.HexColor("#1e293b")
SENA_GREEN = colors.HexColor("#39a900")
AMBER_GOLD = colors.HexColor("#FFBF00")

# Styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='CustomTitle',
    parent=styles['Heading1'],
    fontSize=20,
    leading=24,
    spaceAfter=12,
    textColor=DARK_BLUE
))
styles.add(ParagraphStyle(
    name='CustomSubtitle',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    spaceAfter=15,
    textColor=DARK_SLATE
))
styles.add(ParagraphStyle(
    name='CustomHeader',
    parent=styles['Heading2'],
    fontSize=14,
    leading=18,
    spaceBefore=12,
    spaceAfter=8,
    textColor=DARK_BLUE
))
styles.add(ParagraphStyle(
    name='CustomBody',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    spaceAfter=6,
    textColor=DARK_SLATE
))
styles.add(ParagraphStyle(
    name='ChecklistItem',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    spaceAfter=5,
    leftIndent=15,
    textColor=DARK_SLATE
))
styles.add(ParagraphStyle(
    name='TableHeader',
    parent=styles['Normal'],
    fontSize=7.5,
    leading=8.5,
    fontName='Helvetica-Bold',
    textColor=colors.white
))
styles.add(ParagraphStyle(
    name='TableCell',
    parent=styles['Normal'],
    fontSize=7,
    leading=8.5,
    textColor=DARK_SLATE
))
styles.add(ParagraphStyle(
    name='RubricSummary',
    parent=styles['Normal'],
    fontSize=7.7,
    leading=9,
    spaceAfter=2,
    textColor=DARK_SLATE
))

def generate_checklist():
    pdf_path = os.path.join(OUTPUT_DIR, "Checklist_Jueces_Dia0.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=30, bottomMargin=30)
    story = [
        Paragraph("Lista de preparación para evaluadores", styles['CustomTitle']),
        Paragraph("CGAO · Documento de trabajo para instructores. Ajuste a la especialidad, a las condiciones de la sede y a los protocolos vigentes.", styles['CustomSubtitle']),
    ]
    sections = [
        ("1. Antes de la prueba", [
            "Confirme el objetivo, los entregables, el tiempo y las herramientas permitidas.",
            "Pruebe equipos, programas y materiales con el mismo caso que resolverán los aprendices.",
            "Verifique que las estaciones ofrezcan condiciones equivalentes, accesibles y seguras.",
            "Revise rutas de circulación, equipos de emergencia y elementos de protección pertinentes.",
            "Disponga recipientes identificados para separar residuos según las indicaciones de la sede.",
        ]),
        ("2. Calibración de la rúbrica", [
            "Compruebe que los criterios y puntajes máximos sean claros y observables.",
            "Confirme que el total y la distribución M-J-P correspondan a las reglas de la prueba.",
            "Puntúe un caso de ejemplo y aclare las diferencias antes de iniciar.",
            "Defina cómo registrará las evidencias y resolverá dudas durante la actividad.",
        ]),
        ("3. Durante y al finalizar", [
            "Comunique las instrucciones, el tiempo y los recursos disponibles en igualdad de condiciones.",
            "Registre cada puntaje junto con la evidencia observada; solicite solo los datos necesarios.",
            "Observe postura, orden y prácticas ambientales pertinentes al reto.",
            "Anote fallas del equipo o ambigüedades para corregir la siguiente aplicación.",
            "Al cierre, retire archivos de prueba cuando sea seguro, apague equipos que no se necesiten y deje el puesto limpio.",
        ]),
    ]
    for heading, items in sections:
        story.append(Paragraph(heading, styles['CustomHeader']))
        for item in items:
            story.append(Paragraph(f"[  ]  {item}", styles['ChecklistItem']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Responsable: ____________________________________________    Fecha: __________________", styles['CustomBody']))
    doc.build(story)
    print("Checklist_Jueces_Dia0.pdf generado.")


def generate_guide():
    pdf_path = os.path.join(OUTPUT_DIR, "Guia_Tecnica_Diseno_Prueba.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=30, bottomMargin=30)
    story = [
        Paragraph("Guía de apoyo para diseñar pruebas técnicas", styles['CustomTitle']),
        Paragraph("CGAO · Los rangos y ejemplos son propuestas de diseño. Adáptelos al resultado de aprendizaje, a la especialidad y a las reglas vigentes de la sede.", styles['CustomSubtitle']),
        Paragraph("1. Estructura modular sugerida", styles['CustomHeader']),
    ]
    table_data = [
        [Paragraph('Módulo', styles['TableHeader']), Paragraph('Enfoque', styles['TableHeader']), Paragraph('Alcance', styles['TableHeader']), Paragraph('Rango', styles['TableHeader'])],
        [Paragraph('A', styles['TableCell']), Paragraph('Fundamentos y planeación', styles['TableCell']), Paragraph('Análisis del problema y diseño de la solución.', styles['TableCell']), Paragraph('15-20%', styles['TableCell'])],
        [Paragraph('B', styles['TableCell']), Paragraph('Ejecución principal', styles['TableCell']), Paragraph('Construcción del producto o prestación del servicio.', styles['TableCell']), Paragraph('50-60%', styles['TableCell'])],
        [Paragraph('C', styles['TableCell']), Paragraph('Eficiencia y calidad', styles['TableCell']), Paragraph('Comprobación, tiempos y calidad del resultado.', styles['TableCell']), Paragraph('10-15%', styles['TableCell'])],
        [Paragraph('D', styles['TableCell']), Paragraph('Sostenibilidad y seguridad', styles['TableCell']), Paragraph('Uso de recursos, ergonomía, residuos y seguridad pertinentes al reto.', styles['TableCell']), Paragraph('5-10%', styles['TableCell'])],
    ]
    table = Table(table_data, colWidths=[0.65*inch, 1.7*inch, 3.85*inch, 0.8*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f1f5f9")]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
    ]))
    story.append(table)
    story.append(Spacer(1, 5))
    story.append(Paragraph("2. Regla M-J-P", styles['CustomHeader']))
    story.append(Paragraph("<b>M - Medición objetiva:</b> defina una entrada, un resultado esperado y cómo comprobarlo. <b>J - Juicio técnico:</b> use una escala común de 0 a 3 con descriptores observables. <b>P - Proceso:</b> evalúe prácticas visibles de seguridad, orden y uso responsable de recursos.", styles['CustomBody']))
    story.append(Paragraph("Como referencia para el ejemplo de esta colección, M tiene al menos 60 puntos, J hasta 30 y P hasta 10. El reto de ADSO distribuye 69/23/8; otras pruebas deben definir su propia distribución.", styles['CustomBody']))
    story.append(Paragraph("3. Revisión previa", styles['CustomHeader']))
    story.append(Paragraph("Pruebe el tiempo, confirme que los puntajes sumen el total acordado, calibre la rúbrica con un caso de ejemplo y defina cómo guardar las evidencias según el procedimiento vigente de la sede.", styles['CustomBody']))
    doc.build(story)
    print("Guia_Tecnica_Diseno_Prueba.pdf generado.")


def generate_rubric():
    pdf_path = os.path.join(OUTPUT_DIR, "Rubrica_Maestra_Template.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(letter),
        leftMargin=30,
        rightMargin=30,
        topMargin=24,
        bottomMargin=24
    )
    story = []
    
    story.append(Paragraph("Rúbrica maestra del reto de registro de pedidos", styles['CustomTitle']))
    sub_text = """
    <b>Servicio Nacional de Aprendizaje - SENA | Regional Santander | CGAO Subsede Vélez</b><br/>
    <b>Uso:</b> Ejemplo formativo de Análisis y Desarrollo de Software
    """
    story.append(Paragraph(sub_text, styles['CustomSubtitle']))
    
    csv_path = os.path.join(DOCS_DIR, "Rubrica_Maestra_Template.csv")
    table_data = []
    module_points = {}
    type_points = {}
    
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header:
                header_labels = {
                    "ID": "ID",
                    "MODULO": "Módulo",
                    "ASPECTO": "Aspecto",
                    "CRITERIO_DETALLADO": "Criterio",
                    "TIPO_(M/J/P)": "Tipo",
                    "PUNTOS_MAX": "Máximo",
                    "DESCRIPCION_CUMPLIMIENTO": "Evidencia para puntuar",
                }
                table_data.append([
                    Paragraph(header_labels.get(value, value), styles['TableHeader'])
                    for value in header
                ])
            for row in reader:
                if len(row) != 7:
                    raise ValueError(f"La rúbrica debe tener 7 columnas; se encontraron {len(row)} en {row[0] if row else 'fila vacía'}.")
                module_points[row[1]] = module_points.get(row[1], 0) + float(row[5])
                type_points[row[4]] = type_points.get(row[4], 0) + float(row[5])
                formatted_row = [Paragraph(col, styles['TableCell']) for col in row]
                table_data.append(formatted_row)
    
    if table_data:
        t = Table(table_data, colWidths=[0.45*inch, 0.7*inch, 1.05*inch, 2.0*inch, 0.55*inch, 0.65*inch, 4.75*inch], repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(t)
    
    module_summary = " | ".join(
        f"{module} = {points:g} pts" for module, points in sorted(module_points.items())
    )
    type_labels = {"M": "Medición", "J": "Juicio", "P": "Proceso"}
    type_summary = " | ".join(
        f"{type_labels.get(kind, kind)} ({kind}) = {points:g} pts ({points:g}%)"
        for kind in ("M", "J", "P") if (points := type_points.get(kind)) is not None
    )
    summary_text = (
        f"<b>Ejemplo ADSO:</b> módulos {module_summary}; total {sum(module_points.values()):g} puntos. "
        f"M-J-P: {type_summary}. La guía propone rangos generales para otros retos."
    )
    story.append(Spacer(1, 4))
    story.append(Paragraph(summary_text, styles['RubricSummary']))
    story.append(Paragraph("En M y P registre 0 o el máximo. En J use un nivel de 0 a 3; la plantilla calcula nivel ÷ 3 × máximo.", styles['RubricSummary']))
    
    doc.build(story)
    print("Rubrica_Maestra_Template.pdf generado exitosamente.")

def create_sustainability_manual(filename, title):
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=30, bottomMargin=30)
    story = [
        Paragraph(title, styles['CustomTitle']),
        Paragraph("CGAO · Material formativo. Ajuste estas recomendaciones al reto, a las indicaciones de la sede y a los protocolos vigentes.", styles['CustomSubtitle']),
        Paragraph("1. Conducta durante la evaluación", styles['CustomHeader']),
        Paragraph("<b>Integridad:</b> trabaje con sus propios resultados y siga las instrucciones comunicadas al grupo.<br/><b>Respeto:</b> trate con cortesía a participantes, evaluadores y personal de apoyo.<br/><b>Cuidado:</b> use con responsabilidad los equipos, herramientas y espacios compartidos.", styles['CustomBody']),
        Paragraph("2. Sostenibilidad observable", styles['CustomHeader']),
        Paragraph("La guía técnica propone reservar entre el 5% y el 10% para sostenibilidad y seguridad cuando sean pertinentes. En el ejemplo de pedidos de ADSO, el módulo D suma 10 puntos: 2 por cierre y uso eficiente de la estación, 4 por ergonomía y orden y 4 por separación de residuos. Cada reto debe precisar sus propias evidencias.", styles['CustomBody']),
        Paragraph("<b>Separación de residuos:</b> el artículo 4 de la Resolución 2184 de 2019 establece blanco para residuos aprovechables limpios y secos, verde para orgánicos aprovechables y negro para no aprovechables. Siga también las indicaciones de manejo de residuos de la sede.", styles['CustomBody']),
        Paragraph("<b>Uso eficiente:</b> en pruebas digitales cierre programas que no necesita y retire archivos temporales cuando sea seguro. Apague pantallas o equipos al finalizar si no se usarán de inmediato. En pruebas con materiales, siga el método y la meta de reducción de mermas definidos para el reto.", styles['CustomBody']),
        Paragraph("<b>Ergonomía y seguridad:</b> mantenga el puesto ordenado y adopte una postura cómoda. Use los elementos de protección definidos para la actividad y mantenga despejados los pasos y las rutas señalizadas.", styles['CustomBody']),
        Paragraph("Registre evidencias según el procedimiento vigente de la sede. Evite incluir datos personales que no sean necesarios para la evaluación.", styles['CustomSubtitle']),
    ]
    doc.build(story)
    print("Manual_Sostenibilidad_y_Etica.pdf generado.")


if __name__ == "__main__":
    try:
        generate_checklist()
        generate_guide()
        generate_rubric()
        create_sustainability_manual(
            os.path.join(OUTPUT_DIR, "Manual_Sostenibilidad_y_Etica.pdf"),
            "Manual de Sostenibilidad y Código de Ética"
        )
        print("\n✅ ¡Los documentos de apoyo se generaron correctamente.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error generando documentos: {e}")
