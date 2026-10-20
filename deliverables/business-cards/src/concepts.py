"""Zisel Jewelry print business cards — concept settings. Edit here, then run:  python3 build.py
All sizes in points (1 in = 72 pt). Card with bleed = 270 x 162 pt; trim = 252 x 144 pt; bleed = 9 pt."""
NAME, BIZ, TAG, PHONE, LOC = "Jonathan Shulkin", "ZISEL JEWELRY", "Wholesale Diamond & Fine Jewelry", "725.254.6937", "Las Vegas, Nevada"
SLOGAN = "BOOK A PRIVATE SHOWING"   # headline of the client's favourite invite poster, set as tracked caps

# Brand inks (from invite/zisel.css). GOLD = the metallic gradient used on the poster, site and invite.
NAVY = "#0d1f45"
# Hand-set print navy: profile conversion of #0d1f45 gives a muddy C89 M78 Y48 K73 (288% ink); this keeps it blue at 255% ink.
CMYK_OVERRIDE = {"#0d1f45": (100, 70, 5, 80)}
GOLD = [(0, "#7a5a14"), (.18, "#c99a3a"), (.32, "#fff1b8"), (.46, "#d8b35a"), (.60, "#8f6b1e"), (.76, "#e8c870"), (.88, "#fff5cc"), (1, "#a97d25")]
GEM_EDGE = [(0, "#7a5a14"), (.35, "#fff1b8"), (.6, "#b8892c"), (1, "#f3dc8f")]   # from invite/gem.svg
WHITE, SOFT, MUTED = "#ffffff", "#dfe6f5", "#c9d3ea"

BAND = 0.14 * 72      # metallic band visible inside trim (pt); also runs through the full bleed
HAIR_GAP = 5.0        # navy gap between band and hairline (pt)
HAIR_W = 0.6          # hairline weight (pt)

# style: "gold" = metallic gradient; any hex = flat ink
CONCEPTS = {
 "A": dict(title="A · Gold Frame Classic",
           desc="Gold band + hairline on both sides, plus a second fine inner frame (double-rule classic). Centered back: white name, italic tagline, gold BOOK A PRIVATE SHOWING slogan, plain gold divider, gold phone.",
           inner_frame=True, logo_size=40, align="center", center_ink=True,
           # rev 3 (Oct 19): ZISEL JEWELRY removed (repeats the front logo); slogan added under the tagline
           adv={"tag": 13, "slogan": 12},
           back=[("name", WHITE), ("tag", SOFT), ("slogan", "gold"), ("rule", "gold"), ("phone", "gold"), ("loc", MUTED)]),
 "B": dict(title="B · Midnight",
           desc="Gold band + hairline on both sides. Left-aligned back: gold name and phone, white ZISEL JEWELRY, short gold divider, small diamond accent at the right.",
           inner_frame=False, logo_size=44, align="left", gem_accent=True,
           back=[("name", "gold"), ("biz", WHITE), ("tag", SOFT), ("rule", "gold"), ("phone", "gold"), ("loc", MUTED)]),
 "C": dict(title="C · Diamond Divider",
           desc="Gold band + hairline on both sides, no inner frame, larger logo. Centered back: gold name, white ZISEL JEWELRY, gold rule–diamond–rule divider, white phone.",
           inner_frame=False, logo_size=46, align="center", gem_divider=True,
           back=[("name", "gold"), ("biz", WHITE), ("tag", SOFT), ("rule", "gold"), ("phone", WHITE), ("loc", MUTED)]),
}
