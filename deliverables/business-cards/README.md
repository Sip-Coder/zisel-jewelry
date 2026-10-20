# Zisel Jewelry · Print business cards (3 concepts)

**Made:** Monday Oct 19, 2026, ~8:00 PM PDT · for Jonathan Shulkin (owner) · status: **concepts for Jonathan Yu to choose from, not sent**

**Front:** Zisel logo only (approved gold-frame logo build: Playfair "Zısel", white/bright diamond, gold "JEWELRY").
**Back:** Jonathan Shulkin / Zisel Jewelry / Wholesale Diamond & Fine Jewelry / 725.254.6937 / Las Vegas, Nevada.
**Not on the card:** website, email, street address, job title.

## Concepts

| | Front | Back |
|---|---|---|
| **A · Gold Frame Classic** | Navy, logo centered, fine gold hairline frame | White stock, centered navy name, deep-gold "ZISEL JEWELRY" and rule, navy phone, matching gold hairline |
| **B · Midnight** | Navy, logo only, no frame | Navy, left-aligned: gold name, white "ZISEL JEWELRY", italic tagline, short gold rule, gold phone |
| **C · Ivory & Midnight** | White stock, navy logo with gold "JEWELRY" | Navy, centered white name, gold accents and phone, gold hairline frame |

Preview: ![concepts](zisel-business-card-concepts.png)

## Files

| File | What |
|---|---|
| `zisel-business-card-{A,B,C}_print-bleed_CMYK.pdf` | **Print-ready**, 2 pages (front, back), 3.75 × 2.25 in incl. 0.125 in bleed, no marks. TrimBox/BleedBox set. |
| `zisel-business-card-{A,B,C}_print-crop-marks_CMYK.pdf` | Same, on a 4.25 × 2.75 in sheet with crop marks outside the bleed. |
| `rgb/…_RGB.pdf` | RGB masters straight from Chrome (before CMYK conversion). |
| `zisel-business-card-{A,B,C}_preview.png` | Front + back side by side at trim size (rendered at 600 dpi). |
| `zisel-business-card-concepts.png` | All 3 concepts (copy at `/workspace/zisel/business-card-concepts.png`). |
| `src/concepts.py` | **Edit here:** text, colors, layout per concept. |
| `src/card.css` | Shared type sizes, inks, logo construction, safe zone. |
| `src/build.py` | Rebuild everything: `cd src && python3 build.py` |
| `src/concept-*.html` | Generated editable HTML (bleed, and `-marks`). |
| `src/fonts/` | Static instances of the brand fonts (Playfair Display 400/500 + Italic 400, Montserrat 500/600; SIL OFL). |
| `src/gem.svg` | Logo diamond (vector, copied from `invite/gem.svg`). |

## Print specs

- Trim 3.5 × 2 in (US), bleed 0.125 in each side, safe zone 0.125 in inside trim; all text/logo checked inside safe zone. Hairline frames sit 0.167 in inside trim.
- Fully vector: no raster images in the PDFs; fonts embedded (TrueType subsets).
- Type: name 14 pt Playfair, tagline 8 pt Playfair Italic, "ZISEL JEWELRY" 6.5 pt Montserrat SemiBold tracked, **phone 10 pt** Montserrat SemiBold, location 7 pt Montserrat Medium, logo "JEWELRY" ≈ 8 pt.
- **Color:** converted to DeviceCMYK with Ghostscript's default CMYK profile (not a press-specific profile like GRACoL/SWOP). Brand navy #0d1f45 and gold #c99a3a (on navy) / #a7802d (on white). Flat inks: the on-screen metallic gold gradient was replaced with solid gold for print. For true metallic, ask the printer for gold foil on the gold elements. Ask the printer for a soft proof; navy coverage is heavy on A front, B and C back.
