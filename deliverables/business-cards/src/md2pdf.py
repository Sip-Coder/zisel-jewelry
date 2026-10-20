"""Render a Markdown file to a PDF beside it (Letter, Chrome). Usage: python3 md2pdf.py FILE.md [FILE2.md ...]"""
import sys, os, asyncio, markdown
from playwright.async_api import async_playwright
CSS = ("body{font-family:Montserrat,Helvetica,sans-serif;font-size:10.5px;color:#0d1f45;line-height:1.45}h1,h2,h3{font-family:'Playfair Display',Georgia,serif;color:#0d1f45}"
       "h2{border-bottom:1px solid #c99a3a;padding-bottom:3px}table{border-collapse:collapse;width:100%;margin:6px 0}td,th{border:1px solid #d9d4c7;padding:3px 5px;vertical-align:top;text-align:left}"
       "th{background:#f4efe2}code{background:#f3f1ec;padding:0 3px;font-size:9.5px;word-break:break-all}img{max-width:100%}")
async def main(files):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for f in files:
            f = os.path.abspath(f); html = markdown.markdown(open(f).read(), extensions=["tables", "fenced_code"])
            pg = await b.new_page(); await pg.goto("file://" + os.path.dirname(f) + "/")
            await pg.set_content(f"<html><head><meta charset='utf-8'><title>{os.path.basename(f)}</title><style>{CSS}</style></head><body>{html}</body></html>", wait_until="networkidle")
            await pg.pdf(path=f[:-3] + ".pdf", format="Letter", margin={"top": "0.6in", "bottom": "0.6in", "left": "0.6in", "right": "0.6in"}, print_background=True); await pg.close()
        await b.close()
asyncio.run(main(sys.argv[1:]))
