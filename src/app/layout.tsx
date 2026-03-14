import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Baitul Hikmah — Menelusuri Jejak Peradaban Islam',
  description: 'Portal digital interaktif sejarah peradaban Islam dari Tahun Gajah (570 M) hingga jatuhnya Al-Andalus (1492 M)',
  manifest: '/manifest.json',
  themeColor: '#0d1117',
}

const themeScript = `
(function(){
  var t = localStorage.getItem('theme');
  if (t === 'light') {
    document.documentElement.classList.remove('dark');
  } else {
    document.documentElement.classList.add('dark');
  }
})();
`

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id" className="dark" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
}
