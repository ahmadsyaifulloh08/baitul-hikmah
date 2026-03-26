# Batch Content Generation Brief — Baitul Hikmah

## Task
Generate bilingual content (ID + EN) for assigned Islamic history events. Each event needs 4 markdown files:
1. `general-id.md` — Artikel dewasa (Bahasa Indonesia)
2. `general-en.md` — Adult article (English)
3. `children-id.md` — Konten anak-anak (Bahasa Indonesia)
4. `children-en.md` — Children content (English)

## MANDATORY: Read These Files First
1. `/workspace/projects/baitul-hikmah/docs/content-style-guide.md` — ALL writing rules, citation format, Quran format
2. `/workspace/docs/prd/baitul-hikmah-website.md` — Product requirements (sections 1-4 for context, section 15 for content rules)

## Output Location
Write files to: `/workspace/projects/baitul-hikmah/content/events/{event-folder}/`

Folder naming: `{event_id}-{slug}` (e.g., `e50-revolusi-abbasiyah`, `e51-imam-abu-hanifah`)
- Slug = lowercase, hyphenated, Indonesian version of title
- Keep slug concise (3-5 words max)

## General Article Rules (general-id.md / general-en.md)
- **Structure**: `# Title` → `## Context` → `## Main Event` → `### Sub-sections` → `## Analysis/Hikmah` → `---` → `## Daftar Pustaka`
- **Length**: 800-1500 words per language
- **Citations**: Consolidated bibliography. Min 3 unique sources. Sequential numbering (^1, ^2, ^3). Same source = same number.
- **Quran format**: Arabic text with ﴿N﴾ markers (RTL) + translation with ﴾N﴿ markers (LTR). ONLY in blockquotes.
- **Hadith format**: Include hadith number + kitab/bab. E.g., "HR Muslim, no. 1162, Kitab al-Shiyam"
- **Arabic text**: ONLY for Quran verses and Hadith. NOT for terms, names, places.
- **If article quotes Quran**: Al-Qur'an al-Karim MUST be an entry in Daftar Pustaka (last entry)
- **Tone**: Academic-popular, narrative but scholarly
- **Year format**: "570 M" (ID) / "570 CE" (EN)
- **Bold** first mention of key figures: "**Imam Abu Hanifah** (Nu'man bin Tsabit)"
- **Italic** for Arabic transliterations: *qabilah*, *madzhab*, *ijma'*

## Children Content Rules (children-id.md / children-en.md)
- **4 sections** with emoji headers, separated by `---`
- **Section headers** depend on event type:
  - Figure/Tokoh: 🧑 Siapa dia? → ⭐ Apa yang dilakukan? → 💡 Kenapa luar biasa? → 📖 Dalil
  - Event/Peristiwa: 🌍 Apa yang terjadi? → 📖 Ceritanya → 🌟 Pelajarannya → 🤲 Doa & Dalil
  - Civilization/Ilmu: 🏛 Fun fact → 🔬 Penjelasan → 🌍 Dampak modern → 📖 Islam & Ilmu
- **Tone**: Informative-light, NOT storytelling. No "Teman-teman", "Bayangkan...", "Tahukah kamu?"
- **Each section ends with**: `🎨 *Ilustrasi: [brief description for illustration]*`
- **Illustration brief must include**: Setting, Characters & Pose, Key Objects, Dominant Colors (3-4), Mood, Composition
- **Slide count EN = ID** (must be identical)

## Daftar Pustaka Format
```
## Daftar Pustaka

1. Author, *Title*, details.
2. Author, *Title*, details.
3. Author, *Title*, details.
N. Al-Qur'an al-Karim. QS. [Surah] ([Number]): [Ayat].
```

## Card Data (events-database.json sources)
After writing content, also output a JSON snippet for the event's `sources[]` array:
```json
"sources": [
  {"id": "author-slug", "title": "Book Title", "author": "Author Name", "type": "primary"},
  {"id": "hadith-collection", "title": "Collection Name", "author": "Compiler", "type": "hadith"},
  {"id": "qs-surah", "title": "Al-Quran al-Karim", "author": "QS. Surah Name", "type": "quran"}
]
```

## Quality Self-Check Before Finishing
- [ ] Every ^N in body has matching entry #N in bibliography
- [ ] Every bibliography entry #N is cited at least once in body
- [ ] No duplicate bibliography entries (same source = same number)
- [ ] Min 3 bibliography entries per article
- [ ] Quran separators ﴾N﴿ ONLY in blockquotes (grep non-blockquote lines)
- [ ] Arabic text ONLY for Quran/Hadith, not for names/terms
- [ ] children-id and children-en have SAME number of sections (4)
- [ ] Each children section has illustration brief 🎨
- [ ] No "Teman-teman", "Bayangkan", "Tahukah kamu" in children content
- [ ] EN is faithful translation of ID (not creative rewrite)

## IMPORTANT
- Write ALL 4 files for each event before moving to next
- Use `mkdir -p` to create event folders
- Be historically accurate — use established Islamic historical sources
- Maintain consistent transliteration (e.g., always "Khaththab" not "Khattab")
