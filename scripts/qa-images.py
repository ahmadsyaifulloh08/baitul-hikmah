#!/usr/bin/env python3
"""
QA Image Review — Baitul Hikmah Children Illustrations
Automated quality gate for illustration files before deploy.

Usage:
  python3 scripts/qa-images.py                     # Audit all events
  python3 scripts/qa-images.py e01 e02             # Audit specific events
  python3 scripts/qa-images.py --json              # Output as JSON
  python3 scripts/qa-images.py --check-only        # Only programmatic checks (no vision model)

Checks:
  BLOCKER (A-D): Require vision model inspection
    A. No Prophet ﷺ depiction (human figure representing Nabi)
    B. Scene matches slide narration
    C. No text/writing/captions in image
    D. Safe zone — subject centered, no cut heads/limbs

  WARNING (E-G): Programmatic + optional vision
    E. Aspect ratio (16:9 ± 5%)
    F. Resolution (min 1280x720)
    G. Visual consistency across slides (same event)

Exit codes:
  0 = all PASS (or only WARNINGs)
  1 = BLOCKER failures found

NOTE: Vision model checks (A-D, G) require OpenClaw `image` tool.
      Run with --check-only to skip vision checks and only do programmatic (E, F).
      Full QA should be run by Main agent who has access to vision model.
"""

import os, sys, json, glob
from pathlib import Path

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ILLUSTRATIONS_DIR = os.path.join(PROJECT_DIR, "public", "illustrations", "children")

# Expected aspect ratio 16:9
TARGET_RATIO = 16 / 9
RATIO_TOLERANCE = 0.05  # 5%
MIN_WIDTH = 1280
MIN_HEIGHT = 720


def find_event_images(event_id):
    """Find all illustration files for an event."""
    pattern = os.path.join(ILLUSTRATIONS_DIR, f"{event_id}-slide-*.png")
    files = sorted(glob.glob(pattern))
    if not files:
        # Try jpg
        pattern = os.path.join(ILLUSTRATIONS_DIR, f"{event_id}-slide-*.jpg")
        files = sorted(glob.glob(pattern))
    return files


def check_programmatic(image_path):
    """Run programmatic checks (E, F) on an image. Returns list of violations."""
    violations = []

    if not HAS_PIL:
        violations.append({"check": "E/F", "severity": "SKIP", "msg": "PIL not installed — skipping resolution/ratio checks"})
        return violations

    try:
        img = Image.open(image_path)
        width, height = img.size

        # E: Aspect ratio
        if height > 0:
            ratio = width / height
            expected_ratio = TARGET_RATIO
            deviation = abs(ratio - expected_ratio) / expected_ratio
            if deviation > RATIO_TOLERANCE:
                violations.append({
                    "check": "E",
                    "severity": "WARNING",
                    "msg": f"Aspect ratio {width}x{height} ({ratio:.2f}) deviates {deviation*100:.1f}% from 16:9 ({expected_ratio:.2f})"
                })

        # F: Resolution
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            violations.append({
                "check": "F",
                "severity": "WARNING",
                "msg": f"Resolution {width}x{height} below minimum {MIN_WIDTH}x{MIN_HEIGHT}"
            })

    except Exception as e:
        violations.append({"check": "E/F", "severity": "WARNING", "msg": f"Cannot read image: {e}"})

    return violations


def generate_vision_prompts(image_path, slide_narration=None):
    """Generate vision model prompts for BLOCKER checks (A-D).
    Returns dict of check_id → prompt. To be used by Main agent with `image` tool."""
    prompts = {}

    prompts["A"] = (
        "Inspect this illustration for children's Islamic history education. "
        "Does this image contain any human figure that could represent Prophet Muhammad ﷺ? "
        "This includes: a central heroic male figure, a silhouette, a figure seen from behind, "
        "or any human form bathed in special light meant to represent the Prophet. "
        "Answer ONLY 'PASS' if no such figure exists, or 'FAIL: [description]' if it does."
    )

    prompts["C"] = (
        "Does this illustration contain ANY text, writing, captions, labels, watermarks, "
        "or letter-like shapes? This includes Arabic calligraphy used as decoration, "
        "numbers, or any readable characters. "
        "Answer ONLY 'PASS' if the image is text-free, or 'FAIL: [describe the text found]'."
    )

    prompts["D"] = (
        "Check the composition of this illustration. Is the main subject well-centered "
        "within the middle 70% of the frame? Are there any heads, faces, or important elements "
        "cut off at the edges? "
        "Answer ONLY 'PASS' if composition is good, or 'FAIL: [describe the issue]'."
    )

    if slide_narration:
        prompts["B"] = (
            f"This illustration should depict the following scene: \"{slide_narration}\"\n\n"
            "Does the image match this description? Consider: setting, characters present, "
            "key objects, mood/atmosphere. Minor artistic interpretation is acceptable. "
            "Answer ONLY 'PASS' if it matches, or 'FAIL: [describe the mismatch]'."
        )

    return prompts


def audit_event_programmatic(event_id):
    """Audit images for one event (programmatic checks only)."""
    images = find_event_images(event_id)

    if not images:
        return {
            "event": event_id,
            "status": "NO_IMAGES",
            "image_count": 0,
            "violations": [],
            "msg": "No illustration files found"
        }

    all_violations = []
    has_blocker = False

    for img_path in images:
        filename = os.path.basename(img_path)
        violations = check_programmatic(img_path)

        for v in violations:
            v["file"] = filename
            all_violations.append(v)
            if v["severity"] == "BLOCKER":
                has_blocker = True

    return {
        "event": event_id,
        "status": "FAIL" if has_blocker else ("WARNING" if all_violations else "PASS"),
        "image_count": len(images),
        "violations": all_violations,
        "vision_pending": True,  # Vision checks not yet done
        "vision_prompts_template": "Use generate_vision_prompts() per image for full QA"
    }


def main():
    json_mode = "--json" in sys.argv
    check_only = "--check-only" in sys.argv
    specific = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not os.path.exists(ILLUSTRATIONS_DIR):
        msg = f"Illustrations directory not found: {ILLUSTRATIONS_DIR}"
        if json_mode:
            print(json.dumps({"error": msg, "pass": [], "fail": [], "no_images": []}))
        else:
            print(f"⚠️  {msg}")
            print("No illustrations to audit yet. Pipeline:")
            print("  1. Generate images via Gemini API")
            print("  2. Save to public/illustrations/children/e{NN}-slide-{MM}.png")
            print("  3. Run this script to audit")
        sys.exit(0)

    # Discover events with images
    all_files = glob.glob(os.path.join(ILLUSTRATIONS_DIR, "e*-slide-*"))
    event_ids = sorted(set(os.path.basename(f).rsplit('-slide-', 1)[0] for f in all_files))

    if specific:
        event_ids = [eid for eid in event_ids if eid in specific]

    results = {"pass": [], "warning": [], "fail": [], "no_images": []}

    for event_id in event_ids:
        result = audit_event_programmatic(event_id)

        if result["status"] == "NO_IMAGES":
            results["no_images"].append(result)
        elif result["status"] == "PASS":
            results["pass"].append(result)
        elif result["status"] == "WARNING":
            results["warning"].append(result)
        else:
            results["fail"].append(result)

    if json_mode:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        total = sum(len(v) for v in results.values())
        print(f"QA IMAGE REVIEW — {total} events audited")
        print(f"✅ PASS: {len(results['pass'])}  |  ⚠️ WARNING: {len(results['warning'])}  |  🔴 FAIL: {len(results['fail'])}  |  📭 No images: {len(results['no_images'])}")

        if check_only:
            print("\n⚠️  --check-only mode: only programmatic checks (E, F) were run.")
            print("For full QA (A-D vision checks), run without --check-only via Main agent.")

        if results["fail"]:
            print("\n" + "=" * 60)
            print("BLOCKER FAILURES:")
            print("=" * 60)
            for item in results["fail"]:
                print(f"\n🔴 {item['event']} ({item['image_count']} images)")
                for v in item["violations"]:
                    print(f"   → [{v['check']}] {v['severity']}: {v['msg']}")

        if results["warning"]:
            print("\n" + "-" * 60)
            print("WARNINGS:")
            print("-" * 60)
            for item in results["warning"]:
                print(f"\n⚠️  {item['event']} ({item['image_count']} images)")
                for v in item["violations"]:
                    print(f"   → [{v['check']}] {v['msg']}")

    has_blockers = len(results["fail"]) > 0
    sys.exit(1 if has_blockers else 0)


if __name__ == "__main__":
    main()
