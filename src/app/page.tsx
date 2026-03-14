'use client'

import { useState } from 'react'
import dynamic from 'next/dynamic'
import Header from '@/components/Header'
import Timeline from '@/components/Timeline'

const MapView = dynamic(() => import('@/components/MapView'), { ssr: false })

export default function Home() {
  const [mode, setMode] = useState<'timeline' | 'map'>('timeline')

  return (
    <main className="min-h-screen">
      <Header mode={mode} onModeChange={setMode} />
      {mode === 'timeline' ? <Timeline /> : <MapView />}
      {mode === 'timeline' && (
        <footer className="text-center py-8 text-xs text-[var(--text-secondary)] border-t border-[var(--border)]">
          <p>🏛 Baitul Hikmah — Menelusuri Jejak Peradaban Islam</p>
          <p className="mt-1">Manhaj Bukhari · Riset Sahih · Open Source</p>
        </footer>
      )}
    </main>
  )
}
