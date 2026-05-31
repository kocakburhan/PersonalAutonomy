---
name: seo-audit
description: Teknik ve on-page SEO denetimi. Title, meta, heading, hız, schema, iç bağlantı.
metadata:
  version: 2.0.0
  source: coreyhaines31/marketingskills
---

# SEO Denetimi

SEO teknik denetim uzmanı. Sitenin arama motoru sağlığını kontrol eder, hataları tespit eder, öncelikli düzeltmeleri sıralar.

## Denetim Kategorileri

### 1. On-Page SEO
- **Title tag:** 50-60 karakter, anahtar kelime başta, benzersiz
- **Meta description:** 150-155 karakter, CTA, anahtar kelime
- **H1:** Tek olmalı, anahtar kelime içermeli
- **Heading hiyerarşisi:** H1 → H2 → H3 mantıksal sıralı
- **URL yapısı:** Temiz, okunabilir, anahtar kelimeli
- **Görsel alt tag:** Tüm görsellerde, açıklayıcı

### 2. Teknik SEO
- SSL sertifikası
- Mobil uyumluluk
- Sayfa hızı (hedef < 3sn)
- Schema markup (Article, Product, FAQ, Breadcrumb)
- Robots.txt yapılandırması
- XML sitemap
- Canonical URL'ler
- Kırık linkler

### 3. İçerik Kalitesi
- İçerik uzunluğu ve derinliği
- Özgünlük (duplicate content kontrolü)
- E-E-A-T sinyalleri (Experience, Expertise, Authoritativeness, Trustworthiness)
- Tazelik (güncellenme tarihi)

### 4. İç Bağlantı Yapısı
- Sayfalar arası linkleme
- Önemli sayfalara kaç iç link var
- Anchor text çeşitliliği
- Yetim sayfalar (hiç link almayan)

## Denetim Süreci

1. **Siteyi tara** — Puppeteer MCP veya WebFetch ile
2. **On-page elementleri çıkar:** title, meta, headings, images, links
3. **Teknik kontrolleri yap:** SSL, robots.txt, sitemap
4. **İçeriği değerlendir:** E-E-A-T kriterleri
5. **Hataları önceliklendir:** Kritik → Önemli → İyileştirme

## Çıktı Formatı

```markdown
# SEO Denetimi: {URL}
**Tarih:** {bugün}
**SEO Skoru:** {0-100}

## Kritik Hatalar (Hemen Düzeltilmeli)
| # | Sorun | Sayfa | Çözüm |
|---|-------|-------|-------|

## On-Page SEO
| Öğe | Durum | Mevcut | Önerilen |
|-----|-------|--------|----------|

## Teknik SEO
| Öğe | Durum | Not |
|-----|-------|-----|

## Öncelikli Aksiyonlar
1. 🔴 ...
2. 🟡 ...
3. 🟢 ...
```
