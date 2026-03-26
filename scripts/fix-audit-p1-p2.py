#!/usr/bin/env python3
"""
Phase 1+2: Fix duplicate Al-Quran entries + truncated surah names in bibliography.
- Remove OLD format Al-Quran entries (without parentheses/surah numbers)
- Keep NEW format (with surah number + ayat)
- Re-number bibliography entries after removal
- Update ^N references in body accordingly
"""
import os, re, sys

CONTENT_DIR = 'content/events'
DRY_RUN = '--dry-run' in sys.argv

def find_quran_entries(bib_text):
    """Find all Al-Quran entries with their line numbers."""
    entries = []
    for line in bib_text.strip().split('\n'):
        line = line.strip()
        m = re.match(r'^(\d+)\.\s+(.*)', line)
        if m and re.search(r'Al-Qur.?an', line, re.IGNORECASE):
            num = int(m.group(1))
            text = m.group(2)
            has_parens = bool(re.search(r'\(\d+\)', text))  # has (17): format
            entries.append({'num': num, 'text': text, 'full_line': line, 'has_parens': has_parens})
    return entries

def fix_file(fpath):
    with open(fpath) as f:
        content = f.read()
    
    # Split into body and bibliography
    bib_markers = ['## Daftar Pustaka', '## Bibliography', '## References']
    bib_marker = None
    for marker in bib_markers:
        if marker in content:
            bib_marker = marker
            break
    
    if not bib_marker:
        return False, "no bibliography"
    
    parts = content.split(bib_marker, 1)
    body = parts[0]
    bib_section = parts[1]
    
    quran_entries = find_quran_entries(bib_section)
    
    if len(quran_entries) < 2:
        # Check for truncated surah name in single entry
        if len(quran_entries) == 1:
            entry = quran_entries[0]
            if not entry['has_parens']:
                # Has QS. but no parentheses — truncated
                # We can't auto-fix the surah name without context, just flag it
                return False, f"single truncated entry: {entry['full_line'][:60]}"
        return False, "no duplicates"
    
    # Multiple quran entries — keep the one with parentheses (NEW format)
    new_format = [e for e in quran_entries if e['has_parens']]
    old_format = [e for e in quran_entries if not e['has_parens']]
    
    if not old_format:
        return False, "all entries have parens (no old format to remove)"
    
    if not new_format:
        # All are old format — keep the last one (usually most complete)
        old_format = old_format[:-1]  # remove all but last
        if not old_format:
            return False, "only old format entries, keeping last"
    
    # Remove old format entries from bibliography
    nums_to_remove = set(e['num'] for e in old_format)
    
    # Parse all bib entries
    bib_lines = bib_section.strip().split('\n')
    new_bib_lines = []
    removed_nums = set()
    
    for line in bib_lines:
        m = re.match(r'^(\d+)\.\s+', line.strip())
        if m:
            num = int(m.group(1))
            if num in nums_to_remove:
                removed_nums.add(num)
                continue
        new_bib_lines.append(line)
    
    if not removed_nums:
        return False, "nothing to remove"
    
    # Build renumber map
    old_nums = []
    for line in bib_section.strip().split('\n'):
        m = re.match(r'^(\d+)\.\s+', line.strip())
        if m:
            old_nums.append(int(m.group(1)))
    
    remaining_nums = [n for n in old_nums if n not in removed_nums]
    renumber_map = {}
    for new_idx, old_num in enumerate(remaining_nums, 1):
        renumber_map[old_num] = new_idx
    
    # Renumber bibliography lines
    final_bib_lines = []
    for line in new_bib_lines:
        m = re.match(r'^(\d+)(\.\s+)', line.strip())
        if m:
            old_num = int(m.group(1))
            if old_num in renumber_map:
                line = line.replace(f'{old_num}.', f'{renumber_map[old_num]}.', 1)
        final_bib_lines.append(line)
    
    # Update ^N references in body
    new_body = body
    # Sort by descending number to avoid replacement conflicts
    for old_num in sorted(renumber_map.keys(), reverse=True):
        new_num = renumber_map[old_num]
        if old_num != new_num:
            # Replace ^OLD with temporary placeholder
            new_body = re.sub(rf'\^{old_num}(?!\d)', f'^__TEMP_{new_num}__', new_body)
    
    # Also handle removed nums — remove their citations or point to nearest
    for removed in removed_nums:
        new_body = re.sub(rf'\^{removed}(?!\d)', '', new_body)
    
    # Replace placeholders
    new_body = re.sub(r'\^__TEMP_(\d+)__', r'^\1', new_body)
    
    # Reconstruct
    new_content = new_body + bib_marker + '\n'.join(final_bib_lines)
    
    if not DRY_RUN:
        with open(fpath, 'w') as f:
            f.write(new_content)
    
    return True, f"removed {len(removed_nums)} old entries, renumbered {len(renumber_map)} entries"

# Main
fixed = 0
skipped = 0
errors = []

for event_folder in sorted(os.listdir(CONTENT_DIR)):
    event_path = os.path.join(CONTENT_DIR, event_folder)
    if not os.path.isdir(event_path):
        continue
    
    for fname in ['general-id.md', 'general-en.md']:
        fpath = os.path.join(event_path, fname)
        if not os.path.exists(fpath):
            continue
        
        try:
            success, msg = fix_file(fpath)
            if success:
                fixed += 1
                print(f'  ✅ {event_folder}/{fname}: {msg}')
            else:
                skipped += 1
        except Exception as e:
            errors.append(f'{event_folder}/{fname}: {e}')
            print(f'  ❌ {event_folder}/{fname}: ERROR {e}')

print(f'\n{"DRY RUN - " if DRY_RUN else ""}Fixed: {fixed}, Skipped: {skipped}, Errors: {len(errors)}')
