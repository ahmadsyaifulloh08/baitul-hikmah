# ⛔ OBSOLETE — Batch Image Generation Workflow v2

> **Status: ⛔ OBSOLETE** — Digantikan oleh **v3** (`batch-image-generation-v3.md`).
> Jangan gunakan workflow ini. Baca v3 untuk workflow terbaru.
>
> **Alasan obsolete**: Placeholder chat reuse menyebabkan context pollution (scene event lama muncul).
> v3 menggunakan new chat per slide + sequential generation.
>
> ---
> **Historical note**: Workflow ini berhasil pada 2026-03-20 (e03 batch, 7 images parallel).
> Disimpan sebagai referensi lessons learned saja.
> **Context**: Mengatasi masalah "scene identik" saat generate multiple images di 1 chat Gemini.

---

## Masalah yang Diselesaikan

1. **Scene identik**: Generate banyak prompt di 1 chat → Gemini generate gambar yang sama berulang
2. **Rate limit**: Sequential generate (1 per 1) terlalu lama (~2 min per image)
3. **QA bottleneck**: Kirim gambar satu-satu ke Ahmad untuk review tidak efisien

## Pendekatan

**1 prompt = 1 chat terpisah** → generate paralel di banyak tab.

Setiap tab buka chat berjudul `[N] Placeholder - Image Generation` (N = 1-10).
Chat-chat ini harus sudah dibuat sebelumnya di Gemini.

---

## Pre-requisites

- [ ] PinchTab instance `work` running + logged in Google
- [ ] 10 chat Gemini sudah dibuat dengan judul `[1] Placeholder - Image Generation` s/d `[10] Placeholder - Image Generation`
- [ ] Prompt files siap di `/workspace/tmp/{event}-prompts/`
- [ ] PRD illustration rules loaded (Section 16 / `docs/illustration-guide.md`)

---

## Workflow

### Phase 0: Persiapan Konten

**0.1: Baca PRD**
- Baca `docs/prd/baitul-hikmah-website.md` — khususnya:
  - Section 16 → illustration guidelines (atau `docs/illustration-guide.md`)
  - Mode anak-anak: 6-16 slides per event, 2-3 slide per section
  - Islamic rules, safe zone, no text, golden glow standar
- Baca `docs/content-style-guide.md` — tone dongeng, diksi anak-anak

**0.2: Draft/Review Konten Anak (`children-en.md`)**
- Cek apakah konten children sudah ada di `docs/content/events/{event}/children-en.md`
- Jika belum ada → tulis konten baru mengikuti pola e01/e02:
  - 5-7 sections, ~80-100 words per section
  - Tone dongeng (naratif), bukan eksplanatif
  - Setiap section diakhiri dengan `🎨 Illustration Brief`
- Jika sudah ada → review:
  - Simulasi slide split (jalankan parser atau `audit-slides.js`)
  - Verifikasi jumlah slide masuk range PRD (6-16)
  - Jika terlalu banyak → trim teks. Jika terlalu sedikit → tambah section.

**0.3: Tulis/Review Brief Ilustrasi per Slide**
- Setelah slide split diverifikasi → pastikan setiap slide punya brief unik
- Brief berdasarkan **narasi slide** (hasil split), bukan per section
- Format 6 elemen wajib per PRD:
  1. Setting/Latar
  2. Karakter & Pose
  3. Objek Kunci
  4. Warna Dominan
  5. Suasana/Mood
  6. Komposisi
- 2-3 slide dari section yang sama → brief HARUS scene visual BERBEDA
- Jika 2 slide scene-nya sama → gabung atau buat variasi

**Output Phase 0:**
- `children-en.md` final dengan slide count terverifikasi
- Tabel mapping: Slide N → Section → Brief → Scene description
- Siap untuk Phase 1

---

### Phase 1: Tulis Prompt per Slide

Setiap prompt WAJIB include (per PRD):
```
- "Image ratio: exactly 16:9 landscape (wide). Resolution: 1792x1024."
- "GOLDEN RADIANT GLOW — a circular warm golden-white light with gentle rays like a small warm sun" (untuk Nabi)
- "COMPOSITION: Place all important subjects within the CENTER 70% of the image. Leave outer edges clear."
- "CRITICAL: Do NOT include ANY text, words, letters, labels, captions, titles, signatures, or writing of any kind."
```

Save ke:
```
/workspace/tmp/{event}-prompts/slide-{NN}.txt
```

### Phase 2: Submit Batch (1 prompt per chat)

```
For each prompt (i = 1 to N):
  1. Klik chat "[i] Placeholder - Image Generation" di sidebar
  2. Type prompt ke textbox
  3. Klik "Send message"
  4. JANGAN tunggu — langsung pindah ke chat [i+1]
```

**Key**: Semua chat generate IMAGE secara paralel. Tidak perlu tunggu per chat.

**Max batch**: 10 chat (sesuai jumlah Placeholder yang tersedia).
Untuk >10 gambar, split jadi multiple batch.

### Phase 3: Wait (~3-5 menit)

Tunggu semua chat selesai generate. Gemini generates text dulu, lalu image (~60-90s per prompt).

Tidak perlu polling. Cukup wait 5 menit flat.

### Phase 4: Download Batch

```
For each chat (i = 1 to N):
  1. Klik chat "[i] Placeholder" di sidebar
  2. Find last "AI generated" image node
  3. Hover → Click image → Lightbox opens
  4. Click "Download full size image"
  5. Wait 10-15s for file
  6. Close lightbox
  7. Next chat
```

Files appear di: `/workspace/shared/pinchtab-downloads/`

### Phase 5: Rename & Assign

```bash
# Rename downloaded files to slide names
mv "Gemini_Generated_Image_XXXXX.png" e03-slide-03.png
# Copy to project
cp e03-slide-*.png /workspace/projects/baitul-hikmah/public/illustrations/children/
```

**⚠️ PENTING**: Urutan download ≠ urutan slide!
Harus buat mapping tabel: file → chat → slide.

### Phase 6: QA — Composite Image Review

> QA checklist detail: lihat [`docs/illustration-guide.md`](../illustration-guide.md) Section 9 Phase 2.
> Jangan duplikasi checklist di sini — single source di illustration-guide.

**Langkah:**

1. **Compile semua gambar event** ke 1 composite grid image
   - Resize ke thumbnail ~420x236 (16:9)
   - Grid layout (misal 4×3 untuk 12 slides)
   - Label setiap cell: nomor slide + section title + narasi singkat

2. **Vision model audit** — inspect composite dengan prompt:
   - Per slide: scene match narasi? Golden glow only? No text? Safe zone?
   - Output: tabel PASS / FAIL / BORDERLINE per slide

3. **Kirim composite + audit report ke Ahmad**
   - 1 gambar saja (bukan 12 terpisah)
   - Ahmad review: confirm PASS/FAIL

4. **FAIL → regenerate** di chat cadangan [8], [9], [10]
   - Max 3 retry per image
   - Jika tetap gagal → escalate ke Ahmad

### Phase 7: Post-Batch Evaluation (WAJIB setelah setiap event selesai)

Setelah QA selesai dan semua gambar PASS, lakukan evaluasi menyeluruh:

**7.1: Story Flow Audit**
- Lihat semua 12 gambar berurutan sebagai slideshow
- Apakah ada transisi visual yang janggal? (misal: siang → malam → siang)
- Apakah karakter konsisten? (Abu Thalib, Bahira sama di semua slide?)
- Apakah color palette konsisten? (warm watercolor di semua slide?)

**7.2: Reassignment Check**
- Verifikasi mapping: Slide N → Image file → Scene → Narasi
- Gambar lama yang di-reassign (misal e03-slide-04 = old biara) masih match?
- Urutan visual masuk akal mengikuti alur cerita?

**7.3: Gap Analysis**
- Ada slide yang scene-nya terlalu mirip? → pertimbangkan regenerate salah satu
- Ada slide yang scene-nya tidak cukup berbeda dari sebelahnya?
- Ada Islamic compliance issue yang terlewat di QA per-image?

**7.4: Document Results**
- Catat hasil evaluasi di `memory/YYYY-MM-DD.md`
- Update tabel slide mapping dengan status final
- Log issues untuk improvement di batch berikutnya

**7.5: Bilingual Sync Check**
- Verify `children-en.md` dan `children-id.md` menghasilkan jumlah slide SAMA
- Jika ada merge/split paragraf → WAJIB dilakukan di kedua bahasa
- Run parser di kedua file, bandingkan output

**Output Phase 7:** Event siap deploy. Semua slide PASS QA + evaluasi story flow + bilingual sync verified.

### Phase 8: Update Code & Deploy

```javascript
// EventContent.tsx — update illustration count
'e03-perjalanan-syam': Array.from({length: 12}, (_, i) => 
  `/illustrations/children/e03-slide-${String(i+1).padStart(2,'0')}.png`),
```

Build + push → CF Pages auto-deploy.

---

## Chat Assignment Template

| Chat | Slide | Scene | Status |
|:---:|:---:|:---|:---:|
| [1] | — | — | ❌ |
| [2] | — | — | ❌ |
| [3] | — | — | ❌ |
| [4] | — | — | ❌ |
| [5] | — | — | ❌ |
| [6] | — | — | ❌ |
| [7] | — | — | ❌ |
| [8] | — | cadangan / retry | 🟡 |
| [9] | — | cadangan / retry | 🟡 |
| [10] | — | cadangan / retry | 🟡 |

---

## Risiko & Mitigasi

| Risiko | Mitigasi |
|--------|----------|
| Scene identik meski beda chat | Prompt harus sangat spesifik per scene — detail berbeda |
| Gemini rate limit | 10 paralel = 10 request burst. Jika hit limit, tunggu 15 min |
| Snap error intermittent | Retry 3x per snap call + 3s delay |
| Chat tidak ketemu di sidebar | Search by name atau scroll sidebar |
| Tab limit PinchTab | Max 20 tabs. 10 chat = aman |
| File naming confusion | Buat mapping tabel SEBELUM rename |

---

## Lessons Learned

### ✅ Proven: 2026-03-20 (e03 batch, 7 images)

**Iterasi 1 — GAGAL: Semua prompt di 1 chat**
- Submit 5 prompt berbeda di chat "Placeholder - Image Generation"
- Hasil: 5 gambar IDENTIK (scene sama persis) — Gemini mengulang scene terakhir
- Root cause: Gemini menggunakan context chat sebelumnya, mengabaikan prompt baru

**Iterasi 2 — GAGAL: New chat via navigasi**
- `nav gemini.google.com/app` → type → send
- Hasil: Gemini respond text-only, tidak generate image
- Root cause: New chat blank tidak trigger image generation mode secara konsisten

**Iterasi 3 — BERHASIL: 1 prompt per named chat (parallel)**
- 7 prompt → 7 chat terpisah `[1]-[7] Placeholder - Image Generation`
- Submit berurutan ke setiap chat (~30s per chat, total 5 min)
- Wait 5 menit (parallel generation)
- Download per chat dengan navigate back to main → click chat → lightbox → download
- Hasil: **7 gambar UNIK, scene berbeda-beda** ✅

**Timing breakdown:**
- Phase 2 (submit): ~5 min (7 chats × 30s + retry 3 yang gagal)
- Phase 3 (wait): 5 min flat
- Phase 4 (download): ~5 min (7 chats × 40s)
- Phase 6 (QA composite): ~1 min
- **Total: ~16 min untuk 7 gambar**

### Technical Issues & Fixes

| Issue | Fix |
|-------|-----|
| 1 chat + multi prompt → identical images | **Use separate named chats** — 1 prompt per chat |
| Sidebar refs shift after navigation | **Always navigate to main page first** before finding chat ref |
| `stat -f %m` fails on Linux | Use `stat -c %Y` with macOS fallback |
| Snap JSON corrupt (control chars) | `re.sub(r'[\x00-\x1f]', ' ', raw)` before `json.loads` |
| Snap returns empty string intermittent | Retry loop (3-5 attempts, 3s delay) |
| Send button not found (3/7 first run) | Longer wait after chat click (5s vs 3s) + retry |
| Lightbox has 2 Close buttons sometimes | Download ref = last node with "Download" in name |
| Download file appears after 10-15s | `sleep(15)` after click download |

### Pre-requisites Confirmed
- ✅ Named chats `[1]-[10] Placeholder` MUST exist before batch
- ✅ Ahmad creates these manually in Gemini (agent cannot create named chats)
- ✅ PinchTab instance `work` must be logged into Google
- ✅ Max 10 parallel (10 named chats available)

### Decision: Workflow Doc, Not Skill (2026-03-20)
- Pipeline ini project-specific (Baitul Hikmah + PinchTab + Gemini)
- Skill cocok untuk generic/reusable lintas project
- Workflow doc di project sudah cukup — reference dari TOOLS.md jika perlu
