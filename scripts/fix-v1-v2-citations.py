#!/usr/bin/env python3
"""
Fix V1 (unused bib entries) and V2 (orphan body refs) across all events.
- V1: Remove bib entries not cited in body, renumber remaining
- V2: Clamp body ^N refs to valid bib range, or remove if impossible
"""
import os, re, shutil

PROJECT = '/workspace/projects/baitul-hikmah/content/events'
DOCS = '/workspace/docs/content/events'

def fix_file(fp):
    with open(fp) as f:
        content = f.read()
    
    bib_header = 'Daftar Pustaka' if 'Daftar Pustaka' in content else 'Bibliography'
    parts = re.split(rf'(##\s*{bib_header})', content, maxsplit=1)
    if len(parts) < 3:
        return False
    
    body = parts[0]
    header = parts[1]
    bib = parts[2]
    
    # Parse bib entries
    entries = {}
    bib_lines_other = []
    for line in bib.split('\n'):
        m = re.match(r'(\d+)\.\s*(.+)', line.strip())
        if m:
            entries[int(m.group(1))] = m.group(2).strip()
        elif line.strip():
            bib_lines_other.append(line)
    
    if not entries:
        return False
    
    # Find body refs
    body_refs = set(int(x) for x in re.findall(r'\^(\d+)', body))
    bib_nums = set(entries.keys())
    
    # Check if there are issues
    unused = bib_nums - body_refs
    orphan = body_refs - bib_nums
    
    if not unused and not orphan:
        return False
    
    # Step 1: Keep only entries that are cited in body
    used_entries = {k: v for k, v in entries.items() if k in body_refs}
    
    # If body refs exist that don't have bib entries (V2), we need to handle them
    # Strategy: map orphan refs to the closest valid entry or remove them
    
    # Step 2: Build renumber map (old_num -> new_num)
    # Keep used entries, assign new sequential numbers
    old_to_new = {}
    new_num = 1
    for old_num in sorted(used_entries.keys()):
        old_to_new[old_num] = new_num
        new_num += 1
    
    # For orphan body refs (V2): map to last valid entry or remove
    max_new = new_num - 1
    
    # Step 3: Renumber body refs
    new_body = body
    # Process from highest to lowest to avoid collision
    all_old_nums = sorted(set(list(old_to_new.keys()) + list(orphan)), reverse=True)
    
    for old_num in all_old_nums:
        if old_num in old_to_new:
            new_n = old_to_new[old_num]
            if old_num != new_n:
                # Use a temp placeholder to avoid collision
                new_body = re.sub(rf'\^{old_num}(?!\d)', f'^TEMP{new_n}TEMP', new_body)
        else:
            # Orphan ref - remove the ^N
            new_body = re.sub(rf'\^{old_num}(?!\d)', '', new_body)
    
    # Replace temp placeholders
    new_body = re.sub(r'\^TEMP(\d+)TEMP', r'^\1', new_body)
    
    # Clean up double spaces from removed refs
    new_body = re.sub(r'  +', ' ', new_body)
    # Clean up patterns like ".." from removed refs
    new_body = re.sub(r'\.\.+', '.', new_body)
    
    # Step 4: Rebuild bib
    new_bib_lines = []
    new_num = 1
    for old_num in sorted(used_entries.keys()):
        new_bib_lines.append(f'{new_num}. {used_entries[old_num]}')
        new_num += 1
    
    # Reconstruct
    new_content = new_body + header + '\n\n' + '\n'.join(new_bib_lines) + '\n'
    
    with open(fp, 'w') as f:
        f.write(new_content)
    
    return True

total_fixed = 0
for d in sorted(os.listdir(PROJECT)):
    if not os.path.isdir(os.path.join(PROJECT, d)):
        continue
    
    for lang in ['general-id.md', 'general-en.md']:
        fp = os.path.join(PROJECT, d, lang)
        if not os.path.isfile(fp):
            continue
        
        if fix_file(fp):
            total_fixed += 1
            
            # Sync to docs
            docs_fp = os.path.join(DOCS, d, lang)
            if os.path.isdir(os.path.dirname(docs_fp)):
                shutil.copy2(fp, docs_fp)
            
            # Count new stats
            with open(fp) as f:
                content = f.read()
            parts = re.split(r'##\s*(?:Daftar Pustaka|Bibliography)', content, maxsplit=1)
            body_refs = set(int(x) for x in re.findall(r'\^(\d+)', parts[0])) if len(parts) > 1 else set()
            bib_entries = set(int(x) for x in re.findall(r'^(\d+)\.', parts[1], re.MULTILINE)) if len(parts) > 1 else set()
            unused = bib_entries - body_refs
            orphan = body_refs - bib_entries
            
            status = '✅' if not unused and not orphan else '⚠️'
            print(f'{status} {d}/{lang}: bib={len(bib_entries)}, used={len(body_refs & bib_entries)}, unused={len(unused)}, orphan={len(orphan)}')

print(f'\nTotal files fixed: {total_fixed}')
