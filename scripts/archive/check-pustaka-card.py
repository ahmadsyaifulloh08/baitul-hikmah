#!/usr/bin/env python3
"""
Daftar Pustaka card format checker — verify research_agenda.json sumber field.

Rules enforced:
- Format: "Title — Author" (no markdown asterisks, no duplicated names)
- No empty entries
- Min 3 sources per event
- No asterisks (*) in sumber strings

See: docs/content-style-guide.md Section 3

Usage: python3 scripts/check-pustaka-card.py
"""
import json, sys, re

with open("src/data/research_agenda.json") as f:
    data = json.load(f)

total_errors = 0

for ev in data["events"]:
    errors = []
    sumber = ev.get("sumber", [])
    eid = ev["id"]
    
    # 1. Min 3 sources
    if len(sumber) < 3:
        errors.append(f"only {len(sumber)} sources (min 3)")
    
    for s in sumber:
        # 2. No asterisks
        if "*" in s:
            errors.append(f"asterisk in: {s[:50]}")
        
        # 3. No duplicated author pattern (exact same string both sides)
        parts = s.split(' — ')
        if len(parts) == 2 and parts[0].strip() == parts[1].strip():
            errors.append(f"duplicated name: {s[:50]}")
        
        # 4. Must have " — " separator
        if " — " not in s and len(s) > 10:
            errors.append(f"no separator: {s[:50]}")
        
        # 5. Not empty
        if not s.strip():
            errors.append("empty entry")
    
    if errors:
        print(f"❌ {eid}:")
        for e in errors:
            print(f"   {e}")
        total_errors += len(errors)

if total_errors == 0:
    print(f"✅ All {len(data['events'])} events passed pustaka card check")
else:
    print(f"\n⚠️ {total_errors} errors found")
    sys.exit(1)
