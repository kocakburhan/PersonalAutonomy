# Pipeline 8: Outbound Satış (Outbound Sales)

**Zincirdeki yeri:** Zincir D (P4'ü destekler) veya bağımsız giriş noktası.

**Ne zaman çalışır:** B2B ürün için doğrudan satış/prospecting gerektiğinde.

**Amaç:** İdeal müşteri profili tanımlayıp, prospect listesi oluşturup, cold email dizisiyle outreach yapmak.

**Ön koşul:** Ürün B2B olmalı. `product-context.md` mevcut olmalı.

---

## Pipeline Akışı

```
Kullanıcı: "Müşteri bulalım" / "Outbound satış yapalım"
        │
        ▼
[8.1] Outreach Specialist → ICP tanımı ve prospect listesi
        │  Çıktı: prospect-list.md (veya .csv)
        ▼
[8.2] Outreach Specialist → E-posta dizisi tasarla
        │  Çıktı: email-sequence.md
        ▼
[8.3] Outreach Specialist → A/B test varyantları
        │  Çıktı: email-variants.md
        ▼
[8.4] Analytics Master → Cevap oranı takibi
           Çıktı: outreach-analiz.md
```

---

## Adım Detayları

### 8.1 — Prospect Listesi
**Agent:** Outreach Specialist
**Skill:** `prospecting`

**Çıktı (`prospect-list.md`):**
```markdown
# Prospect Listesi: [Ürün]
- ICP Tanımı:
  - Şirket büyüklüğü: [çalışan sayısı]
  - Sektör: [sektör]
  - Karar verici: [rol/unvan]
  - Trigger: [hangi olay üzerine ihtiyaç duyar]
  - Pain point: [hangi sorunu çözer]

## Prospect'ler
| # | Şirket | Karar Verici | Rol | LinkedIn | Email | Sıcaklık | Not |
|---|--------|-------------|-----|----------|-------|---------|-----|
| 1 | ... | ... | ... | [link] | ... | 🔥 | ... |
```

### 8.2 — Email Dizisi
**Agent:** Outreach Specialist
**Skill:** `cold-email`, `emails`

**Çıktı (`email-sequence.md`):**
- 3-5 email'lik dizi
- Her email için: subject line, gövde, CTA, gönderim günü
- Son email "breakup" formatında
- `cold-email` skill'inden kurallar: 2-4 kelime subject, lowercase, kişiselleştirme

### 8.3 — A/B Test Varyantları
**Agent:** Outreach Specialist
**Çıktı (`email-variants.md`):**
```markdown
# Email A/B Test Planı
| Test | Varyant A | Varyant B | Metrik | Hedef |
|------|----------|----------|--------|-------|
| Subject line | [kısa/direkt] | [merak uyandıran] | Açılma oranı | >%40 |
| CTA | [tekli] | [ikili seçenek] | Tıklama oranı | >%10 |
```

### 8.4 — Performans Takibi
**Agent:** Analytics Master
**Çıktı (`outreach-analiz.md`):**
```markdown
# Outbound Performans: [dönem]
| Metrik | Değer | Hedef | Durum |
|--------|-------|-------|-------|
| Gönderilen email | [x] | - | - |
| Açılma oranı | [%] | >%40 | |
| Cevap oranı | [%] | >%10 | |
| Toplantı dönüşümü | [%] | >%5 | |
```

---

## Çıktı Dosyaları

| Dosya | Üreten |
|-------|--------|
| `prospect-list.md` | Outreach Specialist |
| `email-sequence.md` | Outreach Specialist |
| `email-variants.md` | Outreach Specialist |
| `outreach-analiz.md` | Analytics Master |

---

## Sonraki Adım

Pipeline 8 bağımsız çalışır. Prospect'lerden dönüş alındıkça liste güncellenir, yeni prospect'ler eklenir.
