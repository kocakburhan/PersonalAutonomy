---
name: churn-prevention
description: Müşteri terk önleme — iptal akışı, save offer, ödeme kurtarma, reaktivasyon.
metadata:
  version: 2.0.0
  source: coreyhaines31/marketingskills
---

# Churn Önleme

Müşteri tutma uzmanı. Amaç: müşteri kaybını azaltmak, iptalleri kurtarmak, pasif kullanıcıları yeniden aktive etmek.

## Churn Türleri

| Tür | Neden | Çözüm |
|-----|-------|-------|
| Aktif iptal | Kullanıcı bilinçli iptal etti | Save offer, feedback |
| Pasif churn | Değeri görmedi, unuttu | Re-engagement email |
| Ödeme churn'u | Kredi kartı reddedildi | Dunning (ödeme kurtarma) |
| Büyüme churn'u | Kullanıcı büyüdü, ürün küçük kaldı | Enterprise plan |

## İptal Akışı Tasarımı (Save Offer)

### Kademeli Save Offer Stratejisi

1. **İptal butonuna tıklandı:**
   - Exit survey: "Neden iptal ediyorsun?"
   - En sık sebebe göre itiraz cevabı göster

2. **Birinci save offer:**
   - "Hesabını 1 ay ücretsiz dondurabilirsin."
   - Düşük taahhüt, veri kaybı yok

3. **İkinci save offer:**
   - "3 ay %50 indirimli devam et."
   - Fiyat itirazı için

4. **Son aşama:**
   - "Hesabın donduruldu. 30 gün içinde geri dönebilirsin."
   - Veriyi silme, kapıyı açık bırak

## Ödeme Kurtarma (Dunning)

Kredi kartı reddedilince:
- **Gün 0:** Hemen bildir
- **Gün 3:** Hatırlatma
- **Gün 7:** Son uyarı
- **Gün 14:** Hesabı dondur (iptal etme)
- Her adımda "Kartını güncelle" butonu

## Pasif Kullanıcı Reaktivasyonu

### Tetikleyiciler
- 14 gün giriş yapmama
- 30 gün ana özelliği kullanmama
- Aktivasyonu tamamlamama

### Re-engagement Email Sequence
1. **Gün 14:** "Seni özledik" + yeni özellik
2. **Gün 21:** Kullanıcının kaçırdığı değer
3. **Gün 30:** Özel teklif / destek teklifi

## Erken Uyarı Sinyalleri

| Sinyal | Aksiyon |
|--------|---------|
| Kullanım sıklığı düşüyor | Proaktif destek ulaşsın |
| Destek ticket'ı arttı | Sorunu çöz, takip et |
| NPS düşük | Birebir görüşme |
| Feature kullanımı azalıyor | Eğitim email'i |
| Ekip küçülüyor (B2B) | Fiyatlandırma esnekliği |

## Churn Metrikleri

| Metrik | Hesaplama |
|--------|-----------|
| Aylık churn oranı | İptal eden / Ay başı müşteri |
| Net revenue churn | (Kayıp MRR - Genişleme MRR) / Başlangıç MRR |
| Kurtarma oranı | Kurtarılan iptal / Toplam iptal girişimi |
| LTV | ARPU / Churn oranı |
