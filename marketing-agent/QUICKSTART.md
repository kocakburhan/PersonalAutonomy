# Marketing Agent Quickstart

5 dakikada ilk projeni başlat.

## 1. Gereksinimler

Bilgisayarında şunlar kurulu olmalı:
- **Node.js 18+** — App Store MCP için
- **Python 3.10+** — script'ler için

Yoksa coder'ından kurmasını iste.

## 2. Kurulum (coder yapacak)

```bash
# marketing-agent dizininde:

# MCP sunucularını kur
git clone https://github.com/appreply-co/mcp-appstore vendor/mcp-appstore
npm install --prefix vendor/mcp-appstore

# Python bağımlılıkları
pip install pytrends reportlab

# Sağlık kontrolü
.\scripts\healthcheck.ps1
```

Hepsi `OK` gösteriyorsa hazırsın.

## 3. İlk Projeni Başlat

OpenCode'da şunu yaz:

```
merhaba, yeni bir proje başlatmak istiyorum
```

Sistem seni karşılayacak ve şunları soracak:
1. Marketing deneyimin ne seviyede?
2. Ne tür ürün/işletme? (Mobil app / SaaS / Dükkan / ...)
3. Şu an hangi aşamadasın?

## 4. Hangi Pipeline'ı Seçmelisin?

| Durumun | Ne yazmalısın |
|---------|--------------|
| "Aklımda hiç fikir yok, ne yapabilirim?" | `fikir bul` |
| "Bir fikrim var, işe yarar mı?" | `fikrim var` |
| "MVP hazır, pazarlamaya başlamak istiyorum" | `mvp hazır` |
| "Ürünüm var, daha çok müşteri istiyorum" | `büyüt` |
| "Dükkanım var, internette görünmek istiyorum" | `işletmemi pazarla` |
| "Ne yapacağımı bilmiyorum" | `yardım` |

## 5. Nasıl İlerleyeceksin?

Sistem seni adım adım yönlendirecek. Sen sadece:
- Sana sorulan sorulara cevap ver
- Sana sunulan seçeneklerden birini seç
- "Devam et" veya "Şunu değiştir" de

Her şey otomatik dosyalanır. `sessions/` klasöründe tüm projelerin durur.

## 6. Takılırsan

Her an `yardım` yazabilirsin. Sistem sana bulunduğun aşamayı ve seçeneklerini hatırlatır.

## 7. Birden Fazla Proje

```
projelerim              → tüm projelerini listeler
X projesine geç         → o projeye döner
yeni proje başlat       → yeni proje oluşturur
```

## 8. Manuel Veri Girişi (MCP çalışmazsa)

App Store MCP bazen çalışmayabilir. Sistem sana otomatik olarak "manuel yapman gerekenler" listesi verecek. iPhone'undan App Store'u açıp istenen verileri topla, buraya yaz. Sistem analizi yapmaya devam edecek.

## Önemli Notlar

- Tüm iletişim Türkçedir
- Coder'a verilecek dosyalar (`coder-brief.md`) senin için hazırlanır, direkt ilet
- Sistem pazarlama stratejisi üretir, reklam bütçesini sen yönetirsin
- Her aşamada onayın alınır, izinsiz iş yapılmaz
