"""Zisel packaging mockups. Run from anywhere (e.g. cd /tmp && python3 <this file>).
1) Builds the face artwork as vector PDFs from the business-card A FRONT code (same gold band/hairlines, exact outlined logo).
2) Rasterises it (Ghostscript pngalpha, 700 dpi) and composites it in perspective onto the blank AI-generated base photos
   (no AI lettering: base photos were generated with no text; only the real vector artwork carries the logo)."""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(OUT, "..", "business-cards", "src")); sys.path.insert(0, HERE)
import build as card
from build import shapely_to_path, gradient, logo, EO, GOLD
from reportlab.pdfgen import canvas
from shapely.geometry import Polygon
from PIL import Image
from comp import composite
card.MODE = "rgb"
def ring(c, x0, y0, x1, y1, wgt, W, H):
    g = Polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]); r = g.difference(g.buffer(-wgt, join_style="mitre"))
    c.saveState(); c.clipPath(shapely_to_path(c, r), stroke=0, fill=0, fillMode=EO); gradient(c, 0, H, W, 0, GOLD); c.restoreState()
def face(path, W, H, band, gap, S, cy):
    c = canvas.Canvas(path, pagesize=(W, H), initialFontName="ZOutline")
    ring(c, 0, 0, W, H, band, W, H); e = band + gap; ring(c, e, e, W - e, H - e, .9, W, H)
    e2 = e + 4.5; ring(c, e2, e2, W - e2, H - e2, .6, W, H); logo(c, W / 2, cy, S); c.showPage(); c.save()
P = lambda n: os.path.join(HERE, n)
face(P("art_gift-bag-face.pdf"), 300, 318, 11, 7, 58, 318 * .36)
face(P("art_pouch-face.pdf"), 300, 290, 7, 7, 60, 290 * .5)
for n in ("art_gift-bag-face", "art_pouch-face"):
    subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pngalpha", "-r700", "-dGraphicsAlphaBits=4", f"-sOutputFile=/tmp/{n}.png", P(n + ".pdf")], check=True)
def handle(p):   # keep the gold rope handle in front of the artwork
    m = ((p[..., 0] - p[..., 2]) > .12) & (p.mean(2) > .25); m[:150] = False; m[460:] = False; return m.astype(float)
bag = os.path.join(OUT, "zisel-gift-bag-mockup.png")
composite(P("base_gift-bag_blank.jpg"), "/tmp/art_gift-bag-face.png", [(277, 161), (813, 212), (788, 816), (260, 697)], bag, handle, texture=.3)
Q = [(226, 192), (787, 192), (822, 722), (186, 722)]
L = lambda a, b, t: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
bil = lambda u, v: L(L(Q[0], Q[1], u), L(Q[3], Q[2], u), v)
pouch = os.path.join(OUT, "zisel-jewelry-pouch-mockup.png")
composite(P("base_pouch_blank.jpg"), "/tmp/art_pouch-face.png", [bil(.085, .10), bil(.915, .10), bil(.915, .93), bil(.085, .93)], pouch, None, texture=.7, shade_clip=(.6, 1.4))
for f in (bag, pouch): Image.open(f).convert("RGB").save(f[:-4] + ".pdf", resolution=150)
print("done")
