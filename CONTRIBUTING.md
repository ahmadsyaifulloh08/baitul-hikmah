# Contributing to Baitul Hikmah

## Branch Strategy

| Branch | Environment | URL | Deploy |
|--------|-------------|-----|--------|
| `develop` | Staging | develop.baitul-hikmah.pages.dev | Auto via Cloudflare Pages |
| `main` | Production | baitul-hikmah.id | Manual merge from develop |

## Workflows

See `docs/README.md` for detailed step-by-step workflows.

### General Content (Workflow A)
```
Write .md → Update events-database.json → QA → Build → Push
```

### Children + Illustrations (Workflow B)
```
Write .md → Brief → Prompts → Generate images → Compress → QA → Push
```

## Content Structure per Event

```
content/events/{event}/
├── general-id.md      ← adult article (Bahasa Indonesia)
├── general-en.md      ← adult article (English)
├── children-id.md     ← children storytelling (Bahasa Indonesia)
└── children-en.md     ← children storytelling (English)
```

Event metadata lives in `src/data/events-database.json` (single SSoT).

## Content Validation

All content follows **Manhaj Bukhari** methodology + automated QA:

1. **ISNAD** — Trace the chain of sources
2. **MATAN** — Verify content consistency
3. **JARH WA TA'DIL** — Assess source credibility
4. **TAWATUR** — Cross-reference with independent sources
5. **Automated QA** — `python3 scripts/qa-all.py` before every push

### QA Checks (CI/CD enforced)
- **Citations** — consolidated format, ^N matches bibliography
- **Quran** — Arabic text present for every verse reference
- **Metadata** — events-database.json completeness
- **Docs** — no stale references to renamed/deleted files
- **Images** — size 1-2MB, correct count per event

## Key Docs

| Doc | Purpose |
|-----|---------|
| `docs/README.md` | Full documentation index + workflows |
| `docs/content-style-guide.md` | Writing rules, citations, Quran format |
| `docs/illustration-registry.md` | Character descriptions (SSoT) |
| `docs/briefs/*.md` | Per-episode image briefs |

## Code Standards

- TypeScript strict mode
- Next.js App Router
- Tailwind CSS
- Doc reference comments in every file (`// See: docs/xxx.md`)
- Mobile-first responsive design
