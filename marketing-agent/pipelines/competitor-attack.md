# Pipeline 6: Rakip Saldırı (Competitor Attack)

**Zincirdeki yeri:** Zincir D (P4'ü destekler) veya bağımsız giriş noktası.

**Ne zaman çalışır:** Belirli bir rakibe karşı strateji gerektiğinde. Kullanıcı "şu rakibe karşı ne yapabilirim" dediğinde.

**Amaç:** Rakibi derinlemesine analiz edip, zayıf noktalarına yönelik aksiyon planı çıkarmak.

**Ön koşul:** Hedef rakip belirlenmiş olmalı. `product-context.md` mevcut olmalı.

---

## Pipeline Akışı

```
Kullanıcı: "X rakibine karşı strateji istiyorum"
        │
        ▼
[6.1] Market Scout → Rakibi derinlemesine tara
        │  Çıktı: rakip-profili.md
        ▼
[6.2] Strategy Analyst → Rakibin zayıf noktalarını bul
        │  Çıktı: rakip-acik-analizi.md
        ▼
[6.3] Content Creator → Rakibe karşı içerik stratejisi
        │  Çıktı: karsilastirma-icerik.md
        ▼
[6.4] Campaign Manager → Rakip anahtar kelimelerine reklam
        │  Çıktı: rakip-kampanya.md
        ▼
[6.5] Growth Hacker → Rakip müşterilerini çekme stratejisi
           Çıktı: musteri-cekme.md
```

---

## Adım Detayları

### 6.1 — Derin Rakip Profili
**Agent:** Market Scout
**Skill:** `competitor-profiling`
**Eylem:**
- Rakibin tüm sayfalarını tara (homepage, pricing, features, about, customers, blog)
- SEO analizi yap
- Sosyal medya varlığını incele
- Kullanıcı yorumlarını topla

**Çıktı (`rakip-profili.md`):**
- Özet, konumlandırma, ürün/özellikler, fiyatlandırma, müşteri kanıtları, güçlü/zayıf yanlar

### 6.2 — Zayıf Nokta Analizi
**Agent:** Strategy Analyst
**Çıktı (`rakip-acik-analizi.md`):**
```markdown
# Rakip Açık Analizi: [Rakip]
## Tespit Edilen Zayıflıklar
| Zayıflık | Şiddet | Bizim Avantajımız | Aksiyon |
|---------|--------|------------------|---------|
| ... | Kritik | ... | ... |

## Saldırı Vektörleri
1. ...
```

### 6.3 — Karşılaştırma İçeriği
**Agent:** Content Creator
**Çıktı (`karsilastirma-icerik.md`):**
- "X vs Y" landing page kopyası
- Rakip karşılaştırma tablosu
- Rakip müşterilerine yönelik blog/sosyal medya içeriği

### 6.4 — Rakip Anahtar Kelime Reklamı
**Agent:** Campaign Manager
**Çıktı (`rakip-kampanya.md`):**
- Rakip marka anahtar kelimelerine reklam
- Rakip ürün sayfası ziyaretçilerine retargeting

### 6.5 — Müşteri Çekme Stratejisi
**Agent:** Growth Hacker
**Çıktı (`musteri-cekme.md`):**
- Switching campaign (rakipten geçiş kampanyası)
- Karşılaştırma sayfası CRO
- Rakip müşterilerine özel teklif

---

## Çıktı Dosyaları

| Dosya | Üreten |
|-------|--------|
| `rakip-profili.md` | Market Scout |
| `rakip-acik-analizi.md` | Strategy Analyst |
| `karsilastirma-icerik.md` | Content Creator |
| `rakip-kampanya.md` | Campaign Manager |
| `musteri-cekme.md` | Growth Hacker |

---

## Sonraki Adım

Pipeline 6 bağımsız çalışır. Sonuçları **Pipeline 2 (MVP Lansman)** veya **Pipeline 4 (Büyüme Motoru)** içinde kullanılabilir.
