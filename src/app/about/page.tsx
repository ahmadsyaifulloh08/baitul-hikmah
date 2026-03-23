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
          <div className="text-[var(--text-secondary)] space-y-4 leading-relaxed">
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
          <div className="text-[var(--text-secondary)] space-y-4 leading-relaxed">
            <p>
              Seluruh konten Baitul Hikmah diverifikasi menggunakan metodologi ketat yang mengacu pada
              tradisi ilmiah Islam (<em>manhaj</em>) dan standar akademis modern.
            </p>

            <div className="bg-[var(--bg-secondary)] rounded-lg" style={{marginTop:"1.5rem",padding:"2rem"}}>
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

            <div className="bg-[var(--bg-secondary)] rounded-lg" style={{marginTop:"1rem",padding:"2rem"}}>
              <h3 className="font-semibold text-[var(--text-primary)] mb-3">2. Verifikasi Hadits</h3>
              <p className="mb-2">Hadits yang dikutip diverifikasi statusnya (shahih, hasan, dha&apos;if) dengan merujuk pada:</p>
              <ul className="list-disc pl-5 space-y-1">
                <li><em>Shahih al-Bukhari</em> dan <em>Shahih Muslim</em> — standar tertinggi</li>
                <li><em>Sunan</em> Abu Dawud, Al-Tirmidzi, Al-Nasa&apos;i, Ibn Majah</li>
                <li>Penilaian ulama hadits kontemporer jika diperlukan</li>
              </ul>
            </div>

            <div className="bg-[var(--bg-secondary)] rounded-lg" style={{marginTop:"1rem",padding:"2rem"}}>
              <h3 className="font-semibold text-[var(--text-primary)] mb-3">3. Verifikasi Al-Quran</h3>
              <p className="mb-2">Setiap kutipan Al-Quran diverifikasi secara otomatis menggunakan API Al-Quran Cloud:</p>
              <ul className="list-disc pl-5 space-y-1">
                <li>Teks Arab diambil langsung dari database Mushaf Madinah</li>
                <li>Setiap referensi wajib menyertakan teks Arab asli beserta terjemahan</li>
                <li>Pemisah ayat (<em>verse separator</em>) digunakan secara konsisten</li>
                <li>Automated QA checker memverifikasi keberadaan teks Arab</li>
              </ul>
            </div>

            <div className="bg-[var(--bg-secondary)] rounded-lg" style={{marginTop:"1rem",padding:"2rem"}}>
              <h3 className="font-semibold text-[var(--text-primary)] mb-3">4. Daftar Pustaka Terkonsolidasi</h3>
              <p className="mb-2">Setiap artikel menggunakan format daftar pustaka terkonsolidasi:</p>
              <ul className="list-disc pl-5 space-y-1">
                <li>Satu entry = satu karya unik (tidak ada duplikasi)</li>
                <li>Nomor sitasi konsisten — sumber yang sama selalu menggunakan nomor yang sama</li>
                <li>Detail bab/halaman disebutkan <em>inline</em> dalam teks, bukan di daftar pustaka</li>
                <li>Automated citation checker memverifikasi konsistensi format</li>
              </ul>
            </div>

            <div className="bg-[var(--bg-secondary)] rounded-lg" style={{marginTop:"1rem",padding:"2rem"}}>
              <h3 className="font-semibold text-[var(--text-primary)] mb-3">5. Automated Quality Assurance</h3>
              <p className="mb-2">Seluruh konten melewati pipeline QA otomatis sebelum dipublikasikan:</p>
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
          <div className="text-[var(--text-secondary)] space-y-4 leading-relaxed">
            <p>
              Ilustrasi untuk mode anak-anak dibuat menggunakan AI generative art (Gemini) dengan panduan ketat:
            </p>
            <ul className="list-disc pl-5 space-y-1">
              <li>Style: warm watercolor storybook, konsisten di seluruh peristiwa</li>
              <li>Kepatuhan Islamic: Nabi Muhammad ﷺ direpresentasikan sebagai <em>cahaya emas</em> (golden glow) — tidak ada penggambaran fisik dalam bentuk apapun</li>
              <li>Character consistency melalui <em>illustration registry</em> — deskripsi karakter yang sama digunakan di setiap prompt</li>
              <li>QA review oleh manusia sebelum publikasi</li>
            </ul>
          </div>
        </section>

        <section className="mb-4">
          <h2 className="text-xl font-semibold text-[var(--text-primary)] mb-3">Tim</h2>
          <div className="text-[var(--text-secondary)] space-y-4 leading-relaxed">
            <p>
              Baitul Hikmah adalah project <strong>AhadByte</strong> — dikembangkan oleh Ahmad Syaifulloh
              dengan bantuan AI agents untuk riset, penulisan, dan ilustrasi. Semua konten melewati
              verifikasi manusia sebelum dipublikasikan.
            </p>
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
