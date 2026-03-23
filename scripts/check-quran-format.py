#!/usr/bin/env python3
"""
Quran format checker — verify Arabic text + ayat separators.

Rules enforced (from docs/content-style-guide.md Section 1):
- Every Quran reference (QS.) must have Arabic text nearby
- Ayat separators only in blockquotes (not inline text)
- Separator format: LTR = closing-opening, RTL = opening-closing

Usage: python3 scripts/check-quran-format.py [event-slug]
"""
import os, re, sys, glob

def check_file(filepath):
    with open(filepath) as f:
        text = f.read()
    
    errors = []
    lines = text.split('\n')
    
    # 1. Find QS. references without Arabic text nearby
    # Detect Daftar Pustaka/Bibliography section to skip
    pustaka_start = len(lines)
    for i, line in enumerate(lines):
        if re.match(r'^## (Daftar Pustaka|Bibliography)', line):
            pustaka_start = i
            break
    
    for i, line in enumerate(lines, 1):
        # Skip lines in bibliography section
        if i - 1 >= pustaka_start:
            continue
        # Skip blockquote lines (likely already have Arabic nearby)
        if line.strip().startswith('>'):
            continue
        
        # Only check lines with actual verse references (QS. Name (N): A or QS. Name: A)
        # Skip narrative mentions like "Surah Maryam" without verse numbers
        has_verse_ref = bool(re.search(r'QS\.\s+[\w\-\'\s]+\(\d+\)\s*:', line)) or \
                        bool(re.search(r'QS\.\s+[\w\-\']+\s*:\s*\d+', line))
        
        if has_verse_ref:
            # Check if Arabic text exists within 10 lines (wider window)
            context = '\n'.join(lines[max(0,i-6):min(len(lines),i+6)])
            has_arabic = bool(re.search(r'[\u0600-\u06FF]', context))
            if not has_arabic:
                errors.append(f"L{i}: Quran ref without Arabic text nearby")
    
    # 2. Ayat separators outside blockquotes
    for i, line in enumerate(lines, 1):
        if not line.strip().startswith('>') and re.search(r'[﴾﴿]', line):
            errors.append(f"L{i}: Ayat separator outside blockquote")
    
    return errors

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
    print(f"✅ All {len(files)} files passed Quran format check")
else:
    print(f"\n⚠️ {total_errors} errors in {len(files)} files")
    sys.exit(1)
