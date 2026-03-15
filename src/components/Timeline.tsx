'use client'

import { useState, useMemo, useRef } from 'react'
import { events, eras, categories, regions, getEra, getCategory, slugify, type Event } from '@/lib/data'
import { useI18n } from '@/i18n/context'

// ============================================================
// ERA LAYOUT — exact match from dashboard _civEraLayout
// ============================================================
const _civEraLayout = [
  { id: 'pre_islamic', start: 500, end: 610, height: 300 },
  { id: 'prophetic', start: 610, end: 632, height: 600 },
  { id: 'rashidun', start: 632, end: 661, height: 250 },
  { id: 'umayyad', start: 661, end: 750, height: 280 },
  { id: 'golden_age', start: 750, end: 1055, height: 1000 },
  { id: 'fragmentation', start: 1055, end: 1258, height: 600 },
  { id: 'decline', start: 1258, end: 1500, height: 400 },
]

function yearToPixel(year: number): number {
  let offset = 0
  for (const e of _civEraLayout) {
    if (year <= e.end) {
      const pct = Math.max(0, (year - e.start) / (e.end - e.start))
      return offset + pct * e.height
    }
    offset += e.height
  }
  return offset
}

function getTotalHeight(): number {
  return _civEraLayout.reduce((t, e) => t + e.height, 0)
}

const YEAR_COL_W = 50

function regionLeft(regIdx: number, colCount: number): string {
  const frac = (regIdx + 0.5) / colCount
  const pxPart = YEAR_COL_W * (1 - frac)
  const pctPart = frac * 100
  return `calc(${pxPart.toFixed(1)}px + ${pctPart.toFixed(2)}%)`
}

function separatorLeft(colIdx: number, colCount: number): string {
  const frac = (colIdx + 1) / colCount
  const pxPart = YEAR_COL_W * (1 - frac)
  const pctPart = frac * 100
  return `calc(${pxPart.toFixed(1)}px + ${pctPart.toFixed(2)}%)`
}

const markYears = [500, 570, 576, 583, 595, 605, 610, 613, 615, 616, 619, 620, 621, 622, 623, 624, 625, 627, 628, 629, 630, 631, 632, 650, 661, 680, 700, 711, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1258, 1300, 1350, 1400, 1450, 1492]

function getCategoryColor(catId: string): string {
  return categories.find(c => c.id === catId)?.color || '#888'
}

function getCategoryEmoji(catId: string): string {
  return categories.find(c => c.id === catId)?.emoji || ''
}

function getRegionColor(regId: string): string {
  return regions.find(r => r.id === regId)?.color || '#888'
}

function getRegionName(regId: string): string {
  return regions.find(r => r.id === regId)?.name || regId
}

function getEraName(eraId: string): string {
  return eras.find(e => e.id === eraId)?.name || eraId
}

function getEraColor(eraId: string): string {
  return eras.find(e => e.id === eraId)?.color || '#888'
}

// ============================================================
// EVENT DETAIL PANEL
// ============================================================
function EventDetail({ event, onClose, t }: { event: Event; onClose: () => void; t: (key: string) => string }) {
  const yearStr = event.year + (event.year_end ? ' - ' + event.year_end : '') + ' M'
  const catColor = getCategoryColor(event.category)

  return (
    <div style={{
      background: 'var(--surface, #161b22)',
      border: '1px solid var(--border, #30363d)',
      borderRadius: 10,
      padding: 20,
      marginTop: 12,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12, flexWrap: 'wrap' }}>
        <span style={{ fontSize: 24, fontWeight: 700, color: catColor }}>{yearStr}</span>
        <span style={{
          display: 'inline-block', fontSize: 11, padding: '2px 8px', borderRadius: 10,
          fontWeight: 600, background: catColor + '22', color: catColor,
        }}>
          {getCategoryEmoji(event.category)} {getEraName(event.era)}
        </span>
        <button onClick={onClose} style={{
          marginLeft: 'auto', background: 'none', border: 'none', color: 'var(--text2, #8b949e)',
          cursor: 'pointer', fontSize: 18,
        }}>✕</button>
      </div>
      <h3 style={{ fontSize: 16, marginBottom: 8 }}>{event.title}</h3>
      <p style={{ fontSize: 13, color: 'var(--text2, #8b949e)', lineHeight: 1.7, marginBottom: 12 }}>{event.desc}</p>

      {/* Regions */}
      <div style={{ marginBottom: 8 }}>
        {event.regions.map(rid => {
          const rc = getRegionColor(rid)
          return (
            <span key={rid} style={{
              display: 'inline-block', fontSize: 11, padding: '2px 8px', borderRadius: 10,
              fontWeight: 600, margin: 2, background: rc + '22', color: rc,
            }}>
              {getRegionName(rid)}
            </span>
          )
        })}
      </div>

      {/* Figures */}
      {event.figures?.length > 0 && (
        <div style={{ fontSize: 12, color: 'var(--text2, #8b949e)' }}>
          <strong>{t('detail.figures')}</strong> {event.figures.join(', ')}
        </div>
      )}

      {/* Sumber */}
      {event.sumber?.length > 0 && (
        <div style={{
          marginTop: 10, padding: '10px 12px',
          background: 'rgba(210,169,34,0.08)', borderRadius: 6,
        }}>
          <div style={{ fontSize: 11, fontWeight: 600, color: '#d29922', marginBottom: 4 }}>{t('detail.source')}</div>
          <ul style={{ margin: 0, paddingLeft: 16 }}>
            {event.sumber.map((s, i) => (
              <li key={i} style={{ fontSize: 11, color: 'var(--text2, #8b949e)', marginBottom: 2 }}>{s}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Baca Selengkapnya button */}
      <div style={{ marginTop: 16 }}>
        <a
          href={`/event/${slugify(event.title)}/`}
          style={{
            display: 'inline-block', padding: '8px 16px', borderRadius: 8,
            background: 'var(--bg-secondary)', fontSize: 12, fontWeight: 600,
            textDecoration: 'none', transition: 'background 0.2s',
            color: 'var(--text-primary)', cursor: 'pointer',
          }}
          onMouseEnter={e => e.currentTarget.style.background = 'var(--border)'}
          onMouseLeave={e => e.currentTarget.style.background = 'var(--bg-secondary)'}
        >
          {t('detail.readMore')}
        </a>
      </div>
    </div>
  )
}

// ============================================================
// MAIN TIMELINE EXPORT
// ============================================================
interface TimelineProps {
  search?: string
}

export default function Timeline({ search: externalSearch }: TimelineProps) {
  const { t } = useI18n()
  const search = externalSearch || ''
  const [hiddenCategories, setHiddenCategories] = useState<Set<string>>(new Set())
  const [hiddenEras, setHiddenEras] = useState<Set<string>>(new Set())
  const [hiddenRegions, setHiddenRegions] = useState<Set<string>>(new Set())
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null)
  const [openEras, setOpenEras] = useState<Set<string>>(new Set([eras[0]?.id]))
  const detailRef = useRef<HTMLDivElement>(null)

  // bfcache handles state restoration in production (static export)

  const toggleCategory = (catId: string) => {
    setHiddenCategories(prev => {
      const next = new Set(prev)
      if (next.has(catId)) next.delete(catId)
      else next.add(catId)
      return next
    })
  }

  const toggleEra = (eraId: string) => {
    setHiddenEras(prev => {
      const next = new Set(prev)
      if (next.has(eraId)) next.delete(eraId)
      else next.add(eraId)
      return next
    })
  }

  const toggleRegion = (regId: string) => {
    setHiddenRegions(prev => {
      const next = new Set(prev)
      if (next.has(regId)) next.delete(regId)
      else next.add(regId)
      return next
    })
  }

  const isVisible = (ev: Event): boolean => {
    if (hiddenCategories.has(ev.category)) return false
    if (hiddenEras.has(ev.era)) return false
    if (hiddenRegions.size > 0 && ev.regions.every(r => hiddenRegions.has(r))) return false
    if (search && !ev.title.toLowerCase().includes(search.toLowerCase()) &&
        !ev.desc.toLowerCase().includes(search.toLowerCase())) return false
    return true
  }

  const filteredEvents = useMemo(() => {
    return events.filter(ev => isVisible(ev))
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [search, hiddenCategories, hiddenEras, hiddenRegions])

  const handleEventClick = (evId: string) => {
    const ev = events.find(e => e.id === evId)
    if (ev) {
      setSelectedEvent(ev)
      setTimeout(() => detailRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 50)
    }
  }

  const totalH = getTotalHeight()
  const colCount = regions.length
  const gridCols = `${YEAR_COL_W}px repeat(${colCount}, 1fr)`

  return (
    <div>
      {/* Search bar moved to parent (page.tsx) */}

      {/* ==================== FILTER PILLS ==================== */}
      <div style={{ maxWidth: 1400, margin: '0 auto', padding: '12px 12px 0' }}>
        {/* Era pills */}
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 8, alignItems: 'center' }}>
          <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-secondary)', marginRight: 4 }}>{t('filters.era')}</span>
          {eras.map(era => {
            const active = !hiddenEras.has(era.id)
            return (
              <button key={era.id} onClick={() => toggleEra(era.id)} style={{
                fontSize: 11, padding: '3px 10px', borderRadius: 14,
                border: active ? '1px solid transparent' : '1px solid var(--border)',
                background: active ? era.color : 'var(--surface2)',
                color: active ? '#fff' : 'var(--text2)',
                cursor: 'pointer', transition: 'background 0.15s, border-color 0.15s', userSelect: 'none',
              }}>
                {era.name}
              </button>
            )
          })}
        </div>

        {/* Category pills */}
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 8, alignItems: 'center' }}>
          <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-secondary)', marginRight: 4 }}>{t('filters.category')}</span>
          {categories.map(cat => {
            const active = !hiddenCategories.has(cat.id)
            return (
              <button key={cat.id} onClick={() => toggleCategory(cat.id)} style={{
                fontSize: 11, padding: '3px 10px', borderRadius: 14,
                border: active ? '1px solid transparent' : '1px solid var(--border)',
                background: active ? cat.color : 'var(--surface2)',
                color: active ? '#fff' : 'var(--text2)',
                cursor: 'pointer', transition: 'background 0.15s, border-color 0.15s', userSelect: 'none',
              }}>
                {cat.emoji} {cat.name}
              </button>
            )
          })}
        </div>

        {/* Region pills */}
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 12, alignItems: 'center' }}>
          <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-secondary)', marginRight: 4 }}>{t('filters.region')}</span>
          {regions.map(reg => {
            const active = !hiddenRegions.has(reg.id)
            return (
              <button key={reg.id} onClick={() => toggleRegion(reg.id)} style={{
                fontSize: 11, padding: '3px 10px', borderRadius: 14,
                border: active ? '1px solid transparent' : '1px solid var(--border)',
                background: active ? reg.color : 'var(--surface2)',
                color: active ? '#fff' : 'var(--text2)',
                cursor: 'pointer', transition: 'background 0.15s, border-color 0.15s', userSelect: 'none',
              }}>
                {reg.name}
              </button>
            )
          })}
        </div>
      </div>

      <div style={{ maxWidth: 1400, margin: '0 auto', padding: '0 12px' }}>

      {/* ==================== DESKTOP TIMELINE ==================== */}
      <div className="hidden md:block" style={{
        overflowY: 'auto', maxHeight: 'calc(100vh - 280px)', position: 'relative',
        border: '1px solid var(--border, #30363d)', borderRadius: 10,
        background: 'var(--surface, #161b22)',
      }}>
        {/* Sticky header */}
        <div style={{
          display: 'grid', position: 'sticky', top: 0, zIndex: 10,
          background: 'var(--surface2, #21262d)',
          borderBottom: '2px solid var(--border, #30363d)',
          fontSize: 11, fontWeight: 700, textTransform: 'uppercase' as const,
          letterSpacing: '0.3px', gridTemplateColumns: gridCols,
        }}>
          <div style={{
            padding: '10px 4px', textAlign: 'center',
            borderRight: '1px solid var(--border, #30363d)',
            whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', fontSize: 10,
          }}>Tahun</div>
          {regions.map((r, i) => (
            <div key={r.id} style={{
              padding: '10px 4px', textAlign: 'center',
              borderRight: i < regions.length - 1 ? '1px solid var(--border, #30363d)' : 'none',
              whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
              color: r.color,
            }}>{r.name}</div>
          ))}
        </div>

        {/* Body */}
        <div style={{ position: 'relative', minHeight: 100, height: totalH }}>
          {/* Era bands */}
          {(() => {
            let bandOffset = 0
            return _civEraLayout.map((era, ei) => {
              const top = bandOffset
              bandOffset += era.height
              const eraData = eras.find(e => e.id === era.id)
              const bgColor = ei % 2 === 0 ? 'transparent' : 'rgba(128,128,128,0.04)'
              return (
                <div key={era.id} style={{
                  position: 'absolute', left: 0, right: 0,
                  top, height: era.height,
                  background: bgColor,
                  borderBottom: '1px solid var(--border, #30363d)',
                  display: 'flex', alignItems: 'flex-start',
                }}>
                  {/* Era label — vertical text, sticky left */}
                  <div style={{
                    position: 'sticky', left: 0, zIndex: 5,
                    background: 'var(--surface2, #21262d)',
                    borderRight: '1px solid var(--border, #30363d)',
                    fontSize: 10, fontWeight: 700,
                    writingMode: 'vertical-lr', textOrientation: 'mixed' as const,
                    padding: '8px 4px', textTransform: 'uppercase' as const,
                    letterSpacing: '0.3px',
                    color: eraData?.color || 'var(--text2, #8b949e)',
                    height: era.height, width: YEAR_COL_W,
                    minHeight: 40, display: 'flex', alignItems: 'center', justifyContent: 'center',
                  }}>
                    {eraData?.name || ''}
                  </div>
                </div>
              )
            })
          })()}

          {/* Year markers */}
          {markYears.map(my => {
            const py = yearToPixel(my)
            return (
              <div key={`ym-${my}`} style={{
                position: 'absolute', left: 0,
                top: py, width: YEAR_COL_W,
                fontSize: 10, color: 'var(--text2, #8b949e)', fontWeight: 600,
                textAlign: 'right', paddingRight: 6,
                borderTop: '1px dashed rgba(128,128,128,0.2)',
                zIndex: 4, pointerEvents: 'none',
              }}>{my}</div>
            )
          })}

          {/* Region column separators */}
          {Array.from({ length: colCount - 1 }, (_, ci) => (
            <div key={`sep-${ci}`} style={{
              position: 'absolute', top: 0, bottom: 0,
              left: separatorLeft(ci, colCount),
              width: 0, borderRight: '1px solid rgba(128,128,128,0.1)',
              pointerEvents: 'none',
            }} />
          ))}

          {/* Event dots */}
          {filteredEvents.map(ev => {
            const evY = yearToPixel(ev.year)
            const catColor = getCategoryColor(ev.category)
            const dotClass = ev.significance === 'high' ? 'high' : ev.significance === 'medium' ? 'medium' : 'low'
            const dotSizePx = dotClass === 'high' ? 16 : dotClass === 'medium' ? 12 : 10
            const isSelected = selectedEvent?.id === ev.id

            return ev.regions.map((regId, rIdx) => {
              const regIdx = regions.findIndex(r => r.id === regId)
              if (regIdx === -1) return null
              const evLeft = regionLeft(regIdx, colCount)

              return (
                <div key={`${ev.id}-${regId}`}>
                  <div
                    onClick={() => handleEventClick(ev.id)}
                    title={`${ev.year}: ${ev.title}`}
                    style={{
                      position: 'absolute', cursor: 'pointer', zIndex: 6,
                      display: 'flex', flexDirection: 'column', alignItems: 'center',
                      top: evY, left: evLeft, transform: 'translate(-50%,-50%)',
                      transition: 'transform 0.15s, opacity 0.2s',
                    }}
                    onMouseEnter={e => (e.currentTarget.style.transform = 'translate(-50%,-50%) scale(1.3)')}
                    onMouseLeave={e => (e.currentTarget.style.transform = 'translate(-50%,-50%)')}
                  >
                    <div style={{
                      width: dotSizePx, height: dotSizePx,
                      borderRadius: '50%', background: catColor,
                      border: '2px solid var(--surface, #161b22)',
                      boxShadow: isSelected
                        ? '0 0 0 3px rgba(88,166,255,0.5), 0 1px 3px rgba(0,0,0,0.3)'
                        : '0 1px 3px rgba(0,0,0,0.3)',
                    }} />
                    {ev.significance === 'high' && rIdx === 0 && (
                      <div style={{
                        fontSize: 9, fontWeight: 600, whiteSpace: 'nowrap',
                        maxWidth: 100, overflow: 'hidden', textOverflow: 'ellipsis',
                        marginTop: 2, textAlign: 'center',
                        color: 'var(--text, #c9d1d9)', pointerEvents: 'none',
                      }}>
                        {ev.title.length > 20 ? ev.title.substring(0, 18) + '..' : ev.title}
                      </div>
                    )}
                  </div>

                  {/* Spanning line for year_end */}
                  {ev.year_end && rIdx === 0 && (() => {
                    const spanTop = evY
                    const spanBot = yearToPixel(ev.year_end)
                    const spanH = spanBot - spanTop
                    if (spanH <= 2) return null
                    return (
                      <div style={{
                        position: 'absolute', width: 4, borderRadius: 2, opacity: 0.5, zIndex: 5,
                        top: spanTop, height: spanH, background: catColor,
                        left: evLeft, transform: 'translateX(-50%)',
                      }} />
                    )
                  })()}
                </div>
              )
            })
          })}
        </div>
      </div>

      {/* ==================== MOBILE TIMELINE ==================== */}
      <div className="block md:hidden">
        {eras.map((era, ei) => {
          const eraEvents = filteredEvents.filter(ev => ev.era === era.id)
          const isOpen = openEras.has(era.id)

          return (
            <div key={era.id} style={{
              marginBottom: 16, background: 'var(--surface, #161b22)',
              border: '1px solid var(--border, #30363d)', borderRadius: 10, overflow: 'hidden',
            }}>
              <div
                onClick={() => setOpenEras(prev => {
                  const next = new Set(prev)
                  if (next.has(era.id)) next.delete(era.id)
                  else next.add(era.id)
                  return next
                })}
                style={{
                  padding: '12px 16px', fontSize: 13, fontWeight: 700, cursor: 'pointer',
                  userSelect: 'none', display: 'flex', alignItems: 'center', gap: 8,
                  borderLeft: `4px solid ${era.color}`,
                }}
              >
                <span>{era.name}</span>
                <span style={{ fontSize: 11, color: 'var(--text2, #8b949e)', marginLeft: 'auto' }}>
                  {era.start}-{era.end} ({eraEvents.length})
                </span>
              </div>
              {isOpen && (
                <div style={{ padding: '0 16px 12px' }}>
                  {eraEvents.map(ev => (
                    <div
                      key={ev.id}
                      onClick={() => handleEventClick(ev.id)}
                      style={{
                        padding: '8px 0', borderBottom: '1px solid var(--border, #30363d)',
                        fontSize: 13, cursor: 'pointer', transition: 'background 0.1s',
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <span style={{ fontSize: 12, fontWeight: 700, color: getCategoryColor(ev.category), minWidth: 40 }}>
                          {ev.year}
                        </span>
                        <span style={{ fontSize: 12 }}>
                          {getCategoryEmoji(ev.category)} {ev.title}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Event detail panel */}
      <div ref={detailRef}>
        {selectedEvent && (
          <EventDetail event={selectedEvent} onClose={() => setSelectedEvent(null)} t={t} />
        )}
      </div>

      {filteredEvents.length === 0 && (
        <div style={{ textAlign: 'center', padding: 40, color: 'var(--text2, #8b949e)' }}>
          {t('detail.notFound')}
        </div>
      )}
      </div>
    </div>
  )
}
