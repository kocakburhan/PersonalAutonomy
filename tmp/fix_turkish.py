import re

with open('docs/superpowers/plans/2026-05-27-personalautonomy-plan.md', 'rb') as f:
    data = f.read()
text = data.decode('utf-8', errors='replace')

FF = '\ufffd'

# ====== PHASE 1: Fix box-drawing architecture section ======
box_fixes = [
    # Line 7466: →�  →  │  (vertical line connector)
    ("    →\ufffd\n", "    │\n"),
    # Line 7480: box top border: 31 FFFD → ┌──...──┐
    ("    →-    →  -" + FF*31, "    →-    →  ┌─────────────────────────────┐"),
    # Line 7496: box bottom border: 30 FFFD → └──...──┘
    ("    →-    →  L" + FF*30 + "-", "    →-    →  └─────────────────────────────┘"),
    # Line 7498: →L�� → →└──
    ("→L" + FF*2, "→└──"),
]

for old, new in box_fixes:
    if old in text:
        text = text.replace(old, new)
    else:
        pass

remaining = text.count(FF)

# ====== PHASE 2: Fix Turkish word corruptions ======
# Read all unique corrupted words from current text state
word_freq = {}
for line in text.split('\n'):
    if FF in line:
        for m in re.finditer(r'\S*\ufffd\S*', line):
            w = m.group()
            word_freq[w] = word_freq.get(w, 0) + 1

sorted_wf = sorted(word_freq.items(), key=lambda x: -x[1])

WORD_MAP = {
    # Sort by approximate frequency
    "g\uFFFDrsel": "görsel",
    "m\uFFFD?": "mı?",
    "Kullan\uFFFDc\uFFFDya": "Kullanıcıya",
    "t\uFFFDm": "tüm",
    "i\uFFFDin": "için",
    "g\uFFFDrseli": "görseli",
    "g\uFFFDr selleri": "görselleri",
    "yap\uFFFDlacak.": "yapılacak.",
    "\uFFFDzel": "özel",
    "a\uFFFDamas\uFFFDnda": "aşamasında",
    "\uFFFDretimi": "üretimi",
    "Kullan\uFFFDc\uFFFD": "Kullanıcı",
    "\uFFFDretmemi": "üretmemi",
    "onayl\uFFFDyor": "onaylıyor",
    "ka\uFFFD\uFFFDrmaktan": "kaçırmaktan",
    "s\uFFFDk\uFFFDld\uFFFDn": "sıkıldın",
    "T\uFFFDm": "Tüm",
    "\"Payla\uFFFD\uFFFDmlar\"": "\"Paylaşımlar\"",
    "Kullan\uFFFDc\uFFFDn\uFFFDn": "Kullanıcının",
    "g\uFFFDrnderileri": "gönderileri",
    "g\uFFFDnden": "günden",
    "**Kullan\uFFFDc\uFFFDya": "**Kullanıcıya",
    "**T\uFFFDr:**": "**Tür:**",
    "**G\uFFFDrsel:**": "**Görsel:**",
    "Payla\uFFFD\uFFFDld\uFFFD": "Paylaşıldı",
    "g\uFFFDre": "göre",
    "g\uFFFDnl\uFFFDk": "günlük",
    "d\uFFFDzg\uFFFDn": "düzgün",
    "haftal\uFFFDk": "haftalık",
    "kapsaml\uFFFD": "kapsamlı",
    "\uFFFDretiliyor": "üretiliyor",
    "olu\uFFFDuyor": "oluşuyor",
    "konfig\uFFFDrrasyonuna": "konfigürasyonuna",
    "tan\uFFFDm\uFFFD": "tanımı",
    "dosyas\uFFFDna": "dosyasına",
    "mekanizmas\uFFFDn\uFFFD": "mekanizmasını",
    "yan\uFFFDt": "yanıt",
    "vermedi\uFFFDinde": "vermediğinde",
    "d\uFFFD\uFFFD\uFFFDyor": "düşüyor",
    "olu\uFFFDur,": "oluşur,",
    "olu\uFFFDtur,": "oluştur,",
    "do\uFFFDru": "doğru",
    "\uFFFDal\uFFFD\uFFFDyor": "çalışıyor",
    "aras\uFFFD": "arası",
    "haf\uFFFDza**": "hafıza**",
    "Ayn\uFFFD": "Aynı",
    "kullan\uFFFDc\uFFFD": "kullanıcı",
    "geldi\uFFFDinde": "geldiğinde",
    "\uFFFDnceki": "Önceki",
    "hat\uFFFDrl\uFFFDyor": "hatırlıyor",
    "olu\uFFFDtur**": "oluştur**",
    "**Kullan\uFFFDc\uFFFD": "**Kullanıcı",
    "dok\uFFFDmantasyonu": "dokümantasyonu",
    "i\uFFFDe": "işe",
    "g\uFFFDzden": "gözden",
    "ge\uFFFDir)": "geçir)",
    "buldu\uFFFDun": "bulduğun",
    "di\uFFFDer": "diğer",
    "repolar\uFFFDn\uFFFD": "repolarını",
    "al\uFFFDnd\uFFFDktan": "alındıktan",
    "\uFFFDimdilik": "şimdilik",
    "G\uFFFDncellemesi:": "Güncellemesi:",
    "tan\uFFFDmlar\uFFFD": "tanımları",
    "tamamland\uFFFD.": "tamamlandı.",
    "alt\uFFFDnda": "altında",
    "Kald\uFFFDr\uFFFDlan": "Kaldırılan",
    "de\uFFFDi\uFFFDtirildi):": "değiştirildi):",
    "yap\uFFFDlacaklar": "yapılacaklar",
    "al\uFFFDn\uFFFDnca": "alınınca",
    "De\uFFFDil": "Değil",
    "\uFFFDretiyorlar.": "üretiyorlar.",
    "geli\uFFFDtirme": "geliştirme",
    "Konu\uFFFDarak": "Konuşarak",
    "\uFFFD\uFFFDerik": "İçerik",
    "**Ama\uFFFD:**": "**Amaç:**",
    "konu\uFFFDuyor.": "konuşuyor.",
    "Ayr\uFFFD": "Ayrı",
    "ayr\uFFFD": "ayrı",
    "atmas\uFFFDna": "atmasına",
    "Ak\uFFFD\uFFFD": "Akış",
    "do\uFFFDal": "doğal",
    "i\uFFFDinde": "içinde",
    "de\uFFFDil,": "değil,",
    "i\uFFFDbirli\uFFFDii\"": "işbirliği\"",
    "\"Bug\uFFFDnk\uFFFD": "\"Bugünkü",
    "g\uFFFDrnderisini": "gönderisini",
    "haz\uFFFDrlayal\uFFFDm\"": "hazırlayalım\"",
    "g\uFFFDrnderiyi": "gönderiyi",
    "\"Bug\uFFFDn": "\"Bugün",
    "e\uFFFDitim": "eğitim",
    "i\uFFFDeri\uFFFDii": "içeriği",
    "\uFFFDr\uFFFDn": "ürün",
    "tan\uFFFDt\uFFFDm\uFFFD": "tanıtımı",
    "noktam\uFFFDz:": "noktamız:",
    "\uFFFDzelli\uFFFDinin": "özelliğinin",
    "lansman\uFFFD.": "lansmanı.",
    "\uFFFDretir": "üretir",
    "\uFFFDaa\uFFFDr\uFFFDs\uFFFD": "çağrısı",
    "G\uFFFDnderin": "Gönderin",
    "Haz\uFFFDr!": "Hazır!",
    "aray\uFFFDz\uFFFDnden": "arayüzünden",
    "Onaylan\uFFFDnca": "Onaylanınca",
    "payla\uFFFD\uFFFDr": "paylaşır",
    "Bile\uFFFDenler": "Bileşenler",
    "Bile\uFFFDen": "Bileşen",
    "A\uFFFD\uFFFDklama": "Açıklama",
    "ak\uFFFD\uFFFD\uFFFD": "akışı",
    "y\uFFFDneten": "yöneten",
    "agent'\uFFFD": "agent'ı",
    "ge\uFFFDmi\uFFFD": "geçmiş",
    "g\uFFFDrnderilerin": "gönderilerin",
    "g\uFFFDrnderide": "gönderide",
    "yaz\uFFFDl\uFFFDr.": "yazılır.",
    "k\uFFFDk": "kök",
    "\uFFFDretilen": "üretilen",
    "indirebildi\uFFFDii": "indirebildiği",
    "dolmas\uFFFDn).": "dolmasın).",
    "davran\uFFFD\uFFFD": "davranış",
    "kurallar\uFFFD": "kuralları",
    "kullan\uFFFDc\uFFFDlar": "kullanıcılar",
    "i\uFFFDindir.": "içindir.",
    "\uFFFDretebilirsin\"": "üretebilirsin\"",
    "\uFFFD\uFFFDi": "İşi",
    "\uFFFDok": "çok",
    "i\uFFFD": "iş",
    "**Ge\uFFFDmi\uFFFDi": "**Geçmişi",
    "ayn\uFFFD": "aynı",
    "\uFFFDeyi": "şeyi",
    "**Ba\uFFFDlam\uFFFD": "**Bağlamı",
    "\uFFFDr\uFFFDn\uFFFD,": "ürünü,",
    "G\uFFFDnderi": "Gönderi",
    "oldu\uFFFDunda": "olduğunda",
    "d\uFFFDzenli": "düzenli",
    "y\uFFFDnlendir.**": "yönlendir.**",
    "\"Payla\uFFFD\uFFFDmlar": "\"Paylaşımlar",
    "**T\uFFFDrk\uFFFDe": "**Türkçe",
    "konu\uFFFD.**": "konuş.**",
    "ileti\uFFFDim": "iletişim",
    "T\uFFFDrk\uFFFDe.": "Türkçe.",
    "format\uFFFD\uFFFD": "formatı",
    "E\uFFFDitim": "Eğitim",
    "\uFFFD\uFFFDte": "İşte",
    "ad\uFFFDmda...": "adımda...",
    "kan\uFFFDt": "kanıt",
    "M\uFFFD\uFFFDterimiz": "Müşterimiz",
    "kazand\uFFFD...": "kazandı...",
    "#ba\uFFFDar\uFFFD": "#başarı",
    "#m\uFFFD\uFFFDteri": "#müşteri",
    "Kullan\uFFFDm:": "Kullanım:",
    "g\uFFFDrnderilerini": "gönderilerini",
    "t\uFFFDr,": "tür,",
    "\uFFFDnizlemesi": "önizlemesi",
    "\"Payla\uFFFD\uFFFDld\uFFFD\"": "\"Paylaşıldı\"",
    "i\uFFFDareti": "işareti",
    "tasar\uFFFDm": "tasarım",
    "i\uFFFDlem": "işlem",
    "kullan\uFFFDlaca\uFFFD\uFFFD": "kullanılacağı",
    "kararla\uFFFDt\uFFFDr\uFFFDlacakt\uFFFDr.": "kararlaştırılacaktır.",
    "Se\uFFFDim": "Seçim",
    "uyumlulu\uFFFDu,": "uyumluluğu,",
    "kolayl\uFFFD\uFFFD\uFFFD.": "kolaylığı.",
    "Yukar\uFFFDdaki": "Yukarıdaki",
    "\uFFFDrnekleri": "örnekleri",
    "ama\uFFFDl\uFFFDd\uFFFDr,": "amaçlıdır,",
    "se\uFFFDilen": "seçilen",
    "g\uFFFDncellenecektir.": "güncellenecektir.",
    # Şu / Bu context fixes
    "\"Bu anki": "\"Şu anki",
    "Bu kurallara": "Şu kurallara",
    # Edge case: Görsel
    "G\uFFFDrsel:": "Görsel:",
    "g\uFFFDrseli": "görseli",
    # The standalone Görsel
    "G\uFFFDrseli": "Görseli",
    "g\uFFFDster.**": "göster.**",
    # arayüz
    "aray\uFFFDz.": "arayüz.",
    # değil?
    "de\uFFFDil?": "değil?",
    # lowercase
    "g\uFFFDre,": "göre,",
}

# Apply all word replacements - sort by length descending for correctness
sorted_words = sorted(WORD_MAP.items(), key=lambda x: -len(x[0]))
for old, new in sorted_words:
    text = text.replace(old, new)

# ====== PHASE 3: Fix remaining standalone FFFD ======
remaining = text.count(FF)

# Replace ALL remaining FFFD with em dash
text = text.replace(FF, '—')

# Verify
assert text.count(FF) == 0

# Write back
data = text.encode('utf-8')
with open('docs/superpowers/plans/2026-05-27-personalautonomy-plan.md', 'wb') as f:
    f.write(data)

# Summary
original_fffd = data.count(b'\xef\xbf\xbd')
print(f"Written. Total FFFD now: {original_fffd}")
