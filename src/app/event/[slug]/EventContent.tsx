'use client'

import React, { useState } from 'react'
import { I18nProvider, useI18n } from '@/i18n/context'
import { motion, AnimatePresence } from 'framer-motion'
import { getEra, getCategory, slugify, events, regions, type Event } from '@/lib/data'
import Header from '@/components/Header'
import eventContentData from '@/data/event-content.json'
import eventContentMap from '@/data/event-content-map.json'

const categoryEmoji: Record<string, string> = {
  prophetic: '☆', political: '♛', knowledge: '≡',
  military: '⚔', heritage: '◆', decline: '↓',
}

// ─── Enhanced Markdown Renderer ─────────────────────────────────────
function renderMarkdown(md: string) {
  const lines = md.split('\n')
  let html = ''
  let inUl = false
  let inOl = false
  let inBlockquote = false
  let inTable = false
  let tableHeaders: string[] = []
  let olCounter = 0
  let inBibliography = false

  for (let i = 0; i < lines.length; i++) {
    const trimmed = lines[i].trim()

    // Skip frontmatter
    if (trimmed === '---') continue

    // Empty line — close lists/blockquotes (but peek ahead for continued ordered lists)
    if (!trimmed) {
      if (inUl) { html += '</ul>'; inUl = false }
      if (inOl) {
        // Peek ahead: if next non-empty line is also ordered list, keep counter going
        let nextNonEmpty = ''
        for (let j = i + 1; j < lines.length; j++) {
          if (lines[j].trim()) { nextNonEmpty = lines[j].trim(); break }
        }
        if (!/^\d+\.\s/.test(nextNonEmpty)) {
          html += '</ol>'; inOl = false; olCounter = 0
        }
      }
      if (inBlockquote) { html += '</blockquote>'; inBlockquote = false }
      if (inTable) { html += '</tbody></table></div>'; inTable = false }
      continue
    }

    // Table: detect header row (contains |)
    if (trimmed.includes('|') && !trimmed.startsWith('>')) {
      const cells = trimmed.split('|').map(c => c.trim()).filter(c => c)
      // Check if next line is separator (---|---|---)
      const nextLine = i + 1 < lines.length ? lines[i + 1].trim() : ''
      if (nextLine.match(/^[\|\-\s:]+$/) && nextLine.includes('|')) {
        // Table header
        tableHeaders = cells
        html += '<div style="overflow-x:auto;margin-bottom:16px"><table style="width:100%;border-collapse:collapse;font-size:13px">'
        html += '<thead><tr>'
        for (const h of cells) {
          html += `<th style="padding:8px 12px;border:1px solid var(--border);background:var(--bg-secondary);font-weight:600;text-align:left">${formatInline(h)}</th>`
        }
        html += '</tr></thead><tbody>'
        inTable = true
        i++ // skip separator line
        continue
      } else if (inTable) {
        // Table data row
        html += '<tr>'
        for (let j = 0; j < tableHeaders.length; j++) {
          html += `<td style="padding:8px 12px;border:1px solid var(--border)">${formatInline(cells[j] || '')}</td>`
        }
        html += '</tr>'
        continue
      }
    }

    // Close table if non-table line
    if (inTable && !trimmed.includes('|')) {
      html += '</tbody></table></div>'
      inTable = false
    }

    // Blockquote (handle "> text" and bare ">" continuation)
    if (trimmed === '>') {
      // Empty blockquote line — just continue the block, add spacing
      if (!inBlockquote) {
        html += '<blockquote style="border-left:3px solid #8B6914;padding:12px 16px;margin:16px 0;background:var(--bg-secondary);border-radius:0 8px 8px 0">'
        inBlockquote = true
      }
      html += '<div style="height:8px"></div>'
      continue
    }
    if (trimmed.startsWith('> ')) {
      if (!inBlockquote) {
        html += '<blockquote style="border-left:3px solid #8B6914;padding:12px 16px;margin:16px 0;background:var(--bg-secondary);border-radius:0 8px 8px 0">'
        inBlockquote = true
      }
      const bqText = trimmed.slice(2)
      if (isArabicLine(bqText)) {
        html += `<p dir="rtl" style="margin:8px 0;color:var(--text-primary);line-height:2.2;font-family:'Amiri',serif;font-size:1.3em;text-align:right;font-style:normal">${formatInline(bqText)}</p>`
      } else {
        html += `<p style="margin:4px 0;color:var(--text-primary);line-height:1.7">${formatInline(bqText)}</p>`
      }
      continue
    }
    if (inBlockquote && !trimmed.startsWith('>')) {
      html += '</blockquote>'
      inBlockquote = false
    }

    // Headers
    if (trimmed.startsWith('# ') && !trimmed.startsWith('## ')) {
      inBibliography = false
      // Skip h1 — title already shown in page header badges
      continue
    } else if (trimmed.startsWith('## ')) {
      inBibliography = /daftar pustaka|bibliography|referensi/i.test(trimmed)
      html += `<h2 class="font-heading" style="font-size:1.25rem;font-weight:600;margin:24px 0 12px">${formatInline(trimmed.slice(3))}</h2>`
    } else if (trimmed.startsWith('### ')) {
      html += `<h3 class="font-heading" style="font-size:1.1rem;font-weight:600;margin:16px 0 8px">${formatInline(trimmed.slice(4))}</h3>`
    }
    // Unordered list
    else if (trimmed.startsWith('- ') || (trimmed.startsWith('* ') && !trimmed.startsWith('**'))) {
      if (inOl) { html += '</ol>'; inOl = false; olCounter = 0 }
      if (!inUl) { html += '<ul style="list-style:disc;padding-left:24px;margin-bottom:16px">'; inUl = true }
      html += `<li style="font-size:14px;color:var(--text-secondary);margin-bottom:4px;line-height:1.6">${formatInline(trimmed.slice(2))}</li>`
    }
    // Ordered list
    else if (/^\d+\.\s/.test(trimmed)) {
      if (inUl) { html += '</ul>'; inUl = false }
      if (!inOl) { html += '<ol style="list-style:none;padding-left:0;margin-bottom:16px">'; inOl = true; olCounter = 0 }
      olCounter++
      const text = trimmed.replace(/^\d+\.\s*/, '')
      const refId = inBibliography ? ` id="ref-${olCounter}"` : ''
      html += `<li${refId} style="font-size:14px;color:var(--text-secondary);margin-bottom:8px;line-height:1.6;padding-left:24px;position:relative"><span style="position:absolute;left:0;font-weight:700;color:var(--text-primary)">${olCounter}.</span>${formatInline(text)}</li>`
    }
    // Horizontal rule
    else if (trimmed === '---' || trimmed === '***') {
      html += '<hr style="border:none;border-top:1px solid var(--border);margin:24px 0">'
    }
    // Paragraph
    else {
      if (inUl) { html += '</ul>'; inUl = false }
      if (inOl) { html += '</ol>'; inOl = false; olCounter = 0 }
      if (isArabicLine(trimmed)) {
        html += wrapArabicBlock(formatInline(trimmed))
      } else {
        html += `<p style="color:var(--text-secondary);line-height:1.8;margin-bottom:16px">${formatInline(trimmed)}</p>`
      }
    }
  }
  // Close any open tags
  if (inUl) html += '</ul>'
  if (inOl) html += '</ol>'
  if (inBlockquote) html += '</blockquote>'
  if (inTable) html += '</tbody></table></div>'
  return html
}

function formatInline(text: string) {
  return text
    // Bold
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // Italic
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Code
    .replace(/`(.+?)`/g, '<code style="font-size:13px;background:var(--bg-secondary);padding:2px 6px;border-radius:4px">$1</code>')
    // Superscript citations with anchor links (^1 → linked to #ref-1)
    .replace(/\^(\d+)/g, '<sup style="font-size:10px;color:#8B6914;font-weight:700"><a href="#ref-$1" style="color:#8B6914;text-decoration:none">$1</a></sup>')
    // Unicode superscript numbers (¹²³⁴⁵⁶⁷⁸⁹⁰) → linked
    .replace(/([\u00B9\u00B2\u00B3\u2074\u2075\u2076\u2077\u2078\u2079\u2070]+)/g, (match) => {
      const numMap: Record<string, string> = {'\u00B9':'1','\u00B2':'2','\u00B3':'3','\u2074':'4','\u2075':'5','\u2076':'6','\u2077':'7','\u2078':'8','\u2079':'9','\u2070':'0'}
      const nums = match.split('').map(c => numMap[c] || c).join('')
      // Each char is a separate ref number
      const refs = match.split('').map(c => {
        const n = numMap[c] || c
        return `<sup style="font-size:10px;color:#8B6914;font-weight:700"><a href="#ref-${n}" style="color:#8B6914;text-decoration:none">${n}</a></sup>`
      }).join(' ')
      return refs
    })
    // Single honorific symbols (ﷺ ﷻ etc) — keep inline, don't make RTL
    .replace(/([\uFDFA\uFDFB\uFDFD])/g, '<span style="font-family:\'Amiri\',serif">$1</span>')
}

// Check if a line is predominantly Arabic (for blockquote/paragraph level RTL)
function isArabicLine(text: string): boolean {
  const arabicChars = (text.match(/[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDCF\uFDF0-\uFDFF\uFE70-\uFEFF]/g) || []).length
  const totalChars = text.replace(/\s/g, '').length
  return totalChars > 0 && arabicChars / totalChars > 0.4
}

function wrapArabicBlock(html: string): string {
  return `<div dir="rtl" style="font-family:'Amiri','Scheherazade New',serif;font-size:1.3em;line-height:2.2;text-align:right;margin:12px 0;padding:8px 0;font-style:normal">${html}</div>`
}

// ─── Children Slideshow Component (Fullscreen Modal) ────────────────
function ChildrenSlideshow({ content, contentDir, onClose }: { content: string; contentDir?: string; onClose: () => void }) {
  const [currentSlide, setCurrentSlide] = useState(0)
  const [direction, setDirection] = useState(0) // -1 = left, 1 = right
  const slides = parseChildrenSlides(content, contentDir)
  
  const goNext = () => { if (currentSlide < slides.length - 1) { setDirection(1); setCurrentSlide(prev => prev + 1) } }
  const goPrev = () => { if (currentSlide > 0) { setDirection(-1); setCurrentSlide(prev => prev - 1) } }

  // Keyboard navigation
  React.useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') goNext()
      else if (e.key === 'ArrowLeft') goPrev()
      else if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  })

  // Lock body scroll when modal open
  React.useEffect(() => {
    document.body.style.overflow = 'hidden'
    return () => { document.body.style.overflow = '' }
  }, [])

  // Landscape hint for portrait mobile
  const [showLandscapeHint, setShowLandscapeHint] = React.useState(false)
  React.useEffect(() => {
    const mq = window.matchMedia('(orientation: portrait)')
    if (mq.matches) {
      setShowLandscapeHint(true)
      const timer = setTimeout(() => setShowLandscapeHint(false), 4000)
      return () => clearTimeout(timer)
    }
  }, [])

  if (slides.length === 0) return null

  const progress = ((currentSlide + 1) / slides.length) * 100

  return (
    <>
    <style>{`
      .slide-fullscreen { height: 100vh !important; height: 100dvh !important; }
      .slide-overlay-text { padding: 32px 16px 20px !important; max-height: 45% !important; }
      .slide-overlay-text h3 { font-size: 14px !important; margin-bottom: 4px !important; }
      .slide-overlay-text p { font-size: 12px !important; line-height: 1.55 !important; }
      @media (min-width: 480px) {
        .slide-overlay-text { padding: 40px 20px 24px !important; }
        .slide-overlay-text h3 { font-size: 16px !important; }
        .slide-overlay-text p { font-size: 13px !important; }
      }
      @media (min-width: 768px) {
        .slide-overlay-text { padding: 56px 32px 32px !important; max-height: 50% !important; }
        .slide-overlay-text h3 { font-size: 20px !important; }
        .slide-overlay-text p { font-size: 15px !important; line-height: 1.7 !important; }
      }
      @media (min-width: 1024px) {
        .slide-overlay-text { padding: 64px 48px 40px !important; }
        .slide-overlay-text h3 { font-size: 24px !important; }
        .slide-overlay-text p { font-size: 17px !important; }
      }
    `}</style>
    <motion.div
      className="slide-fullscreen"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      style={{
        position: 'fixed', inset: 0, zIndex: 9999,
        background: '#1a1510',
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      }}
    >
      {/* Progress bar */}
      <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 3, background: 'rgba(0,0,0,0.06)' }}>
        <motion.div
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.3 }}
          style={{ height: '100%', background: '#D4A843', borderRadius: '0 2px 2px 0' }}
        />
      </div>

      {/* Close button */}
      <button onClick={onClose} style={{
        position: 'absolute', top: 12, right: 12, zIndex: 10,
        background: 'rgba(0,0,0,0.3)', border: 'none', borderRadius: '50%',
        width: 36, height: 36, cursor: 'pointer', fontSize: 18, color: '#fff',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>✕</button>

      {/* Landscape hint for portrait mobile */}
      {showLandscapeHint && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
          style={{
            position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
            zIndex: 20, background: 'rgba(0,0,0,0.7)', borderRadius: 12,
            padding: '12px 20px', color: '#fff', fontSize: 14, textAlign: 'center',
            pointerEvents: 'none',
          }}
          onAnimationComplete={() => setTimeout(() => setShowLandscapeHint(false), 3000)}
        >
          📱🔄 Putar HP untuk pengalaman terbaik
        </motion.div>
      )}

      {/* Slide counter */}
      <div style={{
        position: 'absolute', top: 18, left: 20, zIndex: 10,
        fontSize: 'clamp(10px, 2vw, 13px)', color: 'rgba(255,255,255,0.6)', fontWeight: 500,
      }}>
        {currentSlide + 1} / {slides.length}
      </div>

      {/* Slide container — fullscreen */}
      <motion.div
        drag="x"
        dragConstraints={{ left: 0, right: 0 }}
        dragElastic={0.2}
        onDragEnd={(_, info) => {
          if (info.offset.x < -60) goNext()
          else if (info.offset.x > 60) goPrev()
        }}
        className="slide-fullscreen"
        style={{
          width: '100vw', height: '100vh',
          position: 'absolute', inset: 0, overflow: 'hidden',
          touchAction: 'pan-y',
          background: '#1a1510',
        }}
      >
        <AnimatePresence mode="wait" initial={false}>
          <motion.div
            key={currentSlide}
            initial={{ opacity: 0, x: direction * 80 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: direction * -80 }}
            transition={{ duration: 0.25, ease: 'easeOut' }}
            style={{ width: '100%', height: '100%', position: 'absolute', inset: 0 }}
          >
            {/* Full-screen image or emoji fallback */}
            {slides[currentSlide].image ? (
              <img src={slides[currentSlide].image} alt={slides[currentSlide].title}
                style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: 'center' }} />
            ) : (
              <div style={{
                width: '100%', height: '100%', display: 'flex', alignItems: 'center',
                justifyContent: 'center', fontSize: 96,
                background: slides[currentSlide].bgColor || '#faf3e0',
              }}>
                <span style={{ filter: 'drop-shadow(0 4px 12px rgba(0,0,0,0.1))' }}>
                  {slides[currentSlide].emoji || '📜'}
                </span>
              </div>
            )}

            {/* Gradient text overlay from bottom — responsive */}
            <div className="slide-overlay-text" style={{
              position: 'absolute', bottom: 0, left: 0, right: 0,
              background: 'linear-gradient(to top, rgba(20,15,5,0.9) 0%, rgba(20,15,5,0.75) 35%, rgba(20,15,5,0.4) 65%, transparent 100%)',
              padding: '48px 20px 24px',
              display: 'flex', flexDirection: 'column', justifyContent: 'flex-end',
              maxHeight: '55%',
              overflow: 'hidden',
              boxSizing: 'border-box',
            }}>
              {slides[currentSlide].title && (
                <h3 style={{
                  color: '#fff', fontSize: 16, fontWeight: 700,
                  marginBottom: 6, fontFamily: 'Playfair Display, serif',
                  lineHeight: 1.35, textShadow: '0 1px 4px rgba(0,0,0,0.8)',
                }}>
                  {slides[currentSlide].title}
                </h3>
              )}
              <p style={{
                color: 'rgba(255,255,255,0.93)', fontSize: 13, lineHeight: 1.65,
                margin: 0, userSelect: 'text',
                textShadow: '0 1px 3px rgba(0,0,0,0.7)',
                overflowY: 'auto',
                WebkitOverflowScrolling: 'touch',
              }}>
                {slides[currentSlide].text}
              </p>
            </div>
          </motion.div>
        </AnimatePresence>
      </motion.div>

      {/* Navigation arrows (desktop) */}
      {currentSlide > 0 && (
        <button onClick={goPrev} style={{
          position: 'absolute', left: 16, top: '50%', transform: 'translateY(-50%)',
          background: 'rgba(0,0,0,0.06)', border: 'none', borderRadius: '50%',
          width: 44, height: 44, cursor: 'pointer', fontSize: 20, color: '#5c4a2a', zIndex: 10,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>←</button>
      )}
      {currentSlide < slides.length - 1 && (
        <button onClick={goNext} style={{
          position: 'absolute', right: 16, top: '50%', transform: 'translateY(-50%)',
          background: 'rgba(0,0,0,0.06)', border: 'none', borderRadius: '50%',
          width: 44, height: 44, cursor: 'pointer', fontSize: 20, color: '#5c4a2a', zIndex: 10,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>→</button>
      )}

      {/* Dot indicators */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: 5, marginTop: 16 }}>
        {slides.map((_, i) => (
          <button key={i} onClick={() => { setDirection(i > currentSlide ? 1 : -1); setCurrentSlide(i) }} style={{
            width: i === currentSlide ? 20 : 8, height: 6, borderRadius: 3,
            background: i === currentSlide ? '#D4A843' : 'rgba(0,0,0,0.1)',
            border: 'none', cursor: 'pointer', transition: 'all 0.2s',
          }} />
        ))}
      </div>
    </motion.div>
    </>
  )
}

interface Slide {
  title: string
  text: string
  emoji: string
  bgColor: string
  image?: string
}

// Image map for children illustrations — per sub-slide, sequentially assigned
const childrenIllustrations: Record<string, string[]> = {
  'e01-tahun-gajah': Array.from({length: 10}, (_, i) => `/illustrations/children/e01-slide-${String(i+1).padStart(2,'0')}.png`),
  'e02-yatim-piatu': Array.from({length: 15}, (_, i) => `/illustrations/children/e02-slide-${String(i+1).padStart(2,'0')}.png`),
}

const sectionEmojis: Record<number, { emoji: string; bg: string }> = {
  0: { emoji: '🕌', bg: '#faf3e0' },
  1: { emoji: '🐘', bg: '#f0e8d4' },
  2: { emoji: '🐦', bg: '#e8f0e8' },
  3: { emoji: '👶', bg: '#f5eef0' },
  4: { emoji: '⭐', bg: '#f0f0f8' },
  5: { emoji: '📖', bg: '#faf5e8' },
}

function parseChildrenSlides(md: string, contentDir?: string): Slide[] {
  const slides: Slide[] = []
  const images = contentDir ? childrenIllustrations[contentDir] : undefined
  // Split by ## sections
  const sections = md.split(/^## /m).filter(s => s.trim())
  
  let sectionIdx = 0
  let slideIdx = 0
  for (const section of sections) {
    const sectionLines = section.split('\n')
    const sectionTitle = sectionLines[0]?.trim().replace(/^#+\s*/, '') || ''
    
    // Skip frontmatter section
    if (sectionTitle.startsWith('title:') || sectionTitle.startsWith('---')) continue
    // Skip illustration briefs
    const bodyLines = sectionLines.slice(1)
      .filter(l => !l.trim().startsWith('> **🎨') && !l.trim().startsWith('> *') && l.trim() !== '---')
    
    const bodyText = bodyLines
      .map(l => l.trim())
      .filter(l => l && !l.startsWith('#'))
      .join(' ')
      .replace(/\*\*(.+?)\*\*/g, '$1')
      .replace(/\*(.+?)\*/g, '$1')
      .replace(/`(.+?)`/g, '$1')
    
    if (!bodyText.trim()) continue

    // Split into 2-3 slides per section (roughly by sentences)
    // First protect abbreviations from sentence splitting: no. HR. QS. M. dll.
    // Protect abbreviations from sentence splitting by replacing dots with placeholder
    const DOT = '\uFFFC' // Object replacement char as dot placeholder
    const safeText = bodyText
      .replace(/\bno\./gi, 'no' + DOT)
      .replace(/\bHR\./g, 'HR' + DOT)
      .replace(/\bQS\./g, 'QS' + DOT)
      .replace(/\b([Mm])\./g, '$1' + DOT)
    const rawSentences = safeText.match(/[^.!?]+[.!?]+/g) || [safeText]
    // Capture any trailing text not ending in .!? (e.g. parenthetical references)
    const matched = rawSentences.join('')
    const remainder = safeText.slice(matched.length).trim()
    if (remainder && rawSentences.length > 0) {
      rawSentences[rawSentences.length - 1] += ' ' + remainder
    }
    const sentences = rawSentences.map(s => s.replace(/\uFFFC/g, '.'))
    const chunkSize = Math.ceil(sentences.length / (sentences.length > 6 ? 3 : 2))
    
    for (let i = 0; i < sentences.length; i += chunkSize) {
      const chunk = sentences.slice(i, i + chunkSize).join(' ').trim()
      if (!chunk) continue
      const { emoji, bg } = sectionEmojis[sectionIdx] || { emoji: '📜', bg: '#faf3e0' }
      slides.push({
        title: i === 0 ? sectionTitle : '',
        text: chunk,
        emoji,
        bgColor: bg,
        image: images?.[slideIdx],
      })
      slideIdx++
    }
    sectionIdx++
  }
  return slides
}

// ─── Main Component ─────────────────────────────────────────────────
function EventContentInner({ event }: { event: Event }) {
  const [storyMode, setStoryMode] = useState(false)
  const { t } = useI18n()
  const era = getEra(event.era)
  const cat = getCategory(event.category)
  
  const slug = slugify(event.title)
  const contentDir = (eventContentMap as Record<string, string>)[slug]
  const content = contentDir ? (eventContentData as any)[contentDir] : null
  const hasRichContent = !!content

  return (
    <main className="min-h-screen">
      <Header />
      <article className="max-w-3xl mx-auto px-4 py-8">
        <button
          onClick={() => window.history.length > 1 ? window.history.back() : window.location.href = '/'}
          className="text-xs text-[var(--text-secondary)] hover:underline mb-6 inline-block cursor-pointer"
          style={{ background: 'none', border: 'none', padding: 0, font: 'inherit' }}
        >
          {t('detail.back')}
        </button>

        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 12, alignItems: 'center' }}>
          <span style={{
            fontSize: 11, padding: '3px 10px', borderRadius: 14,
            background: era?.color, color: '#fff',
          }}>
            {era?.name}
          </span>
          <span style={{
            fontSize: 11, padding: '3px 10px', borderRadius: 14,
            background: cat?.color, color: '#fff',
          }}>
            {categoryEmoji[event.category]} {cat?.name}
          </span>
          {event.regions.map(r => {
            const region = regions.find(reg => reg.id === r)
            return (
              <span key={r} style={{
                fontSize: 11, padding: '3px 10px', borderRadius: 14,
                background: region?.color || 'var(--bg-secondary)', color: '#fff',
              }}>
                {region?.name || r}
              </span>
            )
          })}
          <span style={{
            fontSize: 11, padding: '3px 10px', borderRadius: 14,
            background: event.significance === 'high' ? '#FEF3C7' : '#F3F4F6',
            color: event.significance === 'high' ? '#92400E' : '#6B7280',
          }}>
            {event.significance === 'high' ? '★ Sangat Penting' : '○ Penting'}
          </span>
          <span style={{ fontSize: 11, padding: '3px 10px', borderRadius: 14, border: '1px solid var(--border)', color: 'var(--text-secondary)' }}>
            {event.year}{event.year_end ? `–${event.year_end}` : ''} M
          </span>
        </div>

        <h1 className="font-heading text-2xl md:text-3xl font-bold mb-3 leading-tight">
          {event.title}
        </h1>

        {/* Tokoh */}
        {event.figures.length > 0 && (
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 16, alignItems: 'center' }}>
            <span style={{ fontSize: 12, color: 'var(--text-secondary)' }}>Tokoh:</span>
            {event.figures.map(f => (
              <span key={f} style={{
                fontSize: 12, padding: '2px 10px', borderRadius: 12,
                background: 'var(--bg-secondary)', color: 'var(--text-secondary)',
              }}>{f}</span>
            ))}
          </div>
        )}

        {/* Mode toggle */}
        <div style={{ marginBottom: 20 }}>
          <button
            onClick={() => setStoryMode(!storyMode)}
            className="text-sm px-4 py-2 rounded-full border transition-all"
            style={{
              background: storyMode ? '#FEF3C7' : 'transparent',
              borderColor: storyMode ? '#FCD34D' : 'var(--border)',
              color: storyMode ? '#92400E' : 'var(--text-secondary)',
            }}
          >
            {storyMode ? '🌙 Mode Anak-Anak Aktif' : '🌙 Mode Anak-Anak'}
          </button>
        </div>

        {/* Fullscreen slideshow modal */}
        <AnimatePresence>
          {storyMode && hasRichContent && content['children-id'] && (
            <ChildrenSlideshow content={content['children-id']} contentDir={contentDir} onClose={() => setStoryMode(false)} />
          )}
        </AnimatePresence>

        {storyMode && !(hasRichContent && content['children-id']) ? (
          <motion.div key="story" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <div style={{
              background: '#FEF3C7', borderRadius: 16, padding: 24,
              border: '1px solid #FCD34D', textAlign: 'center',
            }}>
              <p style={{ fontSize: 48, marginBottom: 12 }}>📖</p>
              <p style={{ fontStyle: 'italic', color: '#92400E' }}>
                Konten dongeng sedang disiapkan...
              </p>
            </div>
          </motion.div>
        ) : !storyMode ? (
          <motion.div key="general" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
            className="max-w-none">
            {hasRichContent && content['general-id'] ? (
              <>
                <div dangerouslySetInnerHTML={{ __html: renderMarkdown(content['general-id']) }} />
              </>
            ) : (
              <>
                <section className="mb-8">
                  <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>{event.desc}</p>
                </section>

                <section className="mb-8">
                  <h2 className="font-heading text-xl font-semibold mb-3">📚 Daftar Pustaka</h2>
                  <ol style={{ listStyle: 'none', padding: 0 }}>
                    {event.sumber.map((s, i) => (
                      <li key={i} id={`ref-${i + 1}`} style={{
                        fontSize: 13, color: 'var(--text-secondary)', marginBottom: 8,
                        paddingLeft: 24, position: 'relative', lineHeight: 1.6,
                      }}>
                        <span style={{ position: 'absolute', left: 0, fontWeight: 700, color: 'var(--text-primary)' }}>{i + 1}.</span>
                        {s}
                      </li>
                    ))}
                  </ol>
                </section>
              </>
            )}
          </motion.div>
        ) : null}

        <div className="mt-12 pt-6 border-t border-[var(--border)] flex justify-between">
          {(() => {
            const sorted = [...events].sort((a, b) => a.year - b.year)
            const idx = sorted.findIndex(e => e.id === event.id)
            const prev = idx > 0 ? sorted[idx - 1] : null
            const next = idx < sorted.length - 1 ? sorted[idx + 1] : null
            return (
              <>
                {prev ? (
                  <a href={`/event/${slugify(prev.title)}/`} className="text-sm text-[var(--text-secondary)] hover:underline">
                    ← {prev.title.slice(0, 40)}...
                  </a>
                ) : <span />}
                {next ? (
                  <a href={`/event/${slugify(next.title)}/`} className="text-sm text-[var(--text-secondary)] hover:underline text-right">
                    {next.title.slice(0, 40)}... →
                  </a>
                ) : <span />}
              </>
            )
          })()}
        </div>
      </article>
    </main>
  )
}

export default function EventContent({ event }: { event: Event }) {
  return (
    <I18nProvider>
      <EventContentInner event={event} />
    </I18nProvider>
  )
}
