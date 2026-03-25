#!/usr/bin/env python3
"""
Fetch Quran ayat text from API.

API: https://api.alquran.cloud/v1
See: docs/content-style-guide.md Section 1 (Quran format rules)

Usage:
    python3 scripts/fetch-quran.py 105:1-5     # Al-Fil 1-5
    python3 scripts/fetch-quran.py 2:144        # Al-Baqarah 144
    python3 scripts/fetch-quran.py 20:114       # Taha 114
"""
import urllib.request, json, sys, re

SURAH_NAMES = {
    1: "Al-Fatihah", 2: "Al-Baqarah", 3: "Ali Imran", 4: "An-Nisa", 5: "Al-Maidah",
    6: "Al-An'am", 7: "Al-A'raf", 8: "Al-Anfal", 9: "At-Taubah", 10: "Yunus",
    11: "Hud", 12: "Yusuf", 13: "Ar-Ra'd", 14: "Ibrahim", 15: "Al-Hijr",
    16: "An-Nahl", 17: "Al-Isra", 18: "Al-Kahf", 19: "Maryam", 20: "Taha",
    21: "Al-Anbiya", 22: "Al-Hajj", 23: "Al-Mu'minun", 24: "An-Nur", 25: "Al-Furqan",
    26: "Asy-Syu'ara", 27: "An-Naml", 28: "Al-Qasas", 29: "Al-Ankabut", 30: "Ar-Rum",
    33: "Al-Ahzab", 36: "Yasin", 37: "As-Saffat", 39: "Az-Zumar",
    40: "Ghafir", 41: "Fussilat", 42: "Asy-Syura", 47: "Muhammad",
    48: "Al-Fath", 49: "Al-Hujurat", 55: "Ar-Rahman", 56: "Al-Waqi'ah",
    57: "Al-Hadid", 58: "Al-Mujadalah", 59: "Al-Hasyr", 61: "As-Saff",
    62: "Al-Jumu'ah", 67: "Al-Mulk", 71: "Nuh", 73: "Al-Muzzammil",
    74: "Al-Muddassir", 87: "Al-A'la", 89: "Al-Fajr", 91: "Asy-Syams",
    93: "Ad-Duha", 94: "Al-Insyirah", 95: "At-Tin", 96: "Al-Alaq",
    97: "Al-Qadr", 105: "Al-Fil", 106: "Quraisy", 108: "Al-Kautsar",
    109: "Al-Kafirun", 110: "An-Nasr", 112: "Al-Ikhlas", 113: "Al-Falaq", 114: "An-Nas",
}

def fetch_ayah(surah, ayah):
    url = f"https://api.alquran.cloud/v1/ayah/{surah}:{ayah}/ar"
    resp = urllib.request.urlopen(url, timeout=10)
    data = json.loads(resp.read())
    if data.get("status") == "OK":
        text = data["data"]["text"]
        # Remove bismillah from non-Fatihah surahs (ayah 1)
        if ayah == 1 and surah != 1:
            text = re.sub(r'^بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\s*', '', text).strip()
        return text
    return None

def fetch_range(ref_str):
    """Parse '105:1-5' or '2:144' and fetch all ayahs."""
    match = re.match(r'(\d+):(\d+)(?:-(\d+))?', ref_str)
    if not match:
        print(f"Invalid format: {ref_str}. Use SURAH:AYAH or SURAH:START-END")
        return
    
    surah = int(match.group(1))
    start = int(match.group(2))
    end = int(match.group(3)) if match.group(3) else start
    
    surah_name = SURAH_NAMES.get(surah, f"Surah {surah}")
    
    print(f"# {surah_name} ({surah}:{start}-{end})\n")
    
    # Arabic text
    arabic_parts = []
    for ayah in range(start, end + 1):
        text = fetch_ayah(surah, ayah)
        if text:
            arabic_parts.append(f"{text} ﴿{ayah}﴾")
    
    arabic_full = " ".join(arabic_parts)
    print(f"> {arabic_full}")
    print(f">")
    
    # Translation placeholder
    print(f'> "..." ﴾{start}﴿' if start == end else f'> "..." ﴾{start}-{end}﴿')
    print(f"> (QS. {surah_name}: {start})" if start == end else f"> (QS. {surah_name}: {start}-{end})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch-quran.py SURAH:AYAH[-END]")
        print("Example: python3 fetch-quran.py 105:1-5")
        sys.exit(1)
    fetch_range(sys.argv[1])
