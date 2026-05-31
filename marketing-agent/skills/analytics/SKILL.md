---
name: analytics
description: Analitik kurulumu ve event tracking planlaması. GA4, Mixpanel, Amplitude, Meta Pixel.
metadata:
  version: 2.0.0
  source: coreyhaines31/marketingskills
---

# Analitik Kurulumu

Analitik ve ölçümleme uzmanı. GA4, Mixpanel, Amplitude, Meta Pixel için event tracking stratejisi.

## Başlamadan Önce

1. **product-marketing** context'ini kontrol et
2. Şunları anla:
   - İş modeli (SaaS, e-ticaret, marketplace)
   - Dönüşüm aksiyonu ne?
   - Mevcut analitik kurulumu var mı?
   - Hangi araçlar kullanılacak?

## Event Tracking Stratejisi

### Kritik Event'ler (SaaS örneği)

| Kategori | Event | Neden Önemli |
|----------|-------|-------------|
| **Edinme** | page_view, signup_started, signup_completed | Kanal verimliliği |
| **Aktivasyon** | onboarding_step_1/2/3, first_project_created | Aha moment |
| **Etkileşim** | feature_used, invite_team_member, dashboard_view | Ürün kullanımı |
| **Gelir** | trial_started, upgrade_to_paid, plan_changed | Gelir takibi |
| **Kayıp** | subscription_cancelled, account_deactivated | Churn analizi |

### Event Parametreleri
Her event için:
- **Plan:** free / pro / enterprise
- **Kaynak:** organic / ads / referral / email
- **Cihaz:** desktop / mobile / tablet
- **Özellik:** (feature-specific)

## Araç Seçimi

| Araç | Ne İçin | Alternatif |
|------|---------|------------|
| GA4 | Web analitiği, trafik kaynağı | Plausible, Fathom |
| Mixpanel | Ürün analitiği, funnel | Amplitude, PostHog |
| Meta Pixel | Meta reklam dönüşüm takibi | — |
| LinkedIn Insight Tag | LinkedIn reklam takibi | — |
| Segment | CDP, event yönlendirme | RudderStack |
| Hotjar | Oturum kaydı, heatmap | Microsoft Clarity |

## Dashboard Önerileri

### Haftalık SaaS Dashboard'u
- Yeni kayıt sayısı
- Aktivasyon oranı (%)
- Haftalık aktif kullanıcı
- Trial → Paid dönüşüm oranı
- Churn oranı
- MRR (aylık yinelenen gelir)

### Aylık Pazarlama Dashboard'u
- Kanal bazlı trafik
- Kanal bazlı dönüşüm
- CAC (müşteri edinme maliyeti)
- LTV (müşteri yaşam boyu değer)
- LTV/CAC oranı
- ROAS (reklam harcaması getirisi)

## Uygulama Kontrol Listesi

- [ ] GA4 property oluşturuldu
- [ ] Google Tag Manager kuruldu (önerilir)
- [ ] Kritik event'ler tanımlandı
- [ ] Conversion event'leri işaretlendi
- [ ] Meta Pixel kuruldu
- [ ] LinkedIn Insight Tag kuruldu
- [ ] UTM parametre standardı belirlendi
- [ ] Dashboard oluşturuldu
- [ ] Anomali uyarıları kuruldu
