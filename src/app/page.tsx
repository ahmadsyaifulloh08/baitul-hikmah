'use client'

import { useState } from 'react'
import dynamic from 'next/dynamic'
import { I18nProvider, useI18n } from '@/i18n/context'
import Header from '@/components/Header'
import Timeline from '@/components/Timeline'

const MapView = dynamic(() => import('@/components/MapView'), { ssr: false })

function HomeContent() {
  const [mode, setMode] = useState<'timeline' | 'map'>('timeline')
  const [search, setSearch] = useState('')
  const { t, lang } = useI18n()

  return (
    <main className="min-h-screen">
      <Header />
      {/* Hero section */}
      <div style={{ textAlign: 'center', padding: '24px 16px 0', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4 }}>
        <img src="/baitul-hikmah.svg" alt="Baitul Hikmah" width={100} height={100} />
        <h2 className="font-heading" style={{
          fontSize: 'clamp(1.6rem, 3.5vw, 2.4rem)', fontWeight: 800,
          lineHeight: 1.2, margin: 0,
        }}>
          {t('hero.title')}
        </h2>
        <p style={{
          fontSize: 'clamp(0.8rem, 1.8vw, 1rem)', color: 'var(--text-secondary)',
          maxWidth: 600, margin: '2px 0 0',
        }}>
          {t('hero.subtitle')}
        </p>

        {/* Search bar */}
        <div style={{ maxWidth: 560, width: '100%', marginTop: 14 }}>
          <input
            type="text"
            placeholder={t('search.placeholder')}
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{
              width: '100%', padding: '12px 18px', borderRadius: 12,
              border: '2px solid var(--border)', background: 'var(--bg-secondary)',
              color: 'var(--text-primary)', fontSize: 16, outline: 'none',
              transition: 'border-color 0.2s',
            }}
            onFocus={e => e.currentTarget.style.borderColor = '#8B6914'}
            onBlur={e => e.currentTarget.style.borderColor = 'var(--border)'}
          />
        </div>

        {/* Mode Toggle */}
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: 16 }}>
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
              {t('nav.timeline')}
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
              {t('nav.maps')}
            </button>
          </div>
        </div>
      </div>

      <div style={{ height: 12 }} />

      {/* Content area */}
      {mode === 'timeline' ? <Timeline search={search} /> : <MapView search={search} />}
      {mode === 'timeline' && (
        <footer className="text-center py-8 text-xs text-[var(--text-secondary)] border-t border-[var(--border)]">
          <p>{t('footer.tagline')}</p>
          <p className="mt-2">{t('footer.methodology')}</p>
          <p className="mt-2">
            <a href="/about" className="underline hover:text-[var(--text-primary)] transition-colors">
              {lang === 'id' ? 'Tentang Baitul Hikmah' : 'About Baitul Hikmah'}
            </a>
          </p>
        </footer>
      )}
    </main>
  )
}

export default function Home() {
  return (
    <I18nProvider>
      <HomeContent />
    </I18nProvider>
  )
}
