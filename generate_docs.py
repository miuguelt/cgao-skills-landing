
import os
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from svglib.svglib import svg2rlg

# Paths
ASSETS_DIR = "assets"
DOCS_DIR = os.path.join(ASSETS_DIR, "documents")
SVG_DIR = os.path.join(ASSETS_DIR, "svg")
OUTPUT_DIR = os.path.join(ASSETS_DIR, "generated_docs")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CustomTitle', parent=styles['Heading1'], fontSize=24, spaceAfter=20, textColor=colors.HexColor("#0f172a")))
styles.add(ParagraphStyle(name='CustomHeader', parent=styles['Heading2'], fontSize=16, spaceAfter=12, textColor=colors.HexColor("#1e1b4b")))
styles.add(ParagraphStyle(name='CustomBody', parent=styles['Normal'], fontSize=11, spaceAfter=8, leading=14))
styles.add(ParagraphStyle(name='ChecklistItem', parent=styles['Normal'], fontSize=12, spaceAfter=8, leading=16, leftIndent=20))

# Colors
NEON_GREEN = colors.HexColor("#39FF14")
AMBER_GOLD = colors.HexColor("#FFBF00")
DARK_BLUE = colors.HexColor("#0f172a")

def add_header(canvas, doc):
    canvas.saveState()
    # Add Logo (if possible, otherwise text)
    logo_path = os.path.join(SVG_DIR, "trophy.svg")
    try:
        drawing = svg2rlg(logo_path)
        # Scale down
        scale_factor = 0.2
        drawing.width *= scale_factor
        drawing.height *= scale_factor
        drawing.scale(scale_factor, scale_factor)
        renderPDF.draw(drawing, canvas, 40, doc.height + doc.topMargin - 50)
    except:
        pass # If logo fails, skip
    
    canvas.setFont('Helvetica-Bold', 10)
    canvas.setFillColor(colors.gray)
    canvas.drawString(inch, doc.height + doc.topMargin + 10, "CGAO SKILLS | La Fragua del Oriente")
    canvas.line(inch, doc.height + doc.topMargin + 5, doc.width + inch, doc.height + doc.topMargin + 5)
    canvas.restoreState()

def generate_checklist():
    doc = SimpleDocTemplate(os.path.join(OUTPUT_DIR, "Checklist_Jueces_Dia0.pdf"), pagesize=letter)
    story = []
    
    # Title
    story.append(Paragraph("CHECKLIST DE JUECES - DÍA CERO", styles['CustomTitle']))
    story.append(Paragraph("<b>Evento:</b> WorldSkills / Competencia CGAO", styles['CustomBody']))
    story.append(Paragraph("<b>Rol:</b> Experto Evaluador", styles['CustomBody']))
    story.append(Spacer(1, 20))
    
    # Section 1
    story.append(Paragraph("1. VERIFICACIÓN DE INFRAESTRUCTURA (AM)", styles['CustomHeader']))
    items = [
        "Energía y Conectividad: Verificar tomas de corriente (110V/220V) y acceso a red.",
        "Software Instalado: Confirmar versiones de IDEs, Compiladores y Drivers.",
        "Materiales (BOM): Conteo físico de consumibles por puesto.",
        "Sillas y Ergonomía: Ajuste de sillas y altura de mesas."
    ]
    for item in items:
        story.append(Paragraph(f"O   {item}", styles['ChecklistItem']))
    story.append(Spacer(1, 15))
    
    # Section 2
    story.append(Paragraph("2. CALIBRACIÓN DE LA RÚBRICA (PM)", styles['CustomHeader']))
    items = [
        "Lectura Cruzada: Todos los jueces leen la prueba completa.",
        "Detección de Errores: ¿Hay cotas imposibles? ¿Hay ambigüedad?",
        "Prueba Piloto (Juicio): Evaluar un ejemplo 'Fantasma'.",
        "Firma de Compromiso: Aceptación del código de ética y confidencialidad."
    ]
    for item in items:
        story.append(Paragraph(f"O   {item}", styles['ChecklistItem']))
    story.append(Spacer(1, 15))
    
    # Section 3
    story.append(Paragraph("3. SEGURIDAD Y SALUD (HSE)", styles['CustomHeader']))
    items = [
        "Extintores vigentes y ubicados.",
        "Salidas de emergencia despejadas.",
        "Botiquín de primeros auxilios disponible.",
        "EPP revisado para cada juez y competidor."
    ]
    for item in items:
        story.append(Paragraph(f"O   {item}", styles['ChecklistItem']))
    story.append(Spacer(1, 30))
    
    # Footer / Signature
    story.append(Paragraph("__________________________", styles['Normal']))
    story.append(Paragraph("Firma del Experto", styles['CustomBody']))
    
    doc.build(story)
    print("Checklist PDF generated.")

def generate_guide():
    doc = SimpleDocTemplate(os.path.join(OUTPUT_DIR, "Guia_Tecnica_Diseno_Prueba.pdf"), pagesize=letter)
    story = []
    
    story.append(Paragraph("GUÍA TÉCNICA DE DISEÑO DE PRUEBA", styles['CustomTitle']))
    story.append(Paragraph("<b>Versión:</b> 2.4 (CGAO SKILLS)", styles['CustomBody']))
    story.append(Paragraph("<b>Objetivo:</b> Estandarizar la creación de proyectos de prueba.", styles['CustomBody']))
    story.append(Spacer(1, 20))
    
    # Table 1
    story.append(Paragraph("1. FICHA TÉCNICA DEL PROYECTO", styles['CustomHeader']))
    data = [
        ['Componente', 'Descripción', 'Peso Sugerido'],
        ['Módulo A: Fundamentos', 'Evaluación de conocimientos teóricos.', '15-20%'],
        ['Módulo B: Ejecución', 'Desarrollo del producto/servicio (Core Skill).', '50-60%'],
        ['Módulo C: Velocidad', 'Tareas cronometradas (Speed Test).', '10-15%'],
        ['Módulo D: Sostenibilidad', 'Gestión de residuos y HSE.', '5-10%']
    ]
    t = Table(data, colWidths=[2*inch, 3*inch, 1.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    # Section 2
    story.append(Paragraph("2. MATRIZ DE EVALUACIÓN (CRITERIOS)", styles['CustomHeader']))
    story.append(Paragraph("<b>Tipo M (Measurement):</b> Mínimo 60%. Objetivos, binarios.", styles['CustomBody']))
    story.append(Paragraph("<b>Tipo J (Judgment):</b> Máximo 30%. Subjetivos, escala 0-3.", styles['CustomBody']))
    story.append(Paragraph("<b>Tipo P (Process):</b> Máximo 10%. Buenas prácticas.", styles['CustomBody']))
    story.append(Spacer(1, 20))
    
    # Section 3
    story.append(Paragraph("3. INFRAESTRUCTURA REQUERIDA", styles['CustomHeader']))
    story.append(Paragraph("- Lista Maestra de Herramientas (Toolbox)", styles['ChecklistItem']))
    story.append(Paragraph("- Lista de Materiales Consumibles (BOM)", styles['ChecklistItem']))
    story.append(Paragraph("- Requisitos de Software", styles['ChecklistItem']))
    
    doc.build(story)
    print("Guide PDF generated.")

def generate_rubric():
    doc = SimpleDocTemplate(os.path.join(OUTPUT_DIR, "Rubrica_Maestra_Template.pdf"), pagesize=landscape(letter))
    story = []
    
    story.append(Paragraph("RÚBRICA MAESTRA (TEMPLATE)", styles['CustomTitle']))
    
    # Read CSV
    csv_path = os.path.join(DOCS_DIR, "Rubrica_Maestra_Template.csv")
    data = []
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
    
    if data:
        # Style the table
        t = Table(data, colWidths=[0.5*inch, 0.8*inch, 1.2*inch, 3*inch, 1*inch, 1*inch, 2.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(t)
    
    doc.build(story)
    print("Rubric PDF generated.")

def create_sustainability_manual(filename, title, logo_path):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Header con Logo
    if logo_path and os.path.exists(logo_path):
        drawing = svg2rlg(logo_path)
        drawing.scale(0.5, 0.5)
        story.append(drawing)
        story.append(Spacer(1, 20))
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#39FF14'),
        alignment=1,
        spaceAfter=30
    )
    story.append(Paragraph(title, title_style))
    
    # Contenido: Código de Ética
    story.append(Paragraph("1. CÓDIGO DE ÉTICA Y CONDUCTA", styles['Heading2']))
    ethics_text = """
    Todos los participantes (Competidores, Expertos y Jefes de Taller) se comprometen a:
    <br/><br/>
    • <b>Integridad:</b> Competir con honestidad, respetando las reglas y a los demás.<br/>
    • <b>Transparencia:</b> Aceptar las evaluaciones y decisiones técnicas con profesionalismo.<br/>
    • <b>Excelencia:</b> Buscar el más alto estándar técnico sin atajos desleales.<br/>
    • <b>Respeto:</b> Tratar a todos los participantes sin discriminación ni hostilidad.
    """
    story.append(Paragraph(ethics_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Contenido: Sostenibilidad (Green Skills)
    story.append(Paragraph("2. ESTÁNDARES DE SOSTENIBILIDAD (GREEN SKILLS)", styles['Heading2']))
    green_text = """
    Siguiendo los lineamientos de WorldSkills Lyon 2024, CGAO Skills incorpora la sostenibilidad como criterio de evaluación transversal (5% del puntaje):
    <br/><br/>
    • <b>Gestión de Residuos:</b> Clasificación correcta de sobrantes (Reciclable, Ordinario, Peligroso).<br/>
    • <b>Eficiencia Energética:</b> Uso racional de equipos eléctricos y apagado en tiempos muertos.<br/>
    • <b>Materiales:</b> Optimización del corte y uso de materias primas (Mínimo Desperdicio).<br/>
    • <b>Seguridad (HSE):</b> El puesto de trabajo debe permanecer limpio y seguro en todo momento.
    """
    story.append(Paragraph(green_text, styles['Normal']))
    story.append(Spacer(1, 20))

    # Juramento
    story.append(Paragraph("3. JURAMENTO DEL COMPETIDOR", styles['Heading2']))
    oath_text = """
    <i>"Prometo competir con honor, respetando a mis compañeros y a los jueces, siguiendo las reglas del oficio y demostrando que la excelencia técnica es el camino para transformar nuestro país."</i>
    """
    story.append(Paragraph(oath_text, styles['Italic']))
    
    doc.build(story)

if __name__ == "__main__":
    try:
        generate_checklist()
        generate_guide()
        generate_rubric()
        
        # 4. Generar Manual de Sostenibilidad y Ética (NUEVO)
        logo_path = os.path.join(SVG_DIR, "trophy.svg")
        create_sustainability_manual(
            os.path.join(OUTPUT_DIR, "Manual_Sostenibilidad_y_Etica.pdf"),
            "Manual de Sostenibilidad y Código de Ética",
            logo_path
        )

        print("\n✅ ¡Todos los documentos han sido generados exitosamente!")
    except Exception as e:
        print(f"Error generating documents: {e}")
