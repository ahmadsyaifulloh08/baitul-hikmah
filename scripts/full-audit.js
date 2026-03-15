const fs = require('fs')

const DOT = '\uFFFC'
function getSlides(eventDir, mdFile) {
  const md = fs.readFileSync(mdFile, 'utf8')
  const sections = md.split(/^## /m).filter(s => s.trim())
  const slides = []
  let slideIdx = 0
  for (const section of sections) {
    const lines = section.split('\n')
    const title = lines[0]?.trim().replace(/^#+\s*/, '') || ''
    if (title.startsWith('title:') || title.startsWith('---')) continue
    const bodyLines = lines.slice(1).filter(l => !l.trim().startsWith('> **🎨') && !l.trim().startsWith('> *') && l.trim() !== '---')
    const bodyText = bodyLines.map(l => l.trim()).filter(l => l && !l.startsWith('#')).join(' ')
      .replace(/\*\*(.+?)\*\*/g, '$1').replace(/\*(.+?)\*/g, '$1').replace(/`(.+?)`/g, '$1')
    if (!bodyText.trim()) continue
    const safeText = bodyText.replace(/\bno\./gi,'no'+DOT).replace(/\bHR\./g,'HR'+DOT).replace(/\bQS\./g,'QS'+DOT).replace(/\b([Mm])\./g,'$1'+DOT)
    const raw = safeText.match(/[^.!?]+[.!?]+/g) || [safeText]
    const matched = raw.join(''); const rem = safeText.slice(matched.length).trim()
    if (rem && raw.length > 0) raw[raw.length-1] += ' ' + rem
    const sentences = raw.map(s => s.replace(/\uFFFC/g, '.'))
    const chunkSize = Math.ceil(sentences.length / (sentences.length > 6 ? 3 : 2))
    for (let i = 0; i < sentences.length; i += chunkSize) {
      const chunk = sentences.slice(i, i + chunkSize).join(' ').trim()
      if (!chunk) continue
      slideIdx++
      const imgFile = `public/illustrations/children/${eventDir}-slide-${String(slideIdx).padStart(2,'0')}.png`
      const imgExists = fs.existsSync(imgFile)
      slides.push({ n: slideIdx, title, text: chunk.substring(0, 80), imgFile, imgExists })
    }
  }
  return slides
}

console.log('=== E01 TAHUN GAJAH ===')
const e01 = getSlides('e01', 'content/events/e01-tahun-gajah/children-id.md')
e01.forEach(s => console.log(`  Slide ${s.n}: ${s.imgExists ? '✅' : '❌'} ${s.imgFile.split('/').pop()} | "${s.text}..."`))
console.log(`  Total: ${e01.length} slides, ${e01.filter(s=>s.imgExists).length} images found\n`)

console.log('=== E02 YATIM PIATU ===')
const e02 = getSlides('e02', 'content/events/e02-yatim-piatu/children-id.md')
e02.forEach(s => console.log(`  Slide ${s.n}: ${s.imgExists ? '✅' : '❌'} ${s.imgFile.split('/').pop()} | "${s.text}..."`))
console.log(`  Total: ${e02.length} slides, ${e02.filter(s=>s.imgExists).length} images found`)
