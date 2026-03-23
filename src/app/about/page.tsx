/**
 * About Us page — project description + verification methodology
 *
 * See: docs/content-style-guide.md (methodology basis)
 * See: docs/README.md (project overview)
 */
import Header from '@/components/Header'

export default function AboutPage() {
  return (
    <main className="min-h-screen bg-[var(--bg-primary)]">
      <Header />
      <article className="max-w-2xl mx-auto px-5 py-10">

        <h1 className="text-2xl font-bold text-[var(--text-primary)] mb-1">
          Tentang Baitul Hikmah
        </h1>
        <p className="text-sm text-[var(--text-secondary)] mb-10">
          Portal digital interaktif sejarah peradaban Islam
        </p>

        {/* Tentang Project */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-[var(--text-primary)] mb-4 flex items-center gap-2">
            <span>🕌</span> Tentang Project
          </h2>
          <div className="text-sm text-[var(--text-secondary)] space-y-4 leading-relaxed">
            <p>
              <strong>Baitul Hikmah</strong> adalah portal digital interaktif untuk menelusuri sejarah peradaban Islam —
              dari Tahun Gajah (570 M) hingga jatuhnya Al-Andalus (1492 M). Terinspirasi dari <em>Baitul Hikmah</em> (Rumah Kebijaksanaan)
              yang didirikan di Baghdad pada abad ke-8 M.
            </p>
            <p>
              Dengan lebih dari <strong>128 peristiwa</strong> yang mencakup 7 era peradaban Islam, Baitul Hikmah menyajikan
              konten dalam dua mode: <strong>Mode Umum</strong> (akademis, dengan sitasi lengkap) dan <strong>Mode Anak-Anak</strong> (dongeng
              interaktif dengan ilustrasi watercolor).
            </p>
            <p>
              Tersedia dalam Bahasa Indonesia dan Bahasa Inggris, dilengkapi peta interaktif, timeline kronologis, dan
              ilustrasi original untuk setiap peristiwa.
            </p>
          </div>
        </section>

        {/* Metode Verifikasi */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-[var(--text-primary)] mb-6 flex items-center gap-2">
            <span>📖</span> Metode Verifikasi Konten
          </h2>
          <p className="text-sm text-[var(--text-secondary)] mb-6 leading-relaxed">
            Seluruh konten Baitul Hikmah diverifikasi menggunakan metodologi ketat yang mengacu pada
            tradisi ilmiah Islam (<em>manhaj</em>) dan standar akademis modern.
          </p>

          <div className="space-y-4">
            <div className="border border-[var(--border)] rounded-lg p-5">
              <h3 className="font-semibold text-[var(--text-primary)] text-sm mb-3">1. Sumber Primer</h3>
              <p className="text-sm text-[var(--text-secondary)] mb-3">Setiap peristiwa dirujuk minimal dari 3 sumber primer yang otoritatif:</p>
              <ul className="text-sm text-[var(--text-secondary)] space-y-1 pl-4" style={{listStyle: 'disc'}}>
                <li><em>Al-Sirah al-Nabawiyyah</em> — Ibn Hisham</li>
                <li><em>Tarikh al-Rusul wa al-Muluk</em> — Al-Tabari</li>
                <li><em>Al-Bidayah wa al-Nihayah</em> — Ibn Kathir</li>
                <li><em>Tabaqat al-Kubra</em> — Ibn Sa&apos;d</li>
                <li><em>Al-Rahiq al-Makhtum</em> — Al-Mubarakfuri</li>
              </ul>
            </div>

            <div className="border border-[var(--border)] rounded-lg p-5">
              <h3 className="font-semibold text-[var(--text-primary)] text-sm mb-3">2. Verifikasi Hadits</h3>
              <p className="text-sm text-[var(--text-secondary)] mb-3">Hadits yang dikutip diverifikasi statusnya (shahih, hasan, dha&apos;if) dengan merujuk pada:</p>
              <ul className="text-sm text-[var(--text-secondary)] space-y-1 pl-4" style={{listStyle: 'disc'}}>
                <li><em>Shahih al-Bukhari</em> dan <em>Shahih Muslim</em> — standar tertinggi</li>
                <li><em>Sunan</em> Abu Dawud, Al-Tirmidzi, Al-Nasa&apos;i, Ibn Majah</li>
                <li>Penilaian ulama hadits kontemporer jika diperlukan</li>
              </ul>
            </div>

            <div className="border border-[var(--border)] rounded-lg p-5">
              <h3 className="font-semibold text-[var(--text-primary)] text-sm mb-3">3. Verifikasi Al-Quran</h3>
              <p className="text-sm text-[var(--text-secondary)] mb-3">Setiap kutipan Al-Quran diverifikasi secara otomatis menggunakan API Al-Quran Cloud:</p>
              <ul className="text-sm text-[var(--text-secondary)] space-y-1 pl-4" style={{listStyle: 'disc'}}>
                <li>Teks Arab diambil langsung dari database Mushaf Madinah</li>
                <li>Setiap referensi wajib menyertakan teks Arab asli beserta terjemahan</li>
                <li>Pemisah ayat (<em>verse separator</em>) digunakan secara konsisten</li>
                <li>Automated QA checker memverifikasi keberadaan teks Arab</li>
              </ul>
            </div>

            <div className="border border-[var(--border)] rounded-lg p-5">
              <h3 className="font-semibold text-[var(--text-primary)] text-sm mb-3">4. Daftar Pustaka Terkonsolidasi</h3>
              <p className="text-sm text-[var(--text-secondary)] mb-3">Setiap artikel menggunakan format daftar pustaka terkonsolidasi:</p>
              <ul className="text-sm text-[var(--text-secondary)] space-y-1 pl-4" style={{listStyle: 'disc'}}>
                <li>Satu entry = satu karya unik (tidak ada duplikasi)</li>
                <li>Nomor sitasi konsisten — sumber yang sama selalu menggunakan nomor yang sama</li>
                <li>Automated citation checker memverifikasi konsistensi format</li>
              </ul>
            </div>

            <div className="border border-[var(--border)] rounded-lg p-5">
              <h3 className="font-semibold text-[var(--text-primary)] text-sm mb-3">5. Automated Quality Assurance</h3>
              <p className="text-sm text-[var(--text-secondary)] mb-3">Seluruh konten melewati pipeline QA otomatis sebelum dipublikasikan:</p>
              <ul className="text-sm text-[var(--text-secondary)] space-y-1 pl-4" style={{listStyle: 'disc'}}>
                <li><strong>Citation Checker</strong> — memverifikasi format sitasi terkonsolidasi</li>
                <li><strong>Quran Format Checker</strong> — memastikan teks Arab ada di setiap referensi</li>
                <li><strong>Metadata Checker</strong> — memverifikasi kelengkapan data setiap peristiwa</li>
                <li><strong>Image Checker</strong> — memastikan ilustrasi sesuai spesifikasi</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Ilustrasi */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-[var(--text-primary)] mb-4 flex items-center gap-2">
            <span>🎨</span> Ilustrasi
          </h2>
          <div className="text-sm text-[var(--text-secondary)] space-y-3 leading-relaxed">
            <p>
              Ilustrasi untuk mode anak-anak dibuat menggunakan AI generative art (Gemini) dengan panduan ketat:
            </p>
            <ul className="space-y-1 pl-4" style={{listStyle: 'disc'}}>
              <li>Style: warm watercolor storybook, konsisten di seluruh peristiwa</li>
              <li>Kepatuhan Islamic: Nabi Muhammad ﷺ direpresentasikan sebagai <em>cahaya emas</em> (golden glow) — tidak ada penggambaran fisik dalam bentuk apapun</li>
              <li>Character consistency melalui <em>illustration registry</em> — deskripsi karakter yang sama digunakan di setiap prompt</li>
              <li>QA review oleh manusia sebelum publikasi</li>
            </ul>
          </div>
        </section>

        {/* Tim */}
        <section className="mb-12">
          <h2 className="text-lg font-semibold text-[var(--text-primary)] mb-4 flex items-center gap-2">
            <span>🤝</span> Tim
          </h2>
          <p className="text-sm text-[var(--text-secondary)] leading-relaxed">
            Baitul Hikmah adalah project <strong>AhadByte</strong> — dikembangkan oleh Ahmad Syaifulloh
            dengan bantuan AI agents untuk riset, penulisan, dan ilustrasi. Semua konten melewati
            verifikasi manusia sebelum dipublikasikan.
          </p>
        </section>

        {/* Quote */}
        <section className="border-t border-[var(--border)] pt-8 text-center">
          <p className="text-lg mb-2 text-[var(--text-secondary)]" dir="rtl" lang="ar">
            رَبِّ زِدْنِي عِلْمًا
          </p>
          <p className="text-sm text-[var(--text-secondary)] italic">
            &quot;Ya Tuhanku, tambahkanlah ilmu kepadaku.&quot;
          </p>
          <p className="text-xs text-[var(--text-secondary)] mt-1">
            (QS. Taha: 114)
          </p>
        </section>

      </article>
    </main>
  )
}
