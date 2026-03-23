# Batch Image Generation Workflow v4

> **Status: ✅ PROVEN** (2026-03-22) — Smooth sequential flow via PinchTab
> **Created**: 2026-03-22
> **Based on**: v3 lessons + working session E04

---

## Perubahan dari v3

| Aspek | v3 | v4 |
|-------|----|----|
| Chat strategy | Placeholder chats [1]-[16] | **New Chat per slide** (navigate fresh each time) |
| Placeholder chats | Required, slide N = chat [N] | **Not used for generation** — old history causes snapshot hang |
| Navigate | Stay in Gemini | **Navigate fresh** `gemini.google.com/app` between each slide |
| Download verify | `ls -t \| head -1` (buggy, grabs old file) | **Before/After filename comparison** (waits for NEW file) |
| Sidebar | Toggle Main Menu | **Skip sidebar** — use fresh page textbox directly |
| Timing | Wait 5s before send | **Wait 7s** before send (safer margin) |

---

## Pre-requisites

- [ ] PinchTab instance `work` running + logged in Google
- [ ] Prompt files ready: `/workspace/tmp/{event}-prompts/slide-{01..NN}.txt`
- [ ] Briefs loaded: `docs/image-briefs-children.md`
- [ ] Character registry loaded: `docs/illustration-registry.md`
- [ ] Shared volume mounted: `/workspace/shared/pinchtab-downloads/` ↔ container `/home/pinchtab/Downloads/`

---

## Core Rules

1. **New Chat per slide** — navigate fresh to `gemini.google.com/app` each time
2. **Wait 7 seconds** after typing before clicking Send
3. **Before/After download** — record latest file BEFORE download, wait until NEW file appears
4. **Lightbox download** — hover → click image → lightbox opens → click "Download full size image"
5. **Close lightbox** before next slide
6. **Max 750 chars per prompt** — Gemini UI hides Send button beyond this. Sweet spot: 650-750 chars
7. **Compress after download** — Gemini raw = ~9MB. Target: 1-2MB via sharp resize + PNG compression

## Batch & QA Flow

Setiap event dibagi menjadi batches (adjust per total slides):

| Example (12 slides) | Slides | Setelah generate |
|---------------------|--------|-----------------|
| Batch 1 | slide 01-04 | Send preview → Ahmad QA → **tunggu approval** |
| Batch 2 | slide 05-08 | Send preview → Ahmad QA → **tunggu approval** |
| Batch 3 | slide 09-12 | Send preview → Ahmad QA → **tunggu approval** |

**Rules:**
- ❌ JANGAN lanjut ke batch berikutnya sebelum Ahmad approve
- Jika revisi → regenerate slide yang bermasalah → kirim ulang
- Approved slides → `cp` ke project + `git push develop`

---

## Phase 0: Preparation (MANDATORY before ANY generation)

### 0.1: Read Registry + Brief
```bash
# WAJIB baca — bukan optional
cat docs/illustration-registry.md | head -50   # character descriptions
cat docs/briefs/{event}.md                      # episode brief + character lock
cat docs/illustration-guide.md | head -30       # rules
```

### 0.2: Generate Prompt Files from Brief
Setiap slide → 1 prompt file. Format WAJIB:

```
[STYLE LOCK - DO NOT MODIFY]
Warm watercolor storybook illustration for children age 6-12.
Image ratio: 16:9 landscape. Resolution: 1792x1024.
Stylized watercolor, soft edges. Center 70%.
NO text. NO black borders.

[CHARACTER LOCK - from registry, DO NOT PARAPHRASE]
GOLDEN GLOW: a small warm circular golden-white light, about 15%
of image height, with 5-7 soft rays radiating outward. NOT a halo,
NOT concentric rings, NOT a column. A ball of golden light like a
small sun.
{other characters from brief Character Lock section}

[SCENE]
{scene description from brief}
```

Save to: `/workspace/tmp/{event}-prompts/slide-{NN}.txt`

### 0.3: Pre-Generate Checklist
```bash
EVENT="e04-pernikahan-khadijah"  # change per event

echo "=== PRE-GENERATE CHECKLIST ==="

# 1. Prompt files exist?
echo "Prompt files:"
ls /workspace/tmp/*-prompts/slide-*.txt | wc -l

# 2. All prompts within 750 chars?
echo "Over 750 chars:"
for f in /workspace/tmp/*-prompts/slide-*.txt; do
    chars=$(wc -c < "$f")
    if [ "$chars" -gt 750 ]; then echo "⚠️ $(basename $f): $chars chars"; fi
done

# 3. Golden glow exact wording in all relevant prompts?
echo "Missing golden glow standard:"
grep -L "5-7 soft rays" /workspace/tmp/*-prompts/slide-*.txt 2>/dev/null

# 4. No shell-breaking chars?
echo "Shell-breaking chars:"
grep -l "[()']" /workspace/tmp/*-prompts/slide-*.txt 2>/dev/null

echo "=== CHECKLIST COMPLETE ==="
```

**If ANY check fails → FIX before generating. Do NOT skip.**

### 0.4: Ahmad Reviews Prompt Files
Send prompt files to Ahmad for approval before generation.
**JANGAN generate sebelum Ahmad approve prompts.**

### 0.5: Golden Glow Batch Strategy
- Count how many slides have golden glow
- If >3 slides → generate ALL golden glow slides in **1 chat session** for style consistency
- Non-golden-glow slides → can use New Chat per slide

---

## Workflow per Slide

### Flow (proven, copy-paste safe):

```bash
BEFORE_FILE=$(ls -t /workspace/shared/pinchtab-downloads/Gemini_Generated_Image_*.png 2>/dev/null | head -1)
echo "Before: $(basename $BEFORE_FILE)"

# 1. Navigate fresh
bash /workspace/scripts/pinchtab.sh nav "https://gemini.google.com/app" 2>/dev/null; sleep 5

# 2. Find textbox
TEXTBOX=$(bash /workspace/scripts/pinchtab.sh snap 2>/dev/null | python3 -c "
import sys,json
for n in json.load(sys.stdin).get('nodes',[]):
    if n.get('role')=='textbox': print(n['ref']); break
")

# 3. Type prompt
PROMPT=$(cat /workspace/tmp/{event}-prompts/slide-{NN}.txt | tr '\n' ' ')
bash /workspace/scripts/pinchtab.sh type "$TEXTBOX" "$PROMPT"
echo "Typed. Waiting 7s..."
sleep 7

# 4. Click Send
SEND=$(bash /workspace/scripts/pinchtab.sh snap 2>/dev/null | python3 -c "
import sys,json
for n in json.load(sys.stdin).get('nodes',[]):
    if 'send message' in n.get('name','').lower(): print(n['ref']); break
")
bash /workspace/scripts/pinchtab.sh click "$SEND"
echo "=== SUBMITTED ==="

# 5. Poll for image (every 15s, max 8 attempts = 2 min)
for attempt in $(seq 1 8); do
    sleep 15
    HAS_IMG=$(bash /workspace/scripts/pinchtab.sh snap 2>/dev/null | python3 -c "
import sys,json
print(sum(1 for n in json.load(sys.stdin).get('nodes',[]) if 'ai generated' in n.get('name','').lower()))
")
    echo "Poll $attempt: images=$HAS_IMG"
    if [ "$HAS_IMG" -gt 0 ] 2>/dev/null; then break; fi
done

# 6. Download via lightbox
IMG=$(bash /workspace/scripts/pinchtab.sh snap 2>/dev/null | python3 -c "
import sys,json
for n in json.load(sys.stdin).get('nodes',[]):
    if 'ai generated' in n.get('name','').lower(): print(n['ref'])
" | tail -1)

bash /workspace/scripts/pinchtab.sh api POST /action "{\"kind\":\"hover\",\"ref\":\"$IMG\"}" 2>/dev/null; sleep 2
bash /workspace/scripts/pinchtab.sh click "$IMG"; sleep 5

DL=$(bash /workspace/scripts/pinchtab.sh snap 2>/dev/null | python3 -c "
import sys,json
for n in json.load(sys.stdin).get('nodes',[]):
    if 'download' in n.get('name','').lower(): print(n['ref']); break
")
bash /workspace/scripts/pinchtab.sh click "$DL"

# 7. Wait for NEW file (before/after comparison)
for i in $(seq 1 20); do
    sleep 3
    AFTER_FILE=$(ls -t /workspace/shared/pinchtab-downloads/Gemini_Generated_Image_*.png 2>/dev/null | head -1)
    if [ "$AFTER_FILE" != "$BEFORE_FILE" ]; then
        cp "$AFTER_FILE" /workspace/tmp/{event}-slide-{NN}.png
        echo "SAVED: $(basename $AFTER_FILE)"
        break
    fi
    echo "Wait... ($i)"
done

# 8. Close lightbox
bash /workspace/scripts/pinchtab.sh snap 2>/dev/null | python3 -c "
import sys,json
for n in json.load(sys.stdin).get('nodes',[]):
    if n.get('name','').lower()=='close': print(n['ref']); break
" | xargs -I{} bash /workspace/scripts/pinchtab.sh click {} 2>/dev/null
echo "=== DONE ==="
```

### Multi-slide batch (chain slides sequentially):

Between slides, update `BEFORE_FILE` to the latest downloaded file:
```bash
BEFORE_FILE="$AFTER_FILE"  # or re-read: BEFORE_FILE=$(ls -t ... | head -1)
```

---

## Post-Download: Compression (MANDATORY)

Gemini downloads = ~9MB (2752x1536). Target = **1-2MB** (match E01 size).

**After downloading ALL slides in a batch**, compress before push:

```bash
cd /workspace/projects/baitul-hikmah
node -e "
const sharp = require('sharp');
const fs = require('fs');
const event = 'e04'; // change per event
const slides = fs.readdirSync('public/illustrations/children/')
    .filter(f => f.startsWith(event + '-slide-') && f.endsWith('.png'));

(async () => {
    for (const file of slides) {
        const src = 'public/illustrations/children/' + file;
        const info = await sharp(src).metadata();
        const needsResize = info.width > 1792;
        let pipeline = sharp(src);
        if (needsResize) pipeline = pipeline.resize(1792, 1024, {fit: 'cover'});
        pipeline = pipeline.png({compressionLevel: 9});
        await pipeline.toFile(src + '.tmp');
        fs.renameSync(src + '.tmp', src);
        const stat = fs.statSync(src);
        console.log(file + ': ' + (stat.size/1048576).toFixed(1) + 'MB');
    }
})();
"
```

**Target sizes**: 1.0-1.8MB per slide (same as E01)

---

## Prompt Guidelines

- **Max 750 chars** — Gemini UI hides Send button on longer prompts. Sweet spot: 650-750 chars
- **NEVER paraphrase character descriptions** — copy-paste EXACT from registry/brief Character Lock
- **NEVER write prompts from memory** — always read brief file first
- **Always include**: style, shot type, century/era, colors with hex, mood, ratio, NO text, NO black borders
- **Em dash** `—` → replace with `--` (causes shell errors)
- **No parentheses** `()` in prompts — breaks shell. Use commas instead
- **No single quotes** `'` in prompts — breaks shell. Use double dashes or rephrase
- **Character descriptions**: copy from `docs/illustration-registry.md`
- **Golden glow rule**: "small subtle golden circular glow with gentle rays -- about 15% of image height"
- **6th century consistency**: always mention "mud-brick", "stone walls", "oil lamp", "clay pots", "woven mats"

### Prompt template:
```
Create an image: Warm watercolor storybook illustration for children age 6-12. [SHOT TYPE]. [SETTING in 6th century pre-Islamic Mecca/Arabia]. [SCENE DESCRIPTION]. [CHARACTER DESCRIPTIONS]. Colors: [warm cream (#fdf6e3), soft gold (#d4a574), earthy brown (#8b6914)]. [LIGHTING]. Mood: [MOOD]. Soft edges, stylized watercolor. Center 70%. Image ratio: 16:9 landscape. Resolution: 1792x1024. NO text. NO black borders.
```

---

## Timing Reference

| Step | Duration |
|------|----------|
| Navigate + load | ~5s |
| Type prompt (~700 chars) | ~15-20s |
| Wait before Send | 7s |
| Image generation | 15-30s (poll every 15s) |
| Lightbox open + download | ~5s + 10-25s wait |
| **Total per slide** | **~60-90s** |
| **4 slides** | **~5-6 min** |

---

## Download Verification (CRITICAL)

**The bug**: `ls -t | head -1` returns the same file if download hasn't completed yet, causing duplicate saves.

**The fix**: Before/After filename comparison.

```bash
# BEFORE download
BEFORE_FILE=$(ls -t /workspace/shared/pinchtab-downloads/Gemini_Generated_Image_*.png | head -1)

# ... click download ...

# AFTER — loop until NEW file appears
for i in $(seq 1 20); do
    sleep 3
    AFTER_FILE=$(ls -t /workspace/shared/pinchtab-downloads/Gemini_Generated_Image_*.png | head -1)
    if [ "$AFTER_FILE" != "$BEFORE_FILE" ]; then
        # New file! Copy it.
        break
    fi
done
```

**Between slides**: update `BEFORE_FILE` to prevent stale comparison:
```bash
BEFORE_FILE="$AFTER_FILE"
```

---

## Error Recovery

| Issue | Solution |
|-------|----------|
| Send button hidden | Prompt >750 chars. Sweet spot 650-750. Shorten or type space. |
| Snapshot hangs | Gemini page too heavy. Navigate to `about:blank` then back. |
| "ai generated" not found | Image still generating. Wait 30s more. Or Gemini refused — check screenshot. |
| Download timeout (20 attempts) | Lightbox method failed. Try: navigate back to chat, re-open lightbox. |
| Session expired | Re-login: `docker exec -it pinchtab sh -c 'read -sp "Password: " PW && echo && echo "$PW" | python3 /tmp/login.py'` |
| Textbox not found | Sidebar overlay. Click "New Chat" button or navigate fresh. |

---

## Lessons Learned (from v1-v3)

| Issue | Root Cause | v4 Fix |
|-------|-----------|--------|
| Duplicate downloaded files | `ls -t \| head -1` grabs same file | Before/After filename comparison |
| Placeholder chat context pollution | Old prompts influence new output | Fresh New Chat each time |
| Snapshot JSON parse error (19K chars) | Heavy chat history | Navigate fresh, skip placeholder chats |
| Sidebar placeholder refs empty | Gemini sidebar truncates/collapses | Skip sidebar, use main page textbox |
| Prompt submitted too fast | Brief terpotong | Wait 7s after type, verify Send button exists |
| Style inconsistency | Missing era/architecture details | Always include "6th century", "mud-brick", "stone walls" |
| Golden glow too large | No size constraint in prompt | Specify "about 15% of image height" |

---

## Checklist per Event

### Pre-Generate (MANDATORY)
- [ ] Read `illustration-registry.md` — character descriptions
- [ ] Read `briefs/{event}.md` — episode brief + character lock
- [ ] Read `illustration-guide.md` — rules & larangan
- [ ] Prompt files generated with STYLE LOCK + CHARACTER LOCK format
- [ ] Pre-generate checklist script passed (chars ≤750, golden glow wording, no shell chars)
- [ ] Ahmad approved prompt files
- [ ] Golden glow slides identified → same-chat batch strategy

### Generate
- [ ] PinchTab logged in (check for "Sign in" link)
- [ ] Golden glow slides generated in 1 chat session
- [ ] Non-golden-glow slides via New Chat per slide
- [ ] All files downloaded + verified (before/after filename)
- [ ] All files compressed to 1-2MB via sharp

### Post-Generate
- [ ] Preview per batch sent to Ahmad
- [ ] Ahmad reviewed — revisions done
- [ ] Files copied to `public/illustrations/children/{event}/`
- [ ] `git commit` + `git push origin develop`
- [ ] All batches approved → ready for production merge
