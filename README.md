# 🕌 Baitul Hikmah — Menelusuri Jejak Peradaban Islam

> "Sesungguhnya para nabi tidak mewariskan dinar ataupun dirham, tetapi mewariskan ilmu."
> — HR. Abu Dawud, Tirmidzi, Ibnu Majah

Portal digital interaktif untuk menelusuri sejarah peradaban Islam — dari Tahun Gajah (570 M) hingga jatuhnya Al-Andalus (1492 M).

## 🌐 Links

- **Production**: [baitul-hikmah.id](https://baitul-hikmah.id)
- **Development**: [dev.baitul-hikmah.id](https://dev.baitul-hikmah.id)

## ✨ Features

- **Interactive Timeline** — 128+ events across 7 eras of Islamic civilization
- **GIS Map Mode** — Explore events on a historical world map
- **Dual Audience** — Adult mode (academic) & Children's mode (storytelling)
- **Bilingual** — Bahasa Indonesia & English
- **PWA** — Install as app, offline reading
- **Verified Sources** — Manhaj Bukhari methodology for content validation

## 🛠 Tech Stack

- **Framework**: Next.js 14+ (App Router)
- **Styling**: Tailwind CSS + shadcn/ui
- **Animation**: Framer Motion + GSAP
- **Map**: MapLibre GL JS + Protomaps
- **Content**: MDX + JSON data
- **Hosting**: Cloudflare Pages
- **Typography**: Playfair Display, Inter, Amiri (Arabic)

## 🚀 Getting Started

```bash
npm install
npm run dev     # http://localhost:3000
npm run build   # Static export to /out
```

## 📁 Project Structure

```
├── src/
│   ├── app/           # Next.js App Router pages
│   ├── components/    # React components
│   ├── data/          # Events JSON, regions, categories
│   └── content/       # MDX articles per event
├── public/            # Static assets, maps
├── design/            # Design system, moodboard, SVG assets
└── content/
    └── events/        # Research output per event (adult + children, ID + EN)
```

## 📖 Documentation

- **PRD**: See internal docs
- **Research Plan**: Manhaj Bukhari → Elaborasi methodology
- **Design System**: See `/design/`

## 🤝 Contributing

This is an AhadByte project. Content is validated using Islamic scholarly methodology (Manhaj Bukhari).

## 📜 License

Content: CC BY-NC-SA 4.0 (Attribution, Non-Commercial, Share Alike)
Code: MIT

---

> رَبِّ زِدْنِي عِلْمًا
> "Rabbi zidni 'ilma" — "Ya Tuhanku, tambahkanlah ilmu kepadaku." (QS. Taha: 114)
