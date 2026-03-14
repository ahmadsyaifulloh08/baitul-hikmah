'use client'

import { useState } from 'react'
import dynamic from 'next/dynamic'
import Header from '@/components/Header'
import Timeline from '@/components/Timeline'

const MapView = dynamic(() => import('@/components/MapView'), { ssr: false })

export default function Home() {
  const [mode, setMode] = useState<'timeline' | 'map'>('timeline')
  const [search, setSearch] = useState('')

  return (
    <main className="min-h-screen">
      <Header />
      {/* Hero section */}
      <div style={{ textAlign: 'center', padding: '40px 16px 0' }}>
        <h2 className="font-heading" style={{
          fontSize: 'clamp(1.8rem, 4vw, 2.8rem)', fontWeight: 800,
          marginBottom: 8, lineHeight: 1.2,
        }}>
          <img src="/baitul-hikmah.svg" alt="Baitul Hikmah" width={48} height={48} style={{ display: 'inline-block', verticalAlign: 'middle', marginRight: 8 }} />
          Baitul Hikmah
        </h2>
        <p style={{
          fontSize: 'clamp(0.85rem, 2vw, 1.1rem)', color: 'var(--text-secondary)',
          marginBottom: 24, maxWidth: 600, margin: '0 auto 24px',
        }}>
          The Golden Age and Beyond — Menelusuri Jejak Peradaban Islam
        </p>

        {/* Search bar - always on top */}
        <div style={{ maxWidth: 640, margin: '0 auto 16px' }}>
          <input
            type="text"
            placeholder="🔍 Cari peristiwa, tokoh, atau kata kunci..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{
              width: '100%', padding: '14px 20px', borderRadius: 12,
              border: '2px solid var(--border)', background: 'var(--bg-secondary)',
              color: 'var(--text-primary)', fontSize: 16, outline: 'none',
              transition: 'border-color 0.2s',
            }}
            onFocus={e => e.currentTarget.style.borderColor = '#58a6ff'}
            onBlur={e => e.currentTarget.style.borderColor = 'var(--border)'}
          />
        </div>

        {/* Mode Toggle - below search */}
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: 16 }}>
          <div style={{
            display: 'inline-flex', gap: 0, borderRadius: 12,
            background: 'var(--bg-secondary)', border: '1px solid var(--border)', padding: 3,
          }}>
            <button
              onClick={() => setMode('timeline')}
              style={{
                padding: '8px 20px', borderRadius: 10, fontSize: 14, fontWeight: 600,
                border: 'none', cursor: 'pointer', transition: 'all 0.2s',
                background: mode === 'timeline' ? 'var(--bg-primary)' : 'transparent',
                color: mode === 'timeline' ? 'var(--text-primary)' : 'var(--text-secondary)',
                boxShadow: mode === 'timeline' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none',
              }}
            >
              📜 Timeline
            </button>
            <button
              onClick={() => setMode('map')}
              style={{
                padding: '8px 20px', borderRadius: 10, fontSize: 14, fontWeight: 600,
                border: 'none', cursor: 'pointer', transition: 'all 0.2s',
                background: mode === 'map' ? 'var(--bg-primary)' : 'transparent',
                color: mode === 'map' ? 'var(--text-primary)' : 'var(--text-secondary)',
                boxShadow: mode === 'map' ? '0 1px 3px rgba(0,0,0,0.1)' : 'none',
              }}
            >
              🗺️ Peta
            </button>
          </div>
        </div>
      </div>

      {/* Content area */}
      {mode === 'timeline' ? <Timeline search={search} /> : <MapView search={search} />}
      {mode === 'timeline' && (
        <footer className="text-center py-8 text-xs text-[var(--text-secondary)] border-t border-[var(--border)]">
          <p>Baitul Hikmah — Menelusuri Jejak Peradaban Islam</p>
          <p className="mt-1">Manhaj Bukhari · Riset Sahih · Open Source</p>
        </footer>
      )}
    </main>
  )
}
