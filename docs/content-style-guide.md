# Content Style Guide — Baitul Hikmah

> Panduan menulis konten untuk semua event. WAJIB dibaca sebelum menulis.
> Extracted from PRD Section 15.

---

## 1. Referensi Al-Quran — Hierarki Kutipan + Wajib Teks Arab

### Hierarki Kutipan Al-Quran (CRITICAL)

Tidak semua event perlu kutipan ayat Al-Quran. Gunakan hierarki berikut:

**Tier 1 — Asbabun Nuzul / Korelasi Historis Langsung (PRIORITAS UTAMA)**
Ayat yang turun berkaitan langsung dengan event, atau secara historis tercatat digunakan oleh tokoh dalam event tersebut.
- Contoh: e48 (Umar Abdul Aziz) → QS. An-Nahl (16): 90 — ayat yang beliau gunakan menggantikan cacian Ali di mimbar ✅
- Contoh: e57 (Al-Khwarizmi) → QS. An-Nisa (4): 11 — hukum waris yang memotivasi pengembangan aljabar ✅
- Contoh: e34 (Pengumpulan Mushaf) → QS. Al-Taubah (9): 128 — ayat terakhir yang ditemukan Zaid ✅

**Tier 2 — Korelasi Tematik Kuat**
Ayat yang temanya langsung relevan dengan inti event, meskipun bukan asbabun nuzul.
- Contoh: e34 → QS. Al-Hijr (15): 9 — janji pemeliharaan Quran, event: pengumpulan mushaf ✅
- Contoh: e75 (Salahuddin) → QS. Al-Isra (17): 1 — isra miraj ke Masjidil Aqsa, event: pembebasan Yerusalem ✅
- Contoh: e78 (Jatuhnya Cordoba) → QS. Ali Imran (3): 103 — berpegang teguh pada persatuan ✅

**Tier 3 — Korelasi Tematik Lemah (HINDARI)**
Ayat umum yang bisa ditempelkan ke event apa saja. **Lebih baik tanpa kutipan daripada memaksakan.**
- ❌ QS. Taha (20): 114 "Rabbi zidni ilma" untuk setiap event pendidikan
- ❌ QS. Al-Hujurat (49): 13 "keragaman bangsa" untuk setiap event multikultural
- ❌ QS. Al-Anfal (8): 60 "siapkan kekuatan" untuk setiap event militer

**Aturan kutipan:**
1. **Tier 1 wajib dikutip** jika ada — ini yang paling berharga
2. **Tier 2 boleh dikutip** — tapi HARUS jelaskan korelasinya dalam 1-2 kalimat setelah ayat
3. **Tier 3 JANGAN dikutip** — ganti dengan hadits relevan, atau hikmah tanpa dalil
4. **Event tanpa Tier 1/2 → boleh tanpa kutipan ayat** — hadits saja cukup, atau penutup hikmah tanpa dalil
5. **Satu ayat TIDAK BOLEH dipakai di >3 events berbeda** — cari alternatif jika sudah 3x
6. Setiap kutipan WAJIB disertai penjelasan korelasi historis/tematik (bukan sekadar "ayat ini mengingatkan kita")

**Anti-pattern (REJECT):**
- ❌ Ayat pernikahan (Ar-Rum 30:21) untuk event politik/peradaban
- ❌ Ayat tentang ruh (Al-Isra 17:85) untuk event non-tasawuf
- ❌ Satu ayat "catch-all" ditempel di banyak event tanpa konteks spesifik
- ❌ Penjelasan korelasi yang dipaksakan: "Ayat ini mencerminkan filosofi X dalam Y" tanpa basis historis

---

### Format Teks Arab

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

### Pemisah Ayat — WAJIB Konsisten

Teks Arab sudah menggunakan pemisah ayat ornamental `﴿N﴾`. **Terjemahan HARUS mengikuti pola yang sama** — setiap akhir ayat diberi pemisah `﴿N﴾` agar pembaca bisa mencocokkan terjemahan dengan ayat Arab.

**❌ SALAH — terjemahan tanpa pemisah:**
```
"Did He not find you an orphan and give you refuge? And He found you lost 
and guided you. And He found you in need and made you self-sufficient."
```

**✅ BENAR — terjemahan dengan pemisah per ayat:**
```
"Did He not find you an orphan and give you refuge? ﴾6﴿ And He found you 
lost and guided you. ﴾7﴿ And He found you in need and made you 
self-sufficient. ﴾8﴿"
```

**Aturan:**
- Terjemahan (LTR) menggunakan `﴾N﴿` dengan angka Western (1, 2, 3...) — bracket terbalik agar render `{N}` di teks kiri-ke-kanan
- Teks Arab (RTL) tetap menggunakan `﴿N﴾` dengan Arabic numerals: `﴿١﴾ ﴿٢﴾ ﴿٣﴾`
- Untuk kutipan 1 ayat saja, pemisah TETAP wajib: `"...give you refuge? ﴾6﴿"`
- Posisi pemisah: SETELAH tanda baca akhir kalimat ayat (setelah titik/tanya/seru)

**⚠️ JANGAN TERTUKAR:**
- `﴿N﴾` = untuk teks Arab (RTL) → tampil benar di RTL
- `﴾N﴿` = untuk terjemahan ID/EN (LTR) → tampil benar di LTR

### ⛔ HANYA untuk Ayat Al-Quran — Lesson Learned (2026-03-20)

Pemisah ayat `﴾N﴿` **HANYA** boleh ada di ayat Al-Quran. **DILARANG** di:
- ❌ Hadits (HR Bukhari, Muslim, Tirmidzi, dll)
- ❌ Dialog historis (percakapan sahabat, raja, dll)
- ❌ Kutipan dari kitab sirah/tarikh
- ❌ Narasi atau komentar ulama

**Cara membedakan:**
- Ayat Quran → diawali teks Arab + referensi `QS.` → ✅ pakai `﴾N﴿`
- Hadits → referensi `HR.` / nama perawi / kitab hadits → ❌ JANGAN
- Dialog → tanda kutip dalam narasi tanpa referensi QS → ❌ JANGAN

**Identifikasi otomatis:** Pemisah ayat HANYA boleh muncul di baris yang diawali `>` (blockquote markdown). Baris non-blockquote TIDAK BOLEH mengandung `﴾N﴿`.

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

### 📖 Al-Qur'an al-Karim sebagai Sumber Pustaka (WAJIB)

Jika artikel mengutip ayat Al-Qur'an (referensi `QS.`), maka **Al-Qur'an al-Karim WAJIB masuk sebagai entry di Daftar Pustaka**.

**Format entry:**
```
N. Al-Qur'an al-Karim. QS. [Nama Surah 1] ([Nomor]): [Ayat]; QS. [Nama Surah 2] ([Nomor]): [Ayat].
```

**Contoh:**
```
6. Al-Qur'an al-Karim. QS. al-Isra' (17): 1; QS. al-Baqarah (2): 190.
```

**Aturan:**
- Entry ini mencakup SEMUA ayat yang dikutip di artikel — dikumpulkan dalam 1 entry
- Letakkan sebagai entry TERAKHIR di daftar pustaka
- Di body text, setiap blockquote ayat Quran HARUS memiliki sitasi `^N` yang merujuk ke entry ini
- Ayat yang hanya direferensikan inline (tanpa blockquote) tetap harus tercantum di entry ini
- **WAJIB** — artikel yang punya `QS.` refs tapi TIDAK punya entry Al-Qur'an di pustaka = **REJECT**
- **SETIAP surah HARUS ditulis lengkap**: `QS. [Nama Surah] ([Nomor]): [Ayat]` — TIDAK BOLEH terpotong
  - ❌ `QS. Ali` → ✅ `QS. Ali Imran (3): 152`
  - ❌ `QS. Al-Anfal` → ✅ `QS. Al-Anfal (8): 60`
  - ❌ `QS. Maryam` → ✅ `QS. Maryam (19): 1–3`
- **SEMUA surah yang dikutip di body HARUS tercantum di entry** — jika body kutip 2 surah, entry harus punya 2 surah
- **1 entry only** — TIDAK BOLEH ada 2 entry Al-Qur'an al-Karim di Daftar Pustaka = **REJECT**

### Card Sources — Al-Qur'an Format (WAJIB)

Card di `events-database.json` juga HARUS menggunakan format lengkap:

```json
{
  "id": "qs-al-fil-quraisy",
  "title": "Al-Quran al-Karim",
  "author": "QS. Al-Fil (105): 1-5, QS. Quraisy (106): 1-4",
  "type": "quran"
}
```

**Aturan card:**
- `author` field HARUS mencantumkan SEMUA surah yang dikutip di artikel
- Setiap surah di `author` HARUS format lengkap: `QS. [Nama] ([Nomor]): [Ayat]`
- ❌ `"author": "QS. Ali"` → ✅ `"author": "QS. Ali Imran (3): 64"`
- Card harus sinkron dengan markdown Daftar Pustaka
- **HANYA 1 entry Al-Qur'an per artikel** — jika ada duplikat (2+ entry Al-Qur'an), hapus yang format lama dan keep yang format lengkap
- **Nama surah TIDAK BOLEH terpotong**: ❌ `QS. Ali` → ✅ `QS. Ali Imran (3): 64` — harus lengkap dengan nomor surah dan ayat dalam parentheses
- **Format wajib**: `Al-Qur'an al-Karim. QS. [Nama Lengkap] ([Nomor]): [Ayat]` — tanpa parentheses/nomor = REJECT

### 🚫 5 Violation Types (Auto-Reject)

| # | Violation | Contoh | Severity |
|---|-----------|--------|----------|
| V1 | **Pustaka tanpa sitasi** — entry di daftar pustaka yang tidak pernah di-cite di body | Pustaka #5 ada tapi ^5 tidak muncul di teks | REJECT |
| V2 | **Sitasi tanpa pustaka** — superscript di body yang mengarah ke entry yang tidak ada | ^8 di teks tapi pustaka cuma 6 entry | REJECT |
| V3 | **Duplikat pustaka** — sumber yang sama muncul >1x di daftar pustaka | Ibn Hisham muncul di #1, #4, #7 | REJECT |
| V4 | **Pustaka <3 entries** — terlalu sedikit, kurang triangulasi | Hanya 1-2 sumber | REJECT |
| V5 | **Sitasi ⁰ (nol)** — nomor sitasi harus mulai dari 1 | ^0 di teks | REJECT |
| V6 | **Duplikat Al-Qur'an entry** — lebih dari 1 entry Al-Qur'an di daftar pustaka, atau nama surah terpotong | 2 entry "Al-Qur'an al-Karim" atau "QS. Ali" tanpa "(3): 64" | REJECT |
| V7 | **Penjelasan ayat tanpa sitasi Al-Qur'an** — paragraf setelah blockquote ayat Al-Quran HARUS cite ke entry Al-Qur'an al-Karim | Paragraf "Ayat ini mencerminkan..." punya ^3 (Ibn Arabshah) tapi tidak punya ^5 (Al-Quran) | REJECT |
| V8 | **Ayat tidak relevan (Tier 3)** — ayat generik yang bisa ditempel ke event apa saja, tanpa korelasi historis | QS. Ar-Rum 30:21 (pernikahan) di event politik Kesultanan Demak | REJECT |
| V9 | **Ayat overused** — ayat spesifik yang sama dipakai di >3 events berbeda | QS. Al-Hujurat 49:13 di 7 events | REJECT — cari alternatif |

### Self-Check Sebelum Submit

Sebelum menyerahkan file, penulis WAJIB melakukan self-check:

```
CHECKLIST SITASI:
□ Hitung jumlah entry di Daftar Pustaka → minimal 3, consolidated (1 entry = 1 karya unik)
□ Untuk SETIAP entry #N → cari ^N atau ⁿ di body → harus ada minimal 1x
□ Untuk SETIAP ^N di body → cek entry #N ada di Daftar Pustaka
□ Cek tidak ada 2 entry yang merujuk kitab/buku yang SAMA
□ V7: Paragraf SETELAH blockquote ayat Al-Quran → HARUS punya ^N yang merujuk entry Al-Qur'an al-Karim
□ V8: Ayat yang dikutip → cek Tier (1=asbabun nuzul, 2=tematik kuat, 3=HINDARI). Tier 3 = REJECT
□ V9: Ayat yang dikutip → cek apakah sudah dipakai di >3 events lain. Jika ya → cari alternatif
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
- Daftar pustaka HANYA dari markdown content (bukan dari JSON `event.sources`)
- **Setiap paragraf fakta historis HARUS punya minimal 1 sitasi** — paragraf tanpa sitasi = klaim tanpa sumber

### ⚠️ Posisi Sitasi (BLOCKER)

Sitasi HARUS setelah tanda baca akhir kalimat, BUKAN sebelumnya:

- ✅ `kalimat selesai.^1` — titik LALU sitasi
- ✅ `kalimat selesai.^1 ^2` — multiple citation setelah titik
- ❌ `kalimat selesai^1.` — sitasi LALU titik = **REJECT**
- ❌ `kalimat selesai^1` — tanpa titik di akhir kalimat = **perlu diperbaiki**

**Pola regex untuk detect violation:** `[^.\s>]\^\d+\.(\s|$)` — jika match > 0, file REJECT.

---

## 4. Children Mode — Slideshow Format

- **Format**: Popup slideshow presentation (fullscreen modal)
- **Visual**: Ilustrasi gambar dominan per slide, dark gradient overlay di bawah untuk teks
- **Slide count**: Per section 2-3 slide, total ~8-16 slide per event
- **Navigasi**: Swipe/arrow, progress dots
- **Teks**: Selectable & copyable di atas overlay

### Gaya Penulisan Anak-Anak (CRITICAL)

**Prinsip utama**: Informasi ringkas untuk anak, BUKAN gaya mendongeng. Orang tua yang menarasikan dengan ekspresi masing-masing.

**❌ DILARANG:**
- Sapaan langsung: "Teman-teman", "Friends", "Tahukah kamu?", "Do you know?"
- Ajakan berimajinasi: "Bayangkan...", "Imagine...", "Coba pikirkan..."
- Nada presenter/pendongeng: "Nah, sekarang kita lihat...", "And just like that..."
- Exclamation berlebihan di tengah teks: "Wow!", "Subhanallah!" (boleh 1x di penutup)
- Kalimat retoris: "Hebat, bukan?", "Amazing, right?"

**✅ YANG BENAR:**
- Langsung ke informasi: "Pada tahun 570 M, di Yaman ada seorang raja bernama Abrahah."
- Kronologis dan faktual: "Abu Thalib membawa Muhammad ke Syam untuk berdagang."
- Kalimat pendek, jelas, tidak bertele-tele
- Konteks lengkap tapi diringkas — jangan skip informasi penting
- Boleh emotif tapi melalui fakta: "Anak-anak menangis kelaparan. Tangisan mereka terdengar dari luar lembah." (fakta yang menyentuh, bukan "Kasihan sekali ya teman-teman!")

**Contoh SALAH vs BENAR:**
| ❌ Salah | ✅ Benar |
|----------|---------|
| "Teman-teman, bayangkan ada seorang anak..." | "Muhammad berusia dua belas tahun saat Abu Thalib bersiap pergi berdagang ke Syam." |
| "Wow, ternyata Bahira tahu lho!" | "Bahira mengenali tanda kenabian pada Muhammad." |
| "Dan begitulah, teman-teman!" | "Abu Thalib segera membawa Muhammad pulang ke Makkah." |
| "Hebat sekali bukan? Subhanallah!" | "Subhanallah." (1x di penutup) |

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

## 6. Data Consistency — JSON Card ↔ Markdown

### Card Data (`events-database.json → sources[]`)

Setiap event WAJIB memiliki card data di `events-database.json` yang sinkron dengan markdown Daftar Pustaka.

**Format card entry:**
```json
{
  "id": "ibn-hisham",
  "title": "Al-Sirah al-Nabawiyyah",
  "author": "Ibn Hisham",
  "type": "primary"
}
```

**Type values:**
- `primary` — kitab sirah, tarikh, biografi
- `hadith` — kitab hadits (Bukhari, Muslim, dll)
- `quran` — Al-Qur'an al-Karim

**Al-Qur'an card entry (WAJIB jika ada ayat dikutip):**
```json
{
  "id": "qs-al-fil-quraisy",
  "title": "Al-Quran al-Karim",
  "author": "QS. Al-Fil, Quraisy",
  "type": "quran"
}
```

**Referensi format**: Lihat **e01** (Tahun Gajah) sebagai contoh card data yang lengkap dan benar.

**Aturan sinkronisasi:**
- `events-database.json` (`event.sources[]`) = versi ringkas (card)
- Markdown `## Daftar Pustaka` = versi lengkap (artikel)
- **Keduanya HARUS sinkron** — setiap sumber di markdown harus ada di JSON, dan sebaliknya
- Ketika rich content tersedia → halaman detail pakai markdown bibliography (bukan card)
- Card tetap diperlukan sebagai: (1) fallback jika markdown belum ada, (2) data untuk filtering/search, (3) preview di timeline/map popup
- **Event tanpa card data = REJECT** — sama pentingnya dengan event tanpa markdown content

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

### ⚠️ Language Purity (BLOCKER)

**`general-id.md` HARUS 100% Bahasa Indonesia.** Tidak boleh ada kata/frasa Inggris yang tercampur.

**❌ DILARANG (English contamination):**
- `systematically menghancurkan` → ✅ `secara sistematis menghancurkan`
- `implementing kebijakan` → ✅ `menerapkan kebijakan`
- `strategic effort untuk eliminate` → ✅ `upaya strategis untuk menghapus`
- `conquest Granada` → ✅ `penaklukan Granada`
- `despite persecution` → ✅ `meskipun ada penganiayaan`

**Yang BOLEH tetap English/asing:**
- Nama tokoh: Cardinal Cisneros, Philip III
- Nama tempat: Granada, Al-Andalus, Iberia
- Istilah teknis yang sudah lazim: *Moriscos*, *convivencia*, *Aljamiado*
- Istilah Arab: *takwa*, *ummah*, *hijrah*

**`general-en.md` HARUS 100% English.** Sama — tidak boleh ada Indonesian contamination.

**File yang gagal language check = REJECT.** Sub-agent harus rewrite.

### Format QS. (Konsisten — BLOCKER)

Format referensi surah HARUS konsisten:
- ✅ `QS. Al-Fil (105): 1-5` — dengan titik, spasi, nomor surah terpisah dari ayat
- ❌ `QS Al-Fil (105:1-5)` — tanpa titik, ayat di dalam parentheses
- ❌ `QS. Al-Fil` — tanpa nomor surah dan ayat

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

### ⛔ QA Gate — WAJIB Sebelum Push (BLOCKER)

**Setiap push ke develop/main HARUS didahului QA check.** Tidak ada exception.

**Kapan QA WAJIB dijalankan:**
- Setelah content generation (batch baru)
- Setelah expand/edit artikel
- Setelah fix script (V6 fix, renumber, dll)
- Setelah sub-agent selesai kerja — **SELALU audit hasilnya sebelum push**

**QA gate flow:**
```
Sub-agent selesai → Main agent jalankan QA → PASS → push
                                            → FAIL → fix → re-QA → PASS → push
```

**Jika skip QA → artikel bermasalah masuk develop → harus revert. JANGAN skip.**

### Sub-Agent Brief — WAJIB Embed V1-V9 (Lesson Learned 2026-03-26)

Setiap brief untuk sub-agent Researcher/Editor **HARUS menyertakan ringkasan V1-V9 rules** dalam brief-nya. Sub-agent tidak baca docs sendiri secara reliable — rules harus di-embed langsung.

**Minimum yang harus ada di brief:**
```
RULES WAJIB:
- V1: Setiap entry pustaka HARUS di-cite di body (tidak boleh ada pustaka hantu)
- V2: Setiap ^N di body HARUS punya entry di pustaka (tidak boleh orphan)
- V3: Tidak boleh duplikat pustaka (1 sumber = 1 entry, reuse nomor)
- V4: Min 3 pustaka consolidated
- V5: Sitasi mulai dari ^1 (tidak boleh ^0)
- V6: Jika ada QS. → Al-Quran al-Karim WAJIB di pustaka, format lengkap
- V7: Paragraf setelah blockquote ayat HARUS cite ke entry Al-Quran
- V8: Ayat harus Tingkatan 1/2, TIDAK BOLEH Tingkatan 3 (generik)
- V9: Satu ayat max 3 events
- FORMAT: .^N (titik LALU sitasi), BUKAN ^N.
- BAHASA: general-id.md 100% Indonesia, general-en.md 100% English
```

**Tanpa embed ini → sub-agent PASTI melanggar** (terbukti dari 11 issue hari ini).

### Post-Expand/Edit QA — MANDATORY (Lesson Learned 2026-03-26)

Setelah expand artikel atau edit besar (>50% perubahan), **WAJIB jalankan audit berikut:**

1. **Citation bijection**: V1 (unused bib) + V2 (orphan refs) — via `scripts/fix-v1-v2-citations.py`
2. **Language purity**: cek English contamination di general-id.md
3. **Quran citation**: V7 (explanation cite Al-Quran) — via script
4. **Duplicate pustaka**: V3 — via dedup script
5. **Card sync**: jalankan `scripts/fix-card-quran-refs.py`

**Urutan fix jika ada masalah:**
```
1. Fix V1+V2 (bijection) → renumber
2. Fix V3 (dedup) → renumber
3. Fix V7 (Quran citation)
4. Fix language
5. Sync card
6. Rebuild content JSON
7. Push
```

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

**Checks:** V1-V5 (sitasi dasar), V6 (duplikat/truncated Al-Quran), V7 (penjelasan ayat tanpa cite Al-Quran), V8 (ayat Tier 3), V9 (ayat overused >3x), ID↔EN section count, children slide count, file completeness.

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
- [ ] **V6**: Jika ada referensi `QS.` di body → Al-Qur'an al-Karim WAJIB ada sebagai entry di Daftar Pustaka. Tidak boleh duplikat. Nama surah lengkap: `QS. [Nama] ([N]): [Ayat]`
- [ ] **V7**: Paragraf setelah blockquote ayat → HARUS punya `^N` ke entry Al-Qur'an (bukan hanya cite sumber sirah)
- [ ] **V8**: Ayat yang dikutip harus Tier 1 (asbabun nuzul) atau Tier 2 (tematik kuat). Tier 3 (generik) = REJECT
- [ ] **V9**: Satu ayat spesifik tidak boleh muncul di >3 events. Cek `ayat_usage` sebelum tambah ayat baru
- [ ] Sitasi reuse — sumber sama = nomor SAMA (bukan nomor baru)
- [ ] Detail bab/halaman di inline text, BUKAN di entry pustaka
- [ ] Setiap paragraf klaim historis punya minimal 1 sitasi

### B. Konten (per event)
- [ ] Teks Arab HANYA di Quran/Hadits — BUKAN di istilah/nama/tempat
- [ ] Ayat Quran: teks Arab + nomor ayat ﴿N﴾ + terjemahan
- [ ] Hadits: nomor hadits + kitab/bab
- [ ] Referensi format: `— QS. [Nama] (nomor): ayat` / `— HR [Perawi], no. [nomor], [Kitab]`
- [ ] Setiap blockquote ada keterangan sumber di baris terakhir
- [ ] JSON `event.sources[]` sinkron dengan markdown
- [ ] Diksi sesuai panduan (Section 8)
- [ ] Tidak ada artefak: `>`, `<`, `*`, `|` yang tidak ter-render
- [ ] Markdown `# Judul` ada (metadata) tapi di-skip renderer

### B. Children Mode (per event)
- [ ] 4 bagian/sections dengan tone informatif-ringan (BUKAN dongeng)
- [ ] Brief ilustrasi 🎨 lengkap 6 elemen per section
- [ ] Tidak ada tabel — gunakan list/visual cards

### C. Layout & Styling (halaman detail)
- [ ] Badges: Era + Kategori + Wilayah + Signifikansi + Tahun (fontSize 11, borderRadius 14)
- [ ] Judul `<h1>` di bawah badges
- [ ] Tokoh: label + pills (fontSize 12) — utama + pendukung
- [ ] Teks Arab: font Amiri, RTL, **tidak italic**
- [ ] Daftar pustaka: tidak dobel

### D. Data Sync — Konten + Card
- [ ] `docs/content/events/` = `projects/baitul-hikmah/content/events/` (identik)
- [ ] `event-content-map.json` di-rebuild
- [ ] `events-database.json` — figures + sumber sinkron
- [ ] **Card data** (`events-database.json → sources[]`):
  - [ ] Setiap event punya `sources[]` yang tidak kosong (min 3 entries)
  - [ ] Format: `{id, title, author, type}` — type = `primary` | `hadith` | `quran`
  - [ ] Jika markdown kutip ayat Quran → card WAJIB punya entry `type: "quran"` dengan `title: "Al-Quran al-Karim"`
  - [ ] Card sources sinkron dengan markdown Daftar Pustaka (jumlah dan sumber cocok)
  - [ ] **Referensi**: e01 sebagai contoh card format yang benar

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
- Tone: same informational level (not storytelling)

---

## 10. Bilingual Sync Rule (CRITICAL)

> **Lesson Learned 2026-03-21**: Edit `children-en.md` tanpa edit `children-id.md` → website tampil 12 slides (ID) padahal EN sudah 11.

**SETIAP edit konten WAJIB dilakukan di KEDUA bahasa secara bersamaan:**
- `children-en.md` ↔ `children-id.md`
- `general-en.md` ↔ `general-id.md`

**Checklist sebelum commit:**
- [ ] Jumlah section EN = ID
- [ ] Jumlah paragraf per section EN ≈ ID (boleh beda sedikit, tapi slide count harus sama)
- [ ] Jika merge/split paragraf di EN → lakukan hal yang sama di ID
- [ ] Run slide count check di KEDUA bahasa sebelum push

**Cara cek slide count:**
```bash
# EN
node -e "..." content/events/{event}/children-en.md
# ID  
node -e "..." content/events/{event}/children-id.md
# Keduanya HARUS sama
```

---

## 11. Pre-Deploy QA Checklist

> Run SEBELUM setiap push ke develop/main. FAIL = JANGAN push.
> Single checklist untuk SEMUA aspek: artikel, konten anak, ilustrasi, build.

### A. Article Content (General Mode)
- [ ] **Struktur**: Pembuka → Narasi kronologis → Analisis → Penutup → Daftar Pustaka
- [ ] **Sitasi bijection**: setiap ^N ↔ entry #N (no orphans di kedua sisi)
- [ ] **Min 3 pustaka** consolidated (1 entry = 1 karya unik)
- [ ] **Setiap paragraf historis** min 1 sitasi
- [ ] **Teks Arab** HANYA di Quran/Hadits — bukan istilah/nama/tempat
- [ ] **Ayat Quran**: Arab + `﴾N﴿` + terjemahan (blockquote only)
- [ ] **Ayat Quran — Hierarki**: Tier 1 (asbabun nuzul) > Tier 2 (tematik kuat) > Tier 3 (HINDARI). Ayat yang sama tidak boleh muncul di >3 events. Penjelasan korelasi WAJIB ada setelah kutipan.
- [ ] **Hadits**: nomor hadits + kitab/bab (bukan hanya "HR Muslim")
- [ ] **`﴾N﴿` bersih**: `grep -rn '﴾[0-9]*﴿' | grep -v '^.*:>'` → 0 results

### B. Children Content (Slideshow Mode)
- [ ] **Slide count EN = ID** — parser output IDENTICAL di kedua bahasa
- [ ] **Slide count = image count** = `EventContent.tsx` length
- [ ] **Tone informatif-ringan** — informasi ringkas untuk anak 6-12 tahun, BUKAN gaya mendongeng
- [ ] **Emoji per section** — setiap `## ` punya emoji representatif
- [ ] **Brief ilustrasi** — setiap section diakhiri `🎨 Brief Ilustrasi` / `🎨 Illustration Brief`
- [ ] **Setiap slide scene unik** — 2 slide bersebelahan tidak boleh visual identik

### C. Illustrations
- [ ] **Image size** ~1-2MB per slide (bukan 8-10MB raw Gemini)
- [ ] **Resolution** ~1024px width, RGB (match e01/e02)
- [ ] **Nabi = golden glow ONLY** — no human figure, no child shape, no silhouette
- [ ] **No text in images** — zero text/labels/captions
- [ ] **Karakter konsisten** — sesuai `illustration-registry.md` (beard, robe, age)
- [ ] **Safe zone** — subjects centered 70%

### D. Build & Data
- [ ] **`node scripts/build-content.js`** → rebuild `event-content-map.json`
- [ ] **Rebuild `event-content-map.json`** dari event-content-map.json
- [ ] **Kedua JSON committed** — CF Pages hanya run `next build`
- [ ] **`next build` success** — no errors

### E. Post-Deploy Verification
- [ ] **Buka halaman event** di dev → klik Mode Anak-Anak
- [ ] **Slide count** di pojok kiri atas = expected
- [ ] **Toggle ID ↔ EN** → slide count sama di kedua bahasa
- [ ] **Semua slide punya gambar** — no broken images
- [ ] **Verse separators** tampil `{N}` di terjemahan (bukan `}N{`)
- [ ] **Artikel general** — scroll, cek format Quran/Hadits, sitasi clickable
