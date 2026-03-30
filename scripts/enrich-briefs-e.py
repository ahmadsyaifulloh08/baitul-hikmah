#!/usr/bin/env python3
"""Enrich illustration briefs for e100-e128 by merging details from children-id.md"""

import re, os

base = "/workspace/projects/baitul-hikmah"
events_dir = f"{base}/content/events"
briefs_dir = f"{base}/docs/briefs"

SUFFIX = "16:9 1792x1024, no text in image, CENTER 70%"

def extract_art_briefs(content):
    """Extract illustration briefs from children-id.md content."""
    briefs = []
    parts = content.split('\u0001f3a8')  # won't match, use below
    # Actually split on the emoji
    parts = content.split('🎨')
    
    for part in parts[1:]:
        # Skip template lines with placeholder brackets
        if '[Setting]' in part[:200] or '[karakter utama]' in part[:200]:
            continue
            
        text = part.strip()
        
        # Remove various prefix patterns
        for prefix in ['**Brief Ilustrasi:**', 'Brief Ilustrasi:**']:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
                break
        
        # Remove leading blockquote marker
        if text.startswith('>'):
            text = text[1:].strip()
        
        # Remove leading * and optional "Ilustrasi:" prefix
        if text.startswith('*Ilustrasi:'):
            text = text[1 + len('Ilustrasi:'):].strip()
        elif text.startswith('*'):
            text = text[1:].strip()
        
        # Find closing asterisk - the illustration text ends there
        close_idx = text.find('*')
        if close_idx > 0:
            text = text[:close_idx].strip()
        else:
            # No closing asterisk - stop at section headers or ---
            for stopper in ['---', '## ', '> **']:
                idx = text.find(stopper)
                if idx > 0:
                    text = text[:idx].strip()
                    break
        
        # Clean artifacts
        text = text.strip().rstrip('.*>')
        text = text.strip()
        
        if len(text) < 30:
            continue
        
        briefs.append(text)
    
    return briefs

def extract_sections(brief_content):
    """Parse brief file into header, base palette, character lock, and slides"""
    lines = brief_content.split('\n')
    header_line = lines[0] if lines else ""
    
    palette_start = palette_end = char_lock_start = char_lock_end = slides_start = None
    
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('## Base Palette'):
            palette_start = i
        elif s.startswith('## Character Lock'):
            char_lock_start = i
            if palette_start is not None and palette_end is None:
                palette_end = i
        elif s.startswith('## Slides'):
            slides_start = i
            if char_lock_start is not None and char_lock_end is None:
                char_lock_end = i
            if palette_start is not None and palette_end is None:
                palette_end = i
    
    if palette_end is None:
        palette_end = char_lock_start or slides_start
    if char_lock_end is None:
        char_lock_end = slides_start
    
    palette_section = '\n'.join(lines[palette_start:palette_end]).rstrip() if palette_start is not None else ""
    char_lock_section = '\n'.join(lines[char_lock_start:char_lock_end]).rstrip() if char_lock_start is not None else ""
    
    slides = []
    if slides_start is not None:
        slide_text = '\n'.join(lines[slides_start+1:])
        slide_blocks = re.split(r'^### slide-', slide_text, flags=re.MULTILINE)
        for block in slide_blocks[1:]:
            first_line, *rest = block.split('\n', 1)
            match = re.match(r'(\d+)\s*[—\-]+\s*(.*)', first_line)
            if match:
                title = match.group(2).strip()
            else:
                title = first_line.strip()
            prompt = rest[0].strip() if rest else ""
            slides.append({'title': title, 'prompt': prompt})
    
    return {
        'header': header_line,
        'palette': palette_section,
        'char_lock': char_lock_section,
        'slides': slides,
    }

def clean_prompt(text):
    """Remove parentheses, em dashes, and markdown artifacts"""
    text = text.replace('\u2014', ',')  # em dash
    text = text.replace('\u2013', ',')  # en dash
    text = re.sub(r'\(([^)]*)\)', r'\1', text)  # remove parens
    text = re.sub(r',\s*,', ',', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('**', '').replace('> ', '')
    return text.strip()

def make_title(art_brief):
    """Generate a short slide title"""
    title = art_brief.split('.')[0].split(',')[0].strip()
    title = clean_prompt(title)
    if len(title) > 60:
        title = title[:57] + "..."
    return title

def build_prompt(art_brief):
    """Build clean prompt with suffix"""
    prompt = clean_prompt(art_brief).rstrip('., ')
    max_body = 950 - len(SUFFIX)
    if len(prompt) > max_body:
        prompt = prompt[:max_body].rsplit(',', 1)[0].rstrip('., ')
    return f"{prompt}. {SUFFIX}"

def process_event(slug):
    cid_path = f"{events_dir}/{slug}/children-id.md"
    brief_path = f"{briefs_dir}/{slug}.md"
    
    if not os.path.exists(cid_path) or not os.path.exists(brief_path):
        return False
    
    with open(cid_path) as f:
        cid_content = f.read()
    with open(brief_path) as f:
        brief_content = f.read()
    
    art_briefs = extract_art_briefs(cid_content)
    sections = extract_sections(brief_content)
    
    if not art_briefs:
        print(f"SKIP {slug}: no art briefs")
        return False
    
    existing_slides = sections['slides']
    
    new_slides = []
    for i, art_brief in enumerate(art_briefs):
        num = f"{i+1:02d}"
        title = existing_slides[i]['title'] if i < len(existing_slides) else make_title(art_brief)
        title = clean_prompt(title)
        prompt = build_prompt(art_brief)
        new_slides.append(f"### slide-{num} — {title}\n{prompt}")
    
    # Rebuild file
    parts = [sections['header'], ""]
    if sections['palette']:
        parts.extend([sections['palette'], ""])
    if sections['char_lock']:
        parts.extend([sections['char_lock'], ""])
    parts.extend(["## Slides", "", "\n\n".join(new_slides), ""])
    
    with open(brief_path, 'w') as f:
        f.write('\n'.join(parts))
    
    print(f"OK {slug}: {len(new_slides)} slides")
    return True

# Main
slugs = sorted([d for d in os.listdir(events_dir) if re.match(r'e1[0-2]\d-', d)])
slugs = [s for s in slugs if 100 <= int(re.match(r'e(\d+)', s).group(1)) <= 128]

ok = skip = 0
for slug in slugs:
    if process_event(slug):
        ok += 1
    else:
        skip += 1

print(f"\nTotal: {ok} processed, {skip} skipped")
