# Pipeline 1: Fikir Keşif ve Doğrulama (Idea Discovery)

**Zincirdeki yeri:** Zincir A (ilk adım) — sonrasında P5'e geçer.

**Ne zaman çalışır:** Kullanıcı "sıfırdan bir fikir bulmak istiyorum" dediğinde. Veya onboarding'de bu pipeline'ı seçtiğinde.

**Amaç:** Pazardaki boşlukları ve fırsatları tarayıp, doğrulanmış bir ürün fikri ve PRD'ye ulaşmak.

**Ön koşul:** `product-context.md` oluşturulmuş olmalı.

---

## Pipeline Akışı

```
Kullanıcı giriş yapar
        │
        ▼
[1.1] Orchestrator → İlgi alanı/sektör/ürün tipi sor
        │
        ▼
[1.2] Market Scout → Kaynakları tara, fırsat haritası çıkar
        │  Çıktı: firsat-haritasi.md
        ▼
[1.3] Orchestrator → Fırsatları kullanıcıya sun, kategori seçtir
        │  Kullanıcı: "X kategorisini analiz et" (veya "vazgeç")
        ▼
[1.4] Market Scout → Seçilen kategoride derin analiz
        │  Çıktı: kategori-analizi.md
        ▼
[1.5] Strategy Analyst → Rekabet analizi, boşluk tespiti
        │  Çıktı: strateji-analizi.md
        ▼
[1.6] Orchestrator → Boşlukları kullanıcıya sun, fırsat seçtir
        │  Kullanıcı: bir boşluk/fırsat seçer (veya "diğer kategoriye dön")
        ▼
[1.7] Product Architect → Seçilen fırsattan fikir üret
        │  Çıktı: idea-brief.md
        ▼
[1.8] Orchestrator → Fikri kullanıcıyla tartış, şekillendir
        │  Kullanıcı: fikri onaylar / revize ister / vazgeçer
        ▼
[1.9] Product Architect → PRD yaz
        │  Çıktı: prd-v1.md
        ▼
[1.10] Orchestrator → PRD'yi onaylat, coder brief'i hazırla
           Çıktı: coder-brief.md
           Sonra: "P5 tamamlandı. Coder'a ilet. MVP hazır olunca P2'ye başlayalım."
```

---

## Adım Detayları

### 1.1 — İlgi Alanı ve Ürün Tipi Belirleme
**Agent:** Orchestrator
**Kullanıcıya sorulan:**
1. Hangi sektörle ilgileniyorsun? (açık uçlu veya önerili liste)
2. Ne tür ürün? (Mobil app / SaaS / E-ticaret / ...)
3. Özel bir ilgi alanın var mı? (spor, sağlık, eğitim, finans...)

**Not:** Kullanıcı "bilmiyorum" derse tüm popüler kategorileri tara.

### 1.2 — Fırsat Haritası
**Agent:** Market Scout
**Eylem:** Ürün tipine uygun tüm kaynakları tara.
- App Store / Google Play (mobil app)
- G2 / Capterra / Reddit (SaaS)
- Google Maps (fiziksel işletme)
- vb.

**Not:** Kullanıcı sektör belirtmişse sadece o sektörü tara. Belirtmemişse tüm kategorileri tara ve en hızlı büyüyenleri sırala.

### 1.3 — Kategori Seçimi
**Agent:** Orchestrator
**Kullanıcıya sunulan:** En az 3 yükselen kategori, her biri için:
- Kaç app/rakip var
- Büyüme oranı
- Ortalama gelir (varsa)
- Öne çıkan bir örnek

**Kullanıcı kararı:** "X kategorisini derinlemesine analiz et" veya "vazgeç, başka kaynak tara"

### 1.4 — Derin Kategori Analizi
**Agent:** Market Scout
**Süre:** Kategorideki rakip sayısına bağlı. En az 3, en çok 10 rakip analiz edilir.

### 1.5 — Stratejik Analiz
**Agent:** Strategy Analyst
**Girdi:** `kategori-analizi.md`
**Çıktı:** SWOT, pozisyon haritası, boşluk listesi

### 1.6 — Fırsat Seçimi
**Agent:** Orchestrator
**Kullanıcıya sunulan:** En az 3 somut fırsat alanı (boşluk). Her biri için:
- Hangi rakiplerin eksikliği
- Kullanıcıların neyden şikayet ettiği
- Tahmini pazar büyüklüğü

### 1.7 — Fikir Üretimi
**Agent:** Product Architect
**Girdi:** Seçilen fırsat alanı
**Çıktı:** `idea-brief.md` — problem, çözüm, hedef kitle, MVP kapsamı, gelir modeli

### 1.8 — Fikir Tartışması
**Agent:** Orchestrator
**Kullanıcıyla yapılan:** Fikrin artıları/eksileri, riskler, alternatif açılar, hedef kitle netleştirme. Kullanıcı fikri şekillendirir.

### 1.9 — PRD Yazımı
**Agent:** Product Architect
**Girdi:** Onaylanmış `idea-brief.md` + tartışma notları
**Çıktı:** `prd-v1.md`

### 1.10 — Onay ve Coder Brief
**Agent:** Orchestrator
**Kullanıcıya sorulan:** "PRD'yi onaylıyor musun?"
**Çıktı:** `coder-brief.md`

---

## Karar Noktaları

| Adım | Karar | Seçenekler |
|------|-------|-----------|
| 1.3 | Kategori seçimi | "X'i analiz et" / "Başka öner" / "Vazgeç" |
| 1.6 | Fırsat seçimi | "X fırsatından fikir üret" / "Başka kategoriye dön" / "Vazgeç" |
| 1.8 | Fikir onayı | "Devam et, PRD'ye dönüştür" / "Şu kısmı değiştir" / "Vazgeç" |
| 1.10 | PRD onayı | "Onaylıyorum, coder'a ilet" / "Revizyon isterim" |

---

## Çıktı Dosyaları

| Dosya | Üreten | Açıklama |
|-------|--------|----------|
| `firsat-haritasi.md` | Market Scout | Tüm kategoriler, büyüme oranları |
| `kategori-analizi.md` | Market Scout | Seçilen kategorideki rakip profilleri |
| `strateji-analizi.md` | Strategy Analyst | SWOT, boşluklar, fırsat alanları |
| `idea-brief.md` | Product Architect | Detaylandırılmış fikir |
| `prd-v1.md` | Product Architect | Tam PRD |
| `coder-brief.md` | Orchestrator | Coder'a iletilecek özet |

---

## Sonraki Pipeline

Pipeline 1 tamamlandığında orchestrator otomatik olarak şu mesajı verir:

```
PRD ve coder brief hazır. Bunları coder'a ilet.

Coder MVP'yi geliştirirken ben sana şu konularda yardımcı olabilirim:
• Sosyal medya hesaplarını şimdiden açmak
• "Coming soon" sayfası hazırlamak
• E-posta listesi oluşturma stratejisi

MVP hazır olduğunda bana haber ver, Pipeline 2 (MVP Lansman) ile devam edelim.
```

Coder MVP'yi teslim ettiğinde → **Pipeline 2 (MVP Lansman)** başlar.
