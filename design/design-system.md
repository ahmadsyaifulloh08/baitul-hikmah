# Baitul Hikmah — Design System

> Portal Sejarah Peradaban Islam | baitul-hikmah.id
> Version 1.0 — 2026-03-14

---

## 1. Color System

### 1.1 Era Colors (Primary Palette)

Each era has a primary color used for badges, timeline markers, accent borders, and backgrounds.

| Era | Primary | Light (bg) | Dark (text) | Usage |
|-----|---------|-----------|-------------|-------|
| Pra-Islam | `#8b949e` | `#8b949e1a` | `#6e7681` | Muted, subdued — pre-revelation era |
| Kenabian | `#3fb950` | `#3fb9501a` | `#2ea043` | Vibrant green — prophetic light |
| Rashidin | `#58a6ff` | `#58a6ff1a` | `#388bfd` | Calm blue — righteous governance |
| Umayyah | `#d29922` | `#d299221a` | `#bb8009` | Golden — empire & architecture |
| Abbasiyah | `#bc8cff` | `#bc8cff1a` | `#a371f7` | Royal purple — golden age of knowledge |
| Fragmentasi | `#f778ba` | `#f778ba1a` | `#db61a2` | Rose — resilience amid fragmentation |
| Kemunduran | `#da3633` | `#da36331a` | `#cf222e` | Deep red — decline & loss |

### 1.2 Neutral Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--bg-primary` | `#0d1117` | Page background (dark mode) |
| `--bg-secondary` | `#161b22` | Card/panel background |
| `--bg-tertiary` | `#21262d` | Hover states, subtle fills |
| `--bg-light` | `#fafbfc` | Page background (light mode) |
| `--bg-light-secondary` | `#f0f1f3` | Card background (light) |
| `--text-primary` | `#f0f6fc` | Main text (dark) / `#1f2328` (light) |
| `--text-secondary` | `#8b949e` | Captions, metadata |
| `--text-muted` | `#6e7681` | Disabled, hints |
| `--border` | `#30363d` | Dividers, card borders |
| `--border-light` | `#d0d7de` | Borders (light mode) |

### 1.3 Semantic Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--success` | `#3fb950` | Positive actions |
| `--warning` | `#d29922` | Caution states |
| `--danger` | `#da3633` | Destructive actions |
| `--info` | `#58a6ff` | Informational |

### 1.4 Children Mode Color Adjustments

In Mode Dongeng (children), colors shift warmer and brighter:

| Era | Adult | Children | Adjustment |
|-----|-------|----------|------------|
| Pra-Islam | `#8b949e` | `#a8b1ba` | +20% lightness |
| Kenabian | `#3fb950` | `#56d364` | +15% lightness, warmer |
| Rashidin | `#58a6ff` | `#79c0ff` | +15% lightness |
| Umayyah | `#d29922` | `#e3b341` | +15% lightness |
| Abbasiyah | `#bc8cff` | `#d2a8ff` | +15% lightness |
| Fragmentasi | `#f778ba` | `#ff9bce` | +15% lightness |
| Kemunduran | `#da3633` | `#f47067` | +20% lightness, less harsh |

Background shifts to warm cream: `#fdf6e3` (light) or `#1a1612` (dark).

---

## 2. Typography

### 2.1 Font Stack

| Role | Font | Weight | Fallback |
|------|------|--------|----------|
| **Headings** | Playfair Display | 700, 800 | Georgia, serif |
| **Body** | Inter | 400, 500, 600 | system-ui, sans-serif |
| **Arabic (Qur'an/Hadits)** | Amiri | 400, 700 | 'Scheherazade New', serif |
| **Arabic (UI)** | Noto Sans Arabic | 400, 600 | sans-serif |
| **Monospace** | JetBrains Mono | 400 | monospace |

### 2.2 Type Scale — Adult Mode

| Level | Size | Line Height | Weight | Font |
|-------|------|-------------|--------|------|
| `h1` | 2.5rem (40px) | 1.2 | 800 | Playfair Display |
| `h2` | 2rem (32px) | 1.25 | 700 | Playfair Display |
| `h3` | 1.5rem (24px) | 1.3 | 700 | Playfair Display |
| `h4` | 1.25rem (20px) | 1.4 | 600 | Inter |
| `body` | 1rem (16px) | 1.7 | 400 | Inter |
| `body-lg` | 1.125rem (18px) | 1.7 | 400 | Inter |
| `small` | 0.875rem (14px) | 1.5 | 400 | Inter |
| `caption` | 0.75rem (12px) | 1.4 | 500 | Inter |
| `arabic-verse` | 1.75rem (28px) | 2.0 | 400 | Amiri |
| `arabic-body` | 1.25rem (20px) | 1.8 | 400 | Amiri |

### 2.3 Type Scale — Children Mode (Mode Dongeng 🌙)

| Level | Size | Line Height | Weight | Notes |
|-------|------|-------------|--------|-------|
| `h1` | 3rem (48px) | 1.2 | 800 | Larger, more playful |
| `h2` | 2.25rem (36px) | 1.25 | 700 | |
| `h3` | 1.75rem (28px) | 1.3 | 700 | |
| `body` | 1.25rem (20px) | 1.8 | 400 | Bigger for readability |
| `arabic-verse` | 2rem (32px) | 2.0 | 400 | |

---

## 3. Spacing & Layout

### 3.1 Spacing Scale

Base unit: `4px`. Use Tailwind's spacing scale.

| Token | Value | Usage |
|-------|-------|-------|
| `xs` | 4px | Tight gaps (icon-text) |
| `sm` | 8px | Component internal padding |
| `md` | 16px | Card padding, form gaps |
| `lg` | 24px | Section gaps |
| `xl` | 32px | Major section separation |
| `2xl` | 48px | Page section breaks |
| `3xl` | 64px | Hero sections |
| `4xl` | 96px | Page top/bottom padding |

### 3.2 Container Widths

| Breakpoint | Max Width | Padding |
|------------|-----------|---------|
| Mobile | 100% | 16px |
| Tablet (768px) | 720px | 24px |
| Desktop (1024px) | 960px | 32px |
| Wide (1280px) | 1140px | 32px |
| Ultra (1536px) | 1280px | 32px |

### 3.3 Grid System

- **Timeline view**: Single column, centered (max 720px content)
- **Event cards grid**: 1 col (mobile) → 2 col (tablet) → 3 col (desktop)
- **Event detail**: Content (65%) + Sidebar (35%) on desktop; stacked on mobile
- **Map mode**: Full viewport, overlay panels

### 3.4 Children Mode Layout Adjustments

- Max content width: 640px (narrower for easier reading)
- Card padding: +50% (24px → 36px)
- Border radius: increased to 16px (more rounded, friendly)
- Gap between sections: +25%

---

## 4. Component Styles

### 4.1 Event Card

```
┌─────────────────────────────────┐
│ [Era Badge]         [Category]  │
│                                 │
│  Event Title (h3)               │
│  570 M · Makkah · Kenabian     │
│                                 │
│  Brief description text that    │
│  wraps to two lines max...      │
│                                 │
│  ●●○ Significance              │
└─────────────────────────────────┘
```

- **Background**: `var(--bg-secondary)`
- **Border**: 1px `var(--border)`, left-border 3px era color
- **Border-radius**: 8px (adult) / 16px (children)
- **Padding**: 20px (adult) / 28px (children)
- **Hover**: Translate Y -2px, shadow `0 4px 12px rgba(0,0,0,0.15)`, border-left brightens
- **Transition**: `all 200ms ease`

### 4.2 Era Badge

- **Shape**: Rounded pill (`border-radius: 999px`)
- **Background**: Era color at 15% opacity
- **Text**: Era color at full opacity
- **Font**: Inter 500, 12px (caption)
- **Padding**: 4px 12px
- **Icon**: Era SVG icon (8-pointed star, crescent, etc.) at 14px, left of text

### 4.3 Category Badge

- **Shape**: Square with rounded corners (6px)
- **Background**: transparent
- **Border**: 1px `var(--border)`
- **Icon**: Category SVG icon at 14px
- **Font**: Inter 400, 12px
- **Color**: `var(--text-secondary)`

### 4.4 Timeline Marker

```
    ●─── Event Card
    │
    ●─── Event Card
    │
    ◆─── Era Change (larger, diamond)
    │
    ●─── Event Card
```

- **Dot**: 12px circle, era color fill, 2px white border
- **Era change**: 20px diamond, era color, pulsing glow animation
- **Line**: 2px solid `var(--border)`, gradient transition between era colors
- **Active dot**: 16px, ring animation (`box-shadow: 0 0 0 4px {era-color}33`)

### 4.5 Buttons

#### Primary Button
- **Background**: Current era color
- **Text**: White or dark (auto-contrast)
- **Border-radius**: 8px (adult) / 12px (children)
- **Padding**: 10px 20px
- **Font**: Inter 500, 14px
- **Hover**: Darken 10%, slight scale (1.02)

#### Secondary Button (Ghost)
- **Background**: transparent
- **Border**: 1px era color
- **Text**: Era color
- **Hover**: Era color at 10% opacity bg

#### Mode Toggle Button (Dewasa ↔ Dongeng)
- **Shape**: Pill toggle (like iOS switch)
- **States**: ☀️ Dewasa (left) | 🌙 Dongeng (right)
- **Animation**: Slide + color morph (neutral → warm cream)
- **Size**: 48px height, 96px width

### 4.6 Dalil Card (Qur'an/Hadits)

```
┌─────────────────────────────────┐
│  ﷽                              │
│                                 │
│  إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ    │  ← Amiri, 28px, centered
│                                 │
│  "Sesungguhnya Kami telah       │  ← Inter, 16px, italic
│   memberikan kepadamu nikmat    │
│   yang banyak."                 │
│                                 │
│  — QS. Al-Kautsar: 1           │  ← caption, muted
└─────────────────────────────────┘
```

- **Background**: `var(--bg-tertiary)` or era color at 5%
- **Border**: Left 3px, `var(--success)` (green for Qur'an) or `var(--info)` (blue for Hadits)
- **Border-radius**: 8px
- **Arabic text**: Centered, `direction: rtl`, Amiri font
- **Translation**: Left-aligned, italic
- **Source**: Right-aligned, caption size, muted color

### 4.7 Bibliography Entry

- **Font**: Inter 400, 14px
- **Style**: Hanging indent (2em padding-left, -2em text-indent first line)
- **Author**: Bold
- **Title**: Italic
- **Separator**: Period + space

---

## 5. Iconography

### 5.1 Category Icons

All category icons are inline SVGs, 20px default, stroke-based (1.5px stroke).

| Category | Symbol | File |
|----------|--------|------|
| Kenabian | ☆ (Star) | `assets/icon-kenabian.svg` |
| Politik | ♛ (Crown) | `assets/icon-politik.svg` |
| Ilmu Pengetahuan | ≡ (Book/Lines) | `assets/icon-ilmu.svg` |
| Militer | ⚔ (Crossed Swords) | `assets/icon-militer.svg` |
| Peradaban | ◆ (Diamond) | `assets/icon-peradaban.svg` |
| Kemunduran | ↓ (Down Arrow) | `assets/icon-kemunduran.svg` |

### 5.2 UI Icons

Use **Lucide** icon set for general UI (search, menu, filter, chevron, share, etc.).

### 5.3 Mode Toggle Icon

Crescent moon (`assets/icon-mode-dongeng.svg`) — animated rotation on toggle.

---

## 6. Patterns & Decorative Elements

### 6.1 Islamic Geometric Patterns

Three pattern variations, implemented as repeating SVGs or CSS backgrounds:

| Pattern | File | Usage |
|---------|------|-------|
| **Star & Cross** | `assets/pattern-star-cross.svg` | Page header backgrounds |
| **Hexagonal Tessellation** | `assets/pattern-hexagonal.svg` | Section dividers |
| **Interlocking Squares** | `assets/pattern-interlocking.svg` | Card/panel subtle backgrounds |

All patterns: monochrome (current text color at 5-8% opacity), repeating tile.

### 6.2 Decorative Borders

- **Arabesque divider** (`assets/border-arabesque.svg`): Horizontal rule replacement
- **Corner ornament**: Used in Dalil cards and hero sections

### 6.3 Usage Guidelines

- Patterns should be **subtle** — never compete with content
- Opacity: 3-8% for backgrounds, 10-15% for dividers
- Color: Inherit from era color or neutral
- **Never stack** patterns — one pattern per visible section max

---

## 7. Motion & Animation

### 7.1 Timing

| Type | Duration | Easing |
|------|----------|--------|
| Micro (hover, focus) | 150ms | `ease-out` |
| Small (toggle, fade) | 200ms | `ease-in-out` |
| Medium (slide, expand) | 300ms | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Large (page transition) | 500ms | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Stagger (list items) | 50ms delay each | `ease-out` |

### 7.2 Page Transitions

- **Between pages**: Fade + slide-up (300ms)
- **Mode switch** (Adult ↔ Children): Color morph (500ms), layout reflow (300ms), font scale (200ms)
- **Era change** (timeline scroll): Background gradient shift (500ms)

### 7.3 Scroll Animations

- **Timeline events**: Fade-in + slide from left/right (alternating) on scroll into viewport
- **Map mode**: Pan/zoom synced with timeline slider (GSAP ScrollTrigger)
- **Parallax**: Hero sections only, subtle (max 20% offset)

---

## 8. Responsive Breakpoints

| Name | Min Width | Key Changes |
|------|-----------|-------------|
| `mobile` | 0 | Single column, bottom sheets, hamburger nav |
| `tablet` | 768px | 2-column grids, side panels |
| `desktop` | 1024px | Full layout, map + timeline side-by-side |
| `wide` | 1280px | Wider containers, 3-column grids |

### Mobile-Specific

- Timeline: Vertical only, left-aligned markers
- Event cards: Full width, swipe to navigate
- Map: Full screen, bottom sheet for event details
- Navigation: Bottom tab bar (Timeline | Map | Search | Settings)

---

## 9. Dark/Light Mode

- **Default**: Follows system preference (`prefers-color-scheme`)
- **Manual toggle**: Available in settings
- **Children mode**: Always light (warm cream background)
- **Transition**: 200ms background, 150ms text color

---

## 10. Accessibility

- **Contrast**: Minimum WCAG AA (4.5:1 for text, 3:1 for large text)
- **Focus indicators**: 2px solid ring, era color, 2px offset
- **Skip links**: To main content, to timeline, to navigation
- **ARIA labels**: All interactive elements, era badges, category icons
- **Reduced motion**: Respect `prefers-reduced-motion` — disable parallax, simplify transitions
- **Font scaling**: Support up to 200% browser zoom
- **RTL**: Arabic text blocks use `dir="rtl"`, Amiri font auto-applied
