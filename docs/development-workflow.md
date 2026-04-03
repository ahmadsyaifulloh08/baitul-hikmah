# Development Workflow — Baitul Hikmah
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


> Extracted from PRD.md Section 7. See PRD.md for product requirements.
