#!/usr/bin/env python3
"""Generate 3 missing children illustrations via Gemini API."""
import json, base64, urllib.request, sys, os

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT_DIR = "/workspace/projects/baitul-hikmah/public/illustrations/children"

STYLE = "Warm watercolor storybook illustration for children age 6-12. 16:9 landscape. Soft edges, stylized (not photorealistic). Arabian 6th century setting. Sandy gold, warm beige, dusty earth palette."

IMAGES = [
    {
        "file": "e01-slide-07.png",
        "prompt": f"""{STYLE}

Scene: Elephant Mahmud (largest war elephant, dark gray, red war saddle with gold cloth) STANDING but REFUSING to walk toward the Ka'bah. The elephant turns its body to walk in a DIFFERENT direction (away from Ka'bah, toward the right side of the image). The Ka'bah (simple stone cube draped in cloth) is visible in the background BEHIND the elephant on the left side. The handler on top is pulling reins trying to steer toward Ka'bah but the elephant stubbornly turns away. Other soldiers look confused and frustrated. Desert setting, clear sky. Mood: divine intervention, the mighty beast obeys only Allah.
CRITICAL: The elephant is STANDING (not kneeling), body angled AWAY from Ka'bah, Ka'bah visible BEHIND it."""
    },
    {
        "file": "e01-slide-11.png",
        "prompt": f"""{STYLE}

Scene: Peaceful pastoral landscape in the desert of Bani Sa'd (Arabian Bedouin territory). In the center, a simple Bedouin tent (brown/cream fabric) with a warm golden glow emanating from inside — symbolizing blessing/barakah. Around the tent: fat healthy sheep and goats grazing on surprisingly green patches of desert grass. A few more Bedouin tents in the background. Gentle rolling sand dunes. Warm sunset sky with pink and gold clouds. NO human figures visible. The scene radiates abundance and divine blessing in an otherwise harsh desert.
IMPORTANT: No human figures. Focus on the blessed tent and thriving animals. Mood: warmth, abundance, divine blessing."""
    },
    {
        "file": "e02-slide-10.png",
        "prompt": f"""{STYLE}

Scene: Courtyard of a simple but dignified Meccan house. Abdul Muthalib (elderly dignified Arab leader, white beard, clean white robe, calm noble posture) sits on a cushion under a palm tree. Next to him, a warm GOLDEN ORB of light (representing young Muhammad — NOT a human figure, just pure warm golden light/nur). Abdul Muthalib looks at the light with deep love and tenderness, one hand gently extended toward it. Evening light, oil lamp nearby. A special woven mat/carpet beneath them. Other family members visible in far background but out of focus. Mood: grandfather's deep love, warmth, protection.
CRITICAL: Muhammad represented ONLY as golden light/nur orb — absolutely NO human figure, no child, no silhouette, no shadow."""
    }
]

for img in IMAGES:
    print(f"\n🎨 Generating {img['file']}...")
    payload = json.dumps({
        "contents": [{"parts": [{"text": img["prompt"]}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }).encode()
    
    req = urllib.request.Request(URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read())
        
        for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                out_path = os.path.join(OUT_DIR, img["file"])
                with open(out_path, "wb") as f:
                    f.write(img_data)
                print(f"  ✅ Saved {len(img_data)} bytes → {out_path}")
                break
        else:
            print(f"  ❌ No image in response")
            print(json.dumps(data)[:300])
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n✅ Done generating 3 images!")
