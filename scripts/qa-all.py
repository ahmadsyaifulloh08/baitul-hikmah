#!/usr/bin/env python3
"""
qa-all.py — Run all QA checks for Baitul Hikmah project.

Bundles all domain-specific linters:
1. check-citations.py   — consolidated citation format
2. check-quran-format.py — Arabic text + ayat separators
3. check-metadata.py    — event metadata completeness
4. check-images.py      — illustration files exist + size

See: docs/content-style-guide.md (content rules)
See: docs/README.md (project structure + checklist)
See: docs/operations/batch-image-generation-v4.md (image specs)

Usage: python3 scripts/qa-all.py              # all checks
       python3 scripts/qa-all.py e04           # specific event
       python3 scripts/qa-all.py --quick       # citations + metadata only
"""
import subprocess, sys, os

event = None
quick = False
for arg in sys.argv[1:]:
    if arg == '--quick':
        quick = True
    else:
        event = arg

scripts_dir = os.path.dirname(os.path.abspath(__file__))
checks = [
    ("Daftar Pustaka", "check-pustaka.py"),
    ("Quran Format", "check-quran-format.py"),
    ("Metadata", "check-metadata.py"),
]
if not quick:
    checks.append(("Images", "check-images.py"))

results = []
total_pass = 0
total_fail = 0

for name, script in checks:
    print(f"\n{'='*50}")
    print(f"  {name}")
    print(f"{'='*50}")
    
    cmd = [sys.executable, os.path.join(scripts_dir, script)]
    if event:
        cmd.append(event)
    
    result = subprocess.run(cmd, cwd=os.path.join(scripts_dir, ".."))
    
    if result.returncode == 0:
        total_pass += 1
        results.append(f"✅ {name}")
    else:
        total_fail += 1
        results.append(f"❌ {name}")

print(f"\n{'='*50}")
print(f"  QA SUMMARY")
print(f"{'='*50}")
for r in results:
    print(f"  {r}")
print(f"\n  Passed: {total_pass}/{len(checks)}")
if total_fail > 0:
    print(f"  FAILED: {total_fail}/{len(checks)}")
    sys.exit(1)
else:
    print(f"  🎉 All checks passed!")
