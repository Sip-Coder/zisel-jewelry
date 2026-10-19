# Zisel Jewelry · WhatsApp Trailer (creative brief)

**Concept: "Brilliance, by appointment."** A quiet, luxe reveal in the poster's navy, white and gold. A large gold-framed 4:5 window (940 px wide) works like a private viewing window: each piece slides into it with a slow Ken Burns move, a soft light sweep and a few diamond glints, grouped by category so it plays like a curated showing. It ends on a clear booking card.

**Spec:** 1080×1920, 30 fps, H.264 High/yuv420p, AAC 128k, faststart, 28.5 s, ~8.5 MB.
**Type:** Playfair (ZPlay) serif and tracked Montserrat (ZSans) caps, the same fonts and logo (diamond over the "i") as the posters and site.
**Music:** self-synthesized lounge/swing jazz (`src/music.py`), 160 BPM half-time feel, so each 1.5 s cut lands on a bar downbeat. Walking upright bass (additive with pluck envelope), swung ride ("ding, ding-da-ding"), brushed snare on 2 and 4 with a brush swish, feathered kick, FM Rhodes comping on a Charleston rhythm through Fmaj9 | D9 | Gm9 | C13, and vibraphone fills on the logo reveal, the diamond glint, each category change and into the end card. It ends with a button: a full Fmaj9 hit at 27.0 s on the end card that rings out. Light room reverb, 1.2 s fade-in, loudness-normalized to about -16 LUFS with true peak -1.5 dBFS and no clipping. Original, so no license issues.
**Rules followed:** real gallery photos only (full-res originals), no Star of David or cross photos, no Las Vegas.

## Shot list and timing (160 BPM half-time; each photo = 1 bar = 1.5 s)
| Time | Shot |
|---|---|
| 0.0–3.0 | Navy and gold frame; the Zisel logo fades and scales in, then a gold shimmer sweeps across it and the diamond glints (2.5 s) |
| 3.0–5.6 | Hook rises under the logo: "Brilliance, by appointment." / WHOLESALE DIAMOND & FINE JEWELRY |
| 5.6–6.2 | Crossfade to the gallery layout (small logo at top, gold-framed window) |
| 6.0–10.5 | **RINGS**: z024 diamond ring tray · z037 yellow-diamond rings · z044 colored-gem ring tray (cropped above the price tag) |
| 10.5–15.0 | **BRACELETS**: z051 tennis bracelets · z068 white/yellow-gold bracelets · z052 yellow-diamond station bracelets |
| 15.0–18.0 | **HOOPS**: z019sq pavé inside-out hoops · z013sq yellow-diamond hoops (tag-free crops) |
| 18.0–24.4 | **PENDANTS & NECKLACES**: z083 pavé pendant group · z010 baguette cushion halo · z001 ruby pendants · z009 opal, yellow-diamond drop and gold pavé heart pendants |
| 24.0–24.7 | Crossfade to the end card |
| 24.7–28.5 | End card (~3.8 s hold): logo · "Book a Private Showing" · WHOLESALE DIAMOND & FINE JEWELRY · "Viewing by appointment only" · "Jonathan Shulkin · Call/Text 725.254.6937" |

Every photo gets a 1.9 s Ken Burns move (alternating zoom in/out and pan direction), 0.5 s crossfades, one diagonal light sweep and three soft round glows on the brightest highlights (round, not star-shaped, so nothing reads as a cross). Category labels fade in at the start of each group, and the last label fades out by 23.7 s, before the end card.

**Revision (Oct 18):** last label now fades out before the end card; z002 swapped for z009 and the cross-shaped sparkles replaced with round glows; photo window enlarged from 888×1184 to 940×1171 (about 4:5); crossfades lengthened to 0.5 s; z044 cropped to keep its price tag out. Every frame was checked at 4 fps for crosses, Stars of David and prominent tags.

## Files
- `zisel-trailer.mp4`: the ad · `zisel-trailer-poster.jpg`: poster frame (end card) · `zisel-trailer-contact-sheet.jpg`: 8 sample frames
- `src/gen.py` (HTML text/brand layers, rendered with headless Chrome into `assets/`), `src/music.py`, `src/render.py` (PIL frames piped to ffmpeg)

**Revision 2 (Oct 18):** music rewritten as an upbeat lounge/swing jazz bed (see Music above); video unchanged, audio remuxed (AAC 160k).
