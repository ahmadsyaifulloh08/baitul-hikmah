# Batch Image Generation Workflow v3

> **Status: ⚠️ REVISED** — Root cause ditemukan (2026-03-22): bukan PinchTab yang gagal, tapi **prompt di-submit terlalu cepat** — Gemini belum selesai menerima input sehingga brief terpotong → gambar random. **Fix: tunggu minimal 5 detik setelah input sebelum klik Send.**
> **Created**: 2026-03-21
> **Based on**: v2 (proven 2026-03-20) + lessons learned 2026-03-21

---

## Perubahan dari v2

| Aspek | v2 | v3 |
|-------|----|----|
| Chat strategy | Placeholder reuse | **New chat per slide** (zero context) |
| Submit method | Parallel burst | **Sequential** (submit → verify → download → next) |
| QA timing | Per batch (5 slides) | **Per event** (semua slides sekaligus) |
| Slide count | Manual count (section) | **Parser-verified** (exact paragraph count) |
| Placeholder chats | Required [1]-[10] | **Not used for generation** (reserved for revisi only) |

---

## Pre-requisites

- [ ] PinchTab instance `work` running + logged in Google (viewport 1440x900)
- [ ] Prompt files siap di `/workspace/tmp/{event}-prompts/slide-{01..NN}.txt`
- [ ] PRD illustration rules loaded (`docs/illustration-guide.md`)
- [ ] Character registry loaded (`docs/illustration-registry.md`)

---

## Core Rules

1. **New chat per slide** — zero context, prompt-only generation
2. **Jumlah prompt = jumlah slide dari parser** — bukan jumlah section
3. **Generate ALL slides → review ALL at once** — 1 event = 1 review cycle
4. **Revisi via new chat** — retype adjusted prompt, bukan append ke chat lama
5. **Max 16 slides per event** — sesuai PRD

---

## Workflow

### Phase 0: Persiapan Konten

**0.1: Hitung Jumlah Slide (WAJIB PERTAMA)**

Sebelum apapun, hitung exact slide count dari parser. JANGAN asumsi dari jumlah section atau brief.

```bash
cd /workspace/projects/baitul-hikmah
node -e "
const content = require('fs').readFileSync('content/events/{event}/children-en.md','utf8');
const sections = content.split(/\n---\n/).filter(s=>s.trim());
let total = 0;
sections.forEach((sec,i) => {
  const paras = sec.split('\n\n').filter(p => {
    const t = p.trim();
    return t && !t.startsWith('#') && !t.startsWith('>') && !t.startsWith('---') && t.length > 20;
  });
  total += paras.length;
  console.log('Section', i+1, ':', paras.length, 'slides');
});
console.log('TOTAL:', total, 'slides');
"
```

Output ini = jumlah prompt yang harus ditulis. Konfirmasi ke Ahmad sebelum lanjut.

**0.2: Load References**
```
1. docs/illustration-guide.md — rules (golden glow, no text, safe zone, 16:9)
2. docs/illustration-registry.md — characters, locations, palettes, prompt template
3. content/events/{event}/children-en.md — narasi + illustration briefs
```

**0.3: Verify Slide Count matches Parser (CRITICAL)**

Run parser to get EXACT slide count — 1 section can have 2-3 slides (per paragraph):

```bash
cd /workspace/projects/baitul-hikmah
node -e "
const content = require('fs').readFileSync('content/events/{event}/children-en.md','utf8');
const sections = content.split(/\n---\n/).filter(s=>s.trim());
let total = 0;
sections.forEach((sec,i) => {
  const paras = sec.split('\n\n').filter(p => {
    const t = p.trim();
    return t && !t.startsWith('#') && !t.startsWith('>') && !t.startsWith('---') && t.length > 20;
  });
  total += paras.length;
  console.log('Section', i+1, ':', paras.length, 'slides');
});
console.log('TOTAL:', total, 'slides');
"
```

**0.4: Map Slides to Scenes**

List setiap slide dan narasi paragrafnya:

```bash
node -e "
const content = require('fs').readFileSync('content/events/{event}/children-en.md','utf8');
const sections = content.split(/\n---\n/).filter(s=>s.trim());
let num = 1;
sections.forEach((sec,i) => {
  const paras = sec.split('\n\n').filter(p => {
    const t = p.trim();
    return t && !t.startsWith('#') && !t.startsWith('>') && !t.startsWith('---') && t.length > 20;
  });
  paras.forEach((p,j) => {
    console.log('SLIDE ' + num + ': ' + p.trim().substring(0,100));
    num++;
  });
});
"
```

**0.5: Write Prompts**
- 1 file per slide: `/workspace/tmp/{event}-prompts/slide-{NN}.txt`
- WAJIB include per prompt:
  - Character descriptions dari registry (exact wording, COPY-PASTE)
  - Setting dari location registry
  - Shot type (establishing/wide/medium/close-up)
  - `"NO text anywhere"` closing
- **Max ~700 chars** — longer prompts may hide Gemini's Send button

---

### Phase 1: Sequential Generation — New Chat per Slide

**Flow per slide:**
```
For i = 1 to N:
  1. Click "New chat" → fresh empty chat (ZERO context)
  2. Type prompt from slide-{i}.txt into textbox
  3. Wait for "Send message" button → click (or auto-sent via type)
  4. Wait ~60-90s for image generation (poll for "AI generated" node)
  5. Download image via lightbox (hover → click image → lightbox → download)
  6. Verify file appeared in /workspace/shared/pinchtab-downloads/
  7. Repeat for next slide
```

**Estimated time**: ~2-3 min per slide
- 6 slides ≈ 15 min
- 13 slides ≈ 30-35 min
- 16 slides ≈ 40-48 min

**Script**: `python3 /workspace/tmp/generate-sequential.py {event} {start} {end}`

**Key technical details:**
- Use `type` (NOT `fill`) — fill doesn't trigger Gemini input events
- Em dash (—) → replace with `--` before typing
- After download, close lightbox before clicking New chat
- Always pick LAST "AI generated" node (new chats should only have 1, but safety check)

---

### Phase 2: QA — Full Event Composite Review

After ALL slides generated:

```
1. Generate composite grid image (ALL slides in 1 image):
   node /workspace/scripts/composite-preview.js \
     --event {event} --slides 1-{N} --output /workspace/tmp/{event}-composite.jpg

2. Send composite to Ahmad via Telegram — 1 event = 1 review

3. Ahmad reviews ALL slides at once:
   - Which slides are OK ✅
   - Which need revision ❌ + feedback

4. Revisi: new chat → adjusted prompt → download → replace file

5. Re-generate composite → re-send → review until all approved

6. Final approval → proceed to deploy
```

**Prinsip: 1 event = 1 review cycle.** Generate semua, review barengan, revisi yang perlu.

---

### Phase 3: Deploy

```bash
# Copy files to project
cp /workspace/tmp/{event}-slides/*.png \
   /workspace/projects/baitul-hikmah/public/illustrations/children/

# Update EventContent.tsx slide count if needed
# Build
cd /workspace/projects/baitul-hikmah && npm run build

# Commit + push develop
git add public/illustrations/children/{event}-slide-*.png
git commit -m "{event}: add {N} illustration slides"
git push origin develop

# Ahmad review di develop.baitul-hikmah.pages.dev
# OK → merge to main (production)
```

---

## Composite Preview Tool

```bash
# Full event
node /workspace/scripts/composite-preview.js --event e10 --slides 1-13 --output /workspace/tmp/e10-composite.jpg

# Custom files
node /workspace/scripts/composite-preview.js \
  --files img1.png,img2.png --labels "Slide 1,Slide 2" --output preview.jpg

# Custom grid columns (default 4)
node /workspace/scripts/composite-preview.js --event e10 --slides 1-13 --cols 4 --output preview.jpg
```

---

## Technical Notes

### New Chat = Zero Context (CRITICAL)
- **JANGAN** reuse Placeholder chats untuk generate baru — old context pollutes results
- Gemini generates based on chat history + new prompt → old images influence new output
- New chat = prompt-only = reliable results
- Placeholder chats [1]-[16] hanya untuk **revisi** (append adjusted prompt ke chat yang sama)

### PinchTab Type Method
- **Use `type` (NOT `fill`)** — fill doesn't trigger Gemini framework events
- Em dash `—` → replace with `--` (causes shell SyntaxError)
- Type is char-by-char (~15-20s for 600 char prompt)
- After typing, Send button should appear; if not, type a space to trigger it

### Lightbox Download Method
1. Find `"AI generated"` node → pick **LAST one** (newest)
2. Hover on image → wait 2s
3. Click image → lightbox opens (2 nodes: `Close` + `Download full size image`)
4. Click `Download full size image`
5. Wait 15s for file in `/workspace/shared/pinchtab-downloads/`
6. Close lightbox before next action

### Sidebar Management
- Gemini sidebar collapses after navigating to/from chats
- Toggle: click `Main menu` button
- After lightbox close, may need to re-toggle sidebar
- New chat button sometimes only available as `link` (not `button`)

### Error Recovery
- 500 errors on click → retry up to 3 times with 5s delay
- Lightbox stuck → find and click `Close` button
- No textbox after New chat → close lightbox first, then retry New chat

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Old chat context → wrong scene | **New chat per slide** (zero context) |
| Wrong image downloaded | Always pick LAST "AI generated" node |
| Gemini rate limit | Sequential = natural throttle (~2-3 min gap) |
| Send button hidden | Keep prompt ≤700 chars; type space if needed |
| PinchTab `fill` fails on Gemini | Always use `type` |
| Sidebar collapses | Re-toggle Main menu; close lightbox first |
| Browser cache on review | Hard refresh / incognito |

---

## Checklist per Event

- [ ] Slide count verified via parser
- [ ] All prompt files ready (`/workspace/tmp/{event}-prompts/slide-*.txt`)
- [ ] Character descriptions copy-pasted from registry
- [ ] ALL slides generated sequentially (new chat per slide)
- [ ] All files downloaded + renamed
- [ ] Full composite generated + sent to Ahmad
- [ ] Ahmad reviewed — revisions done
- [ ] Files copied to project
- [ ] Build successful
- [ ] Pushed to develop → Ahmad reviewed live
- [ ] Merged to main (production)

---

## Lessons Learned (2026-03-21)

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| Wrong scene generated (e03 instead of e10) | Placeholder chat retained old context | New chat per slide |
| Downloaded old image instead of new | Clicked first image, not last | Always pick LAST AI generated node |
| Sidebar collapses after actions | Gemini responsive behavior | Re-toggle Main menu after each action |
| Generate gambar random (anak + kucing) | Chat context too noisy | New chat = zero context |
| Send button hidden | Prompt too long | Keep ≤700 chars |
| `fill` doesn't submit | Gemini custom contenteditable | Use `type` only |
| Lightbox blocks all interactions | Lightbox overlay captures all clicks | Always close lightbox before next action |
| Slide count wrong (6 vs 13) | Counted sections, not paragraphs | Use parser to count exact slides |
| **Gambar tidak sesuai brief** | Prompt di-submit terlalu cepat — Gemini belum selesai menerima input, brief terpotong | **Tunggu minimal 5 detik** setelah paste/type prompt sebelum klik Send. Gemini butuh waktu memproses input panjang. |
