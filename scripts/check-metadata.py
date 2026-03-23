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

# metadata.json no longer exists per event — all data in events-database.json
# This checker now validates events-database.json entries
REQUIRED_DB_FIELDS = ["id", "title", "year", "era", "sources", "status"]

# Also check events-database.json status consistency
def check_status_consistency():
    """Verify status field matches actual content existence."""
    import json as _json
    errors = []
    db_path = "src/data/events-database.json"
    if not os.path.exists(db_path):
        return errors
    
    with open(db_path) as f:
        db = _json.load(f)
    
    for ev in db.get("events", []):
        eid = ev["id"]
        status = ev.get("status", "draft")
        
        # Find content folder
        content_dirs = glob.glob(f"content/events/{eid}-*/")
        has_content = False
        for d in content_dirs:
            has_general = os.path.exists(f"{d}general-id.md") or os.path.exists(f"{d}general-id.mdx")
            has_children = os.path.exists(f"{d}children-id.md") or os.path.exists(f"{d}children-id.mdx")
            if has_general and has_children:
                has_content = True
                break
        
        if status == "published" and not has_content:
            errors.append(f"{eid}: status=published but no content files")
        elif status == "draft" and has_content:
            errors.append(f"{eid}: status=draft but has content — update to published")
    
    return errors
EXPECTED_FILES = ["general-id", "general-en", "children-id", "children-en"]

def check_event_db():
    """Check events-database.json entries."""
    with open("src/data/events-database.json") as f:
        db = json.load(f)
    
    all_errors = {}
    for ev in db["events"]:
        # Draft events only need id, title, year, status
        is_draft = ev.get("status") == "draft"
        check_fields = ["id", "title", "year", "status"] if is_draft else REQUIRED_DB_FIELDS
        
        errors = []
        for field in check_fields:
            if field not in ev or (not ev[field] and ev[field] != 0):
                errors.append(f"missing field: {field}")
        if errors:
            all_errors[ev["id"]] = errors
    return all_errors

def check_event_content(event_dir):
    slug = os.path.basename(event_dir.rstrip("/"))
    warnings = []
    
    for prefix in EXPECTED_FILES:
        found = False
        for ext in [".md", ".mdx"]:
            if os.path.exists(os.path.join(event_dir, f"{prefix}{ext}")):
                found = True
                break
        if not found:
            warnings.append(f"missing {prefix}.md")
    
    return warnings

target = sys.argv[1] if len(sys.argv) > 1 else None
pattern = f"content/events/{target}/" if target else "content/events/e*/"
dirs = sorted(glob.glob(pattern))

total_errors = 0
total_warnings = 0

# Check events-database.json
print("── Events Database ──")
db_errors = check_event_db()
for eid, errors in db_errors.items():
    print(f"  ❌ {eid}: {', '.join(errors)}")
    total_errors += len(errors)
if not db_errors:
    import json as _json
    with open("src/data/events-database.json") as f:
        count = len(_json.load(f)["events"])
    print(f"  ✅ All {count} events in database OK")

# Check content files
print("\n── Content Files ──")
for d in dirs:
    warnings = check_event_content(d)
    slug = os.path.basename(d.rstrip("/"))
    if warnings:
        print(f"  ⚠️ {slug}: {', '.join(warnings)}")
        total_warnings += len(warnings)

if total_warnings == 0:
    print(f"  ✅ All {len(dirs)} event folders have complete content")

if total_errors > 0:
    print(f"\n❌ {total_errors} errors")
    sys.exit(1)
elif total_warnings > 0:
    print(f"\n⚠️ {total_warnings} warnings (non-blocking)")
else:
    print(f"\n✅ All metadata checks passed")
