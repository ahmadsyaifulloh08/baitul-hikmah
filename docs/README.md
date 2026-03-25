# 📚 Baitul Hikmah — Documentation Index

> Semua dokumentasi produk dalam satu tempat.

---

## 🔄 Workflows

### Workflow A: General Content (Artikel Dewasa)

```
1. READ   → docs/content-style-guide.md (aturan penulisan, sitasi, Quran)
2. WRITE  → content/events/{event}/general-id.md + general-en.md
3. META   → content/events/{event}/events-database.json (title, year, sources)
4. STATUS → src/data/events-database.json → ubah status: "draft" → "published"
5. QA     → python3 scripts/qa-all.py --quick
6. SYNC   → node scripts/build-content.js
7. PUSH   → git push origin develop
8. VERIFY → cek di develop.baitul-hikmah.pages.dev
```

**Docs yang WAJIB dibaca:**
1. `content-style-guide.md` — sitasi consolidated, format Quran, daftar pustaka
2. `PRD.md` — product requirements

**QA checks (automated):**
- ✅ Citations: consolidated format, ^N ≤ bibliography entries
- ✅ Quran: Arabic text + separators
- ✅ Metadata: completeness
- ✅ Card pustaka: "Title — Author" format

### Workflow B: Children Content + Illustrations

```
1. READ   → content-style-guide.md + illustration-registry.md + illustration-guide.md
2. WRITE  → content/events/{event}/children-id.md + children-en.md
3. BRIEF  → docs/briefs/{event}.md (character lock, base palette, per-slide brief)
4. PREP   → Phase 0: generate prompt files, pre-generate checklist, Ahmad approve prompts
5. GENERATE → PinchTab v4 workflow (new chat per slide, 7s wait, before/after download)
6. COMPRESS → sharp resize 1792x1024 + PNG level 9 (target 1-2MB)
7. QA     → python3 scripts/qa-all.py (full — includes images)
8. CODE   → Update EventContent.tsx childrenIllustrations mapping
9. SYNC   → node scripts/build-content.js
10. PUSH  → git push origin develop
11. VERIFY → Ahmad review di develop.baitul-hikmah.pages.dev
```

**Docs yang WAJIB dibaca:**
1. `illustration-registry.md` — master character descriptions (WAJIB copy-paste)
2. `briefs/{event}.md` — per-episode brief + character lock
3. `illustration-guide.md` — rules, larangan, Islamic compliance
4. `operations/batch-image-generation-v4.md` — workflow & script

**Image rules:**
- Golden glow slides → generate dalam 1 chat session (konsistensi)
- Max 750 chars per prompt, no `()`, no `'`, no `—`
- Prompt WAJIB pakai STYLE LOCK + CHARACTER LOCK format
- Ahmad approve prompts SEBELUM generate

---

## 📋 New Event Checklist

Setiap event baru WAJIB punya:

```
content/events/{event}/

├── children-en.md     ← story content (English)
├── children-id.md     ← story content (Indonesian)
├── general-en.md      ← adult content (English)
└── general-id.md      ← adult content (Indonesian)

docs/briefs/{event}.md ← WAJIB jika ada ilustrasi

src/data/events-database.json → status: "draft" → "published"
```

### QA Scripts
```bash
# Full QA (citations + quran + metadata + images)
python3 scripts/qa-all.py

# Quick QA (citations + quran + metadata — no image check)
python3 scripts/qa-all.py --quick

# Per event
python3 scripts/qa-all.py e04

# Individual checks
python3 scripts/check-citations.py          # articles + cards
python3 scripts/check-quran-format.py       # Quran Arabic text
python3 scripts/check-metadata.py           # event completeness
python3 scripts/check-images.py             # illustration files

# Content sync (.md → website JSON)
node scripts/build-content.js

# Quran API tools
python3 scripts/fetch-quran.py 105:1-5      # fetch Arabic text
python3 scripts/fix-quran-refs.py --fix     # auto-insert Arabic
```

### events-database.json Template
```json
{
  "id": "eXX",
  "title_id": "...",
  "title_en": "...",
  "year": "XXX M",
  "era": "...",
  "location": "...",
  "tags": ["..."],
  "sources": [
    {"id": "...", "title": "...", "author": "...", "type": "primary|hadith"}
  ]
}
```

### events-database.json Status
```json
{
  "status": "published"  // or "draft"
}
```
- `draft` = content belum ditulis (69 events)
- `published` = content lengkap + QA pass (59 events)

---

## Product

| Doc | Fungsi |
|-----|--------|
| [PRD](PRD.md) | Product Requirements — fitur, tech stack, design decisions, deploy, QA |
| [Design Guide](design-guide.md) | Color system, typography, moodboard per era, components |

## Content

| Doc | Fungsi |
|-----|--------|
| [Content Style Guide](content-style-guide.md) | Aturan penulisan, sitasi, format Quran/Hadits, QC checklist |

## Illustration

| Doc | Fungsi |
|-----|--------|
| [Illustration Registry](illustration-registry.md) | **SSoT** — master character descriptions, locations, palettes |
| [Illustration Guide](illustration-guide.md) | Rules, larangan, Islamic compliance, QA checklist |
| [Briefs per Episode](briefs/) | Brief + character lock per episode |
| [Image Gen v4](operations/batch-image-generation-v4.md) | **ACTIVE** — PinchTab workflow |

### Briefs

| File | Event | Slides |
|------|-------|--------|
| [e01-tahun-gajah.md](briefs/e01-tahun-gajah.md) | Tahun Gajah | 11 |
| [e02-yatim-piatu.md](briefs/e02-yatim-piatu.md) | Yatim Piatu | 15 |
| [e03-perjalanan-syam.md](briefs/e03-perjalanan-syam.md) | Perjalanan Syam | 11 |
| [e04-pernikahan-khadijah.md](briefs/e04-pernikahan-khadijah.md) | Pernikahan Khadijah | 12 |

## CI/CD

```
git push develop
  → Cloudflare Pages build
  → prebuild: python3 qa-all.py --quick   ← QA GATE (fail = no deploy)
  → node build-content.js                 ← sync .md → JSON
  → next build                            ← website build
  → Deploy ✅
```

## Quick Links

- **Dev**: https://develop.baitul-hikmah.pages.dev
- **Prod**: https://baitul-hikmah.id
- **Repo**: https://github.com/ahmadsyaifulloh08/baitul-hikmah

## Folder Structure

```
docs/
├── README.md                 ← you are here
├── PRD.md                    ← product requirements
├── content-style-guide.md    ← writing rules
├── design-guide.md           ← visual design system
├── illustration-registry.md  ← CHARACTER SSoT
├── illustration-guide.md     ← illustration rules
├── briefs/                   ← per-episode image briefs
└── operations/
    ├── batch-image-generation-v4.md  ← ACTIVE workflow
    └── archive/

scripts/
├── qa-all.py                 ← QA runner (prebuild CI/CD)
├── check-citations.py        ← articles + cards
├── check-quran-format.py     ← Quran Arabic text
├── check-metadata.py         ← event completeness
├── check-images.py           ← illustration files
├── build-content.js          ← .md → JSON (prebuild)
├── sync-content.py           ← alternative sync
├── fetch-quran.py            ← Quran API helper
├── fix-quran-refs.py         ← auto-insert Arabic text
└── archive/

src/data/
├── events-database.json      ← master event list (128 events, status field)
└── event-content-map.json    ← content for website (generated by build-content.js)

content/events/
├── e01-tahun-gajah/          ← general-*.md, children-*.md, events-database.json
├── e02-yatim-piatu/
├── ...
└── e128-.../

public/illustrations/children/
├── e01/                      ← slide-01.png, slide-02.png, ...
├── e02/
├── e03/
└── e04/
```
