## Design Decisions Log (2026-03-14/15)

### Theme: Light Mode Only
- **Dark mode dihapus** — website hanya menggunakan light mode
- Tidak ada toggle tema. CSS variables di `:root` = light theme saja
- Map tiles: CARTO `light_all` (bukan dark)

### Bahasa (ID/EN): Custom i18n Context
- Toggle ID/EN di header (pill button, menggantikan dark mode toggle)
- **Implementasi**: Custom React Context (`src/i18n/context.tsx`) + JSON translation files
- **BUKAN `next-intl`** — next-intl di-install tapi TIDAK digunakan. Custom context lebih simpel untuk static export
- Translation files: `src/i18n/id.json` dan `src/i18n/en.json`
- Hero text: ID = "Baitul Hikmah" / EN = "House of Wisdom"
- Subtitle: ID = "Menelusuri Jejak Keemasan Peradaban Islam" / EN = "The Islamic Golden Age and Beyond"
- Header title tetap "Baitul Hikmah" di kedua bahasa
- **Scope i18n**: Semua UI text (hero, filters, labels, buttons, footer, event content, search placeholder, dll)
- **Event content**: Bilingual markdown files (`general-id.md`, `general-en.md`, `children-id.md`, `children-en.md`) — ditampilkan sesuai lang active
- **Default language**: Indonesian (ID)
- **Migrasi ke next-intl**: Nanti jika butuh SEO multi-bahasa (URL-based `/id/...` `/en/...`)

### Children Mode: Slideshow Presentation (bukan artikel)
- **Keputusan**: Mode anak-anak menggunakan format **popup slideshow presentation** — bukan text/artikel biasa
- **Alasan**: Ahmad's feedback dari pengalaman dongeng malam — anak-anak lebih engage dengan gambar besar + teks singkat, bukan scroll artikel panjang
- **Implementasi**:
  - Popup/modal fullscreen dengan slide navigation (swipe/arrows)
  - Setiap slide: ilustrasi gambar dominan + dark overlay di bawah untuk teks (copyable)
  - Per section boleh 2-3 slide (sebelumnya 1 section = 1 view) — lebih fleksibel
  - Total ~8-16 slide per event
- **Impact**: Perlu lebih banyak ilustrasi per event (1 per slide vs 1 hero saja), tapi UX jauh lebih engaging untuk anak-anak
- **Konsekuensi image generation**: ~8-16 gambar per event untuk children mode (vs sebelumnya ~1-3)

### CSS Loading: public/styles.css via `<link>`
- Webpack CSS parsing di Next.js 14 dev mode **tidak reliable** — `@tailwind` directives, maplibre CSS, dll sering error
- **Solusi**: Compile Tailwind CSS terpisah → copy ke `public/styles.css` → load via `<link>` di `<head>` (`layout.tsx`)
- Build workflow: `npx tailwindcss -i src/app/globals.css -o src/app/compiled.css --minify` → `cp src/app/compiled.css public/styles.css` → `npx next build`
- maplibre-gl CSS juga via CDN `<link>` (bukan import)
- Amiri font (Arabic) via Google Fonts CDN `<link>`
- **Dev server** (port 4300) hanya untuk preview layout — bfcache dan CSS tidak reliable di dev mode
- **Testing wajib** di `develop.baitul-hikmah.pages.dev` (Cloudflare Pages deploy)

### State Restore: bfcache (Native Browser)
- **SessionStorage hack dihapus** — browser bfcache natively handles scroll/state restore
- Hanya works di production (static export) — TIDAK di dev mode
- Back navigation dari event detail → homepage: scroll position + filter state restored otomatis

### "Baca Selengkapnya" Button
- Muncul di panel detail event (Timeline mode) dan popup (Map mode)
- **Posisi: rata kiri** (bukan center)
- Link ke halaman `/event/[slug]/`
- **PENTING**: Tampilan dan perilaku harus **konsisten** antara Timeline mode dan Map mode:
  - Style button sama (warna, ukuran, font)
  - Link destination sama (`/event/[slug]/`)
  - Content yang ditampilkan di halaman event sama regardless of entry point

---


## 15. Content Standards & Writing Guidelines 🚀

> **📄 Dipindahkan ke dokumen terpisah untuk efisiensi token.**
> Baca: [`docs/content-style-guide.md`](docs/content-style-guide.md)
>
> Berisi: format Quran/Hadits, sitasi & daftar pustaka, teks Arab, diksi, struktur artikel, QC checklist, ID↔EN sync rules.
>
> **⚠️ CRITICAL RULES (2026-03-20):**
>
> **1. Pemisah Ayat Al-Quran:**
> - Terjemahan (LTR) WAJIB pakai `﴾N﴿` (bracket terbalik, angka Western) di akhir setiap ayat
> - Teks Arab (RTL) tetap pakai `﴿N﴾` (Arabic numerals)
> - Lihat `content-style-guide.md` Section 1 untuk format lengkap
>
> **2. Bilingual Sync**: Edit konten EN WAJIB diikuti edit ID (dan sebaliknya). Slide count harus sama. Lihat `content-style-guide.md` section "Bilingual Sync Rule".
>
> **3. HANYA untuk Ayat Al-Quran — BUKAN Hadits/Dialog:**
> - Pemisah ayat `﴾N﴿` **HANYA** boleh muncul di dalam blockquote (`>`) yang berisi ayat Al-Quran
> - **DILARANG** menambahkan pemisah ayat ke: hadits, dialog historis, kutipan sahabat, narasi, atau teks non-Quran apapun
> - **Lesson learned**: Sub-agent pernah salah menambahkan `﴾N﴿` ke 40+ hadits/dialog (2026-03-20) — harus di-review manual setelah batch edit
> - **Rule of thumb**: Jika kutipan diawali `HR.` / `Bukhari` / `Muslim` / nama perawi → BUKAN ayat Quran → JANGAN tambah pemisah
>
> **⚠️ Ketentuan kritis:**
> - **Pemisah ayat `﴿N﴾` WAJIB** di teks Arab DAN terjemahan — lihat Section 1 content-style-guide.md
> - Teks Arab: `﴿١﴾ ﴿٢﴾` (Arabic numerals). Terjemahan: `﴿6﴾ ﴿7﴾` (angka Latin)
> - Berlaku untuk kutipan 1 ayat maupun multi-ayat
> - File tanpa pemisah ayat di terjemahan = **REJECT** di QA

---

## 16. Children Slideshow — Illustration Guidelines 🚀

> **📄 Dipindahkan ke dokumen terpisah untuk efisiensi token.**
> Baca: [`docs/illustration-guide.md`](docs/illustration-guide.md)
>
> Berisi: larangan visualisasi Nabi ﷺ, no text in image, safe zone, brief format, end-to-end pipeline, QA checklist, lessons learned.
>
> **📚 Related Illustration Documents:**
> - [`docs/illustration-registry.md`](docs/illustration-registry.md) — Character descriptions, genre palettes, time-of-day palettes, cinematic shot types, prompt assembly template. **BACA PERTAMA sebelum generate.**
> - [`docs/briefs/ (per-episode)`](docs/briefs/ (per-episode)) — Prompt per slide per event (E01-E04 ready, lainnya TBD)
> - [`docs/design-guide.md`](docs/design-guide.md) — Color system & moodboard per era
>
> **⚠️ Palette Consistency Rule (2026-03-22):**
> Setiap event WAJIB punya **base palette header** di image briefs — 3-4 warna utama yang konsisten di SEMUA slides.
> Variasi ringan per slide diperbolehkan (indoor vs outdoor, siang vs malam), tapi base tones harus sama.
> Lihat E04 di `briefs/ (per-episode)` sebagai contoh format yang benar.

---

**Wallahu A'lam** — Dokumen ini hidup dan akan diperbarui seiring perkembangan project.

> رَبِّ زِدْنِي عِلْمًا
> "Rabbi zidni 'ilma" — "Ya Tuhanku, tambahkanlah ilmu kepadaku." (QS. Taha: 114)

> Archived from PRD.md.
