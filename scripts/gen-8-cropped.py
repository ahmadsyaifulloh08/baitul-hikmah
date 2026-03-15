#!/usr/bin/env python3
"""Regenerate 8 cropped images with 16:9 ratio + safe zone + no text."""
import json, base64, urllib.request, os

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT_DIR = "/workspace/projects/baitul-hikmah/public/illustrations/children"

STYLE = """Warm watercolor storybook illustration for children age 6-12. Soft edges, stylized (not photorealistic). Arabian 6th century setting. Sandy gold, warm beige, dusty earth palette.
Image ratio: exactly 16:9 landscape (wide). Resolution: 1792x1024 or similar.
CRITICAL: Do NOT include ANY text, words, letters, labels, captions, titles, signatures, or writing of any kind.
COMPOSITION: Place ALL important subjects (faces, heads, key objects, main characters) within the CENTER 70% of the image. Keep the outer edges (top 15%, bottom 15%, left 15%, right 15%) clear of important details — only background/sky/ground at edges. The image will be displayed fullscreen and edges WILL be cropped."""

IMAGES = [
    {
        "file": "e01-slide-03.png",
        "prompt": f"""{STYLE}

Scene: Military camp in Yemen, wide panoramic view. Abrahah (red/gold robe, golden crown, short dark beard) standing on a raised platform in the CENTER of the image giving orders — his full body visible, head well below the top edge. Rows of war elephants being prepared on both sides. Mahmud (biggest elephant, dark gray, red war saddle) front and center. Soldiers lining up. Keep all heads and elephants in the central band. Sky and ground at edges only. Mood: menacing preparation."""
    },
    {
        "file": "e01-slide-05.png",
        "prompt": f"""{STYLE}

Scene: Inside an ornate military tent, wide interior shot. Abdul Muthalib (white robe, white beard, standing tall and calm) on the LEFT facing Abrahah (seated on throne, red/gold robe, golden crown) on the RIGHT. Guards behind Abrahah. Through tent opening in background: camels visible. All figures positioned in the CENTER of the frame — heads at least 25% below the top edge. Tent ceiling NOT visible (cropped above frame). Floor visible but not critical. Mood: dignity vs power, tension."""
    },
    {
        "file": "e01-slide-08.png",
        "prompt": f"""{STYLE}

Scene: Wide panoramic sky scene. Hundreds of small dark birds (ababil) filling the CENTER of the sky, flying in formation. Each bird carries small glowing reddish stones. Stones raining down on panicking soldiers below (small figures at bottom-center). On the LEFT: dark storm clouds. On the RIGHT: golden light over a distant Ka'bah (simple stone cube). The birds are concentrated in the MIDDLE band of the image, not at the top edge. Ground with soldiers at bottom-center, not at very bottom edge. Mood: divine punishment, awe-inspiring."""
    },
    {
        "file": "e01-slide-10.png",
        "prompt": f"""{STYLE}

Scene: Night scene in Makkah, wide horizontal composition. A simple stone house in the CENTER with WARM GOLDEN LIGHT emanating from within — glowing through windows and door. Night sky with bright stars — but the brightest star is positioned at CENTER-TOP of the image (not at the very top edge). Crescent moon to the side, also within center band. Silhouette of Makkah rooftops on both sides (low, at center height). A few women (from behind, small) walking toward the house. Keep all elements well within center 70%. Mood: sacred night, hope.
CRITICAL: NO baby, NO human figure representing the Prophet. Only LIGHT from inside house."""
    },
    {
        "file": "e01-slide-12.png",
        "prompt": f"""{STYLE}

Scene: Symbolic wide composition. Ka'bah (simple stone cube) at CENTER, protected by a dome of golden light. The golden dome stays within the center 70% — does NOT touch the top edge. Around the Ka'bah: remnants of broken elephant armor on the ground (left), a bright star above (but within center area, NOT at top edge). Dawn sky with warm colors — horizon at center height. Desert landscape stretching to both sides. Mood: significance, legacy, hope. Keep all symbolic elements centered."""
    },
    {
        "file": "e02-slide-03.png",
        "prompt": f"""{STYLE}

Scene: Wide market/gathering scene in ancient Makkah. Several Bedouin women on donkeys/camels in the CENTER, looking at babies held by Meccan mothers. Busy, colorful scene. All figures positioned with heads and feet well within the center 70% — no heads near top edge, no important items on the ground at bottom edge. Stone buildings of Makkah as backdrop at center height. Morning light. Keep ground-level items (baskets, pottery) in center band, not at very bottom. Mood: lively cultural tradition."""
    },
    {
        "file": "e02-slide-06.png",
        "prompt": f"""{STYLE}

Scene: Wide open desert field in Bani Sa'd. A brilliant COLUMN OF WHITE-GOLDEN LIGHT rising from the ground in the CENTER — but the column stays within the center 70% vertically (does NOT extend to the very top of the image, fades before reaching top edge). Two luminous silhouettes (angels — no facial features, just glowing white forms) kneeling on either side of the light column. Sheep/goats in the middle distance. Children running away toward tents in far background. A circle of bright blue sky above the column but NOT at the top edge. Mood: supernatural, sacred.
CRITICAL: NO physical form of Muhammad. Pure light column only. Column contained within center area."""
    },
    {
        "file": "e02-slide-15.png",
        "prompt": f"""{STYLE}

Scene: Wide symbolic composition. A SMALL STEADY GOLDEN LIGHT in the CENTER of a desert, facing a LARGE RISING SUN on the right horizon. The sun is positioned at CENTER-RIGHT, NOT at the top edge. From the golden light, flowers and green plants grow outward across the sand — all within the center band. Sky transitions from dusky (left) to golden dawn (right) — but stars/moon are in the center area, NOT at top edge. Birds flying at center height. Faint city outlines within the sun. Keep ALL elements in center 70%. Mood: hope, destiny.
CRITICAL: NO human silhouette. Pure light + nature symbolism."""
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
            if 'error' in data:
                print(f"  Error: {data['error'].get('message','')}")
            else:
                for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                    if "text" in part:
                        print(f"  Text: {part['text'][:200]}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n✅ Done generating 8 images!")
