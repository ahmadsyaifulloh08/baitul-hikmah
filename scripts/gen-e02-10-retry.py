#!/usr/bin/env python3
import json, base64, urllib.request, os

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT = "/workspace/projects/baitul-hikmah/public/illustrations/children/e02-slide-10.png"

PROMPT = """Warm watercolor storybook illustration for children age 6-12. 16:9 landscape. Soft edges, stylized (not photorealistic). Arabian 6th century setting. Sandy gold, warm beige, dusty earth palette.

Scene: Simple courtyard of a Meccan house at evening time. An elderly dignified Arab man (Abdul Muthalib — white long beard, clean white robe, calm noble expression) sits alone on a decorated cushion under a date palm tree. Next to him on his right side floats a warm GOLDEN GLOWING ORB of pure light — ethereal, magical, radiating warmth and love. Abdul Muthalib gazes at this golden orb with deep tenderness and affection, one hand gently extended toward it. A special woven carpet beneath him. Oil lamp nearby. Warm evening light. Stone walls of courtyard visible.

ABSOLUTE REQUIREMENTS:
- Abdul Muthalib is the ONLY human figure in the entire image. NO other people anywhere — no children, no adults, no silhouettes in background.
- The golden orb is PURE LIGHT — not shaped like a person, not a halo around anyone, just a floating sphere of warm golden light.
- NO children anywhere in the image. Zero. None.
- Mood: deep grandfather's love, warmth, divine blessing."""

payload = json.dumps({
    "contents": [{"parts": [{"text": PROMPT}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
}).encode()

req = urllib.request.Request(URL, data=payload, headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(req, timeout=120)
data = json.loads(resp.read())

for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
    if "inlineData" in part:
        img_data = base64.b64decode(part["inlineData"]["data"])
        with open(OUT, "wb") as f:
            f.write(img_data)
        print(f"✅ Saved {len(img_data)} bytes → {OUT}")
        break
else:
    print("❌ No image")
    print(json.dumps(data)[:500])
