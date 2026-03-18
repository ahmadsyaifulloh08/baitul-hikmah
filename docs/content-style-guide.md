# Content Style Guide — Baitul Hikmah

> Panduan menulis konten untuk semua event. WAJIB dibaca sebelum menulis.
> Extracted from PRD Section 15.

---

## 1. Referensi Al-Quran — Wajib Sertakan Teks Arab

Setiap kutipan Al-Quran **WAJIB** menyertakan teks Arab asli.

**Format standar:**

```
<ayat>
  <arab>إِنَّ مَعَ الْعُسْرِ يُسْرًا</arab>
  <terjemahan>"Sesungguhnya bersama kesulitan ada kemudahan." (QS. Al-Insyirah: 6)</terjemahan>
</ayat>
```

- **Urutan**: Teks Arab → Terjemahan Indonesia (dan/atau English jika bilingual)
- **Font Arab**: Amiri atau Scheherazade New
- **Arah teks**: `dir="rtl"` untuk teks Arab
- **Tidak boleh** menampilkan terjemahan saja tanpa teks Arab asli
- **Transliterasi Latin** (opsional): bisa ditambahkan di antara Arab dan terjemahan

---

## 2. Format Tabel — Web-Friendly

**Prioritas format:**
1. Styled HTML table dengan Tailwind classes — untuk data tabular
2. Responsive card list — untuk data vertikal di mobile
3. Definition list (`<dl>/<dt>/<dd>`) — untuk pasangan label-value

**Aturan:**
- Semua tabel HARUS responsive (`overflow-x-auto` wrapper)
- Untuk konten anak-anak: **JANGAN gunakan tabel** — gunakan visual cards atau list

---

## 3. Sitasi & Daftar Pustaka

> ⛔ **ZERO TOLERANCE POLICY**: File yang melanggar aturan sitasi = REJECT. Tidak ada exception.

Setiap klaim yang merujuk sumber **WAJIB** memiliki angka sitasi.

### ⚠️ CONSOLIDATED BIBLIOGRAPHY (WAJIB)

Daftar pustaka menggunakan format **consolidated** — satu entry per sumber unik. Sitasi berulang ke sumber yang sama menggunakan nomor yang SAMA.

**❌ SALAH (footnote-style — DILARANG):**
```
1. Ibn Hisham, Al-Sirah, jilid 1, bab "Kafaalah".
2. Ibn Hisham, Al-Sirah, jilid 1, bab "Kasih Sayang".
3. Al-Mubarakfuri, Al-Rahiq al-Makhtum, bab "Masa Kecil".
4. Ibn Hisham, Al-Sirah, jilid 1, bab "Perjalanan".   ← DUPLIKAT sumber #1!
```

**✅ BENAR (consolidated — WAJIB):**
```
1. Ibn Hisham, *Al-Sirah al-Nabawiyyah*, jilid 1.
2. Al-Mubarakfuri, *Al-Rahiq al-Makhtum*.
3. Al-Tirmidzi, *Sunan al-Tirmidzi*, Kitab al-Manaqib, no. 3620.
```
Lalu dalam teks: "...sebagaimana diriwayatkan Ibn Hisham.¹" dan "...di tempat lain, Ibn Hisham juga mencatat...¹" — pakai nomor **1** lagi, bukan nomor baru.

### Aturan Daftar Pustaka

- **Min 3 sumber** per event — cukup untuk triangulasi
- **Tidak ada batas maksimal** — boleh lebih dari 8 asalkan SEMUA tersitasi dan consolidated (1 entry = 1 karya unik)
- Satu entry = satu karya unik (kitab/buku)
- Detail bab/halaman boleh disebut **inline** di teks, BUKAN di daftar pustaka
- Contoh inline: "Ibn Hisham dalam bab *Perjalanan ke Syam* menyebutkan...¹"
- Sitasi sequential (1, 2, 3, ...) — nomor sama untuk sumber sama
- Klik nomor → scroll ke daftar pustaka (anchor link)

### 🚫 5 Violation Types (Auto-Reject)

| # | Violation | Contoh | Severity |
|---|-----------|--------|----------|
| V1 | **Pustaka tanpa sitasi** — entry di daftar pustaka yang tidak pernah di-cite di body | Pustaka #5 ada tapi ^5 tidak muncul di teks | REJECT |
| V2 | **Sitasi tanpa pustaka** — superscript di body yang mengarah ke entry yang tidak ada | ^8 di teks tapi pustaka cuma 6 entry | REJECT |
| V3 | **Duplikat pustaka** — sumber yang sama muncul >1x di daftar pustaka | Ibn Hisham muncul di #1, #4, #7 | REJECT |
| V4 | **Pustaka <3 entries** — terlalu sedikit, kurang triangulasi | Hanya 1-2 sumber | REJECT |
| V5 | **Sitasi ⁰ (nol)** — nomor sitasi harus mulai dari 1 | ^0 di teks | REJECT |

### Self-Check Sebelum Submit

Sebelum menyerahkan file, penulis WAJIB melakukan self-check:

```
CHECKLIST SITASI:
□ Hitung jumlah entry di Daftar Pustaka → minimal 3, consolidated (1 entry = 1 karya unik)
□ Untuk SETIAP entry #N → cari ^N atau ⁿ di body → harus ada minimal 1x
□ Untuk SETIAP ^N di body → cek entry #N ada di Daftar Pustaka
□ Cek tidak ada 2 entry yang merujuk kitab/buku yang SAMA
□ Tidak ada ^0 (nol) di body
□ Detail bab/halaman di INLINE text, BUKAN di entry pustaka
```

### Format Daftar Pustaka

```
## Daftar Pustaka

1. Ibn Hisham, *Al-Sirah al-Nabawiyyah*, jilid 1.
2. Al-Mubarakfuri, Shafiyyurrahman, *Al-Rahiq al-Makhtum*, Riyadh: Dar al-Salam, 1976.
3. Al-Tirmidzi, *Sunan al-Tirmidzi*, Kitab al-Manaqib, no. 3620.
```

### Format Referensi Hadits
- WAJIB sertakan **nomor hadits** + **kitab/bab**
- Contoh: `HR Muslim, no. 1162, Kitab al-Shiyam`
- TIDAK BOLEH hanya `(HR Muslim)` tanpa nomor

### Format dalam Body Text
- Superscript: `teks klaim¹`, `fakta sejarah²³`
- Renderer auto-converts ke: `<sup><a href="#ref-1">1</a></sup>` (clickable)
- **Multiple citations**: `^4^5` → rendered sebagai `⁴ ⁵` (dipisah spasi, standar sitasi akademis)
- **Heading level**: Renderer support `##` (h2), `###` (h3), dan `####` (h4)
- Daftar pustaka HANYA dari markdown content (bukan dari JSON `event.sumber`)
- **Setiap paragraf fakta historis HARUS punya minimal 1 sitasi** — paragraf tanpa sitasi = klaim tanpa sumber

---

## 4. Children Mode — Slideshow Format

- **Format**: Popup slideshow presentation (fullscreen modal)
- **Visual**: Ilustrasi gambar dominan per slide, dark gradient overlay di bawah untuk teks
- **Slide count**: Per section 2-3 slide, total ~8-16 slide per event
- **Navigasi**: Swipe/arrow, progress dots
- **Teks**: Selectable & copyable di atas overlay

---

## 5. Brief Ilustrasi Anak-Anak

Setiap slide children mode **WAJIB** memiliki brief ilustrasi. Lihat `docs/illustration-guide.md` untuk format lengkap.

**6 Elemen Wajib:**
1. **Setting/Latar** — lokasi + waktu
2. **Karakter & Pose** — siapa, apa yang dilakukan, ekspresi
3. **Objek Kunci** — benda penting
4. **Warna Dominan** — 3-4 warna
5. **Suasana/Mood** — emosi
6. **Komposisi** — foreground/background

---

## 6. Data Consistency — JSON ↔ Markdown

- `research_agenda.json` (`event.sumber[]`) = versi ringkas
- Markdown `## Daftar Pustaka` = versi lengkap
- **Keduanya HARUS sinkron**
- Ketika rich content tersedia → halaman detail pakai markdown saja (cegah duplikasi)

---

## 7. Penggunaan Teks Arab

Teks Arab HANYA untuk **Al-Quran dan Hadits**. TIDAK untuk istilah/nama/tempat/kitab.

**✅ GUNAKAN teks Arab untuk:**
- Ayat Al-Quran — teks Arab lengkap + nomor ayat ﴿N﴾
- Hadits — teks Arab (jika tersedia) + terjemahan
- Kutipan sakral/historis
- Simbol ﷺ (inline)

**❌ JANGAN gunakan teks Arab untuk:**
- Istilah/konsep: cukup *qabilah* (BUKAN قبيلة)
- Nama tokoh, ulama, penulis, tempat, suku, kitab

**Format Quran dalam markdown:**
```
> أَلَمۡ تَرَ كَيۡفَ فَعَلَ رَبُّكَ بِأَصۡحَٰبِ ٱلۡفِيلِ ﴿١﴾
>
> *"Tidakkah engkau perhatikan bagaimana Tuhanmu..."*
> — QS Al-Fil (105): 1-5
```

**Nomor ayat Arab WAJIB**: Setiap ayat diakhiri marker `﴿N﴾`
**Referensi**: `— QS. [Nama Surah] ([Nomor]): [Ayat]` (BUKAN `(QS.` dan BUKAN `[nomor]`)

**Rendering rules:**
- Baris >40% karakter Arab → RTL block dengan font Amiri
- Teks Arab **TIDAK italic** — baik di blockquote maupun paragraph

---

## 8. Diksi & Writing Style

**Kata yang DILARANG → Pengganti:**

| ❌ Jangan | ✅ Gunakan | Alasan |
|---|---|---|
| "klien" | "negara bawahan", "vassal" | Bukan bisnis |
| "produk" | "buah", "hasil", "karya" | Bukan komersial |
| "vivid" | "rinci", "gamblang", "hidup" | Padanan Indonesia |
| "klan" | "suku", "kabilah" | Terminologi Arab |
| "launching" | "peluncuran", "dimulainya" | Baku |
| "impact" | "dampak", "pengaruh" | Baku |

**Prinsip:**
1. Gunakan terminologi Arab yang tepat: "kabilah", "khalifah", "ummah"
2. Hindari kata serapan bisnis/tech
3. Padanan Indonesia > kata asing
4. Tone: Akademis tapi accessible
5. Reviewer wajib flag kata menyalahi panduan

---

## 9. Struktur Artikel General

**Urutan WAJIB:**
```
# [Judul]                          ← di-skip renderer
## [Konteks/Latar Belakang]        ← h2, pembuka
## [Peristiwa Utama]               ← narasi kronologis
### [Sub-section jika perlu]       ← h3
## [Dialog/Momen Kunci]            ← blockquote Quran/Hadits
## [Analisis/Hikmah]               ← bold poin + paragraf
## [Kronologi] (opsional)          ← tabel
## [Catatan Metodologis] (opsional)
---
## Daftar Pustaka
```

**Writing Style:**
1. Naratif akademis-populer — hidup tapi ilmiah
2. Sumber disebut inline: "Ibn Hisham mencatat..."
3. Sitasi superscript sequential ¹²³
4. Paragraf 3-5 kalimat
5. Bold nama tokoh pertama kali: "**Abdul Muthalib** bin Hasyim"
6. Italic istilah Arab transliterasi: *qabilah*
7. Tahun: "570 M" (ID) / "570 CE" (EN)

**Pola Blockquote Quran:**
```markdown
> [Teks Arab + ﴿N﴾]
>
> *"[Terjemahan italic]"*
> — QS. [Nama Surah] ([Nomor]): [Ayat]
```

**Pola Hadits:**
```markdown
> [Teks Arab hadits]
>
> *"[Terjemahan italic]"*
> — HR [Perawi], no. [Nomor], [Kitab]
```

---

## 10. QA Automation

### Script: `scripts/qa-content.py`

Automated quality gate yang WAJIB dijalankan sebelum sync & deploy.

```bash
# Audit semua events
python3 scripts/qa-content.py

# Audit event tertentu
python3 scripts/qa-content.py e03 e47

# Output JSON (untuk automation)
python3 scripts/qa-content.py --json
```

**Checks:** V1-V5 (sitasi), V6 (ID↔EN section count), V7 (children slide count), file completeness.

**Pipeline integration:**
```
Researcher output → qa-content.py audit
       │
  ┌─── PASS ───→ Sync → Build → Deploy
  │
  └─── FAIL ───→ Spawn Researcher (fix brief) → re-audit
                       │
                  ┌─── PASS ───→ Sync
                  └─── FAIL ───→ Retry 1x → PASS or 🚨 Manual review Ahmad
```

**Max retry: 2x.** Jika masih FAIL setelah 2 retry → flag manual review.

---

## 11. QC Checklist — Wajib Lolos Sebelum Deploy

### A. Sitasi & Daftar Pustaka (BLOCKER — cek pertama!)
- [ ] **V1**: Setiap entry pustaka #N → ada ^N di body (tidak ada pustaka tanpa sitasi)
- [ ] **V2**: Setiap ^N di body → ada entry #N di daftar pustaka (tidak ada orphan citation)
- [ ] **V3**: Tidak ada duplikat — setiap entry merujuk karya/kitab BERBEDA
- [ ] **V4**: Jumlah entry daftar pustaka: **minimal 3**, consolidated (1 entry = 1 karya unik)
- [ ] **V5**: Tidak ada sitasi ^0 atau ⁰ — nomor mulai dari 1
- [ ] Sitasi reuse — sumber sama = nomor SAMA (bukan nomor baru)
- [ ] Detail bab/halaman di inline text, BUKAN di entry pustaka
- [ ] Setiap paragraf klaim historis punya minimal 1 sitasi

### B. Konten (per event)
- [ ] Teks Arab HANYA di Quran/Hadits — BUKAN di istilah/nama/tempat
- [ ] Ayat Quran: teks Arab + nomor ayat ﴿N﴾ + terjemahan
- [ ] Hadits: nomor hadits + kitab/bab
- [ ] Referensi format: `— QS. [Nama] (nomor): ayat` / `— HR [Perawi], no. [nomor], [Kitab]`
- [ ] Setiap blockquote ada keterangan sumber di baris terakhir
- [ ] JSON `event.sumber[]` sinkron dengan markdown
- [ ] Diksi sesuai panduan (Section 8)
- [ ] Tidak ada artefak: `>`, `<`, `*`, `|` yang tidak ter-render
- [ ] Markdown `# Judul` ada (metadata) tapi di-skip renderer

### B. Children Mode (per event)
- [ ] 4 bagian/sections dengan tone dongeng
- [ ] Brief ilustrasi 🎨 lengkap 6 elemen per section
- [ ] Tidak ada tabel — gunakan list/visual cards

### C. Layout & Styling (halaman detail)
- [ ] Badges: Era + Kategori + Wilayah + Signifikansi + Tahun (fontSize 11, borderRadius 14)
- [ ] Judul `<h1>` di bawah badges
- [ ] Tokoh: label + pills (fontSize 12) — utama + pendukung
- [ ] Teks Arab: font Amiri, RTL, **tidak italic**
- [ ] Daftar pustaka: tidak dobel

### D. Data Sync
- [ ] `docs/content/events/` = `projects/baitul-hikmah/content/events/` (identik)
- [ ] `event-content.json` di-rebuild
- [ ] `research_agenda.json` — figures + sumber sinkron

---

## 12. ID ↔ EN Sync Rules

Setiap event WAJIB 4 file sinkron: `general-id.md`, `general-en.md`, `children-id.md`, `children-en.md`

| Check | Severity | Rule |
|-------|----------|------|
| Slide count | **BLOCKER** | children-id dan children-en HARUS jumlah slide SAMA |
| Section count | **BLOCKER** | Jumlah `## heading` harus sama |
| Section order | **BLOCKER** | Urutan section sama |
| Content meaning | **BLOCKER** | EN = faithful translation, bukan creative rewrite |

**QA automation:**
```bash
node scripts/qa-sync-id-en.js
```

**Translation rules:**
- EN = faithful translation
- Keep Arabic transliteration + add English
- Names: keep Arabic names konsisten dengan ID
- Tone: same storytelling level
