'use client'

import { useState, useEffect } from 'react'

export default function Header() {
  const [dark, setDark] = useState(true)

  useEffect(() => {
    // Init from current state (set by inline script in layout)
    const isDark = document.documentElement.classList.contains('dark')
    setDark(isDark)
  }, [])

  const toggleDark = () => {
    const next = !dark
    setDark(next)
    if (next) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }

  return (
    <header className="sticky top-0 z-50 bg-[var(--bg-primary)]/80 backdrop-blur-md border-b border-[var(--border)]">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        <a href="/" className="flex items-center gap-2">
          <span className="text-2xl">🏛</span>
          <div>
            <h1 className="font-heading text-lg font-bold leading-tight">Baitul Hikmah</h1>
            <p className="text-[10px] text-[var(--text-secondary)] leading-none">Jejak Peradaban Islam</p>
          </div>
        </a>

        <div className="flex items-center gap-3">
          <button
            onClick={toggleDark}
            className="p-2 rounded-lg hover:bg-[var(--bg-secondary)] transition-colors"
            aria-label="Toggle dark mode"
          >
            {dark ? '☀️' : '🌙'}
          </button>
          <button className="text-sm px-3 py-1.5 rounded-lg border border-[var(--border)] hover:bg-[var(--bg-secondary)] transition-colors">
            EN
          </button>
        </div>
      </div>
    </header>
  )
}
