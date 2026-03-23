/**
 * build-content.js — Prebuild script: .md files → event-content-map.json
 *
 * SSoT: content/events/{slug}/*.md
 * Output: src/data/event-content-map.json (consumed by EventContent.tsx)
 * Slug mapping: events-database.json (event.title → slugified key)
 *
 * See: docs/README.md (Content Flow section)
 * See: docs/content-style-guide.md (content format rules)
 *
 * Run: node scripts/build-content.js (auto-runs via `npm run prebuild`)
 */
const fs = require('fs')
const path = require('path')

const contentDir = path.join(__dirname, '..', 'content', 'events')
const agendaFile = path.join(__dirname, '..', 'src', 'data', 'events-database.json')
const outFile = path.join(__dirname, '..', 'src', 'data', 'event-content-map.json')

// Load research agenda for slug mapping (folder e-id → title slug)
const agenda = JSON.parse(fs.readFileSync(agendaFile, 'utf8'))
const idToSlug = {}
for (const ev of agenda.events) {
  const slug = ev.title.toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim()
  idToSlug[ev.id] = slug
}

const result = {}

if (fs.existsSync(contentDir)) {
  const dirs = fs.readdirSync(contentDir)
  for (const dir of dirs) {
    const dirPath = path.join(contentDir, dir)
    if (!fs.statSync(dirPath).isDirectory()) continue
    
    // Extract event id (e01, e57, etc)
    const eid = dir.split('-')[0]
    const titleSlug = idToSlug[eid]
    if (!titleSlug) {
      console.warn(`  WARN: ${dir} — no matching event in events-database.json`)
      continue
    }

    const entry = {}
    for (const file of fs.readdirSync(dirPath)) {
      const filePath = path.join(dirPath, file)
      
      if (file.endsWith('.md') || file.endsWith('.mdx')) {
        const content = fs.readFileSync(filePath, 'utf8')
        // Strip frontmatter
        const stripped = content.replace(/^---[\s\S]*?---\n*/, '')
        if (stripped.length > 50) {
          // Use key format: general-en, children-id, etc
          const key = file.replace(/\.(md|mdx)$/, '')
          entry[key] = stripped
        }
      }
      // Skip .json files (metadata — not content)
    }
    
    if (Object.keys(entry).length > 0) {
      result[titleSlug] = entry
    }
  }
}

fs.writeFileSync(outFile, JSON.stringify(result, null, 2))
console.log(`Built content for ${Object.keys(result).length} events → ${outFile}`)
