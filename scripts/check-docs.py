#!/usr/bin/env python3
"""
Documentation consistency checker — detect stale references.

Checks all docs and code for references to deleted/renamed files or fields.

See: docs/README.md (project structure)

Usage: python3 scripts/check-docs.py
"""
import os, re, sys, glob

STALE_PATTERNS = [
    ("research_agenda.json", "→ renamed to events-database.json"),
    ("event-content.json", "→ archived, use event-content-map.json"),
    ("image-briefs-children.md", "→ deleted, use docs/briefs/ per-episode"),
    ("metadata.json", "→ merged into events-database.json"),
    ("event.sumber", "→ renamed to event.sources"),
    (".sumber", "→ renamed to .sources (in code)"),
    ("check-pustaka-card.py", "→ merged into check-citations.py"),
]

SCAN_DIRS = ["docs/", "src/", "scripts/"]
SCAN_EXTS = [".md", ".tsx", ".ts", ".js", ".py"]
SKIP_DIRS = ["archive", "node_modules", ".next", ".git"]

errors = []

for scan_dir in SCAN_DIRS:
    for root, dirs, files in os.walk(scan_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not any(fname.endswith(ext) for ext in SCAN_EXTS):
                continue
            fpath = os.path.join(root, fname)
            with open(fpath) as f:
                try:
                    content = f.read()
                except:
                    continue
            
            for pattern, fix in STALE_PATTERNS:
                # Skip if pattern is in the stale checker itself
                if "check-docs.py" in fpath:
                    continue
                matches = [(i+1, line.strip()[:80]) for i, line in enumerate(content.split("\n")) if pattern in line]
                for line_num, line_text in matches:
                    # Skip comments that explain the migration
                    if "renamed" in line_text.lower() or "archived" in line_text.lower() or "merged" in line_text.lower():
                        continue
                    errors.append(f"  {fpath}:{line_num}: '{pattern}' {fix}")

if errors:
    print(f"❌ Found {len(errors)} stale references:\n")
    for e in errors:
        print(e)
    sys.exit(1)
else:
    print("✅ All docs and code references are current")
