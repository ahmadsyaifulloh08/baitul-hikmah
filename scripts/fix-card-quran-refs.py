#!/usr/bin/env python3
"""
Fix card sources quran entries — sync author field from markdown bibliography.
Extracts full QS. format from markdown and updates events-database.json.
"""
import json, re, os

DB_PATH = '/workspace/projects/baitul-hikmah/src/data/events-database.json'
CONTENT_BASE = '/workspace/projects/baitul-hikmah/content/events'

with open(DB_PATH) as f:
    db = json.load(f)

fixed = 0
for event in db['events']:
    eid = event['id']
    sources = event.get('sources', [])
    
    # Find quran source entry
    quran_idx = None
    for i, s in enumerate(sources):
        if s.get('type') == 'quran' or 'Al-Quran' in s.get('title', ''):
            quran_idx = i
            break
    
    if quran_idx is None:
        continue
    
    # Find the markdown file
    md_path = None
    for d in os.listdir(CONTENT_BASE):
        if d.startswith(eid + '-'):
            md_path = os.path.join(CONTENT_BASE, d, 'general-id.md')
            break
    
    if not md_path or not os.path.isfile(md_path):
        continue
    
    with open(md_path) as f:
        content = f.read()
    
    # Find Al-Quran entry in markdown bib
    parts = re.split(r'##\s*Daftar Pustaka', content, maxsplit=1)
    if len(parts) < 2:
        continue
    bib = parts[1]
    
    quran_line = None
    for line in bib.split('\n'):
        if re.match(r'\s*\d+\.\s*Al-Qur', line):
            quran_line = line.strip()
    
    if not quran_line:
        continue
    
    # Extract the QS. refs part from markdown
    # Format: "N. Al-Qur'an al-Karim. QS. X (N): A; QS. Y (M): B."
    qs_match = re.search(r'QS\.\s*.+', quran_line)
    if not qs_match:
        continue
    
    new_author = qs_match.group(0).rstrip('.')
    old_author = sources[quran_idx].get('author', '')
    
    if new_author != old_author:
        # Also generate a clean id
        surah_names = re.findall(r'QS\.\s*([A-Za-z][A-Za-z\'\-\s]+?)(?:\s*\()', new_author)
        if not surah_names:
            surah_names = re.findall(r'QS\.\s*([A-Za-z][A-Za-z\'\-\s]+?)(?:\s*[:;,.])', new_author)
        
        clean_id = 'qs-' + '-'.join(
            re.sub(r'[^a-z0-9]', '-', n.lower().strip())[:20].strip('-')
            for n in surah_names
        )[:50]
        
        sources[quran_idx]['author'] = new_author
        sources[quran_idx]['id'] = clean_id
        fixed += 1
        print(f"✅ {eid}: \"{old_author}\" → \"{new_author}\"")

with open(DB_PATH, 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"\nTotal fixed: {fixed}")
