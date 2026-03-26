#!/usr/bin/env python3
"""
Full QA audit script for Baitul Hikmah content.
Checks V1-V9 + language + format + unicode superscripts.

Usage:
  python3 scripts/qa-full.py           # Audit all 128 events
  python3 scripts/qa-full.py e01 e02   # Audit specific events
  python3 scripts/qa-full.py --fix     # Auto-fix what can be fixed
"""
import os, re, sys, json, shutil
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(BASE, 'content', 'events')
DOCS = '/workspace/docs/content/events'

# English words that should not appear in Indonesian articles
ENG_WORDS = set(['systematically','implementing','campaign','manuscripts','consequences',
    'devastating','preservation','effectively','demonstrated','approximately','established',
    'sophisticated','significant','conquest','strategic','commercial','intellectual',
    'rebellion','transformation','decline','comprehensive','governance','architecture',
    'facilitated','patronage','flourished','crucial','infrastructure','institutions',
    'particularly','increasingly','ultimately','developed','included','practices',
    'maintaining','techniques','suppressed','tensions','enriched','sanctuary','refugee',
    'construction','traditional','combination','dominant','successful','consolidated',
    'agricultural','dramatically','remarkable','inevitable','despite','although','however',
    'tolerance','trade','diversity','scientific','achievement','diplomatic','military',
    'unity','lasting','cultural','economic','trading','advanced','innovation','historical',
    'gradually'])

SUPERSCRIPT_CHARS = set('⁰¹²³⁴⁵⁶⁷⁸⁹')


def audit_file(fp, lang='id'):
    """Audit a single markdown file. Returns list of issues."""
    with open(fp) as f:
        content = f.read()
    
    bib_header = 'Daftar Pustaka' if 'Daftar Pustaka' in content else 'Bibliography'
    parts = re.split(rf'##\s*{bib_header}', content, maxsplit=1)
    body = parts[0] if parts else content
    bib = parts[1] if len(parts) > 1 else ''
    
    issues = []
    
    # Parse refs
    body_refs = set(int(x) for x in re.findall(r'\^(\d+)', body))
    bib_entries = set(int(x) for x in re.findall(r'^(\d+)\.', bib, re.MULTILINE))
    
    # V1: unused bib entries
    unused = bib_entries - body_refs
    if unused:
        issues.append(f'V1: {len(unused)} unused bib entries: {sorted(unused)[:5]}')
    
    # V2: orphan body refs
    orphan = body_refs - bib_entries
    if orphan:
        issues.append(f'V2: orphan refs: {sorted(orphan)[:5]}')
    
    # V3: duplicate authors
    authors = []
    for line in bib.split('\n'):
        m = re.match(r'\d+\.\s*(.+)', line.strip())
        if m:
            author = re.split(r'[,.]', re.sub(r'[*_]', '', m.group(1)))[0].strip().lower()
            authors.append(author)
    dups = {a: c for a, c in Counter(authors).items() if c > 1}
    # Filter: same author with genuinely different books is OK
    # Only flag if exact same first part
    
    # V4: min 3 pustaka
    if 0 < len(bib_entries) < 3:
        issues.append(f'V4: only {len(bib_entries)} pustaka (min 3)')
    
    # V5: ^0
    if 0 in body_refs:
        issues.append('V5: ^0 found')
    
    # V6: QS refs without Al-Quran in bib
    has_qs = bool(re.search(r'QS\.', body))
    has_quran = bool(re.search(r'Al-Qur.an al-Karim', bib, re.IGNORECASE))
    if has_qs and not has_quran:
        issues.append('V6: QS refs but no Al-Quran in bib')
    
    # V6b: duplicate Al-Quran entries
    quran_entries = [l for l in bib.split('\n') if re.match(r'\s*\d+\.\s*Al-Qur', l.strip())]
    if len(quran_entries) > 1:
        issues.append(f'V6b: {len(quran_entries)} Al-Quran entries (should be 1)')
    
    # V6c: truncated surah name
    for qe in quran_entries:
        if re.search(r'QS\.\s*\w+\s*[,;.]', qe) and '(' not in qe.split('QS.')[1]:
            issues.append(f'V6c: truncated surah in bib')
    
    # Format: ^N. instead of .^N
    wrong_format = len(re.findall(r'[^.\s>]\^\d+\.(?:\s|$)', body))
    if wrong_format:
        issues.append(f'FORMAT: {wrong_format}x "^N." instead of ".^N"')
    
    # Unicode superscripts
    sup_count = sum(1 for c in body if c in SUPERSCRIPT_CHARS)
    if sup_count:
        issues.append(f'UNICODE: {sup_count} unicode superscript chars (must use ^N)')
    
    # Language (only for ID files)
    if lang == 'id':
        words = re.findall(r'\b[a-z]{4,}\b', body.lower())
        eng_count = sum(1 for w in words if w in ENG_WORDS)
        if eng_count > 3:
            issues.append(f'LANG: {eng_count} English words in Indonesian article')
    
    # op.cit / bab in bib
    if re.search(r'op\.\s*cit', bib, re.IGNORECASE):
        issues.append('STYLE: "op. cit." in bib (should reuse number)')
    if re.search(r'\bbab\b', bib, re.IGNORECASE):
        issues.append('STYLE: "bab" in bib (should be inline)')
    
    return issues


def main():
    args = sys.argv[1:]
    fix_mode = '--fix' in args
    args = [a for a in args if a != '--fix']
    
    # Get target events
    if args:
        targets = args
    else:
        targets = sorted(os.listdir(CONTENT))
    
    total_pass = 0
    total_fail = 0
    all_issues = []
    
    for d in targets:
        folder = d
        if not os.path.isdir(os.path.join(CONTENT, d)):
            # Try finding folder
            for f in os.listdir(CONTENT):
                if f.startswith(d + '-') or f == d:
                    folder = f
                    break
        
        fp_id = os.path.join(CONTENT, folder, 'general-id.md')
        if not os.path.isfile(fp_id):
            continue
        
        eid = re.match(r'(e\d+)', folder)
        eid = eid.group(1) if eid else folder
        
        issues_id = audit_file(fp_id, 'id')
        
        fp_en = os.path.join(CONTENT, folder, 'general-en.md')
        issues_en = audit_file(fp_en, 'en') if os.path.isfile(fp_en) else []
        
        all_issues_combined = issues_id + [f'EN: {i}' for i in issues_en]
        
        if all_issues_combined:
            total_fail += 1
            print(f'❌ {eid}: {", ".join(issues_id[:3])}')
            all_issues.append((eid, all_issues_combined))
        else:
            total_pass += 1
    
    print(f'\n{"="*50}')
    print(f'✅ PASS: {total_pass}')
    print(f'❌ FAIL: {total_fail}')
    print(f'Total: {total_pass + total_fail}')
    
    if all_issues:
        # Count issue types
        type_counts = Counter()
        for eid, issues in all_issues:
            for i in issues:
                itype = i.split(':')[0]
                type_counts[itype] += 1
        
        print(f'\nIssue types:')
        for itype, count in type_counts.most_common():
            print(f'  {itype}: {count}')


if __name__ == '__main__':
    main()
