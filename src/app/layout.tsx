import type { Metadata } from 'next'
// CSS loaded via <link> in <head> to avoid webpack CSS parsing issues in dev mode

export const metadata: Metadata = {
  title: 'Baitul Hikmah — Menelusuri Jejak Peradaban Islam',
  description: 'Portal digital interaktif sejarah peradaban Islam dari Tahun Gajah (570 M) hingga jatuhnya Al-Andalus (1492 M)',
  manifest: '/manifest.json',
  themeColor: '#faf8f5',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id" suppressHydrationWarning>
      <head>
        <link href="/styles.css" rel="stylesheet" />
        <link href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet" />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
