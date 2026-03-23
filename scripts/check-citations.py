#!/usr/bin/env python3
"""
Citation QA checker — run after content generation.
Verifies consolidated citation format.

Usage: python3 scripts/check-citations.py [event-slug]
       python3 scripts/check-citations.py  # check all
"""
import os, re, sys, glob

def check_file(filepath):
    with open(filepath) as f:
        text = f.read()
    
    errors = []
    filename = os.path.basename(filepath)
    event = os.path.basename(os.path.dirname(filepath))
    
    # 1. Find all inline citations
    citations = re.findall(r'\^(\d+)', text)
    if not citations:
        return []  # No citations = skip (e.g. children mode)
    
    max_cite = max(int(c) for c in citations)
    
    # 2. Count Daftar Pustaka / Bibliography entries
    # Match lines starting with "N. " after Daftar Pustaka/Bibliography header
    pustaka_section = re.search(r'(?:## Daftar Pustaka|## Bibliography)\s*\n([\s\S]+?)(?:\n## |\Z)', text)
    if not pustaka_section:
        errors.append(f"NO Daftar Pustaka/Bibliography section")
        return errors
    
    pustaka_lines = re.findall(r'^\d+\.\s+.+', pustaka_section.group(1), re.MULTILINE)
    pustaka_count = len(pustaka_lines)
    
    # 3. Check: max citation <= pustaka count
    if max_cite > pustaka_count:
        errors.append(f"Citation ^{max_cite} exceeds {pustaka_count} pustaka entries — NOT consolidated!")
    
    # 4. Check: no double citations without space (^1^2)
    doubles = re.findall(r'\^\d+\^\d+', text)
    if doubles:
        errors.append(f"Double citations without space: {doubles[:3]}")
    
    # 5. Check all citation numbers have matching pustaka entry
    used_numbers = set(int(c) for c in citations)
    for n in used_numbers:
        if n > pustaka_count:
            errors.append(f"Citation ^{n} has no matching pustaka entry")
    
    return errors

# Main
target = sys.argv[1] if len(sys.argv) > 1 else None
pattern = f"content/events/{target}/*.md" if target else "content/events/*/general-*.md"

files = sorted(glob.glob(pattern))
total_errors = 0

for f in files:
    errors = check_file(f)
    if errors:
        print(f"❌ {f}:")
        for e in errors:
            print(f"   {e}")
        total_errors += len(errors)

if total_errors == 0:
    print(f"✅ All {len(files)} files passed citation check")
else:
    print(f"\n⚠️ {total_errors} errors found in {len(files)} files")
    sys.exit(1)
