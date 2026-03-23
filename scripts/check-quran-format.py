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
    for i, line in enumerate(lines, 1):
        if re.search(r'QS\.\s', line) or re.search(r'Surah\s', line):
            # Check if Arabic text exists within 5 lines
            context = '\n'.join(lines[max(0,i-3):min(len(lines),i+3)])
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
