#!/usr/bin/env python3
"""Generate 12 children slideshow illustrations via Gemini 2.0 Flash image generation API."""

import json
import base64
import time
import os
import urllib.request
import urllib.error

API_KEY = "AIzaSyDWljXsGmgFVkgIbWHojs9Eab_zqRPc0YU"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent?key={API_KEY}"
OUTPUT_DIR = "/workspace/projects/baitul-hikmah/public/illustrations/children"
os.makedirs(OUTPUT_DIR, exist_ok=True)

STYLE = "Warm watercolor storybook illustration for children age 6-12, 16:9 landscape format, soft edges, no realistic human faces, stylized/silhouette figures. Arabian 6th century setting. No text or writing in the image."

SLIDES = [
    ("e01-slide-1", "A proud king Abrahah standing before his magnificent grand church al-Qullays in Sana'a Yemen. The church has tall pillars, golden ornaments, domed roof, extremely lavish. Abrahah seen from the side/behind wearing luxurious red and gold royal robes with a crown, hand raised proudly. In the far background, a tiny simple cube silhouette of the Kaaba for contrast. Yemen mountains behind. Mood: arrogant grandeur, cold despite the rich colors."),
    
    ("e01-slide-2", "A massive army marching LEFT TO RIGHT through the Arabian desert toward Makkah. Leading the army is Mahmud, the LARGEST war elephant, much bigger than the others, with a red war saddle, trunk raised, marching right. Behind him a long column of soldiers on horses, smaller elephants, war banners flying. Dust clouds from the march. Far right in the distance, a tiny silhouette of Makkah/Kaaba showing their destination. Hot sun, threatening atmosphere. The army moves FROM LEFT TO RIGHT toward the city."),
    
    ("e01-slide-3", "Inside a large military tent, two figures meet. On the left, Abdul Muttalib - an elderly dignified man with white beard, simple white/cream robes, standing tall and calm with confident posture seen from the side. On the right, Abrahah sitting on an ornate throne/chair, wearing luxurious clothes, looking surprised with raised eyebrows. Guards behind Abrahah. Through the tent opening, camels visible outside. Lanterns inside the tent. Mood: contrast between worldly power and spiritual dignity."),
    
    ("e01-slide-4", "Dramatic climax scene. Bottom left: the great elephant Mahmud KNEELING on the ground, front legs folded, head bowed LOW, FACING TOWARD the Kaaba but REFUSING to advance. His handler on top panicking, whipping but elephant won't move. Other elephants behind also stopped. In the distance to the right, the Kaaba stands simple and firm. In the sky above, a massive flock of small dark birds (Ababil) flying in formation, each carrying 3 small glowing reddish stones (1 in beak, 1 in each claw). Sky dramatic - dark stormy on one side, bright light over the Kaaba. Supernatural, awe-inspiring mood."),
    
    ("e01-slide-5", "Night scene of the birth of Prophet Muhammad in Makkah. A simple stone/clay Arab house in center with warm golden light glowing softly from windows and door - special ethereal light spreading outward. A narrow Makkah street at night with stone pavement. One or two women figures (seen from behind) walking toward the house. Sky full of extraordinarily bright stars, crescent moon, one brightest star directly above the house. Silhouette of Makkah rooftops, faint Kaaba in background. Mood: sacred, peaceful, hopeful, beautiful. NO baby or face shown - just the light symbolizing the birth."),
    
    ("e02-slide-1", "A simple fresh grave mound with a plain headstone in an oasis in Yathrib (ancient Medina). Wet fresh earth. Date palm trees casting long afternoon shadows. Several figures in travel clothes standing around the grave with bowed heads, seen from behind/side. In background, ancient Yathrib city with clay buildings and green date palm gardens. Sunset sky in melancholic orange/purple. Near the grave, a traveler's bag/merchant supplies left behind - symbolizing Abdullah died during a trade journey young. Mood: sad but peaceful, not dramatically tragic."),
    
    ("e02-slide-2", "Halimah the Bedouin wet nurse (seen from behind/side, wearing simple brown/cream Bedouin clothes with headscarf) holding a white cloth bundle (baby, no face visible) near a simple Bedouin tent. In foreground, fat healthy goats grazing on GREEN grass (unusual for desert - showing blessing). Full milk containers. Background: Bani Sa'd desert but surprisingly green and lush, bright sky with white clouds, other Bedouin tents in distance. Halimah's livestock visibly healthier/bigger than neighbors'. Mood: warm, blessed, magical but natural, like spring arrived in the desert."),
    
    ("e02-slide-3", "Supernatural sacred scene. A small child (age 3-4, seen from BEHIND/far away, wearing simple white clothes) lying in a grassy meadow. A very bright white-golden column of LIGHT emanating from his chest upward into the sky. Two glowing white light silhouettes (angels - NO detail, just luminous human-shaped forms) kneeling beside the child. Foreground: desert grass and small wildflowers. Goats in distance looking toward the light. Sky split open above with brilliant blue and sunrays, clouds forming a circle above. Far corner: tiny silhouettes of other children running away toward tents in fear. Mood: supernatural, sacred, awe-inspiring, not frightening. Light dominates."),
    
    ("e02-slide-4", "Deeply melancholic desert scene. A small child (Muhammad age 6, seen from BEHIND) standing alone in vast empty desert, small figure with slightly drooped shoulders and bowed head, his long shadow on the sand (low sun). To the right, a stopped camel litter/sedan with cloth slightly open. A woman figure (Ummu Aiman, from behind) kneeling beside the litter, head bowed in grief. Background: barren desert path between Makkah and Madinah, purple/orange twilight sky. Very far in distance, faint silhouette of Makkah. Travel supplies, camel tracks in sand. A small child's sandal on the ground. Mood: deeply sad, lonely, but not hopeless - subtle, respectful, not traumatic for child readers."),
    
    ("e02-slide-5", "Warm family scene at the Kaaba courtyard. Abdul Muttalib (elderly, dignified, white beard, clean white robes) sitting on a carpet/mat near the Kaaba. Young Muhammad (age 6-8, seen from behind/side, white/cream simple clothes) sitting very close beside his grandfather - showing closeness and affection. Foreground: patterned carpet, cushions, dates and drinks. On both sides, other Quraysh leaders sitting in a circle (seen from side, various Arab clothing), some smiling looking at grandfather and grandson. Background: Kaaba wall partially visible, clear evening sky, ancient Makkah stone houses. Mood: warm, loving, family, peaceful moment amid loss."),
    
    ("e02-slide-6", "Young Muhammad (age 10-12, seen from BEHIND, standing on a small hill) holding a shepherd's staff, watching a flock of 15-20 goats grazing in a valley below. Simple, slightly worn clothes showing humble life but dignity. Golden morning light (golden hour) from behind creating a golden silhouette. Background: Makkah's reddish-brown rocky hills, clear morning sky with thin clouds, tiny Makkah visible in the valley far away. A small food bag on the ground beside his feet. A baby goat standing close to his feet showing bond with animals. Mood: peaceful, independent, reflective, simple beauty of shepherd life."),
    
    ("e02-slide-7", "Symbolic/artistic composition - NOT a literal scene. Center: silhouette of a small child standing alone in the desert, facing a LARGE golden SUNRISE on the horizon. Small but upright posture showing resilience. Sky transitions from dark (night/stars) on the LEFT to bright (golden dawn) on the RIGHT - symbolizing journey from sorrow to hope. On the ground: flowers and green plants growing from the child's footprints in the sand - symbolizing goodness growing from orphanhood. In the sunrise light, faint silhouette of a great city/civilization visible. Birds flying in the morning sky (normal birds, not Ababil). Last star still visible on the dark side. Mood: hopeful, inspiring, majestic yet simple."),
]

def generate_image(filename, prompt):
    full_prompt = f"{STYLE} {prompt}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }).encode()
    
    req = urllib.request.Request(ENDPOINT, data=payload, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        return False, str(e)
    
    # Extract image
    try:
        parts = data["candidates"][0]["content"]["parts"]
        for part in parts:
            if "inlineData" in part and part["inlineData"]["mimeType"].startswith("image/"):
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                out_path = os.path.join(OUTPUT_DIR, f"{filename}.png")
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                print(f"✅ {filename} saved ({len(img_bytes)} bytes)")
                return True, ""
        return False, "No image in response parts"
    except (KeyError, IndexError) as e:
        # Dump partial response for debugging
        text_parts = []
        try:
            for p in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                if "text" in p:
                    text_parts.append(p["text"][:200])
        except:
            pass
        return False, f"{e} | response text: {text_parts} | keys: {list(data.keys())}"


def main():
    results = {"success": [], "failed": []}
    
    for i, (filename, prompt) in enumerate(SLIDES):
        print(f"\n[{i+1}/12] Generating {filename}...")
        ok, err = generate_image(filename, prompt)
        if not ok:
            print(f"❌ Failed: {err}. Retrying...")
            time.sleep(5)
            ok, err = generate_image(filename, prompt)
        
        if ok:
            results["success"].append(filename)
        else:
            print(f"❌ FAILED after retry: {err}")
            results["failed"].append((filename, err))
        
        # Rate limit: wait between calls
        if i < len(SLIDES) - 1:
            time.sleep(3)
    
    print(f"\n{'='*50}")
    print(f"SUMMARY: {len(results['success'])}/12 succeeded, {len(results['failed'])}/12 failed")
    if results["failed"]:
        for name, err in results["failed"]:
            print(f"  ❌ {name}: {err}")

if __name__ == "__main__":
    main()
