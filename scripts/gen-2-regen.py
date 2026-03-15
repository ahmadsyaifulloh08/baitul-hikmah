#!/usr/bin/env python3
import json, base64, urllib.request, os

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT = "/workspace/projects/baitul-hikmah/public/illustrations/children"

S = """Warm watercolor storybook illustration for children age 6-12. Soft edges, stylized (not photorealistic). Arabian 6th century. Sandy gold, warm beige, dusty earth.
NO text, words, letters, signatures anywhere.
COMPOSITION: TOP 22% and BOTTOM 22% will be CROPPED. Place ALL important subjects (heads, faces, bodies, animals) in the CENTER 56% vertical band. Nothing important at edges."""

IMGS = [
    ("e02-slide-12.png", f"""{S}
Scene: Simple Meccan room. TWO men only:
- Abdul Muthalib (elderly, white beard, white robe) lying on bed/mat on LEFT, reaching out with one hand
- Abu Thalib (younger, brown robe, kind face) standing on RIGHT with hand on heart accepting responsibility
Between them: a small GOLDEN ORB of warm light floating (Muhammad's presence)
Oil lamp on table. Muted warm colors. Simple room.
CRITICAL: Both men's HEADS must be well within center band — NOT near top edge. Abu Thalib's head at ~35% from top, Abdul Muthalib at ~40%.
Muhammad is ONLY the golden orb — NO third person, NO child figure.
Mood: passing of guardianship, solemn trust."""),

    ("e02-slide-14.png", f"""{S}
Scene: Hilltop overlooking Makkah valley. A shepherd's staff planted in the ground at CENTER with GOLDEN LIGHT emanating around it (Muhammad's presence — NO human figure). A flock of 15-20 sheep and goats grazing around the staff at CENTER height. One baby goat standing close to the staff. Golden morning light from behind. Small bag of provisions on ground. Makkah city small in distance.
CRITICAL: ALL sheep/goats must be fully visible in the CENTER band — their heads AND legs/hooves must be between 25%-75% of image height. Do NOT place any animal at the very bottom where it would be cropped. The staff tip should NOT be at the very top edge.
NO human figure. Staff + golden light only. Mood: peaceful, humble."""),
]

for fn, prompt in IMGS:
    print(f"\n🎨 {fn}...")
    payload = json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"]}}).encode()
    req = urllib.request.Request(URL, data=payload, headers={"Content-Type":"application/json"})
    resp = urllib.request.urlopen(req, timeout=120)
    data = json.loads(resp.read())
    for p in data.get("candidates",[{}])[0].get("content",{}).get("parts",[]):
        if "inlineData" in p:
            d = base64.b64decode(p["inlineData"]["data"])
            with open(os.path.join(OUT,fn),"wb") as f: f.write(d)
            print(f"  ✅ {len(d)} bytes")
            break
    else: print("  ❌ No image")
