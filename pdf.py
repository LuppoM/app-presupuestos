import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm

def generar_pdf_presupuesto(cabecera, detalles):
    """
    Genera un PDF del presupuesto en la carpeta 'presupuestos'.
    """
    # 1. Crear carpeta 'presupuestos' si no existe
    carpeta_destino = os.path.join(os.getcwd(), "presupuestos")
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # 2. Definir ruta del PDF
    id_presu = cabecera.get('id_presupuesto') or cabecera.get('id', 0)
    nombre_pdf = f"Presupuesto_{id_presu}.pdf"
    ruta_pdf = os.path.join(carpeta_destino, nombre_pdf)

    # Documento PDF
    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=letter,
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm
    )

    story = []
    styles = getSampleStyleSheet()

    # --- COLORES ---
    VERDE_CLARO = colors.HexColor("#c8e6c9") 
    VERDE_OSCURO = colors.HexColor("#2e7d32")
    GRIS_TEXTO = colors.HexColor("#333333")

    # --- Estilos de Párrafo ---
    style_normal = styles['Normal']
    style_center = ParagraphStyle('CenterCell', parent=styles['Normal'], alignment=1)
    
    # Estilos para Totales (Centrados al medio de sus celdas)
    style_total_lbl = ParagraphStyle('TotalLbl', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=GRIS_TEXTO, alignment=1)
    style_total_val = ParagraphStyle('TotalVal', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=GRIS_TEXTO, alignment=1)

    # --- 1. BANNER ENCABEZADO ---
    ruta_logo = os.path.join(os.getcwd(), "iconom.ico")
    logo_cell = Image(ruta_logo, width=1.2*cm, height=1.2*cm) if os.path.exists(ruta_logo) else ""

    lbl_empresa = Paragraph("<font color='#2e7d32' size=14><b>Tornería Gonzalez</b></font>", style_normal)

    tabla_logo = Table([[logo_cell, lbl_empresa]], colWidths=[1.5*cm, 16*cm])
    tabla_logo.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,-1), VERDE_CLARO),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(tabla_logo)
    story.append(Spacer(1, 15))

    # --- 2. TÍTULO Y NÚMERO ---
    style_presu = ParagraphStyle('Presu', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=18, textColor=GRIS_TEXTO)
    style_num = ParagraphStyle('Num', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, textColor=GRIS_TEXTO, alignment=2)

    p_presu = Paragraph("PRESUPUESTO", style_presu)
    p_num = Paragraph(f"<br/><font color='#2e7d32' size=13>#{id_presu}</font>", style_num)

    tabla_titulo = Table([[p_presu, p_num]], colWidths=[10*cm, 7.5*cm])
    tabla_titulo.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW', (0,0), (-1,-1), 1.5, VERDE_OSCURO)
    ]))
    story.append(tabla_titulo)
    story.append(Spacer(1, 15))

    # --- 3. DATOS DE EMPRESA Y CLIENTE ---
    datos_empresa = Paragraph(
        "<b>TORNERÍA GONZALEZ</b><br/>"
        "Trabajos de Mecanizado y Tornería<br/>"
        "Teléfono: (3537 65-4177) - Taller<br/>",
        style_normal
    )

    datos_cliente = Paragraph(
        f"<b>PRESUPUESTAR A:</b><br/>"
        f"<b>Cliente:</b> {cabecera.get('cliente', '')}<br/>"
        f"<b>Trabajo:</b> {cabecera.get('descripcion', '')}<br/><br/>"
        f"<b>FECHA:</b> {cabecera.get('fecha', '')}", style_normal
    )

    tabla_datos = Table([[datos_empresa, datos_cliente]], colWidths=[9*cm, 8.5*cm])
    tabla_datos.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBELOW', (0,0), (-1,-1), 1.5, VERDE_OSCURO),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10)
    ]))
    story.append(tabla_datos)
    story.append(Spacer(1, 20))

    # --- 4. TABLA DE DETALLES (MATERIALES) ---
    style_th = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=GRIS_TEXTO, alignment=1)
    
    tabla_data = [[
        Paragraph("DESCRIPCIÓN", style_th),
        Paragraph("CANTIDAD", style_th),
        Paragraph("PRECIO UNIT.", style_th),
        Paragraph("TOTAL", style_th)
    ]]

    if detalles:
        for item in detalles:
            nombre = item.get('nombre') or item.get('material', 'Sin especificación')
            cant = item.get('cantidad', 1)
            unidad = item.get('unidad', '')
            prec = item.get('precio_venta') or item.get('precio_unitario', 0.0)
            sub = item.get('subtotal', cant * prec)

            cant_str = f"{cant} {unidad}".strip() if unidad else f"{cant}"

            tabla_data.append([
                Paragraph(str(nombre), style_normal),
                Paragraph(cant_str, style_center),
                Paragraph(f"$ {prec:.2f}", style_center),
                Paragraph(f"$ {sub:.2f}", style_center)
            ])
    else:
        tabla_data.append([
            Paragraph("Mano de Obra / Trabajo General", style_normal),
            Paragraph("1", style_center),
            Paragraph(f"$ {cabecera.get('mano_obra', 0.0):.2f}", style_center),
            Paragraph(f"$ {cabecera.get('mano_obra', 0.0):.2f}", style_center)
        ])

    tabla_items = Table(tabla_data, colWidths=[8.5*cm, 3*cm, 3*cm, 3*cm])
    tabla_items.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), VERDE_CLARO),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, VERDE_OSCURO),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tabla_items)
    story.append(Spacer(1, 15))

    # --- 5. TOTALES (ALINEADO TODO A LA IZQUIERDA Y ANCHO COMPLETO) ---
    tot_mat = cabecera.get('total_materiales', 0.0)
    mo = cabecera.get('mano_obra', 0.0)
    tot_gen = cabecera.get('total_general', 0.0)

    tabla_totales_data = [
        [Paragraph("SUBTOTAL MATERIALES:", style_total_lbl), Paragraph(f"$ {tot_mat:.2f}", style_total_val)],
        [Paragraph("MANO DE OBRA:", style_total_lbl), Paragraph(f"$ {mo:.2f}", style_total_val)],
        [Paragraph("TOTAL GENERAL:", style_total_lbl), Paragraph(f"$ {tot_gen:.2f}", style_total_val)]
    ]

    # Ocupa los 17.5 cm del ancho de página disponible
    tabla_totales = Table(tabla_totales_data, colWidths=[11.5*cm, 6*cm])
    tabla_totales.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,0), (-1,-1), VERDE_CLARO),
        ('GRID', (0,0), (-1,-1), 0.5, VERDE_OSCURO),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))

    # Se agrega directamente a la lista sin wrapper lateral para arrancar desde la izquierda
    story.append(tabla_totales)
    story.append(Spacer(1, 30))

    # --- 6. PIE DE PÁGINA ---
    p_gracias = Paragraph("<b>GRACIAS POR SU CONFIANZA</b>", ParagraphStyle('G', parent=styles['Normal'], alignment=1, fontSize=10, textColor=GRIS_TEXTO))
    tabla_pie = Table([[p_gracias]], colWidths=[17.5*cm])
    tabla_pie.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), VERDE_CLARO),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tabla_pie)

    # Construir PDF
    doc.build(story)
    return ruta_pdf