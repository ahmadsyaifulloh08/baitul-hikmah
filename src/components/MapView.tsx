'use client'

import { useEffect, useRef, useState, useMemo, useCallback } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { Protocol } from 'pmtiles'
import { events, eras, regions, slugify, type Era } from '@/lib/data'
import { getMapEvents, eventsToGeoJSON, eraColors, getEraBoundaries, regionCoordinates, type MapEvent } from '@/lib/map-data'

// ─── Era Filter Bar ───
function EraFilter({ selectedEra, onSelect }: { selectedEra: string | null; onSelect: (id: string | null) => void }) {
  return (
    <div className="flex flex-wrap gap-1.5 p-2">
      <button
        onClick={() => onSelect(null)}
        className={`px-2.5 py-1 rounded-full text-xs font-medium transition-all ${
          !selectedEra
            ? 'bg-[var(--text-primary)] text-[var(--bg-primary)]'
            : 'bg-[var(--bg-secondary)] text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
        }`}
      >
        Semua Era
      </button>
      {eras.map(era => (
        <button
          key={era.id}
          onClick={() => onSelect(era.id === selectedEra ? null : era.id)}
          className={`px-2.5 py-1 rounded-full text-xs font-medium transition-all ${
            era.id === selectedEra
              ? 'text-white'
              : 'bg-[var(--bg-secondary)] text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
          }`}
          style={era.id === selectedEra ? { backgroundColor: era.color } : undefined}
        >
          {era.name}
        </button>
      ))}
    </div>
  )
}

// ─── Year Slider ───
function YearSlider({ year, onChange }: { year: number; onChange: (y: number) => void }) {
  const minYear = 500
  const maxYear = 1500
  return (
    <div className="px-3 py-2 flex items-center gap-3">
      <span className="text-xs text-[var(--text-secondary)] w-12 text-right font-mono">{year} M</span>
      <input
        type="range"
        min={minYear}
        max={maxYear}
        value={year}
        onChange={e => onChange(Number(e.target.value))}
        className="flex-1 h-1.5 accent-[var(--text-primary)] cursor-pointer"
      />
      <span className="text-xs text-[var(--text-secondary)] w-8 font-mono">{maxYear}</span>
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
export default function MapView() {
  const mapContainer = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const [selectedEra, setSelectedEra] = useState<string | null>(null)
  const [sliderYear, setSliderYear] = useState(750)
  const [selectedEvent, setSelectedEvent] = useState<MapEvent | null>(null)
  const [mapReady, setMapReady] = useState(false)

  const allMapEvents = useMemo(() => getMapEvents(), [])

  const filteredEvents = useMemo(() => {
    let filtered = allMapEvents
    if (selectedEra) {
      filtered = filtered.filter(e => e.era === selectedEra)
    }
    // Show events up to slider year
    filtered = filtered.filter(e => e.year <= sliderYear)
    return filtered
  }, [allMapEvents, selectedEra, sliderYear])

  // Init map
  useEffect(() => {
    if (!mapContainer.current) return

    // Register PMTiles protocol
    const protocol = new Protocol()
    maplibregl.addProtocol('pmtiles', protocol.tile)

    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          'protomaps': {
            type: 'vector',
            url: 'pmtiles://https://build.protomaps.com/20230408.pmtiles',
            attribution: '© <a href="https://protomaps.com">Protomaps</a> © <a href="https://openstreetmap.org">OpenStreetMap</a>',
          }
        },
        layers: [
          // Water
          {
            id: 'water',
            type: 'fill',
            source: 'protomaps',
            'source-layer': 'water',
            paint: { 'fill-color': '#1a2332' },
          },
          // Land
          {
            id: 'land',
            type: 'fill',
            source: 'protomaps',
            'source-layer': 'land',
            paint: { 'fill-color': '#1e2a3a' },
          },
          // Boundaries
          {
            id: 'boundaries',
            type: 'line',
            source: 'protomaps',
            'source-layer': 'boundaries',
            paint: {
              'line-color': '#2d3f52',
              'line-width': 0.5,
            },
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
      maplibregl.removeProtocol('pmtiles')
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

    // Show/hide era boundaries
    const boundaries = getEraBoundaries()
    Object.keys(boundaries).forEach(eraId => {
      const show = selectedEra === eraId
      try {
        map.setPaintProperty(`era-${eraId}-fill`, 'fill-opacity', show ? 0.08 : 0)
        map.setPaintProperty(`era-${eraId}-line`, 'line-opacity', show ? 0.5 : 0)
      } catch {}
    })
  }, [filteredEvents, selectedEra, mapReady])

  return (
    <div className="relative w-full" style={{ height: 'calc(100vh - 52px)' }}>
      {/* Map */}
      <div ref={mapContainer} className="absolute inset-0" />

      {/* Controls overlay */}
      <div className="absolute top-0 left-0 right-0 z-10 bg-[var(--bg-primary)]/90 backdrop-blur-md border-b border-[var(--border)]">
        <EraFilter selectedEra={selectedEra} onSelect={setSelectedEra} />
        <YearSlider year={sliderYear} onChange={setSliderYear} />
      </div>

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
  )
}
