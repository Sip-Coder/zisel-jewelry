"""Build Zisel print business cards: HTML -> vector PDF (Chrome) -> boxes (pypdf) -> CMYK (Ghostscript) -> PNG previews.
Run from this folder:  python3 build.py   (needs playwright + google-chrome, pypdf, ghostscript, poppler-utils, Pillow)"""
import asyncio, subprocess, http.server, threading, functools, os, shutil
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
from PIL import Image, ImageDraw, ImageFont
from playwright.async_api import async_playwright
from concepts import CONCEPTS
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
SLUG = .25  # in, marks area outside bleed
W, H, B = 3.75, 2.25, .125

def mark_divs():
    t = .25 / 72 * 96  # 0.25pt line in px
    m = []
    for x in (SLUG + B, SLUG + B + 3.5):  # vertical marks top/bottom
        for y0, y1 in ((0, SLUG - .03), (SLUG + H + .03, 2 * SLUG + H)):
            m.append(f'<div class="mark" style="left:calc({x}in - {t/2}px);top:{y0}in;width:{t}px;height:{y1-y0}in"></div>')
    for y in (SLUG + B, SLUG + B + 2):
        for x0, x1 in ((0, SLUG - .03), (SLUG + W + .03, 2 * SLUG + W)):
            m.append(f'<div class="mark" style="top:calc({y}in - {t/2}px);left:{x0}in;height:{t}px;width:{x1-x0}in"></div>')
    return "".join(m)

def page_html(c, marks):
    pw, ph, off = (W + 2 * SLUG, H + 2 * SLUG, SLUG) if marks else (W, H, 0)
    sheets = []
    for side in ("front", "back"):
        card = c[side].replace('<div class="card', f'<div style="position:absolute;left:{off}in;top:{off}in;width:{W}in;height:{H}in"><div class="card', 1) + "</div>"
        sheets.append(f'<div class="sheet" style="width:{pw}in;height:{ph}in;page-break-after:always">{card}{mark_divs() if marks else ""}</div>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>Zisel card {c["title"]}</title><link rel="stylesheet" href="card.css">'
            f'<style>@page{{size:{pw}in {ph}in;margin:0}}</style></head><body>{"".join(sheets)}</body></html>'), pw, ph

def set_boxes(path, marks):
    r = PdfReader(path); w = PdfWriter()
    off = SLUG * 72 if marks else 0
    for p in r.pages:
        p.bleedbox = RectangleObject([off, off, off + W * 72, off + H * 72])
        p.trimbox = RectangleObject([off + B * 72, off + B * 72, off + (W - B) * 72, off + (H - B) * 72])
        p.artbox = p.trimbox
        w.add_page(p)
    w.add_metadata({"/Title": os.path.basename(path)}); w.write(path)

def cmyk(src, dst):
    subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-dSAFER", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.6",
                    "-sColorConversionStrategy=CMYK", "-sProcessColorModel=DeviceCMYK", "-dEmbedAllFonts=true", "-dSubsetFonts=true",
                    "-dPDFSETTINGS=/prepress", "-dPreserveAnnots=false", f"-sOutputFile={dst}", src], check=True)

async def render():
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=HERE))
    threading.Thread(target=srv.serve_forever, daemon=True).start(); port = srv.server_address[1]
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for k, c in CONCEPTS.items():
            for marks in (False, True):
                html, pw, ph = page_html(c, marks)
                name = f"concept-{k}" + ("-marks" if marks else "")
                open(os.path.join(HERE, name + ".html"), "w").write(html)
                pg = await b.new_page(); await pg.goto(f"http://127.0.0.1:{port}/{name}.html", wait_until="networkidle")
                await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
                rgb = os.path.join(OUT, "rgb", f"zisel-business-card-{k}" + ("_print-crop-marks" if marks else "_print-bleed") + "_RGB.pdf")
                await pg.pdf(path=rgb, width=f"{pw}in", height=f"{ph}in", print_background=True, prefer_css_page_size=True); await pg.close()
                set_boxes(rgb, marks)
                final = os.path.join(OUT, os.path.basename(rgb).replace("_RGB", "_CMYK"))
                cmyk(rgb, final); set_boxes(final, marks)
        await b.close()
    srv.shutdown()

def previews():
    dpi = 600; tiles = []
    font = ImageFont.truetype(os.path.join(HERE, "fonts/ZSans-600.ttf"), 56)
    for k, c in CONCEPTS.items():
        pdf = os.path.join(OUT, f"zisel-business-card-{k}_print-bleed_CMYK.pdf"); tmp = f"/tmp/zcard{k}"
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png", pdf, tmp], check=True)
        sides = []
        for i in (1, 2):
            im = Image.open(f"{tmp}-{i}.png").convert("RGB"); bp = round(B * dpi)
            sides.append(im.crop((bp, bp, im.width - bp, im.height - bp)))  # trim size 3.5x2
        gap = 80; sw, sh = sides[0].size
        sheet = Image.new("RGB", (2 * sw + 3 * gap, sh + 2 * gap + 90), "#e9e6df"); d = ImageDraw.Draw(sheet)
        for i, s in enumerate(sides):
            x = gap + i * (sw + gap); y = gap + 90
            sheet.paste(Image.new("RGB", (sw, sh), "#c9c5bb"), (x + 10, y + 14)); sheet.paste(s, (x, y))
            d.text((x, gap), ("FRONT" if i == 0 else "BACK") + "  ·  3.5 × 2 in trim", fill="#0d1f45", font=font)
        sheet.save(os.path.join(OUT, f"zisel-business-card-{k}_preview.png")); tiles.append((c["title"], sheet))
    # comparison sheet
    tw = 1800; scaled = [(t, s.resize((tw, round(s.height * tw / s.width)), Image.LANCZOS)) for t, s in tiles]
    big = ImageFont.truetype(os.path.join(HERE, "fonts/ZPlay-500.ttf"), 56)
    hgt = sum(s.height + 110 for _, s in scaled) + 60
    comp = Image.new("RGB", (tw + 120, hgt), "#f4f1ea"); d = ImageDraw.Draw(comp); y = 40
    for t, s in scaled:
        d.text((60, y), t, fill="#0d1f45", font=big); y += 90; comp.paste(s, (60, y)); y += s.height + 20
    comp.save(os.path.join(OUT, "zisel-business-card-concepts.png"))
    os.makedirs("/workspace/zisel", exist_ok=True); shutil.copy(os.path.join(OUT, "zisel-business-card-concepts.png"), "/workspace/zisel/business-card-concepts.png")

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "rgb"), exist_ok=True)
    asyncio.run(render()); previews(); print("done")
