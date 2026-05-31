# Repo Analizi: coreyhaines31/marketingskills

> **31.2k yıldız | 5.2k fork | 309 commit | MIT lisans**
> **v2.3.0** — 43 skill + tools/ dizini | Son güncelleme: Mayıs 2026
> **Yazar:** Corey Haines (Conversion Factory, Swipe Files, Magister)

Bu repo, AI agent'lar için özel olarak tasarlanmış ~43 marketing skill'inden oluşan bir koleksiyondur. Her skill, bir `.md` dosyası olarak tanımlanır ve agent'ın o konuda nasıl davranacağını, hangi framework'leri kullanacağını anlatır.

**Temel prensip:** Tüm skill'ler önce `product-marketing` skill'ini okur — ürününü, hedef kitleni, konumlandırmanı anlamadan hiçbir şey yapmaz.

---

## Skill Mimarisi

```
product-marketing (temel — tüm skill'ler önce bunu okur)
    │
    ├── SEO & Content: seo-audit, ai-seo, site-architecture, programmatic-seo, schema, content-strategy, aso
    ├── CRO (Conversion): cro, signup, onboarding, popups, paywalls
    ├── Content & Copy: copywriting, copy-editing, cold-email, emails, social, video, image, sms
    ├── Paid & Measurement: ads, ad-creative, analytics, ab-testing
    ├── Growth & Retention: referrals, free-tools, churn-prevention, community-marketing, co-marketing, lead-magnets
    ├── Sales & GTM: revops, sales-enablement, launch, pricing, competitors, competitor-profiling, prospecting, directory-submissions
    └── Strategy: marketing-ideas, marketing-psychology, customer-research, marketing-plan
```

---

## A. Temel Skill (Foundation)

### 1. product-marketing — Ürün Pazarlama Bağlamı

**Ne işe yarar:** Bu skill, agent'ın senin ürününü tanımasını sağlar. Bir nevi "şirket kimlik kartı" gibi düşün. Ürünün ne, kime satıyorsun, rakiplerin kim, fiyatın ne — hepsini bu skill'e yazarsın. Diğer tüm skill'ler çalışmadan önce buraya bakar.

**Kullanım senaryosu:**
> "Benim SaaS ürünüm ProjectFlow, küçük ekipler için proje yönetim aracı. Hedef kitlem 5-50 kişilik yazılım ekipleri. Rakibim Jira, Asana, Monday.com. Aylık $12'den başlıyor."

Agent bu bilgiyi `product-marketing.md` dosyasına kaydeder. Sonra sen `/copywriting` dediğinde agent önce bu dosyayı okur, "Ha, ProjectFlow için yazıyorum, hedef kitle yazılım ekipleri, rakip Jira" diye anlar ve ona göre copy üretir.

**Bizde var mı:** ❌ Yok. Çok kritik — tüm agent'ın temel taşı.

---

## B. Conversion Optimization (CRO) — Dönüşüm Optimizasyonu

### 2. cro — Sayfa ve Form Dönüşüm Optimizasyonu

**Ne işe yarar:** Landing page'lerindeki, formlarındaki, CTA'larındaki dönüşüm oranını artırmak için analiz ve öneriler yapar. Ziyaretçiler neden "Satın Al" butonuna tıklamıyor? Formun neresinde terk ediyorlar? Başlık yeterince ikna edici mi?

**Kullanım senaryosu:**
> Landing page'im var, trafik geliyor ama kimse kaydolmuyor.

Agent sayfanı analiz eder ve der ki:
- "Başlığın 'Proje Yönetim Aracı' — çok genel. 'Ekibin 2x Daha Hızlı Teslim Etsin' yap."
- "CTA butonun 'Başla' — zayıf. '14 Gün Ücretsiz Dene' yap."
- "Sosyal kanıt yok. '1,200+ ekip kullanıyor' ekle."
- "Form 7 alan — çok uzun. 3 alana indir."

**Bizde var mı:** ⚠️ Kısmen — `market-funnel` benzer ama CRO spesifik değil, funnel odaklı.

### 3. signup — Kayıt Akışı Optimizasyonu

**Ne işe yarar:** Kullanıcıların kayıt olma sürecini optimize eder. "Sign up" butonundan başlayıp hesap oluşturma tamamlanana kadar her adımı inceler. Google/Apple ile kayıt, şifre politikası, email doğrulama, onboarding trigger.

**Kullanım senaryosu:**
> Kayıt sayfama girenlerin %60'ı formu tamamlamadan çıkıyor.

Agent analiz eder:
- "Şifre kuralların çok karmaşık (büyük harf + küçük harf + rakam + özel karakter). Sadece 8 karakter yap."
- "Google ile kayıt seçeneği ekle — mobil kullanıcıların %40'ı bunu tercih ediyor."
- "Email doğrulama maili 3 dakika sonra gidiyor — anında gelsin."

**Bizde var mı:** ❌ Yok.

### 4. onboarding — Kullanıcı Aktivasyonu

**Ne işe yarar:** Kullanıcı kaydolduktan sonra ürünü gerçekten kullanmaya başlamasını sağlar. "Time to value" (değeri görme süresi) ne kadar kısa olursa, kullanıcı o kadar hızlı bağlanır.

**Kullanım senaryosu:**
> Kullanıcılar kaydoluyor ama ertesi gün geri gelmiyor. 

Agent onboarding flow'unu analiz eder:
- "İlk açılışta boş dashboard gösteriyorsun. Onun yerine demo projesi ile başlat, 30 saniyede değeri görsün."
- "Welcome email'i çok geç gidiyor (1 saat sonra). Hemen gönder."
- "Checklist eksik: 'İlk projeni oluştur, ilk task'ı ekle, ekibini davet et' adımlarını göster."
- "Tooltip'ler rahatsız edici. Sadece kritik 3 özelliği göster."

**Bizde var mı:** ❌ Yok.

### 5. popups — Açılır Pencere Optimizasyonu

**Ne işe yarar:** Popup, modal, slide-in, banner gibi dikkat çekici öğelerin ne zaman, nerede, ne söyleyerek çıkacağını optimize eder. Exit-intent (çıkış niyeti), scroll tetikleyici, zaman tetikleyici stratejileri.

**Kullanım senaryosu:**
> Popup'ım var ama dönüşüm oranı %0.3. 

Agent önerir:
- "Popup 3 saniyede çıkıyor — çok erken. Ziyaretçi sayfanın %50'sini scroll'ladığında çıksın."
- "Başlık 'Bültenimize Kaydol' — sıkıcı. 'Her Hafta 1 Büyüme Taktiği (Ücretsiz)' yap."
- "Exit-intent popup ekle. Tam çıkacakken 'Bekle! Ücretsiz demo ister misin?' göster. Dönüşümü %4 artırır."
- "Mobilde popup'ı tam ekran yapma, altta banner olarak göster. Google mobil popup cezası yersin."

**Bizde var mı:** ❌ Yok.

### 6. paywalls — Ödeme Duvarı Optimizasyonu

**Ne işe yarar:** Uygulama içi ödeme duvarları, upgrade ekranları, upsell modal'ları. Freemium'dan paid'e geçişi optimize eder. Hangi özellik hangi planda olmalı? Ücretsiz kullanıcıya ne zaman "paramız bitti" denmeli?

**Kullanım senaryosu:**
> Freemium kullanıcılarım var ama %1'i bile ücretliye geçmiyor.

Agent analiz eder:
- "Paywall'u çok erken gösteriyorsun (3. gün). Kullanıcı daha değeri görmedi. 14. günde göster."
- "Ücretsiz planda çok fazla özellik var. 'Proje limiti 3' diye kısıtla, 4. projede 'Pro'ya geç' de."
- "Yıllık planı öne çıkarmıyorsun. 'Yıllık al, 2 ay bedava' teklifi ekle."

**Bizde var mı:** ❌ Yok. `market-proposal` teklif hazırlıyor ama app-içi paywall değil.

---

## C. Content & Copy

### 7. copywriting — Pazarlama Metni Yazımı

**Ne işe yarar:** Landing page, homepage, ürün sayfası için ikna edici metinler yazar. AIDA (Attention-Interest-Desire-Action), PAS (Problem-Agitate-Solve), BAB (Before-After-Bridge) gibi framework'leri kullanır.

**Kullanım senaryosu:**
> SaaS ürünüm için yeni homepage copy'si yaz.

Agent sorar: Hedef kitle? Ana değer önerisi? Rakip? Sonra:
- Hero başlık: "Ekibinizin Projeleri 2x Daha Hızlı Bitirmesini Sağlayın"
- Alt başlık: "Jira'nın karmaşıklığı olmadan, Asana'nın basitliğiyle. 1,200+ ekip ProjectFlow ile haftada 5 saat kazanıyor."
- CTA: "14 Gün Ücretsiz Dene — Kredi Kartı Gerekmez"
- Sosyal kanıt bölümü: 3 müşteri logosu + yorum
- Özellik grid'i: her özellik = fayda formatında (sadece "Gantt chart" değil, "Teslim tarihlerini asla kaçırma")

**Bizde var mı:** ⚠️ Kısmen — Mevcut skill'ler direk copywriting yapmıyor. `landing-page-generator` sayfa üretiyor ama copy odaklı değil.

### 8. copy-editing — Mevcut Metni Düzenleme

**Ne işe yarar:** Zaten yazılmış bir metni iyileştirir. Daha net, daha ikna edici, daha okunabilir hale getirir. Gereksiz kelimeleri atar, pasif cümleleri aktif yapar, jargondan arındırır.

**Kullanım senaryosu:**
> Blog yazımı düzenler misin, çok uzun ve karmaşık olmuş.

Agent:
- "Giriş paragrafı 120 kelime — 40 kelimeye indir."
- "'Utilize' yerine 'use', 'facilitate' yerine 'help' kullan."
- "3 pasif cümle var: 'The report was generated' → 'ProjectFlow generates the report'"
- "Okunabilirlik skoru: 45 (zor) → 70 (kolay) seviyesine çektim."
- "Her paragraf max 3 cümle olsun."

**Bizde var mı:** ❌ Yok.

### 9. cold-email — Soğuk E-posta (B2B)

**Ne işe yarar:** Potansiyel müşterilere gönderilen ilk temas (cold outreach) emaillerini yazar. Açılma oranı, yanıt oranı, toplantı dönüşümü optimize edilir.

**Kullanım senaryosu:**
> 50 CTO'ya cold email atacağım, proje yönetim aracımızı tanıtacağım.

Agent 3 aşamalı sequence yazar:
- **Email 1 (ilk temas):** Konu: "Quick question about {sirket}'s dev workflow". Gövde: Kişiselleştirilmiş, spesifik, 80 kelime max. CTA: "15 dk demo?"
- **Email 2 (3 gün sonra):** Değer odaklı. "Teams using ProjectFlow ship 2x faster. Here's how {benzer_sirket} did it."
- **Email 3 (7 gün sonra):** Breakup email. "Wanted to make sure this wasn't the wrong contact. If you're the right person..."

**Bizde var mı:** ⚠️ Kısmen — `market-emails` var ama nurture/launch odaklı, cold outreach yok.

### 10. emails — Email Dizileri

**Ne işe yarar:** Welcome, onboarding, nurture, re-engagement, transactional email dizileri oluşturur. Her email'in konusu, gövdesi, CTA'sı, gönderim zamanlaması bellidir.

**Kullanım senaryosu:**
> Deneme sürümü başlatan kullanıcılar için 7 günlük email sequence'i oluştur.

Agent 7 email'lik trial sequence üretir — her email bir amaca hizmet eder: Hoş geldin → İlk değer → Power user özelliği → Vaka çalışması → Upgrade teklifi → Son şans → Kaybeden geri kazanma.

**Bizde var mı:** ✅ VAR — `market-emails` aynı işi yapıyor.

### 11. social — Sosyal Medya İçeriği

**Ne işe yarar:** LinkedIn, Twitter/X, Instagram için içerik stratejisi ve takvimi oluşturur. Platform'a özel format, hashtag, gönderim zamanı önerir.

**Kullanım senaryosu:**
> LinkedIn'de düzenli içerik üretmek istiyorum, SaaS kurucuları hedef kitlem.

Agent:
- "Haftada 3 gönderi: Salı (değer), Perşembe (vaka), Cumartesi (kişisel hikaye)."
- Her gönderi için: hook (ilk satır), gövde, CTA, en iyi gönderim saati.
- İlk ay içerik takvimi: 12 gönderi, her biri spesifik.

**Bizde var mı:** ✅ VAR — `market-social` aynı işi yapıyor.

### 12. video — Video İçerik Üretimi

**Ne işe yarar:** AI araçlarıyla video içerik üretimi. Demo videosu, ürün tanıtımı, social clip, tutorial. AI video araçlarını (HeyGen, Synthesia, Runway) nasıl kullanacağını bilir.

**Kullanım senaryosu:**
> Ürünümüzün 60 saniyelik demo videosunu yap.

Agent:
- "60 saniyelik script: 0-10sn problem, 10-35sn çözüm (ekran kaydı), 35-50sn sonuçlar, 50-60sn CTA."
- "Ekran kaydı için OBS kullan, voiceover için ElevenLabs."
- "Sosyal medya için 15sn'lik 3 klip kes."

**Bizde var mı:** ❌ Yok.

### 13. image — Görsel Üretimi

**Ne işe yarar:** Blog hero görseli, sosyal medya grafiği, ürün screenshot'ı, infografik gibi pazarlama görsellerini AI ile üretir. Midjourney/DALL-E prompt'ları yazar, Canva/Figma şablonları önerir.

**Kullanım senaryosu:**
> "Yapay Zeka ile Proje Yönetimi" başlıklı blog yazısı için hero görseli lazım.

Agent:
- Midjourney prompt: "A futuristic project management dashboard with AI holograms, clean interface, blue and purple gradient, minimalist style --ar 16:9"
- Alternatif: Canva şablon linki + özelleştirme talimatları.

**Bizde var mı:** ❌ Yok.

### 14. sms — SMS Pazarlama

**Ne işe yarar:** SMS/MMS pazarlama kampanyaları. Welcome SMS, abandoned cart SMS, yeniden aktivasyon SMS'i. Kısa mesaj olduğu için copywriting çok farklıdır — 160 karakterde ikna etmelisin.

**Kullanım senaryosu:**
> Sepeti terk eden müşterilere SMS göndermek istiyorum.

Agent:
- "Sepet terkinden 30 dk sonra: 'Sepetin seni bekliyor! 🛒 Şimdi tamamla, %10 indirim kazan: {link}' (90 karakter)"
- "24 saat sonra: 'Ürünler tükenmeden... {link}' (60 karakter)"
- SMS onayı (opt-in) mekanizmasını unutma — yasal zorunluluk.

**Bizde var mı:** ❌ Yok.

---

## D. SEO & Keşfedilebilirlik

### 15. seo-audit — SEO Teknik Denetimi

**Ne işe yarar:** Sitenin SEO sağlığını kontrol eder. Title tag, meta description, heading yapısı, sayfa hızı, mobil uyumluluk, iç bağlantı, canonical URL, robots.txt, sitemap — hepsini tarar.

**Kullanım senaryosu:**
> Sitem Google'da 3. sayfada çıkıyor, neden?

Agent siteyi tarar:
- "15 sayfanın title tag'i 'Home' — her biri benzersiz olmalı."
- "Blog yazılarında H1 yok. Her yazıya tek H1 ekle."
- "24 görselin alt tag'i boş. Doldur."
- "Sayfa hızı mobilde 8.2 saniye — 3 saniyenin altına inmen lazım."
- "Schema markup hiç yok. FAQ ve Article schema ekle."

**Bizde var mı:** ✅ VAR — `market-seo` aynı işi yapıyor.

### 16. ai-seo — AI Arama Motorları için Optimizasyon

**Ne işe yarar:** Google dışındaki AI arama motorlarında (ChatGPT, Perplexity, Claude, Gemini) görünürlük için optimizasyon. LLM'lerin siteni "kaynak" olarak göstermesi için ne yapmalısın?

**Kullanım senaryosu:**
> ChatGPT'de "en iyi proje yönetim aracı" diye sorulduğunda bizim ürünümüzün çıkmasını istiyorum.

Agent:
- "Structured data kritik — FAQ schema ve Article schema olmadan LLM'ler seni ciddiye almaz."
- "Wikipedia'da geçmen lazım. Wikipedia backlink'i LLM'ler için en güçlü sinyal."
- "Yüksek otoriteli sitelerde misafir yazısı yaz. LLM'ler .edu, .gov, büyük medya sitelerini önceliklendiriyor."
- "İçeriğinde net tanımlar, istatistikler, karşılaştırmalar olmalı. LLM'ler muğlak içeriği sevmez."

**Bizde var mı:** ❌ Yok. SEO'dan farklı, çok yeni bir alan.

### 17. programmatic-seo — Programatik SEO

**Ne işe yarar:** Veri tabanından gelen verilerle binlerce SEO sayfasını otomatik üretme. "X şehrinde Y hizmeti", "A sektöründe B aracı" gibi kalıplarla scale edilebilir sayfalar.

**Kullanım senaryosu:**
> "İstanbul'daki en iyi yazılım ekipleri", "Ankara'daki..." diye 81 il için sayfa oluşturmak istiyorum.

Agent:
- "Veritabanından şehirleri ve özellikleri çek, template'e bas."
- "Her sayfa benzersiz olmalı — en azından şehre özel 1-2 paragraf."
- "URL yapısı: `/sehir/{sehir-adi}-yazilim-ekipleri`"
- "İç bağlantı: her sayfadan diğer 5 şehre link."
- "Dikkat: Google thin content (ince içerik) cezası verebilir. Her sayfa min. 300 kelime olmalı."

**Bizde var mı:** ❌ Yok.

### 18. site-architecture — Site Mimarisi

**Ne işe yarar:** Web sitesinin sayfa hiyerarşisini, navigasyon yapısını, URL yapısını, iç bağlantı stratejisini planlar. Hem SEO hem UX için kritik.

**Kullanım senaryosu:**
> Sitem büyüdü, 200+ sayfa oldu. Navigasyon karmaşası var.

Agent:
- "Ana navigasyon: Home, Features, Pricing, Blog, Docs. En fazla 5 öğe."
- "Blog kategorileri: Product, Engineering, Growth, Culture."
- "URL yapısı: `/blog/kategori/yazi-adi` — düz `/blog/yazi-adi` değil."
- "Her blog yazısından 3 ilgili yazıya link ver."
- "Footer'da önemli sayfaları tekrarla."

**Bizde var mı:** ❌ Yok.

### 19. schema — Schema Markup (Yapılandırılmış Veri)

**Ne işe yarar:** Google'ın zengin snippet'ler (yıldız puanı, fiyat, FAQ, ekmek kırıntısı) göstermesi için gereken schema.org işaretlemelerini ekler.

**Kullanım senaryosu:**
> Google'da ürün sayfam çıkıyor ama fiyat ve yıldız puanı görünmüyor, rakiplerde var.

Agent:
- "Product schema ekle — fiyat, stok durumu, yıldız puanı."
- "FAQ schema ekle — her soru-cevap Google'da akordiyon olarak görünür, tıklama oranını %15 artırır."
- "BreadcrumbList schema — ekmek kırıntısı navigasyonu."
- "JSON-LD formatında ekle, HTML içine göm."

**Bizde var mı:** ❌ Yok. `market-seo` içinde kısmen değiniyor ama detaylı değil.

### 20. competitors — Rakip Karşılaştırma Sayfaları

**Ne işe yarar:** "X vs Y", "X alternatifi" gibi rakip karşılaştırma sayfaları oluşturur. SEO için altın değerinde — alternatif arayan kullanıcıyı yakalarsın.

**Kullanım senaryosu:**
> "Jira alternatifi" aramasında çıkmak istiyorum.

Agent:
- "Sayfa başlığı: 'ProjectFlow vs Jira: Hangi Proje Yönetim Aracı Daha İyi? (2026)'"
- "Tarafsız karşılaştırma tablosu: fiyat, özellikler, kullanım kolaylığı, müşteri desteği."
- "'Jira'dan ProjectFlow'a Geçiş' bölümü — nasıl migrate edilir."
- "Gerçek kullanıcı yorumları (G2, Capterra'dan alıntı)."
- "CTA: '14 gün ücretsiz dene, Jira'dan geçiş 1 gün sürer.'"

**Bizde var mı:** ⚠️ Kısmen — `market-competitors` genel rakip analizi yapıyor ama SEO odaklı alternatif sayfası üretmiyor.

### 21. competitor-profiling — Rakip Profili Çıkarma

**Ne işe yarar:** Bir rakibin URL'sini ver, agent o rakibi didik didik etsin. Hangi özellikleri var, nasıl fiyatlandırıyor, nasıl konumlanıyor, hangi kanalları kullanıyor — hepsini çıkarsın.

**Kullanım senaryosu:**
> "monday.com'u analiz et, nerede zayıflar?"

Agent siteyi tarar:
- "Pazarlama kanalları: Google Ads (agresif), LinkedIn, içerik pazarlaması (blog haftada 3 yazı)."
- "Zayıf nokta: Mobil uygulaması düşük puanlı (3.2/5)."
- "Fiyatlandırma hatası: Orta planları çok pahalı ($10/kullanıcı), küçük ekipleri kaçırıyorlar."
- "Konumlandırma: 'Work OS' — çok geniş, kimse anlamıyor."

**Bizde var mı:** ⚠️ Kısmen — `market-competitors` benzer ama derinlemesine tek rakip profili değil.

### 22. directory-submissions — Dizin Başvuruları

**Ne işe yarar:** Startup'ını, SaaS ürününü dizinlere (Product Hunt, G2, Capterra, AI directories, MCP directories) eklemek için strateji. Hangi dizinler önemli, nasıl başvurulur, açıklama nasıl yazılır.

**Kullanım senaryosu:**
> Ürünümüzü daha fazla yerde listeleyelim, nerelere başvuralım?

Agent:
- "Öncelikli: Product Hunt (lansman için), G2, Capterra (SEO için altın)."
- "AI dizinleri: Futurepedia, There's an AI for That, AI Tool Hunt."
- "Her dizin için özel açıklama yaz: G2'de özellik odaklı, Product Hunt'ta maker hikayesi."
- "Başvuru takvimi: bu hafta 3 dizin, önümüzdeki hafta 5 dizin."

**Bizde var mı:** ❌ Yok.

### 23. content-strategy — İçerik Stratejisi

**Ne işe yarar:** Ne hakkında içerik üretmelisin? Hangi konular, hangi format, hangi sıklıkta? Blog, video, podcast, sosyal medya — hangi kanalda ne yapmalısın?

**Kullanım senaryosu:**
> Blog yazmaya başlayacağım ama ne hakkında yazacağımı bilmiyorum.

Agent:
- "Hedef kitlenin sorduğu 50 soruyu araştır. Reddit, Quora, Google 'People Also Ask'."
- "İçerik takvimi: Haftada 1 uzun blog + 1 kısa sosyal medya."
- "Konu kümeleri: Proje Yönetimi Temelleri, Agile/Scrum, Ekip İletişimi, Uzaktan Çalışma."
- "Her yazı için anahtar kelime araştırması ve hedef kelime."

**Bizde var mı:** ⚠️ Kısmen — `market-social` takvim yapıyor ama strateji değil.

### 24. aso — App Store Optimizasyonu

**Ne işe yarar:** Mobil uygulamanın App Store ve Google Play'deki sıralamasını yükseltir. Başlık, açıklama, anahtar kelime, ekran görüntüsü, yorum stratejisi.

**Kullanım senaryosu:**
> iOS uygulamam App Store'da "proje yönetimi" aramasında 28. sırada.

Agent:
- "Başlığa ana anahtar kelimeyi ekle: 'ProjectFlow: Proje Yönetimi ve Ekip İletişimi'"
- "Açıklamanın ilk 3 satırı en önemli — değer önerini buraya koy."
- "Keyword alanı: rakiplerin kullandığı kelimeleri araştır, 100 karakteri doldur."
- "Ekran görüntülerinde fayda göster, sadece arayüz değil."
- "Her güncellemede yorum iste. 4+ yıldız için en az 50 yorum lazım."

**Bizde var mı:** ❌ Yok.

---

## E. Paid & Measurement — Reklam ve Ölçüm

### 25. ads — Reklam Kampanyaları

**Ne işe yarar:** Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X reklam kampanyaları için strateji, hedefleme, bütçe planlaması.

**Kullanım senaryosu:**
> Google Ads'e aylık 5,000 TL bütçe ayırdık, nasıl harcayalım?

Agent:
- "Search kampanyası: 'proje yönetim aracı', 'ekip yönetimi', 'task management' keyword'leri."
- "Rakip keyword'leri: 'jira alternatifi', 'asana alternatifi'."
- "Bütçe dağılımı: %60 Search, %30 Display (retargeting), %10 YouTube."
- "Landing page özel olmalı — homepage'e gönderme, kampanya için özel sayfa yap."
- "Conversion tracking kur — hangi keyword satış getiriyor?"

**Bizde var mı:** ⚠️ Kısmen — `market-ads` yaratıcı (creative) odaklı, bütçe/strateji yok.

### 26. ad-creative — Reklam Kreatifi Üretimi

**Ne işe yarar:** Büyük ölçekte reklam metni ve görseli üretir. A/B test için varyasyonlar, farklı hedef kitle için farklı mesajlar, sezonluk kampanyalar.

**Kullanım senaryosu:**
> Facebook için 20 farklı reklam varyasyonu lazım.

Agent:
- "5 farklı hedef kitle için (CTO, PM, Founder, Freelancer, Enterprise) 4'er varyasyon = 20 reklam."
- "Her varyasyon: Primary Text, Headline, Description, CTA."
- "CTO'ya: 'Ekip verimliliği', Founder'a: 'Maliyet tasarrufu', PM'e: 'Teslim tarihi' odaklı."
- "A/B test planı: önce hangi kitle, sonra hangi mesaj, sonra hangi görsel."

**Bizde var mı:** ⚠️ Kısmen — `market-ads` içinde var ama bulk üretim yok.

### 27. analytics — Analitik Kurulumu

**Ne işe yarar:** GA4, Mixpanel, Amplitude, Meta Pixel gibi analitik araçlarının kurulumunu ve event tracking'i planlar. Hangi event'ler önemli, nasıl track edilir.

**Kullanım senaryosu:**
> SaaS'ımızda hangi event'leri track etmeliyiz?

Agent:
- "Kritik event'ler: signup, onboarding_complete, first_project_created, invite_team_member, upgrade_to_paid, churn."
- "GA4'te custom event olarak tanımla."
- "Her event için parametre: plan (free/pro), kaynak (organic/ads/referral), cihaz."
- "Dashboard: haftalık aktif kullanıcı, trial-to-paid oranı, feature adoption."
- "Meta Pixel + LinkedIn Insight Tag de ekle — retargeting için."

**Bizde var mı:** ❌ Yok. `product-analytics` genel KPI/metrik skill'i ama teknik kurulum değil.

### 28. ab-testing — A/B Test Tasarımı

**Ne işe yarar:** A/B testi (veya çok değişkenli test) tasarlar. Hipotez oluşturma, örneklem büyüklüğü hesabı, test süresi, istatistiksel anlamlılık.

**Kullanım senaryosu:**
> Landing page'imin başlığını değiştireceğim, test edelim.

Agent:
- "Hipotez: 'Proje Yönetim Aracı' yerine 'Ekibin 2x Hızlı Teslim Etsin' başlığı signup'ları %15 artırır."
- "Örneklem hesabı: Ayda 10,000 ziyaretçin var. %15 fark için 2 hafta test yeterli."
- "Test grupları: %50 kontrol, %50 varyant."
- "İstatistiksel anlamlılık: p < 0.05."
- "Testi çok erken durdurma — minimum 1 hafta bekle."

**Bizde var mı:** ✅ VAR — `experiment-designer` tam olarak bu işi yapıyor.

---

## F. Growth & Retention — Büyüme ve Elde Tutma

### 29. referrals — Referans Programı

**Ne işe yarar:** "Arkadaşını getir, ikiniz de kazanın" tarzı referans programları tasarlar. Dropbox'ın meşhur %3900 büyümesi referans programı sayesindeydi.

**Kullanım senaryosu:**
> Kullanıcılarımızın bizi arkadaşlarına önermesini nasıl teşvik ederiz?

Agent:
- "Çift taraflı ödül: Davet eden 1 ay ücretsiz, gelen %20 indirim."
- "Paylaşımı kolaylaştır: Tek tıkla link kopyalama, email taslağı, sosyal medya paylaşımı."
- "Dashboard'da göster: '3 arkadaşını davet et, 3 ay bedava kullan.'"
- "Referans programını onboarding'in 4. adımı yap — kullanıcı değeri gördükten sonra."

**Bizde var mı:** ❌ Yok.

### 30. free-tools — Ücretsiz Araç Stratejisi

**Ne işe yarar:** Lead generation için ücretsiz araçlar (calculator, checker, generator) planlar. HubSpot'ın "Website Grader"ı gibi. SEO değeri + email capture.

**Kullanım senaryosu:**
> Sitemize trafik çekecek ücretsiz bir araç yapalım.

Agent:
- "Fikir 1: 'Proje Maliyet Hesaplayıcı' — ekip büyüklüğü ve süreyi gir, maliyeti hesaplasın."
- "Fikir 2: 'Sprint Velocity Checker' — takımının hızını ölç."
- "Her araç için email capture formu. Sonucu görmek için email zorunlu olmasın ama 'detaylı raporu email'ine gönderelim' de."
- "SEO: Bu araçlar long-tail keyword'ler için manyetik gibidir."

**Bizde var mı:** ❌ Yok.

### 31. churn-prevention — Terk Önleme

**Ne işe yarar:** Müşterilerin ürünü bırakmasını engeller. İptal akışı, "save offer" (kalma teklifi), ödeme hatası kurtarma (dunning), pasif kullanıcı yeniden aktivasyon.

**Kullanım senaryosu:**
> Aylık %5 müşteri kaybediyoruz, neden?

Agent:
- "İptal akışına 2 kademeli save offer ekle: önce '1 ay ücretsiz dondur', sonra '%50 indirimli 3 ay'."
- "Ödeme hatası: Kredi kartı reddedilince hemen iptal etme. 3 gün, 7 gün, 14 gün sonra tekrar dene."
- "Pasif kullanıcı: 30 gün giriş yapmayana 'Seni özledik' email'i + yeni özellik tanıtımı."
- "Exit survey: İptal edenlere 'Neden?' sor. En sık 3 sebebi çöz."

**Bizde var mı:** ❌ Yok.

### 32. community-marketing — Topluluk Pazarlaması

**Ne işe yarar:** Discord, Slack, forum, Facebook grubu gibi topluluklar kurarak büyüme. Kullanıcıların birbirine yardım ettiği, ürün etrafında bağ kurduğu alanlar.

**Kullanım senaryosu:**
> Kullanıcılarımız için bir Discord topluluğu kuralım.

Agent:
- "Topluluk yapısı: hoşgeldin, genel, ipuçları, özellik-istek, bug-bildirim, duyurular."
- "İlk 100 üye için onboarding: DM ile hoşgeldin, rol ver, ilk gönderiyi atması için teşvik et."
- "Haftalık etkinlik: 'Salı İpuçları', 'Cuma Showcase'."
- "Power user'ları mod yap. Onlar senin ücretsiz destek ekibin olur."
- "Topluluğu product roadmap'e bağla: en çok oy alan özellik isteklerini yap."

**Bizde var mı:** ❌ Yok.

### 33. co-marketing — Ortak Pazarlama

**Ne işe yarar:** Tamamlayıcı ürünlerle ortak kampanyalar. Ortak webinar, ortak blog yazısı, ortak email blast, karşılıklı tavsiye.

**Kullanım senaryosu:**
> Bizimle aynı kitleye hitap eden ama rakip olmayan ürünlerle işbirliği yapalım.

Agent:
- "Potansiyel partnerler: Slack, GitHub, Figma entegrasyonu olan araçlar."
- "Teklif: 'Birlikte webinar yapalım, iki taraf da email listesine duyursun.'"
- "Ortak içerik: 'ProjectFlow + Slack ile Ekip Verimliliğini 2x Artır'."
- "Partner bulma: LinkedIn'de 'integration partner' ara, email at."

**Bizde var mı:** ❌ Yok.

### 34. lead-magnets — Lead Mıknatısları

**Ne işe yarar:** Email toplamak için değerli içerik teklifleri. E-kitap, şablon, checklist, mini kurs, webinar, swipe file.

**Kullanım senaryosu:**
> Email listemizi büyütmek için ne verebiliriz?

Agent:
- "Fikir 1: 'Proje Yönetimi Şablon Paketi' — 10 Notion/Excel şablonu."
- "Fikir 2: 'Sprint Retrospektif Checklist'i' — 1 sayfalık PDF."
- "Fikir 3: 'En İyi 50 Proje Yönetim Aracı Karşılaştırması 2026'."
- "Landing page: başlık, ne kazanacaksın, email formu, CTA. Tek sayfa. Karmaşık değil."
- "Delivery: email'e otomatik gönder, aynı email'de ürüne yumuşak geçiş yap."

**Bizde var mı:** ❌ Yok.

---

## G. Sales & GTM

### 35. revops — Revenue Operations (Gelir Operasyonları)

**Ne işe yarar:** Lead'lerin yaşam döngüsünü yönetir. Lead scoring (hangi lead sıcak?), lead routing (hangi lead hangi satıcıya?), marketing-to-sales handoff (pazarlamadan satışa geçiş). HubSpot/Salesforce gibi CRM'lerle entegre düşünür.

**Kullanım senaryosu:**
> Lead'lerimiz CRM'de birikiyor ama satış ekibi hangisine odaklanacağını bilmiyor.

Agent:
- "Lead scoring modeli: Demografi (şirket büyüklüğü, sektör) + Davranış (demo izledi mi, pricing sayfasına baktı mı, email açtı mı)."
- "Puan > 80 = sıcak lead, direkt satışa. 50-80 = ılık, nurture sequence'e. < 50 = soğuk, bekle."
- "MQL → SQL tanımı: MQL demo izlediğinde, SQL satışla görüştüğünde."
- "Slack notification: '🔥 Sıcak lead: Acme Corp (95 puan) pricing sayfasında.'"

**Bizde var mı:** ❌ Yok.

### 36. sales-enablement — Satış Destek Malzemeleri

**Ne işe yarar:** Satış ekibinin kullanacağı materyalleri hazırlar. Pitch deck, one-pager, itiraz yanıtlama dökümanı, demo script'i, vaka çalışması, ROI hesaplayıcı.

**Kullanım senaryosu:**
> Satış ekibimiz için yeni bir pitch deck hazırlayalım.

Agent:
- "Slide 1: Problem (1 cümle). Slide 2: Çözüm (1 cümle). Slide 3: Nasıl çalışır (3 adım)."
- "Slide 4: Özellikler değil, faydalar. 'Gantt chart' değil 'Teslim tarihini kaçırma'."
- "Slide 5: Sosyal kanıt — logo bulutu + 1 müşteri yorumu."
- "Slide 6: Fiyatlandırma — 3 plan, orta plan önerilen."
- "Slide 7: CTA — 'Demo planlayalım'."
- "Ek: İtiraz yanıtlama sayfası ('Çok pahalı', 'Jira kullanıyoruz', 'Şimdi değil' — her birine 2 cümlelik hazır cevap)."

**Bizde var mı:** ❌ Yok.

### 37. launch — Ürün Lansmanı

**Ne işe yarar:** Yeni ürün, özellik veya duyuru lansmanı için strateji. Pre-launch (ısıtma), launch (büyük gün), post-launch (momentum koruma).

**Kullanım senaryosu:**
> Yeni AI özelliğimizi 2 hafta sonra duyuracağız.

Agent:
- "Pre-launch: 2 hafta önce teaser sosyal medya, 1 hafta önce waitlist, 3 gün önce email."
- "Launch günü: Product Hunt, email blast, sosyal medya push, blog post, PR."
- "Post-launch: kullanıcı yorumlarını topla, vaka yazısı yaz, 1 hafta sonra 'kaçıranlar için' email'i."
- "Metrikler: waitlist signup, launch günü traffic, trial başlangıcı, 7 günlük retention."

**Bizde var mı:** ✅ VAR — `market-launch` aynı işi yapıyor.

### 38. pricing — Fiyatlandırma Stratejisi

**Ne işe yarar:** Fiyatlandırma, paketleme, monetizasyon stratejisi. Freemium mu, flat rate mi, usage-based mi? Kaç plan olmalı? Fiyatlar ne olmalı?

**Kullanım senaryosu:**
> Fiyatlandırmamız karmaşık, sadeleştirelim.

Agent:
- "3 plan yeterli: Free (sınırlı), Pro (tam özellik), Enterprise (özel)."
- "Anchor pricing: Pro planı öne çıkar, Enterprise'ı çok pahalı göster ki Pro makul görünsün."
- "Free plan: özellik değil, kullanım limiti koy ('3 proje', '5 kullanıcı' gibi). Değeri gördükten sonra limit dolunca upgrade doğal olur."
- "Yıllık fiyatlandırma: aylık x 10 = yıllık. 2 ay bedava gibi görünür."

**Bizde var mı:** ❌ Yok. `product-strategist` genel strateji ama spesifik pricing yok.

### 39. prospecting — Potansiyel Müşteri Bulma

**Ne işe yarar:** Hedef kitleye uygun potansiyel müşterileri (prospect) bulmak için araştırma. Linkedin, Apollo.io, devlet kayıtları gibi kaynaklardan liste oluşturma.

**Kullanım senaryosu:**
> B2B SaaS'ımız için 100 potansiyel müşteri bul.

Agent:
- "LinkedIn Search: 'CTO' + 'software company' + '50-200 employees' + 'United States'."
- "İpucu: Yeni işe başlayan CTO'lar/VP Engineering'ler en sıcak lead'lerdir — eski sistemi değiştirmek için bütçe almışlardır."
- "Liste formatı: İsim, Şirket, Unvan, LinkedIn URL, Email (tahmini format)."
- "Qualify: Tech stack'lerine bak (BuiltWith, Wappalyzer). Jira kullanıyorlarsa sıcak lead."

**Bizde var mı:** ❌ Yok.

---

## H. Strategy & Intelligence

### 40. marketing-ideas — Pazarlama Fikirleri

**Ne işe yarar:** 140'tan fazla SaaS pazarlama fikri içeren bir veritabanı. Yaratıcı tıkanıklık anında "ne yapabilirim?" diye sorduğunda fikir üretir.

**Kullanım senaryosu:**
> Büyümemiz durdu, yeni pazarlama fikri lazım.

Agent:
- "Growth hack: Açık kaynak projelere sponsor ol — GitHub README'de logon olsun."
- "İçerik hack: Rakibin en popüler blog yazısını al, 10x daha iyisini yaz (Skyscraper tekniği)."
- "PR hack: Help a Reporter Out (HARO) ile gazetecilere kaynak ol, büyük sitelerde backlink kazan."
- "Product hack: Ürününe 'public roadmap' ekle. Kullanıcılar oy versin, bağlılık artsın."

**Bizde var mı:** ❌ Yok.

### 41. marketing-psychology — Pazarlama Psikolojisi

**Ne işe yarar:** Davranışsal ekonomi ve psikoloji prensiplerini pazarlamaya uygular. Kıtlık (scarcity), sosyal kanıt (social proof), çıpalama (anchoring), kayıptan kaçınma (loss aversion), endowment effect.

**Kullanım senaryosu:**
> Landing page'imi psikolojik olarak daha ikna edici yap.

Agent:
- "Kıtlık: 'Sadece 3 slot kaldı' veya 'İndirim 48 saat geçerli'."
- "Sosyal kanıt: '1,200+ ekibe katıl' (sayı ver, muğlak olma)."
- "Çıpalama: Önce pahalı planı göster, sonra 'en popüler' planı. Pahalıyı görünce ortadaki ucuz görünür."
- "Kayıptan kaçınma: '14 gün ücretsiz dene' yerine '14 gün sonra otomatik iptal, kaybedeceğin bir şey yok'."
- "IKEA etkisi: Onboarding'de kullanıcıya bir şey yaptır (ilk projesini oluştur). Emek verdiği şeye bağlanır."

**Bizde var mı:** ❌ Yok.

### 42. customer-research — Müşteri Araştırması

**Ne işe yarar:** Müşteri görüşmelerini, anketleri, kullanıcı testlerini planlar ve analiz eder. Müşterinin ne dediğini değil, ne demek istediğini anlar (Jobs to be Done framework).

**Kullanım senaryosu:**
> Kullanıcılarımız ürünü neden seviyor/sevmiyor, anlayalım.

Agent:
- "5 müşteriyle 30 dakikalık görüşme ayarla. Sorulacak sorular: 'ProjectFlow'u kullanmasaydın ne kullanırdın?', 'ProjectFlow'u ilk ne zaman işe yarar buldun?'"
- "JTBD analizi: Kullanıcı ürünü 'proje yönetmek' için değil, 'patronuna ilerleme raporu vermek' için kullanıyor olabilir."
- "Anket: NPS + açık uçlu 'Neden bu puanı verdin?' + 'Eksik olan bir şey var mı?'"
- "Bulguları ürün ekibine sun: en çok sevilen 3 özellik, en çok şikayet edilen 3 şey."

**Bizde var mı:** ⚠️ Kısmen — `ux-researcher-designer` persona ve journey map yapıyor ama derinlemesine müşteri görüşmesi değil.

### 43. marketing-plan — Pazarlama Planı (YENİ — v2.3.0)

**Ne işe yarar:** AARRR (Acquisition-Activation-Retention-Revenue-Referral) framework'ü ile kapsamlı pazarlama planı oluşturur. Fractional CMO gibi düşün. Tüm diğer skill'leri koordine eder.

**Kullanım senaryosu:**
> Yeni SaaS ürünümüz için 6 aylık pazarlama planı yap.

Agent:
- **Acquisition:** SEO (blog, alternatif sayfaları), Google Ads (rakip keyword'leri), LinkedIn (founder content).
- **Activation:** Onboarding flow optimizasyonu, welcome email, demo videosu.
- **Retention:** Churn analizi, save offer, community kurulumu.
- **Revenue:** Fiyatlandırma testi, annual plan push, upsell email'leri.
- **Referral:** Referans programı, vaka çalışması, testimonial toplama.
- Her aşama için KPI, bütçe, timeline, sorumlu kişi.

**Bizde var mı:** ❌ Yok. Bizim en büyük eksiğimiz — tüm skill'leri koordine eden ana plan yok.

---

## Bizde Olan vs Eksik — Gap Matrisi

### ✅ Bizde VAR (kısmen veya tam)

| Repo Skill | Bizdeki Karşılığı | Durum |
|-----------|-------------------|-------|
| emails | `market-emails` | ✅ Tam |
| social | `market-social` | ✅ Tam |
| ads (kısmen) | `market-ads` | ⚠️ Yaratıcı var, strateji/bütçe yok |
| launch | `market-launch` | ✅ Tam |
| competitors | `market-competitors` | ⚠️ Genel analiz var, SEO alternatif sayfası yok |
| seo-audit | `market-seo` | ✅ Tam |
| cro (kısmen) | `market-funnel` | ⚠️ Funnel odaklı, sayfa CRO'su detaylı değil |
| copywriting (kısmen) | `landing-page-generator` | ⚠️ Sayfa üretiyor, copy odaklı değil |
| ab-testing | `experiment-designer` | ✅ Tam |
| customer-research | `ux-researcher-designer` | ⚠️ UX odaklı, JTBD/depth interview yok |

### ❌ Bizde YOK — Yeni Eklenecekler (40 skill'den)

| Kategori | Eksik Skill'ler |
|----------|----------------|
| **Temel** | `product-marketing` (KRİTİK) |
| **CRO** | `cro`, `signup`, `onboarding`, `popups`, `paywalls` |
| **Content** | `copywriting`, `copy-editing`, `cold-email`, `video`, `image`, `sms` |
| **SEO** | `ai-seo`, `programmatic-seo`, `site-architecture`, `schema`, `competitors` (SEO alternatif sayfası), `aso` |
| **Paid** | `ads` (strateji/bütçe), `ad-creative` (bulk üretim), `analytics` |
| **Growth** | `referrals`, `free-tools`, `churn-prevention`, `community-marketing`, `co-marketing`, `lead-magnets` |
| **Sales** | `revops`, `sales-enablement`, `pricing`, `competitor-profiling`, `prospecting`, `directory-submissions` |
| **Strategy** | `marketing-plan` (KRİTİK), `marketing-ideas`, `marketing-psychology` |

---

## Kategorilere Göre Kullanım Senaryosu Özeti

### CRO seti (`cro` + `signup` + `onboarding` + `popups` + `paywalls`)
> "Conversion rate'im %2. Bunu %5 yapmak istiyorum."

Agent tüm CRO skill'lerini zincirler: Landing page'i analiz eder → Signup flow'u inceler → Onboarding'i kontrol eder → Popup stratejisi önerir → Paywall'u optimize eder. Tek seferde funnel'ın her aşamasını iyileştirir.

### Content seti (`copywriting` + `copy-editing` + `emails` + `social` + `image` + `video`)
> "Yeni ürünümüz için tüm içerikleri hazırla."

Agent: Copywriting ile homepage yazar → Emails ile welcome sequence hazırlar → Social ile LinkedIn takvimi oluşturur → Image ile hero görseli üretir → Video ile demo script'i yazar.

### SEO seti (`seo-audit` + `ai-seo` + `site-architecture` + `schema` + `programmatic-seo` + `aso`)
> "Google'da ve ChatGPT'de görünür olalım."

Agent: SEO audit ile teknik hataları bulur → Site architecture ile yapıyı düzeltir → Schema markup ekler → AI SEO ile LLM'ler için optimize eder → Programmatic SEO ile ölçeklenebilir sayfalar üretir.

### Sales seti (`prospecting` + `cold-email` + `sales-enablement` + `revops`)
> "Satış ekibimizin verimliliğini artır."

Agent: Prospecting ile 100 lead bulur → Cold-email ile outreach sequence yazar → Sales-enablement ile pitch deck hazırlar → Revops ile lead scoring kurar.

### Growth seti (`referrals` + `free-tools` + `churn-prevention` + `community-marketing`)
> "Büyüme motoru kurmak istiyorum."

Agent: Referrals ile referans programı tasarlar → Free-tools ile lead mıknatısı araç önerir → Churn ile kaybı azaltır → Community ile kullanıcı bağlılığı yaratır.

---

## Araçlar (`tools/` dizini)

Repoda skill'lerin yanında `tools/` dizini de var. Bu araçlar skill'lerin çalışması için yardımcı:
- Web scraping araçları (Puppeteer/tarayıcı)
- Görsel üretim araçları
- Veri analiz script'leri
- PDF raporlama

Bizim `scripts/` dizinimize benzer bir yapı.

---

## Önerilen Entegrasyon Yol Haritası

1. **Önce `product-marketing` skill'ini ekle** — tüm sistemin temeli. Bu olmadan diğer skill'lerin yarısı çalışmaz.

2. **`marketing-plan` skill'ini ekle** — tüm skill'leri AARRR çatısı altında koordine eden ana plan.

3. **Bizde eksik olan CRO setini ekle**: `cro`, `signup`, `onboarding`, `paywalls` (popups opsiyonel).

4. **Bizde eksik olan Content setini ekle**: `copywriting`, `copy-editing` (video, image, sms alt öncelikli).

5. **SEO setini tamamla**: `ai-seo`, `schema`, `competitors` (SEO alternatif sayfası).

6. **Sales setini ekle**: `sales-enablement`, `pricing`, `prospecting`.

7. **Growth setini ekle**: `referrals`, `churn-prevention`.

8. **Strateji setini tamamla**: `marketing-psychology`, `marketing-ideas`.

**Toplamda ~20-25 yeni skill entegre edilebilir.** Önceliklendirmeyi sen yap, ben sırayla yazayım.
