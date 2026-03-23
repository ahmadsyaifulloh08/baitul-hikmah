#!/usr/bin/env python3
import json, base64, urllib.request, os

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT = "/workspace/projects/baitul-hikmah/public/illustrations/children"

S = """Warm watercolor storybook illustration for children age 6-12. Soft edges, stylized (not photorealistic). Arabian 6th century. Sandy gold, warm beige, dusty earth.
NO text, words, letters, signatures of any kind.
Illustration fills ENTIRE canvas edge-to-edge — no white/black borders.
TOP 22% and BOTTOM 30% may be cropped/covered. Important subjects between 22%-70% height."""

GLOW = "a warm GOLDEN RADIANT GLOW — a circular soft golden-white light with gentle rays emanating outward, like a small warm sun. Size ~15% of image height."

IMGS = [
    ("e02-slide-01.png", f"""{S}
Scene: Inspired by Baqi cemetery (Madinah). Wide view of a simple ancient cemetery in Yatsrib — multiple low grave mounds with plain stone markers in sandy ground. The main grave (Abdullah's) is at the EXACT CENTER of the image both horizontally and vertically. Date palms scattered around the cemetery. Low mud-brick walls of ancient Yatsrib/Madinah visible in background. Golden-orange sunset sky. A few travelers' belongings (merchant bag, water flask) near the central grave. The scene is CENTERED — the grave is the focal point at dead center of the image. Sandy desert ground extends to all edges. Mood: sad but peaceful, quiet solitude."""),

    ("e02-slide-04.png", f"""{S}
Scene: Halimah (Bedouin woman, brown/cream clothing, head covering, kind gentle face) standing near a Meccan stone house. Another woman hands her a BUNDLE OF WHITE CLOTH — the bundle is wrapped tightly, NO baby face or body visible at all, just folded white cloth. From the CENTER of the cloth bundle emanates {GLOW} The golden glow is clearly coming FROM the bundle, radiating outward, illuminating Halimah's face. Halimah's expression: awe, surprise, touched by the warmth.
CRITICAL: The bundle is just CLOTH — absolutely NO baby face, NO baby hands, NO skin visible. The glow replaces any visibility of the baby. Only cloth + golden light. Mood: turning point, quiet miracle."""),

    ("e02-slide-07.png", f"""{S}
Scene: Halimah (brown/cream clothing, head covering) riding a donkey along a desert road toward Makkah (city visible ahead in distance). She holds a BUNDLE OF WHITE CLOTH against her chest. WHERE the baby's face would be, there is instead {GLOW} The golden glow completely REPLACES the baby's face — you see cloth wrapping and then golden light where the face should be. No skin, no features visible. Halimah looks worried but protective, gazing down at the glowing bundle. Desert road stretching behind. Other desert travelers' tracks in sand.
CRITICAL: The baby's face is ENTIRELY replaced by the golden glow. No eyes, no nose, no skin — just radiant golden light emanating from where the face would be. The cloth wraps around but the face area is pure light. Mood: concern, maternal protection."""),
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
