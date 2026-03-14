# Contributing to Baitul Hikmah

## Branch Strategy

| Branch | Environment | URL | Deploy |
|--------|-------------|-----|--------|
| `develop` | Development/QA | dev.baitul-hikmah.id | Auto on push |
| `main` | Production | baitul-hikmah.id | Ahmad approve → merge |

## Workflow

1. All work happens on `develop` branch (or feature branches → PR to `develop`)
2. QA tests on `dev.baitul-hikmah.id`
3. When ready: PR from `develop` → `main`
4. Ahmad reviews & approves
5. Merge → auto-deploy to production

## Content Validation

All historical content MUST follow the **Manhaj Bukhari** methodology:

1. **ISNAD** — Trace the chain of sources
2. **MATAN** — Verify content consistency
3. **JARH WA TA'DIL** — Assess source credibility
4. **TAWATUR** — Cross-reference with independent sources

Only **sahih** (verified) information is accepted. Dha'if sources are marked, maudhu' (fabricated) are rejected.

## Content Structure per Event

Each event needs:
- `adult-id.mdx` — Full article (Bahasa Indonesia)
- `adult-en.mdx` — Full article (English)
- `children-id.mdx` — Children's storytelling (Bahasa Indonesia)
- `children-en.mdx` — Children's storytelling (English)
- `metadata.json` — Structured data

## Code Standards

- TypeScript strict mode
- Tailwind CSS (no inline styles)
- Components in `/src/components/`
- Data in `/src/data/`
- Mobile-first responsive design
