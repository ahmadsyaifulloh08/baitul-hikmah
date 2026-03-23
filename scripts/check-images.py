#!/usr/bin/env python3
"""
Image checker — verify illustration files exist and meet size standards.

Rules enforced (from docs/operations/batch-image-generation-v4.md):
- Images in public/illustrations/children/{event}/slide-NN.png
- Target size: 1-2MB per image (match E01)
- Format: PNG, 16:9 landscape

Usage: python3 scripts/check-images.py [event-slug]
"""
import os, sys, glob

EVENTS_WITH_IMAGES = {
    "e01": 11, "e02": 15, "e03": 11, "e04": 12
}
SIZE_MIN = 200 * 1024       # 200KB min
SIZE_MAX = 3 * 1024 * 1024  # 3MB max

def check_event(event_id, expected_count):
    errors = []
    img_dir = f"public/illustrations/children/{event_id}"
    
    if not os.path.isdir(img_dir):
        errors.append(f"Missing folder: {img_dir}")
        return errors
    
    images = sorted(glob.glob(f"{img_dir}/slide-*.png"))
    
    if len(images) != expected_count:
        errors.append(f"Expected {expected_count} images, found {len(images)}")
    
    for img in images:
        size = os.path.getsize(img)
        name = os.path.basename(img)
        if size < SIZE_MIN:
            errors.append(f"{name}: too small ({size//1024}KB < 200KB)")
        if size > SIZE_MAX:
            errors.append(f"{name}: too large ({size//1024//1024:.1f}MB > 3MB)")
    
    return errors

target = sys.argv[1] if len(sys.argv) > 1 else None
total_errors = 0

if target:
    eid = target.split("-")[0]
    if eid in EVENTS_WITH_IMAGES:
        errors = check_event(eid, EVENTS_WITH_IMAGES[eid])
        if errors:
            print(f"❌ {eid}:")
            for e in errors:
                print(f"   {e}")
            total_errors += len(errors)
else:
    for eid, count in sorted(EVENTS_WITH_IMAGES.items()):
        errors = check_event(eid, count)
        if errors:
            print(f"❌ {eid}:")
            for e in errors:
                print(f"   {e}")
            total_errors += len(errors)
        else:
            print(f"✅ {eid}: {count} images OK")

if total_errors == 0:
    print(f"\n✅ All image checks passed")
else:
    print(f"\n⚠️ {total_errors} errors found")
    sys.exit(1)
