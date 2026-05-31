# Pipeline Örneği: App Store Fırsat Keşfi → PRD → MVP → Pazarlama

Bu doküman, marketer kullanıcının orchestrator agent ile etkileşime girerek sıfırdan bir yazılım ürünü fikri bulup pazarlama sürecine kadar nasıl ilerlediğini adım adım gösterir. Her aşamada hangi sub-agent'ın çalıştığı, hangi skill'lerin kullanıldığı, kullanıcıdan ne istendiği ve hangi çıktıların üretildiği belirtilmiştir.

---

## Aşama 1: Pazar Keşfi (Market Discovery)

**Aktif Agent:** Market Scout (Keşifçi)
**Kullanılan Skill'ler:** webwright, customer-research, competitor-profiling
**Script'ler:** competitor_scanner.py, analyze_page.py

### Adım 1.1 — Kaynak Taraması
Market Scout, orchestrator'dan aldığı talimatla aşağıdaki kaynakları tarar:
- Apple App Store (ücretsiz/paralı, son 1 ayda en çok kazanan 50 app)
- Google Play Store (en çok indirilen, en çok gelir getiren)
- Reddit (r/startups, r/SaaS, r/sideproject, r/entrepreneur)
- HackerNews (Show HN, Ask HN)
- Product Hunt (son 30 günde en çok upvote alan ürünler)
- Twitter/X (trending SaaS/product konuşmaları)
- GitHub trending repos

### Adım 1.2 — Kümeleme ve Kategorilendirme
Market Scout topladığı verileri analiz eder:
- Uygulamaları kategorilere ayırır (sağlık, finans, eğitim, kişisel bakım, üretkenlik vb.)
- Her kategorideki büyüme trendini hesaplar
- "Yükselen yıldız" kategorileri belirler (son 6 ayda geliri en çok artan)

### Adım 1.3 — Kullanıcıya İlk Sunum
Orchestrator, Market Scout'un bulgularını kullanıcıya sunar:

```
📊 PAZAR KEŞİF RAPORU

Yükselen kategoriler (son 6 ay gelir artışı):
1. 🥇 Kişisel Bakım / Wellness — %340 artış
2. 🥈 Yapay Zeka Asistanları — %280 artış
3. 🥉 Mikro-SaaS Araçları — %210 artış

Kişisel bakım kategorisinde tespit edilen 12 app var.
Bu kategoriyi derinlemesine analiz edeyim mi? Yoksa başka bir kategori mi seçmek istersin?
```

**Kullanıcı Kararı:** Kullanıcı "Kişisel Bakım kategorisini analiz et" der.

---

## Aşama 2: Derinlemesine Kategori Analizi

**Aktif Agent:** Market Scout + Strategy Analyst (paralel çalışır)
**Kullanılan Skill'ler:** customer-research, market-competitors, competitor-profiling, marketing-psychology

### Adım 2.1 — Detaylı App Analizi
Market Scout, kişisel bakım kategorisindeki her app için:
- App Store sayfasını scraper ile çeker
- Açıklama, özellik listesi, ekran görüntülerini analiz eder
- İndirme sayısı, gelir tahmini, aktif kullanıcı sayısını toplar
- Son 3 aydaki büyüme eğrisini çıkarır

### Adım 2.2 — Kullanıcı Yorumu Analizi
Market Scout, her app için:
- Son 500 kullanıcı yorumunu çeker (olumlu + olumsuz)
- Olumlu yorumlardan "kullanıcılar neyi seviyor" pattern'larını çıkarır
- Olumsuz yorumlardan (1-2 yıldız) "kullanıcıların acısı ne" pattern'larını çıkarır
- En sık tekrar eden şikayetleri kategorilendirir
- Henüz çözülmemiş "beyaz alan" problemlerini tespit eder

### Adım 2.3 — Stratejik Analiz
Strategy Analyst, Market Scout'un verileriyle:
- Her app için SWOT analizi çıkarır
- Rakip pozisyon haritası oluşturur (fiyat vs özellik, hedef kitle vs kapsam)
- Pazarda eksik olan özellikleri ve çözülmemiş problemleri listeler
- Kombinasyon fırsatlarını belirler (App A'nın X özelliği + App B'nin Y özelliği)

### Adım 2.4 — Kullanıcıya Sunum
Orchestrator, analiz sonuçlarını kullanıcıya sunar:

```
📊 KİŞİSEL BAKIM KATEGORİ ANALİZİ

En güçlü 3 app:
1. SkinTracker Pro — Cilt bakım takibi, aylık $45K gelir
   ❤️ Kullanıcıların sevdiği: AI destekli cilt analizi, kişiselleştirilmiş rutin
   💔 Şikayet: Ücretsiz sürüm çok kısıtlı, veri dışa aktarma yok

2. BeautyLog — Makyaj/kozmetik günlüğü, aylık $32K gelir
   ❤️ Sevdiği: Geniş ürün veritabanı, barkod tarama
   💔 Şikayet: UI çok karmaşık, yükleme yavaş, çevrimdışı çalışmıyor

3. GlowUp — Wellness + cilt bakımı, aylık $28K gelir
   ❤️ Sevdiği: Su takibi + cilt bakımı kombinasyonu, topluluk özelliği
   💔 Şikayet: Android'de çökme sorunu, bildirimler rahatsız edici, pahalı premium

🔍 TESPİT EDİLEN FIRSAT ALANLARI:
• 3 app'te de kullanıcılar "ürün önerisi" istiyor ama hiçbiri iyi yapamıyor
• Kullanıcılar cilt tipine göre alışveriş listesi oluşturamıyor
• Hiçbir app dermatolog/uzman bağlantısı sunmuyor
• Kullanıcılar ilerleme fotoğrafı çekip karşılaştırmak istiyor ama mevcut çözümler yetersiz

Bu fırsat alanlarından bir fikir geliştirmemi ister misin?
```

**Kullanıcı Kararı:** "Evet, tüm bu boşlukları dolduran bir fikir geliştir."

---

## Aşama 3: Fikir Geliştirme

**Aktif Agent:** Product Architect (Ürün Mimarı) + Strategy Analyst
**Kullanılan Skill'ler:** product-marketing, pricing, paywalls, marketing-psychology, marketing-ideas

### Adım 3.1 — Fikir Sentezi
Product Architect, tespit edilen boşluklardan bir ürün fikri sentezler:

**Fikir Taslağı: "SkinSync"**
- AI destekli cilt bakımı + ürün öneri motoru + dermatolog ağı
- Kullanıcı cilt tipini tanıtır → AI günlük rutin oluşturur
- Cilt ilerlemesini fotoğrafla takip eder, zaman çizelgesinde gösterir
- Kullanıcının cilt tipine ve bütçesine uygun ürünleri önerir
- Premium: dermatolog ile görüntülü danışmanlık

### Adım 3.2 — Fikir Tartışması
Orchestrator, fikri kullanıcıya açar ve sohbet başlatır:

```
💡 FİKİR ÖNERİSİ: SkinSync

Özet: [fikir detayı...]

Farklılaşma noktalarımız:
1. Ürün öneri motoru (rakiplerde yok)
2. Dermatolog ağı entegrasyonu (rakiplerde yok)
3. AI ile kişiselleştirilmiş bakım rutini (rakiplerden daha iyi)

Riskler:
• Dermatolog ağı kurmak zaman alabilir → MVP'de chat/async danışmanlık olarak başlayabiliriz
• Görüntü işleme AI'ı maliyetli olabilir → açık kaynak modellerle başlayabiliriz

Sence bu fikir nasıl? Eklemek/çıkarmak istediğin bir şey var mı?
Hedef kitle olarak hangi segmenti düşünelim?
- Cilt problemi olan gençler (akne vb.)
- Cilt bakımına önem veren 25-40 yaş kadınlar
- Dermatolog takibi gerektiren kronik cilt hastaları
```

**Kullanıcı:** Cevap verir, tartışır, fikri şekillendirir.

### Adım 3.3 — Fikir Son Haline Getirme
Product Architect, tartışma sonrası fikri günceller:
- Hedef kitleyi netleştirir
- MVP kapsamını belirler
- Gelir modelini tasarlar (freemium, tiered pricing)
- Riskleri ve mitigasyon stratejilerini listeler

**Çıktı:** `sessions/skinsync/idea-brief.md`

---

## Aşama 4: PRD (Product Requirement Document) Yazımı

**Aktif Agent:** Product Architect
**Kullanılan Skill'ler:** product-marketing, pricing, paywalls, aso

### Adım 4.1 — PRD Taslağı
Product Architect, onaylanmış fikirden detaylı PRD üretir:

- **Problem Tanımı:** Kullanıcıların mevcut çözümlerle yaşadığı sorunlar
- **Çözüm:** Ürünün ne yaptığı, nasıl çözdüğü
- **Hedef Kullanıcı Persona'ları:** 2-3 detaylı persona
- **MVP Kapsamı:** Olmazsa olmaz özellikler, güzel olur özellikler, sonra yaparız özellikler
- **Kullanıcı Akışları:** Ana ekranlar ve akış diyagramları
- **Teknik Gereksinimler:** Platform (iOS/Android/Web), API ihtiyaçları, 3. parti servisler
- **Başarı Metrikleri:** Günlük aktif kullanıcı, retention, gelir hedefleri
- **Pazarlama Açısı:** ASO anahtar kelimeleri, hedef kitle büyüklüğü, rakip konumlandırma

### Adım 4.2 — PRD Onayı
Orchestrator, PRD'yi kullanıcıya sunar:

```
📋 PRD: SkinSync v1.0 (MVP)

[PRD özeti...]

Bu PRD'yi coder'a iletmek üzere onaylıyor musun?
Ekleme/çıkarma istediğin bir şey var mı?
```

**Kullanıcı Kararı:** Onaylar veya revizyon ister.

**Çıktı:** `sessions/skinsync/prd-v1.md` (coder'a verilecek dosya)

### Adım 4.3 — Coder Brief'i
Orchestrator, coder için ek bir brief hazırlar:

```
👨‍💻 CODER'A İLETİLECEK DOSYALAR:

sessions/skinsync/prd-v1.md          → Ana PRD
sessions/skinsync/coder-brief.md     → Teknik özet ve önceliklendirme
sessions/skinsync/competitor-data.md → Rakip analizi verileri

Coder'ın bilmesi gerekenler:
• MVP 4-6 haftada çıkmalı
• iOS öncelikli, Android sonra
• AI modeli için OpenAI API veya açık kaynak alternatif
• Kullanıcı verileri GDPR uyumlu olmalı
• Test kullanıcıları için TestFlight build yeterli
```

---

## Aşama 5: Bekleme ve Hazırlık (MVP Geliştirme Süreci)

**Aktif Agent:** Orchestrator (pasif izleme)
**Bu aşamada coder MVP'yi geliştirir.**

### Adım 5.1 — Bekleme Modu
Orchestrator, kullanıcıya şu mesajı verir:

```
⏳ MVP geliştirme süreci başladı.

Bu süreçte ben sana şu konularda yardımcı olabilirim:
• Sosyal medya hesaplarını şimdiden açmak
• Launch öncesi "coming soon" sayfası hazırlamak
• E-posta listesi oluşturma stratejisi
• Rakip takibini güncellemek

MVP hazır olduğunda bana haber ver, pazarlama sürecini başlatalım.
```

### Adım 5.2 — İsteğe Bağlı Hazırlık Çalışmaları
Kullanıcı isterse bu aşamada:
- Content Creator → Sosyal medya profilleri, "coming soon" landing page içeriği
- Outreach Specialist → Erken kayıt e-posta listesi stratejisi
- Brand Guardian → Marka sesi, logo/renk brief'i

---

## Aşama 6: MVP Pazarlama Süreci

Coder MVP'yi teslim eder. Marketer kullanıcı orchestrator'a "MVP hazır" der.

**Aktif Agent'lar:** Launch Commander, Content Creator, Campaign Manager (orchestrator koordinasyonunda)

### Adım 6.1 — MVP Değerlendirmesi
Orchestrator, kullanıcıdan MVP detaylarını ister:

```
MVP hazır! Pazarlama sürecine başlamak için bana şunları ilet:
1. App Store / Google Play linki (yayındaysa) veya TestFlight linki
2. Coder'dan aldığın kısa bir özellik özeti
3. MVP'de hangi özellikler var, hangileri yok?
4. Bilinen bug'lar veya eksikler var mı?
```

### Adım 6.2 — Pazarlama Stratejisi Geliştirme
Strategy Analyst + Launch Commander, MVP özelinde bir pazarlama stratejisi oluşturur:

- Hedef kitle segmentasyonu
- Konumlandırma stratejisi
- Lansman zamanlaması ve kanal seçimi
- İçerik takvimi
- Reklam bütçesi önerisi (düşük bütçeli)
- Başarı metrikleri

**Çıktı:** `sessions/skinsync/marketing-strategy-v1.md`

### Adım 6.3 — Lansman İçeriği Üretimi
Content Creator devreye girer:
- App Store / Google Play açıklamaları (aso skill)
- Sosyal medya lansman postları (social skill, content-calendar template)
- Lansman e-postası (email-launch template)
- Landing page kopyası
- Tanıtım videosu senaryosu

**Çıktılar:** `sessions/skinsync/content/` klasörü altında

### Adım 6.4 — Reklam Kampanyası Kurulumu
Campaign Manager:
- Düşük bütçeli test kampanyaları tasarlar
- Hedefleme stratejisi belirler
- A/B test varyantları üretir
- Günlük bütçe ve KPI hedefleri belirler

**Çıktı:** `sessions/skinsync/ad-campaigns.md`

### Adım 6.5 — Lansman Checklist
Launch Commander, launch-checklist template'ini doldurur:
- Haftalık görev takvimi
- Risk matrisi
- Başarı metrikleri tablosu

**Çıktı:** `sessions/skinsync/launch-checklist.md`

### Adım 6.6 — Lansman
Orchestrator, tüm hazırlıklar tamamlanınca kullanıcıya "Lansmana hazırız" der. Kullanıcı onay verir, Launch Commander lansmanı yönetir.

---

## Aşama 7: Feedback Toplama ve Analiz

**Aktif Agent:** Market Scout + Analytics Master
**Kullanılan Skill'ler:** customer-research, analytics, market-report

### Adım 7.1 — Veri Toplama
Lansmandan 2-4 hafta sonra orchestrator veri toplamaya başlar:

```
📊 Lansman sonrası verileri topluyorum...

Bana yardımcı olabilir misin?
• App Store'dan kaç indirme oldu? (App Store Connect screenshot)
• Google Play'den kaç indirme oldu?
• Web sitesi ziyaretçi sayısı nedir?
• Sosyal medya etkileşimleri nasıl?
• Kullanıcılardan gelen yorumlar/e-postalar neler?
```

### Adım 7.2 — Kullanıcı Yorumu Analizi
Market Scout, app store yorumlarını ve sosyal medya bahislerini analiz eder:
- Olumlu/olumsuz yorum oranı
- En sık talep edilen özellikler
- En sık şikayet edilen sorunlar
- Kullanıcıların ürünü nasıl tanımladığı (customer language mining)

### Adım 7.3 — Kullanıcıya Sunum
Orchestrator, bulguları özetler:

```
📈 FEEDBACK ANALİZ RAPORU

İlgi var mı?
✅ Evet — 2 haftada 500+ indirme, %35 günlük aktif kullanıcı oranı
⚠️ Ama dikkat: 1 haftalık retention %40 (hedef %60'tı)

Kullanıcılar ne diyor?
❤️ "AI cilt analizi harika çalışıyor"
❤️ "Ürün önerileri çok isabetli"
💔 "Fotoğraf yükleme çok yavaş"
💔 "Ücretsiz sürümde neredeyse hiçbir şey yok"
💔 "Arkadaşlarımla paylaşamıyorum, sosyal özellik yok"

Önerim: MVP'yi iyileştirmeye devam edelim. 
Şu 3 konuya odaklanalım:
1. Fotoğraf yükleme hız optimizasyonu
2. Freemium dengesi (ücretsiz sürümü biraz açalım)
3. Sosyal paylaşım özelliği ekleyelim

Bu doğrultuda coder için güncellenmiş bir PRD hazırlayayım mı?
```

**Kullanıcı Kararı:** "Evet, PRD'yi güncelle."

---

## Aşama 8: İyileştirme Döngüsü

**Aktif Agent:** Product Architect + Strategy Analyst

### Adım 8.1 — Güncellenmiş PRD
Product Architect, feedback ve analizler ışığında PRD'yi günceller:
- Yeni özellik isteklerini ekler
- Mevcut özelliklerde iyileştirme noktalarını belirtir
- Önceliklendirme yapar (kritik / önemli / güzel olur)
- Coder için net isterler yazar

### Adım 8.2 — Coder Brief (v2)
Orchestrator, güncellenmiş PRD'yi ve feedback raporunu coder için paketler:

```
👨‍💻 CODER'A İLETİLECEK (v2):

sessions/skinsync/prd-v2.md              → Güncellenmiş PRD
sessions/skinsync/feedback-analysis.md   → Kullanıcı feedback analizi
sessions/skinsync/priority-matrix.md     → Önceliklendirme matrisi

Yeni isterler:
🔴 Kritik: Fotoğraf yükleme performans optimizasyonu
🟡 Önemli: Freemium kullanıcı akışı iyileştirme
🟢 Güzel: Sosyal paylaşım (ileri tarihli)
```

### Adım 8.3 — Döngü Devam
Coder iyileştirmeleri yapar → marketer tekrar pazarlar → feedback toplanır → PRD güncellenir → ... döngü devam eder.

---

## Aşama 9: Büyüme ve Ölçeklendirme

Ürün traction kazanınca Growth Hacker devreye girer:

**Aktif Agent:** Growth Hacker + Outreach Specialist
**Kullanılan Skill'ler:** referrals, churn-prevention, community-marketing, cold-email, prospecting

- Referans programı tasarımı
- Topluluk stratejisi
- Churn önleme mekanizmaları
- Influencer/partner outreach
- App Store featured başvurusu

---

## Süreç Özet Tablosu

| Aşama | Agent(lar) | Skill'ler | Çıktı Dosyası | Kullanıcı Etkileşimi |
|-------|-----------|-----------|---------------|---------------------|
| 1. Pazar Keşfi | Market Scout | webwright, customer-research | fırsat-haritasi.md | Kategori seçimi |
| 2. Derin Analiz | Market Scout + Strategy Analyst | market-competitors, competitor-profiling | kategori-analizi.md | Fırsat seçimi |
| 3. Fikir Geliştirme | Product Architect + Strategy Analyst | product-marketing, pricing | idea-brief.md | Fikir tartışması |
| 4. PRD Yazımı | Product Architect | product-marketing, pricing, aso | prd-v1.md, coder-brief.md | PRD onayı |
| 5. Bekleme | Orchestrator | - | - | İsteğe bağlı hazırlık |
| 6. Pazarlama | Launch Commander + Content Creator + Campaign Manager | launch, content-strategy, ads, social | marketing-strategy.md, içerikler | Strateji onayı |
| 7. Feedback | Market Scout + Analytics Master | customer-research, analytics, market-report | feedback-analysis.md | Veri sağlama |
| 8. İyileştirme | Product Architect + Strategy Analyst | market-competitors | prd-v2.md | İyileştirme onayı |
| 9. Büyüme | Growth Hacker + Outreach Specialist | referrals, churn-prevention, community-marketing | growth-plan.md | Döngüsel kararlar |

---

## Alternatif Keşif Yöntemleri

Bu örnek App Store üzerinden ilerledi. Aynı pipeline şu kaynaklarla da çalışabilir:

| Kaynak | Keşif Yöntemi | Uygun Olduğu Ürün Tipi |
|--------|--------------|----------------------|
| Reddit / HackerNews | Topluluk şikayet ve istek analizi | SaaS, developer tools |
| Product Hunt | Yeni lansmanları analiz etme | Her tür dijital ürün |
| GitHub trending | Açık kaynak projelerdeki boşluklar | Developer tools, altyapı |
| G2 / Capterra | Kurumsal yazılım kullanıcı yorumları | B2B SaaS |
| Google Trends | Arama trendlerindeki yükselişler | Tüketici ürünleri |
| TikTok / Instagram | Viral trendler ve içerik açıkları | B2C uygulamalar |
| LinkedIn job postings | Şirketlerin hangi yetenekleri aradığı | B2B, enterprise |
| Amazon yorumları | Fiziksel+digital ürün şikayetleri | Karma ürünler |
| Forumlar (özel) | Niş toplulukların ihtiyaçları | Niş ürünler |
| App Store / Play Store | Mobil app boşlukları | Mobil uygulamalar |

Orchestrator, keşif aşamasında bu kaynaklardan hangilerinin taranacağını kullanıcıya sorar veya ürün tipine göre otomatik seçer.
