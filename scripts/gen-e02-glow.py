#!/usr/bin/env python3
"""Regenerate e02 slides with consistent golden glow (no calligraphy) + no borders."""
import json, base64, urllib.request, os, time

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT = "/workspace/projects/baitul-hikmah/public/illustrations/children"

S = """Warm watercolor storybook illustration for children age 6-12. Soft edges, stylized (not photorealistic). Arabian 6th century. Sandy gold, warm beige, dusty earth.
NO text, words, letters, signatures, calligraphy of any kind.
The illustration MUST fill the ENTIRE canvas edge-to-edge with the scene — no white borders, no black bars, no vignette edges, no rounded corners. The sky, ground, and scene extend to ALL edges.
TOP 22% and BOTTOM 30% may be cropped/covered. Important subjects between 22%-70% height."""

GLOW = "a warm GOLDEN RADIANT GLOW — a circular soft golden-white light with gentle rays emanating outward, like a small warm sun. Consistent size (~15% of image height), warm golden color."

IMGS = [
    ("e02-slide-01.png", f"""{S}
Scene: A simple fresh grave mound with plain stone marker in an oasis of Yatsrib (ancient Madinah). Date palms casting long shadows. Travelers' belongings (merchant bags, water flask) near grave. Golden-orange sunset sky filling the TOP of the canvas. Sandy ground filling the BOTTOM. Buildings of Yatsrib in background. Mood: sad but peaceful.
No Muhammad light in this scene — just the grave."""),

    ("e02-slide-04.png", f"""{S}
Scene: Halimah (Bedouin woman, brown/cream clothing, head covering, kind face) standing near a Meccan house, being handed a bundle of white cloth. From the bundle emanates {GLOW} Halimah looks surprised, touched.
NO baby face/body — just cloth bundle with golden glow. Mood: turning point."""),

    ("e02-slide-05.png", f"""{S}
Scene: Halimah's camp in desert but LUSH and GREEN. Fat goats on green grass. Full milk containers. Tent well-maintained. Near tent entrance: {GLOW} Other Bani Sa'd tents in background look dry/normal. Mood: miraculous blessing."""),

    ("e02-slide-06.png", f"""{S}
Scene: Open desert field. A brilliant column of white-golden light rising from ground at CENTER. At the base of the column: {GLOW} Two luminous white silhouettes (angels — no faces) kneeling on either side. Sheep/goats watching nearby. All between 25%-70% height.
NO physical form of Muhammad — only the golden glow. Mood: supernatural."""),

    ("e02-slide-07.png", f"""{S}
Scene: Halimah on donkey traveling desert road toward Makkah (ahead). She carries a bundle from which emanates {GLOW} Worried, protective expression. Desert road behind.
NO baby face. Mood: maternal protection."""),

    ("e02-slide-08.png", f"""{S}
Scene: Small caravan (2-3 camels) from Makkah. Aminah (young woman, modest dress) riding camel with howdah. In the howdah beside her: {GLOW} Ummu Aiman (dark-skinned) walking alongside. Road to hills. Morning light.
Muhammad = ONLY the golden glow. NO child."""),

    ("e02-slide-09.png", f"""{S}
Scene: Ummu Aiman (dark-skinned, Ethiopian) walking on desert road toward Makkah (ahead). Leads camel. At her side: {GLOW} floating beside her at waist height. Dusky twilight. Shadow stretches. Determined.
Muhammad = ONLY golden glow."""),

    ("e02-slide-10.png", f"""{S}
Scene: Courtyard of Meccan house. Abdul Muthalib (elderly, white beard, white robe) sits ALONE on cushion under palm tree. Beside him: {GLOW} He gazes at it with tenderness, hand extended. Evening, oil lamp. Woven carpet.
ONLY Abdul Muthalib as human. NO children. Muhammad = golden glow."""),

    ("e02-slide-11.png", f"""{S}
Scene: Abdul Muthalib (elderly, white beard, white robe) on carpet near Ka'bah courtyard. Quraish leaders in circle. Beside Abdul Muthalib: {GLOW} He extends hand toward it. Ka'bah wall background. Afternoon. Heads between 25%-65%.
NO child. Muhammad = golden glow."""),

    ("e02-slide-12.png", f"""{S}
Scene: Simple Meccan room. Abdul Muthalib (elderly, white beard) on bed/mat LEFT, reaching out. Abu Thalib (younger, brown robe) standing RIGHT, hand on heart. Between them: {GLOW} Oil lamp. Both heads 30%-50% from top.
Only 2 humans. Muhammad = golden glow. Mood: solemn trust."""),

    ("e02-slide-13.png", f"""{S}
Scene: Modest home. Abu Thalib (brown robe, kind face) with children at modest meal — bread, dates, milk. Among them: {GLOW} Makes meal glow warmer. Abu Thalib smiling toward light. Cozy. Heads 25%-60% from top.
Muhammad = golden glow. Mood: love despite poverty."""),

    ("e02-slide-14.png", f"""{S}
Scene: Hilltop overlooking Makkah valley. Shepherd's staff planted at CENTER. Around staff: {GLOW} Sheep/goats (15-20) grazing, ALL fully visible between 30%-65% height. Baby goat near staff. Golden morning. Makkah small in distance.
NO human figure. Staff + golden glow only."""),
]

for i, (fn, prompt) in enumerate(IMGS):
    print(f"\n🎨 [{i+1}/{len(IMGS)}] {fn}...")
    payload = json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"]}}).encode()
    req = urllib.request.Request(URL, data=payload, headers={"Content-Type":"application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read())
        for p in data.get("candidates",[{}])[0].get("content",{}).get("parts",[]):
            if "inlineData" in p:
                d = base64.b64decode(p["inlineData"]["data"])
                with open(os.path.join(OUT,fn),"wb") as f: f.write(d)
                print(f"  ✅ {len(d)} bytes")
                break
        else: print("  ❌ No image")
    except Exception as e: print(f"  ❌ {e}")
    if (i+1) % 5 == 0:
        time.sleep(3)

print(f"\n✅ Done!")
