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

## 7. Development Workflow

> See: [docs/development-workflow.md](development-workflow.md)


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

## 11. Milestone Log

> See: [docs/archive/sprint-log.md](archive/sprint-log.md)


## 12. Risiko & Mitigasi

| Risiko | Impact | Mitigasi |
|--------|--------|----------|
| Akurasi konten (dalil/sejarah salah) | 🔴 High | Manhaj Bukhari — validasi 3 tahap, minimal 2 sumber per klaim |
| Ilustrasi tidak konsisten | 🟡 Medium | Lock moodboard per era, gunakan consistent prompts |
| Map complexity terlalu tinggi | 🟡 Medium | Start simple (markers only), iterasi ke animated regions |
| Performance (heavy animations) | 🟡 Medium | SSG, lazy load, code splitting, Cloudflare CDN |
| Konten anak tidak engaging | 🟡 Medium | Test dengan anak Ahmad, iterate berdasarkan feedback dongeng malam |

---

## 13. Image Generation

> See: [docs/illustration-guide.md](illustration-guide.md) + [docs/illustration-registry.md](illustration-registry.md)


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

## Design Decisions

> See: [docs/archive/design-decisions.md](archive/design-decisions.md)
