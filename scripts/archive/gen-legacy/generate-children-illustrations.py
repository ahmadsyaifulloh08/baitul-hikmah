#!/usr/bin/env python3
"""Generate 28 children slideshow illustrations using Gemini image generation."""

import json
import base64
import time
import urllib.request
import urllib.error
import os

API_KEY = "AIzaSyCQAtJXP4I3FaHAf_9mks3OFl6w0KyQgYM"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"
OUTPUT_DIR = "/workspace/projects/baitul-hikmah/public/illustrations/children"

STYLE_PREFIX = "Warm watercolor storybook illustration for children age 6-12. 16:9 landscape aspect ratio. Soft edges, stylized art (not photorealistic). Arabian 6th century setting. Sandy gold, warm beige, dusty earth tones. "

BRIEFS = {
    "e01-slide-01": "Abrahah (Yemeni king in ornate red/gold robe, short dark beard, golden crown, arrogant posture) standing proudly in front of the grand al-Qullays church in Sana'a, Yemen. Massive pillars, gold ornaments, domed roof. Mountains of Sana'a in background. Mood: proud but hollow.",
    "e01-slide-02": "Split composition: LEFT side shows a grand ornate church (empty, no visitors). RIGHT side shows streams of Arab travelers on camels heading toward a distant Ka'bah (simple stone cube) in golden light. Contrast between ignored grandeur and beloved simplicity.",
    "e01-slide-03": "Military camp in Yemen. Abrahah (red/gold robe, golden crown) on a raised platform giving orders. Rows of war elephants being prepared with war saddles. The biggest elephant Mahmud (dark gray, red war saddle with gold cloth) stands front and center, towering over others. Soldiers lining up. Mood: menacing preparation.",
    "e01-slide-04": "Long marching column crossing desert LEFT TO RIGHT. A massive dark gray war elephant with red/gold saddle leads at front, trunk raised. Behind: smaller elephants, cavalry, infantry with banners. Dust clouds rising. Hijaz hills in distance. Tiny silhouette of Makkah far right on horizon. Mood: overwhelming military power.",
    "e01-slide-05": "Soldiers seizing 200 camels from a grazing field near Makkah. Camels being herded away by soldiers. In the background, outskirts of Makkah visible. A few Arab herders watch helplessly. Mood: aggression, theft.",
    "e01-slide-06": "Inside ornate military tent. An elderly dignified Arab leader (white robe, white beard, calm noble posture — Abdul Muthalib) faces Abrahah (red/gold robe, golden crown, seated on throne, surrounded by guards, looking surprised). Between them: tension. Through tent opening: camels visible outside. Mood: dignity vs power.",
    "e01-slide-07": "Close-up dramatic moment inside a tent: an elderly Arab man with white beard raises his hand in calm certainty. A king in red/gold robe leans forward in disbelief. Light coming through tent opening illuminating the elder. Mood: unshakeable faith. Different angle from a standard tent meeting.",
    "e01-slide-08": "A massive dark gray war elephant KNEELING on the ground, front legs folded, head bowed LOW. The elephant FACES TOWARD a distant Ka'bah (simple cube visible ahead) but REFUSES to move forward. Handler on top whipping desperately but elephant won't budge. Other elephants behind also stopping, confused. Desert ground. Mood: divine intervention.",
    "e01-slide-09": "Sky FILLED with hundreds of small dark birds (ababil) flying in formation from above. Each bird carries 3 small glowing reddish stones (1 in beak, 1 in each claw). Stones raining down on panicking soldiers below. Dramatic sky — dark storm on one side, golden light over Ka'bah on other side. Mood: divine punishment, awe-inspiring.",
    "e01-slide-10": "Aftermath scene: abandoned military equipment scattered on desert ground — broken saddles, torn banners, empty armor. No dead bodies (children-friendly). Dust settling. In the distance, Ka'bah stands untouched, bathed in golden light. A few birds still circling in sky. Mood: aftermath, Ka'bah protected.",
    "e01-slide-11": "Night scene in Makkah. A simple stone house with WARM GOLDEN LIGHT emanating from within — glowing through windows and door, spreading outward. Night sky filled with extraordinarily bright stars, one brilliant star directly above the house. Crescent moon. Silhouette of Makkah rooftops, Ka'bah faintly visible. A few women (from behind) walking toward the house. NO baby, NO human figure of the Prophet. Only LIGHT from inside the house.",
    "e01-slide-12": "Symbolic artistic composition: Ka'bah at center, protected by a dome of golden light. Around it: remnants of broken elephant armor (past), bright star above (birth), and radiating timeline markers spreading outward. Desert landscape stretching to horizon. Dawn sky. Mood: significance, legacy, hope.",
    "e02-slide-01": "A simple fresh grave mound with plain stone marker in an oasis of Yatsrib (ancient Madinah). Date palms casting long shadows (late afternoon). A few travelers' belongings (merchant bags, water flask) left near the grave. Golden-orange sunset sky, melancholic. Buildings of ancient Yatsrib in background. Mood: sad but peaceful.",
    "e02-slide-02": "Still-life scene: five camels, a few goats, and a small bundle of belongings arranged in a simple courtyard in Makkah. Morning light. Empty — the owner is gone. A woman's shadow falls across the ground near the animals. Simple, sparse. Mood: modest inheritance, absence.",
    "e02-slide-03": "Market/gathering scene in Makkah. Several Bedouin women arriving on donkeys and camels, looking at babies held by Meccan mothers. Busy, colorful scene. Women examining, negotiating. Focus on the social activity. Mood: lively tradition.",
    "e02-slide-04": "A Bedouin woman (brown/cream clothing, kind face — Halimah) sitting alone on the edge of a gathering, looking dejected. Other Bedouin women walking away with babies. Her thin donkey and skinny goat nearby. Dry, barren look to her belongings. Late afternoon. Mood: disappointment, poverty.",
    "e02-slide-05": "A Bedouin woman (Halimah, brown/cream clothing) standing near a Meccan house, being handed a bundle of white cloth. A WARM GOLDEN GLOW emanates from the bundle. Her expression: surprised, touched. NO baby face or body visible, just cloth bundle with golden light. Mood: turning point, quiet miracle.",
    "e02-slide-06": "Transformation scene: a Bedouin camp in the desert, but everything is LUSH and GREEN (unusual for desert). Fat healthy goats grazing on green grass. Full milk containers. Well-maintained tent. A warm golden glow emanates from near the tent. Other tents in background look dry/normal by comparison. Mood: miraculous blessing, abundance.",
    "e02-slide-07": "A brilliant COLUMN OF WHITE-GOLDEN LIGHT rising from the ground up to the sky in an open desert field. NO human figure inside or near the light — pure divine nur. Two luminous glowing white forms (angels — no facial features) kneeling on either side of the light column. Sheep/goats in distance looking toward the light. Sky opening above with bright blue circle of clear sky. Mood: supernatural, sacred, awe-inspiring.",
    "e02-slide-08": "A Bedouin woman (Halimah, brown/cream clothing) on a donkey traveling along a desert road toward Makkah (city visible ahead). She carries a bundle with golden glow. Her expression: worried, protective. Desert road stretching behind her. Mood: concern, maternal protection.",
    "e02-slide-09": "A small caravan (2-3 camels) setting out from Makkah. A young woman (Aminah, modest dress) riding a camel with a covered howdah/sedan. A golden light sits beside her in the howdah. A dark-skinned woman (Ummu Aiman) walking alongside. Road ahead stretches toward distant hills. Morning light. Mood: mother-son journey, bittersweet. NO physical child shown.",
    "e02-slide-10": "Desert roadside between Makkah and Madinah. A camel sedan stopped. A dark-skinned woman (Ummu Aiman, from behind) kneeling beside the sedan, head bowed in grief. A SMALL GOLDEN LIGHT stands alone in the vast empty desert — dim but not extinguished. A pair of small sandals on the ground near the light. Purple/orange melancholic sunset sky. Distant road stretching both ways. Mood: deep sadness, loneliness. NO child figure.",
    "e02-slide-11": "A dark-skinned woman (Ummu Aiman, Ethiopian, simple modest clothing, protective posture) walking on foot along a desert road toward Makkah (visible ahead). She leads a camel. A warm golden glow travels beside her. Stars appearing in dusky sky. Her shadow stretches long. She looks determined despite exhaustion. Mood: devotion, protection, resilience.",
    "e02-slide-12": "An elderly man (Abdul Muthalib, white beard, white robe) sitting on a carpet near Ka'bah courtyard. Other Quraish leaders sitting in a circle, some smiling warmly. A WARM GOLDEN LIGHT sits close beside the elder — he has one hand gently extended toward it. Ka'bah wall visible in background. Afternoon light. Mood: love, warmth, grandfather's devotion. NO child figure.",
    "e02-slide-13": "An elderly man's hand reaching out from a bed/mat, pointing toward a younger man (Abu Thalib — brown robe, kind face) who stands nearby with hand on heart accepting responsibility. A small golden light between them — being entrusted. Simple Meccan room, oil lamp, muted colors. Mood: passing of guardianship, solemn trust.",
    "e02-slide-14": "Simple modest home interior. A kind-faced man in brown/beige robe (Abu Thalib) sitting with his children at a modest meal — bread, dates, milk. A golden warm light among them. The light makes the modest meal glow warmer. Abu Thalib smiling toward the light. Cozy family scene. Mood: love despite poverty, warmth. NO physical child representing the Prophet.",
    "e02-slide-15": "Hilltop overlooking Makkah valley. A shepherd's staff planted in the ground with GOLDEN LIGHT emanating around it. A flock of 15-20 sheep/goats grazing peacefully in the valley below. One baby goat standing close to the staff/light. Golden morning hour light from behind. Small bag of provisions on the ground. Makkah city small in the distance. Mood: peaceful, humble. NO human figure.",
    "e02-slide-16": "Symbolic artistic composition: A SMALL BUT STEADY GOLDEN LIGHT in the center of a desert, facing a LARGE RISING SUN on the horizon. From the point of light, flowers and green plants grow outward across the sand in all directions. Sky transitions from dark/starry (left) to bright golden dawn (right). Birds flying in morning sky. Within the rising sun, faint outlines of a great city. Mood: hope, destiny, from hardship grows greatness. NO human silhouette.",
}

def generate_image(slide_id, prompt):
    """Generate one image via Gemini API."""
    full_prompt = STYLE_PREFIX + prompt
    payload = json.dumps({
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }).encode("utf-8")
    
    req = urllib.request.Request(API_URL, data=payload, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        return False, str(e)
    
    # Extract base64 image from response
    try:
        candidates = data.get("candidates", [])
        for candidate in candidates:
            parts = candidate.get("content", {}).get("parts", [])
            for part in parts:
                if "inlineData" in part:
                    b64 = part["inlineData"]["data"]
                    img_bytes = base64.b64decode(b64)
                    out_path = os.path.join(OUTPUT_DIR, f"{slide_id}.png")
                    with open(out_path, "wb") as f:
                        f.write(img_bytes)
                    print(f"  ✅ Saved {out_path} ({len(img_bytes)} bytes)")
                    return True, out_path
        return False, f"No image in response: {json.dumps(data)[:300]}"
    except Exception as e:
        return False, str(e)

def main():
    results = {"success": [], "failed": []}
    total = len(BRIEFS)
    
    for i, (slide_id, prompt) in enumerate(BRIEFS.items(), 1):
        print(f"\n[{i}/{total}] Generating {slide_id}...")
        
        # Check if already exists
        out_path = os.path.join(OUTPUT_DIR, f"{slide_id}.png")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
            print(f"  ⏭️ Already exists, skipping")
            results["success"].append(slide_id)
            continue
        
        ok, msg = generate_image(slide_id, prompt)
        if not ok:
            print(f"  ❌ Failed: {msg[:200]}")
            print(f"  🔄 Retrying in 5s...")
            time.sleep(5)
            ok, msg = generate_image(slide_id, prompt)
            if not ok:
                print(f"  ❌ Retry failed: {msg[:200]}")
                results["failed"].append(slide_id)
                continue
        
        results["success"].append(slide_id)
        time.sleep(2)  # Rate limiting
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(results['success'])}/{total} succeeded, {len(results['failed'])}/{total} failed")
    if results["success"]:
        print(f"✅ Success: {', '.join(results['success'])}")
    if results["failed"]:
        print(f"❌ Failed: {', '.join(results['failed'])}")

if __name__ == "__main__":
    main()
