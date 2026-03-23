#!/usr/bin/env python3
"""
Citation & bibliography checker — unified article + card validation.

Checks BOTH article citations AND card display format in one script.

Rules enforced (from docs/content-style-guide.md Section 3):

Article checks:
- Consolidated bibliography: 1 source = 1 fixed number, reuse ^N
- Max citation ^N must <= number of bibliography entries
- No double citations without space (^1^2)
- Every cited ^N must have matching bibliography entry

Card checks (research_agenda.json sumber field):
- Format: "Title — Author" (no markdown asterisks)
- No duplicated names (same string both sides of separator)
- No empty entries
- Min 3 sources per event

See: docs/content-style-guide.md Section 3

Usage:
    python3 scripts/check-citations.py              # check all
    python3 scripts/check-citations.py e04           # specific event
    python3 scripts/check-citations.py --articles    # articles only
    python3 scripts/check-citations.py --cards       # cards only
"""
import os, re, sys, glob, json

# ─── Article Citation Check ───────────────────────────────────────

def check_article(filepath):
    with open(filepath) as f:
        text = f.read()
    
    errors = []
    citations = re.findall(r'\^(\d+)', text)
    if not citations:
        return []
    
    max_cite = max(int(c) for c in citations)
    
    pustaka_section = re.search(
        r'(?:## Daftar Pustaka|## Bibliography)\s*\n([\s\S]+?)(?:\n## |\Z)', text
    )
    if not pustaka_section:
        errors.append("NO Daftar Pustaka/Bibliography section")
        return errors
    
    pustaka_lines = re.findall(r'^\d+\.\s+.+', pustaka_section.group(1), re.MULTILINE)
    pustaka_count = len(pustaka_lines)
    
    if max_cite > pustaka_count:
        errors.append(f"Citation ^{max_cite} exceeds {pustaka_count} pustaka entries — NOT consolidated!")
    
    doubles = re.findall(r'\^\d+\^\d+', text)
    if doubles:
        errors.append(f"Double citations without space: {doubles[:3]}")
    
    used_numbers = set(int(c) for c in citations)
    for n in used_numbers:
        if n > pustaka_count:
            errors.append(f"Citation ^{n} has no matching pustaka entry")
    
    return errors

# ─── Card Pustaka Check ──────────────────────────────────────────

def check_cards(agenda_path="src/data/research_agenda.json"):
    with open(agenda_path) as f:
        data = json.load(f)
    
    all_errors = {}
    for ev in data["events"]:
        errors = []
        sumber = ev.get("sumber", [])
        eid = ev["id"]
        
        if len(sumber) < 3:
            errors.append(f"only {len(sumber)} sources (min 3)")
        
        for s in sumber:
            if "*" in s:
                errors.append(f"asterisk in: {s[:50]}")
            
            parts = s.split(" — ")
            if len(parts) == 2 and parts[0].strip() == parts[1].strip():
                errors.append(f"duplicated name: {s[:50]}")
            
            if " — " not in s and len(s) > 10:
                errors.append(f"no separator: {s[:50]}")
            
            if not s.strip():
                errors.append("empty entry")
        
        if errors:
            all_errors[eid] = errors
    
    return all_errors

# ─── Main ────────────────────────────────────────────────────────

target = None
mode = "all"  # all, articles, cards

for arg in sys.argv[1:]:
    if arg == "--articles":
        mode = "articles"
    elif arg == "--cards":
        mode = "cards"
    else:
        target = arg

total_errors = 0

# Article checks
if mode in ("all", "articles"):
    print("── Article Citations ──")
    pattern = f"content/events/{target}/*.md" if target else "content/events/*/general-*.md"
    files = sorted(glob.glob(pattern))
    article_errors = 0
    
    for f in files:
        errors = check_article(f)
        if errors:
            print(f"  ❌ {f}:")
            for e in errors:
                print(f"     {e}")
            article_errors += len(errors)
    
    if article_errors == 0:
        print(f"  ✅ All {len(files)} article files passed")
    total_errors += article_errors

# Card checks
if mode in ("all", "cards"):
    print("\n── Card Daftar Pustaka ──")
    card_errors = check_cards()
    
    if target:
        card_errors = {k: v for k, v in card_errors.items() if target.startswith(k) or k in target}
    
    if card_errors:
        for eid, errors in card_errors.items():
            print(f"  ❌ {eid}:")
            for e in errors:
                print(f"     {e}")
            total_errors += len(errors)
    else:
        with open("src/data/research_agenda.json") as f:
            count = len(json.load(f)["events"])
        print(f"  ✅ All {count} events passed card check")

# Summary
if total_errors == 0:
    print(f"\n✅ All pustaka checks passed")
else:
    print(f"\n⚠️ {total_errors} total errors")
    sys.exit(1)
