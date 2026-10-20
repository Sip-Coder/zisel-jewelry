"""Zisel Jewelry print business cards — concept settings. Edit here, then run:  python3 build.py
All sizes in points (1 in = 72 pt). Card with bleed = 270 x 162 pt; trim = 252 x 144 pt; bleed = 9 pt."""
NAME, BIZ, TAG, PHONE, LOC = "Jonathan Shulkin", "ZISEL JEWELRY", "Wholesale Diamond & Fine Jewelry", "725.254.6937", "Las Vegas, Nevada"
# Concept A back (rev 3) lines, matched to the trailer end card (trailer/src/end.html)
WHOLE, BOOK, VIEW = "WHOLESALE DIAMOND & FINE JEWELRY", "Book a Private Showing", "Viewing by appointment only"
SLOGAN = "BOOK A PRIVATE SHOWING"   # (unused since rev 3 final)

# Brand inks (from invite/zisel.css). GOLD = the metallic gradient used on the poster, site and invite.
NAVY = "#0d1f45"
# Hand-set print navy: profile conversion of #0d1f45 gives a muddy C89 M78 Y48 K73 (288% ink); this keeps it blue at 255% ink.
CMYK_OVERRIDE = {"#0d1f45": (100, 70, 5, 80)}
GOLD = [(0, "#7a5a14"), (.18, "#c99a3a"), (.32, "#fff1b8"), (.46, "#d8b35a"), (.60, "#8f6b1e"), (.76, "#e8c870"), (.88, "#fff5cc"), (1, "#a97d25")]
GEM_EDGE = [(0, "#7a5a14"), (.35, "#fff1b8"), (.6, "#b8892c"), (1, "#f3dc8f")]   # from invite/gem.svg
WHITE, SOFT, MUTED = "#ffffff", "#dfe6f5", "#c9d3ea"
IVORY = "#f8f2e4"
# soft champagne / rose-gold shimmer for "Book a Private Showing" (lighter, warmer cut of the brand gold, like the end card headline)
CHAMPAGNE = [(0, "#b98d5c"), (.22, "#e6c39a"), (.4, "#fbecd2"), (.58, "#dcb48a"), (.78, "#f3dcbc"), (1, "#c49a6c")]

BAND = 0.14 * 72      # metallic band visible inside trim (pt); also runs through the full bleed
HAIR_GAP = 5.0        # navy gap between band and hairline (pt)
HAIR_W = 0.6          # hairline weight (pt)

# style: "gold" = metallic gradient; any hex = flat ink
CONCEPTS = {
 "A": dict(title="A · Gold Frame Classic",
           desc="Gold band + hairline on both sides, plus a second fine inner frame (double-rule classic). Centered back (rev 3): white name, ivory WHOLESALE caps, champagne-shimmer “Book a Private Showing”, gold divider, gold phone, location, ivory italic “Viewing by appointment only”.",
           inner_frame=True, logo_size=40, align="center", center_ink=True,
           # rev 3 (Oct 19, Jonathan): ZISEL JEWELRY removed; type and colours matched to the trailer end card
           size={"name": 12.5}, rule_drop=7.8,
           adv={"whole": 11, "book": 13.5, "phone": 19.5, "loc": 9.5, "view": 10},
           back=[("name", WHITE), ("whole", IVORY), ("book", "champagne"), ("rule", "gold"), ("phone", "gold"), ("loc", MUTED), ("view", IVORY)]),
 "B": dict(title="B · Midnight",
           desc="Gold band + hairline on both sides. Left-aligned back: gold name and phone, white ZISEL JEWELRY, short gold divider, small diamond accent at the right.",
           inner_frame=False, logo_size=44, align="left", gem_accent=True,
           back=[("name", "gold"), ("biz", WHITE), ("tag", SOFT), ("rule", "gold"), ("phone", "gold"), ("loc", MUTED)]),
 "C": dict(title="C · Diamond Divider",
           desc="Gold band + hairline on both sides, no inner frame, larger logo. Centered back: gold name, white ZISEL JEWELRY, gold rule–diamond–rule divider, white phone.",
           inner_frame=False, logo_size=46, align="center", gem_divider=True,
           back=[("name", "gold"), ("biz", WHITE), ("tag", SOFT), ("rule", "gold"), ("phone", WHITE), ("loc", MUTED)]),
}
