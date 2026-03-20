# Illustration Guide — Baitul Hikmah Children Mode

> Panduan generate & QA ilustrasi slideshow anak-anak.
> Extracted from PRD Section 16.
>
> **Related docs:**
> - **[Illustration Registry](illustration-registry.md)** — ⭐ BACA PERTAMA. Characters, locations, time palettes, scene rules, prompt template
> - [Batch Workflow v2](operations/batch-image-generation-v2.md) — ✅ PROVEN parallel generation workflow
> - [PinchTab Image Pipeline](operations/pinchtab-image-pipeline.md) — single image step-by-step
> - [Image Briefs](image-briefs-children.md) — prompt per event/slide
> - [Design Guide](design-guide.md) — color system, moodboard per era

---

## 1. Larangan Visualisasi Nabi Muhammad ﷺ (MUTLAK)

| ❌ DILARANG | ✅ BOLEH |
|-------------|---------|
| Wajah Nabi (realistis/kartun) | Lafadz/kaligrafi "Muhammad" |
| Tubuh Nabi (detail/outline) | Cahaya/nur keemasan (bukan bentuk manusia) |
| Siluet tubuh Nabi | Simbol non-manusia (bintang terang, sinar langit) |
| Sosok dari belakang | Objek terkait (tongkat, sandal — tanpa sosok) |
| Bayangan berbentuk manusia | Lingkungan/setting tanpa figur Nabi |
| Anak kecil yang merepresentasikan Nabi | Efek cahaya yang menunjukkan kehadiran |

### Konsistensi Cahaya Muhammad ﷺ

**Bentuk standar:** Cahaya emas bersinar (golden radiant glow) — lingkaran cahaya emas dengan sinar-sinar lembut (rays). Warm golden-white, ~15-20% tinggi gambar.

**WAJIB konsisten di SEMUA slide** — bentuk, warna, ukuran sama. Tidak boleh variasi (column/ribbon/burst).

**Prompt standar:**
> "Muhammad's presence is represented as a GOLDEN RADIANT GLOW — a circular warm golden-white light with gentle rays emanating outward in all directions, like a small warm sun. This representation MUST be identical in style across all slides."

---

## 2. No Text in Image (MUTLAK)

Semua ilustrasi **TIDAK BOLEH mengandung text** apapun:
- ❌ Caption, judul, label, watermark, signature
- ❌ Text dalam bahasa apapun

**Prompt WAJIB include:**
> "CRITICAL: Do NOT include ANY text, words, letters, labels, captions, titles, signatures, or writing of any kind in the image."

Jika QA menemukan text → **BLOCKER**, wajib regenerate.

---

## 3. No Black Borders (MUTLAK)

Gambar HARUS mengisi canvas 100% edge-to-edge. Tidak boleh ada black bars/letterbox/padding.

---

## 4. Safe Zone Composition (MUTLAK)

Subjek utama di **CENTER 70%** gambar. Edge akan ter-crop pada berbagai viewport (`object-fit: cover`).

**Prompt WAJIB include:**
> "COMPOSITION: Place all important subjects within the CENTER 70% of the image. Leave outer edges clear of important details."

**Image Ratio:** 16:9 landscape (1792×1024). Prompt WAJIB include: `"Image ratio: exactly 16:9 landscape (wide). Resolution: 1792x1024."`

**Mobile UX:** Hint "Putar HP untuk pengalaman terbaik 📱🔄" saat portrait (4 detik, fade out).

---

## 5. Setiap Slide = Gambar Unik

1 slide = 1 ilustrasi unik. Tidak boleh duplikat antar slide, meskipun section sama.

---

## 6. Fullscreen Display

- Container: `100vw × 100vh`
- Gambar: `object-fit: cover`
- Tidak ada border, shadow, rounded corners

---

## 7. Text Overlay

- **Gradient**: bawah ke atas (`linear-gradient(to top, ...)`)
- **Bawah**: `rgba(0,0,0,0.75)` (solid untuk teks terbaca)
- **Atas**: transparan (gambar tetap terlihat)
- **Tinggi overlay**: ~40-45% dari tinggi slide
- **Teks**: putih/krem, readable, selectable/copyable

---

## 8. Brief Ilustrasi — Format Standar

**6 Elemen Wajib per Brief:**

| # | Elemen | Contoh |
|---|--------|--------|
| 1 | **Setting/Latar** | "Kota Sana'a, gereja al-Qullays yang megah" |
| 2 | **Karakter & Pose** | "Abrahah berdiri di balkon, wajah sombong" |
| 3 | **Objek Kunci** | "Ka'bah bersinar keemasan di kejauhan" |
| 4 | **Warna Dominan** | "Emas, cokelat gurun, langit biru cerah" |
| 5 | **Suasana/Mood** | "Dramatis tapi tidak menyeramkan" |
| 6 | **Komposisi** | "Kontras: kekuatan besar vs ketenangan iman" |

**Format dalam markdown:**
```markdown
> **🎨 Brief Ilustrasi:**
> *[Deskripsi lengkap 6 elemen]*
```

**Contoh BENAR:**
```
> **🎨 Brief Ilustrasi:**
> *Gajah Mahmud berlutut menolak maju, ratusan burung ababil di langit
> membawa batu kecil. Ka'bah berdiri kokoh bersinar keemasan. Suasana
> dramatis tapi aman untuk anak.*
```

**Contoh SALAH:**
```
[Ilustrasi: Seorang anak menggembala domba.]
```
❌ Tidak ada warna, mood, komposisi, detail karakter

---

## 9. End-to-End Pipeline (MANDATORY)

### Phase 0: Content Authoring

```
0.1: TULIS NARASI (children-id.md) → tone dongeng, 2-5 kalimat per slide
0.2: SIMULASI SLIDE SPLIT → jalankan audit-slides.js, verifikasi jumlah
0.3: TULIS IMAGE BRIEF → 1 brief per slide (bukan per section!)
     Brief berdasarkan NARASI SLIDE (hasil split)
```

### Phase 1: Image Generation

```
1.1: GENERATE per brief via Gemini
     Setiap prompt include: safe zone + no text + prophet rule + 16:9
1.2: SLIDE ↔ IMAGE MAPPING AUDIT (WAJIB)
     Buat tabel: Slide N → Narasi → Gambar → Match?
     Jangan asumsikan urutan generate = urutan slide!
```

```bash
# Single image
python3 scripts/pinchtab-gemini-single.py --prompt-file /tmp/prompt.txt --output e03-slide-01

# Batch (auto-extract briefs dari children-id.md)
python3 scripts/pinchtab-gemini-batch.py --event e03
```

> **Pipeline docs:**
> - [`docs/operations/pinchtab-image-pipeline.md`](operations/pinchtab-image-pipeline.md) — single image step-by-step
> - [`docs/operations/batch-image-generation-v2.md`](operations/batch-image-generation-v2.md) — **✅ PROVEN** batch workflow (parallel generation via named Gemini chats, composite QA, post-batch evaluation)

### Phase 2: QA (MANDATORY sebelum deploy)

**Checklist per gambar:**

| Check | Severity | Rule |
|-------|----------|------|
| A. Larangan Nabi ﷺ | **BLOCKER** | Tidak ada fisik/siluet manusia represent Nabi |
| B. Kesesuaian narasi | **BLOCKER** | Scene gambar match teks slide |
| C. Konsistensi visual | WARNING | Karakter sama terlihat konsisten |
| D. Technical | WARNING | 16:9, resolusi cukup, no artefak |
| E. No text in image | **BLOCKER** | Zero text elements |
| F. Safe zone | **BLOCKER** | Subjek di center 70%, no cut heads |

**Verdict:**
- ✅ PASS → siap deploy
- ❌ FAIL (A/B/E/F) → WAJIB regenerate
- ⚠️ WARNING (C/D) → deploy tapi catat untuk fix

**Max 3 retry per gambar** — jika tetap gagal, escalate ke Ahmad.

**QA Method:** Vision model inspect gambar + brief + checklist.

### Automated QA Pipeline

```
Image generated → qa-images.py audit (per event)
       │
  ┌─── PASS ───→ Deploy to public/illustrations/
  │
  └─── FAIL ───→ Categorize violations
                       │
                  ┌─── BLOCKER (A/B/E/F) ───→ Spawn Doc Designer (regenerate brief)
                  │                                    │
                  │                              re-generate → re-audit
                  │                                    │
                  │                              max 3 retry → 🚨 Ahmad
                  │
                  └─── WARNING (C/D) ───→ Deploy + log for batch fix
```

**Script: `scripts/qa-images.py`**

```bash
# Audit semua ilustrasi
python3 scripts/qa-images.py

# Audit event tertentu
python3 scripts/qa-images.py e01 e02

# Output JSON
python3 scripts/qa-images.py --json
```

**Checks per gambar:**

| Check | Method | Severity |
|-------|--------|----------|
| A. Nabi ﷺ depiction | Vision model: "Is there a human figure representing Prophet Muhammad?" | BLOCKER |
| B. Narasi match | Vision model: compare image scene vs slide text | BLOCKER |
| C. Text in image | Vision model: "Does the image contain any text/writing/captions?" | BLOCKER |
| D. Safe zone | Vision model: "Is the main subject centered with no cut heads/limbs at edges?" | BLOCKER |
| E. Aspect ratio | Programmatic: check 16:9 ± tolerance | WARNING |
| F. Resolution | Programmatic: min 1280x720 | WARNING |
| G. Visual consistency | Vision model: compare with other slides same event | WARNING |

**Auto-fix spawning:**
- BLOCKER fail → Main agent spawns Doc Designer with fix brief:
  - Include: original brief, violation type, image path, what to fix
  - Doc Designer regenerates image with corrected prompt
- Max 3 retry per image. If still FAIL → escalate to Ahmad with violation screenshot.
- WARNING only → deploy anyway, log to `qa-report.json` for batch fix later.

**Vision model integration:**
- Uses OpenClaw `image` tool to inspect each generated illustration
- Prompt template per check type (stored in script)
- Binary PASS/FAIL per check, aggregated per image

---

## 10. Konsistensi Visual Antar Slide

- Karakter sama → pakaian, warna, proporsi konsisten
- Objek sama → bentuk dan warna konsisten
- Style artistik → satu event = satu style
- Color palette → mengikuti moodboard era (lihat `design-guide.md`)
- Prompt: sertakan deskripsi karakter identik di setiap slide

---

## 11. Narasi QA — Children Mode

**Checklist per slide:**
- [ ] Min 2 kalimat, maks 4-5 kalimat
- [ ] Storyline mengalir logis antar slide
- [ ] Tone dongeng konsisten (naratif, bukan eksplanatif)
- [ ] Setiap slide punya konteks visual BERBEDA (bisa digambar unik)
- [ ] Slide yang konteksnya mirip → pertimbangkan gabung

### Slide Split Verification (WAJIB sebelum brief)
```
1. Simulasi split (audit-slides.js)
2. Per slide: apakah scene visual unik? Bisa digambar berbeda dari sebelumnya?
3. 2 slide bersebelahan scene sama → GABUNG
4. 1 slide terlalu panjang → SPLIT dengan scene berbeda
5. Jumlah slide final = jumlah gambar
```

---

## 12. Lessons Learned

### Sentence Splitter Memotong Referensi Hadits
- Titik di `no.` dianggap akhir kalimat → potong referensi hadits
- Fix: placeholder char `\uFFFC` untuk abbreviasi sebelum split
- Rule: titik penutup di SETELAH referensi: `"kutipan" (HR Bukhari, no. 2262).`

### AI Images Sering Ada Text
- Gemini suka tambah caption/judul meski tidak diminta
- Fix: prompt anti-text eksplisit + QA checklist E

### Image-Narasi Mismatch dari Sequential Mapping
- Urutan generate ≠ urutan slide
- Fix: WAJIB buat remap plan setelah generate batch

### Kepala Terpotong di Viewport Berbeda
- `object-fit: cover` crop edge → kepala hilang
- Fix: safe zone center 70% + 16:9 wajib (bukan fix di CSS)

### Slide Redundan
- 2 slide scene visual sama → mubazir
- Fix: verifikasi slide split, gabung jika scene sama

### Full Batch Regeneration = Risiko
- Regenerate semua 27 → kualitas menurun
- Fix: SELEKTIF — hanya regenerate yang bermasalah. Selalu backup.

### Docker Copy Container Name
- Container OpenClaw = `openclaw-gateway` (bukan `openclaw`) untuk `docker cp`
- PinchTab downloads dir: `/home/pinchtab/Downloads/Gemini_Generated_Image_*.png`
