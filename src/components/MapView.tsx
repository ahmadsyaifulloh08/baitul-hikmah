'use client'

import { useEffect, useRef, useState, useMemo, useCallback } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
// pmtiles removed - using CARTO raster tiles
import { events, eras, categories, regions, slugify, type Era } from '@/lib/data'
import { getMapEvents, eventsToGeoJSON, eraColors, getEraBoundaries, regionCoordinates, type MapEvent } from '@/lib/map-data'

// Inline filter components removed - using same style as Timeline directly in JSX

// ─── Year Slider ─── styled to match filter rows
function YearSlider({ year, onChange }: { year: number; onChange: (y: number) => void }) {
  const minYear = 500
  const maxYear = 1500
  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'center', padding: '4px 12px 8px', maxWidth: 1400, margin: '0 auto' }}>
      <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-secondary)', marginRight: 4, whiteSpace: 'nowrap' }}>Tahun:</span>
      <span style={{ fontSize: 11, color: '#8B6914', fontWeight: 600, fontFamily: 'monospace', minWidth: 48, textAlign: 'right' }}>{year} M</span>
      <input
        type="range"
        min={minYear}
        max={maxYear}
        value={year}
        onChange={e => onChange(Number(e.target.value))}
        style={{ flex: 1, height: 4, cursor: 'pointer', accentColor: '#8B6914' }}
      />
      <span style={{ fontSize: 11, color: 'var(--text-secondary)', fontFamily: 'monospace', minWidth: 40 }}>{maxYear}</span>
    </div>
  )
}

// ─── Popup Card ───
function EventPopup({ event, onClose }: { event: MapEvent; onClose: () => void }) {
  const era = eras.find(e => e.id === event.era)
  return (
    <div className="absolute bottom-20 left-1/2 -translate-x-1/2 w-[90%] max-w-sm z-50 bg-[var(--bg-primary)] border border-[var(--border)] rounded-xl shadow-2xl p-4 animate-fade-in">
      <button onClick={onClose} className="absolute top-2 right-3 text-[var(--text-secondary)] hover:text-[var(--text-primary)] text-lg">×</button>
      <div className="flex items-center gap-2 mb-2">
        <span
          className="inline-block w-2.5 h-2.5 rounded-full"
          style={{ backgroundColor: eraColors[event.era] || '#888' }}
        />
        <span className="text-[10px] uppercase tracking-wider text-[var(--text-secondary)]">
          {era?.name} · {event.year} M
        </span>
      </div>
      <h3 className="font-heading text-base font-bold leading-snug mb-1.5">{event.title}</h3>
      <p className="text-xs text-[var(--text-secondary)] line-clamp-3 mb-3">{event.desc}</p>
      <a
        href={`/event/${slugify(event.title)}/`}
        className="inline-block text-xs px-3 py-1.5 rounded-lg bg-[var(--bg-secondary)] hover:bg-[var(--border)] transition-colors font-medium"
      >
        Baca Selengkapnya →
      </a>
    </div>
  )
}

// ─── Region Labels ───
const regionLabels: { id: string; name: string; coords: [number, number] }[] = [
  { id: 'arabia', name: 'Arabia', coords: [39.8, 21.4] },
  { id: 'levant', name: 'Levant / Sham', coords: [36.3, 33.9] },
  { id: 'persia', name: 'Persia / Iraq', coords: [44.4, 33.3] },
  { id: 'egypt', name: 'Mesir / N. Afrika', coords: [31.2, 30.0] },
  { id: 'andalus', name: 'Al-Andalus', coords: [-3.7, 37.2] },
  { id: 'central_asia', name: 'Asia Tengah', coords: [64.6, 39.7] },
  { id: 'india', name: 'India / SE Asia', coords: [78.0, 20.0] },
  { id: 'nusantara', name: 'Nusantara', coords: [110.4, -6.9] },
  { id: 'china', name: 'China', coords: [104.1, 35.9] },
]

// ─── Main Map Component ───
// Region center coordinates for map panning
const regionCenters: Record<string, { center: [number, number]; zoom: number }> = {
  arabia: { center: [42, 24], zoom: 5 },
  levant: { center: [36, 33], zoom: 5.5 },
  persia: { center: [52, 32], zoom: 5 },
  egypt: { center: [30, 28], zoom: 5 },
  andalus: { center: [-3, 38], zoom: 5.5 },
  central_asia: { center: [65, 40], zoom: 4.5 },
  india: { center: [78, 20], zoom: 4.5 },
  nusantara: { center: [115, -2], zoom: 4.5 },
  china: { center: [105, 35], zoom: 4.5 },
}

// Filters now inline in JSX (same style as Timeline)

interface MapViewProps {
  search?: string
}

export default function MapView({ search }: MapViewProps = {}) {
  const mapContainer = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const [hiddenEras, setHiddenEras] = useState<Set<string>>(new Set())
  const [hiddenCategories, setHiddenCategories] = useState<Set<string>>(new Set())
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null)

  const toggleEra = (id: string) => {
    setHiddenEras(prev => { const s = new Set(prev); s.has(id) ? s.delete(id) : s.add(id); return s })
  }
  const toggleCategory = (id: string) => {
    setHiddenCategories(prev => { const s = new Set(prev); s.has(id) ? s.delete(id) : s.add(id); return s })
  }
  const [sliderYear, setSliderYear] = useState(750)
  const [selectedEvent, setSelectedEvent] = useState<MapEvent | null>(null)
  const [mapReady, setMapReady] = useState(false)
  const [isDark, setIsDark] = useState(true)

  // Watch for dark mode changes
  useEffect(() => {
    const check = () => setIsDark(document.documentElement.classList.contains('dark'))
    check()
    const observer = new MutationObserver(check)
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })
    return () => observer.disconnect()
  }, [])

  // Update map tiles when dark mode changes
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapReady) return
    const tileUrl = isDark
      ? 'https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png'
      : 'https://basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png'
    const src = map.getSource('carto') as any
    if (src) {
      src.setTiles([tileUrl])
    }
  }, [isDark, mapReady])

  const allMapEvents = useMemo(() => getMapEvents(), [])

  const filteredEvents = useMemo(() => {
    let filtered = allMapEvents
    if (hiddenEras.size > 0) {
      filtered = filtered.filter(e => !hiddenEras.has(e.era))
    }
    if (hiddenCategories.size > 0) {
      filtered = filtered.filter(e => !hiddenCategories.has(e.category))
    }
    if (selectedRegion) {
      filtered = filtered.filter(e => e.regions?.includes(selectedRegion))
    }
    if (search) {
      const q = search.toLowerCase()
      filtered = filtered.filter(e => e.title.toLowerCase().includes(q) || e.desc?.toLowerCase().includes(q))
    }
    filtered = filtered.filter(e => e.year <= sliderYear)
    return filtered
  }, [allMapEvents, hiddenEras, hiddenCategories, selectedRegion, search, sliderYear])

  // Pan map when region selected
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapReady || !selectedRegion) return
    const target = regionCenters[selectedRegion]
    if (target) {
      map.flyTo({ center: target.center, zoom: target.zoom, duration: 1000 })
    }
  }, [selectedRegion, mapReady])

  // Multi-select: no auto-adjust needed

  // Init map
  useEffect(() => {
    if (!mapContainer.current) return

    // Detect theme for appropriate basemap
    const isDark = document.documentElement.classList.contains('dark')
    const tileUrl = isDark
      ? 'https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png'
      : 'https://basemaps.cartocdn.com/light_all/{z}/{x}/{y}@2x.png'

    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          'carto': {
            type: 'raster',
            tiles: [tileUrl],
            tileSize: 256,
            attribution: '© <a href="https://carto.com">CARTO</a> © <a href="https://openstreetmap.org">OpenStreetMap</a>',
          }
        },
        layers: [
          {
            id: 'carto-basemap',
            type: 'raster',
            source: 'carto',
            minzoom: 0,
            maxzoom: 19,
          },
        ],
        glyphs: 'https://cdn.protomaps.com/fonts/pbf/{fontstack}/{range}.pbf',
      },
      center: [42, 28],
      zoom: 3,
      minZoom: 2,
      maxZoom: 10,
    })

    map.addControl(new maplibregl.NavigationControl(), 'top-right')

    map.on('load', () => {
      // Add events source
      map.addSource('events', {
        type: 'geojson',
        data: eventsToGeoJSON(allMapEvents),
      })

      // Event markers - circles
      map.addLayer({
        id: 'event-circles',
        type: 'circle',
        source: 'events',
        paint: {
          'circle-radius': [
            'match', ['get', 'significance'],
            'high', 7,
            'medium', 5,
            3,
          ],
          'circle-color': [
            'match', ['get', 'era'],
            'pre_islamic', '#8b949e',
            'prophetic', '#3fb950',
            'rashidun', '#58a6ff',
            'umayyad', '#d29922',
            'golden_age', '#bc8cff',
            'fragmentation', '#f778ba',
            'decline', '#da3633',
            '#888',
          ],
          'circle-stroke-width': 1.5,
          'circle-stroke-color': '#0d1117',
          'circle-opacity': 0.85,
        },
      })

      // Glow effect for high significance
      map.addLayer({
        id: 'event-glow',
        type: 'circle',
        source: 'events',
        filter: ['==', ['get', 'significance'], 'high'],
        paint: {
          'circle-radius': 14,
          'circle-color': [
            'match', ['get', 'era'],
            'pre_islamic', '#8b949e',
            'prophetic', '#3fb950',
            'rashidun', '#58a6ff',
            'umayyad', '#d29922',
            'golden_age', '#bc8cff',
            'fragmentation', '#f778ba',
            'decline', '#da3633',
            '#888',
          ],
          'circle-opacity': 0.15,
          'circle-blur': 1,
        },
      }, 'event-circles')

      // Region labels source
      map.addSource('region-labels', {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features: regionLabels.map(r => ({
            type: 'Feature' as const,
            geometry: { type: 'Point' as const, coordinates: r.coords },
            properties: { name: r.name, id: r.id },
          })),
        },
      })

      map.addLayer({
        id: 'region-labels-text',
        type: 'symbol',
        source: 'region-labels',
        layout: {
          'text-field': ['get', 'name'],
          'text-size': 11,
          'text-font': ['Noto Sans Regular'],
          'text-transform': 'uppercase',
          'text-letter-spacing': 0.1,
        },
        paint: {
          'text-color': '#4a6a8a',
          'text-halo-color': '#0d1117',
          'text-halo-width': 1.5,
          'text-opacity': 0.7,
        },
      })

      // Add era boundary polygons
      const boundaries = getEraBoundaries()
      Object.entries(boundaries).forEach(([eraId, geojson]) => {
        map.addSource(`era-${eraId}`, { type: 'geojson', data: geojson })
        map.addLayer({
          id: `era-${eraId}-fill`,
          type: 'fill',
          source: `era-${eraId}`,
          paint: {
            'fill-color': geojson.features[0]?.properties?.color || '#888',
            'fill-opacity': 0,
          },
        }, 'event-glow')
        map.addLayer({
          id: `era-${eraId}-line`,
          type: 'line',
          source: `era-${eraId}`,
          paint: {
            'line-color': geojson.features[0]?.properties?.color || '#888',
            'line-width': 1.5,
            'line-opacity': 0,
            'line-dasharray': [3, 2],
          },
        }, 'event-glow')
      })

      // Click handler
      map.on('click', 'event-circles', (e) => {
        if (e.features?.[0]) {
          const props = e.features[0].properties
          const me = allMapEvents.find(ev => ev.id === props?.id)
          if (me) setSelectedEvent(me)
        }
      })

      map.on('mouseenter', 'event-circles', () => {
        map.getCanvas().style.cursor = 'pointer'
      })
      map.on('mouseleave', 'event-circles', () => {
        map.getCanvas().style.cursor = ''
      })

      setMapReady(true)
    })

    mapRef.current = map
    return () => {
      map.remove()
    }
  }, [])

  // Update filtered markers
  useEffect(() => {
    const map = mapRef.current
    if (!map || !mapReady) return

    const src = map.getSource('events') as maplibregl.GeoJSONSource
    if (src) {
      src.setData(eventsToGeoJSON(filteredEvents))
    }

    // Show/hide era boundaries - show visible eras
    const boundaries = getEraBoundaries()
    Object.keys(boundaries).forEach(eraId => {
      const show = !hiddenEras.has(eraId) && hiddenEras.size > 0
      try {
        map.setPaintProperty(`era-${eraId}-fill`, 'fill-opacity', show ? 0.08 : 0)
        map.setPaintProperty(`era-${eraId}-line`, 'line-opacity', show ? 0.5 : 0)
      } catch {}
    })
  }, [filteredEvents, hiddenEras, mapReady])

  return (
    <div>
      {/* Filter controls */}
      <div className="border-b border-[var(--border)]" style={{ background: 'var(--bg-primary)' }}>
        <div style={{ maxWidth: 1400, margin: '0 auto', padding: '12px 12px 0' }}>
          {/* Era pills - multi-select like Timeline */}
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 8, alignItems: 'center' }}>
            <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-secondary)', marginRight: 4 }}>Era:</span>
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

          {/* Category pills - multi-select like Timeline */}
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 8, alignItems: 'center' }}>
            <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-secondary)', marginRight: 4 }}>Kategori:</span>
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

          {/* Region pills - same as Timeline + map panning */}
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 12, alignItems: 'center' }}>
            <span style={{ fontSize: 11, fontWeight: 600, color: 'var(--text-secondary)', marginRight: 4 }}>Wilayah:</span>
            {regions.map(reg => {
              const active = selectedRegion === reg.id
              return (
                <button key={reg.id} onClick={() => {
                  const newId = active ? null : reg.id
                  setSelectedRegion(newId)
                  if (!newId && mapRef.current) {
                    mapRef.current.flyTo({ center: [42, 28], zoom: 3, duration: 1000 })
                  }
                }} style={{
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
        <YearSlider year={sliderYear} onChange={setSliderYear} />
      </div>

      {/* Map container */}
      <div className="relative" style={{ height: 'calc(100vh - 280px)', minHeight: 400 }}>
        <div ref={mapContainer} style={{ width: '100%', height: '100%' }} />

        {/* Event count badge */}
        <div className="absolute top-2 right-12 z-10 bg-[var(--bg-primary)]/80 backdrop-blur-sm rounded-lg px-2.5 py-1 text-xs text-[var(--text-secondary)] border border-[var(--border)]">
          {filteredEvents.length} peristiwa
        </div>

        {/* Event popup */}
        {selectedEvent && (
          <EventPopup event={selectedEvent} onClose={() => setSelectedEvent(null)} />
        )}

        {/* Legend */}
        <div className="absolute bottom-4 left-4 z-10 bg-[var(--bg-primary)]/90 backdrop-blur-sm rounded-lg p-3 border border-[var(--border)] max-w-[200px]">
          <p className="text-[10px] uppercase tracking-wider text-[var(--text-secondary)] mb-2 font-medium">Era</p>
          <div className="space-y-1">
            {eras.map(era => (
              <div key={era.id} className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: era.color }} />
                <span className="text-[10px] text-[var(--text-secondary)] truncate">{era.name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
