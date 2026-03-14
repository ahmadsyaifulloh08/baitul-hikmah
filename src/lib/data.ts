import researchData from '@/data/research_agenda.json'

export interface Event {
  id: string
  title: string
  year: number
  year_end: number | null
  era: string
  regions: string[]
  category: string
  desc: string
  figures: string[]
  significance: string
  sumber: string[]
}

export interface Era {
  id: string
  name: string
  start: number
  end: number
  color: string
}

export interface Category {
  id: string
  name: string
  emoji: string
  color: string
}

export interface Region {
  id: string
  name: string
  color: string
}

export const events: Event[] = researchData.events as Event[]
export const eras: Era[] = researchData.eras as Era[]
export const categories: Category[] = researchData.categories as Category[]
export const regions: Region[] = researchData.regions as Region[]

export function getEra(id: string): Era | undefined {
  return eras.find(e => e.id === id)
}

export function getCategory(id: string): Category | undefined {
  return categories.find(c => c.id === id)
}

export function slugify(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim()
}

export function getEventBySlug(slug: string): Event | undefined {
  return events.find(e => slugify(e.title) === slug)
}

export function getEventById(id: string): Event | undefined {
  return events.find(e => e.id === id)
}

export const eraColorMap: Record<string, string> = Object.fromEntries(
  eras.map(e => [e.id, e.color])
)

export const categoryColorMap: Record<string, string> = Object.fromEntries(
  categories.map(c => [c.id, c.color])
)
