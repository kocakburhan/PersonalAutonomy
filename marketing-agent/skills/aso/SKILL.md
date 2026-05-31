---
name: aso
description: App Store ve Google Play için uygulama mağazası optimizasyonu.
metadata:
  version: 2.0.0
  source: coreyhaines31/marketingskills
---

# ASO (App Store Optimizasyonu)

Mobil uygulama mağazası optimizasyon uzmanı. App Store ve Google Play'de sıralama yükseltme.

## Optimizasyon Alanları

### 1. Uygulama Adı ve Alt Başlık
- App Store: 30 karakter (ad) + 30 karakter (alt başlık)
- Google Play: 50 karakter (ad) + 80 karakter (kısa açıklama)
- Ana anahtar kelimeyi ada ekle
- Örnek: "ProjectFlow: Proje Yönetimi & Ekip İletişimi"

### 2. Anahtar Kelimeler
- App Store: 100 karakter keyword alanı
- Google Play: Açıklamada doğal olarak geçmeli
- Rakip analizi: Rakipler hangi kelimeleri kullanıyor?
- Uzun kuyruklu (long-tail) fırsatları ara

### 3. Açıklama
- İlk 3 satır en kritik — arama sonuçlarında görünen kısım
- Değer önerisi hemen başta
- Fayda odaklı, özellik listesi değil
- Sosyal kanıt: ödüller, kullanıcı sayısı, puan

### 4. Görsel Asset'ler
- **Simge (Icon):** Basit, tanınabilir, renk kontrastı yüksek
- **Ekran görüntüleri:** Fayda göster, sadece arayüz değil
  - App Store: 10 adede kadar
  - Google Play: 8 adede kadar
- **Öne çıkan görsel (Feature Graphic):** Google Play için zorunlu
- **Video:** App Store 30 sn, Google Play 30 sn-2 dk

### 5. Puan ve Yorumlar
- Hedef: 4+ yıldız, en az 50 yorum
- Her güncellemede yorum iste
- Negatif yorumlara hızlı ve yapıcı cevap ver
- iOS: SKStoreReviewController API ile uygulama içi yorum iste

## Sıralama Faktörleri

| Faktör | App Store | Google Play |
|--------|:---------:|:-----------:|
| Uygulama adı | Yüksek | Yüksek |
| Anahtar kelimeler | Yüksek | Orta |
| İndirme sayısı | Yüksek | Yüksek |
| Puan ve yorum | Orta | Yüksek |
| İndirme hızı | Yüksek | Orta |
| Güncelleme sıklığı | Orta | Orta |
| Etkileşim (açılma) | Düşük | Yüksek |

## ASO Denetim Adımları

1. Mevcut sıralamayı kontrol et (App Store Connect, Google Play Console)
2. Rakiplerin sıralandığı kelimeleri araştır
3. Başlık, alt başlık, açıklamayı optimize et
4. Görselleri güncelle
5. Yorum stratejisi uygula
6. A/B test (Google Play listing experiments)
7. 2 hafta sonra tekrar ölç
