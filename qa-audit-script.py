#!/usr/bin/env python3
"""
QA Script untuk audit 32 events dalam chunk 2
Cek V1-V9 violations dan issues lainnya
"""

import os
import re
from pathlib import Path

# Event list untuk chunk 2
EVENTS = [
    'e120-perang-salib-kedua', 'e121-perang-salib-ketiga', 'e122-perang-salib-keempat', 
    'e123-perang-salib-kelima', 'e124-perang-salib-keenam', 'e125-perang-salib-ketujuh', 
    'e126-perang-salib-terakhir', 'e127-sultan-baibars', 'e128-jatuhnya-acre', 
    'e13-baiat-aqabah', 'e14-baiat-aqabah-kedua', 'e15-hijrah-madinah', 
    'e16-piagam-madinah', 'e17-masjid-nabawi', 'e18-perubahan-kiblat', 
    'e19-perang-badr', 'e20-perang-uhud', 'e21-perang-khandaq', 
    'e22-hudaibiyah', 'e23-surat-dakwah-raja', 'e24-perang-khaibar', 
    'e25-umrah-qadha', 'e26-fath-makkah', 'e27-penghancuran-berhala', 
    'e28-perang-hunain', 'e29-amul-wufud', 'e30-haji-wada', 
    'e31-wafat-rasulullah', 'e32-abu-bakr-khalifah', 'e33-perang-riddah', 
    'e34-pengumpulan-mushaf', 'e35-umar-khalifah'
]

BASE_PATH = '/workspace/projects/baitul-hikmah/content/events'

def audit_event(event_id):
    """Audit single event untuk V1-V9 violations"""
    file_path = Path(BASE_PATH) / event_id / 'general-id.md'
    
    if not file_path.exists():
        return {'status': 'MISSING', 'issues': [f'File {file_path} not found']}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    status = 'PASSED'
    
    # Find all citations in body (^N format)
    citations = set(re.findall(r'\^([0-9]+)', content))
    
    # Find bibliography entries - look for numbered entries after "## Daftar Pustaka"
    bib_section_match = re.search(r'## Daftar Pustaka\s*\n(.*)', content, re.DOTALL)
    if bib_section_match:
        bib_content = bib_section_match.group(1)
        # Find entries that start with number. pattern
        bib_entries = re.findall(r'^([0-9]+)\.', bib_content, re.MULTILINE)
        bib_numbers = set(bib_entries)
    else:
        bib_numbers = set()
        if citations:
            issues.append('V4: No "## Daftar Pustaka" section found')
            status = 'FAILED'
    
    # V1: Pustaka tanpa sitasi (unused bibliography entries)
    unused_bib = bib_numbers - citations
    if unused_bib:
        issues.append(f'V1: Unused bibliography entries: {sorted(unused_bib)}')
        status = 'FAILED'
    
    # V2: Sitasi tanpa pustaka (orphan citations)
    orphan_cites = citations - bib_numbers
    if orphan_cites:
        issues.append(f'V2: Orphan citations: {sorted(orphan_cites)}')
        status = 'FAILED'
    
    # V4: Minimum 3 pustaka
    if len(bib_numbers) < 3:
        issues.append(f'V4: Only {len(bib_numbers)} bibliography entries, need minimum 3')
        status = 'FAILED'
    
    # V5: No ^0 citations
    if '0' in citations:
        issues.append('V5: Found ^0 citation (should start from 1)')
        status = 'FAILED'
    
    # Check for QS. references
    qs_refs = re.findall(r'QS\.\s+([^(]+)', content)
    al_quran_entries = [entry for entry in bib_content.split('\n') if 'Al-Qur\'an al-Karim' in entry or 'Al-Quran al-Karim' in entry] if bib_section_match else []
    
    # V6: If QS refs exist, must have Al-Quran entry
    if qs_refs and not al_quran_entries:
        issues.append('V6: Found QS. references but no Al-Qur\'an al-Karim entry in bibliography')
        status = 'FAILED'
    elif len(al_quran_entries) > 1:
        issues.append('V6: Multiple Al-Qur\'an al-Karim entries (should be only 1)')
        status = 'FAILED'
    
    # Check for language purity (basic check)
    english_words_in_id = re.findall(r'\b(and|the|with|from|systematically|implementing|strategic|despite|conquest)\b', content, re.IGNORECASE)
    if english_words_in_id:
        issues.append(f'Language: English words found in Indonesian text: {set(english_words_in_id)}')
        status = 'FAILED'
    
    # Check for malformed citations
    malformed = re.findall(r'[^.\s>]\^[0-9]+\.', content)
    if malformed:
        issues.append(f'Format: Malformed citation position: {malformed}')
        status = 'FAILED'
    
    return {
        'status': status,
        'issues': issues,
        'stats': {
            'citations': len(citations),
            'bibliography': len(bib_numbers),
            'qs_refs': len(qs_refs)
        }
    }

def main():
    """Audit all 32 events and generate report"""
    results = {}
    
    for event_id in EVENTS:
        print(f"Auditing {event_id}...")
        results[event_id] = audit_event(event_id)
    
    # Generate summary
    passed = sum(1 for r in results.values() if r['status'] == 'PASSED')
    failed = sum(1 for r in results.values() if r['status'] == 'FAILED')
    missing = sum(1 for r in results.values() if r['status'] == 'MISSING')
    
    print(f"\n=== QA SUMMARY ===")
    print(f"Total events: {len(EVENTS)}")
    print(f"PASSED: {passed}")
    print(f"FAILED: {failed}")
    print(f"MISSING: {missing}")
    
    # Show failed events
    if failed > 0:
        print(f"\n=== FAILED EVENTS ===")
        for event_id, result in results.items():
            if result['status'] == 'FAILED':
                print(f"\n{event_id}:")
                for issue in result['issues']:
                    print(f"  - {issue}")
    
    return results

if __name__ == '__main__':
    main()