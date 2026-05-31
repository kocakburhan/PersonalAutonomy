---
name: competitor-profiling
description: Rakip URL'lerinden derinlemesine profil çıkarma — site scraping + SEO verisi + konumlandırma.
metadata:
  version: 2.0.0
  source: coreyhaines31/marketingskills
---

# Rakip Profili Çıkarma

Rekabet istihbaratı analisti. Rakip URL'lerini alır, site scraping + SEO verisi + pazar verisi ile kapsamlı profil oluşturur.

## Veri Kaynakları

1. **Site Scraping:** Puppeteer MCP ile rakip sitesinin sayfalarını tara
2. **SEO Verisi:** Domain otoritesi, backlink profili, organik trafik
3. **İnceleme Verisi:** G2, Capterra, Product Hunt yorumları

## Araştırma Süreci

### Aşama 1: Site Tarama
Öncelikli sayfalar:
- Homepage → başlık, değer önerisi, CTA, hedef kitle sinyali
- Pricing → planlar, fiyatlar, özellik dağılımı
- Features → yetenekler, vurgulanan farklılıklar
- About → kuruluş hikayesi, ekip, funding
- Customers → logolar, vaka çalışmaları, sektörler
- Blog → içerik stratejisi, sıklık, odak konular

### Aşama 2: SEO ve Pazar Verisi
- Domain otoritesi
- Organik trafik tahmini
- Sıralanan anahtar kelimeler
- Backlink profili
- En yakın organik rakipler

### Aşama 3: Sentez
Toplanan verileri birleştir, profil oluştur.

## Profil Şablonu

```markdown
# {Rakip Adı} — Rakip Profili
**URL:** {url} | **Tarih:** {bugün}

## Özet
| Metrik | Değer |
|--------|-------|
| Slogan | ... |
| Kuruluş | {yıl} |
| Domain otoritesi | {puan} |
| Tahmini organik trafik | {sayı}/ay |

## Konumlandırma & Mesaj
- Ana değer önerisi: ...
- Hedef kitle: ...
- Konumlandırma açısı: ...
- Ana mesaj temaları: ...

## Ürün & Özellikler
- Temel yetenekler
- Öne çıkan farklılıklar
- Entegrasyonlar

## Fiyatlandırma
| Plan | Fiyat | İçerik |
|------|-------|--------|

## Müşteriler & Sosyal Kanıt
- Önemli müşteriler
- İnceleme puanları

## Güçlü & Zayıf Yönler
### Güçlü
- ...
### Zayıf
- ...

## Bizim İçin Stratejik Çıkarımlar
- Nerede güçlüler (kaçın)
- Nerede zayıflar (saldır)
- Fırsat pencereleri
```
