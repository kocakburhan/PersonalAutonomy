# Pipeline 7: İçerik Makinesi (Content Machine)

**Zincirdeki yeri:** Zincir C (P9'u destekler) ve Zincir E (bağımsız, sürekli döngü).

**Ne zaman çalışır:**
- Düzenli içerik üretimi gerektiğinde
- "Sosyal medyada aktif olmak istiyorum" dendiğinde
- Fiziksel işletme için sürekli içerik akışı gerektiğinde

**Amaç:** 30 günlük içerik takvimi oluşturup, performansa göre sürekli güncellemek.

**Ön koşul:** `product-context.md` mevcut olmalı. Marka sesi belirlenmiş olmalı (Brand Guardian'dan).

---

## Pipeline Akışı

```
Kullanıcı: "İçerik üretmeye başlayalım"
        │
        ▼
[7.1] Content Creator → 30 günlük içerik takvimi oluştur
        │  Script: social_calendar.py
        │  Çıktı: content-calendar.md
        ▼
[7.2] Content Creator → Platform'a özel post'ları yaz
        │  Çıktı: content/ klasörü (her post bir .md)
        ▼
[7.3] Analytics Master → İçerik performansını takip et (30 gün sonra)
        │  Çıktı: icerik-performans.md
        ▼
[7.4] Content Creator → Performansa göre takvimi güncelle
           Çıktı: content-calendar-v2.md
           │
           └── [7.2]'ye dön (yeni post'lar) → sürekli döngü
```

---

## Adım Detayları

### 7.1 — İçerik Takvimi
**Agent:** Content Creator
**Script:** `python social_calendar.py --topic "[konu]" --platforms instagram,linkedin --brand "[marka]"`

**Çıktı (`content-calendar.md`):**
- 5 sütun: Eğitim (%40), Sosyal Kanıt (%20), Ürün/Tanıtım (%15), Topluluk/Etkileşim (%15), Marka/Kültür (%10)
- Haftalık temalar
- Günlük post başlıkları

### 7.2 — Post Üretimi
**Agent:** Content Creator
**Her post için:**
- Platform (Instagram/LinkedIn/TikTok/Twitter)
- Görsel brief
- Post metni
- Hashtag'ler
- Yayınlanma tarihi

**Platform özel kurallar:**
- Instagram: görsel odaklı, carousel/reels/story, 15-20 hashtag
- LinkedIn: profesyonel ton, uzun form, 3-5 hashtag
- Twitter/X: kısa/direkt, thread opsiyonu, 1-2 hashtag
- TikTok: trend odaklı, kısa video script, 3-5 hashtag

### 7.3 — Performans Takibi
**Agent:** Analytics Master (30 gün sonra)
**Çıktı (`icerik-performans.md`):**
```markdown
# İçerik Performansı: [30 günlük dönem]
## Platform Bazlı
| Platform | Post Sayısı | Toplam Etkileşim | Ort. Etkileşim | En İyi Post |
|----------|------------|-----------------|---------------|------------|
| Instagram | 30 | [x] | [x] | [link] |
| LinkedIn | 20 | [x] | [x] | [link] |

## En İyi Performans Gösteren İçerik Tipleri
1. [tip] — ortalama [x] etkileşim

## Öğrenilenler ve Öneriler
- ...
```

### 7.4 — Takvim Güncelleme
**Agent:** Content Creator
Performans verisine göre yeni takvim:
- İyi performans gösteren içerik tiplerinin oranını artır
- Kötü performans gösterenleri azalt veya değiştir
- Yeni trend/konuları ekle

---

## Çıktı Dosyaları

| Dosya | Üreten |
|-------|--------|
| `content-calendar.md` | Content Creator |
| `content/social-post-*.md` | Content Creator |
| `icerik-performans.md` | Analytics Master |
| `content-calendar-v2.md` | Content Creator |

---

## Sonraki Adım

Pipeline 7 sürekli döngü halinde çalışır. Her ay yeni takvim + performans analizi yapılır.
