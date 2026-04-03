// See: docs/PRD.md Section 5 (Design System) + Section 1 (Bahasa)
// PRD#5: Header component — site title, navigation, language toggle (ID/EN)
// PRD#1: Bilingual support — Indonesian primary, English secondary
'use client'

import { useI18n } from '@/i18n/context'

export default function Header() {
  const { lang, setLang, t } = useI18n()

  return (
    <header className="sticky top-0 z-50 bg-[var(--bg-primary)]/80 backdrop-blur-md border-b border-[var(--border)]">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <a href="/" className="flex items-center gap-2">
          <img src="/baitul-hikmah.svg" alt="Baitul Hikmah" width={32} height={32} />
          <div>
            <h1 className="font-heading text-lg font-bold leading-tight">{t('header.title')}</h1>
            <p className="text-[10px] text-[var(--text-secondary)] leading-none">
              {t('header.subtitle')}
            </p>
          </div>
        </a>

        <div className="flex items-center gap-0">
          <button
            onClick={() => setLang('id')}
            className="text-sm px-3 py-1.5 rounded-l-lg border transition-colors"
            style={{
              background: lang === 'id' ? '#8B6914' : 'var(--bg-secondary)',
              color: lang === 'id' ? '#fff' : 'var(--text-secondary)',
              borderColor: lang === 'id' ? '#8B6914' : 'var(--border)',
              fontWeight: lang === 'id' ? 700 : 400,
            }}
          >
            ID
          </button>
          <button
            onClick={() => setLang('en')}
            className="text-sm px-3 py-1.5 rounded-r-lg border transition-colors"
            style={{
              background: lang === 'en' ? '#8B6914' : 'var(--bg-secondary)',
              color: lang === 'en' ? '#fff' : 'var(--text-secondary)',
              borderColor: lang === 'en' ? '#8B6914' : 'var(--border)',
              fontWeight: lang === 'en' ? 700 : 400,
            }}
          >
            EN
          </button>
        </div>
      </div>
    </header>
  )
}
