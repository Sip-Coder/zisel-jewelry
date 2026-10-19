# Zisel Jewelry · Master Asset Inventory

**Last updated:** Sunday Oct 18, 2026, ~6:40 PM America/Los_Angeles (PDT)  
**Repo / project home:** `/workspace/zisel-jewelry/`  
**Working scratch / send packs:** `/workspace/zisel/`  
**Do not commit** this inventory update until Jonathan asks.

Every editable file should keep a matching PDF beside it (repo rule). This file’s PDF twin is `ASSETS.pdf`.

---

## Rules (client deliverables)

1. **No “Las Vegas”** on any client-facing asset (posters, invite, site, emails, cards, trailers).
2. **No website URL** on client assets sent to Shulkin (removed from photo business cards Oct 18 ~6:21 PM; posters / invite / trailers never had it).
3. **No category labels** on the trailer (RINGS / BRACELETS / etc. were dropped for the rev4 cut).
4. **Proper file extensions** on every deliverable (`.png`, `.jpg`, `.pdf`, `.mp4`, etc.).
5. **Poster 4** = stars-only / **no crosses** version for Shulkin’s local contacts (cross tile `z080` replaced with poster-2 top-center `z010`; Stars of David `z076` / `z002` stay).
6. Religious pieces: keep **poster 3** (cross + Star of David) for general use; use **poster 4** when he needs a no-cross local share.

---

## Known WhatsApp sends to Jonathan Shulkin (America/Los_Angeles)

| When (PDT) | What went out |
|---|---|
| **~11:30 AM Oct 18** | Early pack from `/workspace/zisel/send-1019/`: posters 1–3 (pre–heart-fix / pre–Shulkin-18 revisions), invite card, trailer-a + trailer-b (older cuts). Confirmation screenshot: `send-1019/sent-confirmation.png`. |
| **5:28 PM Oct 18** | Latest **posters 1, 2, 3** + **jazz** + **calm** trailers (31 s each, hearts crop fix). No caption. |
| **6:02 PM Oct 18** | Three **photo business cards** that still had the website: square, story, 3.5×2. **Superseded** by the no-URL re-render. |
| **~6:28 PM Oct 18** | **No-website** photo business cards (square, story, 3.5×2) + **poster 4** + **cafe-music trailer**. Silent trailer and Kevin-MacLeod music trials **not** in this send. |
| **6:32 PM Oct 18** | **Silent trailer** (`zisel-trailer-silent.mp4`, same 31 s cut, no audio). No caption. |
| **~6:36 PM Oct 18** | **Jazz Brunch**, **Lobby Time** and **Bossa Antigua** trailers, followed by a note naming each song (all Kevin MacLeod) and the license: CC BY 4.0, commercial use OK, credit line required when posted publicly (exact text in `/workspace/zisel/music-candidates/LICENSES.md`). |

---

## 1. Invite posters (1080×1350)

Navy + gold frame, “Book a Private Showing”, wholesale line, appointment + phone. Source HTML in `invite/print/`. Photos from `collection/photos/`.

### Poster 1 — current (no religious symbols)
| | |
|---|---|
| **Type** | Poster |
| **Outputs** | `/workspace/zisel-jewelry/invite/zisel-invite-poster.png` · `.jpg` · `.pdf` |
| **Editable** | `/workspace/zisel-jewelry/invite/print/poster.html` |
| **Photos** | z083, z024, z051, z019sq, z063, z074sq |
| **Version** | Oct 18 ~5:05 PM revision (current) |
| **Sent** | Yes — ~11:30 AM (older), again **5:28 PM** (current) |
| **Re-render** | Playwright Chromium screenshot of `poster.html` at 1080×1350 (see `/workspace/zisel/render.py` pattern); also export PDF/JPG from PNG. Serve `invite/print/` over HTTP so relative photo paths resolve. |
| **Backups** | `invite/backup-posters-2026-10-18-pre-shulkin15/` · `invite/backup-posters-2026-10-18-pre-shulkin18/` |

### Poster 2 — current (hearts tile fixed)
| | |
|---|---|
| **Type** | Poster |
| **Outputs** | `/workspace/zisel-jewelry/invite/zisel-invite-poster-2.png` · `.jpg` · `.pdf` |
| **Editable** | `/workspace/zisel-jewelry/invite/print/poster-2.html` |
| **Photos** | z037, z010, z068, z013sq, z001, **z004sq** (hearts: apple + drop pendant fully in frame) |
| **Version** | Oct 18 ~5:15 PM (heart pendant crop fix) |
| **Sent** | Yes — ~11:30 AM (older), again **5:28 PM** (fixed) |
| **Re-render** | Same as poster 1, target `poster-2.html` → `zisel-invite-poster-2.*` |
| **Backups** | Same backup folders as poster 1 |

### Poster 3 — current (cross + Star of David)
| | |
|---|---|
| **Type** | Poster |
| **Outputs** | `/workspace/zisel-jewelry/invite/zisel-invite-poster-3.png` · `.jpg` · `.pdf` |
| **Editable** | `/workspace/zisel-jewelry/invite/print/poster-3.html` |
| **Photos** | z075, z052, **z080** (crosses), z002, **z076** (Star of David), z011 |
| **Version** | Oct 18 ~5:06 PM revision |
| **Sent** | Yes — ~11:30 AM (older), again **5:28 PM** (current) |
| **Re-render** | `poster-3.html` → `zisel-invite-poster-3.*` |
| **Note** | Keep for clients who want religious pieces; for local no-cross shares use **Poster 4**. |

### Poster 4 — current (stars-only / no crosses) ★ for local contacts
| | |
|---|---|
| **Type** | Poster |
| **Outputs** | `/workspace/zisel-jewelry/invite/zisel-invite-poster-4.png` · `.jpg` · `.pdf` |
| **Editable** | `/workspace/zisel-jewelry/invite/print/poster-4.html` |
| **Photos** | z075, z052, **z010** (from poster 2 top-center, replaces crosses), z002, z076, z011 |
| **Version** | Oct 18 ~6:22 PM (new) |
| **Sent** | Yes — **~6:28 PM** with no-URL cards + cafe trailer |
| **Re-render** | `poster-4.html` → `zisel-invite-poster-4.*` |

### Poster comparison sheets (internal)
- `/workspace/zisel-jewelry/invite/zisel-posters-side-by-side.jpg`
- `/workspace/zisel-jewelry/invite/zisel-posters-before-after.jpg`
- `/workspace/zisel-jewelry/invite/zisel-posters-shulkin18-side-by-side.jpg`

---

## 2. Business cards

### Photo cards — CURRENT (no website) ★
Four tiles: **z083** pendants, **z024** ring tray, **z051** tennis bracelets (poster 1), **z013sq** gold hoops (poster 2). Tight gold inlay (`--hair:8px` / tile `--hair:3px`). Text: Jonathan Shulkin · Wholesale Diamond & Fine Jewelry · Call/Text 725.254.6937 · Private showings by appointment.

| Size | Outputs | Editable source |
|---|---|---|
| Square 1080×1080 | `/workspace/zisel-jewelry/brand/card_business_photo_1080.png` · `.pdf` | `invite/print/business-card-photo.html` |
| Story 1080×1920 | `/workspace/zisel-jewelry/brand/card_business_photo_story_1080x1920.png` · `.pdf` | `invite/print/business-card-photo-story.html` |
| Print 3.5×2 in | `/workspace/zisel-jewelry/brand/card_business_photo_3.5x2in.png` · `.pdf` | `invite/print/business-card-photo-3.5x2.html` |

| | |
|---|---|
| **Version** | Oct 18 ~6:21–6:22 PM (website removed) |
| **Sent** | Yes — **~6:28 PM** (current). Prior **6:02 PM** send was the with-URL set (superseded). |
| **Re-render** | Playwright screenshot / PDF of each HTML at its `@page` size; copy PNG+PDF into `brand/`. |
| **Backups (with URL — SUPERSEDED)** | `/workspace/zisel-jewelry/brand/archive/pre-nourl-1018/` (PNG+PDF for all three sizes) · HTML: `invite/print/backup-pre-nourl-1018/` |

### Text-only gold-frame cards (no photos)
| Size | Outputs | Editable |
|---|---|---|
| Square | `brand/card_business_gold-frame_1080.png` · `.pdf` | `invite/print/business-card.html` |
| Story | `brand/card_business_gold-frame_story_1080x1920.png` · `.pdf` | `invite/print/business-card-story.html` |

**Sent:** Not in today’s Shulkin packs (photo cards preferred). Still valid brand assets.

### Invite card (square cover)
| | |
|---|---|
| **Outputs** | `/workspace/zisel-jewelry/brand/card_invite_gold-frame_1080.png` · `.pdf` |
| **Editable** | `invite/print/card-cover.html` |
| **Sent** | Yes — ~11:30 AM (in `send-1019/4-invite-card.png`) |

---

## 3. Trailers (1080×1920, ~31 s, H.264)

**Current pipeline:** `trailer/rev4/render_v4.py` (PIL frames → ffmpeg). Brand layers from `trailer/assets/` (built via `trailer/src/gen.py` + headless Chrome). Shot list includes poster tiles + religious pieces for the longer cut; **no category labels** on rev4. Music is muxed per variant.

**Photos used (rev4 shot list):** z083, z024, z051, z019sq, z063, z074sq, z037, z010, z068, z013sq, z001, z004sq, z052, z002, z011, z080, z075, z076.

### CURRENT / sent variants

| Name | File | Music | Sent |
|---|---|---|---|
| **Jazz** | `/workspace/zisel-jewelry/trailer/rev4/zisel-trailer-jazz.mp4` (copy also in `deliver-1018/`) | Original synth jazz (`music_jazz.wav`) | **5:28 PM** |
| **Calm** | `/workspace/zisel-jewelry/trailer/rev4/zisel-trailer-calm.mp4` | Original calm bed (`music_calm.py` → wav) | **5:28 PM** |
| **Cafe** | `/workspace/zisel-jewelry/trailer/rev4/zisel-trailer-cafe.mp4` | Original upbeat coffee-shop jazz (`music_cafe.py`) — response to Shulkin’s [Happy Morning Coffee Shop short](https://youtube.com/shorts/Cji8ciXu3cA) | **~6:28 PM** |
| **Silent** | `/workspace/zisel/deliver-1018/zisel-trailer-silent.mp4` | No audio | **6:32 PM** |
| **Jazz Brunch** | `/workspace/zisel/deliver-1018/zisel-trailer-jazz-brunch.mp4` | "Jazz Brunch" Kevin MacLeod, CC BY 4.0 (credit required) | **~6:36 PM** |
| **Lobby Time** | `/workspace/zisel/deliver-1018/zisel-trailer-lobby-time.mp4` | "Lobby Time" Kevin MacLeod, CC BY 4.0 (credit required) | **~6:36 PM** |
| **Bossa Antigua** | `/workspace/zisel/deliver-1018/zisel-trailer-bossa-antigua.mp4` | "Bossa Antigua" Kevin MacLeod, CC BY 4.0 (credit required) | **~6:36 PM** |

### Non-religious backup batch (made ~6:50 PM Oct 18, **not sent**)
Same rev4 design and end card (no website, no labels), 31.0 s, 1080×1920 H.264, faststart. 14 photos instead of 18, each shown longer (1.63 s step instead of 1.25 s). **Removed:** z080 (crosses), z075 and z076 (Star of David), and z074sq (hamsa pendants, left out to keep this version fully non-religious). Other photos checked: no crosses or stars. Glints are round glows, not cross-shaped.

| Version | File | Music |
|---|---|---|
| Silent | `/workspace/zisel/deliver-1018/zisel-trailer-silent-nonreligious.mp4` | No audio |
| Jazz Brunch | `/workspace/zisel/deliver-1018/zisel-trailer-jazz-brunch-nonreligious.mp4` | Kevin MacLeod, CC BY 4.0 (credit required) |
| Lobby Time | `/workspace/zisel/deliver-1018/zisel-trailer-lobby-time-nonreligious.mp4` | Kevin MacLeod, CC BY 4.0 (credit required) |
| Bossa Antigua | `/workspace/zisel/deliver-1018/zisel-trailer-bossa-antigua-nonreligious.mp4` | Kevin MacLeod, CC BY 4.0 (credit required) |

**Editable source:** `trailer/rev4/render_v4_nonreligious.py <out.mp4>` (silent render), then mux the MP3s with ffmpeg: first 31 s, 1.5 s fade out, loudnorm I=-14, AAC 192k, `+faststart`. Contact sheet: `trailer/rev4/zisel-trailer-nonreligious-contact-sheet.jpg`.

License note sent with the ~6:36 PM batch. Credit line format: "&lt;Title&gt;" Kevin MacLeod (incompetech.com) / Licensed under Creative Commons: By Attribution 4.0 License / http://creativecommons.org/licenses/by/4.0/

Music source MP3s + license notes: `/workspace/zisel/music-candidates/` (`LICENSES.md`). Attribution required for MacLeod tracks.

### SUPERSEDED trailer cuts
| Rev | File | Notes |
|---|---|---|
| Rev1/2 | `/workspace/zisel-jewelry/trailer/zisel-trailer.mp4` | Early cut; also mirrored as `send-1019/trailer-a.mp4` / `trailer-b.mp4` |
| Rev3 | `/workspace/zisel-jewelry/trailer/rev3/zisel-trailer-v3.mp4` | Pre–hearts-fix / older music |

**Re-render rev4:** from `trailer/rev4/`, run `python3 render_v4.py` (writes frames → ffmpeg; music selected via cafe/calm/jazz logs or remux). Edit `music_*.py` then regenerate wav before remux.

**Contact sheets:** `trailer/zisel-trailer-contact-sheet.jpg`, `trailer/rev4/zisel-trailer-rev4-contact-sheet.jpg`, `trailer/zisel-trailer-poster.jpg`.

---

## 4. Logos

| Asset | Output | Editable |
|---|---|---|
| Primary (navy) | `brand/logo_zisel_gold-frame_primary.png` | `invite/print/logo-primary.html` |
| Horizontal (white) | `brand/logo_zisel_gold-frame_horizontal.png` | `invite/print/logo-horizontal.html` |
| Monogram seal | `brand/logo_zisel_monogram-seal.png` | `invite/print/logo-monogram.html` |

**Archive (earlier concepts):** `brand/archive/` — logo_A/B/C, stickers, flyer, old front-back card.  
**Re-render:** `/workspace/zisel/render.py` (Playwright jobs for logos + card-cover + poster 1 + invite PDF).

---

## 5. Invite page + PDF

| Asset | Paths |
|---|---|
| Live e-invite | `/workspace/zisel-jewelry/invite/index.html` (+ `zisel.css`, `lightbox.js`, `gem.svg`, `fonts/`) |
| Invite PDF | `/workspace/zisel-jewelry/invite/Zisel_Invite_Private_Showings.pdf` |
| PDF source | `invite/print/invite-pdf.html` |
| Docs | `invite/README.md` · `invite/README.pdf` |

**Sent:** Invite card PNG in ~11:30 AM pack; full PDF not listed in later WhatsApp batches.  
**Notes:** Star of David / cross on invite page replaced Oct 14 with z024 / z065; Las Vegas removed Oct 18.

---

## 6. Website / collection / email / deck / research

| Type | Paths | Editable / notes |
|---|---|---|
| Main site | `index.html` | Live: https://sip-coder.github.io/zisel-jewelry/ |
| Collection (83 photos) | `collection/index.html`, `collection/photos/` (~173 files incl. thumbs) | `collection/README.md` · `.pdf` |
| Market snapshot deck | `deck/Zisel_Market_Snapshot.pptx` · `.pdf` (also root `Zisel_Market_Snapshot.pdf`) | PowerPoint |
| Research | `research/*.md` · matching `.pdf`; `competitors.csv` · `.pdf`; playbook `.docx` · `.pdf` | |
| Email drafts | `email/index.html`, `email/v3|v4|v5/` | Hero GIFs, tile JPGs |
| Site previews | `site-previews/*.png` | Screenshots |

**Not WhatsApp client packs** (internal / site).

---

## 7. Invoices & time log (Sip Studies)

| Asset | Paths |
|---|---|
| Time log (current) | `/workspace/zisel-invoice/Zisel_Time_Log.xlsx` · `.pdf` |
| Draft invoice SS-2026-001 | `/workspace/zisel-invoice/draft-2026-10-18/` (PDF + xlsx + `inv/build_draft.py`) |
| Invoice template + sample | `/workspace/sipstudies-invoice/` (`build.py`, logos, Sample_Zisel + Template xlsx/pdf) |
| Backup | `/workspace/zisel-invoice/backup-2026-10-18/` |

**Sent to Shulkin:** No (billing / internal).

---

## 8. Photo sources & revision packs

| Pack | Path | Role |
|---|---|---|
| Full cleaned gallery | `/workspace/zisel-jewelry/collection/photos/` | Master photos for posters / trailers / cards |
| Shulkin 18-photo bundle | `/workspace/zisel/shulkin-18/` | Original WhatsApp JPEGs (Oct 14) |
| Revisions capture | `/workspace/zisel/revisions-1018/` | Voice notes, 18 photos, `messages.md`, `transcripts.md`, contact sheet |
| Early send pack | `/workspace/zisel/send-1019/` | Snapshot of ~11:30 AM WhatsApp send |
| Deliver staging | `/workspace/zisel/deliver-1018/` | Current trailer variants for handoff |
| Music candidates | `/workspace/zisel/music-candidates/` | Open-source jazz trials + `LICENSES.md` |
| WhatsApp notes | `/workspace/zisel/shulkin-whatsapp.md` | Thread log |

Useful crops: `z004sq.jpg` (hearts, zoomed out), `z013sq.jpg`, `z019sq.jpg`, `z074sq.jpg`.

---

## 9. How to re-render (cheat sheet)

**Posters / photo cards / logos (HTML → PNG/PDF)**  
1. Serve `/workspace/zisel-jewelry/` (or `invite/print/` with collection reachable).  
2. Playwright + `/usr/bin/google-chrome`: open the HTML, viewport = design size, `page.screenshot` → PNG; `page.pdf` for print PDF.  
3. Pattern script: `/workspace/zisel/render.py` (extend jobs list for poster-2/3/4 and photo cards).  
4. Always write matching PDF next to PNG/MD.

**Trailers**  
1. Brand layers: `cd trailer/src && python3 gen.py` → `trailer/assets/`.  
2. Music: `python3 music_cafe.py` (or calm / jazz) in `trailer/rev4/`.  
3. Video: `python3 render_v4.py` → `zisel-trailer-*.mp4`.  
4. Silent: remux without audio track into `deliver-1018/`.

**Invoice**  
- Template: `python3 /workspace/sipstudies-invoice/build.py`  
- Draft: `python3 /workspace/zisel-invoice/draft-2026-10-18/inv/build_draft.py`

---

## 10. Status snapshot (end of Oct 18 workday)

| Item | Status |
|---|---|
| Posters 1–3 (latest) | Sent 5:28 PM |
| Poster 4 (no crosses) | Sent ~6:28 PM |
| Photo cards no-URL (3 sizes) | Sent ~6:28 PM |
| Jazz + calm trailers | Sent 5:28 PM |
| Cafe trailer | Sent ~6:28 PM |
| Silent trailer | Ready, **not sent** |
| MacLeod music trials | Ready for Jonathan’s pick; **not sent**; need CC BY credit if used |
| Cards with website (6:02 PM) | **Superseded** — keep only in `brand/archive/pre-nourl-1018/` |
| Older posters / rev1–3 trailers | **Superseded** — backups under `invite/backup-*` and `trailer/` / `send-1019/` |

---

## Folder map (quick)

```
/workspace/zisel-jewelry/          ← project repo (brand, invite, trailer, collection, deck, email, research)
/workspace/zisel/                  ← scratch: deliver-1018, send-1019, revisions-1018, music-candidates, shulkin-18, render.py
/workspace/zisel-invoice/          ← time log + draft invoice
/workspace/sipstudies-invoice/     ← invoice template + sample
```

---

## Repo paths (GitHub: Sip-Coder/zisel-jewelry), updated Oct 18, 2026

| What | Repo path |
|---|---|
| Send-ready trailers (jazz, calm, cafe, silent, jazz-brunch, lobby-time, bossa-antigua + `*-nonreligious`) | `deliverables/videos/` |
| Kevin MacLeod MP3s + license/credit lines | `music/` (`LICENSES.md`) |
| Shulkin's revision photos (18) + contact sheet | `photos/shulkin-revisions-1018/` |
| Posters 1–4 outputs / sources | `invite/` / `invite/print/` |
| Business cards (photo + text), archive | `brand/`, `brand/archive/` |
| Trailer scripts and renders | `trailer/rev3/`, `trailer/rev4/` |

Not in the public repo (private): invoices, time logs, Shulkin's messages/transcripts, voice notes.

## Private repo

Invoice, time log and client communications are kept in the private repo **Sip-Coder/zisel-jewelry-private** (access restricted).

## Marketing trailers (non-religious, renamed) — sent Oct 18 ~6:55 PM PT
- deliverables/videos/zisel-marketing-jazz-brunch.mp4, -lobby-time.mp4, -bossa-antigua.mp4, -silent.mp4 (copies of the *-nonreligious renders; no crosses, Stars of David or hamsa).
- Sent to Shulkin by Jonathan himself on WhatsApp, with the caption "these are versions without any of the religious symbols just in case". One earlier copy (jazz-brunch-nonreligious) also went through at 6:50 PM.
- Music credit (CC BY 4.0) is still required when posted publicly.
