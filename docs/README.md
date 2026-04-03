# 📚 Baitul Hikmah — Documentation Index

> Semua dokumentasi produk dalam satu tempat.
> **PRD.md adalah sumber kebenaran** — semua code harus trace back ke PRD section.

---

## 📋 Core Documents

| Document | Purpose | Status |
|----------|---------|--------|
| **[PRD.md](PRD.md)** | Product Requirements — fitur, UI, data model | 🚀 Active |
| **[content-style-guide.md](content-style-guide.md)** | Aturan penulisan, sitasi, format Quran, QA | 🚀 Active |
| **[illustration-guide.md](illustration-guide.md)** | Pipeline image generation, children mode rules | 🚀 Active |
| **[illustration-registry.md](illustration-registry.md)** | Character & location visual consistency bible | 🚀 Active |
| **[development-workflow.md](development-workflow.md)** | Multi-agent model, content & feature pipeline | 🚀 Active |
| **[design-guide.md](design-guide.md)** | Color system, moodboard per era | 🚀 Active |

---

## 🔄 Workflows

### Workflow A: General Content (Artikel Dewasa)

```
1. READ   → docs/content-style-guide.md (aturan penulisan, sitasi, Quran)
2. WRITE  → content/events/{event}/general-id.md + general-en.md
3. META   → src/data/events-database.json (title, year, sources — sinkron dengan bibliography)
4. QA     → V1-V9 checklist (see content-style-guide.md Section 11)
5. SYNC   → node scripts/build-content.js → event-content-map.json
6. PUSH   → git push origin develop
7. VERIFY → develop.baitul-hikmah.pages.dev
```

### Workflow B: Children Content (Slideshow Anak-Anak)

```
1. READ   → docs/content-style-guide.md Section 4 (children mode)
2. WRITE  → content/events/{event}/children-id.md + children-en.md
3. BRIEF  → docs/briefs/{event}.md (self-contained image prompts)
4. QA     → Slide count ID = EN, no forbidden phrases, brief format ✓
5. SYNC   → node scripts/build-content.js
6. UPLOAD → Brief ke Google Drive (Baitul Hikmah/prompt folder)
```

### Workflow C: Image Generation

```
1. READ   → docs/illustration-guide.md + docs/illustration-registry.md
2. OPEN   → Brief dari docs/briefs/{event}.md — setiap slide = 1 prompt copy-paste
3. PASTE  → Prompt ke Gemini (sudah self-contained, tinggal paste)
4. SAVE   → public/illustrations/children/{event}/slide-NN.png
5. QA     → No text, no prophet depiction, safe zone, 16:9
```

---

## 📁 Content Structure

```
content/events/{event-id}/
├── general-id.md      → Artikel dewasa (Bahasa Indonesia)
├── general-en.md      → Artikel dewasa (English)
├── children-id.md     → Slideshow anak (Bahasa Indonesia)
└── children-en.md     → Slideshow anak (English)
```

**Per file rules:**
- `general-*.md`: Consolidated bibliography, ^N citations, blockquote Quran with Arabic
- `children-*.md`: Section-based slides, `🎨 *Ilustrasi:*` brief per slide, no `<ayat>` tags

---

## 🗄 Archive

| File | Content |
|------|---------|
| [archive/sprint-log.md](archive/sprint-log.md) | Sprint milestone history (Mar 2026) |
| [archive/design-decisions.md](archive/design-decisions.md) | Design decisions log |
| [archive/children-drafts/](archive/children-drafts/) | 48 early children content drafts |

---

## ⚠️ Key Rules

1. **PRD first** — no code without PRD section reference (`// PRD#X.X`)
2. **Blockquote for Quran** — `> Arabic text` + `> *"Translation"*` + `> — QS. ref` (NOT `<ayat>` tags)
3. **Consolidated bibliography** — 1 entry per unique source, `^N` citations
4. **Children format** — `🎨 *Ilustrasi: description*` (inline italic, NOT bold multi-line)
5. **Slide count sync** — children-id = children-en (BLOCKER)
6. **Card sync** — events-database.json sources[] must match article bibliography
