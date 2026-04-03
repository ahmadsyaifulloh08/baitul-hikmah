// See: docs/PRD.md Section 9 (Data Architecture) + Section 3.2 (Map Mode)
// PRD#9: GeoJSON event data — coordinates from event-coordinates.json
// PRD#3.2: Map event markers, region coordinates, jitter for clustered events
import { events, eras, type Event, type Era } from './data'
import eventCoordinates from '@/data/event-coordinates.json'

// Center coordinates for each region
export const regionCoordinates: Record<string, [number, number]> = {
  arabia:       [39.8, 21.4],    // Makkah/Madinah area
  levant:       [36.3, 33.9],    // Damascus/Jerusalem
  persia:       [44.4, 33.3],    // Baghdad area
  egypt:        [31.2, 30.0],    // Cairo
  andalus:      [-3.7, 37.2],    // Cordoba/Granada
  central_asia: [64.6, 39.7],    // Samarkand/Bukhara
  india:        [78.0, 20.0],    // Central India
  nusantara:    [110.4, -6.9],   // Java
  china:        [104.1, 35.9],   // Central China
}

// Slight offset per event to avoid overlap
function jitter(base: [number, number], index: number): [number, number] {
  const angle = (index * 137.5) * (Math.PI / 180) // golden angle
  const r = 0.5 + (index % 5) * 0.3
  return [
    base[0] + r * Math.cos(angle),
    base[1] + r * Math.sin(angle),
  ]
}

export interface MapEvent {
  id: string
  title: string
  year: number
  yearEnd: number | null
  era: string
  regions: string[]
  category: string
  desc: string
  significance: string
  lng: number
  lat: number
}

export function getMapEvents(): MapEvent[] {
  const coords = (eventCoordinates as any).coordinates || {}
  const regionCounter: Record<string, number> = {}
  
  return events.map(e => {
    // Use researched coordinates if available, fallback to region jitter
    const accurate = coords[e.title]
    let lng: number, lat: number
    if (accurate) {
      lng = accurate[0]
      lat = accurate[1]
    } else {
      const primaryRegion = e.regions[0] || 'arabia'
      const base = regionCoordinates[primaryRegion] || regionCoordinates.arabia
      const idx = regionCounter[primaryRegion] || 0
      regionCounter[primaryRegion] = idx + 1
      ;[lng, lat] = jitter(base, idx)
    }
    
    return {
      id: e.id,
      title: e.title,
      year: e.year,
      yearEnd: e.year_end,
      era: e.era,
      regions: e.regions,
      category: e.category,
      desc: e.desc,
      significance: e.significance,
      lng,
      lat,
    }
  })
}

export function eventsToGeoJSON(mapEvents: MapEvent[]): GeoJSON.FeatureCollection {
  return {
    type: 'FeatureCollection',
    features: mapEvents.map(e => ({
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [e.lng, e.lat],
      },
      properties: {
        id: e.id,
        title: e.title,
        year: e.year,
        yearEnd: e.yearEnd,
        era: e.era,
        category: e.category,
        desc: e.desc,
        significance: e.significance,
        regions: e.regions.join(','),
      },
    })),
  }
}

// Simplified empire boundary polygons for major eras
export function getEraBoundaries(): Record<string, GeoJSON.FeatureCollection> {
  return {
    rashidun: {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: { era: 'rashidun', name: 'Khulafa ar-Rashidin', color: '#58a6ff' },
        geometry: {
          type: 'Polygon',
          coordinates: [[
            [32, 15], [55, 15], [55, 37], [32, 37], [32, 15]
          ]]
        }
      }]
    },
    umayyad: {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: { era: 'umayyad', name: 'Dinasti Umayyah', color: '#d29922' },
        geometry: {
          type: 'Polygon',
          coordinates: [[
            [-10, 30], [-10, 42], [5, 42], [5, 30], // Iberia/Maghreb
            [10, 15], [55, 15], [75, 25], [75, 42], [32, 42], [10, 30], [-10, 30]
          ]]
        }
      }]
    },
    golden_age: {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: { era: 'golden_age', name: 'Abbasiyah', color: '#bc8cff' },
        geometry: {
          type: 'Polygon',
          coordinates: [[
            [25, 15], [80, 15], [80, 42], [25, 42], [25, 15]
          ]]
        }
      }]
    },
  }
}

// Era color lookup
export const eraColors: Record<string, string> = {
  pre_islamic:   '#8b949e',
  prophetic:     '#3fb950',
  rashidun:      '#58a6ff',
  umayyad:       '#d29922',
  golden_age:    '#bc8cff',
  fragmentation: '#f778ba',
  decline:       '#da3633',
}
