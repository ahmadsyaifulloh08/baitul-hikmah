#!/usr/bin/env python3
"""Regenerate e01-slide-07 with centered safe-zone composition."""
import urllib.request, urllib.error, base64, json, sys, shutil

API_KEY = open("/workspace/credentials/api-gemini.txt").read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT = "/workspace/projects/baitul-hikmah/public/illustrations/children/e01-slide-07.png"

prompt = """Create a children's book illustration in warm watercolor style with ink outlines.

Scene: Inside a decorated military tent. Close-up moment — an elderly Arab leader (Abdul Muthalib, white beard, white turban, dignified) raises his hand in a calm gesture of certainty. Across from him, a foreign military commander (Abrahah, dark skin, ornate armor, golden crown) leans forward in disbelief. Warm light streams through the tent opening, illuminating Abdul Muthalib's face.

Style: Soft watercolor washes, warm earth tones (amber, ochre, cream), gentle ink outlines, storybook illustration quality. Two characters facing each other in dialogue.

CRITICAL COMPOSITION — MUST FOLLOW: Frame the two characters in the LOWER-CENTER of the image. Their heads must NOT go above 30% from top. Leave generous empty space (tent ceiling, fabric drapes) in the top 25% of the image. Bottom 15% should be floor/carpets only. All faces and hands must be in the vertical middle band (25%-85% from top). This ensures safe cropping on wide screens.

ABSOLUTELY NO TEXT of any kind in the image — no captions, labels, titles, watermarks, signatures, letters, numbers, or writing in any script. The image must be purely illustrative with zero text elements."""

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "responseModalities": ["image", "text"]
    }
}

print("Generating e01-slide-07...")
req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
try:
    resp = urllib.request.urlopen(req, timeout=120)
    data = json.loads(resp.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:500]}")
    sys.exit(1)

if "candidates" not in data:
    print(f"ERROR: {json.dumps(data, indent=2)[:500]}")
    sys.exit(1)

for part in data["candidates"][0]["content"]["parts"]:
    if "inlineData" in part:
        img_bytes = base64.b64decode(part["inlineData"]["data"])
        # Backup old
        shutil.copy2(OUT, OUT.replace(".png", "-old.png"))
        with open(OUT, "wb") as f:
            f.write(img_bytes)
        print(f"Saved to {OUT} ({len(img_bytes)} bytes)")
        break
else:
    print("No image in response")
    print(json.dumps(data, indent=2)[:500])
    sys.exit(1)
