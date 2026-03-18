# PinchTab × Gemini Image Generation — Full Pipeline

> **Status**: ✅ WORKING — end-to-end pipeline verified 2026-03-18
> **Date**: 2026-03-18
> **Instance**: `work` (prof_00e13ed7, port 9868, headless)
> **Target**: Gemini Pro (ahmad@chickin.id) image generation via browser automation
> **First success**: e03-slide-01 (Perjalanan Syam — kafilah unta) — QA PASS

---

## Architecture

```
Agent (container)
    ↓ HTTP API
PinchTab API (pinchtab:9867)
    ↓ CDP
Chrome instance (port 9868, headless, profile=work)
    ↓ HTTPS
gemini.google.com (Gemini Pro, logged in as ahmad@chickin.id)
    ↓ generates
Image (PNG, ~8MB, 2752×1536)
    ↓ click "Download full size image"
/home/pinchtab/Downloads/ (inside PinchTab container)
    ↓ docker cp (via Watchdog terminal)
/workspace/projects/baitul-hikmah/out/illustrations/children/
    ↓ QA (vision model)
/workspace/projects/baitul-hikmah/public/illustrations/children/
    ↓ git push → CF Pages auto-build
https://develop.baitul-hikmah.pages.dev
```

**Key constraints**:
- PinchTab runs inside Docker — headless only (no display)
- Agent container ≠ PinchTab container — file transfer via `docker cp`
- All API calls MUST include `instance` + `tabId` params (wrapper defaults to wrong instance)

---

## Critical: API Call Pattern

**Every** PinchTab API call must include instance + tabId:

```bash
TOKEN=$(wc.get_secret('pinchtab_token', reason))
INST="inst_XXXXXX"   # Changes on restart! Get from /instances
TABID="XXXXXXXXXX"   # Gemini tab ID, stable within session

curl -s -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -X POST "http://pinchtab:9867/action" \
  -d '{"kind":"type","ref":"e23","text":"...","instance":"'$INST'","tabId":"'$TABID'"}'
```

**Without instance+tabId**: commands go to `default` instance (wrong Chrome, wrong login, wrong tab).

---

## Step 1: Login to Google ✅ WORKS

```bash
# Navigate to sign in
POST /navigate {"url":"https://accounts.google.com/signin","instance":"..."}

# Fill email → click Next
POST /action {"kind":"fill","ref":"<email_ref>","text":"ahmad@chickin.id","instance":"...","tabId":"..."}
POST /action {"kind":"click","ref":"<next_ref>","instance":"...","tabId":"..."}

# Fill password → click Next
POST /action {"kind":"fill","ref":"<password_ref>","text":"<from_temp_file>","instance":"...","tabId":"..."}
POST /action {"kind":"click","ref":"<next_ref>","instance":"...","tabId":"..."}
```

**Password handling**: Ahmad creates temp file → agent reads once → Ahmad deletes immediately.

**Session persistence**:
- ✅ Login persists within same headless instance run
- ❌ Login LOST on instance stop/restart
- ❌ Login LOST on headless ↔ headed mode switch
- ⚠️ Google may require 2FA — not always, depends on session

---

## Step 2: Navigate to Gemini ✅ WORKS

```bash
POST /navigate {"url":"https://gemini.google.com/app","instance":"...","tabId":"..."}
```

Get tabId from:
```bash
GET /instances/<inst_id>/tabs
# Find tab with url containing "gemini.google.com"
```

---

## Step 3: Type Prompt ✅ WORKS

```bash
# Get textbox ref from snapshot
GET /snapshot?instance=...&tabId=...
# Look for: role=textbox, name="Enter a prompt for Gemini"

# Type prompt
POST /action {"kind":"type","ref":"<textbox_ref>","text":"<prompt>","instance":"...","tabId":"..."}
```

**What works**: `type` action with explicit instance+tabId targeting
**What DOESN'T work**:
- ❌ `pinchtab.sh type` wrapper → defaults to wrong instance
- ❌ `fill` action → doesn't trigger Gemini's React change detection
- ❌ `press` individual keys → no effect on Gemini's custom textbox
- ❌ JavaScript `evaluate` → disabled in PinchTab (all action kinds rejected)

---

## Step 4: Submit Prompt ✅ WORKS (click Send button)

```bash
# Get send button ref from snapshot
GET /snapshot?instance=...&tabId=...
# Look for: role=button, name="Send message"

# Click send
POST /action {"kind":"click","ref":"<send_ref>","instance":"...","tabId":"..."}
```

**Important**:
- ✅ Click "Send message" button = reliable
- ❌ Press Enter on textbox = unreliable (sometimes Gemini echoes prompt as text)
- Start prompt with "Create an image:" or "Create an image of" to help Gemini recognize image gen intent
- Keep prompts under ~500 chars (long prompts more likely to get text response)
- Use new chat per image to avoid context confusion

---

## Step 5: Wait for Generation ✅ WORKS (polling)

```bash
# Poll every 10-15 seconds
GET /snapshot?instance=...&tabId=...

# Check for completion signals:
# ✅ DONE: role=image, name=", AI generated"
# ✅ DONE: role=button, name="Download full size image"
# ⏳ STILL GENERATING: role=button, name="Stop response"
# ❌ FAILED: no image after 60s, no "Stop response" → retry
```

**Timing**: Image generation takes ~15-45 seconds.
**Detection**: Snapshot polling for `"Download full size image"` button is the most reliable completion signal.

---

## Step 6: Download Image ✅ WORKS

```bash
# Click download button
POST /action {"kind":"click","ref":"<download_ref>","instance":"...","tabId":"..."}

# File saves to: /home/pinchtab/Downloads/Gemini_Generated_Image_XXXXX.png
# (~8MB, 2752×1536, RGBA PNG)
```

**Important**: Download folder is `/home/pinchtab/Downloads/` — NOT `/data/profiles/work/Downloads/`.

---

## Step 7: Copy to Project ✅ WORKS (via Watchdog)

```python
from lib.watchdog_client import WatchdogClient
wc = WatchdogClient(agent='main')

# List downloaded files
tid = wc.request_terminal(
    command="docker exec pinchtab ls -la /home/pinchtab/Downloads/",
    target="host",
    reason="List PinchTab downloaded images"
)
# → Needs Ahmad approval via Telegram

# Copy specific file to project
tid = wc.request_terminal(
    command="docker cp pinchtab:/home/pinchtab/Downloads/Gemini_Generated_Image_XXXXX.png /Users/ahmad/projects/dev/ahadbyte/projects/baitul-hikmah/out/illustrations/children/e03-slide-01.png",
    target="host",
    reason="Copy Gemini image to Baitul Hikmah project"
)

# Clean up downloads after copy
tid = wc.request_terminal(
    command="docker exec pinchtab rm /home/pinchtab/Downloads/Gemini_Generated_Image_XXXXX.png",
    target="host",
    reason="Clean PinchTab downloads after copy"
)
```

**Note**: Watchdog terminal requires Ahmad approval for each command. Batch when possible.

---

## Step 8: QA Image ✅ WORKS (vision model)

```python
# Resize for vision model (max 5MB)
# Original: ~8MB RGBA PNG → convert to JPEG ~500KB
PYTHONPATH=/workspace/lib/pip python3 -c "
from PIL import Image
img = Image.open('out/illustrations/children/e03-slide-01.png')
img.convert('RGB').save('out/illustrations/children/e03-slide-01-qa.jpg', 'JPEG', quality=75)
"

# QA via OpenClaw image tool with checklist:
# A. No Prophet Muhammad depiction (BLOCKER) → only golden radiant glow
# B. Scene matches narasi (BLOCKER)
# C. No text in image (BLOCKER)
# D. Safe zone — subjects in center 70% (BLOCKER)
# E. Aspect ratio 16:9 (WARNING)
# F. Resolution min 1280x720 (WARNING)
# G. Visual consistency (WARNING)

# Max 3 retry per image. If still FAIL → escalate to Ahmad.
```

---

## Step 9: Deploy ✅ WORKS (git push → CF Pages)

```bash
# Copy QA-passed image to public/
cp out/illustrations/children/e03-slide-01.png public/illustrations/children/

# Add illustration mapping in EventContent.tsx
# 'e03-perjalanan-syam': Array.from({length: 4}, (_, i) => `/illustrations/children/e03-slide-${...}.png`)

# Build + push
node scripts/build-content.js
npx tailwindcss -i src/app/globals.css -o public/styles.css --minify
npx next build
git add -A && git commit -m "feat: add e03 illustrations" && git push origin develop

# CF Pages auto-builds from develop branch → https://develop.baitul-hikmah.pages.dev
```

**⚠️ DANGER: Do NOT run `build-content.js` with Python-generated slugs!**
Use Node.js slugify (same as site code) to generate `event-content-map.json`.
Python `re.sub` produces different slugs than JS `.replace(/[^\w\s-]/g, '')` for special chars like `'`.

---

## Lessons Learned

### 1. Instance + TabId Targeting (CRITICAL)
PinchTab wrapper script defaults to `default` instance. Gemini login is on `work` instance.
ALL raw API calls must include `instance` and `tabId` params. Without them, commands go to wrong Chrome.

### 2. Gemini Custom Textbox
Gemini uses a custom Shadow DOM textbox that resists standard DOM manipulation.
Only `type` action works (not `fill`, not `press`, not JS evaluate).

### 3. Submit = Click Send, Not Enter
Enter key on Gemini textbox is unreliable. Always find and click the "Send message" button.

### 4. Download Path
Chrome headless downloads go to `/home/pinchtab/Downloads/`, NOT `/data/profiles/work/Downloads/`.

### 5. JS eval Disabled
PinchTab has "Optional JavaScript evaluation" per docs, but it's disabled by default.
All action kinds (eval, evaluate, js, etc.) return "unknown action kind".
Need to enable in PinchTab server config if we want DOM extraction.

### 6. Login Doesn't Survive Restart
Stopping/restarting PinchTab instance kills the Google session.
Headed ↔ headless switch also kills it. Keep the instance running.

### 7. Image Size
Gemini generates ~8MB RGBA PNG (2752×1536). Too large for vision model QA (max 5MB).
Convert to JPEG with PIL before QA. Keep original PNG for production.

### 8. Slugify Mismatch
Python `re.sub(r'[^a-z0-9]+', '-', title.lower())` ≠ JS `.replace(/[^\w\s-]/g, '')`.
Example: "Syi'b" → Python: `syi-b` | JS: `syib`
Always use Node.js script to generate `event-content-map.json`.

### 9. Content Mapping Architecture
- `content/events/<folder>/` → markdown source files
- `src/data/event-content.json` → folder→content map (build-content.js generates)
- `src/data/event-content-map.json` → slug→content map (Node.js script generates, using JS slugify)
- `EventContent.tsx` → reads both, needs illustration mapping per event

### 10. CF Pages Deploy
Push to `develop` branch → CF Pages auto-builds. No need for wrangler CLI or API token.
`wrangler deploy` from host fails due to platform mismatch (Linux node_modules on macOS).

---

## Prompt Template (Baitul Hikmah Children Illustrations)

```
Create an image of a warm watercolor storybook illustration for children.
[Scene description - 2-3 sentences max]
[Color palette]
[Mood]
Main subjects centered. No text or writing anywhere in the image.
```

**For Prophet Muhammad**: Replace with "a GOLDEN RADIANT GLOW, a circular warm golden-white light with gentle rays like a small sun, representing a blessed young presence"

**Islamic rules (MUTLAK)**:
- ❌ No human figure for Prophet Muhammad — only golden glow
- ❌ No text in image
- ✅ 16:9 landscape, center 70% safe zone
- ✅ Consistent golden glow style across all slides

---

## Files

| Path | Purpose |
|------|---------|
| `prompts/e03-slide-{01..04}.txt` | Prompt files per slide |
| `out/illustrations/children/e03-slide-*.png` | Raw generated images |
| `out/illustrations/children/e03-slide-*-qa.jpg` | QA-compressed versions |
| `public/illustrations/children/e03-slide-*.png` | Production images (served by site) |

---

## Future Improvements

1. **Enable PinchTab JS eval** → extract image URL directly, skip docker cp
2. **Mount shared volume** between PinchTab & OpenClaw containers → direct file access
3. **Set Chrome download path** via launch preferences → predictable location
4. **Gemini API key** → bypass browser entirely for image gen (best long-term)
5. **Automation script** → batch generate all slides in one run
6. **Clean downloads** after copy to prevent disk buildup
