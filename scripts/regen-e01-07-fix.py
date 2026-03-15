#!/usr/bin/env python3
"""Regenerate e01-slide-07: Gajah menolak + langit gelap + burung ababil datang."""
import urllib.request, urllib.error, base64, json, sys, shutil

API_KEY = open("/workspace/credentials/api-gemini.txt").read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT = "/workspace/projects/baitul-hikmah/public/illustrations/children/e01-slide-07.png"

prompt = """Create a children's book illustration in warm watercolor style with ink outlines.

Scene: A large grey elephant (Mahmud) KNEELING on the desert ground, front legs folded, head bowed — refusing to move toward the Ka'bah visible in the distance. His handler on top is desperately trying to make him move but the elephant won't budge. In the SKY above, dark storm clouds are gathering and a large flock of small birds (ababil) can be seen approaching from the distance. The mood is dramatic — divine intervention is beginning. Desert landscape, Ka'bah small in the background.

Style: Soft watercolor washes, warm earth tones (amber, ochre, cream), dramatic sky with contrast between dark clouds and golden light over Ka'bah, gentle ink outlines, storybook illustration for children aged 6-12.

CRITICAL COMPOSITION — MUST FOLLOW: Place the elephant in the CENTER-LOWER portion of the image. The elephant's head/back must NOT go above 30% from top. Leave generous empty sky (with clouds and distant birds) in the TOP 30% of the image. Bottom 15% should be desert ground only. All important subjects between 25%-85% from top.

ABSOLUTELY NO TEXT of any kind in the image — no captions, labels, titles, watermarks, signatures, letters, numbers, or writing in any script."""

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"responseModalities": ["image", "text"]}
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
        shutil.copy2(OUT, OUT.replace(".png", "-mismatch.png"))
        with open(OUT, "wb") as f:
            f.write(img_bytes)
        print(f"Saved ({len(img_bytes)} bytes)")
        break
else:
    print("No image in response")
    sys.exit(1)
