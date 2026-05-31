# Pipeline 3: Feedback ve İyileştirme (Feedback & Improvement)

**Zincirdeki yeri:** Zincir A, B ve C (P2 veya P9'dan sonra). Döngüsel — P3 → P5 veya P3 → P9 şeklinde tekrarlanır.

**Ne zaman çalışır:**
- Lansmandan 2-4 hafta sonra
- Kullanıcı "feedback toplayalım" dediğinde
- Her iyileştirme döngüsünde

**Amaç:** Kullanıcı geri bildirimlerini ve ürün metriklerini analiz edip, iyileştirme alanlarını belirlemek ve coder için güncellenmiş PRD üretmek.

**Ön koşul:** Ürün yayında olmalı, kullanıcı etkileşimi başlamış olmalı.

---

## Pipeline Akışı

```
Orchestrator: "Feedback toplama zamanı"
        │
        ▼
[3.1] Orchestrator → Kullanıcıdan temel metrikleri iste
        │  Sorular: indirme, yorum, gelir, ziyaretçi, sosyal medya etkileşimi
        ▼
[3.2] Market Scout → Kullanıcı yorumlarını analiz et
        │  Kaynaklar: App Store, Google Play, Google Maps, forumlar, sosyal medya
        │  Çıktı: yorum-analizi.md
        ▼
[3.3] Analytics Master → Metrik analizi yap
        │  Çıktı: analytics-raporu.md
        ▼
[3.4] Strategy Analyst → İyileştirme alanlarını belirle
        │  Çıktı: iyilestirme-onerileri.md
        ▼
[3.5] Orchestrator → Bulguları kullanıcıya sun, öncelikleri sor
        │
        ▼
[3.6] Product Architect → Güncellenmiş PRD yaz
        │  Çıktı: prd-v2.md
        ▼
[3.7] Orchestrator → Coder için güncellenmiş brief hazırla
           Çıktı: coder-brief-v2.md
```

---

## Adım Detayları

### 3.1 — Metrik Toplama
**Agent:** Orchestrator

```
📊 Lansman sonrası verileri toplama zamanı!

Bana şu verileri iletebilir misin?

App Store / Google Play'den:
• Toplam indirme sayısı
• Günlük aktif kullanıcı (varsa)
• Ortalama puan ve yorum sayısı
• Son 30 gündeki gelir (varsa)

Web sitesinden (varsa):
• Ziyaretçi sayısı
• Dönüşüm oranı

Sosyal medyadan:
• Gönderi etkileşimleri
• Takipçi sayısı

Kullanıcılardan:
• Gelen e-postalar/mesajlar (özet)
• Test kullanıcılarının sözlü geri bildirimleri

(Bu verilerin bir kısmını coder'dan da isteyebilirsin — onun erişimi olan dashboard'lar olabilir)
```

### 3.2 — Kullanıcı Yorumu Analizi
**Agent:** Market Scout
**Eylem:**
- App Store/Google Play yorumlarını çek
- Google Maps/GBP yorumlarını çek (fiziksel işletme)
- Sosyal medya bahislerini tara
- Forum/şikayet sitesi yorumlarını kontrol et

**Çıktı (`yorum-analizi.md`):**
```markdown
# Kullanıcı Yorum Analizi: [Ürün]
- Dönem: [tarih aralığı]
- Toplam yorum: [sayı]
- Ortalama puan: [x/5]
- Olumlu oranı: [%] | Olumsuz oranı: [%]

## Olumlu Yorumlardan Pattern'lar
1. [pattern] — [kaç yorumda geçiyor]

## Olumsuz Yorumlardan Pattern'lar
1. [pattern] — [kaç yorumda geçiyor]

## En Sık Talep Edilen Özellikler
1. [özellik] — [kaç kez istendi]

## Customer Language Mining
Kullanıcıların ürünü tanımlarken kullandığı ifadeler:
- ...
```

### 3.3 — Metrik Analizi
**Agent:** Analytics Master
**Girdi:** Kullanıcıdan alınan metrik verileri
**Çıktı (`analytics-raporu.md`):**
- Kritik metrikler tablosu (değer vs hedef)
- Trend analizi
- Alarm durumları
- Büyüme/düşüş yorumları

### 3.4 — İyileştirme Önerileri
**Agent:** Strategy Analyst
**Girdi:** `yorum-analizi.md` + `analytics-raporu.md`
**Çıktı (`iyilestirme-onerileri.md`):**
- 3 seviyeli önceliklendirme:
  - 🔴 Kritik (hemen yapılmalı)
  - 🟡 Önemli (bu ay yapılmalı)
  - 🟢 Güzel olur (zaman kalırsa)

### 3.5 — Kullanıcıya Sunum
**Agent:** Orchestrator

```
📈 FEEDBACK ANALİZ RAPORU

İlgi var mı?
✅ / ⚠️ / ❌ [durum değerlendirmesi]

Öne çıkan bulgular:
❤️ Kullanıcıların sevdiği: [ilk 3]
💔 Kullanıcıların şikayet ettiği: [ilk 3]
📊 Metriklerde alarm: [varsa]

Önerilen iyileştirmeler:
🔴 Kritik: ...
🟡 Önemli: ...
🟢 Güzel olur: ...

Hangi önceliklerle ilerleyelim?
A) Sadece kritik olanları yapalım
B) Kritik + önemlileri yapalım
C) Hepsini yapalım
D) Kendi seçtiklerimi belirteyim
```

### 3.6 — Güncellenmiş PRD
**Agent:** Product Architect
**Girdi:** `iyilestirme-onerileri.md` + kullanıcının öncelik kararı
**Çıktı:** `prd-v2.md`

### 3.7 — Coder Brief (v2)
**Agent:** Orchestrator
**Çıktı:** `coder-brief-v2.md`

---

## Karar Noktaları

| Adım | Karar |
|------|-------|
| 3.5 | İyileştirme önceliklerini seç |

---

## Çıktı Dosyaları

| Dosya | Üreten |
|-------|--------|
| `yorum-analizi.md` | Market Scout |
| `analytics-raporu.md` | Analytics Master |
| `iyilestirme-onerileri.md` | Strategy Analyst |
| `prd-v2.md` | Product Architect |
| `coder-brief-v2.md` | Orchestrator |

---

## Sonraki Pipeline

Coder iyileştirmeleri yapar → ürün güncellenir → istenirse tekrar **Pipeline 3** çalıştırılır (döngü).

Veya traction varsa → **Pipeline 4 (Büyüme Motoru)** başlatılır.
