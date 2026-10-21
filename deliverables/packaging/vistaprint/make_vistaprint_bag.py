"""Vistaprint Luxury Shopping Bag 8x4x10 (Navy, Glossy, Metallic Gold foil, front only): upload artwork + previews.
Template: t_pdf/pdf/NA Luxury Gift Bags, 8" x 4" x 10" Design Template.pdf -> 360 x 360 pt page, 'Trim' line on the page edge,
no separate bleed/safe lines, bag colour PANTONE 655 C. Foil = ONE solid colour: 100% K, DeviceCMYK, no gradients/transparency/overprint.
Logo = the exact card-A-front logo geometry (outlined Playfair 'Zısel' + gem.svg diamond + Montserrat 'JEWELRY'),
adapted for foil: the diamond becomes foil outline + facet lines at >= 2.5 pt (no white facet fills).  Run: cd /tmp && python3 <this file>"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "business-cards", "src"))
import build as card
from build import text_path, shape, font, shapely_to_path, NZ, EO, GEM_LINES
from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor
from shapely.geometry import LineString, LinearRing, Polygon
from shapely.ops import unary_union
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

PAGE = 360.0                 # 5 x 5 in print area (template page)
MARGIN = 18.0                # our own safe margin (0.25 in): template has no safe line
FRAME_INSET, FRAME_W = 22.0, 2.5
S = 128.0                    # wordmark size -> JEWELRY = 0.2*S = 25.6 pt (>= 16 pt); Playfair hairlines ~2.3-2.6 pt
MIN_STROKE = 2.5
FOIL = CMYKColor(0, 0, 0, 1)
OUT_PDF = os.path.join(HERE, "zisel-luxury-bag-8x4x10_gold-foil_upload.pdf")

def gem_foil(c, cx, top, width):
    s = width / 100
    T = lambda pts: [(cx + (float(a) - 50) * s, top - float(b) * s) for a, b in (q.split(",") for q in pts.split())]
    geoms = []
    for pts, sw, closed in GEM_LINES:
        w = max(sw * s, MIN_STROKE + (0.5 if closed else 0))      # outline 3 pt, facet lines 2.5 pt
        P = T(pts); g = LinearRing(P) if closed else LineString(P)
        geoms.append(g.buffer(w / 2, join_style="round" if closed else "mitre", mitre_limit=4, cap_style="flat"))
    edge = unary_union(geoms); c.setFillColor(FOIL); c.drawPath(shapely_to_path(c, edge), stroke=0, fill=1, fillMode=EO)

def logo_foil(c, cx, cy):
    ft, _ = font("play"); glyphs, w = shape("Zısel", "play", S)
    top = cy + 1.31 * S / 2; base = top - 0.9155 * S; x0 = cx - w / 2
    p, _ = text_path(c, "Zısel", "play", S, x0, base); c.setFillColor(FOIL); c.drawPath(p, stroke=0, fill=1, fillMode=NZ)
    gname, gx = glyphs[1]; adv = ft["hmtx"][gname][0]; icx = x0 + (gx + adv / 2) * S / 1000
    gem_foil(c, icx, base + 0.9355 * S, 0.42 * S)
    js = 0.2 * S; jbase = top - S - 0.11 * S - 0.8585 * js; _, jw = shape("JEWELRY", "sans6", js, .55)
    p, _ = text_path(c, "JEWELRY", "sans6", js, cx - jw / 2, jbase, .55); c.drawPath(p, stroke=0, fill=1, fillMode=NZ)
    return w, jw

def build_pdf(path, frame=True):
    c = canvas.Canvas(path, pagesize=(PAGE, PAGE), initialFontName="ZOutline")
    c.setTitle("Zisel Jewelry - Vistaprint luxury bag 8x4x10 - gold foil (100% K)"); c.setAuthor("Sip Studies")
    c.setTrimBox((0, 0, PAGE, PAGE)); c.setBleedBox((0, 0, PAGE, PAGE)); c.setArtBox((0, 0, PAGE, PAGE))
    if frame:
        g = Polygon([(FRAME_INSET, FRAME_INSET), (PAGE - FRAME_INSET, FRAME_INSET), (PAGE - FRAME_INSET, PAGE - FRAME_INSET), (FRAME_INSET, PAGE - FRAME_INSET)])
        c.setFillColor(FOIL); c.drawPath(shapely_to_path(c, g.difference(g.buffer(-FRAME_W, join_style="mitre"))), stroke=0, fill=1, fillMode=EO)
    w, jw = logo_foil(c, PAGE / 2, PAGE / 2)
    c.showPage(); c.save(); return w, jw

# ---------- previews ----------
NAVY655 = (0, 37, 84)    # PANTONE 655 C alternate from the template
def foil_mask(pdf, dpi):
    subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pnggray", f"-r{dpi}", "-dGraphicsAlphaBits=4", "-dTextAlphaBits=4", "-sOutputFile=/tmp/vp_mask.png", pdf], check=True)
    return ImageChops.invert(Image.open("/tmp/vp_mask.png").convert("L"))
def gold_texture(size):
    w, h = size; x = np.linspace(0, 1, w)[None, :]; y = np.linspace(0, 1, h)[:, None]; t = (x + y) / 2
    stops = [(0, (122, 90, 20)), (.18, (201, 154, 58)), (.32, (255, 241, 184)), (.46, (216, 179, 90)), (.60, (143, 107, 30)), (.76, (232, 200, 112)), (.88, (255, 245, 204)), (1, (169, 125, 37))]
    out = np.zeros((h, w, 3))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        m = (t >= a) & (t <= b); f = np.where(m, (t - a) / (b - a), 0)[..., None]
        out = np.where(m[..., None], np.array(ca) * (1 - f) + np.array(cb) * f, out)
    return Image.fromarray(out.astype(np.uint8))
def foil_on_navy(mask, bg):
    gold = gold_texture(mask.size)
    sh = Image.new("RGB", mask.size, (0, 0, 0)); sh = Image.composite(Image.new("RGB", mask.size, (0, 12, 30)), bg, mask.filter(ImageFilter.GaussianBlur(2)).point(lambda v: v * 0.35))
    return Image.composite(gold, sh, mask)

def previews(w_pdf):
    dpi = 300; mask = foil_mask(w_pdf, dpi); N = mask.size[0]
    # 1) the 5x5 print area as foil on navy
    area = foil_on_navy(mask, Image.new("RGB", mask.size, NAVY655))
    lab = Image.new("RGB", (N + 160, N + 230), (236, 233, 226)); lab.paste(area, (80, 80)); d = ImageDraw.Draw(lab)
    f = card.ImageFont.truetype(card.FONTS["sans6"], 40) if hasattr(card, "ImageFont") else None
    from PIL import ImageFont
    f = ImageFont.truetype(card.FONTS["sans6"], 40)
    d.text((80, N + 110), "5 × 5 in print area · gold foil on Navy (PANTONE 655 C)", fill=(13, 31, 69), font=f)
    p1 = os.path.join(HERE, "zisel-luxury-bag_foil-area-preview.png"); lab.save(p1); lab.save(p1[:-4] + ".pdf", resolution=dpi)
    # 2) straight-on bag front 8 x 10 in with the 5x5 area centred
    px = dpi; BW, BH = 8 * px, 10 * px; M = int(1.2 * px); top_extra = int(3.6 * px)
    img = Image.new("RGB", (BW + 2 * M, BH + M + top_extra), (240, 237, 231)); W, H = img.size
    bx, by = M, top_extra
    # shadow
    shm = Image.new("L", img.size, 0); ImageDraw.Draw(shm).rectangle((bx + 40, by + 60, bx + BW + 40, by + BH + 50), fill=110)
    img = Image.composite(Image.new("RGB", img.size, (70, 62, 50)), img, shm.filter(ImageFilter.GaussianBlur(70)))
    # navy glossy face: vertical light falloff + soft diagonal gloss band
    yy = np.linspace(0, 1, BH)[:, None]; xx = np.linspace(0, 1, BW)[None, :]
    base = np.array(NAVY655, float); shade = 1.12 - 0.22 * yy + 0 * xx
    gloss = np.exp(-((xx * 0.9 + yy * 0.5 - 0.42) / 0.07) ** 2) * 0.10
    face = np.clip(base[None, None, :] * shade[..., None] + 255 * gloss[..., None] * np.array([0.55, 0.65, 0.8]), 0, 255).astype(np.uint8)
    face = Image.fromarray(face)
    # top fold line
    fd = ImageDraw.Draw(face); fy = int(1.4 * px); fd.line((0, fy, BW, fy), fill=(0, 22, 55), width=4); fd.line((0, fy + 4, BW, fy + 4), fill=(18, 60, 112), width=2)
    # foil art, 5x5 centred on the 8x10 face
    ax, ay = (BW - N) // 2, (BH - N) // 2
    region = face.crop((ax, ay, ax + N, ay + N)); face.paste(foil_on_navy(mask, region), (ax, ay))
    # cord handles (navy), back handle first
    hd = ImageDraw.Draw(img)
    def cord(dx, lift, col, wid):
        xL, xR = bx + BW / 2 - 1.7 * px, bx + BW / 2 + 1.7 * px; yb = by + 0.75 * px
        pts = []
        for i in range(101):
            t = i / 100; P = [(xL + dx, yb), (xL - 0.3 * px + dx, by - lift), (xR + 0.3 * px - dx, by - lift), (xR - dx, yb)]
            x = sum(c * pt[0] for c, pt in zip(((1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3), P)); y = sum(c * pt[1] for c, pt in zip(((1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3), P))
            pts.append((x, y))
        hd.line(pts, fill=col, width=wid, joint="curve")
        return pts
    cord(30, 3.9 * px, (0, 20, 48), 26)
    img.paste(face, (bx, by)); hd = ImageDraw.Draw(img)
    pts = cord(0, 3.6 * px, (10, 40, 86), 30); hd.line(pts, fill=(40, 80, 140), width=6)   # front cord with a highlight
    for x in (bx + BW / 2 - 1.7 * px, bx + BW / 2 + 1.7 * px):
        y = by + 0.75 * px; hd.ellipse((x - 26, y - 26, x + 26, y + 26), fill=(0, 12, 32))
    f2 = ImageFont.truetype(card.FONTS["sans6"], 60); hd = ImageDraw.Draw(img)
    hd.text((bx, by + BH + 60), "Navy glossy 8 × 4 × 10 in · gold foil 5 × 5 in area, centred", fill=(13, 31, 69), font=f2)
    p2 = os.path.join(HERE, "zisel-luxury-bag_front-preview.png"); img.save(p2); img.save(p2[:-4] + ".pdf", resolution=dpi)
    return p1, p2

if __name__ == "__main__":
    card.MODE = "cmyk"
    w, jw = build_pdf(OUT_PDF)
    print("wordmark width %.1f pt, JEWELRY width %.1f pt, JEWELRY size %.1f pt" % (w, jw, 0.2 * S))
    print(previews(OUT_PDF))
