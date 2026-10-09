"""Build a synthetic, interactive project-brief PDF. Requires reportlab."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


OUTPUT = Path(__file__).resolve().parents[1] / "output" / "pdf" / "project-brief-fillable.pdf"
INK = colors.HexColor("#243A38")
MUTED = colors.HexColor("#536763")
BORDER = colors.HexColor("#AABBB5")
PAPER = colors.HexColor("#F7FAF8")


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    page = canvas.Canvas(str(OUTPUT), pagesize=A4, invariant=1)
    page.setTitle("Project brief - fillable PDF demonstration")
    page.setAuthor("Tom Vu")
    page.setSubject("Synthetic interactive form sample; no customer data")
    width, height = A4
    left, right = 48, width - 48
    page.setFillColor(INK)
    page.setFont("Helvetica", 10)
    page.drawString(left, height - 52, "TOM VU  /  DATA & WEB")
    page.setFont("Helvetica-Bold", 31)
    page.drawString(left, height - 111, "Project brief")
    page.setFillColor(MUTED)
    page.setFont("Helvetica", 11)
    page.drawString(left, height - 136, "A simple form you can fill, save and reuse.")
    page.setStrokeColor(BORDER)
    page.line(left, height - 163, right, height - 163)

    def label(text, y):
        page.setFillColor(INK)
        page.setFont("Helvetica-Bold", 10)
        page.drawString(left, y, text)

    common = dict(
        x=left, width=right - left, height=33,
        borderColor=BORDER, fillColor=PAPER, textColor=INK,
        borderWidth=0.8, borderStyle="solid", forceBorder=True,
        fontName="Helvetica", fontSize=11,
    )
    label("Contact name", 646)
    page.acroForm.textfield(name="contact_name", tooltip="Contact name", y=604, maxlen=80, **common)
    label("Project name", 574)
    page.acroForm.textfield(name="project_name", tooltip="Project name", y=532, maxlen=120, **common)
    label("Service type", 502)
    page.acroForm.choice(
        name="service_type", tooltip="Choose a service type", y=460,
        value="Choose a service", options=["Choose a service", "CSV / Python", "Website layout", "PDF form"],
        fieldFlags="combo", **common,
    )
    page.acroForm.checkbox(
        name="source_ready", tooltip="Source files are ready", x=left, y=421,
        size=15, buttonStyle="check", borderWidth=0.8, borderColor=BORDER,
        fillColor=PAPER, textColor=INK, forceBorder=True, checked=False,
    )
    page.setFillColor(INK)
    page.setFont("Helvetica", 11)
    page.drawString(left + 25, 425, "Source files are ready to share")
    label("What should the finished result do?", 386)
    page.setFillColor(MUTED)
    page.setFont("Helvetica", 9)
    page.drawString(left, 369, "Include the intended output, constraints and preferred deadline.")
    notes = dict(common, height=137, fontSize=10)
    page.acroForm.textfield(
        name="brief", tooltip="Project brief", y=217, maxlen=500,
        fieldFlags="multiline", **notes,
    )
    page.setFillColor(MUTED)
    page.setFont("Helvetica", 9)
    page.drawString(left, 189, "Open in a PDF form viewer. Save a copy after entering your answers.")
    page.drawString(left, 174, "This sample uses standard fields; viewer support can vary.")
    page.setStrokeColor(BORDER)
    page.line(left, 105, right, 105)
    page.setFillColor(MUTED)
    page.setFont("Helvetica", 8)
    page.drawString(left, 86, "SYNTHETIC DEMONSTRATION  /  No customer or personal data")
    page.drawRightString(right, 86, "1 / 1")
    page.showPage()
    page.save()
    print(OUTPUT)


if __name__ == "__main__":
    build()
