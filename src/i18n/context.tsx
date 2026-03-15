'use client'

import { createContext, useContext, useState, useCallback, type ReactNode } from 'react'
import idMessages from './id.json'
import enMessages from './en.json'

type Lang = 'id' | 'en'
type Messages = typeof idMessages

const messages: Record<Lang, Messages> = { id: idMessages, en: enMessages }

interface I18nContextType {
  lang: Lang
  setLang: (lang: Lang) => void
  t: (key: string) => string
}

const I18nContext = createContext<I18nContextType>({
  lang: 'id',
  setLang: () => {},
  t: (key: string) => key,
})

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLang] = useState<Lang>('id')

  const t = useCallback((key: string): string => {
    const parts = key.split('.')
    let result: any = messages[lang]
    for (const part of parts) {
      result = result?.[part]
    }
    return typeof result === 'string' ? result : key
  }, [lang])

  return (
    <I18nContext.Provider value={{ lang, setLang, t }}>
      {children}
    </I18nContext.Provider>
  )
}

export function useI18n() {
  return useContext(I18nContext)
}
