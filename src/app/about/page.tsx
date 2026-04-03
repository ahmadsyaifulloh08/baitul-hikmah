// See: docs/PRD.md Section 3.4 (Halaman Tentang)
// PRD#3.4: About page — project vision, methodology overview, content statistics
'use client'

import Header from '@/components/Header'
import { I18nProvider } from '@/i18n/context'

export default function AboutPage() {
  return (
    <I18nProvider>
    <main className="min-h-screen bg-[var(--bg-primary)]">
      <Header />
      <article className="max-w-3xl mx-auto px-4 pt-6 pb-12">

        <section className="mb-4">
          <h2 className="text-xl font-semibold text-[var(--text-primary)] mb-3">Tentang Baitul Hikmah</h2>
          <div className="text-[var(--text-secondary)] leading-relaxed" style={{display:"flex",flexDirection:"column",gap:"1rem"}}>
            <p>
              <strong>Baitul Hikmah</strong> adalah portal digital interaktif untuk menelusuri sejarah peradaban Islam —
              dari Tahun Gajah (570 M) hingga jatuhnya Al-Andalus (1492 M). Terinspirasi dari <em>Baitul Hikmah</em> (Rumah Kebijaksanaan)
              yang didirikan di Baghdad pada abad ke-8 M, project ini bertujuan melanjutkan tradisi keilmuan Islam di era digital.
            </p>
            <p>
              Dengan lebih dari <strong>128 peristiwa</strong> yang mencakup 7 era peradaban Islam, Baitul Hikmah menyajikan
              konten dalam dua mode: <strong>Mode Umum</strong> (akademis, dengan sitasi lengkap) dan <strong>Mode Anak-Anak</strong> (dongeng
              interaktif dengan ilustrasi watercolor).
            </p>
            <p>
              Tersedia dalam Bahasa Indonesia dan Bahasa Inggris, dilengkapi peta interaktif, timeline kronologis,
              dan ilustrasi original untuk setiap peristiwa.
            </p>

          </div>
        </section>

        <section className="mb-4">
          <h2 className="text-xl font-semibold text-[var(--text-primary)] mb-3">Metode Verifikasi Konten</h2>
          <div className="text-[var(--text-secondary)] leading-relaxed" style={{display:"flex",flexDirection:"column",gap:"1rem"}}>
            <p>
              Seluruh konten Baitul Hikmah diverifikasi menggunakan metodologi ketat yang mengacu pada
              tradisi ilmiah Islam (<em>manhaj</em>) dan standar akademis modern.
            </p>

            <div className="bg-[var(--bg-secondary)] rounded-lg" style={{padding:"0.5rem"}}>
              <h3 className="font-semibold text-[var(--text-primary)] mb-3">1. Sumber Primer</h3>
              <p className="mb-2">Setiap peristiwa dirujuk minimal dari 3 sumber primer yang otoritatif:</p>
              <ul className="list-disc pl-5 space-y-1">
                <li><em>Al-Sirah al-Nabawiyyah</em> — Ibn Hisham</li>
                <li><em>Tarikh al-Rusul wa al-Muluk</em> — Al-Tabari</li>
                <li><em>Al-Bidayah wa al-Nihayah</em> — Ibn Kathir</li>
                <li><em>Tabaqat al-Kubra</em> — Ibn Sa&apos;d</li>
                <li><em>Al-Rahiq al-Makhtum</em> — Al-Mubarakfuri</li>
              </ul>
            </div>

            <div className="bg-[var(--bg-secondary)] rounded-lg" style={{padding:"0.5rem"}}>
              <h3 className="font-semibold text-[var(--text-primary)] mb-3">2. Verifikasi Hadits</h3>
              <p className="mb-2">Hadits yang dikutip diverifikasi statusnya (shahih, hasan, dha&apos;if) dengan merujuk pada:</p>
              <ul className="list-disc pl-5 space-y-1">
                <li><em>Shahih al-Bukhari</em> dan <em>Shahih Muslim</em> — standar tertinggi</li>
                <li><em>Sunan</em> Abu Dawud, Al-Tirmidzi, Al-Nasa&apos;i, Ibn Majah</li>
                <li>Penilaian ulama hadits kontemporer jika diperlukan</li>
              </ul>
            </div>

            <div className="bg-[var(--bg-secondary)] rounded-lg" style={{padding:"0.5rem"}}>
              <h3 className="font-semibold text-[var(--text-primary)] mb-3">3. Kutipan Ayat Suci Al-Quran</h3>
              <p className="mb-2">
                Ayat Al-Quran yang dikutip dalam setiap artikel dipilih berdasarkan <strong>hierarki relevansi historis</strong>:
              </p>
              <ul className="list-disc pl-5 space-y-1">
                <li><strong>Tingkatan 1 — Asbabun Nuzul:</strong> Ayat yang turun berkaitan langsung dengan peristiwa, atau secara historis tercatat digunakan oleh tokoh dalam peristiwa tersebut. <em>Contoh: QS. Al-Fil (105): 1-5 pada artikel Tahun Gajah — surah yang turun mengabadikan peristiwa penghancuran pasukan Abrahah oleh burung ababil.</em></li>
                <li><strong>Tingkatan 2 — Korelasi Hikmah Kuat:</strong> Ayat yang hikmahnya langsung relevan dengan inti peristiwa. Bermanfaat untuk menjelaskan hikmah Al-Quran, termasuk kepada anak-anak. <em>Contoh: QS. Al-Hijr (15): 9 tentang janji pemeliharaan Al-Quran pada artikel Pengumpulan Mushaf.</em></li>
                <li><strong>Tingkatan 3 — Dihindari:</strong> Ayat yang dipaksakan ke peristiwa yang tidak relevan tidak digunakan. Artikel yang tidak memiliki ayat Tingkatan 1 atau Tingkatan 2 yang relevan tidak memaksakan kutipan ayat dengan korelasi yang lemah.</li>
              </ul>
              <p className="mt-3 mb-2">Setiap kutipan Al-Quran juga memenuhi standar teknis:</p>
              <ul className="list-disc pl-5 space-y-1">
                <li>Teks Arab asli wajib disertakan beserta terjemahan</li>
                <li>Pemisah ayat (<em>verse separator</em>) digunakan secara konsisten</li>
                <li>Setiap ayat yang dikutip disertai penjelasan korelasi historis/hikmahnya</li>
                <li>Satu ayat spesifik tidak digunakan di lebih dari 3 artikel berbeda</li>
              </ul>
              <p className="mt-3 text-sm" style={{color:"var(--text-secondary)"}}>
                Dari 128 peristiwa, <strong>97 artikel</strong> memuat kutipan ayat Al-Quran (Tingkatan 1/2), 
                sementara <strong>31 artikel</strong> tidak memuat kutipan ayat karena tidak ditemukan korelasi historis yang memadai.
              </p>
            </div>

            <div className="bg-[var(--bg-secondary)] rounded-lg" style={{padding:"0.5rem"}}>
              <h3 className="font-semibold text-[var(--text-primary)] mb-3">4. Daftar Pustaka Terkonsolidasi</h3>
              <p className="mb-2">Setiap artikel menggunakan format daftar pustaka terkonsolidasi:</p>
              <ul className="list-disc pl-5 space-y-1">
                <li>Satu entry = satu karya unik (tidak ada duplikasi)</li>
                <li>Nomor sitasi konsisten — sumber yang sama selalu menggunakan nomor yang sama</li>
                <li>Detail bab/halaman disebutkan <em>inline</em> dalam teks, bukan di daftar pustaka</li>
                <li>Automated citation checker memverifikasi konsistensi format</li>
              </ul>
            </div>

            <div className="bg-[var(--bg-secondary)] rounded-lg" style={{padding:"0.5rem"}}>
              <h3 className="font-semibold text-[var(--text-primary)] mb-3">5. Sistem Validasi Artikel</h3>
              <p className="mb-2">Seluruh konten melewati sistem validasi artikel sebelum dipublikasikan:</p>
              <ul className="list-disc pl-5 space-y-1">
                <li><strong>Citation Checker</strong> — memverifikasi format sitasi terkonsolidasi</li>
                <li><strong>Quran Format Checker</strong> — memastikan teks Arab ada di setiap referensi</li>
                <li><strong>Metadata Checker</strong> — memverifikasi kelengkapan data setiap peristiwa</li>
                <li><strong>Image Checker</strong> — memastikan ilustrasi sesuai spesifikasi</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="mb-4">
          <h2 className="text-xl font-semibold text-[var(--text-primary)] mb-3">Ilustrasi</h2>
          <div className="text-[var(--text-secondary)] leading-relaxed" style={{display:"flex",flexDirection:"column",gap:"1rem"}}>
            <p>
              Ilustrasi untuk mode anak-anak dibuat menggunakan AI generative art (Gemini) dengan panduan ketat:
            </p>
            <ul className="list-disc pl-5 space-y-1">
              <li>Style: warm watercolor storybook, konsisten di seluruh peristiwa</li>
              <li>Kepatuhan Islamic: Nabi Muhammad ﷺ direpresentasikan sebagai <em>cahaya emas</em> (golden glow) — tidak ada penggambaran fisik dalam bentuk apapun</li>
              <li>Character consistency melalui <em>illustration registry</em> — deskripsi karakter yang sama digunakan di setiap prompt</li>

            </ul>
          </div>
        </section>

        <section className="border-t border-[var(--border)] pt-8 text-center">
          <p className="text-lg mb-2" dir="rtl" lang="ar">
            رَبِّ زِدْنِي عِلْمًا
          </p>
          <p className="text-sm text-[var(--text-secondary)] italic">&quot;Ya Tuhanku, tambahkanlah ilmu kepadaku.&quot;</p>
          <p className="text-xs text-[var(--text-secondary)] mt-1">(QS. Taha: 114)</p>
        </section>

      </article>
    </main>
    </I18nProvider>
  )
}
