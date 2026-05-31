---
name: image
description: Pazarlama görselleri için AI görsel üretimi — blog hero, sosyal grafik, infografik.
metadata:
  version: 2.0.0
  source: coreyhaines31/marketingskills
---

# AI Görsel Üretimi

Pazarlama amaçlı AI görsel üretim uzmanı. Blog hero, sosyal medya grafiği, ürün ekran görüntüsü, infografik.

## ÖNEMLİ NOT

**Görsel üretim araçlarının API entegrasyonu henüz yapılmadı.** Bu skill şu an için görsel stratejisi, prompt yazımı ve tasarım brief'i oluşturur. Gerçek görsel üretimi için aşağıdaki araçlardan birinin API entegrasyonu gereklidir.

**Entegre edilecek araç seçenekleri (proje kodlama aşamasında karar verilecek):**
- **Midjourney API:** En kaliteli, ama API resmi değil (webhook ile)
- **DALL-E 3 (OpenAI API):** Kolay entegrasyon, iyi kalite
- **Stable Diffusion API:** Açık kaynak, self-host edilebilir
- **Canva API:** Şablon bazlı, hızlı
- **Figma API:** Tasarım sistemi ile entegre

**API key alımı ve entegrasyon:** Proje geliştirme aşamasında yapılacak.

## Görsel Tipleri

| Tip | Boyut | Kullanım |
|-----|-------|----------|
| Blog hero | 1200x630 (16:9) | Blog yazısı, sosyal paylaşım |
| Sosyal grafik | 1080x1080 (1:1) veya 1080x1350 (4:5) | Instagram, LinkedIn |
| Infografik | 800x2000 (dikey) | Blog, Pinterest |
| Thumbnail | 1280x720 (16:9) | YouTube |
| Reklam banner'ı | 1200x628 | Google Display, Meta |

## Prompt Yazımı

### Midjourney Prompt Formülü
```
[Konu] + [Stil] + [Kompozisyon] + [Renk paleti] + [Teknik detaylar] --ar [en-boy] --v 6
```

**Örnek:**
```
Futuristic project management dashboard with AI holograms, clean interface, 
blue and purple gradient, minimalist style, isometric view --ar 16:9 --v 6
```

### DALL-E Prompt Formülü
```
[Detaylı sahne açıklaması], [stil], [aydınlatma], [renk], [kompozisyon]
```

## Görsel Stratejisi

- **Tutarlılık:** Tüm görseller aynı stil, renk paleti, tipografi
- **Marka:** Logo, renkler, font
- **Duygu:** Hangi duyguyu uyandırmalı?
- **Hikaye:** Görsel ne anlatıyor?

## Kullanım Kanalları

| Kanal | Optimal Boyut | Format |
|-------|-------------|--------|
| Blog | 1200x630 | JPEG/WebP |
| LinkedIn | 1200x627 | JPEG |
| Instagram Feed | 1080x1080 | JPEG |
| Instagram Story | 1080x1920 | JPEG |
| Twitter/X | 1200x675 | JPEG |
