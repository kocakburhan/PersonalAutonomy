# Pipeline 5: Fikirden PRD'ye (Idea to PRD)

**Zincirdeki yeri:** Zincir A (P1'den sonra) veya Zincir B (başlangıç noktası).

**Ne zaman çalışır:** Kullanıcının aklında zaten bir fikir varsa ve bunu doğrulatıp PRD'ye dönüştürmek istiyorsa.

**Amaç:** Eldeki fikri pazar verileriyle doğrulamak, "devam et" kararı çıkarsa tam PRD ve coder brief üretmek.

**Ön koşul:** Kullanıcının bir fikri olmalı. `product-context.md` oluşturulmuş olmalı.

---

## Pipeline Akışı

```
Kullanıcı: "Elimde bir fikir var"
        │
        ▼
[5.1] Orchestrator → Kullanıcıdan fikri ve ürün tipini al
        │
        ▼
[5.2] Market Scout → Pazar/rakip/trend verisi topla
        │  Çıktı: pazar-arastirmasi.md
        ▼
[5.3] Strategy Analyst → SWOT, rekabet avantajı, risk, fiyatlandırma ön analizi
        │  Çıktı: fikir-dogrulama.md
        ▼
[5.4] Orchestrator → Karar noktası: DEVAM ET / PİVOT ET / VAZGEÇ
        │
        ├── "devam et" →
        │       ▼
        │  [5.5] Product Architect → Fikri detaylandır, persona, değer önerisi, MVP kapsamı
        │       │  Çıktı: idea-brief.md
        │       ▼
        │  [5.6] Orchestrator → Kullanıcıyla tartış, şekillendir
        │       │
        │       ▼
        │  [5.7] Product Architect → Tam PRD yaz
        │       │  Çıktı: prd-v1.md
        │       ▼
        │  [5.8] Strategy Analyst → Pazara giriş stratejisi
        │       │  Çıktı: pazara-giris-stratejisi.md
        │       ▼
        │  [5.9] Orchestrator → PRD onayı, coder brief hazırla
        │          Çıktı: coder-brief.md
        │
        ├── "pivot et" → Kullanıcı fikri günceller → [5.1]'e dön
        │
        └── "vazgeç" → Oturum sonu, fikir arşivlenir
```

---

## Adım Detayları

### 5.1 — Fikir Toplama
**Agent:** Orchestrator
**Kullanıcıya sorulan:**
1. Fikrini 3-5 cümleyle anlatır mısın?
2. Bu fikir nereden çıktı? (kendi ihtiyacın mı, gözlemlediğin bir sorun mu, bir rakibin eksiği mi?)
3. Hedef kitlen kim? (tahmini)
4. Ürün tipi ne? (mobil app / SaaS / fiziksel işletme / e-ticaret / karma / içerik / hizmet)
5. Rakip olarak gördüğün ürünler var mı? Varsa hangileri?

### 5.2 — Pazar Araştırması
**Agent:** Market Scout
**Eylem:** Ürün tipine göre doğru kaynaklardan veri topla.
- Rakip ürünlerin sayfalarını tara
- Kullanıcı yorumlarını analiz et
- Pazar büyüklüğü ve trend verisi topla
- Google Trends'te ilgili anahtar kelimeleri kontrol et

**Çıktı formatı (`pazar-arastirmasi.md`):**
```markdown
# Pazar Araştırması: [Fikir]
## Pazar Büyüklüğü
- TAM (Total Addressable Market): [tahmin]
- SAM (Serviceable Addressable Market): [tahmin]
- SOM (Serviceable Obtainable Market): [tahmin]

## Rakip Listesi
| Rakip | Tip | Güçlü Yan | Zayıf Yan | Pazar Payı |
|-------|-----|----------|----------|-----------|
| ... | ... | ... | ... | ... |

## Trend Verisi
- Google Trends: [yükselişte/düşüşte/durağan]
- Sektör raporları: [özet]

## Kullanıcı Yorumlarından Çıkanlar
- En sık şikayet: ...
- En sık övgü: ...
```

### 5.3 — Fikir Doğrulama
**Agent:** Strategy Analyst
**Girdi:** `pazar-arastirmasi.md` + kullanıcının fikri
**Çıktı formatı (`fikir-dogrulama.md`):**
```markdown
# Fikir Doğrulama: [Fikir]
## SWOT
[tablo]

## Değerlendirme Kriterleri
| Kriter | Puan (1-10) | Açıklama |
|--------|------------|----------|
| Pazar büyüklüğü | [x] | ... |
| Rekabet yoğunluğu | [x] | ... |
| Giriş bariyeri | [x] | ... |
| Farklılaşma potansiyeli | [x] | ... |
| Gelir potansiyeli | [x] | ... |
| **Toplam** | **[x]/50** | |

## Risk Değerlendirmesi
| Risk | Olasılık | Etki | Mitigasyon |
|------|---------|------|-----------|
| ... | Düşük/Orta/Yüksek | Düşük/Orta/Yüksek | ... |

## Fiyatlandırma Ön Analizi
- Önerilen model: ...
- Tahmini ARPU: [₺]
```

### 5.4 — Karar Noktası
**Agent:** Orchestrator
**Kullanıcıya sunulan seçenekler:**

```
📊 DOĞRULAMA SONUCU

Puan: [x]/50 — [yorum]

Seçenekler:
✅ DEVAM ET — Fikir pazar verileriyle uyumlu, PRD aşamasına geçelim
🔄 PİVOT ET — Şu yönde değiştirirsek daha iyi olur: [öneri]
❌ VAZGEÇ — Pazar yeterince büyük değil / rekabet çok yoğun / ...

Hangisini seçersin?
```

### 5.5 — Fikir Detaylandırma (Idea Brief)
**Agent:** Product Architect
**Sadece "devam et" kararı verilirse çalışır.**
**Çıktı:** `idea-brief.md`

### 5.6 — Fikir Tartışması
**Agent:** Orchestrator
**Kullanıcıyla:** Fikrin detayları tartışılır, eksik/fazla yönler belirlenir. Hedef kitle netleştirilir.

### 5.7 — PRD Yazımı
**Agent:** Product Architect
**Çıktı:** `prd-v1.md`

### 5.8 — Pazara Giriş Stratejisi
**Agent:** Strategy Analyst
**Çıktı:** `pazara-giris-stratejisi.md`

### 5.9 — Onay ve Coder Brief
**Agent:** Orchestrator
**Çıktı:** `coder-brief.md`

---

## P1 ve P5 Arasındaki Fark

| Özellik | P1 (Fikir Keşif) | P5 (Fikirden PRD) |
|---------|-----------------|-------------------|
| Başlangıç noktası | Fikir yok | Fikir var |
| Keşif aşaması | Var (1.2-1.6) | Yok |
| Doğrulama | Fikrin parçası | Ayrı adım (5.2-5.4) |
| PRD yazımı | Var | Var |
| Coder brief | Var | Var |
| Pazar giriş stratejisi | Ayrıca P5'te | Var (5.8) |

**Not:** P1'den gelen kullanıcı zaten doğrulama yaptığı için P1 tamamlandığında direkt PRD'ye geçilir. P5 bağımsız bir giriş noktasıdır.

---

## Çıktı Dosyaları

| Dosya | Üreten | Açıklama |
|-------|--------|----------|
| `pazar-arastirmasi.md` | Market Scout | Rakip, trend, yorum verisi |
| `fikir-dogrulama.md` | Strategy Analyst | SWOT, skor, risk, fiyat ön analizi |
| `idea-brief.md` | Product Architect | Detaylandırılmış fikir |
| `prd-v1.md` | Product Architect | Tam PRD |
| `pazara-giris-stratejisi.md` | Strategy Analyst | İlk hedef, konumlandırma, fiyat |
| `coder-brief.md` | Orchestrator | Coder'a özet brief |

---

## Sonraki Pipeline

"Devam et" → PRD onayı → **Pipeline 2 (MVP Lansman)** — coder MVP'yi teslim ettiğinde.
