#!/usr/bin/env python3
"""
Fix V6 bijection: Add ^N citation to body for Al-Qur'an al-Karim bibliography entries
that were added but not cited in body text.

Strategy: Find the FIRST line that introduces a Quran blockquote (line before > with Arabic text)
and add ^N there. If that fails, find any paragraph mentioning "Qur'an" or "QS." or "Al-Qur'an".
"""

import os
import re
import shutil

PROJECT_CONTENT = '/workspace/projects/baitul-hikmah/content/events'
DOCS_CONTENT = '/workspace/docs/content/events'


def find_quran_bib_num(content):
    """Find the entry number for Al-Qur'an al-Karim in bibliography."""
    parts = re.split(r'##\s*(?:Daftar Pustaka|Bibliography|References)', content, maxsplit=1)
    if len(parts) < 2:
        return None
    bib = parts[1]
    for line in bib.split('\n'):
        m = re.match(r'(\d+)\.\s*Al-Qur', line)
        if m:
            return int(m.group(1))
    return None


def is_cited(content, num):
    """Check if ^num exists in body (before bibliography)."""
    parts = re.split(r'##\s*(?:Daftar Pustaka|Bibliography|References)', content, maxsplit=1)
    body = parts[0] if parts else content
    return bool(re.search(rf'\^{num}(?!\d)', body))


def add_citation(content, cite_num):
    """Add ^N to the line introducing the first Quran blockquote."""
    lines = content.split('\n')
    cite_str = f'^{cite_num}'
    
    # Find bibliography start to limit search to body only
    bib_line = len(lines)
    for i, line in enumerate(lines):
        if re.match(r'##\s*(?:Daftar Pustaka|Bibliography|References)', line):
            bib_line = i
            break
    
    # Strategy 1: Find line just before a blockquote containing Arabic or QS.
    for i in range(bib_line):
        line = lines[i].strip()
        if not line or line.startswith('#') or line.startswith('>') or line.startswith('---') or line.startswith('|'):
            continue
        
        # Check if next non-empty line is a blockquote with Arabic/QS
        for j in range(i + 1, min(i + 4, bib_line)):
            next_line = lines[j].strip()
            if not next_line:
                continue
            if next_line.startswith('>'):
                # Check if this blockquote contains Arabic text or QS ref
                block_text = ''
                for k in range(j, min(j + 15, bib_line)):
                    if lines[k].strip().startswith('>') or not lines[k].strip():
                        block_text += lines[k] + '\n'
                    else:
                        break
                
                if re.search(r'[\u0600-\u06FF]', block_text) or 'QS.' in block_text:
                    # This line introduces a Quran blockquote - add citation
                    stripped = lines[i].rstrip()
                    if cite_str in stripped:
                        return '\n'.join(lines), False  # Already there
                    
                    # Insert citation
                    if stripped.endswith(':'):
                        lines[i] = stripped[:-1] + cite_str + ':'
                    elif stripped.endswith('.'):
                        lines[i] = stripped[:-1] + cite_str + '.'
                    else:
                        lines[i] = stripped + cite_str
                    return '\n'.join(lines), True
            break  # Only check immediate next non-empty line
    
    # Strategy 2: Find first paragraph that mentions Quran/QS/Al-Qur'an
    for i in range(bib_line):
        line = lines[i].strip()
        if not line or line.startswith('#') or line.startswith('>') or line.startswith('---') or line.startswith('|'):
            continue
        
        if re.search(r"(?:Qur'an|Quran|Al-Qur|QS\.|surah|surat)", line, re.IGNORECASE):
            stripped = lines[i].rstrip()
            if cite_str in stripped:
                return '\n'.join(lines), False
            
            if stripped.endswith(':'):
                lines[i] = stripped[:-1] + cite_str + ':'
            elif stripped.endswith('.'):
                lines[i] = stripped[:-1] + cite_str + '.'
            else:
                lines[i] = stripped + cite_str
            return '\n'.join(lines), True
    
    # Strategy 3: Find first blockquote line that has "— QS." and add to line before it
    for i in range(1, bib_line):
        if '— QS.' in lines[i]:
            # Go back to find the introducing line
            for j in range(i - 1, -1, -1):
                stripped = lines[j].strip()
                if stripped and not stripped.startswith('>') and not stripped.startswith('#') and not stripped.startswith('---'):
                    if cite_str not in lines[j]:
                        s = lines[j].rstrip()
                        if s.endswith(':'):
                            lines[j] = s[:-1] + cite_str + ':'
                        elif s.endswith('.'):
                            lines[j] = s[:-1] + cite_str + '.'
                        else:
                            lines[j] = s + cite_str
                        return '\n'.join(lines), True
                    break
    
    return '\n'.join(lines), False


def main():
    fixed = 0
    failed = []
    
    for d in sorted(os.listdir(PROJECT_CONTENT)):
        for lang in ['general-id.md', 'general-en.md']:
            fp = os.path.join(PROJECT_CONTENT, d, lang)
            if not os.path.isfile(fp):
                continue
            
            with open(fp) as f:
                content = f.read()
            
            quran_num = find_quran_bib_num(content)
            if quran_num is None:
                continue
            
            if is_cited(content, quran_num):
                continue
            
            new_content, modified = add_citation(content, quran_num)
            if modified:
                with open(fp, 'w') as f:
                    f.write(new_content)
                
                # Sync to docs
                docs_fp = os.path.join(DOCS_CONTENT, d, lang)
                if os.path.isdir(os.path.dirname(docs_fp)):
                    shutil.copy2(fp, docs_fp)
                
                fixed += 1
                print(f"✅ {d}/{lang}: added ^{quran_num}")
            else:
                failed.append(f"{d}/{lang} (#{quran_num})")
    
    print(f"\n{'='*50}")
    print(f"Fixed: {fixed}")
    if failed:
        print(f"Could not auto-fix: {len(failed)}")
        for f in failed:
            print(f"  ❌ {f}")


if __name__ == '__main__':
    main()
