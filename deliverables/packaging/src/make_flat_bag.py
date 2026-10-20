"""Zisel gift bag: flat, straight-on design reference image (fully programmatic, vector -> PNG/PDF).
Same face design as the gift-bag mockup (art_gift-bag-face.pdf): navy, metallic gold edge band, hairline + inner frame,
exact outlined Zisel logo from business-cards/src. Gold rope handles drawn as vector ropes. Run: cd /tmp && python3 <this file>"""
import os, sys, subprocess, math
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(OUT, "..", "business-cards", "src"))
import build as card
from build import shapely_to_path, gradient, logo, ink, EO, NZ, GOLD
from reportlab.pdfgen import canvas
from shapely.geometry import Polygon, LineString, Point
from PIL import Image, ImageFilter
card.MODE = "rgb"
PW, PH = 440, 560                      # page (pt)
FW, FH = 300, 318                      # bag face, same proportions as the mockup artwork
X0 = (PW - FW) / 2; Y0 = 52; TOP = Y0 + FH; CX = PW / 2
ROPE = [(.0, "#6f5418"), (.25, "#b8903e"), (.45, "#ecd391"), (.6, "#c9a24f"), (.8, "#8f6d24"), (1, "#a9843a")]
ROPE_BACK = [(0, "#4d3a10"), (.5, "#8a6a2a"), (1, "#5c4614")]

def bez(p0, p1, p2, p3, n=120):
    return [tuple((1-t)**3*a + 3*(1-t)**2*t*b + 3*(1-t)*t**2*c + t**3*d for a, b, c, d in zip(p0, p1, p2, p3)) for t in (i / n for i in range(n + 1))]

def clipfill(c, geom, stops, box):
    c.saveState(); c.clipPath(shapely_to_path(c, geom), stroke=0, fill=0, fillMode=EO)
    gradient(c, *box, stops); c.restoreState()

def rope(c, pts, w, stops, twist=True):
    line = LineString(pts); body = line.buffer(w / 2, cap_style="flat", join_style="round")
    clipfill(c, body, stops, (CX - 90, TOP + 110, CX + 90, TOP - 40))
    if not twist: return
    c.saveState(); c.clipPath(shapely_to_path(c, body), stroke=0, fill=0, fillMode=EO)
    L = line.length; s = 0; c.setLineWidth(.75); c.setStrokeColor(ink("#5b4412")); c.setStrokeAlpha(.55)
    while s < L:                                   # twisted-rope strands
        p = line.interpolate(s); q = line.interpolate(min(s + .5, L)); dx, dy = q.x - p.x, q.y - p.y; n = math.hypot(dx, dy) or 1
        tx, ty = dx / n, dy / n; nx, ny = -ty, tx; a = math.radians(38)
        ux, uy = tx * math.sin(a) + nx * math.cos(a), ty * math.sin(a) + ny * math.cos(a)
        c.line(p.x - ux * w, p.y - uy * w, p.x + ux * w, p.y + uy * w); s += 2.6
    c.setStrokeAlpha(.35); c.setStrokeColor(ink("#fff1c4")); c.setLineWidth(.45); s = 1.1
    while s < L:
        p = line.interpolate(s); q = line.interpolate(min(s + .5, L)); dx, dy = q.x - p.x, q.y - p.y; n = math.hypot(dx, dy) or 1
        tx, ty = dx / n, dy / n; nx, ny = -ty, tx; a = math.radians(38)
        ux, uy = tx * math.sin(a) + nx * math.cos(a), ty * math.sin(a) + ny * math.cos(a)
        c.line(p.x - ux * w * .4, p.y - uy * w * .4, p.x + ux * w * .15, p.y + uy * w * .15); s += 2.6
    c.restoreState()

def ring(c, x0, y0, x1, y1, wgt):
    g = Polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]); r = g.difference(g.buffer(-wgt, join_style="mitre"))
    clipfill(c, r, GOLD, (X0, TOP, X0 + FW, Y0))

def main():
    pdf = os.path.join(HERE, "art_gift-bag-flat.pdf")
    c = canvas.Canvas(pdf, pagesize=(PW, PH), initialFontName="ZOutline"); c.setTitle("Zisel gift bag - flat design reference")
    hx, hy = 52, TOP - 30                                   # handle holes: +-52 pt from centre, 30 pt below the top edge
    back = bez((CX - hx + 6, TOP - 4), (CX - hx - 2, TOP + 126), (CX + hx + 2, TOP + 126), (CX + hx - 6, TOP - 4))
    rope(c, back, 6.2, ROPE_BACK, twist=False)              # back handle, seen behind the bag
    g = c.beginPath(); g.rect(X0, Y0, FW, FH)                                    # navy face with a soft top-light falloff
    c.saveState(); c.clipPath(g, stroke=0, fill=0); gradient(c, CX, TOP, CX, Y0, [(0, "#16295a"), (.55, "#0f2149"), (1, "#0b1a3d")]); c.restoreState()
    ring(c, X0, Y0, X0 + FW, TOP, 11); e = 11 + 7
    ring(c, X0 + e, Y0 + e, X0 + FW - e, TOP - e, .9); e2 = e + 4.5
    ring(c, X0 + e2, Y0 + e2, X0 + FW - e2, TOP - e2, .6)
    c.setStrokeColor(ink("#000000")); c.setStrokeAlpha(.18); c.setLineWidth(.6)            # top fold crease
    c.line(X0 + 11, TOP - 38, X0 + FW - 11, TOP - 38); c.setStrokeAlpha(1)
    logo(c, CX, Y0 + FH * .36, 58)                          # exact card-front logo, same placement as the mockup
    for sx in (-1, 1):                                      # grommets
        x = CX + sx * hx
        c.setFillColor(ink("#06102a")); c.circle(x, hy, 3.6, stroke=0, fill=1)
        clipfill(c, Point(x, hy).buffer(5.2).difference(Point(x, hy).buffer(3.4)), GOLD, (x - 6, hy + 6, x + 6, hy - 6))
    front = bez((CX - hx, hy), (CX - hx - 10, TOP + 120), (CX + hx + 10, TOP + 120), (CX + hx, hy))
    rope(c, front, 7, ROPE)
    for sx in (-1, 1):                                      # rope ends entering the grommets
        x = CX + sx * hx; c.setFillColor(ink("#3a2c0c")); c.setFillAlpha(.6); c.ellipse(x - 3.6, hy - 1.6, x + 3.6, hy + 1.6, stroke=0, fill=1); c.setFillAlpha(1)
    c.showPage(); c.save(); return pdf

pdf = main()
dpi = 300; tmp = "/tmp/zisel_flat_bag_alpha.png"
subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pngalpha", f"-r{dpi}", "-dGraphicsAlphaBits=4", f"-sOutputFile={tmp}", pdf], check=True)
art = Image.open(tmp).convert("RGBA"); W, H = art.size
bg = Image.new("RGBA", (W, H), (242, 239, 233, 255))
# soft floor-contact + drop shadow from the bag silhouette
a = art.split()[3]; s = 300 / 72
sh = Image.new("L", (W, H), 0); sh.paste(a.point(lambda v: int(v * .30)), (int(6 * s), int(9 * s)))
sh = sh.filter(ImageFilter.GaussianBlur(12 * s))
bg = Image.composite(Image.new("RGBA", (W, H), (60, 52, 40, 255)), bg, sh)
c2 = Image.new("L", (W, H), 0)                              # tight contact shadow under the base
from PIL import ImageDraw
ImageDraw.Draw(c2).ellipse((int((X0 - 6) * s), int((PH - Y0 - 6) * s), int((X0 + FW + 6) * s), int((PH - Y0 + 10) * s)), fill=120)
c2 = c2.filter(ImageFilter.GaussianBlur(5 * s)); bg = Image.composite(Image.new("RGBA", (W, H), (40, 34, 26, 255)), bg, c2)
out = Image.alpha_composite(bg, art).convert("RGB")
png = os.path.join(OUT, "zisel-gift-bag-flat.png"); out.save(png)
out.save(png[:-4] + ".pdf", resolution=dpi)
print(png, out.size)
