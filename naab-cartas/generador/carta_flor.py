# -*- coding: utf-8 -*-
"""Carta NAAB — Flor (Capricornio / La Matriarca / Ónix)"""
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

# ---------- fonts ----------
pdfmetrics.registerFont(TTFont("Cormorant", "Cormorant-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Cormorant-Md", "Cormorant-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Cormorant-SB", "Cormorant-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Cormorant-It", "Cormorant-Italic.ttf"))

# ---------- brand palette ----------
SAND      = HexColor("#EFE6D8")   # fondo
SAND_DEEP = HexColor("#E6D9C5")
TERRA     = HexColor("#B5674C")   # terracota
GOLD      = HexColor("#A8894E")   # oro envejecido
SAGE      = HexColor("#8A9B84")   # verde salvia
INK       = HexColor("#3E362E")   # texto principal (café oscuro)
INK_SOFT  = HexColor("#6B5F52")

W, H = A4
M = 22 * mm  # margin

# ---------- helpers ----------

def torus_logo(c, cx, cy, r, color=GOLD, lw=0.9):
    """NAAB torus mark: concentric ellipses rotating — a wireframe torus seen front-on."""
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    # outer + inner circle of the torus
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.circle(cx, cy, r * 0.38, stroke=1, fill=0)
    # meridian ellipses
    n = 8
    for i in range(n):
        ang = 180.0 * i / n
        c.saveState()
        c.translate(cx, cy)
        c.rotate(ang)
        # ellipse spanning the ring width
        rx, ry = r, r * 0.38
        c.ellipse(-rx, -ry, rx, ry, stroke=1, fill=0)
        c.restoreState()
    c.restoreState()


def wordmark(c, cx, y, size=30, tracking=10, color=INK):
    """N A A B letter-spaced wordmark, centered at cx."""
    txt = "NAAB"
    c.setFont("Cormorant-SB", size)
    c.setFillColor(color)
    widths = [pdfmetrics.stringWidth(ch, "Cormorant-SB", size) for ch in txt]
    total = sum(widths) + tracking * (len(txt) - 1)
    x = cx - total / 2
    for ch, w in zip(txt, widths):
        c.drawString(x, y, ch)
        x += w + tracking


def hairline(c, x1, x2, y, color=GOLD, lw=0.6):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(x1, y, x2, y)


def diamond(c, cx, cy, s=2.4, color=GOLD):
    c.saveState()
    c.setFillColor(color)
    p = c.beginPath()
    p.moveTo(cx, cy + s)
    p.lineTo(cx + s, cy)
    p.lineTo(cx, cy - s)
    p.lineTo(cx - s, cy)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


def section_divider(c, y, label=None):
    x1, x2 = M + 8 * mm, W - M - 8 * mm
    hairline(c, x1, W/2 - 6*mm, y, GOLD, 0.5)
    hairline(c, W/2 + 6*mm, x2, y, GOLD, 0.5)
    diamond(c, W/2, y, 2.2, GOLD)


styles = {
    "eyebrow": ParagraphStyle("eyebrow", fontName="Cormorant-Md", fontSize=10.5,
                              leading=13, textColor=GOLD, alignment=TA_CENTER,
                              spaceBefore=0, spaceAfter=0, tracking=0),
    "h": ParagraphStyle("h", fontName="Cormorant-SB", fontSize=21, leading=24,
                        textColor=TERRA, alignment=TA_CENTER),
    "body": ParagraphStyle("body", fontName="Cormorant", fontSize=12.3, leading=16.8,
                           textColor=INK, alignment=TA_JUSTIFY),
    "quote": ParagraphStyle("quote", fontName="Cormorant-It", fontSize=13,
                            leading=17.5, textColor=INK_SOFT, alignment=TA_CENTER),
}


def draw_bg(c):
    c.setFillColor(SAND)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    # frame
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.rect(M * 0.55, M * 0.55, W - 1.1 * M * 0.55 * 2 + (1.1*M*0.55*2 - (W - M*0.55*2))*0 , 0, stroke=0, fill=0)
    c.rect(12 * mm, 12 * mm, W - 24 * mm, H - 24 * mm, stroke=1, fill=0)
    c.setLineWidth(0.4)
    c.rect(14 * mm, 14 * mm, W - 28 * mm, H - 28 * mm, stroke=1, fill=0)


def para(c, text, style, x, y_top, width):
    p = Paragraph(text, style)
    w, h = p.wrap(width, H)
    p.drawOn(c, x, y_top - h)
    return y_top - h


# ---------- content ----------
NUM_TXT = ("Naciste bajo el número de la culminación y la totalidad. El 9 no es un final "
           "en el sentido de clausura, sino de plenitud — el momento en que todas las "
           "lecciones de los ciclos anteriores se integran en sabiduría. Quienes llevan "
           "este número no están aquí para empezar caminos, sino para completarlos: "
           "llegan a cerrar círculos que otros dejaron abiertos, a perdonar lo que parecía "
           "imperdonable, a ver el cuadro completo donde otros solo ven fragmentos. "
           "Tu alma es vieja en el mejor sentido: ya sabe cómo terminan las historias, "
           "y aun así elige amarlas.")

SIGN_TXT = ("Naciste en el umbral del invierno, cuando la naturaleza guarda su fuerza "
            "bajo tierra para resistir. Capricornio es el signo de la perseverancia "
            "silenciosa: no es el brillo del que llega primero, sino la certeza del que "
            "llega siempre. Los nacidos bajo este signo comprenden el valor del tiempo — "
            "saben que lo que vale la pena no se improvisa, se cultiva. "
            "Tu ambición no es ruido: es raíz.")

ELEM_TXT = ("En ti, la Tierra se vive como la esencia femenina la conoce: no como "
            "territorio que se conquista, sino como cuerpo que sostiene. Eres el suelo "
            "donde otros encuentran dónde pararse. Tu fuerza no empuja — abraza; "
            "no dirige — nutre. La tierra femenina no pregunta hacia dónde vamos: "
            "pregunta quién necesita descansar, quién necesita raíz, quién necesita "
            "volver a casa. Y todo lo que descansa en ella, florece.")

ARQ_TXT = ("Eres la que sostiene linajes enteros. La Matriarca no asciende a la montaña — "
           "ella <i>es</i> la montaña: el punto fijo alrededor del cual la familia, el clan, "
           "la tribu, encuentran su centro. Su poder no viene de mandar sino de sostener: "
           "nada de lo suyo cae, porque ella es el cimiento. Combinada con tu número 9, "
           "tu figura se completa: eres la Matriarca al final del ciclo, la que ya no "
           "sostiene por obligación sino por amor consciente — la que ha aprendido que "
           "sostener a otros y soltarse a sí misma pueden ser el mismo gesto.")

QTZ_TXT = ("Tu piedra es el Ónix — la piedra negra de la fortaleza serena. Desde la "
           "antigüedad se le asocia con la protección, el anclaje y la resistencia "
           "silenciosa: absorbe lo que pesa para que tú no lo cargues. No es una piedra "
           "que brilla hacia afuera; es una piedra que sostiene hacia adentro — como tú. "
           "Llevarla cerca del corazón es un recordatorio de tu naturaleza: la fuerza "
           "más profunda no es la que se ve, sino la que sostiene todo lo que se ve.")


def eyebrow(c, y, text):
    c.setFont("Cormorant-Md", 10)
    c.setFillColor(GOLD)
    # manual letterspacing
    t = " ".join(text)  # simple spaced caps
    w = pdfmetrics.stringWidth(t, "Cormorant-Md", 10)
    c.drawString(W/2 - w/2, y, t)


def heading(c, y, text):
    c.setFont("Cormorant-SB", 20)
    c.setFillColor(TERRA)
    w = pdfmetrics.stringWidth(text, "Cormorant-SB", 20)
    c.drawString(W/2 - w/2, y, text)


c = canvas.Canvas("/home/claude/naab/Carta_NAAB_Flor.pdf", pagesize=A4)
c.setTitle("Carta NAAB — Flor")
c.setAuthor("NAAB")

# ================= PAGE 1 — portada =================
draw_bg(c)

torus_logo(c, W/2, H - 78 * mm, 24 * mm, GOLD, 0.85)
wordmark(c, W/2, H - 118 * mm, 34, 12, INK)

c.setFont("Cormorant-It", 12.5)
c.setFillColor(INK_SOFT)
sub = "el centro del que todo emana"
w = pdfmetrics.stringWidth(sub, "Cormorant-It", 12.5)
c.drawString(W/2 - w/2, H - 128 * mm, sub)

section_divider(c, H - 148 * mm)

eyebrow(c, H - 165 * mm, "CARTA DE NACIMIENTO")

c.setFont("Cormorant-SB", 30)
c.setFillColor(INK)
name = "Flor"
w = pdfmetrics.stringWidth(name, "Cormorant-SB", 30)
c.drawString(W/2 - w/2, H - 178 * mm, name)

c.setFont("Cormorant", 12)
c.setFillColor(INK_SOFT)
d = "23 de diciembre de 1981"
w = pdfmetrics.stringWidth(d, "Cormorant", 12)
c.drawString(W/2 - w/2, H - 187 * mm, d)

# identity summary line
c.setFont("Cormorant-Md", 12.5)
c.setFillColor(SAGE)
line = "Capricornio  ·  Tierra  ·  La Matriarca  ·  Número 9  ·  Ónix"
w = pdfmetrics.stringWidth(line, "Cormorant-Md", 12.5)
c.drawString(W/2 - w/2, H - 202 * mm, line)

section_divider(c, H - 216 * mm)

c.setFont("Cormorant-It", 11)
c.setFillColor(INK_SOFT)
foot = "Una lectura simbólica de numerología, astrología y arquetipos"
w = pdfmetrics.stringWidth(foot, "Cormorant-It", 11)
c.drawString(W/2 - w/2, 30 * mm, foot)

c.showPage()

# ================= PAGE 2 — número / signo / elemento =================
draw_bg(c)
TEXT_W = W - 2 * (M + 4 * mm)
TX = M + 4 * mm

y = H - 30 * mm
torus_logo(c, W/2, y, 7 * mm, GOLD, 0.6)
y -= 16 * mm

eyebrow(c, y, "TU NÚMERO")
y -= 9 * mm
heading(c, y, "Nueve — La Culminación")
y -= 7 * mm
y = para(c, NUM_TXT, styles["body"], TX, y, TEXT_W)
y -= 8 * mm
section_divider(c, y)
y -= 12 * mm

eyebrow(c, y, "TU SIGNO SOLAR")
y -= 9 * mm
heading(c, y, "Capricornio")
y -= 7 * mm
y = para(c, SIGN_TXT, styles["body"], TX, y, TEXT_W)
y -= 8 * mm
section_divider(c, y)
y -= 12 * mm

eyebrow(c, y, "TU ELEMENTO")
y -= 9 * mm
heading(c, y, "Tierra")
y -= 7 * mm
y = para(c, ELEM_TXT, styles["body"], TX, y, TEXT_W)

c.setFont("Cormorant-Md", 9.5)
c.setFillColor(GOLD)
pg = "N A A B"
w = pdfmetrics.stringWidth(pg, "Cormorant-Md", 9.5)
c.drawString(W/2 - w/2, 17.5 * mm, pg)

c.showPage()

# ================= PAGE 3 — arquetipo / cuarzo / cierre =================
draw_bg(c)

y = H - 30 * mm
torus_logo(c, W/2, y, 7 * mm, GOLD, 0.6)
y -= 16 * mm

eyebrow(c, y, "TU ARQUETIPO")
y -= 9 * mm
heading(c, y, "La Matriarca")
y -= 7 * mm
y = para(c, ARQ_TXT, styles["body"], TX, y, TEXT_W)
y -= 8 * mm
section_divider(c, y)
y -= 12 * mm

eyebrow(c, y, "TU CUARZO")
y -= 9 * mm
heading(c, y, "Ónix")
y -= 7 * mm
y = para(c, QTZ_TXT, styles["body"], TX, y, TEXT_W)
y -= 12 * mm

# closing quote
y = para(c, "«La fuerza más profunda no es la que se ve,<br/>sino la que sostiene todo lo que se ve.»",
         styles["quote"], TX, y, TEXT_W)
y -= 14 * mm

section_divider(c, y)
y -= 16 * mm

torus_logo(c, W/2, y, 9 * mm, GOLD, 0.6)
wordmark(c, W/2, y - 17 * mm, 16, 7, INK)
c.setFont("Cormorant-It", 9.5)
c.setFillColor(INK_SOFT)
s = "el centro del que todo emana"
w = pdfmetrics.stringWidth(s, "Cormorant-It", 9.5)
c.drawString(W/2 - w/2, y - 22.5 * mm, s)

# disclaimer
c.setFont("Cormorant-It", 8.5)
c.setFillColor(INK_SOFT)
disc = "Esta carta pertenece a las tradiciones simbólicas de la numerología, la astrología y los arquetipos."
w = pdfmetrics.stringWidth(disc, "Cormorant-It", 8.5)
c.drawString(W/2 - w/2, 20 * mm, disc)

c.save()
print("PDF creado")
