# 📚 Baitul Hikmah — Documentation Index

> Semua dokumentasi produk dalam satu tempat.

## 🚀 Quick Start — Reading Order

**Mau generate image?** Baca urutan ini:
1. `illustration-registry.md` — master character descriptions (WAJIB copy-paste)
2. `briefs/e{XX}-{name}.md` — brief per episode + character lock
3. `illustration-guide.md` — rules, larangan, Islamic compliance
4. `operations/batch-image-generation-v4.md` — workflow & script

**Mau tulis konten baru?** Baca + lakukan:
1. `content-style-guide.md` — aturan penulisan, sitasi, format Quran/Hadits
2. `PRD.md` — product requirements lengkap
3. **WAJIB buat `metadata.json`** di `content/events/{event}/` (lihat template di bawah)
4. **WAJIB buat brief** di `docs/briefs/{event}.md` jika ada ilustrasi

## 📋 New Event Checklist

Setiap event baru WAJIB punya:

```
content/events/{event}/
├── metadata.json      ← WAJIB (title, year, era, sources)
├── children-en.md     ← story content (English)
├── children-id.md     ← story content (Indonesian)
├── general-en.md      ← adult content (English)
└── general-id.md      ← adult content (Indonesian)

docs/briefs/{event}.md ← WAJIB jika ada ilustrasi
```

### metadata.json Template
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
| [Briefs per Episode](briefs/) | Brief + character lock per episode (e01, e02, ...) |

### Briefs

| File | Event | Slides |
|------|-------|--------|
| [e01-tahun-gajah.md](briefs/e01-tahun-gajah.md) | Tahun Gajah | 11 |
| [e02-yatim-piatu.md](briefs/e02-yatim-piatu.md) | Yatim Piatu | 15 |
| [e03-perjalanan-syam.md](briefs/e03-perjalanan-syam.md) | Perjalanan Syam | 11 |
| [e04-pernikahan-khadijah.md](briefs/e04-pernikahan-khadijah.md) | Pernikahan Khadijah | 12 |

## Operations

| Doc | Fungsi |
|-----|--------|
| [Image Generation v4](operations/batch-image-generation-v4.md) | **ACTIVE** — proven workflow PinchTab → Gemini → download → compress |
| [Archive](operations/archive/) | v2, v3, old pipeline (reference only) |

## Quick Links

- **Dev**: https://develop.baitul-hikmah.pages.dev
- **Prod**: https://baitul-hikmah.id
- **Repo**: https://github.com/ahmadsyaifulloh08/baitul-hikmah

## Folder Structure

```
docs/
├── README.md              ← you are here
├── PRD.md                 ← product requirements
├── content-style-guide.md ← writing rules
├── design-guide.md        ← visual design system
├── illustration-registry.md ← CHARACTER SSoT
├── illustration-guide.md  ← illustration rules
├── briefs/                ← per-episode briefs
│   ├── e01-tahun-gajah.md
│   ├── e02-yatim-piatu.md
│   ├── e03-perjalanan-syam.md
│   └── e04-pernikahan-khadijah.md
└── operations/
    ├── batch-image-generation-v4.md  ← ACTIVE workflow
    └── archive/                       ← old versions
```
