import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  safelist: ['mt-10', 'mt-14', 'mt-16', 'mb-10', 'mb-14', 'mb-16', 'pt-10', 'pb-10', 'gap-8', 'gap-10'],
  darkMode: undefined,
  theme: {
    extend: {
      colors: {
        era: {
          'pre-islamic': '#8b949e',
          'prophetic': '#3fb950',
          'rashidun': '#58a6ff',
          'umayyad': '#d29922',
          'golden-age': '#bc8cff',
          'fragmentation': '#f778ba',
          'decline': '#da3633',
        },
        cat: {
          prophetic: '#3fb950',
          political: '#d29922',
          knowledge: '#58a6ff',
          military: '#f85149',
          heritage: '#bc8cff',
          decline: '#da3633',
        },
      },
      fontFamily: {
        heading: ['Playfair Display', 'serif'],
        body: ['Inter', 'sans-serif'],
        arabic: ['Amiri', 'serif'],
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
}
export default config
