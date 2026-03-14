'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { getEra, getCategory, slugify, events, type Event } from '@/lib/data'
import Header from '@/components/Header'
import eventContentData from '@/data/event-content.json'
import eventContentMap from '@/data/event-content-map.json'

const categoryEmoji: Record<string, string> = {
  prophetic: '☆', political: '♛', knowledge: '≡',
  military: '⚔', heritage: '◆', decline: '↓',
}

// Simple markdown to HTML (headers, bold, italic, lists, paragraphs)
function renderMarkdown(md: string) {
  const lines = md.split('\n')
  let html = ''
  let inList = false

  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) { 
      if (inList) { html += '</ul>'; inList = false }
      continue 
    }
    if (trimmed.startsWith('# ')) {
      html += `<h1 class="font-heading text-2xl font-bold mt-8 mb-4">${trimmed.slice(2)}</h1>`
    } else if (trimmed.startsWith('## ')) {
      html += `<h2 class="font-heading text-xl font-semibold mt-6 mb-3">${trimmed.slice(3)}</h2>`
    } else if (trimmed.startsWith('### ')) {
      html += `<h3 class="font-heading text-lg font-semibold mt-4 mb-2">${trimmed.slice(4)}</h3>`
    } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      if (!inList) { html += '<ul class="list-disc list-inside space-y-1 mb-4">'; inList = true }
      html += `<li class="text-sm text-[var(--text-secondary)]">${formatInline(trimmed.slice(2))}</li>`
    } else if (/^\d+\./.test(trimmed)) {
      if (!inList) { html += '<ol class="list-decimal list-inside space-y-1 mb-4">'; inList = true }
      html += `<li class="text-sm text-[var(--text-secondary)]">${formatInline(trimmed.replace(/^\d+\.\s*/, ''))}</li>`
    } else {
      if (inList) { html += '</ul>'; inList = false }
      html += `<p class="text-[var(--text-secondary)] leading-relaxed mb-4">${formatInline(trimmed)}</p>`
    }
  }
  if (inList) html += '</ul>'
  return html
}

function formatInline(text: string) {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code class="text-sm bg-[var(--bg-secondary)] px-1 rounded">$1</code>')
}

export default function EventContent({ event }: { event: Event }) {
  const [storyMode, setStoryMode] = useState(false)
  const era = getEra(event.era)
  const cat = getCategory(event.category)
  
  // Load rich content if available
  const slug = slugify(event.title)
  const contentDir = (eventContentMap as Record<string, string>)[slug]
  const content = contentDir ? (eventContentData as any)[contentDir] : null
  const hasRichContent = !!content

  return (
    <main className="min-h-screen">
      <Header />
      <article className="max-w-3xl mx-auto px-4 py-8">
        <a href="/" className="text-xs text-[var(--text-secondary)] hover:underline mb-6 inline-block">
          ← Kembali ke Timeline
        </a>

        <div className="flex items-center gap-2 mb-3 flex-wrap">
          <span className="text-xs font-mono px-2.5 py-1 rounded-full"
            style={{ background: era?.color + '20', color: era?.color }}>
            {era?.name}
          </span>
          <span className="text-xs px-2 py-1 rounded-full border border-[var(--border)]"
            style={{ color: cat?.color }}>
            {categoryEmoji[event.category]} {cat?.name}
          </span>
          <span className="text-xs font-mono text-[var(--text-secondary)]">
            {event.year}{event.year_end ? `–${event.year_end}` : ''} M
          </span>
        </div>

        <motion.h1
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="font-heading text-2xl md:text-3xl font-bold mb-4 leading-tight"
        >
          {event.title}
        </motion.h1>

        <div className="mb-6">
          <button
            onClick={() => setStoryMode(!storyMode)}
            className={`text-sm px-4 py-2 rounded-full border transition-all ${
              storyMode
                ? 'bg-amber-100 dark:bg-amber-900/30 border-amber-300 dark:border-amber-700 text-amber-800 dark:text-amber-300'
                : 'border-[var(--border)] text-[var(--text-secondary)] hover:bg-[var(--bg-secondary)]'
            }`}
          >
            {storyMode ? '🌙 Mode Dongeng Aktif' : '🌙 Mode Dongeng'}
          </button>
        </div>

        {storyMode ? (
          <motion.div key="story" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
            className="bg-amber-50 dark:bg-amber-900/10 rounded-2xl p-6 border border-amber-200 dark:border-amber-800 max-w-none">
            {hasRichContent && content['children-id'] ? (
              <div dangerouslySetInnerHTML={{ __html: renderMarkdown(content['children-id']) }} />
            ) : (
              <>
                <p className="text-lg italic font-heading mb-4">
                  ✨ Hai nak, malam ini kita akan bercerita tentang...
                </p>
                <h3>🧑 Siapa tokohnya?</h3>
                <p>{event.figures.join(', ') || 'Tokoh-tokoh dalam peristiwa ini'}</p>
                <h3>📖 Ceritanya...</h3>
                <p>{event.desc}</p>
                <p className="italic text-[var(--text-secondary)] mt-4">[Konten dongeng sedang disiapkan oleh Researcher]</p>
              </>
            )}
          </motion.div>
        ) : (
          <motion.div key="adult" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
            className="max-w-none">
            {hasRichContent && content['adult-id'] ? (
              <div dangerouslySetInnerHTML={{ __html: renderMarkdown(content['adult-id']) }} />
            ) : (
              <section className="mb-8">
                <h2 className="font-heading text-xl font-semibold mb-3">Narasi</h2>
                <p className="text-[var(--text-secondary)] leading-relaxed">{event.desc}</p>
              </section>
            )}

            {event.figures.length > 0 && (
              <section className="mb-8">
                <h2 className="font-heading text-xl font-semibold mb-3">Tokoh</h2>
                <div className="flex flex-wrap gap-2">
                  {event.figures.map(f => (
                    <span key={f} className="px-3 py-1.5 rounded-lg bg-[var(--bg-secondary)] text-sm">{f}</span>
                  ))}
                </div>
              </section>
            )}

            <section className="mb-8">
              <h2 className="font-heading text-xl font-semibold mb-3">Signifikansi</h2>
              <span className={`px-3 py-1 rounded-full text-sm ${
                event.significance === 'high'
                  ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400'
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'
              }`}>
                {event.significance === 'high' ? '★ Sangat Penting' : '○ Penting'}
              </span>
            </section>

            <section className="mb-8">
              <h2 className="font-heading text-xl font-semibold mb-3">Wilayah</h2>
              <div className="flex gap-2">
                {event.regions.map(r => (
                  <span key={r} className="text-sm px-3 py-1 rounded-lg border border-[var(--border)]">{r}</span>
                ))}
              </div>
            </section>

            <section className="mb-8">
              <h2 className="font-heading text-xl font-semibold mb-3">📚 Daftar Pustaka</h2>
              <ol className="list-decimal list-inside space-y-1">
                {event.sumber.map((s, i) => (
                  <li key={i} className="text-sm text-[var(--text-secondary)]">{s}</li>
                ))}
              </ol>
            </section>
          </motion.div>
        )}

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
