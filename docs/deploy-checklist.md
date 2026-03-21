# Deploy QA Checklist — Baitul Hikmah

> Run SEBELUM setiap push ke develop/main.
> Setiap item yang FAIL = JANGAN push sampai fix.

---

## Content Checks

- [ ] **Slide count EN = ID** — parser menghasilkan jumlah slide SAMA di kedua bahasa
  ```bash
  node -e "..." content/events/{event}/children-en.md  # → N slides
  node -e "..." content/events/{event}/children-id.md  # → N slides (harus sama)
  ```
- [ ] **Slide count = Image count** — `EventContent.tsx` length = jumlah file `e{XX}-slide-*.png`
- [ ] **Verse separators Quran only** — `﴾N﴿` HANYA di blockquote (`>`), BUKAN di hadits/dialog
  ```bash
  grep -rn '﴾[0-9]*﴿' */general-*.md | grep -v '^[^:]*:[0-9]*:>'  # harus 0
  ```
- [ ] **No false verse markers** — hadits, dialog, kutipan non-Quran BERSIH dari `﴾N﴿`

## Image Checks

- [ ] **Image size ~1-2MB** per slide (bukan 8-10MB raw Gemini)
- [ ] **Resolution ~1024px** width (match e01/e02 scale)
- [ ] **Character consistency** — Abu Thalib, Bahira, dll sesuai illustration-registry.md
- [ ] **Prophet = golden glow ONLY** — no human figure, no child shape
- [ ] **No text in images** — zero text/labels/captions

## Build Checks

- [ ] **`event-content.json` rebuilt** — `node scripts/build-content.js`
- [ ] **`event-content-map.json` rebuilt** — regenerate from event-content.json
- [ ] **Both JSON files committed** — CF Pages hanya run `next build`, BUKAN build-content.js
- [ ] **`next build` success** — no errors

## Post-Deploy

- [ ] **Verify di dev** — buka halaman event, cek Mode Anak-Anak
- [ ] **Check slide count di browser** — angka di pojok kiri atas = expected
- [ ] **Cek kedua bahasa** — toggle ID/EN, slide count harus sama
- [ ] **Image loads** — semua slide punya gambar, tidak ada broken image
