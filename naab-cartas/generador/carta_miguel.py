# -*- coding: utf-8 -*-
"""Carta NAAB — Miguel (Tauro / El Constructor / Aventurina + Ágata elegida)"""
import runpy, math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

pdfmetrics.registerFont(TTFont("Cormorant", "Cormorant-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Cormorant-Md", "Cormorant-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Cormorant-SB", "Cormorant-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Cormorant-It", "Cormorant-Italic.ttf"))

SAND      = HexColor("#EFE6D8")
TERRA     = HexColor("#B5674C")
GOLD      = HexColor("#A8894E")
SAGE      = HexColor("#8A9B84")
INK       = HexColor("#3E362E")
INK_SOFT  = HexColor("#6B5F52")

W, H = A4
M = 22 * mm

def torus_logo(c, cx, cy, r, color=GOLD, lw=0.9):
    c.saveState()
    c.setStrokeColor(color); c.setLineWidth(lw)
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.circle(cx, cy, r * 0.38, stroke=1, fill=0)
    n = 8
    for i in range(n):
        ang = 180.0 * i / n
        c.saveState(); c.translate(cx, cy); c.rotate(ang)
        c.ellipse(-r, -r*0.38, r, r*0.38, stroke=1, fill=0)
        c.restoreState()
    c.restoreState()

def wordmark(c, cx, y, size=30, tracking=10, color=INK):
    txt = "NAAB"
    c.setFont("Cormorant-SB", size); c.setFillColor(color)
    widths = [pdfmetrics.stringWidth(ch, "Cormorant-SB", size) for ch in txt]
    total = sum(widths) + tracking * (len(txt) - 1)
    x = cx - total / 2
    for ch, w in zip(txt, widths):
        c.drawString(x, y, ch); x += w + tracking

def hairline(c, x1, x2, y, color=GOLD, lw=0.6):
    c.setStrokeColor(color); c.setLineWidth(lw); c.line(x1, y, x2, y)

def diamond(c, cx, cy, s=2.4, color=GOLD):
    c.saveState(); c.setFillColor(color)
    p = c.beginPath()
    p.moveTo(cx, cy + s); p.lineTo(cx + s, cy); p.lineTo(cx, cy - s); p.lineTo(cx - s, cy)
    p.close(); c.drawPath(p, stroke=0, fill=1); c.restoreState()

def section_divider(c, y):
    x1, x2 = M + 8 * mm, W - M - 8 * mm
    hairline(c, x1, W/2 - 6*mm, y, GOLD, 0.5)
    hairline(c, W/2 + 6*mm, x2, y, GOLD, 0.5)
    diamond(c, W/2, y, 2.2, GOLD)

styles = {
    "body": ParagraphStyle("body", fontName="Cormorant", fontSize=12.3, leading=16.8,
                           textColor=INK, alignment=TA_JUSTIFY),
    "quote": ParagraphStyle("quote", fontName="Cormorant-It", fontSize=13,
                            leading=17.5, textColor=INK_SOFT, alignment=TA_CENTER),
}

def draw_bg(c):
    c.setFillColor(SAND); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.rect(12 * mm, 12 * mm, W - 24 * mm, H - 24 * mm, stroke=1, fill=0)
    c.setLineWidth(0.4)
    c.rect(14 * mm, 14 * mm, W - 28 * mm, H - 28 * mm, stroke=1, fill=0)

def para(c, text, style, x, y_top, width):
    p = Paragraph(text, style)
    w, h = p.wrap(width, H)
    p.drawOn(c, x, y_top - h)
    return y_top - h

def eyebrow(c, y, text):
    c.setFont("Cormorant-Md", 10); c.setFillColor(GOLD)
    t = " ".join(text)
    w = pdfmetrics.stringWidth(t, "Cormorant-Md", 10)
    c.drawString(W/2 - w/2, y, t)

def heading(c, y, text, size=20):
    c.setFont("Cormorant-SB", size); c.setFillColor(TERRA)
    w = pdfmetrics.stringWidth(text, "Cormorant-SB", size)
    c.drawString(W/2 - w/2, y, text)

def footer_mark(c):
    c.setFont("Cormorant-Md", 9.5); c.setFillColor(GOLD)
    pg = "N A A B"
    w = pdfmetrics.stringWidth(pg, "Cormorant-Md", 9.5)
    c.drawString(W/2 - w/2, 17.5 * mm, pg)

# ---------- content ----------
NUM_TXT = ("Naciste bajo el número de la culminación y la totalidad. El 9 no es un final "
           "en el sentido de clausura, sino de plenitud — el momento en que todas las "
           "lecciones de los ciclos anteriores se integran en sabiduría. Quienes llevan "
           "este número no están aquí para empezar caminos, sino para completarlos: "
           "llegan a cerrar círculos que otros dejaron abiertos, a perdonar lo que parecía "
           "imperdonable, a ver el cuadro completo donde otros solo ven fragmentos. "
           "Tu alma es vieja en el mejor sentido: ya sabe cómo terminan las historias, "
           "y aun así elige amarlas.")

SIGN_TXT = ("Naciste cuando la primavera se asienta y el mundo comienza a solidificarse. "
            "Tauro es el signo de la estabilidad, del valor, de quien construye imperios "
            "con paciencia infinita. Los nacidos bajo este signo comprenden el mundo a "
            "través de los sentidos — necesitan tocar, probar, sentir para creer. "
            "Tu relación con el placer y lo tangible es sagrada: entiendes que lo físico "
            "es la expresión más honesta de la existencia. En ti habita un constructor "
            "que sabe que todo lo duradero requiere tiempo. Tu don es la capacidad de "
            "crear abundancia. Tu lección es aprender que soltar también es una forma "
            "de abundancia.")

ELEM_TXT = ("En ti, la Tierra se vive como la esencia masculina la conoce: solidez, "
            "construcción, el arte de edificar lo que perdura. Eres las raíces que "
            "penetran profundo, la roca sobre la que otros construyen sus casas, la "
            "estabilidad que no tiembla. La tierra masculina no se dispersa — se asienta. "
            "Tu fuerza es la de quien comprende que todo lo valioso requiere tiempo, "
            "paciencia, trabajo constante. Llevas en ti la capacidad de materializar, "
            "de convertir sueños en realidad tangible. En ti habita la paciencia de la "
            "montaña. Tu lección es aprender que la rigidez no es fortaleza: a veces "
            "ceder es más sabio que resistir.")

ARQ_TXT = ("Eres el que convierte la visión en piedra. El Constructor no sueña con "
           "imperios — los levanta, ladrillo por ladrillo, con la paciencia de quien "
           "sabe que el tiempo es su aliado y no su enemigo. Su esencia masculina se "
           "expresa en la constancia: su dirección no es veloz, es inevitable. Donde "
           "otros abandonan, él sigue; donde otros improvisan, él cimienta. Sus manos "
           "conocen el valor de lo tangible: el pan, la casa, el abrazo, el trabajo "
           "bien hecho. Combinado con tu número 9, tu figura se completa: eres el "
           "Constructor al final del ciclo — el que ya no edifica para demostrar, "
           "sino para heredar. Y el edificio más importante que construirás "
           "eres tú mismo.")

QTZ_BIRTH = ("Tu piedra de nacimiento es la Aventurina — la piedra de la abundancia "
             "serena. Desde la antigüedad se le asocia con la prosperidad, el "
             "crecimiento y la fortuna que llega a quien cultiva con paciencia: los "
             "antiguos la llamaban la piedra de la oportunidad. Su verde es el verde "
             "de lo que crece sin prisa — el bosque, el campo fértil, lo que da fruto "
             "porque tuvo raíz. No podía ser otra tu piedra: naciste bajo el signo del "
             "constructor, y tu cuarzo es semilla. La abundancia verdadera no es la que "
             "se acumula, sino la que florece — y todo lo que tocas con paciencia, "
             "florece.")

QTZ_CHOSEN = ("Pero tú elegiste el Ágata — y elegir una piedra es declarar qué energía "
              "quieres invocar en este ciclo. Elegiste la piedra de las mil capas: la "
              "que se formó banda sobre banda durante milenios, y por eso conoce el "
              "arte de integrar lo diverso. Quien la elige no está pidiendo simpleza — "
              "está pidiendo equilibrio: reconciliar las propias contradicciones, "
              "encontrar claridad en la palabra, armonizar las voces internas. Tu signo "
              "te dio la semilla, pero tu voluntad pidió integración. Llevarla cerca "
              "del corazón es llevar tu declaración puesta: en este ciclo, eliges "
              "escucharte completo. Eliges tus matices. Eliges la armonía de todo "
              "lo que eres.")

c = canvas.Canvas("/home/claude/naab/Carta_NAAB_Miguel.pdf", pagesize=A4)
c.setTitle("Carta NAAB — Miguel")
c.setAuthor("NAAB")

# ============ PAGE 1 — portada ============
draw_bg(c)
torus_logo(c, W/2, H - 78 * mm, 24 * mm, GOLD, 0.85)
wordmark(c, W/2, H - 118 * mm, 34, 12, INK)

c.setFont("Cormorant-It", 12.5); c.setFillColor(INK_SOFT)
sub = "el centro del que todo emana"
w = pdfmetrics.stringWidth(sub, "Cormorant-It", 12.5)
c.drawString(W/2 - w/2, H - 128 * mm, sub)

section_divider(c, H - 148 * mm)
eyebrow(c, H - 165 * mm, "CARTA DE NACIMIENTO")

c.setFont("Cormorant-SB", 30); c.setFillColor(INK)
name = "Miguel"
w = pdfmetrics.stringWidth(name, "Cormorant-SB", 30)
c.drawString(W/2 - w/2, H - 178 * mm, name)

c.setFont("Cormorant", 12); c.setFillColor(INK_SOFT)
d = "27 de abril de 1976"
w = pdfmetrics.stringWidth(d, "Cormorant", 12)
c.drawString(W/2 - w/2, H - 187 * mm, d)

c.setFont("Cormorant-Md", 12.5); c.setFillColor(SAGE)
line = "Tauro  ·  Tierra  ·  El Constructor  ·  Número 9  ·  Aventurina · Ágata"
w = pdfmetrics.stringWidth(line, "Cormorant-Md", 12.5)
c.drawString(W/2 - w/2, H - 202 * mm, line)

section_divider(c, H - 216 * mm)

c.setFont("Cormorant-It", 11); c.setFillColor(INK_SOFT)
foot = "Una lectura simbólica de numerología, astrología y arquetipos"
w = pdfmetrics.stringWidth(foot, "Cormorant-It", 11)
c.drawString(W/2 - w/2, 30 * mm, foot)
c.showPage()

# ============ PAGE 2 — número / signo / elemento ============
draw_bg(c)
TEXT_W = W - 2 * (M + 4 * mm)
TX = M + 4 * mm

y = H - 30 * mm
torus_logo(c, W/2, y, 7 * mm, GOLD, 0.6)
y -= 16 * mm

eyebrow(c, y, "TU NÚMERO"); y -= 9 * mm
heading(c, y, "Nueve — La Culminación"); y -= 7 * mm
y = para(c, NUM_TXT, styles["body"], TX, y, TEXT_W)
y -= 7 * mm; section_divider(c, y); y -= 11 * mm

eyebrow(c, y, "TU SIGNO SOLAR"); y -= 9 * mm
heading(c, y, "Tauro"); y -= 7 * mm
y = para(c, SIGN_TXT, styles["body"], TX, y, TEXT_W)
y -= 7 * mm; section_divider(c, y); y -= 11 * mm

eyebrow(c, y, "TU ELEMENTO"); y -= 9 * mm
heading(c, y, "Tierra"); y -= 7 * mm
y = para(c, ELEM_TXT, styles["body"], TX, y, TEXT_W)

footer_mark(c)
c.showPage()

# ============ PAGE 3 — arquetipo / cuarzo de nacimiento ============
draw_bg(c)
y = H - 30 * mm
torus_logo(c, W/2, y, 7 * mm, GOLD, 0.6)
y -= 16 * mm

eyebrow(c, y, "TU ARQUETIPO"); y -= 9 * mm
heading(c, y, "El Constructor"); y -= 7 * mm
y = para(c, ARQ_TXT, styles["body"], TX, y, TEXT_W)
y -= 8 * mm; section_divider(c, y); y -= 12 * mm

eyebrow(c, y, "TU CUARZO DE NACIMIENTO"); y -= 9 * mm
heading(c, y, "Aventurina"); y -= 7 * mm
y = para(c, QTZ_BIRTH, styles["body"], TX, y, TEXT_W)
y -= 12 * mm

y = para(c, "«Todo lo que tocas con paciencia, florece.»",
         styles["quote"], TX, y, TEXT_W)

footer_mark(c)
c.showPage()

# ============ PAGE 4 — cuarzo elegido / cierre ============
draw_bg(c)
y = H - 30 * mm
torus_logo(c, W/2, y, 7 * mm, GOLD, 0.6)
y -= 16 * mm

eyebrow(c, y, "TU CUARZO ELEGIDO"); y -= 9 * mm
heading(c, y, "Ágata"); y -= 7 * mm
y = para(c, QTZ_CHOSEN, styles["body"], TX, y, TEXT_W)
y -= 12 * mm

y = para(c, "«Tu signo te dio la semilla.<br/>Tu voluntad pidió integración.»",
         styles["quote"], TX, y, TEXT_W)
y -= 14 * mm

section_divider(c, y)
y -= 20 * mm

torus_logo(c, W/2, y, 9 * mm, GOLD, 0.6)
wordmark(c, W/2, y - 17 * mm, 16, 7, INK)
c.setFont("Cormorant-It", 9.5); c.setFillColor(INK_SOFT)
s = "el centro del que todo emana"
w = pdfmetrics.stringWidth(s, "Cormorant-It", 9.5)
c.drawString(W/2 - w/2, y - 22.5 * mm, s)

c.setFont("Cormorant-It", 8.5); c.setFillColor(INK_SOFT)
disc = "Esta carta pertenece a las tradiciones simbólicas de la numerología, la astrología y los arquetipos."
w = pdfmetrics.stringWidth(disc, "Cormorant-It", 8.5)
c.drawString(W/2 - w/2, 20 * mm, disc)

c.save()
print("PDF creado")
