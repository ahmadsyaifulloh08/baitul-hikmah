#!/usr/bin/env python3
"""
QA Content Review — Baitul Hikmah
Automated quality gate for content files before deploy.

Usage:
  python3 scripts/qa-content.py                    # Audit all events
  python3 scripts/qa-content.py e03 e47            # Audit specific events
  python3 scripts/qa-content.py --json             # Output as JSON (for automation)

Exit codes:
  0 = all PASS
  1 = some FAIL (details in output)

Violation Types:
  V1: Pustaka tanpa sitasi (entry #N tanpa ^N di body)
  V2: Sitasi tanpa pustaka (^N di body tanpa entry #N)
  V3: Duplikat pustaka (sumber sama muncul >1x)
  V4: Pustaka count too few (<3)
  V5: Sitasi ^0 (nol)
  V6: ID↔EN section count mismatch (general)
  V7: ID↔EN children slide count mismatch
"""

import os, re, sys, json, glob

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content", "events")
# Fallback to workspace docs if project content dir empty
DOCS_CONTENT_DIR = "/workspace/docs/content/events"


def find_content_dir():
    if os.path.exists(CONTENT_DIR) and os.listdir(CONTENT_DIR):
        return CONTENT_DIR
    return DOCS_CONTENT_DIR


def parse_citations(text):
    """Extract all citation numbers from body text (before bibliography section)."""
    # Split at bibliography
    parts = re.split(r'^## (?:Daftar Pustaka|Referensi|Bibliography)', text, flags=re.MULTILINE)
    if len(parts) < 2:
        return set(), [], []

    body = parts[0]
    bib_section = parts[1]

    # Find caret refs: ^1, ^2, etc.
    caret_refs = set(int(x) for x in re.findall(r'\^(\d+)', body))

    # Find unicode superscripts: ¹²³⁴⁵⁶⁷⁸⁹⁰
    sup_map = {
        '\u00B9': 1, '\u00B2': 2, '\u00B3': 3,
        '\u2074': 4, '\u2075': 5, '\u2076': 6,
        '\u2077': 7, '\u2078': 8, '\u2079': 9, '\u2070': 0
    }
    unicode_refs = set()
    for ch, num in sup_map.items():
        if ch in body:
            unicode_refs.add(num)

    all_refs = caret_refs | unicode_refs

    # Parse bibliography entries
    bib_entries = re.findall(r'^\d+\.\s*(.+)$', bib_section, re.MULTILINE)
    bib_count = len(bib_entries)

    return all_refs, bib_entries, bib_count


def normalize_bib(entry):
    """Normalize bibliography entry for duplicate detection."""
    return re.sub(r'[^a-zA-Z0-9]', '', entry.lower())


def count_sections(text):
    """Count ## headings (excluding Daftar Pustaka)."""
    headings = re.findall(r'^## (.+)$', text, re.MULTILINE)
    return [h for h in headings if not re.match(r'(?:Daftar Pustaka|Referensi|Bibliography|References)', h)]


def count_children_slides(text):
    """Count content sections in children file (split by ## or ---)."""
    sections = re.split(r'^## ', text, flags=re.MULTILINE)
    # Filter empty and frontmatter
    valid = [s for s in sections if s.strip() and not s.strip().startswith('title:')]
    return len(valid)


def audit_event(event_dir):
    """Audit a single event directory. Returns (event_name, pass/fail, violations)."""
    dirname = os.path.basename(event_dir.rstrip('/'))
    violations = []

    # Check general-id.md exists
    gen_id_path = os.path.join(event_dir, "general-id.md")
    if not os.path.exists(gen_id_path):
        return dirname, False, ["MISSING: general-id.md not found"]

    gen_id = open(gen_id_path, 'r').read()
    gen_id_clean = re.sub(r'^---.*?---\n*', '', gen_id, flags=re.DOTALL)

    # === Citation checks (V1-V5) ===
    all_refs, bib_entries, bib_count = parse_citations(gen_id_clean)

    if bib_count == 0:
        violations.append("V4: Tidak ada section Daftar Pustaka")
    else:
        # V4: Minimum count (no max — any amount OK if all cited & consolidated)
        if bib_count < 3:
            violations.append(f"V4: Pustaka terlalu sedikit ({bib_count} < 3)")

        # V1: Pustaka tanpa sitasi
        uncited = [i for i in range(1, bib_count + 1) if i not in all_refs]
        if uncited:
            violations.append(f"V1: Pustaka tanpa sitasi: entry {uncited}")

        # V2: Sitasi tanpa pustaka
        orphans = [r for r in sorted(all_refs) if r > bib_count or r < 1]
        if orphans:
            violations.append(f"V2: Sitasi tanpa pustaka: ^{orphans}")

        # V5: Sitasi nol
        if 0 in all_refs:
            violations.append("V5: Ada sitasi ^0 (nol) — harus mulai dari ^1")

        # V3: Duplikat pustaka
        dupes = []
        for i in range(len(bib_entries)):
            for j in range(i + 1, len(bib_entries)):
                a = normalize_bib(bib_entries[i])
                b = normalize_bib(bib_entries[j])
                if len(a) > 20 and len(b) > 20 and (a == b or a in b or b in a):
                    dupes.append(f"#{i+1} ≈ #{j+1}")
        if dupes:
            violations.append(f"V3: Duplikat pustaka: {dupes[:5]}{'...' if len(dupes) > 5 else ''}")

    # === ID↔EN sync checks (V6-V7) ===
    gen_en_path = os.path.join(event_dir, "general-en.md")
    if os.path.exists(gen_en_path):
        gen_en = open(gen_en_path, 'r').read()
        gen_en_clean = re.sub(r'^---.*?---\n*', '', gen_en, flags=re.DOTALL)
        id_sections = count_sections(gen_id_clean)
        en_sections = count_sections(gen_en_clean)
        if len(id_sections) != len(en_sections):
            violations.append(f"V6: Section count mismatch — general-id has {len(id_sections)}, general-en has {len(en_sections)}")

    child_id_path = os.path.join(event_dir, "children-id.md")
    child_en_path = os.path.join(event_dir, "children-en.md")
    if os.path.exists(child_id_path) and os.path.exists(child_en_path):
        child_id = open(child_id_path, 'r').read()
        child_en = open(child_en_path, 'r').read()
        child_id_clean = re.sub(r'^---.*?---\n*', '', child_id, flags=re.DOTALL)
        child_en_clean = re.sub(r'^---.*?---\n*', '', child_en, flags=re.DOTALL)
        id_slides = count_children_slides(child_id_clean)
        en_slides = count_children_slides(child_en_clean)
        if id_slides != en_slides:
            violations.append(f"V7: Children slide count mismatch — id has {id_slides}, en has {en_slides}")

    # === File completeness ===
    expected_files = ["general-id.md", "general-en.md", "children-id.md", "children-en.md"]
    missing = [f for f in expected_files if not os.path.exists(os.path.join(event_dir, f))]
    if missing:
        violations.append(f"INCOMPLETE: Missing files: {missing}")

    passed = len(violations) == 0
    return dirname, passed, violations


def main():
    content_dir = find_content_dir()
    json_mode = "--json" in sys.argv
    specific = [a for a in sys.argv[1:] if not a.startswith("--")]

    results = {"pass": [], "fail": []}

    event_dirs = sorted(glob.glob(f"{content_dir}/e*/"))

    for event_dir in event_dirs:
        dirname = os.path.basename(event_dir.rstrip('/'))

        # Filter specific events if requested
        if specific:
            event_id = dirname.split('-')[0]
            if event_id not in specific and dirname not in specific:
                continue

        # Skip empty dirs
        if not any(f.endswith('.md') for f in os.listdir(event_dir)):
            continue

        name, passed, violations = audit_event(event_dir)

        if passed:
            results["pass"].append(name)
        else:
            results["fail"].append({"event": name, "violations": violations})

    if json_mode:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        total = len(results["pass"]) + len(results["fail"])
        print(f"QA CONTENT REVIEW — {total} events audited")
        print(f"✅ PASS: {len(results['pass'])}  |  🔴 FAIL: {len(results['fail'])}")
        print()

        if results["fail"]:
            print("=" * 60)
            print("FAILURES:")
            print("=" * 60)
            for item in results["fail"]:
                print(f"\n🔴 {item['event']}")
                for v in item["violations"]:
                    print(f"   → {v}")

            print()
            print("=" * 60)
            print(f"PASS list ({len(results['pass'])}): {', '.join(results['pass'][:10])}{'...' if len(results['pass']) > 10 else ''}")
        else:
            print("🎉 All events passed QA!")

    sys.exit(1 if results["fail"] else 0)


if __name__ == "__main__":
    main()
