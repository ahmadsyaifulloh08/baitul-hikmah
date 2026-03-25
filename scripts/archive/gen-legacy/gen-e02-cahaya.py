#!/usr/bin/env python3
"""Regenerate e02 slides with consistent cahaya + fix slide-01 border."""
import json, base64, urllib.request, os, time

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT = "/workspace/projects/baitul-hikmah/public/illustrations/children"

S = """Warm watercolor storybook illustration for children age 6-12. Soft edges, stylized (not photorealistic). Arabian 6th century. Sandy gold, warm beige, dusty earth.
NO text, words, signatures EXCEPT the Arabic calligraphy "محمد" inside the golden light (see below).
The image MUST fill the entire canvas edge-to-edge. NO black borders, NO letterbox, NO padding.
TOP 22% and BOTTOM 30% may be cropped/covered. Place important subjects between 22%-70% height."""

CAHAYA = """Muhammad's presence is represented as a GOLDEN RADIANT GLOW — a circular warm golden-white light radiating outward in all directions, with soft rays. In the CENTER of this glow, the Arabic calligraphy "محمد" (Muhammad) is visible, beautifully integrated into the light. The glow is warm, inviting, and proportional to the scene (~15-20% of image height). This exact same representation must be used."""

IMGS = [
    ("e02-slide-01.png", f"""{S}
Scene: A simple fresh grave mound with plain stone marker in an oasis of Yatsrib (ancient Madinah). Date palms casting long shadows in late afternoon light. A few travelers' belongings (merchant bags, water flask) left near the grave. Golden-orange sunset sky. Buildings of Yatsrib in background. The illustration fills the ENTIRE canvas — no borders, no padding. Mood: sad but peaceful.
This scene does NOT contain Muhammad's light — it's just a grave scene."""),

    ("e02-slide-04.png", f"""{S}
Scene: Halimah (Bedouin woman, brown/cream clothing, kind face, head covering) standing near a Meccan house, being handed a bundle of white cloth. From the bundle emanates {CAHAYA} The glow illuminates Halimah's face with warmth. She looks surprised, touched. Mood: turning point, quiet miracle.
NO baby face/body visible — just cloth bundle with the golden calligraphy light."""),

    ("e02-slide-05.png", f"""{S}
Scene: Halimah's camp in the desert, but everything is LUSH and GREEN. Fat healthy goats grazing on green grass. Full milk containers. Well-maintained Bedouin tent at center. Near the tent entrance: {CAHAYA} The golden light with "محمد" calligraphy emanates warmth that seems to cause the greenery. Other tents in background look dry/normal. Mood: miraculous blessing."""),

    ("e02-slide-06.png", f"""{S}
Scene: Open desert field at Bani Sa'd. A brilliant column of white-golden light rising from the ground at CENTER. At the BASE of the column: {CAHAYA} Two luminous white silhouettes (angels — no faces, pure glowing forms) kneeling on either side. Sheep/goats watching from nearby. Children running to tents in background. All elements between 25%-70% height.
NO physical form of Muhammad. The "محمد" calligraphy light at the base of the column. Mood: supernatural, sacred."""),

    ("e02-slide-07.png", f"""{S}
Scene: Halimah (brown/cream clothing) on a donkey traveling desert road toward Makkah (city ahead). She carries a bundle — from which emanates {CAHAYA} The golden "محمد" calligraphy light at her chest/arms. Her expression: worried but protective. Desert road behind. Mood: maternal protection.
NO baby face — just the golden calligraphy glow in the bundle."""),

    ("e02-slide-08.png", f"""{S}
Scene: Small caravan (2-3 camels) setting out from Makkah. Aminah (young woman, modest dress) riding camel with howdah/sedan. Beside her in the howdah: {CAHAYA} The golden "محمد" calligraphy light floating in the howdah. Ummu Aiman (dark-skinned woman) walking alongside. Road to hills. Morning light. Mood: bittersweet journey.
Muhammad = ONLY the golden calligraphy light. NO child figure."""),

    ("e02-slide-09.png", f"""{S}
Scene: Ummu Aiman (dark-skinned, Ethiopian, protective posture) walking on desert road toward Makkah (visible ahead). She leads a camel. Beside her at waist height: {CAHAYA} The golden "محمد" calligraphy light traveling alongside her. Dusky twilight sky. Shadow stretches long. Determined despite exhaustion. Mood: devotion, resilience.
Muhammad = ONLY the golden calligraphy light."""),

    ("e02-slide-10.png", f"""{S}
Scene: Courtyard of simple Meccan house. Abdul Muthalib (elderly, white beard, white robe) sits ALONE on cushion under palm tree. Next to him: {CAHAYA} The golden "محمد" calligraphy light floating beside him at chest height. He gazes at it with tenderness, one hand extended. Evening light, oil lamp. Woven carpet.
ONLY Abdul Muthalib as human. NO other people, NO children. Muhammad = golden calligraphy light only."""),

    ("e02-slide-11.png", f"""{S}
Scene: Abdul Muthalib (elderly, white beard, white robe) on carpet near Ka'bah courtyard. Quraish leaders in circle, smiling warmly. Close beside Abdul Muthalib: {CAHAYA} The golden "محمد" calligraphy light, he extends hand toward it. Ka'bah wall background. Afternoon. All heads between 25%-65% height.
NO child figure. Muhammad = golden calligraphy light."""),

    ("e02-slide-12.png", f"""{S}
Scene: Simple Meccan room. Abdul Muthalib (elderly, white beard) lying on bed/mat LEFT, reaching out. Abu Thalib (younger, brown robe, kind face) standing RIGHT, hand on heart. Between them floating: {CAHAYA} The golden "محمد" calligraphy light being entrusted from one guardian to next. Oil lamp. Both men's heads between 30%-50% from top.
Muhammad = ONLY the golden calligraphy light. Only 2 humans. Mood: solemn trust."""),

    ("e02-slide-13.png", f"""{S}
Scene: Modest home interior. Abu Thalib (brown/beige robe, kind face) sitting with his children at modest meal — bread, dates, milk. Among them: {CAHAYA} The golden "محمد" calligraphy light makes the meal glow warmer. Abu Thalib smiling toward light. Cozy family scene. All heads between 25%-60% from top. Mood: love despite poverty."""),

    ("e02-slide-14.png", f"""{S}
Scene: Hilltop overlooking Makkah valley. Shepherd's staff planted in ground at CENTER. Around the staff: {CAHAYA} The golden "محمد" calligraphy light emanating around the staff. Sheep/goats (15-20) grazing peacefully, ALL fully visible between 30%-65% height. Baby goat near staff. Golden morning light. Makkah small in distance.
NO human figure. Staff + golden calligraphy light only. Mood: peaceful, humble."""),
]

for i, (fn, prompt) in enumerate(IMGS):
    print(f"\n🎨 [{i+1}/{len(IMGS)}] {fn}...")
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
        else:
            print("  ❌ No image")
    except Exception as e:
        print(f"  ❌ {e}")
    if (i+1) % 5 == 0:
        print("  ⏳ pause...")
        time.sleep(3)

print(f"\n✅ Done! {len(IMGS)} images.")
