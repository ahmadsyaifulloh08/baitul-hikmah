#!/usr/bin/env python3
"""Regenerate e02-slide-07 with centered safe-zone composition."""
import urllib.request, urllib.error, base64, json, sys, shutil

API_KEY = open("/workspace/credentials/api-gemini.txt").read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT = "/workspace/projects/baitul-hikmah/public/illustrations/children/e02-slide-07.png"

prompt = """Create a children's book illustration in warm watercolor style with ink outlines.

Scene: A woman (Halimah, wearing modest brown/beige robes and white headscarf) riding a small grey donkey through a desert path, heading toward a distant city (Makkah, visible as small buildings on the horizon). She cradles a BRILLIANTLY GLOWING GOLDEN ORB OF INTENSE LIGHT in her arms — the orb radiates bright golden rays and warm light beams in all directions, illuminating her face and surroundings. The light is VERY BRIGHT and RADIANT, like a small sun, with visible rays spreading outward. NOT a human baby — purely a supernatural sphere of divine golden light/nur. Desert landscape with sandy dunes, a few palm trees. Warm sunset lighting.

Style: Soft watercolor washes, warm earth tones (amber, ochre, cream, sand), gentle ink outlines, storybook illustration for children aged 6-12.

⚠️ PROPHET MUHAMMAD MUST BE DEPICTED ONLY AS A BRILLIANTLY GLOWING GOLDEN ORB OF LIGHT with VISIBLE BRIGHT RAYS emanating outward — absolutely NO human figure, NO baby, NO child, NO face, NO silhouette. The orb must be the brightest element in the entire image, with strong light rays and a warm golden glow that illuminates everything around it.

CRITICAL COMPOSITION — MUST FOLLOW: Place the woman and donkey in the CENTER of the image, positioned LOW — her head must be at approximately 40% from the top (NOT near the top edge). Leave generous empty sky/clouds in the TOP 25% of the image. The BOTTOM 15% should be ground/sand only. All faces and important details must be between 30%-80% from the top of the image. This is critical because the top and bottom edges WILL be cropped on wide screens.

ABSOLUTELY NO TEXT of any kind in the image — no captions, labels, titles, watermarks, signatures, letters, numbers, or writing in any script."""

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "responseModalities": ["image", "text"]
    }
}

print("Generating e02-slide-07...")
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
        shutil.copy2(OUT, OUT.replace(".png", "-old.png"))
        with open(OUT, "wb") as f:
            f.write(img_bytes)
        print(f"Saved to {OUT} ({len(img_bytes)} bytes)")
        break
else:
    print("No image in response")
    sys.exit(1)
