# Marketing Agent Architecture v4.1

## Vizyon

Kullanıcı (marketer) → **tek bir agent'la** (Orchestrator) konuşur.
Orchestrator, bir pazarlama şirketi müdürü gibi davranır:
- Pipeline'ları yönetir
- Sub-agent'lara görev paslar
- Kullanıcıya sadece karar anlarında soru sorar
- Tüm süreci dosyalara kaydeder (hafıza)

Kullanıcı "ne yapacağım" diye düşünmez. Sistem yönlendirir, kullanıcı karar verir.

### Desteklenen İşletme/Ürün Tipleri

Sistem her tür yazılım ürününü ve fiziksel işletmeyi kapsar:

| Tip | Örnekler | Keşif Kaynakları | Özel Strateji |
|-----|----------|-----------------|---------------|
| **Mobil App** | iOS/Android uygulamaları | App Store, Google Play, Product Hunt | ASO, app store yorum analizi, rakip app karşılaştırma |
| **SaaS / Web App** | B2B/B2C yazılım | G2, Capterra, Reddit, HackerNews, Product Hunt | PLG, funnel optimizasyonu, onboarding |
| **Fiziksel İşletme** | Spor salonu, mobilyacı, diş hekimi, psikolog, kuaför, restoran, hukuk bürosu, veteriner | Google Maps, Google Business Profile, yerel forumlar, şikayet siteleri | Lokal SEO, Google Maps optimizasyonu, yerel reklam |
| **E-ticaret** | Online mağaza, dropshipping | Amazon, Trendyol, Hepsiburada, Shopify mağazaları | Ürün sayfası CRO, fiyat karşılaştırma, lojistik |
| **Karma Ürün** | Yazılım + donanım (IoT, POS, medikal cihaz) | İlgili tüm kaynaklar + sektör raporları | Donanım tedarik zinciri, sertifikasyon, bayi ağı |
| **İçerik / Medya** | Blog, podcast, YouTube kanalı, bülten | Spotify, YouTube, Substack, Medium | İçerik takvimi, sponsorluk, abonelik modeli |
| **Hizmet / Ajans** | Dijital ajans, danışmanlık, koçluk | LinkedIn, Clutch, B2B dizinler | Portfolyo, vaka çalışması, inbound marketing |

Sistem, ürün tipine göre otomatik olarak doğru keşif kaynaklarını, doğru skill'leri ve doğru metrikleri seçer. Kullanıcının bunu bilmesi gerekmez.

---

## Agent Hiyerarşisi

```
                         ┌─────────────────────┐
                         │   Marketer Kullanıcı  │
                         └──────────┬──────────┘
                                    │ Sohbet
                         ┌──────────▼──────────┐
                         │    Orchestrator      │
                         │  (Pazarlama Müdürü)  │
                         └──────────┬──────────┘
                                    │ Görev paslar, rapor alır
        ┌────────┬──────┬──────┬────┼────┬──────┬──────┬────────┐
        ▼        ▼      ▼      ▼    │    ▼      ▼      ▼        ▼
   ┌────────┐┌──────┐┌────┐┌────┐  │  ┌────┐┌──────┐┌────┐┌──────────┐
   │ Scout  ││Stratej││Ürün ││Lans │  │  │İçer││Büyüme││Eriş ││Kampanya │
   │Keşifçi ││Analist││Mimar││Komut│  │  │ik  ││Hacker││im   ││Yönetici │
   └────────┘└──────┘└────┘└────┘  │  └────┘└──────┘└────┘└──────────┘
                                    │
                               ┌────▼────┐┌──────┐┌────────┐
                               │Analiz   ││Marka ││Onboard │
                               │Uzmanı   ││Koruy.││Rehber  │
                               └─────────┘└──────┘└────────┘
```

---

## Agent Tanımları

### Orchestrator (Pazarlama Müdürü)
**Dosya:** `marketing-agent/agents/orchestrator.md`
**Kullanıcıya dönük tek agent.** Diğer tüm agent'ları yönetir.

**Sorumlulukları:**
- Pipeline seçimi ve yönetimi
- Sub-agent'lara görev atama
- Sub-agent çıktılarını birleştirip kullanıcıya sunma
- Kullanıcıdan karar isteme (sadece gerektiğinde)
- Proje state'ini dosyalarda tutma
- Session'lar arası hafıza yönetimi

**Kullandığı Skill'ler:** product-marketing (product-context.md için)
**Kullandığı Pipeline'lar:** Tümü
**Konuştuğu Kişiler:** Kullanıcı + tüm sub-agent'lar

---

### 1. Market Scout (Keşifçi)
**Dosya:** `marketing-agent/agents/market-scout.md`
**Görevi:** Pazar fırsatlarını keşfetmek, veri toplamak.

**Skill'ler:**
- webwright (web scraping)
- competitor-profiling (rakip profilleme)
- customer-research (müşteri araştırması)
- market-competitors (rekabet analizi)
- ai-seo (AI motorlarında görünürlük)

**Script'ler:**
- analyze_page.py
- competitor_scanner.py

**Kaynaklar (ürün tipine göre otomatik seçilir):**

| Ürün Tipi | Kaynaklar |
|-----------|----------|
| Mobil App | App Store, Google Play, Product Hunt, SensorTower alternatifleri |
| SaaS / Web App | G2, Capterra, Reddit, HackerNews, Product Hunt, Trustpilot |
| Fiziksel İşletme | Google Maps, Google Business Profile, yerel şikayet portalları (Şikayetvar), yerel forumlar (Ekşi Sözlük, Kadınlar Kulübü), sektörel dizinler |
| E-ticaret | Amazon, Trendyol, Hepsiburada, Shopify mağazaları, ürün yorumları |
| Tümü | Google Trends, Twitter/X, LinkedIn, GitHub, sektör raporları, haber siteleri

**Çıktı Formatı:** `OPPORTUNITY-REPORT.md` (fırsat haritası, kategori analizi, trend raporu)

---

### 2. Strategy Analyst (Stratejist)
**Dosya:** `marketing-agent/agents/strategy-analyst.md`
**Görevi:** Verileri analiz etmek, stratejik içgörü üretmek.

**Skill'ler:**
- market-competitors (rekabet analizi)
- marketing-psychology (davranış psikolojisi)
- pricing (fiyatlandırma stratejisi)
- market-funnel (satış hunisi analizi)
- marketing-ideas (fikir havuzu)
- marketing-plan (AARRR planı)

**Çıktı Formatı:** `STRATEGY-REPORT.md` (SWOT, fırsat analizi, stratejik öneriler)

---

### 3. Product Architect (Ürün Mimarı)
**Dosya:** `marketing-agent/agents/product-architect.md`
**Görevi:** Fikri ürüne dönüştürmek, PRD yazmak.

**Skill'ler:**
- product-marketing (ürün bağlamı)
- pricing (fiyatlandırma)
- paywalls (ödeme duvarı tasarımı)
- aso (app store optimizasyonu)

**Çıktı Formatı:** `PRD.md`, `IDEA-BRIEF.md`, `CODER-BRIEF.md`

---

### 4. Launch Commander (Lansman Komutanı)
**Dosya:** `marketing-agent/agents/launch-commander.md`
**Görevi:** Ürün lansmanını planlamak ve yönetmek.

**Skill'ler:**
- launch (lansman stratejisi)
- aso (uygulama mağazası optimizasyonu)
- seo-audit (teknik SEO denetimi)
- directory-submissions (dizin kayıtları)
- community-marketing (topluluk stratejisi)

**Template'ler:**
- launch-checklist.md
- email-launch.md

**Çıktı Formatı:** `LAUNCH-PLAN.md`, `LAUNCH-CHECKLIST.md`

---

### 5. Content Creator (İçerik Üreticisi)
**Dosya:** `marketing-agent/agents/content-creator.md`
**Görevi:** Tüm içerikleri üretmek.

**Skill'ler:**
- content-strategy (içerik stratejisi)
- copywriting (metin yazarlığı)
- copy-editing (metin düzenleme)
- social (sosyal medya)
- image (görsel üretimi — API henüz yok)
- video (video üretimi — API henüz yok)

**Template'ler:**
- content-calendar.md
- email-welcome.md
- email-nurture.md

**Script'ler:**
- social_calendar.py

**Çıktı Formatı:** `CONTENT-CALENDAR.md`, sosyal medya postları, e-posta dizileri

---

### 6. Growth Hacker (Büyüme Uzmanı)
**Dosya:** `marketing-agent/agents/growth-hacker.md`
**Görevi:** Büyüme deneyleri, retention, viral döngüler.

**Skill'ler:**
- referrals (referans programı)
- churn-prevention (terk önleme)
- community-marketing (topluluk)
- paywalls (ödeme duvarı optimizasyonu)
- marketing-ideas (büyüme fikirleri)

**Çıktı Formatı:** `GROWTH-PLAN.md`, deney raporları

---

### 7. Outreach Specialist (Erişim Uzmanı)
**Dosya:** `marketing-agent/agents/outreach-specialist.md`
**Görevi:** Doğrudan erişim, prospecting, cold outreach.

**Skill'ler:**
- cold-email (soğuk e-posta)
- emails (e-posta dizileri)
- prospecting (müşteri adayı bulma)
- directory-submissions (dizin kayıtları)

**Template'ler:**
- email-nurture.md
- email-welcome.md

**Çıktı Formatı:** `OUTREACH-PLAN.md`, prospect listesi, e-posta şablonları

---

### 8. Analytics Master (Analiz Uzmanı)
**Dosya:** `marketing-agent/agents/analytics-master.md`
**Görevi:** Veri analizi, raporlama, metrik takibi.

**Skill'ler:**
- analytics (analitik kurulumu)
- market-report (pazarlama raporu)
- market-report-pdf (PDF rapor)
- ai-seo (AI görünürlük analizi)

**Script'ler:**
- analyze_page.py
- generate_pdf_report.py

**Çıktı Formatı:** `ANALYTICS-REPORT.md`, `MARKETING-REPORT.pdf`

---

### 9. Brand Guardian (Marka Koruyucusu)
**Dosya:** `marketing-agent/agents/brand-guardian.md`
**Görevi:** Marka stratejisi, ses, konumlandırma.

**Skill'ler:**
- market-brand (marka ses analizi)
- market-proposal (müşteri teklifi)
- ad-creative (reklam kreatifi)

**Çıktı Formatı:** `BRAND-VOICE.md`, `BRAND-STRATEGY.md`

---

### 10. Campaign Manager (Kampanya Yöneticisi)
**Dosya:** `marketing-agent/agents/campaign-manager.md`
**Görevi:** Reklam kampanyaları yönetimi.

**Skill'ler:**
- ads (reklam stratejisi)
- market-ads (reklam üretimi)
- ad-creative (kreatif üretim)

**Çıktı Formatı:** `AD-CAMPAIGNS.md`, A/B test planları

---

### 11. Onboarding Guide (Karşılama Rehberi)
**Dosya:** `marketing-agent/agents/onboarding-guide.md`
**Görevi:** Yeni kullanıcıyı sisteme alıştırmak.

**Sorumlulukları:**
- İlk oturumda sistemin nasıl çalıştığını anlatmak
- Kullanıcının seviyesini ölçmek (başlangıç/orta/ileri)
- product-context.md oluşturmak (product-marketing skill ile)
- İlk pipeline'ı önermek
- Kullanıcı takıldığında `/help` ile devreye girmek

---

## Pipeline Kataloğu

Her pipeline bir dizi aşamadan oluşur. Orchestrator, pipeline'ı adım adım yürütür.

### Pipeline 1: Fikir Keşif ve Doğrulama
**Dosya:** `marketing-agent/pipelines/idea-discovery.md`
**Ne zaman:** Kullanıcı "yeni bir ürün fikri bulmak istiyorum" dediğinde. Sıfırdan fırsat keşfi yapar, PRD'ye kadar götürür.

| Adım | Agent | Eylem | Çıktı |
|------|-------|-------|-------|
| 1.1 | Orchestrator | Kullanıcıya ilgi alanı/sektör/ürün tipi sor | - |
| 1.2 | Market Scout | Ürün tipine uygun kaynakları tara, fırsatları bul | `firsat-haritasi.md` |
| 1.3 | Orchestrator | Fırsatları kullanıcıya sun, kategori seçtir | - |
| 1.4 | Market Scout | Seçilen kategoride derin analiz | `kategori-analizi.md` |
| 1.5 | Strategy Analyst | Rekabet analizi, boşluk tespiti | `strateji-analizi.md` |
| 1.6 | Orchestrator | Boşlukları kullanıcıya sun, fırsat seçtir | - |
| 1.7 | Product Architect | Seçilen fırsattan fikir üret | `idea-brief.md` |
| 1.8 | Orchestrator | Fikri kullanıcıyla tartış, şekillendir | - |
| 1.9 | Product Architect | PRD yaz | `prd-v1.md` |
| 1.10 | Orchestrator | PRD'yi onaylat, coder brief'i hazırla | `coder-brief.md` |

**Not:** Pipeline 1 (sıfırdan keşif) ile Pipeline 5 (eldeki fikirden PRD) arasındaki fark: P1'de Market Scout fırsatları kendisi bulur (adım 1.2-1.6), P5'te kullanıcı fikri verir ve doğrulamayla başlar. Her ikisi de PRD ve coder brief ile sonuçlanır.

---

### Pipeline 2: MVP Lansman
**Dosya:** `marketing-agent/pipelines/mvp-launch.md`
**Ne zaman:** Coder MVP'yi teslim ettiğinde

| Adım | Agent | Eylem | Çıktı |
|------|-------|-------|-------|
| 2.1 | Orchestrator | MVP detaylarını kullanıcıdan al | - |
| 2.2 | Strategy Analyst | MVP'ye özel pazarlama stratejisi | `marketing-strategy.md` |
| 2.3 | Content Creator | Lansman içeriklerini üret | `content-calendar.md`, post'lar |
| 2.4 | Campaign Manager | Reklam kampanyası tasarla | `ad-campaigns.md` |
| 2.5 | Launch Commander | Lansman checklist'i oluştur | `launch-checklist.md` |
| 2.6 | Orchestrator | Tüm planı kullanıcıya sun, onay al | - |
| 2.7 | Launch Commander | Lansmanı başlat | - |

---

### Pipeline 3: Feedback ve İyileştirme
**Dosya:** `marketing-agent/pipelines/feedback-improvement.md`
**Ne zaman:** Lansman sonrası 2-4 hafta geçtiğinde veya kullanıcı istediğinde

| Adım | Agent | Eylem | Çıktı |
|------|-------|-------|-------|
| 3.1 | Orchestrator | Kullanıcıdan temel metrikleri iste | - |
| 3.2 | Market Scout | App store yorumlarını analiz et | `yorum-analizi.md` |
| 3.3 | Analytics Master | Metrik analizi yap | `analytics-raporu.md` |
| 3.4 | Strategy Analyst | İyileştirme alanlarını belirle | `iyilestirme-onerileri.md` |
| 3.5 | Orchestrator | Bulguları kullanıcıya sun, öncelikleri sor | - |
| 3.6 | Product Architect | Güncellenmiş PRD yaz | `prd-v2.md` |
| 3.7 | Orchestrator | Coder için güncellenmiş brief hazırla | `coder-brief-v2.md` |

---

### Pipeline 4: Büyüme Motoru
**Dosya:** `marketing-agent/pipelines/growth-engine.md`
**Ne zaman:** Ürün traction kazandığında

| Adım | Agent | Eylem | Çıktı |
|------|-------|-------|-------|
| 4.1 | Analytics Master | Mevcut metrikleri analiz et | `buyume-analizi.md` |
| 4.2 | Growth Hacker | Büyüme deneyleri tasarla | `buyume-deneyleri.md` |
| 4.3 | Orchestrator | Deneyleri kullanıcıya sun, seçtir | - |
| 4.4 | Growth Hacker | Deneyleri uygula | - |
| 4.5 | Analytics Master | Sonuçları raporla | `deney-sonuclari.md` |
| 4.6 | Orchestrator | Döngü: başarılıysa ölçekle, değilse yeni deney | - |

---

### Pipeline 5: Fikirden PRD'ye (From Idea to PRD)
**Dosya:** `marketing-agent/pipelines/idea-to-prd.md`
**Ne zaman:** Kullanıcının aklında zaten bir fikir varsa. Doğrulama ile başlar, "devam et" kararı çıkarsa tam PRD'ye kadar gider.

| Adım | Agent | Eylem | Çıktı |
|------|-------|-------|-------|
| 5.1 | Orchestrator | Kullanıcıdan fikri al, ürün tipini belirle (app/SaaS/fiziksel işletme/e-ticaret vs.) | - |
| 5.2 | Market Scout | Ürün tipine uygun kaynaklardan pazar büyüklüğü, trend, rakip verisi topla | `pazar-arastirmasi.md` |
| 5.3 | Strategy Analyst | Fikrin SWOT analizi, rekabet avantajı, risk değerlendirmesi, fiyatlandırma ön analizi | `fikir-dogrulama.md` |
| 5.4 | Orchestrator | Sonucu sun: **"devam et"** / **"pivot et (şu yönde değiştir)"** / **"vazgeç (sebep: ...)"** | - |
| —— | **Aşağısı sadece "devam et" kararı verilirse çalışır** | | |
| 5.5 | Product Architect | Fikri detaylandır, hedef kitle persona'ları, değer önerisi, MVP kapsamı | `idea-brief.md` |
| 5.6 | Orchestrator | Fikri kullanıcıyla tartış, eksik/fazla yönleri şekillendir | - |
| 5.7 | Product Architect | Tam PRD yaz (problem, çözüm, persona, MVP kapsamı, kullanıcı akışları, başarı metrikleri, ASO/pazarlama ön bilgileri) | `prd-v1.md` |
| 5.8 | Strategy Analyst | Pazara giriş stratejisi (rakiplere göre konumlanma, ilk hedef segment, fiyat konumlandırma) | `pazara-giris-stratejisi.md` |
| 5.9 | Orchestrator | PRD'yi onaylat, coder brief'i hazırla | `coder-brief.md` |

**Pipeline akış diyagramı:**
```
Kullanıcı fikri → Pazar araştırması → Doğrulama → Karar
                                                      ├── "devam et" → Idea brief → Tartışma → PRD → Coder brief
                                                      ├── "pivot et" → Fikir güncelle → 5.1'e dön
                                                      └── "vazgeç" → Oturum sonu, fikir arşivlenir
```

---

### Pipeline 6: Rakip Saldırı (Competitor Attack)
**Dosya:** `marketing-agent/pipelines/competitor-attack.md`
**Ne zaman:** Belirli bir rakibe karşı strateji gerektiğinde

| Adım | Agent | Eylem | Çıktı |
|------|-------|-------|-------|
| 6.1 | Market Scout | Rakibi derinlemesine tara | `rakip-profili.md` |
| 6.2 | Strategy Analyst | Rakibin zayıf noktalarını bul | `rakip-acik-analizi.md` |
| 6.3 | Content Creator | Rakibe karşı içerik stratejisi | `karsilastirma-icerik.md` |
| 6.4 | Campaign Manager | Rakip anahtar kelimelerine reklam | `rakip-kampanya.md` |
| 6.5 | Growth Hacker | Rakip müşterilerini çekme stratejisi | `musteri-cekme.md` |

---

### Pipeline 7: İçerik Makinesi (Content Machine)
**Dosya:** `marketing-agent/pipelines/content-machine.md`
**Ne zaman:** Düzenli içerik üretimi gerektiğinde

| Adım | Agent | Eylem | Çıktı |
|------|-------|-------|-------|
| 7.1 | Content Creator | 30 günlük içerik takvimi | `content-calendar.md` |
| 7.2 | Content Creator | Platform'a özel post'lar | `posts/` klasörü |
| 7.3 | Analytics Master | İçerik performans takibi | `icerik-performans.md` |
| 7.4 | Content Creator | Performansa göre takvim güncelle | `content-calendar-v2.md` |

---

### Pipeline 8: Outbound Satış
**Dosya:** `marketing-agent/pipelines/outbound-sales.md`
**Ne zaman:** B2B ürün için doğrudan satış gerektiğinde

| Adım | Agent | Eylem | Çıktı |
|------|-------|-------|-------|
| 8.1 | Outreach Specialist | ICP tanımı ve prospect listesi | `prospect-list.csv` |
| 8.2 | Outreach Specialist | E-posta dizisi tasarla | `email-sequence.md` |
| 8.3 | Outreach Specialist | A/B test varyantları | `email-variants.md` |
| 8.4 | Analytics Master | Cevap oranı takibi | `outreach-analiz.md` |

---

### Pipeline 9: Fiziksel İşletme Dijital Varlık (Local Business Launch)
**Dosya:** `marketing-agent/pipelines/local-business-launch.md`
**Ne zaman:** Fiziksel işletme (spor salonu, diş hekimi, mobilyacı, psikolog, restoran vb.) için dijital pazarlama gerektiğinde

| Adım | Agent | Eylem | Çıktı |
|------|-------|-------|-------|
| 9.1 | Orchestrator | İşletme detaylarını al (konum, sektör, hedef kitle, mevcut dijital varlık) | - |
| 9.2 | Market Scout | Google Maps rakip analizi, bölgedeki rakip işletmeleri tara, Google Business Profile'larını karşılaştır | `yerel-pazar-analizi.md` |
| 9.3 | Market Scout | Yerel forum/şikayet sitelerinde rakiplerin müşteri yorumlarını analiz et, memnuniyetsizlikleri/memnuniyetleri tespit et | `yerel-musteri-analizi.md` |
| 9.4 | Strategy Analyst | SWOT + yerel rekabet avantajı + fırsat alanları | `rekabet-stratejisi.md` |
| 9.5 | Content Creator | Google Business Profile optimizasyonu, hizmet/açıklama metinleri, fotoğraf stratejisi | `gbp-optimizasyon.md` |
| 9.6 | Content Creator | Sosyal medya stratejisi (Instagram/TikTok öncelikli, sektöre özel içerik takvimi) | `icerik-takvimi.md`, `sosyal-medya-plan.md` |
| 9.7 | Brand Guardian | Marka sesi, logo/renk önerileri, kurumsal kimlik brief'i | `marka-kimligi.md` |
| 9.8 | Campaign Manager | Lokal reklam stratejisi (Google Local Ads, Instagram/TikTok konum hedefli reklam) | `lokal-reklam-plani.md` |
| 9.9 | Orchestrator | Tüm planı kullanıcıya sun, onay al | - |
| 9.10 | Outreach Specialist | Yerel iş birlikleri, çapraz tanıtım stratejisi (diğer esnaflarla) | `yerel-isbirlikleri.md` |
| 9.11 | Analytics Master | Başarı metrikleri: Google Maps görüntülenme, arama tıklaması, arama sayısı, web sitesi trafiği, randevu/iletişim dönüşümleri | `basari-metrikleri.md` |

**Fiziksel işletme için özel keşif kaynakları:**
- Google Maps (bölgedeki rakip yoğunluğu, puan/yorum analizi)
- Google Business Profile (rakip profillerinin kalitesi)
- Yerel şikayet portalları (Şikayetvar vb.)
- Sektörel forumlar ve Facebook grupları
- Instagram lokasyon etiketi analizi (bölgedeki popüler mekanlar)
- Yerel haber siteleri (bölgede öne çıkan işletmeler)

**Bu pipeline'ın diğer pipeline'larla ilişkisi:**
- Pipeline 9, Pipeline 5'in (Fikirden PRD'ye) fiziksel işletme versiyonu gibi çalışır
- Pipeline 9 tamamlandıktan sonra Pipeline 3 (Feedback ve İyileştirme) ve Pipeline 4 (Büyüme Motoru) fiziksel işletmelere de uyarlanarak çalışır
- Fiziksel işletme için "coder brief" yerine "tasarımcı brief"i veya "web geliştirici brief"i üretilir (web sitesi, randevu sistemi vb.)

---

## Pipeline Zincirleri (End-to-End Akışlar)

Pipeline'lar tek başına değil, zincirler halinde çalışır. Orchestrator bir pipeline bittiğinde otomatik olarak bir sonrakini önerir.

### Zincir A: Sıfırdan Ürüne (En Kapsamlı)
```
P1 (Fikir Keşif) → P5 (Fikirden PRD'ye) → [Coder MVP geliştirir] → P2 (MVP Lansman) → P3 (Feedback) → P4 (Büyüme)
                                                                                                │
                                                                                                └── P3'e dön (döngü)
```

### Zincir B: Eldeki Fikirden Ürüne
```
P5 (Fikirden PRD'ye) → [Coder MVP geliştirir] → P2 (MVP Lansman) → P3 (Feedback) → P5 (PRD güncelle)
       ↑                                                                                    │
       └──────────────────────────────── (döngü) ────────────────────────────────────────────┘
```

### Zincir C: Fiziksel İşletme
```
P9 (Fiziksel İşletme Dijital Varlık) → P7 (İçerik Makinesi — sürekli) → P3 (Feedback) → P9 güncelle
       ↑                                                                              │
       └────────────────────────────── (döngü) ───────────────────────────────────────┘
```

### Zincir D: Mevcut Ürünü Büyütme
```
P4 (Büyüme Motoru) → P6 (Rakip Saldırı — gerekirse) → P8 (Outbound Satış — B2B ise)
```

### Zincir E: Pasif İçerik/Sosyal Medya
```
P7 (İçerik Makinesi) → sürekli döngü (aylık takvim güncelleme)
```

Orchestrator, her pipeline sonunda kullanıcıya otomatik olarak zincirdeki bir sonraki pipeline'ı önerir. Kullanıcı "tamam" derse devam eder, "bekle" derse durur, "başka bir şey" derse seçenek sunulur.

---

## Dosya Yapısı

```
marketing-agent/
├── AGENTS.md                          # Orchestrator agent tanımı (güncellenecek)
├── SKILLS.md                          # Skill manifest (mevcut)
├── ARCHITECTURE.md                    # Bu dosya — mimari dokümanı
├── mcps.json                          # MCP/webwright config (mevcut)
│
├── agents/                            # Sub-agent tanımları
│   ├── orchestrator.md                # Ana orchestrator
│   ├── market-scout.md
│   ├── strategy-analyst.md
│   ├── product-architect.md
│   ├── launch-commander.md
│   ├── content-creator.md
│   ├── growth-hacker.md
│   ├── outreach-specialist.md
│   ├── analytics-master.md
│   ├── brand-guardian.md
│   ├── campaign-manager.md
│   └── onboarding-guide.md
│
├── pipelines/                         # Hazır pipeline akışları
│   ├── idea-discovery.md              # P1: Sıfırdan fikir keşfi
│   ├── idea-to-prd.md                 # P5: Eldeki fikirden PRD'ye (doğrulama dahil)
│   ├── mvp-launch.md                  # P2: MVP lansman
│   ├── feedback-improvement.md        # P3: Feedback → iyileştirme
│   ├── growth-engine.md               # P4: Büyüme motoru
│   ├── competitor-attack.md           # P6: Rakip saldırı
│   ├── content-machine.md             # P7: İçerik makinesi
│   ├── outbound-sales.md              # P8: Outbound satış
│   └── local-business-launch.md       # P9: Fiziksel işletme dijital varlık lansmanı
│
├── skills/                            # 36 skill modülü (mevcut)
├── scripts/                           # Python script'ler (mevcut)
├── templates/                         # Şablonlar (mevcut)
│
└── sessions/                          # Proje bazlı kalıcı depolama (ÇOKLU PROJE)
    │
    ├── _index.md                      # Tüm projelerin listesi ve durum özeti
    │
    ├── skinsync/                      # Örnek Proje A (mobil app)
    │   ├── state.md                   # Proje durumu
    │   ├── product-context.md         # Ürün bağlamı
    │   ├── idea-brief.md
    │   ├── firsat-haritasi.md
    │   ├── kategori-analizi.md
    │   ├── strateji-analizi.md
    │   ├── pazar-arastirmasi.md
    │   ├── prd-v1.md
    │   ├── coder-brief-v1.md
    │   ├── pazara-giris-stratejisi.md
    │   ├── marketing-strategy.md
    │   ├── launch-checklist.md
    │   ├── content-calendar.md
    │   ├── ad-campaigns.md
    │   ├── feedback-analysis.md
    │   ├── prd-v2.md
    │   ├── coder-brief-v2.md
    │   ├── analytics-raporu.md
    │   └── content/
    │       ├── social-post-1.md
    │       └── social-post-2.md
    │
    ├── dis-klinigi-dijital/           # Örnek Proje B (fiziksel işletme)
    │   ├── state.md
    │   ├── product-context.md
    │   ├── yerel-pazar-analizi.md
    │   ├── rakip-klinik-analizi.md
    │   ├── dijital-strateji.md
    │   ├── google-maps-optimizasyon.md
    │   ├── icerik-takvimi.md
    │   └── sosyal-medya-plan.md
    │
    └── proje-c/                        # ... daha fazla proje
        └── state.md
```

### Çoklu Proje Yönetimi

- Her proje kendi `sessions/<proje-adi>/` klasöründe izole çalışır. Projeler birbirine karışmaz.
- `sessions/_index.md` tüm projelerin listesini ve güncel durumlarını tutar:

```markdown
# Aktif Projeler

| Proje | Tip | Aşama | Son Güncelleme |
|-------|-----|-------|---------------|
| skinsync | Mobil App | Pipeline 3, Adım 3.5 (feedback analizi) | 2026-05-31 |
| dis-klinigi-dijital | Fiziksel İşletme | Pipeline 9, Adım 9.2 (Google Maps optimizasyonu) | 2026-05-30 |
| gym-crm | SaaS | Pipeline 5, Adım 5.7 (PRD yazımı) | 2026-05-29 |
```

- Kullanıcı orchestrator'a "X projesine geç" dediğinde orchestrator `sessions/x/state.md`'yi okuyarak kaldığı yerden devam eder.
- Yeni proje başlatırken orchestrator `sessions/_index.md`'e yeni kayıt ekler.
- Aynı anda tek bir proje üzerinde çalışılır (aktif proje). Geçiş yapmak serbesttir.

---

## Agent'lar Arası İletişim Protokolü

Orchestrator, sub-agent'lara görev paslarken şu formatı kullanır:

```
GÖREV: [görev adı]
PIPELINE: [hangi pipeline'ın hangi adımı]
KULLANICI KARARI: [kullanıcının bu aşamada verdiği karar]
GİRDİ DOSYALARI:
  - sessions/proje/xxx.md
BEKLENEN ÇIKTI:
  - sessions/proje/yyy.md
  - Format: [beklenen format]
KISITLAR:
  - [varsa kısıtlar]
```

Sub-agent, işi bitince orchestrator'a şu formatta rapor verir:

```
DURUM: tamamlandı / hata / kullanıcıya soru var
ÇIKTI DOSYALARI:
  - sessions/proje/yyy.md
ÖZET: [3 cümlelik özet]
KULLANICIYA SORU: [varsa soru - sadece orchestrator kullanıcıya sorar]
SONRAKİ ADIM ÖNERİSİ: [varsa]
```

---

## Hafıza ve Session Yönetimi

Her proje `sessions/<proje-adi>/` altında saklanır.
`state.md` dosyası projenin güncel durumunu tutar:

```markdown
# Proje Durumu: SkinSync
- Tip: Mobil App
- Aşama: Lansman sonrası feedback toplama (Pipeline 3, Adım 3.5)
- Son kullanıcı kararı: "PRD'yi güncelle, fotoğraf yükleme ve freemium'a odaklan"
- Aktif Agent'lar: Product Architect
- Son güncelleme: 2026-05-31
- Tamamlanan pipeline'lar: P1 (Fikir Keşif) → P5 (Fikirden PRD'ye) → P2 (MVP Lansman)
```

Orchestrator her oturum başında `state.md`'yi okuyarak kaldığı yerden devam eder.
Kullanıcı "X projesine geç" dediğinde `sessions/x/state.md` okunur, `sessions/_index.md` güncellenir.

---

## Onboarding Akışı

Yeni kullanıcı (marketer) ilk kez sisteme girdiğinde:

1. **Onboarding Guide** devreye girer
2. Kullanıcının deneyim seviyesini sorar (marketing bilgisi var mı?)
3. Kullanıcının ilgilendiği işletme/ürün tipini sorar (mobil app, SaaS, fiziksel işletme, e-ticaret...)
4. `product-marketing` skill ile `sessions/<proje>/product-context.md` oluşturur
5. Kullanıcıya pipeline seçeneklerini sunar:
   - "Sıfırdan bir fikir bulmak istiyorum" → **Pipeline 1** (Fikir Keşif)
   - "Elimde bir fikir var, PRD'ye dönüştürmek istiyorum" → **Pipeline 5** (Fikirden PRD'ye — doğrulama + PRD + coder brief)
   - "MVP'm hazır, pazarlamak istiyorum" → **Pipeline 2** (MVP Lansman)
   - "Ürünüm var, büyütmek istiyorum" → **Pipeline 4** (Büyüme Motoru)
   - "Fiziksel işletmem var, dijital pazarlama yapmak istiyorum" → **Pipeline 9** (Fiziksel İşletme Dijital Varlık)
   - "Belirli bir rakibe karşı strateji istiyorum" → **Pipeline 6** (Rakip Saldırı)
   - "Sadece düzenli içerik/sosyal medya yönetimi istiyorum" → **Pipeline 7** (İçerik Makinesi)
   - "Ne yapacağımı bilmiyorum, bana yol göster" → Onboarding Guide derinlemesine sorularla yönlendirir
6. Seçilen pipeline'ı başlatır, proje için `sessions/<proje-adi>/state.md` oluşturur
7. Kullanıcı her `/help` dediğinde veya sistem kararsızlık tespit ettiğinde Onboarding Guide devreye girer
8. Kullanıcı `sessions/_index.md`'den tüm projelerini ve durumlarını görebilir

---

## Temel Prensipler

1. **Kullanıcı soyutlanır.** Kullanıcı hangi agent'ın çalıştığını, hangi skill'in kullanıldığını bilmek zorunda değil.
2. **Sistem yönlendirir.** Kullanıcı "şimdi ne yapayım" diye düşünmez, orchestrator her zaman bir sonraki adımı söyler.
3. **Karar anları nettir.** Kullanıcı sadece "A mı B mi" tipi sorularda karar verir.
4. **Her şey dosyalanır.** Tüm analizler, kararlar, çıktılar `sessions/` altında kalıcıdır.
5. **Context kaybolmaz.** Orchestrator `state.md` ile oturumlar arası hafızayı korur.
6. **Ölçülebilir çıktı.** Her pipeline adımının somut bir dosya çıktısı vardır.
