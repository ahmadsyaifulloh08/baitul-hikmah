#!/usr/bin/env python3
import json, base64, urllib.request

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT = "/workspace/projects/baitul-hikmah/public/illustrations/children/e01-slide-10.png"

PROMPT = """Warm watercolor storybook illustration for children age 6-12. Soft edges, stylized. Arabian 6th century. Sandy gold, warm beige, dusty earth.
CRITICAL: No text, no words, no letters, no signatures.

Scene: Night scene in ancient Makkah. The composition is a HORIZONTAL BAND — everything important happens in the MIDDLE THIRD of the image vertically.

In the CENTER: a simple stone house with WARM GOLDEN LIGHT glowing brilliantly from its windows and door, spreading outward like a halo. The house is at the EXACT vertical center.

ABOVE the house (but still in the middle third, NOT at the top): a single brilliant bright star. The star must be BELOW the top 25% of the image. Dark night sky fills the rest of the upper area — it's OK if this gets cropped.

TO THE SIDES: silhouettes of other Makkah houses at the same height as the central house. A distant Ka'bah silhouette.

BELOW: a street/path with a few small women figures (from behind) walking toward the glowing house. Their feet can be near the bottom — OK if cropped since text overlay goes there.

The KEY FOCAL POINT is the glowing house + star — both MUST be in the center 50% vertically.

Mood: sacred night, miraculous birth, divine light.
CRITICAL: NO baby, NO child figure, NO human representing the Prophet. Only golden LIGHT emanating from the house."""

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
        print(f"✅ Saved {len(img_data)} bytes")
        break
