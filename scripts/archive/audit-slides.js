const fs = require('fs')
const md = fs.readFileSync('/workspace/projects/baitul-hikmah/content/events/e01-tahun-gajah/children-id.md', 'utf8')

const DOT = '\uFFFC'
const sections = md.split(/^## /m).filter(s => s.trim())

let slideIdx = 0
for (const section of sections) {
  const lines = section.split('\n')
  const title = lines[0]?.trim().replace(/^#+\s*/, '') || ''
  if (title.startsWith('title:') || title.startsWith('---')) continue
  
  const bodyLines = lines.slice(1)
    .filter(l => !l.trim().startsWith('> **🎨') && !l.trim().startsWith('> *') && l.trim() !== '---')
  
  const bodyText = bodyLines.map(l => l.trim()).filter(l => l && !l.startsWith('#')).join(' ')
    .replace(/\*\*(.+?)\*\*/g, '$1').replace(/\*(.+?)\*/g, '$1').replace(/`(.+?)`/g, '$1')
  
  if (!bodyText.trim()) continue

  const safeText = bodyText.replace(/\bno\./gi, 'no'+DOT).replace(/\bHR\./g, 'HR'+DOT).replace(/\bQS\./g, 'QS'+DOT).replace(/\b([Mm])\./g, '$1'+DOT)
  const rawSentences = safeText.match(/[^.!?]+[.!?]+/g) || [safeText]
  const matched = rawSentences.join('')
  const remainder = safeText.slice(matched.length).trim()
  if (remainder && rawSentences.length > 0) rawSentences[rawSentences.length-1] += ' ' + remainder
  const sentences = rawSentences.map(s => s.replace(/\uFFFC/g, '.'))
  
  const chunkSize = Math.ceil(sentences.length / (sentences.length > 6 ? 3 : 2))
  
  for (let i = 0; i < sentences.length; i += chunkSize) {
    const chunk = sentences.slice(i, i + chunkSize).join(' ').trim()
    if (!chunk) continue
    slideIdx++
    console.log(`\n=== SLIDE ${slideIdx} (e01-slide-${String(slideIdx).padStart(2,'0')}) ===`)
    console.log(`Section: ${title}`)
    console.log(`Text: ${chunk.substring(0, 120)}...`)
  }
}
