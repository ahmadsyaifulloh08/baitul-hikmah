#!/usr/bin/env python3
"""Retry 4 images with stronger center composition."""
import json, base64, urllib.request, os

API_KEY = open('/workspace/credentials/api-gemini.txt').read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUT_DIR = "/workspace/projects/baitul-hikmah/public/illustrations/children"

STYLE = """Warm watercolor storybook illustration for children age 6-12. Soft edges, stylized (not photorealistic). Arabian 6th century. Sandy gold, warm beige, dusty earth palette.
CRITICAL: Do NOT include ANY text, words, letters, signatures.
MANDATORY COMPOSITION RULE: The image will be cropped — the TOP 22% and BOTTOM 22% will be REMOVED. ONLY the middle 56% vertical strip will be visible. ALL important content MUST be in this middle strip. Nothing important at the top or bottom of the image."""

IMAGES = [
    {
        "file": "e01-slide-03.png",
        "prompt": f"""{STYLE}

Scene: Wide military camp. In the CENTER MIDDLE of the image: Abrahah (red/gold robe, golden crown) on a platform giving orders. His HEAD must be at the VERTICAL CENTER of the image, not near the top. Elephants on both sides — Mahmud (biggest, dark gray, red saddle) front center. Soldiers around. All heads at vertical center. Sky above is just empty wash. Ground below is just sand. Mood: menacing preparation."""
    },
    {
        "file": "e01-slide-10.png",
        "prompt": f"""{STYLE}

Scene: Night scene in Makkah. A simple stone house in the EXACT CENTER of the image with WARM GOLDEN LIGHT glowing from windows and door. The bright star is DIRECTLY ABOVE the house but at the VERTICAL CENTER of the image (NOT near the top edge). Makkah rooftops at same height as house (center). Dark blue sky fills upper area (can be cropped — no important elements). Ground/street fills lower area (can be cropped). A few women walking toward house, positioned at center height. Mood: sacred night.
CRITICAL: NO baby, NO human figure. Only LIGHT from house. Star must be in center area."""
    },
    {
        "file": "e02-slide-06.png",
        "prompt": f"""{STYLE}

Scene: Desert field. A COLUMN OF WHITE-GOLDEN LIGHT in the CENTER of the image — the column starts at VERTICAL CENTER and rises upward but does NOT reach the top 22% of the image (it fades/dissipates before reaching the top edge). Two glowing white silhouettes (angels, no faces) kneeling at the BASE of the column — positioned at VERTICAL CENTER, not near the bottom edge. Sheep/goats nearby at center height. Desert sky above (can be cropped). Sand below (can be cropped). Mood: supernatural, sacred.
CRITICAL: NO physical form of Muhammad. Light column and angels must be ENTIRELY within the center 56% vertical band."""
    },
    {
        "file": "e02-slide-15.png",
        "prompt": f"""{STYLE}

Scene: Wide symbolic desert composition. At the CENTER: a small steady GOLDEN LIGHT ORB. To the RIGHT at HORIZON LEVEL (vertical center): a LARGE RISING SUN. From the golden light, flowers and green plants grow outward across sand — all at CENTER height. The horizon line is at the EXACT VERTICAL CENTER. Sky above horizon is warm dawn colors (can be cropped, no important elements). Sand below horizon has flowers (can be cropped at edges). NO stars or moon — just dawn colors. Birds flying at center height near the sun. Mood: hope, destiny.
CRITICAL: NO human silhouette. Keep ALL elements at vertical center band."""
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
                with open(os.path.join(OUT_DIR, img["file"]), "wb") as f:
                    f.write(img_data)
                print(f"  ✅ Saved {len(img_data)} bytes")
                break
        else:
            print("  ❌ No image")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n✅ Done!")
