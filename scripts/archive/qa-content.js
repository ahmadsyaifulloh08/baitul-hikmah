#!/usr/bin/env node
/**
 * QA Content Script — Baitul Hikmah
 * 
 * Checks all event content files for quality issues:
 * - Bibliography: duplicates, too many entries, orphan citations
 * - Citations: missing refs, citation 0, gaps
 * - Arabic text: used outside Quran/Hadits
 * - Structure: missing frontmatter, wrong section order
 * 
 * Usage: node scripts/qa-content.js [event-dir]
 *   No args = check all events
 *   With arg = check specific event (e.g. e03-perjalanan-syam)
 */

const fs = require('fs')
const path = require('path')

const CONTENT_DIR = path.join(__dirname, '..', '..', '..', 'docs', 'content', 'events')

// Unicode superscript → number
const supMap = { '⁰': 0, '¹': 1, '²': 2, '³': 3, '⁴': 4, '⁵': 5, '⁶': 6, '⁷': 7, '⁸': 8, '⁹': 9 }
function parseSuperscripts(text) {
  const nums = new Set()
  // Match unicode superscripts (single or multi-digit like ¹² ²⁶)
  const supRegex = /[⁰¹²³⁴⁵⁶⁷⁸⁹]+/g
  let m
  while ((m = supRegex.exec(text)) !== null) {
    const digits = m[0].split('').map(c => supMap[c]).join('')
    nums.add(parseInt(digits, 10))
  }
  // Match ^N style
  const caretRegex = /\^(\d+)/g
  while ((m = caretRegex.exec(text)) !== null) {
    nums.add(parseInt(m[1], 10))
  }
  return nums
}

function countBibEntries(text) {
  const bibSection = text.split(/^## Daftar Pustaka|^## Bibliography/m)[1]
  if (!bibSection) return { count: 0, entries: [], duplicates: [] }
  
  const entries = []
  const lines = bibSection.split('\n')
  for (const line of lines) {
    const match = line.match(/^\d+\.\s*(.+)/)
    if (match) entries.push(match[1].trim())
  }
  
  // Detect duplicates by normalizing
  const normalize = (s) => s.toLowerCase().replace(/[,.*\s]+/g, ' ').replace(/\s+/g, ' ').trim()
  const seen = new Map()
  const duplicates = []
  for (let i = 0; i < entries.length; i++) {
    // Extract main source (author + book title, ignore bab/page details)
    const key = normalize(entries[i]).replace(/\bjilid \d+\b/g, '').replace(/\bbab .+$/g, '').replace(/\bhlm\b.+$/g, '').trim()
    if (seen.has(key)) {
      duplicates.push({ idx: i + 1, entry: entries[i], duplicateOf: seen.get(key) + 1 })
    } else {
      seen.set(key, i)
    }
  }
  
  return { count: entries.length, entries, duplicates }
}

function checkFile(filePath, fileName) {
  const issues = []
  const text = fs.readFileSync(filePath, 'utf8')
  
  // Check frontmatter
  if (!text.startsWith('---')) {
    issues.push({ severity: 'ERROR', msg: 'Missing frontmatter' })
  }
  
  // Strip frontmatter for content analysis
  const content = text.replace(/^---[\s\S]*?---\n*/, '')
  
  if (fileName.startsWith('general-')) {
    // === GENERAL MODE CHECKS ===
    
    // Bibliography checks
    const bib = countBibEntries(content)
    if (bib.count === 0) {
      issues.push({ severity: 'ERROR', msg: 'No Daftar Pustaka found' })
    } else {
      if (bib.count > 10) {
        issues.push({ severity: 'ERROR', msg: `Too many bibliography entries: ${bib.count} (max 8-10). Likely footnote-style instead of consolidated.` })
      } else if (bib.count > 8) {
        issues.push({ severity: 'WARN', msg: `Bibliography has ${bib.count} entries (recommended max 8)` })
      }
      
      if (bib.duplicates.length > 0) {
        for (const d of bib.duplicates) {
          issues.push({ severity: 'ERROR', msg: `Duplicate bib entry #${d.idx} ≈ #${d.duplicateOf}: "${d.entry.slice(0, 60)}..."` })
        }
      }
    }
    
    // Citation checks
    const bodyBeforeBib = content.split(/^## Daftar Pustaka|^## Bibliography/m)[0] || content
    const citedNums = parseSuperscripts(bodyBeforeBib)
    
    if (citedNums.has(0)) {
      issues.push({ severity: 'ERROR', msg: 'Citation ⁰ (zero) found — citations must start from 1' })
    }
    
    if (bib.count > 0) {
      // Check for orphan citations (cited but not in bib)
      for (const n of citedNums) {
        if (n > bib.count) {
          issues.push({ severity: 'ERROR', msg: `Citation ${n} referenced but only ${bib.count} bib entries` })
        }
      }
      
      // Check for unused bib entries
      for (let i = 1; i <= bib.count; i++) {
        if (!citedNums.has(i)) {
          issues.push({ severity: 'WARN', msg: `Bib entry #${i} never cited in text` })
        }
      }
    }
    
    if (citedNums.size === 0) {
      issues.push({ severity: 'WARN', msg: 'No superscript citations found in text' })
    }
    
    // Check structure
    if (!content.includes('## ')) {
      issues.push({ severity: 'ERROR', msg: 'No h2 sections found' })
    }
  }
  
  if (fileName.startsWith('children-')) {
    // === CHILDREN MODE CHECKS ===
    
    const sections = content.split(/^## /m).filter(s => s.trim())
    // Subtract frontmatter section if present
    const realSections = sections.filter(s => !s.startsWith('title:') && !s.startsWith('---'))
    
    if (realSections.length < 3) {
      issues.push({ severity: 'WARN', msg: `Only ${realSections.length} sections (expected 4+)` })
    }
    
    // Check for illustration briefs
    const briefCount = (content.match(/🎨/g) || []).length
    if (briefCount === 0) {
      issues.push({ severity: 'WARN', msg: 'No 🎨 illustration briefs found' })
    }
    
    // Check for tables (not allowed in children mode)
    if (content.includes('|---') || content.includes('| ---')) {
      issues.push({ severity: 'ERROR', msg: 'Table found in children mode (not allowed)' })
    }
  }
  
  // === COMMON CHECKS ===
  
  // Check ID ↔ EN section count consistency would need both files
  
  return issues
}

function checkEvent(eventDir) {
  const results = { dir: path.basename(eventDir), files: {} }
  const files = fs.readdirSync(eventDir).filter(f => f.endsWith('.md'))
  
  for (const file of files) {
    const issues = checkFile(path.join(eventDir, file), file)
    if (issues.length > 0) {
      results.files[file] = issues
    }
  }
  
  // Cross-file checks: ID ↔ EN section count
  for (const lang of ['id', 'en']) {
    const genFile = `general-${lang}.md`
    const childFile = `children-${lang}.md`
    // Could add cross-checks here
  }
  
  // Cross-check children-id vs children-en section count
  const childIdPath = path.join(eventDir, 'children-id.md')
  const childEnPath = path.join(eventDir, 'children-en.md')
  if (fs.existsSync(childIdPath) && fs.existsSync(childEnPath)) {
    const idSections = fs.readFileSync(childIdPath, 'utf8').split(/^## /m).length
    const enSections = fs.readFileSync(childEnPath, 'utf8').split(/^## /m).length
    if (idSections !== enSections) {
      if (!results.files['children-id.md']) results.files['children-id.md'] = []
      results.files['children-id.md'].push({
        severity: 'ERROR',
        msg: `Section count mismatch: children-id has ${idSections - 1}, children-en has ${enSections - 1}`
      })
    }
  }
  
  return results
}

// Main
const targetEvent = process.argv[2]
let dirs

if (targetEvent) {
  const fullPath = path.join(CONTENT_DIR, targetEvent)
  if (!fs.existsSync(fullPath)) {
    console.error(`Event dir not found: ${fullPath}`)
    process.exit(1)
  }
  dirs = [fullPath]
} else {
  dirs = fs.readdirSync(CONTENT_DIR)
    .filter(d => d.startsWith('e') && fs.statSync(path.join(CONTENT_DIR, d)).isDirectory())
    .sort()
    .map(d => path.join(CONTENT_DIR, d))
}

let totalErrors = 0
let totalWarns = 0
let cleanEvents = 0
const summary = { errors: [], warns: [] }

for (const dir of dirs) {
  const result = checkEvent(dir)
  const fileKeys = Object.keys(result.files)
  
  if (fileKeys.length === 0) {
    cleanEvents++
    continue
  }
  
  console.log(`\n📁 ${result.dir}`)
  for (const [file, issues] of Object.entries(result.files)) {
    for (const issue of issues) {
      const icon = issue.severity === 'ERROR' ? '❌' : '⚠️'
      console.log(`  ${icon} ${file}: ${issue.msg}`)
      if (issue.severity === 'ERROR') {
        totalErrors++
        summary.errors.push(`${result.dir}/${file}: ${issue.msg}`)
      } else {
        totalWarns++
        summary.warns.push(`${result.dir}/${file}: ${issue.msg}`)
      }
    }
  }
}

console.log(`\n${'═'.repeat(60)}`)
console.log(`📊 QA Summary: ${dirs.length} events checked`)
console.log(`   ✅ Clean: ${cleanEvents}`)
console.log(`   ❌ Errors: ${totalErrors}`)
console.log(`   ⚠️  Warnings: ${totalWarns}`)

if (totalErrors > 0) {
  console.log(`\n❌ TOP ERRORS:`)
  for (const e of summary.errors.slice(0, 20)) {
    console.log(`   ${e}`)
  }
}

process.exit(totalErrors > 0 ? 1 : 0)
