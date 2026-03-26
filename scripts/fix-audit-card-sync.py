#!/usr/bin/env python3
"""
Phase 6: Sync card sources (events-database.json) from markdown bibliography.
Reads each event's general-id.md bibliography → updates sources[] in events-database.json.
"""
import os, re, json, sys

CONTENT_DIR = 'content/events'
DB_PATH = 'src/data/events-database.json'
DRY_RUN = '--dry-run' in sys.argv

with open(DB_PATH) as f:
    db = json.load(f)

def parse_bibliography(content):
    """Extract bibliography entries from markdown."""
    bib_markers = ['## Daftar Pustaka', '## Bibliography', '## References']
    bib_text = None
    for marker in bib_markers:
        if marker in content:
            bib_text = content.split(marker, 1)[1]
            break
    if not bib_text:
        return []
    
    entries = []
    for line in bib_text.strip().split('\n'):
        line = line.strip()
        m = re.match(r'^(\d+)\.\s+(.*)', line)
        if not m:
            continue
        text = m.group(2).strip()
        if not text:
            continue
        
        # Determine type
        if re.search(r'Al-Qur.?an', text, re.IGNORECASE):
            entry_type = 'quran'
            # Extract surah info for author field
            qs_refs = re.findall(r'QS\.\s+([^;.]+)', text)
            author = '; '.join(f'QS. {q.strip()}' for q in qs_refs) if qs_refs else 'Al-Quran al-Karim'
            title = 'Al-Quran al-Karim'
            entry_id = 'qs-' + re.sub(r'[^a-z0-9]', '-', author.lower().split(',')[0].replace('qs.','').strip())[:30]
        elif re.search(r'(Sunan|Sahih|Musnad|Muwatta|HR\s)', text, re.IGNORECASE):
            entry_type = 'hadith'
            # Parse author
            parts = text.split(',', 1)
            author = parts[0].strip().rstrip('.')
            title_match = re.search(r'\*([^*]+)\*', text)
            title = title_match.group(1) if title_match else parts[0].strip()
            entry_id = re.sub(r'[^a-z0-9]', '-', author.lower())[:30]
        else:
            entry_type = 'primary'
            parts = text.split(',', 1)
            author = parts[0].strip().rstrip('.')
            title_match = re.search(r'\*([^*]+)\*', text)
            title = title_match.group(1) if title_match else (parts[1].strip()[:60] if len(parts) > 1 else author)
            entry_id = re.sub(r'[^a-z0-9]', '-', author.lower())[:30]
        
        entries.append({
            'id': entry_id.strip('-'),
            'title': title,
            'author': author,
            'type': entry_type
        })
    
    return entries

# Process each event
updated = 0
for event in db['events']:
    eid = event['id']
    
    # Find folder
    folder = None
    for d in os.listdir(CONTENT_DIR):
        if d.startswith(eid + '-') and os.path.isdir(os.path.join(CONTENT_DIR, d)):
            folder = d
            break
    if not folder:
        continue
    
    fpath = os.path.join(CONTENT_DIR, folder, 'general-id.md')
    if not os.path.exists(fpath):
        continue
    
    with open(fpath) as f:
        content = f.read()
    
    new_sources = parse_bibliography(content)
    if not new_sources:
        continue
    
    # Compare with existing
    old_count = len(event.get('sources', []))
    new_count = len(new_sources)
    
    if old_count != new_count:
        event['sources'] = new_sources
        updated += 1
        if DRY_RUN:
            print(f'  Would update {eid}: {old_count} → {new_count} sources')
        else:
            print(f'  ✅ {eid}: {old_count} → {new_count} sources')

if not DRY_RUN:
    with open(DB_PATH, 'w') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

print(f'\n{"DRY RUN - " if DRY_RUN else ""}Updated: {updated} events')
