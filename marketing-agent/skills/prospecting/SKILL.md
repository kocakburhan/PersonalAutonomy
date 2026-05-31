---
name: prospecting
description: Potansiyel müşteri bulma ve liste oluşturma. LinkedIn, Apollo, sektör verileri.
metadata:
  version: 2.0.0
  source: coreyhaines31/marketingskills
---

# Prospecting (Müşteri Adayı Bulma)

Potansiyel müşteri araştırma uzmanı. Hedef kitleye uygun prospect'leri bulur, kalifiye eder, liste oluşturur.

## Başlamadan Önce

1. **product-marketing** context'ini kontrol et
2. Şunları anla:
   - Hedef kitle profili (ICP — Ideal Customer Profile)
   - Kaç prospect lazım?
   - Hangi kanallar? (LinkedIn, Apollo, manual)

## Prospect Kaynakları

| Kaynak | Ne İçin | Yöntem |
|--------|---------|--------|
| LinkedIn Sales Navigator | B2B, unvan/şirket filtresi | Manuel + scraping |
| Apollo.io | B2B, email + telefon | CSV export |
| BuiltWith / Wappalyzer | Tech stack bazlı | Site analizi |
| CrunchBase | Startup, funding | Veritabanı |
| Google Maps | Lokal işletme | Manuel |
| İş ilanları | Büyüyen şirketler | Indeed, LinkedIn Jobs |
| Konferans katılımcıları | Sektör spesifik | Etkinlik siteleri |

## ICP (Ideal Customer Profile) Tanımı

Net tanımla ki doğru kişileri bulasın:

- **Şirket:** Sektör, büyüklük, lokasyon, aşama
- **Karar verici:** Unvan, departman, kıdem
- **Tetikleyiciler:** Yeni işe başlama, funding, büyüme, tech stack değişimi
- **Acı noktası:** Hangi problem için senin ürününü ararlar?

## Sıcak Prospect Sinyalleri

- Yeni işe başlayan yönetici (eski sistemi değiştirmek için bütçe almıştır)
- Yeni funding alan startup (büyüme bütçesi vardır)
- Rakip ürünü kullanan ama şikayet eden (Twitter/Reddit/G2)
- Sektör etkinliğinde konuşmacı (sektörde aktif)
- İş ilanında senin ürün kategorini arayan şirket

## Prospect Listesi Formatı

```csv
İsim,Şirket,Unvan,LinkedIn,Email,Tahmini Email,Notlar,Sıcaklık
Ahmet Yılmaz,TechCorp,CTO,linkedin.com/in/...,ahmet@techcorp.com,ahmet@techcorp.com,Jira kullanıyor,Yüksek
```

- **Sıcaklık:** Yüksek (tetikleyici var) / Orta (ICP uyuyor) / Düşük (potansiyel)

## Outreach Öncesi Araştırma

Her prospect için 2 dk araştırma:
- Son LinkedIn paylaşımı
- Şirket haberi
- Tech stack
- Ortak bağlantı
- Kişiselleştirme için bir "hook"

## Kalifikasyon Soruları

Listeyi cold-email'e başlamadan önce süz:
- Bütçe var mı? (şirket büyüklüğü, funding)
- İhtiyaç var mı? (mevcut çözüm, acı noktası)
- Zamanlama doğru mu? (büyüme, değişim sinyali)
- Karar verici mi? (unvan kontrolü)
