# Design Guide — Baitul Hikmah

> Design system + moodboard per era. Merged dari `design-system.md` dan `moodboard-per-era.md`.

---

## 1. Color System

### Era Colors (Primary Palette)

| Era | Primary | Light (bg) | Dark (text) |
|-----|---------|-----------|-------------|
| Pra-Islam | `#8b949e` | `#8b949e1a` | `#6e7681` |
| Kenabian | `#3fb950` | `#3fb9501a` | `#2ea043` |
| Rashidin | `#58a6ff` | `#58a6ff1a` | `#388bfd` |
| Umayyah | `#d29922` | `#d299221a` | `#bb8009` |
| Abbasiyah | `#bc8cff` | `#bc8cff1a` | `#a371f7` |
| Fragmentasi | `#f778ba` | `#f778ba1a` | `#db61a2` |
| Kemunduran | `#da3633` | `#da36331a` | `#cf222e` |

### Children Mode Color Adjustments
All era colors +15-20% lightness. Background: warm cream `#fdf6e3`.

### Neutral Palette

| Token | Light | Dark |
|-------|-------|------|
| `--bg-primary` | `#fafbfc` | `#0d1117` |
| `--bg-secondary` | `#f0f1f3` | `#161b22` |
| `--text-primary` | `#1f2328` | `#f0f6fc` |
| `--text-secondary` | `#8b949e` | `#8b949e` |
| `--border` | `#d0d7de` | `#30363d` |

### Semantic: `--success` #3fb950 | `--warning` #d29922 | `--danger` #da3633 | `--info` #58a6ff

---

## 2. Typography

| Role | Font | Weights | Fallback |
|------|------|---------|----------|
| Headings | Playfair Display | 700, 800 | Georgia, serif |
| Body | Inter | 400, 500, 600 | system-ui, sans-serif |
| Arabic (Quran/Hadits) | Amiri | 400, 700 | Scheherazade New, serif |
| Arabic (UI) | Noto Sans Arabic | 400, 600 | sans-serif |

### Type Scale — General Mode
| Level | Size | Line Height | Font |
|-------|------|-------------|------|
| h1 | 2.5rem | 1.2 | Playfair 800 |
| h2 | 2rem | 1.25 | Playfair 700 |
| h3 | 1.5rem | 1.3 | Playfair 700 |
| body | 1rem | 1.7 | Inter 400 |
| arabic-verse | 1.75rem | 2.0 | Amiri 400 |
| caption | 0.75rem | 1.4 | Inter 500 |

### Children Mode: h1 3rem, h2 2.25rem, body 1.25rem, arabic 2rem

---

## 3. Spacing & Layout

Base unit: 4px (Tailwind spacing scale).

| Breakpoint | Max Width | Padding |
|------------|-----------|---------|
| Mobile (0) | 100% | 16px |
| Tablet (768px) | 720px | 24px |
| Desktop (1024px) | 960px | 32px |
| Wide (1280px) | 1140px | 32px |

**Grid:** Timeline = single column 720px. Event cards = 1→2→3 col. Event detail = 65% content + 35% sidebar.
**Children:** Max width 640px, padding +50%, border-radius 16px.

---

## 4. Component Styles

### Event Card
- Border: 1px `--border`, left 3px era color
- Radius: 8px (general) / 16px (children)
- Hover: translateY -2px, shadow, border-left brightens (200ms)

### Era Badge
- Pill shape, era color 15% opacity bg, full opacity text, Inter 500 12px, padding 4px 12px

### Dalil Card (Quran/Hadits)
- Border-left 3px green (Quran) or blue (Hadits)
- Arabic: centered RTL, Amiri 28px
- Translation: left-aligned, italic
- Source: right-aligned, caption, muted

### Buttons
- Primary: era color bg, white text, 8px radius, hover darken 10%
- Secondary/Ghost: transparent, era color border
- Mode Toggle: pill (☀️ General | 🌙 Dongeng), slide + color morph

### Timeline Marker
- Dot: 12px era color, 2px white border
- Era change: 20px diamond, pulsing glow
- Line: 2px `--border`, gradient between eras

---

## 5. Patterns & Decorative

| Pattern | File | Usage |
|---------|------|-------|
| Star & Cross | `design/assets/pattern-star-cross.svg` | Page headers |
| Hexagonal | `design/assets/pattern-hexagonal.svg` | Section dividers |
| Interlocking | `design/assets/pattern-interlocking.svg` | Card backgrounds |
| Arabesque border | `design/assets/border-arabesque.svg` | Horizontal rules |

**Rules:** Subtle (3-8% opacity), never stack, inherit era color or neutral.

---

## 6. Motion & Animation

| Type | Duration | Easing |
|------|----------|--------|
| Micro (hover) | 150ms | ease-out |
| Small (toggle) | 200ms | ease-in-out |
| Medium (slide) | 300ms | cubic-bezier(0.4, 0, 0.2, 1) |
| Large (page) | 500ms | cubic-bezier(0.4, 0, 0.2, 1) |
| Stagger | 50ms each | ease-out |

Mode switch: color morph 500ms + layout reflow 300ms. Scroll: fade-in + slide alternate. Parallax: hero only, max 20%.

---

## 7. Moodboard Per Era

### Pra-Islam (500–610 M) — Sandy, Muted
- **Mood**: Kegelapan sebelum cahaya, padang pasir, sepia
- **Motifs**: Tribal zigzags, sand grain, tenda Badui, Ka'bah, unta
- **Pattern**: Sand dune waves, faded tribal geometric (4-6% opacity)
- **Children**: Warmer sandy gold, friendly camel, twinkling stars

### Kenabian (610–632 M) — Emerald Green, Radiant
- **Mood**: Cahaya wahyu, harapan, transformasi, Madinah
- **Motifs**: 8-pointed star (Rub el Hizb), cahaya, mihrab arch, kurma, zaitun
- **Pattern**: 8-pointed star tessellation, radial gradient (5-8%)
- **Children**: Extra bright green, golden sparkles, warm glow

### Khulafaur Rashidin (632–661 M) — Sky Blue, Noble
- **Mood**: Keadilan, ekspansi, langit terbuka
- **Motifs**: Hexagonal, perisai, scroll, sword, Masjid Al-Aqsa
- **Pattern**: Hexagonal tessellation, expanding circles (4-6%)
- **Children**: Bright sky blue, shield/knight imagery

### Dinasti Umayyah (661–750 M) — Gold, Grand
- **Mood**: Kemegahan Damaskus, matahari terbenam di atas masjid emas
- **Motifs**: Interlocking squares, marble, mosaic, horseshoe arch, Dome of the Rock
- **Pattern**: Interlocking squares, vine arabesque (5-8%)
- **Children**: Bright gold, treasure-chest feel, shiny coins

### Dinasti Abbasiyah (750–1258 M) — Royal Purple, Intellectual
- **Mood**: Zaman keemasan, Baitul Hikmah, malam cendekia menulis
- **Motifs**: 12-pointed star, astrolabe, ink & quill, Baghdad, spiral minaret Samarra
- **Pattern**: 12-pointed star complex, overlapping circles (5-8%)
- **Children**: Bright purple + gold, "magic library", animated stars

### Fragmentasi (1000–1400 M) — Rose, Resilient
- **Mood**: Terpecah tapi hidup, Al-Andalus, sunset colors
- **Motifs**: Zellige tiles, mashrabiya, Alhambra, fortress, ship
- **Pattern**: Zellige tessellation, mashrabiya lattice (5-7%)
- **Children**: Soft pink, castle & adventure, colorful mosaics

### Kemunduran (1200–1500 M) — Deep Red, Reflective
- **Mood**: Jatuhnya Baghdad, introspeksi, bara api padam
- **Motifs**: Broken geometric, cracked parchment, scattered manuscripts, dimming lamp
- **Pattern**: Fragmented geometric, faded arabesque (3-5%)
- **Children**: Warm terracotta, saving books theme, sunrise (hope)

### Cross-Era Rules
- Pattern complexity: ●○○○○ (Pra-Islam) → ●●●●● (Abbasiyah) → ●●○○○ (Kemunduran)
- Architecture evolves: tents → grand mosques → ruins
- Light direction: Kenabian = from above; Kemunduran = dim/twilight
- Era boundary: background gradient blend 500ms, pattern crossfade

---

## 8. Accessibility

- Contrast: WCAG AA minimum (4.5:1 text, 3:1 large)
- Focus: 2px solid ring, era color, 2px offset
- Skip links, ARIA labels on all interactive elements
- `prefers-reduced-motion`: disable parallax, simplify transitions
- Font scaling: support 200% zoom
- RTL: `dir="rtl"` for Arabic blocks, Amiri auto-applied
