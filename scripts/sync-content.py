#!/usr/bin/env python3
"""
Sync content/events/*.md → src/data/event-content-map.json

SSoT: content/events/{slug}/*.md files
Output: src/data/event-content-map.json (consumed by EventContent.tsx)
Slug mapping: src/data/events-database.json (event.title → slugified key)

See: docs/README.md (Content Flow section)
See: docs/content-style-guide.md (content format rules)

Usage: python3 scripts/sync-content.py
Run after any content .md file changes.
"""
import json, os, glob, re, sys

EVENTS_DIR = "content/events"
OUTPUT = "src/data/event-content-map.json"
AGENDA = "src/data/events-database.json"

def slugify(title):
    s = title.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

# Load research agenda for slug mapping
with open(AGENDA) as f:
    agenda = json.load(f)

id_to_slug = {}
for ev in agenda["events"]:
    id_to_slug[ev["id"]] = slugify(ev["title"])

# Build content map from .md files
content_map = {}
updated = 0

for event_dir in sorted(glob.glob(f"{EVENTS_DIR}/e*/")):
    folder = os.path.basename(event_dir.rstrip("/"))
    eid = folder.split("-")[0]
    title_slug = id_to_slug.get(eid, "")
    
    if not title_slug:
        print(f"  WARN: {folder} — no matching event in events-database.json")
        continue
    
    content = {}
    for prefix in ["general", "children"]:
        for lang in ["en", "id"]:
            for ext in [".md", ".mdx"]:
                fpath = os.path.join(event_dir, f"{prefix}-{lang}{ext}")
                if os.path.exists(fpath):
                    with open(fpath) as f:
                        text = f.read().strip()
                    if len(text) > 50:
                        content[f"{prefix}-{lang}"] = text
                    break
    
    if content:
        content_map[title_slug] = content
        updated += 1

# Write output
with open(OUTPUT, "w") as f:
    json.dump(content_map, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Synced {updated} events to {OUTPUT}")
print(f"File size: {os.path.getsize(OUTPUT) / 1024:.0f}KB")
