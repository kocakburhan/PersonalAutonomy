# Pipeline 4: Büyüme Motoru (Growth Engine)

**Zincirdeki yeri:** Zincir A ve D (P3'ten sonra, traction kazanınca).

**Ne zaman çalışır:** Ürün traction kazandığında, düzenli kullanıcı akışı olduğunda, gelir oluşmaya başladığında.

**Amaç:** Büyüme deneyleri tasarlayıp uygulayarak kullanıcı sayısını, retention'ı ve geliri artırmak.

**Ön koşul:** Ürün canlı, kullanıcı ve metrik verisi mevcut.

---

## Pipeline Akışı

```
Orchestrator: "Büyüme zamanı"
        │
        ▼
[4.1] Analytics Master → Mevcut metrikleri analiz et
        │  Çıktı: buyume-analizi.md
        ▼
[4.2] Growth Hacker → Büyüme deneyleri tasarla
        │  Çıktı: buyume-deneyleri.md
        ▼
[4.3] Orchestrator → Deneyleri kullanıcıya sun, seçtir
        │
        ▼
[4.4] Growth Hacker + Campaign Manager → Deneyleri uygula
        │  (Referans programı, churn önleme, topluluk, reklam)
        ▼
[4.5] Analytics Master → Deney sonuçlarını raporla
        │  Çıktı: deney-sonuclari.md
        ▼
[4.6] Orchestrator → Döngü kararı:
        ├── Başarılı → ölçekle, yeni deney tasarla
        └── Başarısız → analiz et, yeni deney tasarla
```

---

## Adım Detayları

### 4.1 — Büyüme Analizi
**Agent:** Analytics Master
**Girdi:** Kullanıcıdan alınan güncel metrikler
**Çıktı (`buyume-analizi.md`):**

```markdown
# Büyüme Analizi: [Ürün]
## AARRR Metrikleri
| Aşama | Metrik | Değer | Benchmark | Durum |
|-------|--------|-------|-----------|-------|
| Acquisition | İndirme/ziyaret | [x] | [x] | |
| Activation | Kayıt tamamlama | [%] | [%] | |
| Retention | D7/D30 | [%] | [%] | |
| Revenue | ARPU | [₺] | [₺] | |
| Referral | Viral katsayı | [x] | [x] | |

## Büyüme Fırsatları
[En düşük metrikten en yükseğe fırsat alanları]
```

### 4.2 — Büyüme Deneyleri
**Agent:** Growth Hacker
**Çıktı (`buyume-deneyleri.md`):**
- Her deney için: hipotez, etki alanı, uygulama, süre, başarı kriteri, efor
- ICE skorlaması (Impact, Confidence, Ease)

### 4.3 — Deney Seçimi
**Agent:** Orchestrator
**Kullanıcıya sunulan seçenekler:** En az 3 deney, ICE skoruyla birlikte. Kullanıcı hangilerini uygulayacağını seçer.

### 4.4 — Deney Uygulama
**Agent:** Growth Hacker + Campaign Manager (paralel)
**Uygulanabilecek deney tipleri:**
- Referans programı (`referrals` skill)
- Churn önleme kampanyası (`churn-prevention` skill)
- Topluluk inşası (`community-marketing` skill)
- Paywall/upgrade CRO (`paywalls` skill)
- Reklam optimizasyonu (`ads` skill)
- Yaratıcı büyüme fikirleri (`marketing-ideas` skill)

### 4.5 — Sonuç Raporu
**Agent:** Analytics Master
**Çıktı (`deney-sonuclari.md`):**
```markdown
# Deney Sonuçları: [Ürün]
| Deney | Hipotez | Süre | Sonuç | Başarı? | Öğrenilen |
|-------|---------|------|-------|---------|----------|
| ... | ... | [gün] | [metrik] | ✅/❌ | ... |
```

### 4.6 — Döngü Kararı
**Agent:** Orchestrator
- Başarılı deneyler → ölçeklendir, kalıcı hale getir
- Başarısız deneyler → neden analizi yap, pivot et
- Yeni deneyler tasarla → 4.2'ye dön

---

## Çıktı Dosyaları

| Dosya | Üreten |
|-------|--------|
| `buyume-analizi.md` | Analytics Master |
| `buyume-deneyleri.md` | Growth Hacker |
| `deney-sonuclari.md` | Analytics Master |

---

## Sonraki Adım

Pipeline 4 döngüseldir. Sürekli çalışır. Gerekirse **Pipeline 6 (Rakip Saldırı)** veya **Pipeline 8 (Outbound Satış)** ile desteklenir.
