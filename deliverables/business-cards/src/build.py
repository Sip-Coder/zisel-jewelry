"""Build the Zisel print business cards as native vector PDFs (no browser, no colour conversion step).
- Text is shaped with HarfBuzz (kerning) and OUTLINED from the brand fonts (Playfair Display, Montserrat) -> no font dependency.
- Gold = the brand metallic gradient as real PDF axial shadings (DeviceCMYK in the print files, DeviceRGB in rgb/).
- Logo = same construction as invite/print/logo-*.html: Playfair 500 "Zısel" + invite/gem.svg diamond + Montserrat 600 "JEWELRY".
Run:  cd src && python3 build.py      Needs: reportlab, uharfbuzz, fonttools, shapely, Pillow, ghostscript (previews)."""
import os, subprocess, math
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from shapely.geometry import LineString, LinearRing, Polygon
from shapely.ops import unary_union
from PIL import Image, ImageCms, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import FILL_EVEN_ODD as EO, FILL_NON_ZERO as NZ
from reportlab.lib.colors import CMYKColor, Color
from concepts import *

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
W, H, B, SLUG = 270.0, 162.0, 9.0, 18.0
FONTS = {k: os.path.join(HERE, "fonts", v) for k, v in dict(play="ZPlay-500.ttf", play4="ZPlay-400.ttf", ital="ZPlay-400-italic.ttf", sans5="ZSans-500.ttf", sans6="ZSans-600.ttf").items()}
_ft, _hb = {}, {}
CMYK_ICC = "/usr/share/color/icc/ghostscript/default_cmyk.icc"
_xf = ImageCms.buildTransform(ImageCms.createProfile("sRGB"), ImageCms.getOpenProfile(CMYK_ICC), "RGB", "CMYK", renderingIntent=0)
MODE = "cmyk"
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLTTF
pdfmetrics.registerFont(RLTTF("ZOutline", FONTS["sans5"]))   # dynamic font -> no unembedded Helvetica in the preamble; never used (text is outlined)

def ink(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    if MODE == "rgb": return Color(r / 255, g / 255, b / 255)
    if hexc.lower() in CMYK_OVERRIDE: return CMYKColor(*(v / 100 for v in CMYK_OVERRIDE[hexc.lower()]))
    c = ImageCms.applyTransform(Image.new("RGB", (1, 1), (r, g, b)), _xf).getpixel((0, 0))
    return CMYKColor(*(v / 255 for v in c))

# ---------- outlined text ----------
class RLPen(BasePen):
    def __init__(self, gs, path, x, y, s): super().__init__(gs); self.p, self.x, self.y, self.s = path, x, y, s
    def T(self, pt): return self.x + pt[0] * self.s, self.y + pt[1] * self.s
    def _moveTo(self, p): self.p.moveTo(*self.T(p))
    def _lineTo(self, p): self.p.lineTo(*self.T(p))
    def _curveToOne(self, a, b, c): self.p.curveTo(*self.T(a), *self.T(b), *self.T(c))
    def _closePath(self): self.p.close()

def font(k):
    if k not in _ft:
        _ft[k] = TTFont(FONTS[k]); blob = hb.Blob.from_file_path(FONTS[k]); _hb[k] = hb.Font(hb.Face(blob))
    return _ft[k], _hb[k]

def shape(text, k, size, track=0.0):
    """returns glyph list [(name, x_offset_units)], width in pt (tracking applied between glyphs only)."""
    ft, hf = font(k); upm = ft["head"].unitsPerEm
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(hf, buf, {"kern": True, "liga": True})
    order = ft.getGlyphOrder(); x = 0; out = []
    for i, (inf, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        out.append((order[inf.codepoint], x + pos.x_offset)); x += pos.x_advance
        if i < len(buf.glyph_infos) - 1: x += track * upm
    return out, x * size / upm

def text_path(c, text, k, size, x, y, track=0.0, anchor="left"):
    glyphs, w = shape(text, k, size, track)
    if anchor == "center": x -= w / 2
    ft, _ = font(k); gs = ft.getGlyphSet(); s = size / ft["head"].unitsPerEm; p = c.beginPath()
    for name, gx in glyphs: gs[name].draw(RLPen(gs, p, x + gx * s, y, s))
    return p, (x, y - .25 * size, x + w, y + .75 * size)

def paint(c, path, style, bbox, even_odd=False):
    """fill `path` with a flat ink or the metallic gold gradient mapped like CSS .goldtext (200% box, 135deg)."""
    if style != "gold":
        c.setFillColor(ink(style)); c.drawPath(path, stroke=0, fill=1, fillMode=EO if even_odd else NZ); return
    x0, y0, x1, y1 = bbox; w, h = x1 - x0, y1 - y0
    c.saveState(); c.clipPath(path, stroke=0, fill=0, fillMode=EO if even_odd else NZ)
    gradient(c, x0, y1, x0 + 2 * w, y1 - 2 * max(h, w * .12), GOLD); c.restoreState()

def gradient(c, xa, ya, xb, yb, stops):
    c.linearGradient(xa, ya, xb, yb, [ink(h) for _, h in stops], [p for p, _ in stops], extend=True)

def shapely_to_path(c, geom):
    p = c.beginPath(); polys = geom.geoms if hasattr(geom, "geoms") else [geom]
    for g in polys:
        for ring in [g.exterior, *g.interiors]:
            pts = list(ring.coords); p.moveTo(*pts[0]); [p.lineTo(*q) for q in pts[1:]]; p.close()
    return p

# ---------- gem (invite/gem.svg, viewBox 100x80, y down) ----------
GEM_FACETS = [("20,4 80,4 98,26 50,78 2,26", "#ffffff"), ("20,4 35,26 2,26", "#eef4ff"), ("80,4 65,26 98,26", "#dfe9fb"), ("35,26 65,26 50,78", "#ffffff"),
              ("2,26 35,26 50,78", "#e6eefc"), ("98,26 65,26 50,78", "#d4e1f7"), ("20,4 50,4 35,26", "#ffffff"), ("50,4 80,4 65,26", "#f4f8ff")]
GEM_LINES = [("20,4 35,26 50,4 65,26 80,4", 2.4, False), ("2,26 98,26", 2.4, False), ("35,26 50,78 65,26", 2.0, False), ("20,4 80,4 98,26 50,78 2,26", 3.2, True)]

def gem(c, cx, top, width):
    s = width / 100; T = lambda pts: [(cx + (float(a) - 50) * s, top - float(b) * s) for a, b in (q.split(",") for q in pts.split())]
    for pts, col in GEM_FACETS:
        P = T(pts); p = c.beginPath(); p.moveTo(*P[0]); [p.lineTo(*q) for q in P[1:]]; p.close()
        c.setFillColor(ink(col)); c.drawPath(p, stroke=0, fill=1, fillMode=NZ)
    geoms = []
    for pts, sw, closed in GEM_LINES:
        P = T(pts); g = LinearRing(P) if closed else LineString(P)
        geoms.append(g.buffer(sw * s / 2, join_style="round" if closed else "mitre", mitre_limit=4, cap_style="flat"))
    edge = unary_union(geoms); c.saveState(); c.clipPath(shapely_to_path(c, edge), stroke=0, fill=0, fillMode=EO)
    gradient(c, cx - 50 * s, top, cx + 50 * s, top - 80 * s, GEM_EDGE); c.restoreState()

# ---------- logo: replicates .logo css (line-height 1, gem top -.02em on dotless i, JEWELRY .2em, tracking .55em, gap .55em) ----------
def logo(c, cx, cy, S):
    ft, _ = font("play"); upm = 1000
    glyphs, w = shape("Zısel", "play", S); total_h = 1.31 * S
    top = cy + total_h / 2; base = top - 0.9155 * S              # baseline inside the 1em line box
    x0 = cx - w / 2; p, bb = text_path(c, "Zısel", "play", S, x0, base)
    paint(c, p, WHITE, bb)
    gname, gx = glyphs[1]; adv = ft["hmtx"][gname][0]; icx = x0 + (gx + adv / 2) * S / upm
    gem(c, icx, base + 0.9355 * S, 0.42 * S)
    js = 0.2 * S; jbase = top - S - 0.11 * S - (0.8585 * js)
    _, jw = shape("JEWELRY", "sans6", js, .55)
    p, bb = text_path(c, "JEWELRY", "sans6", js, cx - jw / 2, jbase, .55); paint(c, p, "gold", bb)

# ---------- frame ----------
def frame(c, ox, oy, inner_frame):
    full = c.beginPath(); full.rect(ox, oy, W, H)
    c.saveState(); c.clipPath(full, stroke=0, fill=0); gradient(c, ox, oy + H, ox + W, oy, GOLD); c.restoreState()   # band, runs through bleed
    e = B + BAND; c.setFillColor(ink(NAVY)); c.rect(ox + e, oy + e, W - 2 * e, H - 2 * e, stroke=0, fill=1)
    def hairline(inset, wgt):
        g = Polygon([(ox + inset, oy + inset), (ox + W - inset, oy + inset), (ox + W - inset, oy + H - inset), (ox + inset, oy + H - inset)])
        ring = g.difference(g.buffer(-wgt, join_style="mitre"))
        c.saveState(); c.clipPath(shapely_to_path(c, ring), stroke=0, fill=0, fillMode=EO); gradient(c, ox, oy + H, ox + W, oy, GOLD); c.restoreState()
    hairline(e + HAIR_GAP, HAIR_W)
    if inner_frame: hairline(e + HAIR_GAP + 3.2, 0.4)
    return e + HAIR_GAP + HAIR_W + (3.6 if inner_frame else 0)   # inner edge of last frame line

# ---------- back ----------
SPEC = {"name": ("play", 13.5, 0, 0), "biz": ("sans6", 6.5, .42, 12), "tag": ("ital", 8, 0, 11), "phone": ("sans6", 10, .12, 23.5), "loc": ("sans5", 7, .1, 11), "slogan": ("sans6", 6.3, .3, 11)}
TEXT = lambda k: {"name": NAME, "biz": BIZ, "tag": TAG, "phone": PHONE, "loc": LOC, "slogan": SLOGAN}[k]

def ink_v(k):
    """vertical ink extent (ymin, ymax) of a back line relative to its baseline, in pt."""
    from fontTools.pens.boundsPen import BoundsPen
    f, size, tr, _ = SPEC[k]; ft, _ = font(f); gs = ft.getGlyphSet(); lo, hi = 0, 0
    for name, _ in shape(TEXT(k), f, size, tr)[0]:
        bp = BoundsPen(gs); gs[name].draw(bp)
        if bp.bounds: lo, hi = min(lo, bp.bounds[1]), max(hi, bp.bounds[3])
    s = size / ft["head"].unitsPerEm; return lo * s, hi * s

def back(c, ox, oy, cfg):
    left = cfg["align"] == "left"; safe_l = ox + 44 if left else None
    lines = [l for l in cfg["back"] if l[0] != "rule"]
    first = SPEC["name"][1] * .72; last = SPEC["loc"][1] * .22
    total = first + sum(SPEC[k][3] for k, _ in lines) + last
    y = oy + H / 2 + total / 2 - first; cx = ox + W / 2
    advs = {k: cfg.get("adv", {}).get(k, SPEC[k][3]) for k, _ in lines}
    if cfg.get("center_ink"):   # exact optical centering of the ink block on the card (= inside the symmetric frame)
        drop = sum(advs[k] for k, _ in lines[1:])
        top = ink_v(lines[0][0])[1]; bot = -drop + ink_v(lines[-1][0])[0]
        y = oy + H / 2 - (top + bot) / 2 + advs[lines[0][0]]
    rule_style = dict(cfg["back"])["rule"]
    for k, style in lines:
        f, size, tr, _ = SPEC[k]; adv = advs[k]; y -= adv
        if k == "phone":   # divider sits between tagline and phone
            ry = y + adv - 11.2
            if cfg.get("gem_divider"):
                gw = 9; gem(c, cx, ry + gw * .4, gw)
                for sx in (-1, 1):
                    p = c.beginPath(); a, b = cx + sx * (gw / 2 + 4), cx + sx * (gw / 2 + 4 + 30); p.rect(min(a, b), ry - .3, 30, .6); paint(c, p, rule_style, (min(a, b), ry - 1, min(a, b) + 30, ry + 1))
            else:
                rw = 36 if left else 48; rx = safe_l if left else cx - rw / 2
                p = c.beginPath(); p.rect(rx, ry - .35, rw, .7); paint(c, p, rule_style, (rx, ry - 1, rx + rw, ry + 1))
        if left: p, bb = text_path(c, TEXT(k), f, size, safe_l, y, tr)
        else: p, bb = text_path(c, TEXT(k), f, size, cx, y, tr, anchor="center")
        paint(c, p, style, bb)
    if cfg.get("gem_accent"): gem(c, ox + W - 58, oy + H / 2 + 7, 16)

def front(c, ox, oy, cfg): logo(c, ox + W / 2, oy + H / 2, cfg["logo_size"])

def marks(c, ox, oy):
    c.setStrokeColor(CMYKColor(1, 1, 1, 1) if MODE == "cmyk" else Color(0, 0, 0)); c.setLineWidth(.25)
    for x in (ox + B, ox + W - B):
        c.line(x, oy + H + 2, x, oy + H + SLUG); c.line(x, oy - 2, x, oy - SLUG)
    for y in (oy + B, oy + H - B):
        c.line(ox - SLUG, y, ox - 2, y); c.line(ox + W + 2, y, ox + W + SLUG, y)

def build_pdf(k, cfg, with_marks, path):
    off = SLUG if with_marks else 0; pw, ph = W + 2 * off, H + 2 * off
    c = canvas.Canvas(path, pagesize=(pw, ph), initialFontName="ZOutline"); c.setTitle(f"Zisel Jewelry business card {cfg['title']}"); c.setAuthor("Sip Studies"); c.setSubject("3.5x2 in, 0.125 in bleed")
    for side in (front, back):
        c.setBleedBox((off, off, off + W, off + H)); c.setTrimBox((off + B, off + B, off + W - B, off + H - B)); c.setArtBox((off + B, off + B, off + W - B, off + H - B))
        frame(c, off, off, cfg["inner_frame"]); side(c, off, off, cfg)
        if with_marks: marks(c, off, off)
        c.showPage()
    c.save()

def previews():
    tiles = []; lab = ImageFont.truetype(FONTS["sans6"], 56); big = ImageFont.truetype(FONTS["play"], 64); dpi = 600
    for k, cfg in CONCEPTS.items():
        pdf = os.path.join(OUT, f"zisel-business-card-{k}_print-bleed_CMYK.pdf")
        subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-dSAFER", "-sDEVICE=png16m", f"-r{dpi}", "-dGraphicsAlphaBits=4", "-dTextAlphaBits=4", f"-sOutputFile=/tmp/zc{k}-%d.png", pdf], check=True)
        bp = round(B / 72 * dpi); sides = []
        for i in (1, 2):
            im = Image.open(f"/tmp/zc{k}-{i}.png").convert("RGB"); sides.append(im.crop((bp, bp, im.width - bp, im.height - bp)))
        gap = 80; sw, sh = sides[0].size
        sheet = Image.new("RGB", (2 * sw + 3 * gap, sh + 2 * gap + 100), "#e9e6df"); d = ImageDraw.Draw(sheet)
        for i, s in enumerate(sides):
            x = gap + i * (sw + gap); y = gap + 100
            sheet.paste(Image.new("RGB", (sw, sh), "#c9c5bb"), (x + 10, y + 14)); sheet.paste(s, (x, y))
            d.text((x, gap), ("FRONT" if i == 0 else "BACK") + "  ·  3.5 × 2 in trim", fill="#0d1f45", font=lab)
        sheet.save(os.path.join(OUT, f"zisel-business-card-{k}_preview.png")); tiles.append((cfg["title"], sheet))
    tw = 1800; sc = [(t, s.resize((tw, round(s.height * tw / s.width)), Image.LANCZOS)) for t, s in tiles]
    comp = Image.new("RGB", (tw + 120, sum(s.height + 120 for _, s in sc) + 60), "#f4f1ea"); d = ImageDraw.Draw(comp); y = 40
    for t, s in sc: d.text((60, y), t, fill="#0d1f45", font=big); y += 100; comp.paste(s, (60, y)); y += s.height + 20
    comp.save(os.path.join(OUT, "zisel-business-card-concepts.png")); os.makedirs("/workspace/zisel", exist_ok=True)
    comp.save("/workspace/zisel/business-card-concepts.png")

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "rgb"), exist_ok=True)
    for MODE in ("cmyk", "rgb"):
        globals()["MODE"] = MODE
        for k, cfg in CONCEPTS.items():
            for m in (False, True):
                name = f"zisel-business-card-{k}_print-{'crop-marks' if m else 'bleed'}_{MODE.upper()}.pdf"
                build_pdf(k, cfg, m, os.path.join(OUT, name) if MODE == "cmyk" else os.path.join(OUT, "rgb", name))
    previews(); print("done")
