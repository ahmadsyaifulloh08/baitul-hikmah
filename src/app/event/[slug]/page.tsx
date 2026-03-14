import { events, slugify } from '@/lib/data'
import EventContent from './EventContent'

export function generateStaticParams() {
  return events.map(event => ({
    slug: slugify(event.title),
  }))
}

export default function EventPage({ params }: { params: { slug: string } }) {
  const event = events.find(e => slugify(e.title) === params.slug)

  if (!event) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-4xl mb-4">📜</p>
          <h2 className="font-heading text-2xl font-bold mb-2">Peristiwa tidak ditemukan</h2>
          <a href="/" className="text-sm underline">← Kembali</a>
        </div>
      </div>
    )
  }

  return <EventContent event={event} />
}
