# 🕌 Baitul Hikmah — Menelusuri Jejak Peradaban Islam

> "Sesungguhnya para nabi tidak mewariskan dinar ataupun dirham, tetapi mewariskan ilmu."
> — HR. Abu Dawud, Tirmidzi, Ibnu Majah

Portal digital interaktif untuk menelusuri sejarah peradaban Islam — dari Tahun Gajah (570 M) hingga jatuhnya Acre (1291 M). 129 events, 7 era, bilingual ID/EN.

## 🌐 Links

- **Production**: [baitul-hikmah.id](https://baitul-hikmah.id)

## ✨ Features

- **Interactive Timeline** — 129 events across 7 eras, multi-select category filters, search
- **GIS Map Mode** — MapLibre GL JS + CARTO tiles, year slider, event markers with fly-to
- **Dual Audience** — General mode (academic articles with citations) & Children mode (slideshow)
- **Bilingual** — Bahasa Indonesia & English, toggle per page
- **Verified Sources** — Consolidated bibliography, Quran with Arabic text, hadith with numbers

## 🛠 Tech Stack

- **Framework**: Next.js 14 (App Router, static export)
- **Styling**: CSS (public/styles.css) — light mode only
- **Map**: MapLibre GL JS + CARTO raster basemaps
- **Content**: Markdown (general + children) → JSON (event-content-map.json)
- **Data**: events-database.json (129 events, eras, categories, regions)
- **Hosting**: Cloudflare Pages (static)
- **Typography**: Playfair Display, Inter, Amiri (Arabic RTL)

## 📁 Project Structure

```
├── src/
│   ├── app/
│   │   ├── page.tsx            → Homepage (Timeline + Map) [PRD#3.1, #3.2]
│   │   ├── about/page.tsx      → About page [PRD#3.4]
│   │   └── event/[slug]/
│   │       ├── page.tsx         → Event detail [PRD#3.3]
│   │       └── EventContent.tsx → Article + Children slideshow [PRD#3.3, #2B]
│   ├── components/
│   │   ├── Timeline.tsx         → Timeline grid [PRD#3.1]
│   │   ├── MapView.tsx          → GIS map [PRD#3.2]
│   │   └── Header.tsx           → Navigation + i18n [PRD#5]
│   ├── i18n/context.tsx         → ID/EN language context [PRD#5]
│   └── lib/
│       ├── data.ts              → Event data loader [PRD#9]
│       └── map-data.ts          → GeoJSON converter [PRD#9, #3.2]
├── content/events/              → 129 event content (general + children, ID + EN)
├── docs/
│   ├── PRD.md                   → Product Requirements Document
│   ├── content-style-guide.md   → Content writing rules, citations, Quran format
│   ├── illustration-guide.md    → Children illustration pipeline & QA
│   ├── illustration-registry.md → Character & location visual bible
│   ├── briefs/                  → 129 image generation briefs (per event)
│   └── development-workflow.md  → Multi-agent development model
└── src/data/
    ├── events-database.json     → Master event data (129 events)
    └── event-content-map.json   → Compiled markdown content
```

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [PRD.md](docs/PRD.md) | Product requirements — all code traces back here |
| [content-style-guide.md](docs/content-style-guide.md) | Writing rules, citation format, QA checklist |
| [illustration-guide.md](docs/illustration-guide.md) | Image generation pipeline, children mode rules |
| [illustration-registry.md](docs/illustration-registry.md) | Character descriptions, location visuals, consistency |
| [development-workflow.md](docs/development-workflow.md) | Multi-agent workflow, content pipeline |

## 🔗 SDLC Traceability

Every source file references its PRD section via `// PRD#X.X` comments. See [SDLC v2.0](../../dashboard/data/sdlc.json) for the development lifecycle.

## 📊 Content Stats

- **129 events** (e01–e129) across 7 eras
- **516 content files** (general-id, general-en, children-id, children-en per event)
- **1.465 illustration slides** (briefs ready for image generation)
- **102 events** with Quran verses (Arabic + translation in blockquote format)
