import Header from '@/components/Header'
import Timeline from '@/components/Timeline'

export default function Home() {
  return (
    <main className="min-h-screen">
      <Header />
      <Timeline />
      <footer className="text-center py-8 text-xs text-[var(--text-secondary)] border-t border-[var(--border)]">
        <p>🏛 Baitul Hikmah — Menelusuri Jejak Peradaban Islam</p>
        <p className="mt-1">Manhaj Bukhari · Riset Sahih · Open Source</p>
      </footer>
    </main>
  )
}
