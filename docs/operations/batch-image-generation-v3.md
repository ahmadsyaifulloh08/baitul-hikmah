# Batch Image Generation Workflow v3

> **Status: 📝 DRAFT** — belum proven, perlu testing.
> **Created**: 2026-03-21
> **Based on**: v2 (proven 2026-03-20) + Ahmad's hybrid batch idea
> **Key change**: 16 Placeholder chats, Slide N = Chat [N], hybrid 5+5+6 batching

---

## Perubahan dari v2

| Aspek | v2 | v3 |
|-------|----|----|
| Placeholder chats | 10 ([1]-[10]) | 16 ([1]-[16]) |
| Mapping | Manual tabel (chat → slide) | **Fixed: Slide N = Chat [N]** |
| Batch strategy | Full sequential (1-by-1) | **Hybrid 5+5+6 burst** |
| Max paralel | ~7-10 natural | **5 controlled** |
| QA timing | Setelah semua selesai | **Per batch (mid-batch QA)** |
| Revisi | Cari chat mana → bingung | **Langsung ke Chat [N]** |
| Cadangan chat | [8]-[10] reserved | **Tidak ada cadangan — semua mapped** |

---

## Pre-requisites

- [ ] PinchTab instance `work` running + logged in Google
- [ ] 16 chat Gemini: `[1] Placeholder - Image Generation` s/d `[16] Placeholder - Image Generation`
- [ ] Prompt files siap di `/workspace/tmp/{event}-prompts/slide-{01..NN}.txt`
- [ ] PRD illustration rules loaded (`docs/illustration-guide.md`)
- [ ] Character registry loaded (`docs/illustration-registry.md`)

---

## Core Rules

1. **Slide N = Chat [N]** — no exceptions, no mapping table needed
2. **Max 16 slides per event** — sesuai PRD
3. **Revisi slide N → regenerate di Chat [N]** — same chat, append prompt
4. **1 batch = 1 event** — selesai event, clear chats jika perlu

---

## Workflow

### Phase 0: Persiapan Konten

**0.1: Load References**
- `docs/illustration-guide.md` — illustration guidelines
- `docs/illustration-registry.md` — character descriptions (COPY-PASTE, jangan paraphrase)
- `docs/content-style-guide.md` — tone & style
- `content/events/{event}/children-en.md` — konten anak + illustration briefs

**0.2: Verify Slide Count**
- Hitung jumlah slide dari children content (1 section = 2-3 slides)
- Pastikan ≤16 slides
- Map setiap slide ke scene description

**0.3: Write Prompts**
- 1 file per slide: `/workspace/tmp/{event}-prompts/slide-{NN}.txt`
- Setiap prompt WAJIB include:
  - Character descriptions dari registry (exact wording)
  - Setting dari location registry
  - Shot type (establishing/wide/medium/close-up/over-shoulder)
  - Time of day + palette
  - `"NO text anywhere"` closing

**Prompt length**: ≤1000 chars recommended (Gemini hides Send button on long prompts)

---

### Phase 1: Batch Submit — Hybrid 5+5+6

**Kenapa hybrid**: 
- 5 paralel = proven safe (tested 7 on v2, no rate limit)
- Burst rapid submit → wait → QA → next batch
- Mid-batch QA = catch issues early, don't waste all 16

#### Batch 1: Slides 1-5

```
For i = 1 to 5:
  1. Navigate to Gemini main page
  2. Click sidebar: "[i] Placeholder - Image Generation"
  3. Wait 5s (page load)
  4. Type prompt dari slide-{i}.txt ke textbox
  5. Click "Send message" (atau type triggers it)
  6. DON'T wait — immediately next chat
```

**Estimated time**: ~2.5 min (5 chats × 30s)

#### Wait + Download Batch 1

```
  7. Wait 3 min (parallel generation)
  8. Download 5 images via lightbox method:
     For i = 1 to 5:
       - Navigate to Chat [i]
       - Hover → Click image → Lightbox → Download
       - Wait 15s for file
  9. Rename: Gemini_*.png → {event}-slide-{i}.png
```

**Estimated time**: ~5.5 min (3 wait + 2.5 download)

#### Mid-Batch QA 1 — Composite Review

```
  10. Generate composite grid image (5 thumbnails in 1 image):
      - Resize each to ~420x236 (16:9 thumbnail)
      - Grid layout: 1 row × 5 cols (or 2 rows if needed)
      - Label each cell: "Slide N" + color code
      - Labels: 🟢 green = new, 🔵 blue = shifted, ⬛ grey = unchanged
  11. Send composite to Ahmad via Telegram
  12. Ahmad review: "OK lanjut" / "revisi slide X"
  13. If revisi → regenerate di Chat [X], re-download, update composite
```

**Composite script**: `node /workspace/tmp/composite-preview.js`
- Input: list of image paths + labels
- Output: single JPG grid image
- Uses sharp (from baitul-hikmah/node_modules)

#### Batch 2: Slides 6-10

Same flow as Batch 1, using Chats [6]-[10].

#### Mid-Batch QA 2

Same composite flow as QA 1. Send grid of slides 6-10 to Ahmad.

#### Batch 3: Slides 11-16 (or remaining)

Same flow, using Chats [11]-[16].
Skip unused chats if event has <16 slides.

#### Final QA — Full Composite

```
  1. Generate FULL composite grid (ALL slides in 1 image):
     - Grid layout: 4 cols × N rows
     - Label: "Slide N — [scene brief]"
     - Color code: 🟢 approved, 🟡 pending, 🔴 needs revision
  2. Send full composite to Ahmad
  3. Story flow audit: view slides 1→N sequentially
  4. Character consistency check (same character across slides)
  5. Islamic compliance check (golden glow only, no text)
  6. Ahmad final approval → proceed to deploy
```

---

### Phase 2: Download & Assign

Files appear di: `/workspace/shared/pinchtab-downloads/`

```bash
# Rename and copy
mv "Gemini_Generated_Image_XXXXX.png" {event}-slide-{NN}.png
cp {event}-slide-*.png /workspace/projects/baitul-hikmah/public/illustrations/children/
```

**Mapping rule**: Download order = chat visit order = slide order.
No confusion karena Slide N = Chat [N].

---

### Phase 3: Revisi

Revisi jadi simple:

```
Ahmad: "Revisi slide 7 — golden glow terlalu besar"
Agent:
  1. Open Chat [7]
  2. Type revisi prompt
  3. Send → wait → download
  4. Replace slide-07.png
```

Tidak perlu cari-cari chat. Tidak perlu mapping tabel.

---

### Phase 4: Deploy

```bash
# Update EventContent.tsx count if needed
# Build
cd /workspace/projects/baitul-hikmah && npm run build

# Commit + push develop
git add public/illustrations/children/{event}-slide-*.png
git commit -m "{event}: add {N} illustration slides"
git push origin develop

# Ahmad review di develop.baitul-hikmah.pages.dev
# Kalau OK → merge to main (production)
```

---

## Timing Estimates

| Phase | 5 slides | 10 slides | 16 slides |
|-------|:--------:|:---------:|:---------:|
| Prompt prep | ~10 min | ~20 min | ~30 min |
| Batch submit | 2.5 min | 5 min | 8 min |
| Wait (generate) | 3 min | 6 min | 9 min |
| Download | 2.5 min | 5 min | 8 min |
| QA composites | 2 min | 4 min | 6 min |
| **Total (excl. prep)** | **~10 min** | **~20 min** | **~31 min** |

Add ~5-10 min per revision cycle.

---

## Revisi Workflow (Quick Reference)

```
1. Ahmad: "Revisi slide N — [feedback]"
2. Agent: Open Chat [N] di sidebar
3. Agent: Type revisi prompt (incorporate feedback)
4. Agent: Send → wait ~90s → download via lightbox
5. Agent: Replace file → send preview to Ahmad
6. Loop until approved
```

---

## Composite Preview Tool

**Script**: `/workspace/scripts/composite-preview.js`

```bash
# Full event preview (all slides)
node /workspace/scripts/composite-preview.js --event e10 --slides 1-13 --output /workspace/tmp/e10-full.jpg

# Batch 1 preview (slides 1-5)
node /workspace/scripts/composite-preview.js --event e10 --slides 1-5 --output /workspace/tmp/e10-batch1.jpg

# Batch 2 preview (slides 6-10)
node /workspace/scripts/composite-preview.js --event e10 --slides 6-10 --output /workspace/tmp/e10-batch2.jpg

# Custom files
node /workspace/scripts/composite-preview.js --files img1.png,img2.png --labels "Slide 1,Slide 2" --output preview.jpg

# Change grid columns (default 4)
node /workspace/scripts/composite-preview.js --event e03 --slides 1-11 --cols 3 --output preview.jpg
```

**Output**: Single JPG grid image with labeled thumbnails (420×236 per cell).
Send directly to Ahmad via Telegram for quick review.

---

## Technical Notes

### PinchTab Submit Method
- **Use `type` (NOT `fill`)** — fill doesn't trigger Gemini input events
- Em dash (—) causes shell SyntaxError → use Python urllib directly
- Type is char-by-char but reliable (~15-20s for 800 char prompt)

### Lightbox Download Method (MANDATORY)
1. Hover on image button (name contains "AI generated")
2. Click image → lightbox opens (2 nodes: Close + Download)
3. Click "Download full size image"
4. Wait 15s for file in `/workspace/shared/pinchtab-downloads/`
- **JANGAN** click download button langsung di chat — file tidak ter-save

### Snapshot JSON Fix
```python
raw = re.sub(r'[\x00-\x1f]', ' ', raw)  # before json.loads
```

### Chat Navigation
- Always navigate to main page first (`gemini.google.com/app`)
- Then click sidebar chat — refs shift after navigation
- Wait 5s after clicking chat before typing

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Gemini rate limit (5 burst) | Proven safe at 7; 5 is conservative |
| Scene identik meski beda chat | Prompt harus spesifik per scene |
| Send button hidden (long prompt) | Keep prompt ≤1000 chars |
| `fill` doesn't work on Gemini | Always use `type` |
| Chat context influences new prompt | Each chat = clean context per event |
| Download file naming confusion | Slide N = Chat [N] = download order |
| Browser cache on CF Pages | Hard refresh / incognito for review |

---

## Checklist per Event

- [ ] Content children-en.md reviewed + slide count verified
- [ ] Prompt files ready (`/workspace/tmp/{event}-prompts/slide-*.txt`)
- [ ] Character descriptions copy-pasted from registry
- [ ] Batch 1 (1-5): submitted → generated → downloaded → QA'd
- [ ] Batch 2 (6-10): submitted → generated → downloaded → QA'd
- [ ] Batch 3 (11-16): submitted → generated → downloaded → QA'd
- [ ] Full composite QA: approved by Ahmad
- [ ] Story flow audit: passed
- [ ] Islamic compliance: passed
- [ ] Files copied to project
- [ ] Build successful
- [ ] Pushed to develop → Ahmad reviewed
- [ ] Merged to main (production)

---

## Migration from v2

1. v2 chats [1]-[10] masih ada → bisa dipakai, tapi clear history jika mulai event baru
2. Ahmad sudah buat [11]-[16] → total 16 ready
3. Cadangan chat concept removed — semua chat mapped 1:1 ke slides
4. Mapping tabel removed — Slide N = Chat [N] is the rule
