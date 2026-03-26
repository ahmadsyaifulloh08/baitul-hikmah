#!/usr/bin/env python3
"""Phase 3: Fix double citations without space: ^5^4 → ^5 ^4"""
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
        
        # Fix ^N^M → ^N ^M (add space between adjacent citations)
        new_content = re.sub(r'\^(\d+)\^(\d+)', r'^\1 ^\2', content)
        # Handle triple: ^N^M^O
        new_content = re.sub(r'\^(\d+)\^(\d+)', r'^\1 ^\2', new_content)
        
        if new_content != content:
            fixed += 1
            if not DRY_RUN:
                with open(fpath, 'w') as f:
                    f.write(new_content)
            print(f'  ✅ {event_folder}/{fname}')

print(f'\n{"DRY RUN - " if DRY_RUN else ""}Fixed: {fixed}')
