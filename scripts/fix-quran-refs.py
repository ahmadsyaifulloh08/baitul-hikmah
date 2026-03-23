#!/usr/bin/env python3
"""
Auto-fix Quran references — add Arabic text where missing.

Scans articles for QS./Surah references without Arabic text nearby,
fetches from API, and inserts in correct format.

See: docs/content-style-guide.md Section 1 (Quran format rules)
API: https://api.alquran.cloud/v1

Usage:
    python3 scripts/fix-quran-refs.py                    # dry-run all
    python3 scripts/fix-quran-refs.py --fix               # fix all
    python3 scripts/fix-quran-refs.py e04                 # dry-run specific
    python3 scripts/fix-quran-refs.py e04 --fix           # fix specific
"""
import os, re, sys, glob, json, urllib.request, time

SURAH_LOOKUP = {
    "al-fatihah": 1, "al-baqarah": 2, "ali imran": 3, "ali-imran": 3,
    "an-nisa": 4, "al-maidah": 5, "al-an'am": 6, "al-a'raf": 7,
    "al-anfal": 8, "at-taubah": 9, "at-tawbah": 9, "yunus": 10,
    "hud": 11, "yusuf": 12, "ar-ra'd": 13, "ibrahim": 14, "al-hijr": 15,
    "an-nahl": 16, "al-isra": 17, "al-isra'": 17, "al-kahf": 18,
    "maryam": 19, "taha": 20, "al-anbiya": 21, "al-hajj": 22,
    "al-mu'minun": 23, "an-nur": 24, "al-furqan": 25,
    "asy-syu'ara": 26, "ash-shu'ara": 26, "an-naml": 27,
    "al-qasas": 28, "al-ankabut": 29, "ar-rum": 30,
    "luqman": 31, "as-sajdah": 32, "al-ahzab": 33,
    "saba": 34, "fatir": 35, "yasin": 36, "ya sin": 36,
    "as-saffat": 37, "shad": 38, "sad": 38, "az-zumar": 39,
    "ghafir": 40, "al-mu'min": 40, "fussilat": 41, "asy-syura": 42,
    "az-zukhruf": 43, "ad-dukhan": 44, "al-jatsiyah": 45,
    "al-ahqaf": 46, "muhammad": 47, "al-fath": 48, "al-hujurat": 49,
    "qaf": 50, "adz-dzariyat": 51, "at-tur": 52, "an-najm": 53,
    "al-qamar": 54, "ar-rahman": 55, "al-waqi'ah": 56,
    "al-hadid": 57, "al-mujadalah": 58, "al-hasyr": 59,
    "al-mumtahanah": 60, "as-saff": 61, "al-jumu'ah": 62,
    "al-munafiqun": 63, "at-taghabun": 64, "at-talaq": 65,
    "at-tahrim": 66, "al-mulk": 67, "al-qalam": 68, "al-haqqah": 69,
    "al-ma'arij": 70, "nuh": 71, "al-jinn": 72, "al-muzzammil": 73,
    "al-muddassir": 74, "al-muddaththir": 74, "al-qiyamah": 75,
    "al-insan": 76, "al-mursalat": 77, "an-naba": 78, "an-nazi'at": 79,
    "abasa": 80, "at-takwir": 81, "al-infitar": 82, "al-mutaffifin": 83,
    "al-insyiqaq": 84, "al-buruj": 85, "at-tariq": 86, "al-a'la": 87,
    "al-ghasyiyah": 88, "al-fajr": 89, "al-balad": 90, "asy-syams": 91,
    "al-lail": 92, "ad-duha": 93, "al-insyirah": 94, "asy-syarh": 94,
    "at-tin": 95, "al-alaq": 96, "al-qadr": 97, "al-bayyinah": 98,
    "az-zalzalah": 99, "al-adiyat": 100, "al-qari'ah": 101,
    "at-takasur": 102, "al-asr": 103, "al-humazah": 104,
    "al-fil": 105, "quraisy": 106, "al-ma'un": 107, "al-kautsar": 108,
    "al-kafirun": 109, "an-nasr": 110, "al-lahab": 111, "al-masad": 111,
    "al-ikhlas": 112, "al-falaq": 113, "an-nas": 114,
}

def resolve_surah(name):
    clean = name.strip().lower().replace("'", "'")
    if clean in SURAH_LOOKUP:
        return SURAH_LOOKUP[clean]
    for k, v in SURAH_LOOKUP.items():
        if clean in k or k in clean:
            return v
    return None

def fetch_ayah_text(surah, ayah):
    try:
        url = f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}/ar"
        resp = urllib.request.urlopen(url, timeout=10)
        data = json.loads(resp.read())
        if data.get("status") == "OK":
            text = data["data"]["text"]
            if ayah == 1 and surah != 1:
                text = re.sub(r'^بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\s*', '', text).strip()
            return text
        return None
    except Exception:
        return None

def has_arabic_nearby(lines, line_idx, window=5):
    start = max(0, line_idx - window)
    end = min(len(lines), line_idx + window)
    context = "\n".join(lines[start:end])
    return bool(re.search(r'[\u0600-\u06FF]', context))

def extract_qs_refs(line):
    """Extract (surah_name, start, end) from QS. or Surah references."""
    refs = []
    patterns = [
        r'QS\.?\s+([A-Za-z\-\']+)(?:\s*[\[(\:]?\s*(\d+)\s*[\])]?\s*:\s*(\d+)(?:\s*-\s*(\d+))?)',
        r'QS\.?\s+([A-Za-z\-\']+)\s*:\s*(\d+)(?:\s*-\s*(\d+))?',
        r'Surah\s+([A-Za-z\-\']+)\s*[\[(\:]?\s*(\d+)\s*[\])]?\s*:\s*(\d+)(?:\s*-\s*(\d+))?',
    ]
    for pat in patterns:
        for m in re.finditer(pat, line):
            groups = m.groups()
            surah_name = groups[0]
            if len(groups) == 4:
                start = int(groups[2])
                end = int(groups[3]) if groups[3] else start
            elif len(groups) == 3:
                start = int(groups[1])
                end = int(groups[2]) if groups[2] else start
            else:
                continue
            refs.append((surah_name, start, end))
    return refs

def scan_file(filepath, do_fix=False):
    with open(filepath) as f:
        lines = f.readlines()
    
    issues = []
    insertions = []
    
    for i, line in enumerate(lines):
        if re.search(r'QS\.\s|Surah\s', line):
            if not has_arabic_nearby(lines, i):
                refs = extract_qs_refs(line)
                for surah_name, start, end in refs:
                    surah_num = resolve_surah(surah_name)
                    if surah_num:
                        issues.append((i, surah_name, surah_num, start, end))
    
    if not do_fix:
        return issues, []
    
    # Build insertions (reverse order to preserve line numbers)
    for line_idx, surah_name, surah_num, start, end in reversed(issues):
        arabic_parts = []
        for ayah in range(start, end + 1):
            text = fetch_ayah_text(surah_num, ayah)
            if text:
                arabic_parts.append(f"{text} ﴿{ayah}﴾")
            time.sleep(0.3)  # Rate limit
        
        if arabic_parts:
            arabic_full = " ".join(arabic_parts)
            # Insert Arabic blockquote before the line
            insert_text = f"\n> {arabic_full}\n>\n"
            lines.insert(line_idx, insert_text)
            insertions.append((line_idx, surah_name, start, end))
    
    if insertions and do_fix:
        with open(filepath, 'w') as f:
            f.writelines(lines)
    
    return issues, insertions

# Main
do_fix = '--fix' in sys.argv
target = None
for arg in sys.argv[1:]:
    if arg != '--fix':
        target = arg

pattern = f"content/events/{target}/*.md" if target else "content/events/*/general-*.md"
files = sorted(glob.glob(pattern))

total_issues = 0
total_fixed = 0

for f in files:
    issues, fixed = scan_file(f, do_fix)
    if issues:
        slug = f.split('/')[2]
        mode = "FIXED" if do_fix else "FOUND"
        print(f"  {slug}/{os.path.basename(f)}: {len(issues)} refs {mode}")
        total_issues += len(issues)
        total_fixed += len(fixed)

if do_fix:
    print(f"\n✅ Fixed {total_fixed} of {total_issues} Quran refs")
else:
    print(f"\n📋 Found {total_issues} Quran refs without Arabic text (dry-run)")
    print(f"   Run with --fix to auto-insert Arabic text from API")
