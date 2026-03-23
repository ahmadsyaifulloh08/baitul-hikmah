#!/usr/bin/env python3
"""
Reusable image generation script for Baitul Hikmah children illustrations.

Usage:
  python3 scripts/generate-image.py --event e01 --slide 7 --prompt "scene description..."
  python3 scripts/generate-image.py --event e02 --slide 3 --prompt-file briefs/e02-03.txt
  python3 scripts/generate-image.py --event e01 --slide 7  # uses default brief from image-briefs-children-v3.md

All prompts automatically include: safe zone, no text, prophet rules.
"""
import urllib.request, urllib.error, base64, json, sys, shutil, argparse, os, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
API_KEY = open("/workspace/credentials/api-gemini.txt").read().strip()
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"

MANDATORY_SUFFIX = """

CRITICAL COMPOSITION — MUST FOLLOW: ALL important subjects (faces, heads, hands, key objects) MUST be placed in the CENTER 70% of the image. Their heads must NOT go above 30% from top. Leave generous empty space (sky/ceiling/background) in the TOP 25% of the image. Bottom 15% should be ground/floor only. All faces and important details must be between 25%-85% from top.

ABSOLUTELY NO TEXT of any kind in the image — no captions, labels, titles, watermarks, signatures, letters, numbers, or writing in any script. The image must be purely illustrative with zero text elements."""

PROPHET_SUFFIX = """

⚠️ If Prophet Muhammad appears in this scene: depict him ONLY as a BRILLIANTLY GLOWING GOLDEN ORB OF LIGHT with visible bright rays. Absolutely NO human figure, NO baby, NO child, NO face, NO silhouette, NO shadow of a person."""

def get_brief_from_file(event, slide):
    """Extract brief from image-briefs-children-v3.md"""
    brief_file = os.path.join(PROJECT_DIR, "design", "image-briefs-children-v3.md")
    if not os.path.exists(brief_file):
        return None
    content = open(brief_file).read()
    pattern = f"### {event}-slide-{slide:02d} —.*?\n(.*?)(?=\n### |$)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def main():
    parser = argparse.ArgumentParser(description="Generate Baitul Hikmah illustration")
    parser.add_argument("--event", required=True, help="Event ID (e01, e02, etc.)")
    parser.add_argument("--slide", required=True, type=int, help="Slide number")
    parser.add_argument("--prompt", help="Custom prompt text")
    parser.add_argument("--prompt-file", help="Read prompt from file")
    parser.add_argument("--no-backup", action="store_true", help="Skip backup of existing image")
    args = parser.parse_args()

    out_file = os.path.join(PROJECT_DIR, "public", "illustrations", "children",
                            f"{args.event}-slide-{args.slide:02d}.png")

    # Get prompt
    if args.prompt:
        prompt = args.prompt
    elif args.prompt_file:
        prompt = open(args.prompt_file).read().strip()
    else:
        brief = get_brief_from_file(args.event, args.slide)
        if brief:
            prompt = f"Create a children's book illustration in warm watercolor style with ink outlines.\n\nScene: {brief}\n\nStyle: Soft watercolor washes, warm earth tones (amber, ochre, cream), gentle ink outlines, storybook illustration for children aged 6-12."
        else:
            print(f"ERROR: No brief found for {args.event}-slide-{args.slide:02d} and no --prompt given")
            sys.exit(1)

    # Add mandatory rules
    prompt += MANDATORY_SUFFIX + PROPHET_SUFFIX

    print(f"Generating {args.event}-slide-{args.slide:02d}...")
    print(f"Output: {out_file}")

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["image", "text"]}
    }

    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
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
            # Backup
            if os.path.exists(out_file) and not args.no_backup:
                backup = out_file.replace(".png", "-backup.png")
                shutil.copy2(out_file, backup)
                print(f"Backed up to {backup}")
            with open(out_file, "wb") as f:
                f.write(img_bytes)
            print(f"✅ Saved ({len(img_bytes)} bytes)")
            return
    print("❌ No image in response")
    sys.exit(1)

if __name__ == "__main__":
    main()
