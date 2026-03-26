#!/usr/bin/env python3
"""
Fix V6 violation: Add Al-Qur'an al-Karim to Daftar Pustaka for events that cite QS. refs.

Also adds ^N citation to the line introducing the first Quran blockquote.
Handles both general-id.md and general-en.md.
Syncs fixes to docs/content/events/ as well.
Updates events-database.json card sources with quran entry.
"""

import os
import re
import json
import shutil

PROJECT_CONTENT = '/workspace/projects/baitul-hikmah/content/events'
DOCS_CONTENT = '/workspace/docs/content/events'
DB_PATH = '/workspace/projects/baitul-hikmah/src/data/events-database.json'


def extract_qs_refs(content):
    """Extract all QS. references from content."""
    refs = re.findall(r'QS\.\s*([A-Za-z][A-Za-z\'\-\s]+?)(?:\s*\((\d+)\))?\s*:\s*(\d+(?:\s*[-–]\s*\d+)?)', content)
    # Also catch refs like "— QS. Al-Fil (105): 1-5" and "— QS Al-Fil (105): 1-5"
    surah_set = {}
    for match in refs:
        surah_name = match[0].strip().rstrip(',').rstrip(';')
        surah_num = match[1] if match[1] else ''
        ayat = match[2]
        key = surah_name
        if key not in surah_set:
            surah_set[key] = {'name': surah_name, 'num': surah_num, 'ayats': []}
        surah_set[key]['ayats'].append(ayat)
    return surah_set


def get_max_bib_num(content):
    """Get the highest bibliography entry number."""
    parts = re.split(r'##\s*(?:Daftar Pustaka|Bibliography|References)', content, maxsplit=1)
    if len(parts) < 2:
        return 0
    bib = parts[1]
    nums = re.findall(r'^(\d+)\.', bib, re.MULTILINE)
    return max(int(n) for n in nums) if nums else 0


def has_quran_bib(content):
    """Check if bibliography already has Al-Qur'an al-Karim entry."""
    return bool(re.search(r'Al-Qur.an al-Karim', content, re.IGNORECASE))


def has_qs_refs(content):
    """Check if content has QS. references."""
    return bool(re.search(r'QS\.', content))


def build_quran_bib_entry(num, qs_refs):
    """Build the Al-Qur'an al-Karim bibliography entry."""
    parts = []
    for key, info in qs_refs.items():
        if info['num']:
            parts.append(f"QS. {info['name']} ({info['num']}): {', '.join(info['ayats'])}")
        else:
            parts.append(f"QS. {info['name']}: {', '.join(info['ayats'])}")
    return f"{num}. Al-Qur'an al-Karim. {'; '.join(parts)}."


def add_citation_near_quran_blockquote(content, cite_num):
    """Add ^N citation to the paragraph that introduces a Quran blockquote."""
    lines = content.split('\n')
    modified = False
    cite_str = f'^{cite_num}'
    
    # Check if ^cite_num already exists in body
    parts = re.split(r'##\s*(?:Daftar Pustaka|Bibliography|References)', content, maxsplit=1)
    body = parts[0] if parts else content
    if re.search(rf'\^{cite_num}(?!\d)', body):
        return content  # Already has this citation
    
    for i, line in enumerate(lines):
        # Find lines that introduce a Quran quote (before a blockquote with Arabic or QS.)
        if i + 1 < len(lines) and lines[i + 1].strip().startswith('>'):
            # Check if the next blockquote contains QS. or Arabic
            block_start = i + 1
            block_text = ''
            for j in range(block_start, min(block_start + 10, len(lines))):
                if lines[j].strip().startswith('>') or lines[j].strip() == '':
                    block_text += lines[j] + '\n'
                else:
                    break
            
            if 'QS.' in block_text or re.search(r'[\u0600-\u06FF]', block_text):
                # This line introduces a Quran blockquote
                stripped = lines[i].rstrip()
                if stripped and not stripped.startswith('#') and not stripped.startswith('>'):
                    # Don't add if already has this cite num
                    if cite_str not in stripped:
                        # Add citation before the colon at end, or at end of line
                        if stripped.endswith(':'):
                            lines[i] = stripped[:-1] + cite_str + ':'
                        elif stripped.endswith(':' + cite_str):
                            pass  # Already there
                        else:
                            lines[i] = stripped + cite_str
                        modified = True
                        break  # Only add to first occurrence
    
    if not modified:
        # Fallback: add to first paragraph that mentions Quran/QS
        for i, line in enumerate(lines):
            stripped = lines[i].rstrip()
            if 'QS.' in stripped or "Qur'an" in stripped or 'Quran' in stripped or 'Al-Qur' in stripped:
                if not stripped.startswith('#') and not stripped.startswith('>') and not stripped.startswith('---'):
                    if cite_str not in stripped:
                        if stripped.endswith(':'):
                            lines[i] = stripped[:-1] + cite_str + ':'
                        else:
                            # Add before period or at end
                            lines[i] = stripped + cite_str
                        break
    
    return '\n'.join(lines)


def fix_file(filepath):
    """Fix a single markdown file for V6 compliance."""
    with open(filepath) as f:
        content = f.read()
    
    if not has_qs_refs(content):
        return False, "no QS refs"
    
    if has_quran_bib(content):
        return False, "already has Al-Quran in bib"
    
    # Get QS refs and max bib number
    qs_refs = extract_qs_refs(content)
    if not qs_refs:
        return False, "no parseable QS refs"
    
    max_num = get_max_bib_num(content)
    new_num = max_num + 1
    
    # Build entry
    entry = build_quran_bib_entry(new_num, qs_refs)
    
    # Add entry to bibliography
    # Find the last line of bibliography
    lines = content.split('\n')
    bib_start = None
    for i, line in enumerate(lines):
        if re.match(r'##\s*(?:Daftar Pustaka|Bibliography|References)', line):
            bib_start = i
            break
    
    if bib_start is None:
        return False, "no bibliography section found"
    
    # Find last numbered entry in bibliography
    last_entry_idx = bib_start
    for i in range(bib_start + 1, len(lines)):
        if re.match(r'\d+\.', lines[i].strip()):
            last_entry_idx = i
    
    # Insert new entry after last entry
    lines.insert(last_entry_idx + 1, entry)
    content = '\n'.join(lines)
    
    # Add citation near Quran blockquote
    content = add_citation_near_quran_blockquote(content, new_num)
    
    # Write back
    with open(filepath, 'w') as f:
        f.write(content)
    
    return True, f"added entry #{new_num}: {entry[:80]}..."


def fix_card_sources(db_path, event_id, qs_refs):
    """Add quran entry to events-database.json sources for an event."""
    with open(db_path) as f:
        data = json.load(f)
    
    for e in data['events']:
        if e['id'] == event_id:
            sources = e.get('sources', [])
            # Check if already has quran entry
            has_quran = any(s.get('type') == 'quran' or 'Al-Quran' in s.get('title', '') for s in sources)
            if has_quran:
                return False
            
            # Build author string from QS refs
            author_parts = []
            for key, info in qs_refs.items():
                author_parts.append(info['name'])
            author = 'QS. ' + ', '.join(author_parts)
            
            # Build id
            sid = 'qs-' + re.sub(r'[^a-z0-9-]', '-', '-'.join(author_parts).lower())[:40].strip('-')
            
            sources.append({
                'id': sid,
                'title': 'Al-Quran al-Karim',
                'author': author,
                'type': 'quran'
            })
            e['sources'] = sources
            
            with open(db_path, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
    return False


def main():
    fixed_md = 0
    fixed_card = 0
    errors = []
    
    # Load DB for card fixes
    with open(DB_PATH) as f:
        db_data = json.load(f)
    events_by_id = {e['id']: e for e in db_data['events']}
    
    folders = sorted(os.listdir(PROJECT_CONTENT))
    
    for folder in folders:
        m = re.match(r'(e\d+)', folder)
        if not m:
            continue
        eid = m.group(1)
        folder_path = os.path.join(PROJECT_CONTENT, folder)
        
        for lang_file in ['general-id.md', 'general-en.md']:
            filepath = os.path.join(folder_path, lang_file)
            if not os.path.isfile(filepath):
                continue
            
            success, msg = fix_file(filepath)
            if success:
                fixed_md += 1
                print(f"✅ Fixed {folder}/{lang_file}: {msg}")
                
                # Sync to docs
                docs_folder = os.path.join(DOCS_CONTENT, folder)
                if os.path.isdir(docs_folder):
                    shutil.copy2(filepath, os.path.join(docs_folder, lang_file))
            elif 'no QS refs' not in msg and 'already has' not in msg:
                errors.append(f"⚠️ {folder}/{lang_file}: {msg}")
        
        # Fix card sources if needed
        md_path = os.path.join(folder_path, 'general-id.md')
        if os.path.isfile(md_path):
            with open(md_path) as f:
                content = f.read()
            if has_qs_refs(content):
                qs_refs = extract_qs_refs(content)
                e = events_by_id.get(eid, {})
                sources = e.get('sources', [])
                has_quran = any(s.get('type') == 'quran' or 'Al-Quran' in s.get('title', '') for s in sources)
                if not has_quran and qs_refs:
                    if fix_card_sources(DB_PATH, eid, qs_refs):
                        fixed_card += 1
                        print(f"🃏 Fixed card {eid}: added quran source entry")
    
    print(f"\n{'='*50}")
    print(f"SUMMARY: Fixed {fixed_md} markdown files, {fixed_card} card entries")
    if errors:
        print(f"Errors: {len(errors)}")
        for e in errors:
            print(f"  {e}")


if __name__ == '__main__':
    main()
