'use client'

import { useState, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { events, eras, categories, regions, getEra, getCategory, slugify, type Event } from '@/lib/data'

const categoryEmoji: Record<string, string> = {
  prophetic: '☆', political: '♛', knowledge: '≡',
  military: '⚔', heritage: '◆', decline: '↓',
}

function EventCard({ event, index }: { event: Event; index: number }) {
  const era = getEra(event.era)
  const cat = getCategory(event.category)
  const slug = slugify(event.title)

  return (
    <motion.a
      href={`/event/${slug}/`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.3, delay: Math.min(index * 0.03, 0.5) }}
      className="block group"
    >
      <div className="relative border border-[var(--border)] rounded-xl p-4 hover:border-opacity-60 transition-all hover:shadow-lg bg-[var(--bg-primary)]"
        style={{ borderLeftWidth: 4, borderLeftColor: era?.color || '#888' }}>
        {/* Year badge */}
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-full"
            style={{ background: era?.color + '20', color: era?.color }}>
            {event.year}{event.year_end ? ` – ${event.year_end}` : ''} M
          </span>
          <span className="text-xs px-1.5 py-0.5 rounded" style={{ color: cat?.color }}>
            {categoryEmoji[event.category] || '•'} {cat?.name}
          </span>
        </div>

        {/* Title */}
        <h3 className="font-heading font-semibold text-sm leading-snug mb-1.5 group-hover:text-[var(--text-primary)] transition-colors">
          {event.title}
        </h3>

        {/* Description */}
        <p className="text-xs text-[var(--text-secondary)] line-clamp-2 mb-2">
          {event.desc}
        </p>

        {/* Footer */}
        <div className="flex items-center gap-2 flex-wrap">
          {event.significance === 'high' && (
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400">
              ★ Penting
            </span>
          )}
          {event.figures.slice(0, 2).map(f => (
            <span key={f} className="text-[10px] px-1.5 py-0.5 rounded-full bg-[var(--bg-secondary)] text-[var(--text-secondary)]">
              {f}
            </span>
          ))}
          {event.figures.length > 2 && (
            <span className="text-[10px] text-[var(--text-secondary)]">+{event.figures.length - 2}</span>
          )}
        </div>
      </div>
    </motion.a>
  )
}

export default function Timeline() {
  const [search, setSearch] = useState('')
  const [selectedEra, setSelectedEra] = useState<string | null>(null)
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null)

  const filtered = useMemo(() => {
    let result = [...events].sort((a, b) => a.year - b.year)

    if (search) {
      const q = search.toLowerCase()
      result = result.filter(e =>
        e.title.toLowerCase().includes(q) ||
        e.desc.toLowerCase().includes(q) ||
        e.figures.some(f => f.toLowerCase().includes(q)) ||
        e.year.toString().includes(q)
      )
    }
    if (selectedEra) result = result.filter(e => e.era === selectedEra)
    if (selectedCategory) result = result.filter(e => e.category === selectedCategory)
    if (selectedRegion) result = result.filter(e => e.regions.includes(selectedRegion))

    return result
  }, [search, selectedEra, selectedCategory, selectedRegion])

  const activeEra = selectedEra ? eras.find(e => e.id === selectedEra) : null

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      {/* Hero */}
      <div className="text-center mb-8 islamic-pattern py-10 rounded-2xl">
        <h2 className="font-heading text-3xl md:text-4xl font-bold mb-2">
          Menelusuri Jejak Peradaban Islam
        </h2>
        <p className="text-[var(--text-secondary)] text-sm md:text-base max-w-xl mx-auto">
          Dari Gua Hira hingga Baitul Hikmah — 128 peristiwa penting, 7 era, 1000 tahun peradaban
        </p>
      </div>

      {/* Search */}
      <div className="relative mb-4">
        <input
          type="text"
          placeholder="🔍 Cari peristiwa, tokoh, atau tahun..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="w-full px-4 py-3 rounded-xl border border-[var(--border)] bg-[var(--bg-secondary)] text-sm focus:outline-none focus:ring-2 focus:ring-era-golden-age/40"
        />
      </div>

      {/* Era Filter - Scrubber */}
      <div className="mb-3">
        <div className="flex gap-1.5 overflow-x-auto timeline-scroll pb-2">
          <button
            onClick={() => setSelectedEra(null)}
            className={`shrink-0 text-xs px-3 py-1.5 rounded-full border transition-all ${
              !selectedEra ? 'bg-[var(--text-primary)] text-[var(--bg-primary)] border-transparent' : 'border-[var(--border)] hover:bg-[var(--bg-secondary)]'
            }`}
          >
            Semua Era
          </button>
          {eras.map(era => (
            <button
              key={era.id}
              onClick={() => setSelectedEra(selectedEra === era.id ? null : era.id)}
              className="shrink-0 text-xs px-3 py-1.5 rounded-full border transition-all"
              style={{
                borderColor: selectedEra === era.id ? era.color : 'var(--border)',
                background: selectedEra === era.id ? era.color + '20' : 'transparent',
                color: selectedEra === era.id ? era.color : 'var(--text-secondary)',
              }}
            >
              {era.name} ({era.start}–{era.end})
            </button>
          ))}
        </div>
      </div>

      {/* Category & Region Filters */}
      <div className="flex gap-4 mb-6 flex-wrap">
        <div className="flex gap-1 overflow-x-auto timeline-scroll">
          {categories.map(cat => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(selectedCategory === cat.id ? null : cat.id)}
              className="shrink-0 text-[11px] px-2 py-1 rounded-lg border transition-all"
              style={{
                borderColor: selectedCategory === cat.id ? cat.color : 'var(--border)',
                color: selectedCategory === cat.id ? cat.color : 'var(--text-secondary)',
              }}
            >
              {cat.emoji} {cat.name}
            </button>
          ))}
        </div>
        <div className="flex gap-1 overflow-x-auto timeline-scroll">
          {regions.map(reg => (
            <button
              key={reg.id}
              onClick={() => setSelectedRegion(selectedRegion === reg.id ? null : reg.id)}
              className="shrink-0 text-[11px] px-2 py-1 rounded-lg border transition-all"
              style={{
                borderColor: selectedRegion === reg.id ? reg.color : 'var(--border)',
                color: selectedRegion === reg.id ? reg.color : 'var(--text-secondary)',
              }}
            >
              {reg.name}
            </button>
          ))}
        </div>
      </div>

      {/* Active Era Info */}
      {activeEra && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="mb-4 p-3 rounded-xl border-l-4"
          style={{ borderColor: activeEra.color, background: activeEra.color + '10' }}
        >
          <span className="font-heading font-semibold" style={{ color: activeEra.color }}>
            {activeEra.name}
          </span>
          <span className="text-xs text-[var(--text-secondary)] ml-2">
            {activeEra.start} – {activeEra.end} M · {filtered.length} peristiwa
          </span>
        </motion.div>
      )}

      {/* Results count */}
      <p className="text-xs text-[var(--text-secondary)] mb-4">
        Menampilkan {filtered.length} dari {events.length} peristiwa
      </p>

      {/* Event Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        <AnimatePresence mode="popLayout">
          {filtered.map((event, i) => (
            <EventCard key={event.id} event={event} index={i} />
          ))}
        </AnimatePresence>
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-20 text-[var(--text-secondary)]">
          <p className="text-4xl mb-2">🔍</p>
          <p>Tidak ditemukan peristiwa yang cocok</p>
        </div>
      )}
    </div>
  )
}
