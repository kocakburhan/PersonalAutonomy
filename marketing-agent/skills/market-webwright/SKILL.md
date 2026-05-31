# market-webwright — Web Scraping Bridge

Bu skill marketing agent ile Webwright browser agent arasinda kopru gorevi gorur. Webwright'i dogru parametrelerle cagirir, sonuclari parse eder ve ust skill'lere iletir.

---

## Webwright Nedir?

Microsoft'un Playwright tabanli LLM-driven browser agent'i. LLM'e terminal verir, LLM Playwright script'i yazarak siteyi tarar. Her tarama yeniden calistirilabilir `.py` dosyasidir.

**Repo:** `https://github.com/microsoft/Webwright`
**Kurulum:** `pip install -e vendor/webwright && playwright install chromium`
**API Key:** GEREKMEZ — OpenCode host agent olarak native surer.

---

## Komutlar

### `/webwright:run <task>`
Tek seferlik tarama. Verilen gorevi yerine getirir, `final_script.py` uretir.

### `/webwright:craft <task>`
Parametrik CLI tool uretir. Uretilen `.py` dosyasi farkli parametrelerle tekrar calistirilabilir.

---

## Marketing Kullanim Desenleri

### Desen 1: Sayfa Analizi (SEO, Brand, Report)
```bash
/webwright:run "https://example.com sayfasini ac. Title, meta description, tum H1/H2/H3 basliklarini, buton metinlerini, form sayisini, gorsel alt tag'lerini JSON olarak cikar."
```

### Desen 2: Rakip Tarama (Competitors)
```bash
/webwright:craft "ac {site} sayfasini. Pricing sayfasini bul ve tikla. Tum plan isimlerini, fiyatlarini, ozellik listelerini tablo olarak cikar."
# Sonra: python final_script.py --site "https://rakip1.com"
```

### Desen 3: Funnel Walk (Funnel, CRO)
```bash
/webwright:run "https://example.com ac. Ana sayfadan basla → Sign Up tikla → formu bos birak submit et → hata mesajlarini kaydet → geri don → Pricing tikla → ekran goruntusu al."
```

### Desen 4: Multi-Site Karsilastirma (Competitors, Report)
```bash
/webwright:run "Su siteleri sirayla ac ve her birinden title, meta, H1, CTA metinlerini topla: https://site1.com, https://site2.com, https://site3.com. Sonuclari karsilastirmali tablo yap."
```

---

## Entegrasyon Kurallari

1. **Once bu skill'i cagir** — URL'li her marketing gorevinde ilk adim Webwright ile veri toplamak
2. **Sonra ust skill'e gec** — Toplanan veriyi `market-seo`, `market-competitors` vb. skill'lere input olarak ver
3. **Fallback zinciri:** Webwright → WebFetch (statik sayfalar)
4. **Sonuclari kaydet** — Webwright ciktisini `outputs/{task-id}/` altinda sakla
5. **Craft tercih et** — Ayni tur is tekrarlanacaksa `/webwright:craft` kullan, parametrik tool uret

---

## Ornek Akis

```
Kullanici: "/market competitors rakip1.com rakip2.com"

Agent:
1. /webwright:craft "ac {url} sitesini → pricing sayfasini bul → plan ve fiyatlari cikar"
2. python final_script.py --url "rakip1.com"  → rakip1.json
3. python final_script.py --url "rakip2.com"  → rakip2.json
4. market-competitors SKILL.md oku → raporu olustur
5. COMPETITOR-REPORT.md kaydet
```
