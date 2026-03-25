#!/usr/bin/env python3
"""Regenerate ALL 27 images with safe zone composition + no text."""
import json, base64, urllib.request, os, time

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT_DIR = "/workspace/projects/baitul-hikmah/public/illustrations/children"

S = """Warm watercolor storybook illustration for children age 6-12. Soft edges, stylized (not photorealistic). Arabian 6th century. Sandy gold, warm beige, dusty earth.
CRITICAL: No text, words, letters, signatures of any kind.
COMPOSITION: The TOP 22% and BOTTOM 22% of this image will be CROPPED. ALL important subjects (heads, faces, key objects) MUST be in the CENTER 56% vertical band. Keep edges clear — only sky/ground/background at edges."""

IMAGES = [
    # === E01 ===
    ("e01-slide-01.png", f"""{S}
Scene: Abrahah (red/gold robe, golden crown, short dark beard) standing proudly in front of the grand al-Qullays church. Massive pillars, gold ornaments, domed roof. Mountains of Sana'a behind. His HEAD at vertical center, not near top edge. Mood: proud but hollow."""),

    ("e01-slide-02.png", f"""{S}
Scene: Split composition. LEFT: grand ornate church (empty, no visitors). RIGHT: streams of Arab travelers on camels heading toward a distant Ka'bah (simple cube) in golden light. Contrast between ignored grandeur and beloved simplicity. All figures in center band. Desert landscape."""),

    ("e01-slide-03.png", f"""{S}
Scene: Military camp. Abrahah (red/gold robe, crown) on platform CENTER giving orders. His head at VERTICAL CENTER, not near top. War elephants around — Mahmud (biggest, dark gray, red saddle) front center. Soldiers lining up. Sky above and ground below are expendable edges. Mood: menacing."""),

    ("e01-slide-04.png", f"""{S}
Scene: Soldiers seizing 200 camels from a grazing field near Makkah. Camels being herded by soldiers. Outskirts of Makkah in background. Arab herders watching helplessly. All figures in center band. Mood: aggression, theft."""),

    ("e01-slide-05.png", f"""{S}
Scene: Inside ornate military tent. Abdul Muthalib (white robe, white beard, standing calm) LEFT faces Abrahah (seated on throne, red/gold robe, crown) RIGHT. Guards behind. Through tent opening: camels. All heads in CENTER band — tent ceiling NOT visible. Mood: dignity vs power."""),

    ("e01-slide-06.png", f"""{S}
Scene: Mahmud the elephant KNEELING, front legs folded, head bowed. He FACES TOWARD Ka'bah (visible ahead) but REFUSES to move. Handler on top whipping but elephant won't budge. Other elephants behind stopping. All subjects in center band. Mood: divine intervention.
CRITICAL: Elephant faces TOWARD Ka'bah but kneels. Ka'bah AHEAD of elephant."""),

    ("e01-slide-07.png", f"""{S}
Scene: Elephant Mahmud STANDING but REFUSING to walk toward Ka'bah. Turns body AWAY. Ka'bah visible behind the elephant. Handler pulling reins desperately. Soldiers confused. All in center band. Desert setting. Mood: divine intervention.
Elephant is STANDING (not kneeling), body angled AWAY from Ka'bah."""),

    ("e01-slide-08.png", f"""{S}
Scene: Wide sky. Hundreds of small dark birds (ababil) filling CENTER of sky in formation. Each carries small glowing reddish stones. Stones raining on panicking soldiers below (center-bottom). LEFT: dark storm. RIGHT: golden light over Ka'bah. Birds concentrated in MIDDLE band, NOT at top edge. Mood: divine punishment."""),

    ("e01-slide-09.png", f"""{S}
Scene: Aftermath — abandoned military equipment on desert ground. Broken saddles, torn banners, empty armor. No dead bodies (children-friendly). Dust settling. In distance: Ka'bah untouched, bathed in golden light. Birds circling. All elements in center band. Mood: Ka'bah protected."""),

    ("e01-slide-10.png", f"""{S}
Scene: Night in Makkah. Simple stone house CENTER with WARM GOLDEN LIGHT from windows and door. Bright star ABOVE house but at CENTER of image (NOT near top edge). Makkah rooftops at same height. Women (from behind) walking toward house. Star and house both in center 56%.
CRITICAL: NO baby, NO human figure for Prophet. Only LIGHT from house. Mood: sacred night."""),

    ("e01-slide-11.png", f"""{S}
Scene: Peaceful pastoral Bani Sa'd desert. Simple Bedouin tent CENTER with warm golden glow from inside. Fat healthy sheep and goats grazing around. Green patches. Sunset sky. NO human figures. Tent and animals in center band. Mood: divine blessing, abundance."""),

    ("e01-slide-12.png", f"""{S}
Scene: Symbolic. Ka'bah CENTER protected by dome of golden light. Dome stays within center 70%, NOT touching top edge. Around: broken elephant armor (left), bright star (within center), dawn horizon. Desert landscape. Mood: significance, hope."""),

    # === E02 ===
    ("e02-slide-01.png", f"""{S}
Scene: Simple fresh grave mound with stone marker in oasis of Yatsrib. Date palms casting shadows. Travelers' belongings near grave. Golden-orange sunset. Buildings of Yatsrib background. All in center band. Mood: sad but peaceful."""),

    ("e02-slide-02.png", f"""{S}
Scene: Still-life courtyard. Five camels, few goats, small bundle of belongings. Morning light. Empty — owner gone. Ummu Aiman's shadow on ground. All animals in center band. Mood: modest inheritance."""),

    ("e02-slide-03.png", f"""{S}
Scene: Market in Makkah. Bedouin women on donkeys/camels, looking at babies held by Meccan mothers. Busy, colorful. All figures with heads in CENTER band — no heads near top, no baskets at very bottom edge. Stone buildings backdrop. Mood: lively tradition."""),

    ("e02-slide-04.png", f"""{S}
Scene: Halimah (brown/cream clothing, kind face, head covering) being handed a bundle of white cloth with WARM GOLDEN GLOW. Near a Meccan house. Halimah surprised, touched. Figures in center band.
CRITICAL: NO baby face/body visible. Just cloth bundle with golden light. Mood: turning point."""),

    ("e02-slide-05.png", f"""{S}
Scene: Halimah's camp in desert, but LUSH and GREEN. Fat goats on green grass. Full milk containers. Tent well-maintained. Golden glow near tent (Muhammad's presence — NO physical form). Other tents in background look dry/normal. All in center band. Mood: miraculous blessing."""),

    ("e02-slide-06.png", f"""{S}
Scene: Desert field. COLUMN OF WHITE-GOLDEN LIGHT from ground, rising but contained in center 56% — fades before top edge. Two glowing white silhouettes (angels, no faces) kneeling at base, positioned at vertical CENTER. Sheep/goats nearby. Children running to tents in background. All in center band.
CRITICAL: NO physical form of Muhammad. Pure light column only."""),

    ("e02-slide-07.png", f"""{S}
Scene: Halimah (brown/cream clothing) on donkey traveling desert road toward Makkah. She carries bundle with golden glow (Muhammad — no physical form). Worried, protective expression. Desert road behind. All in center band. Mood: concern, maternal protection."""),

    ("e02-slide-08.png", f"""{S}
Scene: Small caravan (2-3 camels) from Makkah. Aminah (young woman, modest dress) riding camel with howdah. Small golden light beside her in howdah (Muhammad — NOT a child). Ummu Aiman walking alongside. Road to hills ahead. Morning light. Center band.
CRITICAL: Muhammad ONLY as golden light. Mood: bittersweet journey."""),

    ("e02-slide-09.png", f"""{S}
Scene: Ummu Aiman (dark-skinned, Ethiopian, protective) walking on desert road toward Makkah (ahead). Leads camel. Warm golden glow beside her (Muhammad — NOT a child). Dusky twilight sky. Shadow stretches long. Determined despite exhaustion. Center band.
CRITICAL: Muhammad ONLY as golden glow. Mood: devotion."""),

    ("e02-slide-10.png", f"""{S}
Scene: Courtyard of Meccan house. Abdul Muthalib (elderly, white beard, white robe) sits ALONE on cushion under palm tree. Next to him: warm GOLDEN ORB of pure light. He gazes at orb with tenderness. Evening light. Woven carpet beneath. He is the ONLY human figure.
CRITICAL: NO other humans. NO children. Golden orb = pure light, not human-shaped. Center band."""),

    ("e02-slide-11.png", f"""{S}
Scene: Abdul Muthalib (elderly, white beard, white robe) sitting on carpet near Ka'bah courtyard. Quraish leaders in circle, smiling. WARM GOLDEN LIGHT beside Abdul Muthalib, he extends hand toward it. Ka'bah wall background. Afternoon. All heads in center band.
CRITICAL: NO child figure. Golden light only."""),

    ("e02-slide-12.png", f"""{S}
Scene: Elderly man's hand (Abdul Muthalib) reaching from bed/mat, pointing toward younger man (Abu Thalib — brown robe, kind face) standing with hand on heart. Small golden light between them. Simple Meccan room, oil lamp. All in center band. Mood: solemn trust."""),

    ("e02-slide-13.png", f"""{S}
Scene: Simple modest home. Abu Thalib (brown/beige robe, kind face) sitting with children at modest meal — bread, dates, milk. Golden warm light among them (Muhammad). Light makes meal glow warmer. Abu Thalib smiling toward light. Cozy family. All heads in center band. Mood: love despite poverty."""),

    ("e02-slide-14.png", f"""{S}
Scene: Hilltop overlooking Makkah valley. Shepherd's staff planted in ground with GOLDEN LIGHT around it (Muhammad — NO human). Sheep/goats grazing in valley. Baby goat near staff. Golden morning light. Bag of provisions. Makkah distant below. Staff and animals in center band.
CRITICAL: NO human figure. Staff + golden light only."""),

    ("e02-slide-15.png", f"""{S}
Scene: Symbolic desert. Small GOLDEN LIGHT ORB at center. LARGE RISING SUN at right HORIZON (vertical center). Flowers and green plants grow from light across sand, all at center height. Dawn sky transition dark-to-golden. Birds at center height. Horizon at vertical center. All elements in center band.
CRITICAL: NO human silhouette. Pure light + nature."""),
]

for i, (filename, prompt) in enumerate(IMAGES):
    print(f"\n🎨 [{i+1}/27] Generating {filename}...")
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }).encode()
    
    req = urllib.request.Request(URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read())
        
        saved = False
        for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                with open(os.path.join(OUT_DIR, filename), "wb") as f:
                    f.write(img_data)
                print(f"  ✅ {len(img_data)} bytes")
                saved = True
                break
        if not saved:
            print("  ❌ No image")
            if 'error' in data:
                print(f"  Error: {data['error'].get('message','')}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Small delay to avoid rate limiting
    if (i + 1) % 5 == 0:
        print("  ⏳ Rate limit pause...")
        time.sleep(3)

print(f"\n✅ Done! Generated 27 images.")
