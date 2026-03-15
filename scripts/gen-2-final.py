#!/usr/bin/env python3
import json, base64, urllib.request, os

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT = "/workspace/projects/baitul-hikmah/public/illustrations/children"

S = """Warm watercolor storybook illustration for children age 6-12. Soft edges, stylized. Arabian 6th century. Sandy gold, warm beige, dusty earth.
NO text, words, signatures anywhere.
TOP 22% and BOTTOM 22% will be CROPPED. Everything important in CENTER 56%."""

IMGS = [
    ("e01-slide-10.png", f"""{S}
Night scene in Makkah. A simple stone house at the CENTER of the image with WARM GOLDEN LIGHT flooding from its windows and door, creating a massive glow/halo around it. The house sits at the EXACT VERTICAL MIDDLE. NO star in the sky — instead, the golden light from the house itself creates rays upward. Dark night sky with small scattered stars (not important if cropped). Makkah rooftop silhouettes at center height. A few women (from behind) walking toward the house in foreground. The FOCAL POINT is the glowing house at dead center.
NO baby, NO human for Prophet. Only LIGHT from house."""),

    ("e02-slide-12.png", f"""{S}
Simple Meccan room. TWO human figures ONLY:
- LEFT: Abdul Muthalib (elderly, white beard, white robe) lying on bed/mat, reaching out
- RIGHT: Abu Thalib (younger man, brown robe, kind face) standing with hand on heart
Between them FLOATING in the air: a GOLDEN GLOWING ORB OF LIGHT — this orb is Muhammad's presence. The orb is just pure light, spherical, warm golden, floating at chest height between the two men. No third person. Oil lamp on table. Muted warm colors.
ABSOLUTELY NO third human figure. Muhammad is the GOLDEN ORB ONLY. Only 2 humans in the entire image: the elderly man on the bed and the younger man standing."""),
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
