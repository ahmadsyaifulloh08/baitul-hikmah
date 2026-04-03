# PRD: Baitul Hikmah — Website Peradaban Islam

**Domain**: baitul-hikmah.id
**Owner**: Ahmad Syaifulloh
**Date**: 2026-03-14
**Status**: Draft — Pending Approval
**Version**: 1.0

---

## 1. Visi & Misi 🚀

### Visi
Menjadi portal digital terlengkap dan terindah untuk menelusuri sejarah peradaban Islam — dari Tahun Gajah (570 M) hingga jatuhnya Al-Andalus (1492 M) — dengan pendekatan riset ilmiah (Manhaj Bukhari) dan penyajian visual yang imersif.

### Misi
1. Menyajikan kisah peradaban Islam yang **sahih** (tervalidasi sumber) dan **kontekstual** (historis, geografis, intelektual)
2. Menjangkau **dua segmentasi**: pembaca dewasa (detail & akademis) dan anak-anak (visual & inspiratif)
3. Memvisualisasikan timeline sejarah Islam melalui **peta interaktif** dan **animasi timeline** yang imersif
4. Menghidupkan kembali semangat Baitul Hikmah — pusat ilmu pengetahuan — di era digital

### Tagline
> "Menelusuri Jejak Peradaban Islam — dari Gua Hira hingga Baitul Hikmah"

### Bahasa
- **Bahasa Indonesia** — bahasa utama (default)
- **English** — bahasa kedua (full translation)
- Implementasi: i18n routing (`/id/...` dan `/en/...`) atau language switcher
- Konten riset ditulis dalam kedua bahasa (Researcher output bilingual)
- UI labels, navigation, metadata — bilingual dari Fase 1

---

## 2. Target Audiens 🚀

### Segmen A: General (Default)
- **Profil**: Muslim dewasa, mahasiswa, peneliti, educator, pencari pengetahuan
- **Kebutuhan**: Narasi detail, konteks historis mendalam, sumber rujukan lengkap (daftar pustaka)
- **Tone**: Akademis tapi accessible, serius tapi engaging
- **Konten wajib per artikel**:
  - Konteks historis & geografis
  - Narasi detail peristiwa
  - Analisis signifikansi
  - Dalil Al-Qur'an & Hadits yang relevan (lihat **Hierarki Kutipan Al-Quran** di `content-style-guide.md` — prioritaskan ayat dengan korelasi asbabun nuzul/historis langsung, hindari ayat "tempelan" generik)
  - Daftar pustaka (minimal: sumber primer + kitab rujukan)

### Segmen B: Anak-Anak (Mode Anak-Anak)
- **Profil**: Anak usia 6-12 tahun (dibacakan orang tua)
- **Kebutuhan**: Visual menarik, informasi ringkas tapi akurat, mudah dipahami anak
- **Tone**: Informatif-ringan — fokus menyampaikan INFORMASI yang dirangkum untuk anak. BUKAN gaya mendongeng ("Teman-teman, bayangkan..."). Biarkan orang tua dengan ekspresi masing-masing yang menarasikan.
- **⚠️ YANG DILARANG dalam gaya penulisan:**
  - ❌ Sapaan langsung ke pembaca: "Teman-teman", "Friends", "Tahukah kamu?"
  - ❌ Ajakan berimajinasi: "Bayangkan...", "Coba pikirkan..."
  - ❌ Nada presenter/pendongeng: "Nah, sekarang kita lihat...", "Dan begitulah..."
  - ❌ Exclamation berlebihan: "Wow!", "Luar biasa!", "Subhanallah!" (boleh 1x di penutup)
- **✅ YANG BENAR:**
  - Langsung ke informasi: "Pada tahun 570 M, di Yaman ada seorang raja bernama Abrahah."
  - Kronologis dan faktual: "Abu Thalib membawa Muhammad ke Syam untuk berdagang."
  - Kalimat pendek, jelas, tidak bertele-tele
  - Konteks lengkap tapi diringkas — jangan skip informasi penting demi "lucu"
- **Format konten adaptif** — menyesuaikan jenis event:

  **Jika event = Tokoh/Figure:**
  1. 🧑 **"Siapa dia?"** — Perkenalan tokoh (sederhana, relatable)
  2. ⭐ **"Apa yang beliau lakukan?"** — Karya/kontribusi utama
  3. 💡 **"Kenapa beliau luar biasa?"** — Motivasi & karakter
  4. 📖 **"Allah berfirman..."** — Korelasi Al-Qur'an/Hadits

  **Jika event = Peristiwa/Kejadian:**
  1. 🌍 **"Apa yang terjadi?"** — Setting waktu & tempat, sederhana
  2. 📖 **"Ceritanya..."** — Narasi kronologis, bahasa dongeng
  3. 🌟 **"Pelajarannya..."** — Hikmah & motivasi yang bisa dipetik
  4. 🤲 **"Doa & Dalil"** — Ayat/Hadits yang relevan

  **Jika event = Peradaban/Ilmu Pengetahuan:**
  1. 🏛 **"Tahukah kamu?"** — Fun fact pembuka
  2. 🔬 **"Apa itu?"** — Penjelasan sederhana (sains/karya/institusi)
  3. 🌍 **"Dampaknya sampai sekarang!"** — Relevansi modern
  4. 📖 **"Islam & Ilmu"** — Dalil tentang menuntut ilmu

  **Jika event = Perang/Konflik:**
  1. ⚔️ **"Kenapa ini terjadi?"** — Latar belakang (tanpa glorifikasi kekerasan)
  2. 🛡 **"Bagaimana ceritanya?"** — Narasi fokus strategi & keberanian
  3. 🕊 **"Setelahnya..."** — Dampak & perdamaian
  4. 💪 **"Nilai yang bisa kita teladani"** — Keberanian, keadilan, sabar

- **Format presentasi**: **Slideshow popup** (bukan text/artikel biasa) — seperti presentasi Google Slides
  - **Ilustrasi gambar dominan** di setiap slide (visual-first)
  - **Overlay warna gelap di bagian bawah** slide untuk tempat tulisan (teks tetap bisa di-copy/select)
  - **Per section boleh 2-3 slide** sesuai konteks (bukan 1 section = 1 view)
  - Format singkat, visual-first — anak-anak engage lewat gambar, bukan teks panjang
  - Navigasi: swipe/arrow antar slide, progress indicator dots
- **Referensi visual**: Canva presentation style — kali ini memang bentuk **slideshow presentation** (bukan hanya inspirasi layout)
- **Prinsip visual anak-anak**: Ilustrasi gambar per slide (generated), dengan text overlay di dark overlay bawah. Moodboard konsisten per era, adjustment tema per kisah.

---

## 3. Sitemap & Fitur

### 3.1 Halaman Utama — Timeline Mode 🚀

**URL**: `baitul-hikmah.id/`

Tampilan utama berupa **timeline grid** — mirip format di `agents.ahadbyte.id/governance?tab=research`.

**Layout:**
- **Grid columns**: Kolom pertama = Tahun | Kolom sisanya = Region (Arabia, Levant/Sham, Persia/Iraq, Egypt/N.Africa, Al-Andalus, Central Asia, India/SE Asia, Nusantara, China)
- **Era bands**: Background stripes horizontal per era, dengan label era di sisi kiri
- **Event dots/nodes**: Diposisikan di kolom region yang sesuai, pada posisi vertikal sesuai tahun
- **Sticky header**: Row header region tetap visible saat scroll
- **Click event** → navigasi ke halaman detail `/event/[slug]`

**Referensi visual**: Persis seperti tab Research di `agents.ahadbyte.id/governance?tab=research`

**Filter (multi-select):**
- Category filter buttons: Kenabian ☆ | Politik ♛ | Ilmu Pengetahuan ≡ | Militer ⚔ | Peradaban ◆ | Kemunduran ↓
- Bisa **select multiple** categories sekaligus (toggle on/off per category)
- Search bar: cari by tokoh, peristiwa, tahun
- Color-coded per category

**Mobile**: Collapsible era sections (accordion) — klik era → expand daftar events

**Data source**: `events-database.json` (128 events, sudah terstruktur)

### 3.2 Halaman Utama — Map Mode (GIS Interaktif) 🚀

**URL**: `baitul-hikmah.id/map`

Peta dunia interaktif ala WebGIS yang menampilkan events berdasarkan lokasi geografis + timeline.

**Referensi visual**: YouTube video — animated historical map style

**Fitur:**
- **Peta dunia** dengan region peradaban Islam (Arabia, Sham, Persia, Mesir, Al-Andalus, dll)
- **Timeline slider** di bawah peta — geser tahun, peta berubah
- **Marker/pin** di setiap lokasi event — klik untuk preview
- **Nama lokasi historis** yang menyesuaikan era/timeline:
  - Sebelum 750 M: "Persia", "Sham", "Habasyah"
  - Setelah 750 M: tetap nama historis, dengan tooltip nama modern
  - Contoh: "Sham (kini Suriah/Levant)", "Persia (kini Iran/Iraq)"
- **Animated transitions** saat scroll timeline — peta zoom/pan ke region yang relevan
- **Region highlighting** — area kekuasaan Islam yang berubah per era
- **Cluster events** jika banyak event di satu lokasi
- **Mini timeline bar** menunjukkan era aktif

**Akurasi Koordinat (CRITICAL):**
- Setiap event WAJIB memiliki koordinat GPS yang akurat berdasarkan lokasi historis sebenarnya
- Koordinat disimpan di `src/data/event-coordinates.json` sebagai `[longitude, latitude]` (GeoJSON standard)
- TIDAK BOLEH menggunakan jitter/random dari region center — harus riset per event
- Contoh akurasi:
  - "Kelahiran Nabi Muhammad SAW" → Ka'bah, Makkah: [39.8262, 21.4225]
  - "Kerajaan Samudera Pasai" → Aceh Utara: [97.07, 5.22]
  - "Penaklukan Konstantinopel" → Istanbul: [28.9784, 41.0082]
- Untuk event perjalanan (hijrah, ekspedisi): gunakan koordinat TUJUAN
- Untuk perang: gunakan lokasi pertempuran
- Koordinat di-maintain oleh Researcher agent, divalidasi via web search
- `map-data.ts` membaca dari `event-coordinates.json`, fallback ke region center jika belum ada

**Multi-select Filters:**
- Semua filter (Era, Kategori, Wilayah) mendukung multi-select (toggle on/off)
- Style filter di Map mode HARUS konsisten dengan Timeline mode
- Wilayah filter: klik → peta fly-to region tersebut
- Year slider: warna mengikuti light theme

**Theme:**
- **Light mode only** — tidak ada dark mode toggle
- Map tiles: CARTO `light_all` saja (basemaps.cartocdn.com/light_all)
- Legend, badge, dan overlay menggunakan `var(--bg-primary)` solid (bukan transparan)

**Tech considerations:**
- Map library: **MapLibre GL JS** (open source)
- Tiles: **CARTO** raster basemaps (`light_all` only) — no self-hosted tiles needed
- Animasi: CSS transitions + MapLibre flyTo untuk smooth region panning

### 3.3 Halaman Detail Event 🚀

**URL**: `baitul-hikmah.id/event/{event-id}` (contoh: `/event/tahun-gajah`)

Halaman penjelasan lengkap per peristiwa. Default mode: **General**. Ada toggle ke mode **Anak-Anak**.

#### Mode General (Default)
- **Header badges (1 baris)**: Era + Kategori + Wilayah + Signifikansi + Tahun — semua di satu baris sebagai badges/pills
  - Contoh: `Pra-Islam (Jahiliyyah)` `☆ Kenabian` `Arabia` `★ Sangat Penting` `570 M`
- **Tokoh**: Di bawah judul, sebelum mode toggle — label "Tokoh:" + pills kecil (fontSize 12, borderRadius 12, bg secondary)
  - Include tokoh utama DAN pendukung (contoh e01: + Abrahah, Halimah)
  - Contoh: `Tokoh: [Nabi Muhammad SAW] [Abdul Muthalib] [Abrahah] [Halimah al-Sa'diyyah]`
- **Judul `<h1>`**: Ditampilkan di bawah badges, sebelum tokoh. Markdown `# Judul` di content file di-skip oleh renderer (mencegah duplikasi)
- **Konsistensi styling**: Badges di halaman detail HARUS sama dengan filter pills di homepage — `fontSize: 11, padding: 3px 10px, borderRadius: 14`, warna era/kategori/wilayah filled (background), signifikansi amber, tahun outlined

**Hierarki layout halaman detail:**
```
← Kembali ke Timeline
[Era] [Kategori] [Wilayah] [Signifikansi] [Tahun M]     ← badges (fontSize 11)
Judul Event                                                ← h1 (text-2xl/3xl, bold)
Tokoh: [Nama1] [Nama2] [Nama3] ...                       ← pills (fontSize 12, bg secondary)
[🌙 Mode Anak-Anak]                                       ← toggle button
── artikel dimulai ──                                      ← ## Sub-heading pertama
```
- **Hero visual**: Ilustrasi/artwork event (generated atau curated)
- **Narasi lengkap**: Konteks → kronologi → analisis → signifikansi
- **Tokoh terkait**: Card per tokoh (nama, peran, tahun hidup)
- **Peta mini**: Lokasi event di peta
- **Dalil terkait**: Ayat Al-Qur'an dan/atau Hadits yang relevan (dengan teks Arab, transliterasi, terjemahan). **WAJIB** mengikuti Hierarki Kutipan (Tier 1: asbabun nuzul/historis → Tier 2: tematik kuat → Tier 3: HINDARI). Event tanpa Tier 1/2 boleh tanpa ayat. Lihat `content-style-guide.md`.
- **Daftar Pustaka**: Sumber rujukan dari markdown content (BUKAN dari JSON `event.sources` jika rich content tersedia)
- **Navigasi**: Previous/Next event secara kronologis
- **Related events**: Events terkait di era/region yang sama

#### Mode Anak-Anak (Toggle) — Slideshow Presentation
- **Trigger**: Button/toggle animasi "Mode Dongeng 🌙"
- **Format**: **Popup slideshow presentation** (fullscreen/modal) — bukan halaman artikel biasa
  - Muncul sebagai overlay/popup di atas halaman event
  - Setiap slide: **ilustrasi gambar dominan** (hampir full-slide)
  - **Overlay gelap (dark gradient) di bagian bawah** slide → tempat teks narasi
  - Teks di overlay tetap **selectable & copyable**
  - **Per section 2-3 slide** sesuai konteks (misal "Siapa dia?" bisa 2 slide, "Apa yang beliau lakukan?" bisa 3 slide)
  - **Minimum 6 slide per event** — agar anak-anak mendapat konteks yang cukup mendalam
  - Total per event: ~6-16 slide (standar: 6-7 slide, event besar bisa lebih)
- **Navigasi slide**: Arrow buttons (kiri/kanan), swipe gesture (mobile), keyboard arrows
- **Progress indicator**: Dots atau progress bar di bawah slide
- **Format storytelling**: Adaptif berdasarkan jenis event (lihat Section 2 — Format konten adaptif)
- **Gaya bahasa**: Seperti bercerita (naratif), bukan menjelaskan (eksplanatif) — singkat per slide
- **Font**: Lebih besar, lebih rounded — readable di atas dark overlay
- **Ilustrasi**: 1 gambar per slide (generated via Gemini nanobanana), style anak-anak (bright, rounded, Pixar-meets-Islamic-art)
- **Close**: Tombol close (X) untuk kembali ke halaman event dewasa
- **Audio** (future): Option baca cerita (TTS dengan suara warm) — auto-advance slide per narasi

### 3.4 Halaman Tentang 🚀

**URL**: `baitul-hikmah.id/about`

- Visi & misi project
- Metodologi riset (Manhaj Bukhari → Elaborasi)
- Tim (Ahmad + AI Research Partner)
- Sumber data & referensi utama

### 3.5 Halaman Metodologi ⬜

**URL**: `baitul-hikmah.id/methodology`

- Penjelasan detail 3 tahap riset:
  1. Prinsip Imam Bukhari (validasi sumber)
  2. Elaborasi Al-Ghazali, Ibn Rushd, Ibn Taimiyah
  3. Standar dokumentasi akademis
- Transparency: bagaimana setiap artikel divalidasi

---

## 4. Konten — Fase Pertama

### Event Pertama: Tahun Gajah / Kelahiran Nabi Muhammad SAW (570 M)

Riset dan penulisan dimulai dari event `e01` — peristiwa paling awal dalam timeline.

**Scope riset (Manhaj Bukhari)**:
- Sumber primer: Sirah Nabawiyyah (Ibn Hisham), Al-Rahiq al-Makhtum, Tafsir Ibn Kathir (Surah Al-Fil)
- Cross-reference: Shahih Bukhari, Shahih Muslim, Tabaqat al-Kubra (Ibn Sa'd)
- Konteks: Kondisi Jazirah Arab pra-Islam, latar belakang Abrahah, signifikansi Ka'bah

**Output**:
1. Artikel dewasa (2000-3000 kata) + daftar pustaka
2. Konten anak-anak (4 section storytelling) + brief ilustrasi

### Roadmap Konten (Sequential)
| # | Event | Tahun | Prioritas |
|---|-------|-------|-----------|
| 1 | Tahun Gajah / Kelahiran Nabi | 570 M | 🔴 Pertama |
| 2 | Yatim piatu — wafat ayah, ibu, kakek | 576-578 M | Ke-2 |
| 3 | Perjalanan ke Syam & Pendeta Bahira | 583 M | Ke-3 |
| 4 | Pernikahan dengan Khadijah | 595 M | Ke-4 |
| 5 | Renovasi Ka'bah & Hajar Aswad | 605 M | Ke-5 |
| ... | (sequential per timeline) | ... | ... |

---

## 5. Design & Frontend 🚀

### Design System
- **Referensi utama**: [21st.dev](https://21st.dev) — modern, clean, component-driven UI
- **Framework**: Next.js 14+ (App Router) + Tailwind CSS + Framer Motion
- **Typography**: Serif untuk heading (nuansa klasik/Islamic), Sans-serif untuk body
- **Color palette**: Berdasarkan era colors di `events-database.json`:
  - Pra-Islam: `#8b949e` (muted gray)
  - Kenabian: `#3fb950` (vibrant green)
  - Rashidin: `#58a6ff` (calm blue)
  - Umayyah: `#d29922` (golden)
  - Abbasiyah: `#bc8cff` (royal purple)
  - Fragmentasi: `#f778ba` (rose)
  - Kemunduran: `#da3633` (deep red)

### Moodboard & Ilustrasi
- **Style**: Semi-realistic Islamic art — blend antara kaligrafi, geometric patterns, dan modern illustration
- **Konsistensi**: Satu moodboard per era, adjustment warna/tone per kisah
- **Children mode**: Lebih bright, karakter lebih friendly/rounded (mirip style buku cerita anak Islami)
- **Tool**: Gemini image generation (Ahmad provide model `nanobanana`)
- **Per event**: 1 hero image + 1-3 supporting illustrations

### Responsive Design
- **Desktop**: Full experience (map mode, timeline, side panels)
- **Tablet**: Adapted layout (stacked timeline, simplified map)
- **Mobile**: Timeline-first, bottom sheet untuk detail, swipe navigation
- **PWA (Progressive Web App)**: Install ke homescreen, offline reading (cached articles), push notifications (future)

### Animations & Interactions
- **Page transitions**: Smooth, purposeful (Framer Motion)
- **Timeline scrub**: Parallax effect, era indicators
- **Map mode**: Zoom/pan animations synced with timeline
- **Mode switch** (General ↔ Anak): Animated transition (color shift, layout morph)
- **Scroll-driven**: Content reveals as user scrolls through timeline

---

## 6. Open Source Resource Catalog

Seluruh resource di bawah ini **free & open source** (atau free tier cukup), dipilih untuk meminimalkan cost dan memaksimalkan kualitas.

### 🎨 UI Component Libraries

| Resource | URL | Kegunaan | License |
|----------|-----|----------|---------|
| **shadcn/ui** | [ui.shadcn.com](https://ui.shadcn.com) | Base component library (Button, Card, Dialog, Sheet, Tabs, dll) | MIT |
| **Magic UI** | [magicui.design](https://magicui.design) | 150+ animated components — timeline, scroll animations, text effects, number tickers | MIT |
| **Aceternity UI** | [aceternity.com/components](https://aceternity.com/components) | Parallax scroll, spotlight cards, text reveal, hero sections — cocok untuk landing page | MIT |
| **21st.dev** | [21st.dev](https://21st.dev) | UI building blocks & templates — referensi design patterns | Open |

### 🖼 SVG & Illustrations

| Resource | URL | Kegunaan | License |
|----------|-----|----------|---------|
| **unDraw** | [undraw.co](https://undraw.co) | SVG illustrations customizable warna — untuk section headers, empty states | Free, no attribution |
| **Storyset** | [storyset.com](https://storyset.com) | Animated SVG illustrations, customizable layers & colors | Free with attribution |
| **Heroicons** | [heroicons.com](https://heroicons.com) | SVG icons by Tailwind team — general UI icons | MIT |
| **Lucide** | [lucide.dev](https://lucide.dev) | 1500+ SVG icons, React-ready — replacement for Feather icons | ISC |
| **Hugeicons** | [hugeicons.com](https://hugeicons.com) | 4000+ SVG icons, multiple styles — jika butuh variasi lebih | Free tier + MIT core |

### 🗺 Map & GIS

| Resource | URL | Kegunaan | License |
|----------|-----|----------|---------|
| **MapLibre GL JS** | [github.com/maplibre/maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js) | Interactive vector tile map — **core map engine** | BSD-3 |
| **Protomaps** | [protomaps.com](https://protomaps.com) | Self-hosted map tiles (single PMTiles file, no server) — deploy ke Cloudflare R2 | BSD-3 |
| **Natural Earth** | [naturalearthdata.com](https://naturalearthdata.com) | Public domain map data (borders, rivers, terrain) — base cartography | Public domain |
| **OpenStreetMap** | [openstreetmap.org](https://openstreetmap.org) | Modern geographic data — untuk overlay modern names | ODbL |
| **GeoJSON.io** | [geojson.io](https://geojson.io) | Tool untuk buat/edit custom GeoJSON — historical borders per era | Open |

### ⏳ Timeline

| Resource | URL | Kegunaan | License |
|----------|-----|----------|---------|
| **TimelineJS3** | [timeline.knightlab.com](https://timeline.knightlab.com) | Storytelling timeline — referensi UX, bisa embed atau fork | MPL-2.0 |
| **GSAP ScrollTrigger** | [gsap.com](https://gsap.com) | Scroll-driven timeline animations — parallax, pinning, scrubbing | Free for non-commercial (kita free site ✅) |
| **Framer Motion** | [motion.dev](https://motion.dev) | React animation library — layout animations, gestures, transitions | MIT |

### ✨ Animation

| Resource | URL | Kegunaan | License |
|----------|-----|----------|---------|
| **Lottie Web** | [github.com/airbnb/lottie-web](https://github.com/airbnb/lottie-web) | Render After Effects JSON animations di web — untuk micro-animations | MIT |
| **LottieFiles** | [lottiefiles.com](https://lottiefiles.com) | Library animasi Lottie gratis — loading, transitions, decorative | Free tier |
| **Rive** | [rive.app](https://rive.app) | Interactive state-machine animations — untuk mode anak-anak | Free tier |
| **CSS.gg** | [css.gg](https://css.gg) | Pure CSS icons & animations — zero JS, ultra lightweight | MIT |

### 🔤 Typography & Arabic

| Resource | URL | Kegunaan | License |
|----------|-----|----------|---------|
| **Amiri** | [Google Fonts](https://fonts.google.com/specimen/Amiri) | Arabic serif font — untuk teks Qur'an & Hadits | OFL |
| **Scheherazade New** | [Google Fonts](https://fonts.google.com/specimen/Scheherazade+New) | Arabic font, clarity at small sizes | OFL |
| **Noto Sans Arabic** | [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+Arabic) | Sans-serif Arabic — untuk UI text | OFL |
| **Inter** | [Google Fonts](https://fonts.google.com/specimen/Inter) | UI font Latin — body text | OFL |
| **Playfair Display** | [Google Fonts](https://fonts.google.com/specimen/Playfair+Display) | Serif heading — nuansa klasik | OFL |

### 🕌 Islamic / Arabic / Middle Eastern Themed Assets

| Resource | URL | Kegunaan | License |
|----------|-----|----------|---------|
| **TiledPatternMaker** | [github.com/ChortleMortal/TiledPatternMaker](https://github.com/ChortleMortal/TiledPatternMaker) | Generate geometric Islamic/Andalusian tile patterns — untuk backgrounds & dividers | GPL |
| **Hero Patterns** | [heropatterns.com](https://heropatterns.com) | Repeatable SVG background patterns — beberapa cocok untuk geometric Islamic feel | Free |
| **Patternico** | [patternico.com](https://patternico.com) | Seamless pattern maker — buat custom Islamic-themed backgrounds | Free |
| **Flaticon** (Islamic pack) | [flaticon.com](https://flaticon.com) — search "islamic", "mosque", "arabic" | SVG icons: mosque, crescent, lantern, scroll, sword, book, minaret | Free with attribution |
| **Storyset** (Arabic theme) | [storyset.com](https://storyset.com) — filter "cuate" or "bro" style | Animated SVG scenes — caravans, desert, markets | Free with attribution |

### 📖 Quran & Hadith Data Sources

**Strategi: Hybrid** — self-hosted primary + API enrichment

| Resource | URL | Role | Kegunaan | License |
|----------|-----|------|----------|---------|
| **quran-database** ⭐ | [github.com/AbdullahGhanem/quran-database](https://github.com/AbdullahGhanem/quran-database) | **Primary** | MySQL dump 187MB — full Quran + multi-translation + editions. Extract ke JSON untuk static build. Offline, no rate limit, no API dependency. | Open source |
| **Quran.com API v4** | [api-docs.quran.com](https://api-docs.quran.com) | **Enrichment** | Tafsir (Ibn Kathir, dll), audio recitation, word-by-word — satu-satunya yang punya tafsir | Free |
| **AlQuran Cloud API** | [alquran.cloud/api](https://alquran.cloud/api) | **Fallback/verify** | Simple REST, 100+ editions — cross-check terjemahan | Free, no key |
| **Sunnah.com API** | [sunnah.com](https://sunnah.com) | **Hadith** | Hadits Bukhari, Muslim, dll — search by keyword/reference | Free |

**Build-time pipeline:**
1. Import `quran-database` → SQLite atau JSON (per surah/ayat)
2. Enrich dengan tafsir dari Quran.com API (cache locally)
3. Static JSON files di `/data/quran/` — consumed at build time oleh Next.js
4. Hasil: **zero runtime API calls** untuk ayat Qur'an → fast, offline-capable

### 🖼 Image Generation (fallback — untuk Hero Images saja)

> **Strategi Fase 1**: Prioritaskan **SVG + CSS illustrations** (lebih ringan, scalable). Image generation hanya untuk hero artwork yang tidak bisa di-SVG-kan.

| Resource | URL | Kegunaan | License |
|----------|-----|----------|---------|
| **Gemini (nanobanana)** | Ahmad provide | Generate hero illustrations per event — consistent moodboard | Perlu akses |
| **Stable Diffusion XL** | Open source | Fallback jika perlu generate lokal | Open |

### 📦 Development Tools

| Resource | URL | Kegunaan | License |
|----------|-----|----------|---------|
| **Next.js 14+** | [nextjs.org](https://nextjs.org) | React framework, SSG/SSR, App Router | MIT |
| **Tailwind CSS** | [tailwindcss.com](https://tailwindcss.com) | Utility-first CSS | MIT |
| ~~MDX~~ | ~~mdxjs.com~~ | ~~Tidak digunakan — konten pakai plain markdown~~ | — |
| ~~ContentLayer~~ | ~~contentlayer.dev~~ | ~~Tidak digunakan — konten loaded via JSON~~ | — |
| **Cloudflare Pages** | [pages.cloudflare.com](https://pages.cloudflare.com) | Static site hosting, edge-deployed | Free tier |

---

## 7. Multi-Agent Development Model 🚀

### Agent Assignment

Project ini dikerjakan secara **multi-agent**, sesuai prinsip "Avengers, not Superman!".

| Role | Agent | Soul | Tanggung Jawab |
|------|-------|------|----------------|
| **Project Lead & Orchestrator** | Main (Byte) | Abu Bakar As-Siddiq | Koordinasi semua agent, review PRD, komunikasi dengan Ahmad |
| **Researcher** | Researcher (Ali) | Ali bin Abi Thalib | Riset konten per event — Manhaj Bukhari, validasi sumber, penulisan narasi dewasa & anak-anak |
| **Frontend Engineer** | Engineer | Al-Khwarizmi | Development web — Next.js, components, map integration, animations |
| **QA Tester** | Quality Assurance | Al-Biruni | Testing di `develop.baitul-hikmah.pages.dev`, cross-browser, mobile, content accuracy check |
| **Product Manager** | Product Manager | Ibn al-Haytham | Maintain PRD, prioritize backlog, acceptance criteria |
| **Document Designer** | Document Designer | Ibn Muqla | Moodboard, style guide, visual consistency per era, illustration briefs |
| **Data Analyst** | Data Analyst | Mirzo Ulugbek | Data structuring, GeoJSON preparation, historical coordinates mapping |

### Workflow per Event (Content Pipeline)

```
Ahmad approve event → Researcher riset (Manhaj Bukhari)
                          ↓
                    Draft konten (dewasa + anak-anak)
                          ↓
              Document Designer → illustration brief (format Section 15.5) + moodboard check
                          ↓
              Engineer → implement di web (markdown + components)
                          ↓
              QA → test di develop.baitul-hikmah.pages.dev
                          ↓
              Ahmad review → approve → merge to main → production
```

### Workflow Web Development (Feature Pipeline)

```
Product Manager → define feature + acceptance criteria
                          ↓
              Data Analyst → prepare data (GeoJSON, coordinates, etc.)
                          ↓
              Engineer → develop feature (branch → PR)
                          ↓
              QA → test di develop.baitul-hikmah.pages.dev
                          ↓
              Ahmad approve → merge → production
```

### Content File Structure per Event

```
/workspace/docs/content/events/e{NN}-{slug}/
├── general-id.md          # General — Bahasa Indonesia
├── general-en.md          # General — English
├── children-id.md       # Anak-anak — Bahasa Indonesia (with 🎨 Brief Ilustrasi per section)
└── children-en.md       # Anak-anak — English (with 🎨 Illustration Brief per section)
```

- Naming: `e01`, `e02`, ... (sequential per timeline)
- Slug: kebab-case dari nama event (e.g. `tahun-gajah`, `yatim-piatu`)
- Children files WAJIB include illustration brief per Section 15.5
- All files plain markdown (bukan MDX)

### Content Authoring Guide — Checklist per File

Setiap file konten HARUS memenuhi checklist berikut sebelum dianggap "siap deploy".

#### `general-id.md` / `general-en.md` (General)

**Frontmatter (wajib):**
```yaml
---
title: "Judul lengkap event"
date: "570 M"
era: "Pra-Islam"
location: "Makkah, Jazirah Arab"
tags: ["tag1", "tag2"]
sources: ["ibn-hisham", "rahiq-makhtum", ...]
---
```

**Body checklist:**
- [ ] **Judul `# ...`**: Tetap tulis di markdown (untuk metadata/referensi) tapi TIDAK di-render di web — renderer skip h1. Artikel langsung dimulai dari `## Sub-heading pertama`
- [ ] **Struktur minimal**: Pembuka konteks → Narasi kronologis → Analisis/signifikansi → Penutup → Daftar Pustaka
- [ ] **Sitasi (BLOCKER)**: Setiap klaim faktual ada angka superscript (`¹²³` atau `^1`) — sequential, linked ke daftar pustaka. **BIJECTION WAJIB**: setiap ^N punya entry #N, setiap entry #N punya ^N di body. Tidak ada orphan di kedua sisi. **Setiap paragraf historis minimal 1 sitasi.**
- [ ] **Daftar Pustaka (BLOCKER)**: Minimal 3 entries UNIK (consolidated). DILARANG: duplikat sumber, footnote-style. Detail bab/halaman di inline text saja. Sumber sama = nomor SAMA (reuse, bukan entry baru). Tidak ada batas maks asalkan semua tersitasi.
- [ ] **Self-Check Sitasi (BLOCKER)**: Sebelum submit, penulis WAJIB verify: (1) minimal 3 entries consolidated, (2) setiap #N ada ^N di body, (3) setiap ^N ada entry #N, (4) tidak ada duplikat sumber, (5) tidak ada ^0.
- [ ] **Teks Arab**: HANYA untuk Quran dan Hadits — BUKAN untuk istilah/nama/tempat/kitab (Section 15.7)
- [ ] **Ayat Al-Quran**: Teks Arab lengkap + nomor ayat ﴿N﴾ di atas terjemahan (Section 15.1, 15.7)
- [ ] **Hadits**: Sertakan nomor hadits + kitab/bab — bukan hanya "(HR Muslim)" (Section 15.3)
- [ ] **Diksi**: Sesuai panduan (Section 15.8) — tidak ada kata bisnis/tech yang menyalahi konteks
- [ ] **Tidak ada raw markdown artifacts**: Tidak ada `>`, `*`, `|` yang tidak ter-render

#### `children-id.md` / `children-en.md` (Anak-anak)

**Frontmatter (wajib):**
```yaml
---
title: "Judul cerita anak"
date: "570 M"
era: "Pra-Islam"
audience: "children"
ageRange: "6-12"
language: "id"     # atau "en"
sections: 4        # jumlah bagian
---
```

**Body checklist:**
- [ ] **4 bagian/sections** mengikuti format adaptif berdasarkan jenis event (Section 2)
- [ ] **Tone dongeng**: Naratif, bukan eksplanatif. Bahasa sederhana untuk usia 6-12
- [ ] **Emoji**: Setiap section punya emoji representatif
- [ ] **Brief ilustrasi**: Setiap section diakhiri dengan `🎨 Brief Ilustrasi` / `🎨 Illustration Brief` yang memenuhi 6 elemen wajib (Section 15.5)
- [ ] **Ayat Al-Quran**: Jika ada, sertakan teks Arab + terjemahan (boleh tanpa transliterasi untuk versi anak)
- [ ] **Tidak ada tabel**: Gunakan list/visual cards (Section 15.2)
- [ ] **Penutup**: Pelajaran/hikmah dalam bentuk list pendek

### Content Deploy Pipeline — Draft → Web

Alur lengkap dari draft konten sampai tampil di website:

```
STEP 1: AUTHOR (Researcher/sub-agent)
  └── Tulis file di /workspace/docs/content/events/e{NN}-{slug}/
      ├── general-id.md, general-en.md
      └── children-id.md, children-en.md
  └── Penulis WAJIB self-check sitasi sebelum submit (lihat Section 15.3)
  └── ⚠️ Sub-agent brief HARUS embed V1-V9 rules langsung (lihat content-style-guide.md Section 10)

STEP 2: QA CONTENT REVIEW — MANDATORY GATE (tidak boleh skip)
  └── ⛔ SETIAP push HARUS didahului QA. Berlaku untuk: content baru, expand, edit, fix script.
  └── Main agent jalankan `python3 scripts/qa-content.py` pada batch yang baru masuk
  └── Script mengecek 5 violation types (V1-V5) per file:
      V1: Pustaka tanpa sitasi (entry #N tanpa ^N di body)
      V2: Sitasi tanpa pustaka (^N di body tanpa entry #N)
      V3: Duplikat pustaka (sumber sama muncul >1x)
      V4: Pustaka >8 atau <3 entries
      V5: Sitasi ^0 (nol)
      V6: Al-Qur'an tidak di pustaka / duplikat / nama surah terpotong
      V7: Penjelasan ayat tanpa sitasi Al-Qur'an (paragraf setelah blockquote ayat harus cite entry Al-Quran)
      V8: Ayat tidak relevan (Tier 3 — generik, tidak ada korelasi historis)
      V9: Ayat overused (>3 events pakai ayat spesifik yang sama)
  └── Juga cek: section count ID↔EN sync, children slide count match
  └── Output: PASS list + FAIL list per event

STEP 2b: AUTO-FIX (jika ada FAIL)
  └── Main agent spawn Researcher sub-agent dengan brief spesifik:
      "Fix [event_id]: [violation list]. Baca file existing, perbaiki HANYA yang error.
       JANGAN rewrite seluruh artikel. Output ke path yang sama."
  └── Setelah fix selesai → re-run qa-content.py pada file yang diperbaiki
  └── Loop max 2x. Jika masih FAIL setelah 2 retry → flag untuk manual review Ahmad
  └── ⚠️ Hanya file PASS yang lanjut ke STEP 3

STEP 3: SYNC to project
  └── cp /workspace/docs/content/events/e{NN}-{slug}/*.md \
         /workspace/projects/baitul-hikmah/content/events/e{NN}-{slug}/
  └── ⚠️ KEDUA direktori harus identik — docs/ = source of truth, project/ = build copy
  └── ⚠️ HANYA file yang PASS QA yang di-sync

STEP 4: SYNC JSON sumber / Card Data (WAJIB setiap event baru)
  └── Update events-database.json → event.sources[] harus match markdown Daftar Pustaka
  └── Format JSON: versi ringkas. Format markdown: versi lengkap.
  └── **Card format** (events-database.json → sources[]):
      ```json
      {
        "id": "ibn-hisham",
        "title": "Al-Sirah al-Nabawiyyah",
        "author": "Ibn Hisham",
        "type": "primary"
      }
      ```
  └── Type values: `primary` (kitab sirah/tarikh), `hadith` (kitab hadits), `quran` (Al-Qur'an al-Karim)
  └── Al-Qur'an entry format: `{"id": "qs-...", "title": "Al-Quran al-Karim", "author": "QS. [Surah1], [Surah2]", "type": "quran"}`
  └── **Referensi**: lihat e01 sebagai contoh card data yang lengkap
  └── Card di-render di halaman event sebagai fallback "📚 Daftar Pustaka" saat markdown content tidak tersedia
  └── **WAJIB**: setiap event yang punya markdown content JUGA harus punya card data (JSON sources) yang sinkron

STEP 5: BUILD content JSON
  └── cd /workspace/projects/baitul-hikmah
  └── node scripts/build-content.js
  └── Output: src/data/event-content-map.json (stripped frontmatter, keyed by dir name)

STEP 6: BUILD website
  └── npx tailwindcss -i src/app/globals.css -o src/app/compiled.css --minify
  └── cp src/app/compiled.css public/styles.css
  └── npx --cache /workspace/.npm-cache next build

STEP 7: DEPLOY to dev
  └── CLOUDFLARE_API_TOKEN=... CLOUDFLARE_ACCOUNT_ID=... \
      npx wrangler pages deploy out --project-name=baitul-hikmah \
      --branch=develop --commit-dirty=true

STEP 8: VERIFY
  └── Buka https://develop.baitul-hikmah.pages.dev/event/{slug}/
  └── Cek: teks Arab render RTL ✓, sitasi clickable ✓, daftar pustaka tidak dobel ✓,
      wilayah + signifikansi muncul ✓, children slideshow works ✓
```

**QA Content Review Flow:**
```
Researcher output → qa-content.py audit
                         │
                    ┌─── PASS ───→ Sync to project → Build → Deploy
                    │
                    └─── FAIL ───→ Spawn Researcher (fix brief)
                                        │
                                   qa-content.py re-audit
                                        │
                                   ┌─── PASS ───→ Sync
                                   │
                                   └─── FAIL ───→ Retry 1x
                                                     │
                                                ┌─── PASS ───→ Sync
                                                │
                                                └─── FAIL ───→ 🚨 Manual review Ahmad
```

**QA Image Review Flow (illustrations):**
```
Doc Designer generates images → qa-images.py audit
                                      │
           ┌────── PASS ──────────────┤
           │                          │
           │    ┌── WARNING (E/F) ──→ Deploy + log for batch fix
           │    │
           │    └── BLOCKER (A-D) ──→ Spawn Doc Designer (regenerate brief)
           │                                │
           │                          qa-images.py re-audit
           │                                │
           │                          max 3 retry → 🚨 Ahmad
           │
           └→ Deploy to public/illustrations/
```

**Image QA Checks:**

| Check | Method | Severity |
|-------|--------|----------|
| A. No Prophet ﷺ depiction | Vision model | BLOCKER |
| B. Scene matches slide text | Vision model | BLOCKER |
| C. No text in image | Vision model | BLOCKER |
| D. Safe zone (centered, no cuts) | Vision model | BLOCKER |
| E. Aspect ratio 16:9 | Programmatic | WARNING |
| F. Min resolution 1280x720 | Programmatic | WARNING |
| G. Visual consistency (same event) | Vision model | WARNING |

**Scripts:** `scripts/qa-content.py` (content) + `scripts/qa-images.py` (illustrations)

**Shortcut command (full pipeline):**
```bash
# Sync + build + deploy (dari workspace root)
cp docs/content/events/e{NN}-{slug}/*.md projects/baitul-hikmah/content/events/e{NN}-{slug}/ && \
cd projects/baitul-hikmah && \
node scripts/build-content.js && \
npx tailwindcss -i src/app/globals.css -o src/app/compiled.css --minify && \
cp src/app/compiled.css public/styles.css && \
npx --cache /workspace/.npm-cache next build && \
CLOUDFLARE_API_TOKEN=$(cat /workspace/credentials/cloudflare-baitul-hikmah-token.txt) \
CLOUDFLARE_ACCOUNT_ID=e4cd70f84267e96fcb4391058053b995 \
npx wrangler pages deploy out --project-name=baitul-hikmah --branch=develop --commit-dirty=true
```

### Coordination Rules
1. **Main agent (Byte)** = orchestrator — TIDAK code sendiri, delegate ke specialist agents
2. **Researcher** = independent riset, output ke `/workspace/docs/content/events/`
3. **Engineer** = development di repo `baitul-hikmah`, push ke `develop` branch
4. **QA** = test setiap PR di dev environment sebelum Ahmad review
5. **All agents** brief HARUS specify absolute paths untuk output files
6. **Content & code** are separate pipelines — bisa parallel

---

## 8. Tech Stack 🚀

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Framework** | Next.js 14+ (App Router) | SSR/SSG, SEO-friendly, React ecosystem |
| **Styling** | Tailwind CSS + shadcn/ui | Rapid dev, consistent design system |
| **Animation** | Framer Motion + GSAP | Smooth page transitions, timeline animations |
| **Map** | MapLibre GL JS | Open-source, self-hosted, customizable |
| **Data** | JSON (dari `events-database.json`) + Markdown (artikel) | Structured data + rich content |
| **CMS** | Markdown files in repo (phase 1) → Headless CMS (phase 2) | Start simple, scale later |
| **i18n** | Custom React Context (`src/i18n/context.tsx`) | Simpler than next-intl for static export |
| **Hosting** | Cloudflare Pages | Sudah punya domain + CF token, edge-deployed |
| **Image Gen** | Gemini (nanobanana model) | Untuk ilustrasi per event |
| **Font Arabic** | Amiri / Scheherazade New | Untuk teks Qur'an & Hadits |

### Deployment & CI/CD

Project ini **external-facing** (akses publik) → menggunakan SDLC Tier 2 (External).

**Architecture: Single CF Pages Project + Branch Preview**

Menggunakan 1 CF Pages project dengan branch-based deployment (best practice):
- Branch `main` = production deployment
- Branch `develop` = preview deployment (auto-generated preview URL)
- Feature branches → PR ke `develop` → PR ke `main`

| Env | Domain | CF Pages Project | Branch | Deploy |
|-----|--------|-----------------|--------|--------|
| **Dev** | `develop.baitul-hikmah.pages.dev` | `baitul-hikmah` | `develop` | Auto-deploy on push |
| **Production** | `baitul-hikmah.id` | `baitul-hikmah` | `main` | Ahmad approve → merge → auto-deploy |

> **Why single project?** CF Pages natively supports branch previews within 1 project.
> 2 separate projects = duplicate config, double webhook, double maintenance — unnecessary.

**CI/CD Pipeline:**
1. Engineer push ke `develop` → Watchdog webhook → build + deploy (branch=develop) → preview di `develop.baitul-hikmah.pages.dev`
2. QA review di dev environment
3. Ahmad review & approve → merge PR `develop` → `main`
4. Watchdog webhook → build + deploy (branch=main) → production di `baitul-hikmah.id`

**Watchdog Integration:**
- Webhook URL: `https://webhook.ahadgroup.id/deploy/webhook`
- Project registered: `baitul-hikmah` (repo: `ahmadsyaifulloh08/baitul-hikmah`)
- Auth: HMAC-SHA256 (GitHub secret)

**DNS Setup:**
- `baitul-hikmah.id` → CF Pages custom domain (production)
- Dev: langsung pakai `develop.baitul-hikmah.pages.dev` (no custom domain needed)
- SSL: Cloudflare automatic

**GitHub Branch Protection:**
- `main`: require PR from `develop`, require review
- `develop`: direct push allowed (auto-deploy to preview)

---

## 9. Data Architecture 🚀

### Content Model per Event

```
Event
├── metadata (id, title, year, era, regions, category, significance)
├── content_general
│   ├── hero_image
│   ├── narrative (markdown — full article, bukan MDX)
│   ├── figures[] (tokoh terkait)
│   ├── dalil[] (ayat Qur'an + hadits, teks Arab wajib)
│   ├── analysis (signifikansi + konteks)
│   ├── citations (superscript ¹²³ → numbered bibliography)
│   └── bibliography[] (daftar pustaka, format standar Section 15.3)
├── content_children (slideshow presentation)
│   ├── slides[] (ordered array of slides)
│   │   ├── section (e.g. "siapa", "karya", "kenapa", "dalil")
│   │   ├── slide_number (1-3 per section)
│   │   ├── illustration_brief (🎨 detailed brief per Section 15.5)
│   │   ├── illustration (generated image — dominan di slide)
│   │   ├── text (narasi singkat — ditampilkan di dark overlay bawah)
│   │   └── emoji (section icon, placeholder until illustration ready)
│   └── total_slides (8-16 per event)
├── geo (coordinates, historical_name, modern_name)
└── nav (prev_event, next_event, related_events[])
```

### File Structure
```
/baitul-hikmah/
├── src/
│   ├── app/
│   │   ├── page.tsx              # Homepage (timeline)
│   │   ├── map/page.tsx          # Map mode
│   │   ├── event/[slug]/page.tsx # Event detail
│   │   ├── about/page.tsx
│   │   └── methodology/page.tsx
│   ├── components/
│   │   ├── timeline/             # Timeline components
│   │   ├── map/                  # Map components
│   │   ├── event/                # Event detail components
│   │   ├── ui/                   # shadcn/ui primitives
│   │   └── mode-switch.tsx       # General ↔ Anak toggle
│   ├── data/
│   │   ├── event-content-map.json    # Content data per event
│   │   ├── event-content-map.json # Content mapping
│   │   └── event-coordinates.json # GPS coordinates per event
│   ├── i18n/
│   │   ├── context.tsx           # Custom i18n React context
│   │   ├── id.json               # Indonesian translations
│   │   └── en.json               # English translations
│   └── ...
├── public/
│   ├── styles.css                # Compiled Tailwind CSS (loaded via <link>)
│   ├── illustrations/            # Generated artwork
│   │   └── children/             # Children slideshow illustrations
│   └── ...
├── postcss.config.js             # tailwindcss + autoprefixer
├── tailwind.config.ts            # darkMode: undefined (light only)
└── next.config.js                # output: 'export' (static)
```

---

## 10. SEO & Metadata ⚠️

- **Open Graph**: Per event — gambar, title, deskripsi
- **Structured Data**: JSON-LD (Article, Event, Person schemas)
- **Sitemap**: Auto-generated dari events data
- **Multi-language**: Indonesia (default) + English (Fase 1). Arabic (future)
- **Share**: Per event shareable link + social card

---

## 11. Fase & Milestone

### Fase 1-4 — SPRINT (Target: 14-15 Maret 2026) ⚡⚡⚡
> Agent-driven development — full parallel multi-agent execution.
> **Target LIVE: Sabtu 14 Maret 2026 (hari ini)**
> **Target ALL PHASES COMPLETE: Minggu 15 Maret 2026**

**Sabtu 14 Mar — GO LIVE 🚀**

| Waktu | Task | Agent | Status |
|-------|------|-------|--------|
| Siang | Setup project (Next.js + CF Pages + CI/CD dev/prod) | Engineer | ✅ Done |
| Siang | Design system & moodboard (era colors, typography, Islamic patterns) | Doc Designer | ✅ Done |
| Siang | Riset Event #1: Tahun Gajah (dewasa + anak) | Researcher | ✅ Done |
| Sore | Homepage timeline (interactive, filterable) | Engineer | ✅ Done |
| Sore | Event detail page + mode dewasa/dongeng toggle | Engineer | ✅ Done |
| Sore | Konten Tahun Gajah integrated | Engineer + Researcher | ✅ Done |
| Malam | Mobile responsive + PWA setup | Engineer | ⚠️ Responsive ✅ / PWA partial |
| Malam | QA di develop.baitul-hikmah.pages.dev | QA | ✅ Ongoing |
| Malam | Ahmad review → approve → **DEPLOY PRODUCTION** | Ahmad | ⏳ Pending (dev OK) |

**Minggu 15 Mar — ALL PHASES COMPLETE**

| Waktu | Task | Agent | Status |
|-------|------|-------|--------|
| Pagi | GIS interactive map (MapLibre + CARTO tiles) | Engineer + Data Analyst | ✅ Done |
| Pagi | Historical region names + timeline-synced animations | Engineer | ✅ Done (region labels) |
| Siang | Event #2: Yatim Piatu content (dewasa + anak) | Researcher | ✅ Done |
| Siang | SVG illustrations per event | Doc Designer | ⏳ Pending (emoji placeholders) |
| Siang | Bilingual content (ID + EN) | Researcher | ✅ e01 + e02 done |
| Sore | Children slideshow mode (fullscreen modal) | Engineer | ✅ Done |
| Sore | Enhanced markdown renderer (tables, citations, Arabic) | Engineer | ✅ Done |
| Sore | Light mode only + i18n toggle | Engineer | ✅ Done |
| Malam | Polish, performance, bug fixes | Engineer + QA | 🔄 In progress |
| Malam | Final deploy production | Ahmad | ⏳ Pending |

**Post-Sprint (ongoing):**
- [ ] Content expansion (128 events sequential)
- [ ] Arabic language support
- [ ] TWA → Google Play Store
- [ ] Community contributions
- [ ] Print/PDF export per article

---

## 12. Risiko & Mitigasi

| Risiko | Impact | Mitigasi |
|--------|--------|----------|
| Akurasi konten (dalil/sejarah salah) | 🔴 High | Manhaj Bukhari — validasi 3 tahap, minimal 2 sumber per klaim |
| Ilustrasi tidak konsisten | 🟡 Medium | Lock moodboard per era, gunakan consistent prompts |
| Map complexity terlalu tinggi | 🟡 Medium | Start simple (markers only), iterasi ke animated regions |
| Performance (heavy animations) | 🟡 Medium | SSG, lazy load, code splitting, Cloudflare CDN |
| Konten anak tidak engaging | 🟡 Medium | Test dengan anak Ahmad, iterate berdasarkan feedback dongeng malam |

---

## 13. Image Generation Brief

**Model**: Gemini (nanobanana) — Ahmad to provide access

**Moodboard per Era:**
| Era | Color Tone | Visual Style | Elements |
|-----|-----------|--------------|----------|
| Pra-Islam | Sandy, muted | Desert landscapes, Ka'bah | Sand dunes, caravans, stars |
| Kenabian | Green + gold | Warm, luminous | Light rays, Madinah, crescents |
| Rashidin | Blue + white | Noble, expansive | Maps, scrolls, swords |
| Umayyah | Gold + amber | Grand, architectural | Damascus, mosques, coins |
| Abbasiyah | Purple + gold | Intellectual, rich | Books, astrolabes, Baghdad |
| Fragmentasi | Rose + steel | Conflicted, resilient | Castles, scholars, ships |
| Kemunduran | Deep red + gray | Somber, reflective | Ruins, fire, manuscripts |

**Children's style**: Bright, rounded characters, big eyes, simplified backgrounds, Pixar-meets-Islamic-art aesthetic

---

## 14. Dependencies & Kebutuhan dari Ahmad

1. ✅ Domain `baitul-hikmah.id` — sudah connected ke Cloudflare
2. ✅ Cloudflare API Token — sudah disimpan
3. ⏳ **Gemini nanobanana model access** — untuk generate ilustrasi (hero images saja, bukan konten utama)
4. ⏳ **Review & approval PRD ini** — sebelum mulai development
5. ⏳ **Feedback format anak-anak** — dari pengalaman dongeng malam dengan Canva presentation
6. ⏳ **Git repo setup** — branches `main` (prod) + `develop` (dev), Cloudflare Pages connected

---

## Appendix

### A. Referensi Visual
- **GIS Map Animation**: [YouTube - Historical Map](https://www.youtube.com/watch?v=AvFl6UBZLv4)
- **Timeline History**: [YouTube - Timeline](https://youtu.be/d0AbF1FlqCE)
- **Frontend Components**: [21st.dev](https://21st.dev)
- **Children's Format**: [Canva Presentation](https://www.canva.com/design/DAG2YQ-Mcoc/)

### B. Data Source
- `events-database.json`: 128 events, 7 eras, 9 regions, 6 categories
- `islamic-research.md`: Full narrative per era + tokoh kunci + daftar pustaka

### C. Metodologi Riset
- Tahap 1: Prinsip Imam Bukhari (ISNAD → MATAN → JARH WA TA'DIL → TAWATUR)
- Tahap 2: Elaborasi Al-Ghazali (sintesis) + Ibn Rushd (rasionalisme) + Ibn Taimiyah (kritik & dalil)
- Tahap 3: Dokumentasi akademis (struktur, daftar pustaka, netralitas, kontekstualisasi, verifikasi silang)

---

## Appendix D. Document Structure

Project Baitul Hikmah memiliki 2 dokumen utama yang saling terkait:

| Dokumen | Lokasi | Fungsi |
|---------|--------|--------|
| **PRD (Product Requirements Document)** | `/workspace/docs/prd/baitul-hikmah-website.md` | Spesifikasi produk — fitur, tech stack, design, CI/CD, multi-agent model |
| **Research Plan** | `/workspace/docs/research/islamic-research.md` | Materi riset — timeline 128+ events, metodologi Manhaj Bukhari, tokoh, daftar pustaka |
| **Research Data (JSON)** | `/workspace/dashboard/data/events-database.json` | Data terstruktur — events, regions, categories, eras (machine-readable) |

**Alur kerja:**
- PRD mendefinisikan **apa yang dibangun** (website spec)
- Research Plan mendefinisikan **konten apa yang diisi** (materi per event)
- Research Data adalah **sumber data terstruktur** yang di-consume oleh website

**Jangan duplikasi** — PRD reference ke Research Plan, bukan copy isinya.

---

---

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
