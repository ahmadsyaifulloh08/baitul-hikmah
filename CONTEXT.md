# Baitul Hikmah — Project Context

> **Baca file ini setelah compaction untuk mendapatkan konteks lengkap project.**
> Last updated: 2026-03-16

## Overview

Website sejarah Islam interaktif dengan timeline, peta, dan mode anak-anak (slideshow ilustrasi AI).
- **URL Develop**: https://develop.baitul-hikmah.pages.dev
- **URL Produksi**: https://baitul-hikmah.id (belum deploy, masih di develop)
- **Stack**: Next.js 14, Static Export, Cloudflare Pages, Tailwind CSS, Framer Motion, MapLibre GL
- **Hosting**: Cloudflare Pages (free tier, 500 deploy/bulan)

## Project Structure

```
/workspace/projects/baitul-hikmah/
├── CONTEXT.md              ← FILE INI — baca pertama
├── docs/
│   └── PRD.md              ← Product Requirements Document (master reference)
├── design/
│   ├── design-system.md    ← Warna, font, komponen
│   ├── moodboard-per-era.md
│   ├── image-briefs-children.md      ← Brief v1 (deprecated)
│   ├── image-briefs-children-v3.md   ← Brief v3 (active) — 1 brief per slide
│   └── assets/             ← SVG patterns, icons, badges
├── content/events/
│   ├── e01-tahun-gajah/    ← general-id.md, children-id.md, *-en.md, metadata.json
│   ├── e02-yatim-piatu/    ← same structure
│   └── e{NN}-*/            ← 12 events total, 2 fully developed (e01, e02)
├── public/
│   ├── illustrations/children/  ← AI-generated PNGs (e01: 11, e02: 15 = 26 total)
│   └── styles.css
├── src/
│   └── app/event/[slug]/EventContent.tsx  ← Main component: slideshow, renderer, parser
├── scripts/
│   ├── build-content.js    ← Markdown → JSON builder
│   ├── audit-slides.js     ← Simulate slide split (verify narasi↔gambar mapping)
│   ├── gen-all-27.py       ← Batch generation script (reference)
│   └── regen-*.py, gen-*.py ← Per-image regeneration scripts
├── README.md
└── CONTRIBUTING.md
```

## Key Files

| File | Purpose |
|------|---------|
| `docs/PRD.md` | Master reference — Section 16 = illustration pipeline & QA |
| `src/app/event/[slug]/EventContent.tsx` | Slideshow component + `parseChildrenSlides()` + `childrenIllustrations` mapping |
| `design/image-briefs-children-v3.md` | Active briefs — 1 per slide, character consistency in header |
| `scripts/audit-slides.js` | Simulate slide split — WAJIB jalankan sebelum generate gambar |
| `scripts/build-content.js` | Content builder: markdown → JSON (di-run sebelum `next build`) |

## Credentials (JANGAN cat langsung — auto-loaded)

| File | Purpose |
|------|---------|
| `/workspace/credentials/api-gemini.txt` | Gemini API key (image generation) |
| `/workspace/credentials/cloudflare-baitul-hikmah-token.txt` | CF Pages deploy token |

## Build & Deploy

```bash
cd /workspace/projects/baitul-hikmah
node scripts/build-content.js
npx tailwindcss -i src/app/globals.css -o src/app/compiled.css --minify
cp src/app/compiled.css public/styles.css
npx --cache /workspace/.npm-cache next build
CLOUDFLARE_API_TOKEN=$(cat /workspace/credentials/cloudflare-baitul-hikmah-token.txt) \
CLOUDFLARE_ACCOUNT_ID=e4cd70f84267e96fcb4391058053b995 \
npx wrangler pages deploy out --project-name=baitul-hikmah --branch=develop --commit-dirty=true
```

## Image Generation (Gemini API)

```bash
# Model: gemini-2.5-flash-image
# Endpoint: https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent
# Output: selalu 1024×1024 (tidak bisa 16:9)
# Key: cat /workspace/credentials/api-gemini.txt

# Setiap prompt WAJIB include:
# 1. Safe zone: subjek di CENTER 70%, head < 30% dari atas
# 2. No text: "ABSOLUTELY NO TEXT of any kind"
# 3. Prophet: "nur/cahaya only, NO human figure"
```

## Children Slideshow — Slide Mapping

| Event | Slides | Images | Image naming |
|-------|--------|--------|-------------|
| e01-tahun-gajah | 11 | 11 | `e01-slide-01.png` ... `e01-slide-11.png` |
| e02-yatim-piatu | 15 | 15 | `e02-slide-01.png` ... `e02-slide-15.png` |

`childrenIllustrations` di `EventContent.tsx` maps `contentDir → image paths[]` (sequential).

## Content & Illustration Pipeline (from PRD 16.7)

```
Phase 0: CONTENT AUTHORING
  0.1 Tulis narasi children-id.md (per section)
  0.2 Simulasi slide split (audit-slides.js) → verify jumlah & text per slide
  0.3 Verify: setiap slide punya scene visual UNIK (gabung jika redundan)
  0.4 Tulis image brief per slide (bukan per section!)

Phase 1: IMAGE GENERATION
  1.1 Generate batch via Gemini API
  1.2 Slide↔Image mapping audit — verify setiap gambar cocok narasinya

Phase 2: QA ILUSTRASI (6-point checklist, vision model)
  A. Larangan Nabi ﷺ (BLOCKER)
  B. Kesesuaian Narasi↔Ilustrasi (BLOCKER)
  C. Konsistensi Visual (WARNING)
  D. Technical — resolusi, artefak (WARNING)
  E. No Text in Image (BLOCKER)
  F. Safe Zone Composition (BLOCKER)

Phase 3: DEPLOY
  Build → CF Pages deploy → Verify di browser
```

## Islamic Rules (MUTLAK)

1. **Nabi Muhammad ﷺ** = HANYA cahaya/nur (golden orb, light column, glowing bundle). TIDAK BOLEH: wajah, tubuh, siluet, bayi, anak, bayangan.
2. **No text in images** — no captions, labels, watermarks, signatures, writing apapun.
3. **Statues/idols** = haram. 2D animal illustrations = boleh.
4. **Hadith format**: `"kutipan" (HR Bukhari, no. 2262).` — titik SETELAH parenthetical.
5. **Arabic text**: HANYA untuk ayat Quran + hadits. BUKAN untuk istilah/nama/tempat.

## Lesson Learned (ringkasan)

- **Jangan full batch regenerate** — selective fix saja, backup dulu
- **Brief = per SLIDE**, bukan per section (section bisa split jadi 2-3 slide)
- **Slide yang scene-nya mirip → gabung** (kurangi redundansi)
- **Sentence splitter**: protect abbreviasi (`no.`, `HR.`, `QS.`) dengan placeholder `\uFFFC`
- **Gemini selalu output 1024×1024** — safe zone composition adalah solusinya
- **`object-fit: cover`** (bukan `contain`) — contain = not fullscreen, rejected
- **Mapping audit WAJIB** setelah generate batch (jangan asumsikan urutan)

## Current Status (2026-03-16)

- e01 (Tahun Gajah): 11 slides, semua gambar match narasi ✅
- e02 (Yatim Piatu): 15 slides, semua gambar match narasi ✅
- Deploy ke develop branch: ~35 deploys
- PRD: Section 16 lengkap (pipeline, QA, lesson learned)
- Production deploy: belum (menunggu approval Ahmad)
- Events e03+: belum dimulai
- Git push ke GitHub: pending
