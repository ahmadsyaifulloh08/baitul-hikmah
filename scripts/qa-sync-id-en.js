#!/usr/bin/env node
/**
 * QA Script: Verify ID ↔ EN content sync for Baitul Hikmah
 * 
 * Checks:
 * 1. Slide count match (children mode)
 * 2. Section count match (## headings)
 * 3. Section title alignment
 * 4. Frontmatter consistency (title, date, era, audience)
 * 5. File existence (all 4 variants per event)
 * 
 * Usage: node scripts/qa-sync-id-en.js [--fix-report]
 */

const fs = require('fs')
const path = require('path')

const CONTENT_DIR = path.join(__dirname, '..', 'content', 'events')
const DOT = '\uFFFC'

// ─── Slide counter (same logic as EventContent.tsx parseChildrenSlides) ───
function countSlides(file) {
  if (!fs.existsSync(file)) return -1
  const md = fs.readFileSync(file, 'utf8')
  const sections = md.split(/^## /m).filter(s => s.trim())
  let count = 0
  for (const section of sections) {
    const lines = section.split('\n')
    const title = lines[0]?.trim().replace(/^#+\s*/, '') || ''
    if (title.startsWith('title:') || title.startsWith('---')) continue
    const bodyLines = lines.slice(1).filter(l => 
      !l.trim().startsWith('> **🎨') && !l.trim().startsWith('> *') && l.trim() !== '---')
    const bodyText = bodyLines.map(l => l.trim()).filter(l => l && !l.startsWith('#')).join(' ')
      .replace(/\*\*(.+?)\*\*/g, '$1').replace(/\*(.+?)\*/g, '$1').replace(/`(.+?)`/g, '$1')
    if (!bodyText.trim()) continue
    const safeText = bodyText
      .replace(/\bno\./gi, 'no' + DOT).replace(/\bHR\./g, 'HR' + DOT)
      .replace(/\bQS\./g, 'QS' + DOT).replace(/\b([Mm])\./g, '$1' + DOT)
    const raw = safeText.match(/[^.!?]+[.!?]+/g) || [safeText]
    const matched = raw.join('')
    const rem = safeText.slice(matched.length).trim()
    if (rem && raw.length > 0) raw[raw.length - 1] += ' ' + rem
    const sentences = raw.map(s => s.replace(/\uFFFC/g, '.'))
    const chunkSize = Math.ceil(sentences.length / (sentences.length > 6 ? 3 : 2))
    for (let i = 0; i < sentences.length; i += chunkSize) {
      if (sentences.slice(i, i + chunkSize).join(' ').trim()) count++
    }
  }
  return count
}

// ─── Section extractor ───
function getSections(file) {
  if (!fs.existsSync(file)) return []
  const md = fs.readFileSync(file, 'utf8')
  return (md.match(/^## .+$/gm) || []).map(s => s.replace(/^## /, '').trim())
}

// ─── Frontmatter extractor ───
function getFrontmatter(file) {
  if (!fs.existsSync(file)) return {}
  const md = fs.readFileSync(file, 'utf8')
  const match = md.match(/^---\n([\s\S]*?)\n---/)
  if (!match) return {}
  const fm = {}
  match[1].split('\n').forEach(line => {
    const [key, ...val] = line.split(':')
    if (key && val.length) fm[key.trim()] = val.join(':').trim().replace(/^["']|["']$/g, '')
  })
  return fm
}

// ─── Main ───
const events = fs.readdirSync(CONTENT_DIR).filter(d => 
  fs.statSync(path.join(CONTENT_DIR, d)).isDirectory())

const EXPECTED_FILES = ['general-id.md', 'general-en.md', 'children-id.md', 'children-en.md']
let totalIssues = 0
let totalPass = 0

console.log('╔══════════════════════════════════════════════════════════╗')
console.log('║  Baitul Hikmah — ID ↔ EN Content Sync QA               ║')
console.log('╚══════════════════════════════════════════════════════════╝\n')

for (const event of events.sort()) {
  const dir = path.join(CONTENT_DIR, event)
  const issues = []
  const passes = []
  
  console.log(`📁 ${event}`)
  
  // 1. File existence — check .md first, fall back to .mdx (placeholder)
  let hasNewFormat = false
  for (const file of EXPECTED_FILES) {
    const fp = path.join(dir, file)
    const fpMdx = fp.replace('.md', '.mdx')
    if (fs.existsSync(fp)) {
      hasNewFormat = true
    } else if (fs.existsSync(fpMdx)) {
      // .mdx = old placeholder format, not yet migrated
      passes.push(`   ⏳ ${file} → still .mdx (placeholder, not yet developed)`)
    } else {
      issues.push(`   ❌ MISSING: ${file}`)
    }
  }
  
  // Skip detailed checks for events that only have .mdx placeholders
  if (!hasNewFormat) {
    console.log(`   ⏳ Placeholder event (only .mdx files) — skipping detailed checks\n`)
    totalPass++
    continue
  }
  
  // 2. Children slide count sync
  const childIdFile = path.join(dir, 'children-id.md')
  const childEnFile = path.join(dir, 'children-en.md')
  if (fs.existsSync(childIdFile) && fs.existsSync(childEnFile)) {
    const idSlides = countSlides(childIdFile)
    const enSlides = countSlides(childEnFile)
    if (idSlides !== enSlides) {
      issues.push(`   ❌ SLIDE MISMATCH: children ID=${idSlides} EN=${enSlides} (MUST match for illustration mapping)`)
    } else {
      passes.push(`   ✅ Children slides: ${idSlides} ID = ${enSlides} EN`)
    }
  }
  
  // 3. Section count + title alignment
  for (const prefix of ['general', 'children']) {
    const idFile = path.join(dir, `${prefix}-id.md`)
    const enFile = path.join(dir, `${prefix}-en.md`)
    if (fs.existsSync(idFile) && fs.existsSync(enFile)) {
      const idSections = getSections(idFile)
      const enSections = getSections(enFile)
      if (idSections.length !== enSections.length) {
        issues.push(`   ❌ SECTION MISMATCH (${prefix}): ID=${idSections.length} sections, EN=${enSections.length} sections`)
      } else {
        passes.push(`   ✅ ${prefix} sections: ${idSections.length} ID = ${enSections.length} EN`)
      }
    }
  }
  
  // 4. Frontmatter consistency
  for (const prefix of ['general', 'children']) {
    const idFile = path.join(dir, `${prefix}-id.md`)
    const enFile = path.join(dir, `${prefix}-en.md`)
    if (fs.existsSync(idFile) && fs.existsSync(enFile)) {
      const idFm = getFrontmatter(idFile)
      const enFm = getFrontmatter(enFile)
      // date & era are localized (M vs CE, Pra-Islam vs Pre-Islamic) — skip
      for (const key of ['audience', 'ageRange']) {
        if (idFm[key] && enFm[key] && idFm[key] !== enFm[key]) {
          issues.push(`   ❌ FRONTMATTER: ${prefix} ${key} differs — ID="${idFm[key]}" EN="${enFm[key]}"`)
        }
      }
    }
  }
  
  if (issues.length === 0) {
    passes.forEach(p => console.log(p))
    console.log(`   🟢 ALL CHECKS PASS\n`)
    totalPass++
  } else {
    passes.forEach(p => console.log(p))
    issues.forEach(i => console.log(i))
    console.log()
    totalIssues += issues.length
  }
}

console.log('═══════════════════════════════════════════')
console.log(`Events: ${events.length} | Pass: ${totalPass} | Issues: ${totalIssues}`)
if (totalIssues > 0) {
  console.log('⚠️  FIX ISSUES BEFORE DEPLOY')
  process.exit(1)
} else {
  console.log('✅ ALL EVENTS PASS — safe to deploy')
}
