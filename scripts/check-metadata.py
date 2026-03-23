#!/usr/bin/env python3
"""
Metadata checker — verify all events have required files.

Rules enforced (from docs/README.md New Event Checklist):
- Every event folder must have metadata.json
- metadata.json must have: id, title_id, title_en, year, era, sources
- Every event should have general-id.md and general-en.md
- Every event should have children-id.md and children-en.md

Usage: python3 scripts/check-metadata.py [event-slug]
"""
import os, json, sys, glob

REQUIRED_META_FIELDS = ["id", "title_id", "title_en", "year", "era", "sources"]
EXPECTED_FILES = ["general-id", "general-en", "children-id", "children-en"]

def check_event(event_dir):
    slug = os.path.basename(event_dir.rstrip("/"))
    errors = []
    warnings = []
    
    # 1. metadata.json exists?
    meta_path = os.path.join(event_dir, "metadata.json")
    if not os.path.exists(meta_path):
        errors.append("NO metadata.json")
        return errors, warnings
    
    # 2. metadata.json has required fields?
    with open(meta_path) as f:
        meta = json.load(f)
    for field in REQUIRED_META_FIELDS:
        if field not in meta or not meta[field]:
            errors.append(f"metadata.json missing: {field}")
    
    # 3. Content files exist?
    for prefix in EXPECTED_FILES:
        found = False
        for ext in [".md", ".mdx"]:
            if os.path.exists(os.path.join(event_dir, f"{prefix}{ext}")):
                found = True
                break
        if not found:
            warnings.append(f"missing {prefix}.md")
    
    return errors, warnings

target = sys.argv[1] if len(sys.argv) > 1 else None
pattern = f"content/events/{target}/" if target else "content/events/e*/"
dirs = sorted(glob.glob(pattern))

total_errors = 0
total_warnings = 0

for d in dirs:
    errors, warnings = check_event(d)
    slug = os.path.basename(d.rstrip("/"))
    if errors or warnings:
        print(f"{'❌' if errors else '⚠️'} {slug}:")
        for e in errors:
            print(f"   ❌ {e}")
        for w in warnings:
            print(f"   ⚠️ {w}")
        total_errors += len(errors)
        total_warnings += len(warnings)

if total_errors == 0 and total_warnings == 0:
    print(f"✅ All {len(dirs)} events passed metadata check")
elif total_errors == 0:
    print(f"\n⚠️ {total_warnings} warnings in {len(dirs)} events (no errors)")
else:
    print(f"\n❌ {total_errors} errors, ⚠️ {total_warnings} warnings in {len(dirs)} events")
    sys.exit(1)
