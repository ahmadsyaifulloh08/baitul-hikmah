#!/usr/bin/env python3
import json, base64, urllib.request, os

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT = "/workspace/projects/baitul-hikmah/public/illustrations/children"

S = """Warm watercolor storybook illustration for children age 6-12. Soft edges, stylized (not photorealistic). Arabian 6th century. Sandy gold, warm beige, dusty earth.
NO text, words, letters, signatures anywhere.
COMPOSITION: TOP 22% and BOTTOM 30% will be CROPPED or covered by text overlay. Place ALL important subjects between 25%-70% of image height. Nothing important at top or bottom edges."""

IMGS = [
    ("e02-slide-12.png", f"""{S}
Scene: Simple Meccan room interior. TWO men:
- LEFT: Abdul Muthalib (elderly, white beard, white robe) lying/reclining on a low bed, one hand reaching out
- RIGHT: Abu Thalib (younger man, brown robe, kind face) standing with hand on heart
Between them: a RADIANT BURST OF WARM GOLDEN LIGHT — not a small orb/ball, but a large spreading warm GLOW/RADIANCE like a small sun, with soft rays emanating outward. This light represents Muhammad's presence. The light should be prominent, warm, and clearly divine/special — bigger than a lantern flame, more like a gentle explosion of golden warmth filling the space between the two men.
Oil lamp on side table. Simple mud-brick walls.
CRITICAL: Both men's heads at 30-40% from top (well below crop line). The golden radiance at center height (~45-50% from top).
Muhammad = ONLY this golden radiance. NO third person. NO child.
Mood: solemn trust, passing of guardianship."""),

    ("e02-slide-06.png", f"""{S}
Scene: Open desert field at Bani Sa'd. A brilliant COLUMN OF WHITE-GOLDEN LIGHT rising from the ground in the CENTER of the image. The light column is tall but contained — its BASE starts at ~55% from top and its TOP reaches ~30% from top (well within safe zone). Two glowing luminous silhouettes (angels — pure white light forms, no facial features) kneeling on either side of the column BASE, positioned at ~50-55% from top.
Sheep and goats nearby at ~50-60% height, all FULLY visible (heads AND legs). Children (small figures) running toward tents in far background at ~55% height.
Above: sky with bright blue opening (decorative, can be cropped). Below: desert sand (can be cropped/covered by text).
CRITICAL: ALL important elements (light column, angels, animals) MUST be between 25%-70% of image height. Nothing important below 70%.
NO physical form of Muhammad. Pure light column only.
Mood: supernatural, sacred."""),
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
