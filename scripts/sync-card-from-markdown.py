#!/usr/bin/env python3
"""
Sync card sources (events-database.json) from markdown Daftar Pustaka.
Replaces card sources[] with entries parsed from markdown bibliography.
"""
import json, os, re

DB_PATH = '/workspace/projects/baitul-hikmah/src/data/events-database.json'
CONTENT = '/workspace/projects/baitul-hikmah/content/events'

with open(DB_PATH) as f:
    db = json.load(f)

def parse_md_to_card(entry_text):
    """Parse a markdown bibliography entry into card format {id, title, author, type}"""
    clean = re.sub(r'^\*\*|\*\*$', '', entry_text.strip())
    
    # Detect type
    entry_lower = entry_text.lower()
    if 'al-qur' in entry_lower:
        # Quran entry
        qs_match = re.search(r'QS\..*', entry_text)
        author = qs_match.group(0).rstrip('.') if qs_match else 'Al-Quran'
        return {
            'id': 'qs-' + re.sub(r'[^a-z0-9-]', '-', author.lower())[:40].strip('-'),
            'title': 'Al-Quran al-Karim',
            'author': author,
            'type': 'quran'
        }
    
    if any(k in entry_lower for k in ['shahih', 'sunan', 'musnad', 'hadits', 'hadith']):
        stype = 'hadith'
    else:
        stype = 'primary'
    
    # Extract author (before first comma or period, strip bold/italic markers)
    clean_entry = re.sub(r'[*_]', '', entry_text)
    author = re.split(r'[,.]', clean_entry)[0].strip()
    
    # Extract title (in *italics* or after first comma)
    title_match = re.search(r'\*([^*]+)\*', entry_text)
    if title_match:
        title = title_match.group(1).strip()
    else:
        parts = entry_text.split(',', 1)
        title = parts[1].strip()[:60] if len(parts) > 1 else author
    
    # Generate id
    sid = re.sub(r'[^a-z0-9-]', '-', author.lower())[:30].strip('-')
    
    return {
        'id': sid,
        'title': title,
        'author': author,
        'type': stype
    }

synced = 0
for event in db['events']:
    eid = event['id']
    
    # Find folder
    folder = None
    for d in os.listdir(CONTENT):
        if d.startswith(eid + '-'):
            folder = d
            break
    if not folder:
        continue
    
    fp = os.path.join(CONTENT, folder, 'general-id.md')
    if not os.path.isfile(fp):
        continue
    
    with open(fp) as f:
        content = f.read()
    
    parts = re.split(r'##\s*Daftar Pustaka', content, maxsplit=1)
    if len(parts) < 2:
        continue
    
    bib = parts[1]
    
    # Parse entries
    md_entries = []
    for line in bib.split('\n'):
        m = re.match(r'\d+\.\s*(.+)', line.strip())
        if m:
            md_entries.append(m.group(1).strip())
    
    if not md_entries:
        continue
    
    # Convert to card format
    new_sources = []
    for entry in md_entries:
        try:
            card = parse_md_to_card(entry)
            new_sources.append(card)
        except:
            pass
    
    if new_sources:
        old_count = len(event.get('sources', []))
        event['sources'] = new_sources
        if old_count != len(new_sources):
            synced += 1

with open(DB_PATH, 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"Synced {synced} events (card sources updated from markdown)")
