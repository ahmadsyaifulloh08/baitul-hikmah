import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Baitul Hikmah — Menelusuri Jejak Peradaban Islam',
  description: 'Portal digital interaktif sejarah peradaban Islam dari Tahun Gajah (570 M) hingga jatuhnya Al-Andalus (1492 M)',
  manifest: '/manifest.json',
  themeColor: '#0d1117',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id" suppressHydrationWarning>
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
