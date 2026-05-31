# Pipeline 9: Fiziksel İşletme Dijital Varlık (Local Business Launch)

**Zincirdeki yeri:** Zincir C (başlangıç noktası). Sonrasında P7 ve P3 ile devam eder.

**Ne zaman çalışır:** Fiziksel işletme (spor salonu, diş hekimi, mobilyacı, psikolog, restoran, kuaför, vb.) için dijital pazarlama stratejisi gerektiğinde.

**Amaç:** Fiziksel işletmenin dijital varlığını (Google Maps, sosyal medya, web sitesi) oluşturup optimize etmek ve yerel pazarlama stratejisi geliştirmek.

**Ön koşul:** İşletme bilgileri (isim, adres, telefon, sektör) mevcut olmalı.

---

## Pipeline Akışı

```
Kullanıcı: "İşletmem için dijital pazarlama istiyorum"
        │
        ▼
[9.1] Orchestrator → İşletme detaylarını al
        │  (isim, adres, telefon, sektör, hedef kitle, mevcut dijital varlık)
        ▼
[9.2] Market Scout → Google Maps rakip analizi
        │  Bölgedeki rakipleri tara, GBP profillerini karşılaştır
        │  Çıktı: yerel-pazar-analizi.md
        ▼
[9.3] Market Scout → Yerel müşteri yorumu analizi
        │  Forum/şikayet sitelerinde rakiplerin müşteri yorumlarını analiz et
        │  Çıktı: yerel-musteri-analizi.md
        ▼
[9.4] Strategy Analyst → SWOT + rekabet avantajı + fırsat alanları
        │  Çıktı: rekabet-stratejisi.md
        ▼
[9.5] Content Creator → Google Business Profile optimizasyonu
        │  Açıklama, hizmet listesi, fotoğraf stratejisi
        │  Çıktı: gbp-optimizasyon.md
        ▼
[9.6] Content Creator → Sosyal medya stratejisi
        │  Instagram/TikTok öncelikli, sektöre özel içerik takvimi
        │  Çıktı: icerik-takvimi.md, sosyal-medya-plan.md
        ▼
[9.7] Brand Guardian → Marka kimliği
        │  Ses, logo/renk önerileri, kurumsal kimlik brief'i
        │  Çıktı: marka-kimligi.md
        ▼
[9.8] Campaign Manager → Lokal reklam stratejisi
        │  Google Local Ads, Instagram/TikTok konum hedefli reklam
        │  Çıktı: lokal-reklam-plani.md
        ▼
[9.9] Orchestrator → Tüm planı kullanıcıya sun, onay al
        │
        ▼
[9.10] Outreach Specialist → Yerel iş birlikleri
        │  Çapraz tanıtım, diğer esnaflarla partnerlik
        │  Çıktı: yerel-isbirlikleri.md
        ▼
[9.11] Analytics Master → Başarı metrikleri
           Google Maps görüntülenme, arama, web trafiği, randevu dönüşümleri
           Çıktı: basari-metrikleri.md
```

---

## Adım Detayları

### 9.1 — İşletme Detaylarını Toplama
**Agent:** Orchestrator

```
İşletmeni dijital dünyaya taşıyalım! Bana şu bilgileri ver:

ZORUNLU:
• İşletme adı
• Adres (tam)
• Telefon numarası
• Sektör (spor salonu / diş hekimi / mobilyacı / psikolog / restoran / ...)
• Çalışma saatleri

ÖNEMLİ:
• Hedef kitlen kim? (yaş aralığı, gelir seviyesi, bölge)
• Mevcut dijital varlığın var mı? (web sitesi, Instagram, Google Maps kaydı)
• Rakiplerin kimler? (isim verirsen daha iyi analiz yaparım)

OPSİYONEL:
• Logo / görsel materyalin var mı?
• Bütçen nedir? (aylık pazarlama bütçesi)
• Özel kampanyaların / fırsatların var mı?
```

### 9.2 — Google Maps Rakip Analizi
**Agent:** Market Scout
**Kaynaklar:**
- Google Maps (işletmenin bulunduğu bölgede aynı sektördeki işletmeler)
- Google Business Profile (rakip profillerinin puan, yorum sayısı, fotoğraf kalitesi)
- Rakip web siteleri (varsa)

**Çıktı (`yerel-pazar-analizi.md`):**
```markdown
# Yerel Pazar Analizi: [İşletme]
## Bölge: [il/ilçe/semt]
- Taranan yarıçap: [x] km
- Tespit edilen rakip: [sayı]

## Rakip Karşılaştırması
| İşletme | Puan | Yorum | Fotoğraf | Web | GBP Kalitesi |
|---------|------|-------|----------|-----|-------------|
| Biz | - | - | - | - | - |
| Rakip 1 | 4.5 | 120 | 25 | Var | Yüksek |
| Rakip 2 | 3.8 | 45 | 5 | Yok | Düşük |

## Google Maps Yoğunluk Analizi
- Bölgede rakip yoğunluğu: [düşük/orta/yüksek]
- En yakın rakip mesafesi: [km]
- Bölgenin arama hacmi: [tahmini]
```

### 9.3 — Yerel Müşteri Yorumu Analizi
**Agent:** Market Scout
**Kaynaklar:**
- Google Maps yorumları (rakip işletmelerin)
- Şikayetvar, Ekşi Sözlük, sektörel forumlar
- Yerel Facebook grupları
- Instagram lokasyon etiketi yorumları

**Çıktı (`yerel-musteri-analizi.md`):**
```markdown
# Yerel Müşteri Analizi: [Sektör]
## Rakiplerin Güçlü Yanları (müşteri yorumlarından)
1. [pattern] — [kaç işletmede görüldü]

## Rakiplerin Zayıf Yanları (şikayetlerden)
1. [pattern] — [kaç işletmede görüldü]

## Müşterilerin Aradığı Ama Bulamadığı
1. [ihtiyaç]

## Fırsat Alanları
- ...
```

### 9.4 — Rekabet Stratejisi
**Agent:** Strategy Analyst
**Çıktı (`rekabet-stratejisi.md`):**
- SWOT analizi (işletme özelinde)
- Yerel rekabet avantajı (konum, fiyat, hizmet kalitesi, uzmanlık)
- Fırsat alanları (hangi hizmet eksik, hangi müşteri segmenti boş)
- Fiyat konumlandırma önerisi

### 9.5 — Google Business Profile Optimizasyonu
**Agent:** Content Creator
**Çıktı (`gbp-optimizasyon.md`):**
```markdown
# Google Business Profile Optimizasyonu: [İşletme]

## İşletme Açıklaması (750 karakter)
[SEO optimize, anahtar kelime içeren, müşteriye hitap eden açıklama]

## Hizmet Listesi
| Hizmet | Açıklama | Fiyat (opsiyonel) |
|--------|----------|------------------|
| ... | ... | ... |

## Fotoğraf Stratejisi
- Kapak fotoğrafı: [açıklama]
- İç mekan: en az 5 fotoğraf
- Dış mekan: en az 2 fotoğraf
- Ürün/hizmet: en az 5 fotoğraf
- Ekip: en az 2 fotoğraf

## Haftalık Gönderi Planı
| Gün | İçerik Tipi | Başlık |
|-----|------------|--------|
| Pzt | Teklif/Kampanya | ... |

## Soru-Cevap (Q&A) Stratejisi
[En sık sorulacak 10 soru ve yanıtı]

## Yorum Yönetimi
- Olumlu yoruma yanıt şablonu
- Olumsuz yoruma yanıt şablonu
```

### 9.6 — Sosyal Medya Stratejisi
**Agent:** Content Creator
**Çıktılar:**
- `icerik-takvimi.md` — 30 günlük içerik takvimi (sektöre özel)
- `sosyal-medya-plan.md`:
  ```markdown
  # Sosyal Medya Planı: [İşletme]
  ## Platform Seçimi
  | Platform | Öncelik | Hedef Kitle | İçerik Tipi |
  |----------|---------|------------|------------|
  | Instagram | Yüksek | 25-45 yaş | Reels, hikaye, before/after |
  | TikTok | Orta | 18-35 yaş | Kısa video, trend |
  | Facebook | Düşük | 35+ yaş | Etkinlik, topluluk |

  ## İçerik Sütunları
  - Eğitim/Bilgi: %35
  - Hizmet Tanıtımı: %25
  - Müşteri Deneyimi/Sosyal Kanıt: %25
  - Perde Arkası/Ekip: %15
  ```

### 9.7 — Marka Kimliği
**Agent:** Brand Guardian
**Çıktı (`marka-kimligi.md`):**
- Marka sesi (Türkçe, sektöre uygun ton)
- Logo brief'i (konsept, renk, tipografi)
- Renk paleti önerisi
- Kurumsal kimlik uygulama alanları

### 9.8 — Lokal Reklam Stratejisi
**Agent:** Campaign Manager
**Çıktı (`lokal-reklam-plani.md`):**
```markdown
# Lokal Reklam Planı: [İşletme]

## Google Local Ads
- Hedef bölge: [il/ilçe]
- Yarıçap: [x] km
- Anahtar kelimeler: [liste]
- Günlük bütçe önerisi: ₺[x]
- Aylık tahmini bütçe: ₺[x]

## Instagram/TikTok Reklam
- Hedef lokasyon: [bölge]
- Hedef kitle: [yaş, ilgi]
- Reklam formatı: [story/reels/feed]
- Günlük bütçe önerisi: ₺[x]

## Toplam Aylık Bütçe: ₺[x]
```

### 9.9 — Onay
**Agent:** Orchestrator
Tüm planı kullanıcıya özetler, onay alır.

### 9.10 — Yerel İş Birlikleri
**Agent:** Outreach Specialist
**Çıktı (`yerel-isbirlikleri.md`):**
```markdown
# Yerel İş Birlikleri: [İşletme]

## Potansiyel Partnerler
| İşletme | Sektör | Ortak Hedef Kitle | İş Birliği Türü |
|---------|--------|------------------|----------------|
| ... | ... | ... | Çapraz tanıtım / ortak kampanya / referans |

## İş Birliği Stratejisi
1. [strateji]
```

### 9.11 — Başarı Metrikleri
**Agent:** Analytics Master
**Çıktı (`basari-metrikleri.md`):**
```markdown
# Başarı Metrikleri: [İşletme]

## Google Maps Metrikleri
| Metrik | Başlangıç | 30 Gün Hedef | 90 Gün Hedef |
|--------|----------|-------------|-------------|
| Görüntülenme | - | [x] | [x] |
| Arama | - | [x] | [x] |
| Web tıklaması | - | [x] | [x] |
| Arama tıklaması | - | [x] | [x] |
| Yol tarifi | - | [x] | [x] |

## Dönüşüm Metrikleri
| Metrik | Başlangıç | Hedef |
|--------|----------|-------|
| Telefon araması | - | [x]/ay |
| Randevu/rezervasyon | - | [x]/ay |
| Web sitesi ziyareti | - | [x]/ay |

## Sosyal Medya Metrikleri
| Metrik | Başlangıç | Hedef |
|--------|----------|-------|
| Takipçi | 0 | [x] |
| Etkileşim oranı | - | >%3 |
```

---

## Karar Noktaları

| Adım | Karar |
|------|-------|
| 9.9 | Tüm planı onayla / revize et |

---

## Çıktı Dosyaları

| Dosya | Üreten |
|-------|--------|
| `yerel-pazar-analizi.md` | Market Scout |
| `yerel-musteri-analizi.md` | Market Scout |
| `rekabet-stratejisi.md` | Strategy Analyst |
| `gbp-optimizasyon.md` | Content Creator |
| `icerik-takvimi.md` | Content Creator |
| `sosyal-medya-plan.md` | Content Creator |
| `marka-kimligi.md` | Brand Guardian |
| `lokal-reklam-plani.md` | Campaign Manager |
| `yerel-isbirlikleri.md` | Outreach Specialist |
| `basari-metrikleri.md` | Analytics Master |

---

## Fiziksel İşletme vs Dijital Ürün Karşılaştırması

| Özellik | Dijital Ürün (P1-P8) | Fiziksel İşletme (P9) |
|---------|---------------------|----------------------|
| Keşif kaynağı | App Store, G2, Reddit | Google Maps, yerel forumlar |
| SEO odağı | ASO, web SEO | Google Maps SEO, lokal SEO |
| Sosyal medya | Tüm platformlar | Instagram/TikTok öncelikli |
| Reklam | Google Ads, Meta, LinkedIn | Google Local Ads, konum hedefli |
| Başarı metriği | İndirme, DAU, gelir | Görüntülenme, arama, randevu |
| "Coder brief" | PRD → yazılımcı | Web sitesi/randevu sistemi brief'i |
| Müşteri kazanımı | Dijital onboarding | Fiziksel ziyaret/telefon |

---

## Sonraki Pipeline

Pipeline 9 tamamlandıktan sonra orchestrator şu zinciri önerir:

- **Pipeline 7 (İçerik Makinesi)** → sürekli içerik üretimi
- **Pipeline 3 (Feedback ve İyileştirme)** → Google Maps yorumları, müşteri memnuniyeti takibi → P9'u güncelle

Bu döngü sürekli çalışır: P9 → P7 → P3 → P9 (güncelle) → P7 → ...
