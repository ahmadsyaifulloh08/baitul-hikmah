#!/usr/bin/env python3
"""Phase 5: Add missing Al-Quran entry to pustaka for events that have QS. refs."""
import os, re, sys

CONTENT_DIR = 'content/events'
DRY_RUN = '--dry-run' in sys.argv
fixed = 0

for event_folder in sorted(os.listdir(CONTENT_DIR)):
    event_path = os.path.join(CONTENT_DIR, event_folder)
    if not os.path.isdir(event_path): continue
    
    for fname in ['general-id.md', 'general-en.md']:
        fpath = os.path.join(event_path, fname)
        if not os.path.exists(fpath): continue
        
        with open(fpath) as f:
            content = f.read()
        
        # Check if has QS. references
        qs_refs = re.findall(r'QS\.\s+([^,\n]+?)(?:\s*[\n,;])', content)
        if not qs_refs:
            continue
        
        # Check if already has Al-Quran in bibliography
        bib_markers = ['## Daftar Pustaka', '## Bibliography', '## References']
        has_bib = any(m in content for m in bib_markers)
        if not has_bib:
            continue
        
        bib_marker = next(m for m in bib_markers if m in content)
        bib_section = content.split(bib_marker, 1)[1]
        
        has_quran_entry = bool(re.search(r'Al-Qur.?an', bib_section, re.IGNORECASE))
        if has_quran_entry:
            continue
        
        # Need to add Al-Quran entry
        # Find max entry number
        nums = re.findall(r'^(\d+)\.', bib_section, re.MULTILINE)
        max_num = max(int(n) for n in nums) if nums else 0
        new_num = max_num + 1
        
        # Collect all QS. refs from body
        all_qs = re.findall(r'QS\.\s+([A-Za-z\'\-\s]+)\s*\((\d+)\)\s*:\s*([\d\-,\s]+)', content)
        if all_qs:
            qs_parts = '; '.join(f'QS. {name.strip()} ({num}): {ayat.strip()}' for name, num, ayat in all_qs)
        else:
            # Simpler format
            all_qs_simple = re.findall(r'QS\.\s+([^\n,;]+)', content)
            qs_parts = '; '.join(set(f'QS. {q.strip()}' for q in all_qs_simple[:5]))
        
        quran_entry = f'\n{new_num}. Al-Qur\'an al-Karim. {qs_parts}.\n'
        
        # Append to bibliography
        new_content = content.rstrip() + quran_entry
        
        fixed += 1
        if not DRY_RUN:
            with open(fpath, 'w') as f:
                f.write(new_content)
        print(f'  ✅ {event_folder}/{fname}: added entry #{new_num}')

print(f'\n{"DRY RUN - " if DRY_RUN else ""}Fixed: {fixed}')
