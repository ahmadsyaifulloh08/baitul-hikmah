#!/usr/bin/env python3
"""Regenerate images that contain text — with NO TEXT instruction."""
import json, base64, urllib.request, os

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT_DIR = "/workspace/projects/baitul-hikmah/public/illustrations/children"

STYLE = "Warm watercolor storybook illustration for children age 6-12. 16:9 landscape. Soft edges, stylized (not photorealistic). Arabian 6th century. Sandy gold, warm beige, dusty earth palette."
NO_TEXT = "CRITICAL: Do NOT include ANY text, words, letters, labels, captions, titles, signatures, or writing of any kind in the image. The image must be purely visual with zero text elements."

IMAGES = [
    {
        "file": "e01-slide-02.png",
        "prompt": f"""{STYLE}
{NO_TEXT}

Scene: Split composition. LEFT side shows a grand ornate church (al-Qullays) with massive pillars and gold ornaments — but EMPTY, no visitors at all. RIGHT side shows streams of Arab travelers on camels heading toward a distant Ka'bah (simple stone cube) bathed in golden light. Strong contrast between the ignored grandeur on left and the beloved simplicity on right. Desert landscape. Mood: the heart goes where it belongs."""
    },
    {
        "file": "e01-slide-07.png",
        "prompt": f"""{STYLE}
{NO_TEXT}

Scene: Elephant Mahmud (largest war elephant, dark gray, red war saddle with gold cloth) STANDING but REFUSING to walk toward the Ka'bah. The elephant turns its body to walk in a DIFFERENT direction (away from Ka'bah). The Ka'bah (simple stone cube draped in cloth) is visible in the background BEHIND the elephant. The handler on top is pulling reins desperately but the elephant stubbornly turns away. Other soldiers look confused and frustrated. Desert setting, clear sky. Mood: divine intervention.
The elephant is STANDING (not kneeling), body angled AWAY from Ka'bah."""
    },
    {
        "file": "e02-slide-01.png",
        "prompt": f"""{STYLE}
{NO_TEXT}

Scene: A simple fresh grave mound with a plain stone marker in an oasis of Yatsrib (ancient Madinah). Date palms casting long shadows in late afternoon light. A few travelers' belongings (merchant bags, water flask) left near the grave. Golden-orange sunset sky, melancholic atmosphere. Buildings of ancient Yatsrib visible in background. Mood: sad but peaceful."""
    },
    {
        "file": "e02-slide-03.png",
        "prompt": f"""{STYLE}
{NO_TEXT}

Scene: Market/gathering scene in ancient Makkah. Several Bedouin women arriving on donkeys and camels, looking at babies held by Meccan mothers. Busy, colorful scene with women examining and negotiating. Focus on the social activity and lively tradition. Stone buildings of Makkah in background. Morning light. Mood: lively cultural tradition."""
    },
    {
        "file": "e02-slide-08.png",
        "prompt": f"""{STYLE}
{NO_TEXT}

Scene: A woman (Aminah — young Arab woman in modest dress) riding a camel with a covered howdah/sedan. A small golden light sits beside her in the howdah — representing Muhammad's presence (NOT a physical child, just pure warm golden light/nur). Another woman (Ummu Aiman — dark-skinned, Ethiopian) walking alongside the camel. A small caravan of 2-3 camels setting out from Makkah (city visible behind). Road ahead stretches toward distant hills. Morning light, hopeful departure. Mood: mother-son journey, bittersweet.
CRITICAL: Muhammad represented ONLY as golden light — NO child figure."""
    },
    {
        "file": "e02-slide-09.png",
        "prompt": f"""{STYLE}
{NO_TEXT}

Scene: Ummu Aiman (dark-skinned woman, Ethiopian, protective posture, modest clothing) walking on foot along a desert road toward Makkah (visible ahead in the distance). She leads a camel behind her. A warm golden glow travels beside her at waist height — representing Muhammad's presence (NOT a physical child). Stars beginning to appear in dusky twilight sky. Her shadow stretches long on the sand. She looks determined despite exhaustion. Mood: devotion, protection, resilience.
CRITICAL: Muhammad is ONLY a golden glow — NO child or human figure."""
    },
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
                print(f"  ✅ Saved {len(img_data)} bytes")
                break
        else:
            print(f"  ❌ No image in response")
            # Check for error
            if 'error' in data:
                print(f"  Error: {data['error'].get('message','')}")
            else:
                print(json.dumps(data)[:300])
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n✅ Done!")
