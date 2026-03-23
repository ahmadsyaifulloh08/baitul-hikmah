#!/usr/bin/env python3
import json, base64, urllib.request, os

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT = "/workspace/projects/baitul-hikmah/public/illustrations/children"

S = """Warm watercolor storybook illustration for children age 6-12. Soft edges, stylized (not photorealistic). Arabian 6th century. Sandy gold, warm beige, dusty earth.
ABSOLUTELY NO text, words, letters, signatures, watermarks, or writing of ANY kind anywhere in the image.
COMPOSITION: TOP 22% and BOTTOM 22% will be CROPPED. ALL important subjects in CENTER 56% vertical band."""

IMGS = [
    ("e01-slide-03.png", f"""{S}
Military camp. Abrahah (red/gold robe, crown) on platform CENTER giving orders. Head at VERTICAL CENTER. Elephants — Mahmud (biggest, dark gray, red saddle) front center. Soldiers. Mood: menacing.
ABSOLUTELY NO signatures, watermarks, or text marks anywhere."""),

    ("e01-slide-10.png", f"""{S}
Night in Makkah. Stone house CENTER with GOLDEN LIGHT from windows/door. Bright star BELOW the top 25% of image — star at roughly 30-35% from top. Makkah rooftops at same height. Women (from behind) walking toward house. Everything in center band.
NO baby, NO human for Prophet. Only LIGHT from house."""),

    ("e02-slide-02.png", f"""{S}
Still-life courtyard in Makkah. Five camels, few goats, small bundle of belongings. Morning light. Empty — owner gone. A woman's SHADOW (not labeled, not named) on ground near animals. Simple, sparse. Mood: modest inheritance.
NO labels, NO names, NO text of any kind."""),

    ("e02-slide-03.png", f"""{S}
Market in Makkah. Bedouin women on donkeys/camels, looking at babies held by Meccan mothers. Busy, colorful. All heads in center band. Stone buildings backdrop. Mood: lively tradition.
NO signatures, NO watermarks, NO text anywhere."""),

    ("e02-slide-11.png", f"""{S}
Abdul Muthalib (elderly, white beard, white robe) sitting on carpet near Ka'bah courtyard. Other Quraish leaders in circle, some smiling. A WARM GOLDEN ORB OF LIGHT floats close beside Abdul Muthalib — he extends hand toward it. Ka'bah wall background. Afternoon light. All heads in center band.
CRITICAL: Muhammad is represented ONLY as a GOLDEN ORB OF LIGHT — absolutely NO child figure, NO human figure, NO silhouette. Only Abdul Muthalib and other adult Quraish leaders are human figures in this scene."""),

    ("e02-slide-12.png", f"""{S}
Simple Meccan room. Elderly Abdul Muthalib (white beard) lying on bed/mat, one hand reaching out pointing toward Abu Thalib (younger man, brown robe, kind face, hand on heart). Between them: a small GOLDEN ORB OF LIGHT (Muhammad's presence). Oil lamp, muted colors. All in center band.
CRITICAL: Muhammad is ONLY a golden orb of light — NO child, NO human figure, NO silhouette for Muhammad. Only Abdul Muthalib and Abu Thalib are human. Mood: solemn trust."""),
]

for fn, prompt in IMGS:
    print(f"\n🎨 {fn}...")
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

print("\n✅ Done!")
