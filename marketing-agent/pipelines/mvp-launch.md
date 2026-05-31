# Pipeline 2: MVP Lansman (MVP Launch)

**Zincirdeki yeri:** Zincir A ve B (P1/P5'ten sonra, coder MVP'yi teslim edince).

**Ne zaman çalışır:** Coder MVP'yi teslim ettiğinde, kullanıcı "MVP hazır" dediğinde.

**Amaç:** MVP'yi pazarlamak için strateji, içerik, reklam ve lansman planı oluşturmak.

**Ön koşul:** MVP hazır olmalı (app store'da yayında veya TestFlight'ta, ya da web app URL'si var). `product-context.md` ve `prd-v1.md` mevcut olmalı.

---

## Pipeline Akışı

```
Kullanıcı: "MVP hazır"
        │
        ▼
[2.1] Orchestrator → MVP detaylarını kullanıcıdan al
        │  Sorular: link, özellik listesi, bilinen bug'lar, eksikler
        ▼
[2.2] Strategy Analyst → MVP'ye özel pazarlama stratejisi
        │  Çıktı: marketing-strategy.md
        ▼
[2.3] Content Creator → Lansman içeriklerini üret
        │  Çıktı: content-calendar.md, social post'lar, email dizileri
        ▼
[2.4] Campaign Manager → Reklam kampanyası tasarla
        │  Çıktı: ad-campaigns.md, ad-creatives.md
        ▼
[2.5] Launch Commander → Lansman checklist'i oluştur
        │  Çıktı: launch-plan.md, launch-checklist.md
        ▼
[2.6] Orchestrator → Tüm planı kullanıcıya sun, onay al
        │
        ▼
[2.7] Launch Commander → Lansmanı başlat
           (Kullanıcıya adım adım yapılacakları ilet)
```

---

## Adım Detayları

### 2.1 — MVP Detaylarını Toplama
**Agent:** Orchestrator

```
MVP detaylarını alabilir miyim? İhtiyacım olanlar:

ZORUNLU:
• App/ürün adı
• App Store / Google Play linki (veya TestFlight / web URL'si)
• MVP'de hangi özellikler var? (kısaca liste)
• Hangi özellikler eksik? (ileride eklenecek)

OPSİYONEL (varsa):
• Bilinen bug'lar neler?
• Coder'ın eklemek istediği notlar var mı?
• Test kullanıcılarından gelen ilk izlenimler?
```

### 2.2 — Pazarlama Stratejisi
**Agent:** Strategy Analyst
**Girdi:** `prd-v1.md`, `pazara-giris-stratejisi.md` (varsa), MVP detayları

**Çıktı (`marketing-strategy.md`):**
```markdown
# Pazarlama Stratejisi: [Ürün] v1.0
## Hedef Kitle
- Primer segment: ...
- Sekonder segment: ...

## Konumlandırma
[1 cümle]

## Lansman Kanalları (öncelikli)
1. [kanal] — [neden, hedef]
2. ...

## Lansman Zamanlaması
- D-14: ...
- D-7: ...
- D-Day: ...
- D+7: ...

## Bütçe Planı
| Kalem | Bütçe | Beklenen Dönüş |
|-------|-------|---------------|
| Reklam | ₺xxx | [hedef] |
| ... | ... | ... |

## Başarı Metrikleri
| Metrik | 7 gün | 30 gün | 90 gün |
|--------|-------|--------|--------|
| İndirme | [x] | [x] | [x] |
| DAU | [x] | [x] | [x] |
| Gelir | [₺] | [₺] | [₺] |
```

### 2.3 — Lansman İçerikleri
**Agent:** Content Creator
**Paralel görevler (hepsi aynı anda yapılabilir):**

- `social_calendar.py` ile 30 günlük sosyal medya takvimi
- App Store / Google Play açıklaması (ASO optimize)
- Lansman email dizisi (email-launch template)
- Landing page kopyası (varsa web sitesi)
- Sosyal medya lansman post'ları
- Tanıtım videosu senaryosu (video skill)

**Çıktılar:**
- `content-calendar.md`
- `content/social-post-*.md`
- `content/email-launch.md`
- `content/aso-metni.md`

### 2.4 — Reklam Kampanyası
**Agent:** Campaign Manager
**Çıktılar:**
- `ad-campaigns.md` — platform seçimi, bütçe, kampanya yapısı
- `ad-creatives.md` — 3+ varyant (her platform için)

### 2.5 — Lansman Planı ve Checklist
**Agent:** Launch Commander
**Çıktılar:**
- `launch-plan.md` — lansman özeti, kanallar, takvim, metrik hedefleri
- `launch-checklist.md` — 8 haftalık detaylı checklist (template'ten doldurulur)

### 2.6 — Onay
**Agent:** Orchestrator

```
📋 LANSMA PAKETİ HAZIR

İşte lansman için hazırladıklarımız:
• Pazarlama stratejisi → [dosya]
• İçerik takvimi (30 gün) → [dosya]
• Reklam kampanyası → [dosya]
• Lansman planı → [dosya]

Toplam tahmini bütçe: ₺xxx

Onaylıyor musun? Lansmanı başlatalım mı?
```

### 2.7 — Lansman
**Agent:** Launch Commander
Lansman günü adım adım yapılacakları kullanıcıya iletir.

---

## Karar Noktaları

| Adım | Karar |
|------|-------|
| 2.6 | Lansman planını onayla / revize et |

---

## Çıktı Dosyaları

| Dosya | Üreten |
|-------|--------|
| `marketing-strategy.md` | Strategy Analyst |
| `content-calendar.md` | Content Creator |
| `content/social-post-*.md` | Content Creator |
| `content/email-launch.md` | Content Creator |
| `content/aso-metni.md` | Content Creator |
| `ad-campaigns.md` | Campaign Manager |
| `ad-creatives.md` | Campaign Manager |
| `launch-plan.md` | Launch Commander |
| `launch-checklist.md` | Launch Commander |

---

## Sonraki Pipeline

Lansmandan 2-4 hafta sonra → **Pipeline 3 (Feedback ve İyileştirme)** başlar. Veya kullanıcı "feedback toplamaya başlayalım" dediğinde.
