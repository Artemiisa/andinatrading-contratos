import os
from pathlib import Path
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

# === Paths robustos ===
# /app/services/pdf_service.py -> base del proyecto = dos niveles arriba
BASE_DIR = Path(__file__).resolve().parents[2]  # .../Andinatrading-contratos
PDF_DIR = BASE_DIR / "pdfs"
STATIC_DIR = BASE_DIR / "static"
LOGO_PATH = STATIC_DIR / "logoandinatrading.png"

PDF_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)  # por si quieres colocar el logo luego

# === Estilos ===
_styles = getSampleStyleSheet()
TITLE = ParagraphStyle(
    "TITLE", parent=_styles["Heading1"], fontName="Helvetica-Bold",
    fontSize=18, textColor=colors.HexColor("#0B3C5D"), spaceAfter=8
)
SUBTITLE = ParagraphStyle(
    "SUBTITLE", parent=_styles["Normal"], fontName="Helvetica",
    fontSize=11, textColor=colors.HexColor("#4A4A4A"), spaceAfter=6
)
BODY = ParagraphStyle(
    "BODY", parent=_styles["Normal"], fontName="Helvetica",
    fontSize=11, leading=16, textColor=colors.HexColor("#222222")
)
HILIGHT = ParagraphStyle(
    "HILIGHT", parent=_styles["Normal"], fontName="Helvetica-Bold",
    fontSize=11, textColor=colors.HexColor("#0B61A4")
)
FOOTER = ParagraphStyle(
    "FOOTER", parent=_styles["Normal"], fontName="Helvetica-Oblique",
    fontSize=9, textColor=colors.HexColor("#7A7A7A")
)

def _p(text: str, style: ParagraphStyle = BODY) -> Paragraph:
    return Paragraph(text, style)

def generar_pdf_contrato_templatizado(
    contrato_id: str,
    nombre_cliente: str,
    monto: str,
    fecha_emision: str | None = None,
    descripcion: str = "",
    duracion_horas: int = 24,
) -> str:
    """
    Genera un PDF con branding AndinaTrading.
    Variables (ID, cliente, monto, fecha, duración) salen en negrita y color.
    El logo se toma de static/logo-andinatrading.png si existe.
    """
    if not fecha_emision:
        fecha_emision = datetime.now().strftime("%d/%m/%Y %H:%M")

    filename = f"contrato_{contrato_id}.pdf"
    filepath = PDF_DIR / filename

    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title=f"Contrato {contrato_id} - AndinaTrading",
        author="AndinaTrading",
    )

    story = []

    # --- Encabezado (título + logo a la derecha)
    left = [_p("AndinaTrading", TITLE), _p("Contrato de Intermediación Financiera", SUBTITLE)]
    if LOGO_PATH.exists():
        img = Image(str(LOGO_PATH), width=3.2 * cm, height=3.2 * cm, hAlign="RIGHT")
    else:
        img = Table(
            [[_p("LOGO", ParagraphStyle("PH", parent=SUBTITLE, alignment=2))]],
            colWidths=[3.2 * cm], rowHeights=[3.2 * cm],
        )
        img.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ]))

    header = Table([[left, img]], colWidths=[None, 3.6 * cm], hAlign="LEFT")
    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [header, Spacer(1, 6)]

    # Línea separadora
    story += [
        Table([[""]], colWidths=[None],
              style=TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.75, colors.HexColor("#DDDDDD"))])),
        Spacer(1, 12)
    ]

    # Grid de variables
    grid = Table(
        [
            [_p("ID Contrato:"),         _p(contrato_id, HILIGHT)],
            [_p("Cliente:"),             _p(nombre_cliente, HILIGHT)],
            [_p("Monto total:"),         _p(f"${monto}", HILIGHT)],
            [_p("Fecha de emisión:"),    _p(fecha_emision, HILIGHT)],
            [_p("Duración del contrato:"), _p(f"{duracion_horas} horas", HILIGHT)],
        ],
        colWidths=[4.5 * cm, None], hAlign="LEFT"
    )
    grid.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story += [grid, Spacer(1, 14)]

    # Texto base del contrato
    texto_fijo = (
        "El presente documento representa un acuerdo de intermediación financiera entre "
        "<b>AndinaTrading</b> y el/la cliente indicado/a. "
        "AndinaTrading actuará como comisionista para ejecutar órdenes bursátiles en nombre del cliente, "
        "conforme a la normativa vigente y las políticas internas de la compañía.<br/><br/>"
        "El cliente autoriza expresamente a AndinaTrading a gestionar, en su nombre, la creación, "
        "modificación y cancelación de órdenes, así como el seguimiento de su estado. "
        "Las comisiones aplicables y demás condiciones particulares se detallan en el sistema y/o anexo del contrato.<br/><br/>"
        "Al aceptar este contrato, el cliente reconoce haber leído y entendido los términos y condiciones, "
        "así como la política de privacidad y tratamiento de datos. Este contrato tiene una duración mínima "
        f"de <b>{duracion_horas} horas</b>, contadas a partir de la fecha de emisión y/o aceptación."
    )
    story += [_p(texto_fijo, BODY), Spacer(1, 10)]

    # Descripción variable
    if descripcion:
        story += [_p("<b>Descripción / Observaciones</b>", HILIGHT), Spacer(1, 4),
                  _p(descripcion.replace("\n", "<br/>"), BODY), Spacer(1, 10)]

    # Firmas
    firmas = Table(
        [
            [_p("<b>Cliente</b>", BODY),          _p("<b>AndinaTrading</b>", BODY)],
            [_p(nombre_cliente, BODY),            _p("Representante Autorizado", BODY)],
            [_p("Firma: ____________________", BODY), _p("Firma: ____________________", BODY)],
        ],
        colWidths=[8 * cm, 8 * cm], hAlign="LEFT"
    )
    firmas.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story += [Spacer(1, 14), firmas, Spacer(1, 12)]

    # Footer
    story.append(_p(f"Documento generado automáticamente — AndinaTrading © {datetime.now().year}", FOOTER))

    doc.build(story)
    return str(filepath)
