'use client'

import { useI18n } from '@/i18n/context'

export default function Header() {
  const { lang, setLang, t } = useI18n()

  return (
    <header className="sticky top-0 z-50 bg-[var(--bg-primary)]/80 backdrop-blur-md border-b border-[var(--border)]">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <a href="/" className="flex items-center gap-2 min-w-0">
          <img src="/baitul-hikmah.svg" alt="Baitul Hikmah" width={28} height={28} className="shrink-0" />
          <div className="min-w-0">
            <h1 className="font-heading text-base sm:text-lg font-bold leading-tight truncate">{t('header.title')}</h1>
            <p className="text-[10px] text-[var(--text-secondary)] leading-none hidden sm:block">
              {t('header.subtitle')}
            </p>
          </div>
        </a>

        <div className="flex items-center gap-3 shrink-0">
          <a href="/about" className="text-xs sm:text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">
            {lang === 'id' ? 'Tentang' : 'About'}
          </a>
          <div className="flex items-center gap-0">
            <button
              onClick={() => setLang('id')}
              className="text-xs sm:text-sm px-2 sm:px-3 py-1 sm:py-1.5 rounded-l-lg border transition-colors"
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
              className="text-xs sm:text-sm px-2 sm:px-3 py-1 sm:py-1.5 rounded-r-lg border transition-colors"
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
      </div>
    </header>
  )
}
