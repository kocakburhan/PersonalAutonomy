import re, sys

with open('docs/superpowers/plans/2026-05-27-personalautonomy-plan.md', 'rb') as f:
    data = f.read()
text = data.decode('utf-8', errors='replace')

FF = '\ufffd'
total_before = text.count(FF)
print(f"Total FFFD before: {total_before}")

# ====== PHASE 1: Fix box-drawing architecture section ======
# These are long runs of FFFD that are NOT Turkish chars
box_fixes = {
    # Line 7466: →FF  →  │  (vertical line, tree branch connector)
    "    →" + FF + "\n": "    │\n",
    # Line 7480: top border of box
    "    →-    →  -" + FF*31: "    →-    →  ┌─────────────────────────────┐",
    # Line 7496: bottom border of box
    "    →-    →  L" + FF*30 + "-": "    →-    →  └─────────────────────────────┘",
    # Line 7498: →LFF → →└──
    "→L" + FF*2: "→└──",
    # Line 7469-7497: +FF 10 times → +──
    # But careful: only in architecture section, not in regular text
}
for old, new in box_fixes.items():
    if old in text:
        text = text.replace(old, new)

# Fix +FF → +── (only 10 occurrences, all in architecture diagram)
text = text.replace("+" + FF*2, "+──")
# Fix LFF → └── (only 1 occurrence after the +FF fix)
# Already handled above

remaining = text.count(FF)
fixed = total_before - remaining
print(f"After box fixes: {remaining} FFFD (fixed {fixed})")

# ====== PHASE 2: Turkish word mapping ======
word_map = {
    # question particles (gotta be careful with context)
    "m" + FF + "?": "mı?",
    "m" + FF: "mı",
    # common words
    "i" + FF + "in": "için",
    "g" + FF + "rsel": "görsel",
    "g" + FF + "rseli": "görseli",
    "g" + FF + "rselleri": "görselleri",
    "g" + FF + "nderileri": "gönderileri",
    "g" + FF + "nderilerin": "gönderilerin",
    "g" + FF + "nderide": "gönderide",
    "g" + FF + "nderisini": "gönderisini",
    "g" + FF + "nderiyi": "gönderiyi",
    "g" + FF + "nderilerini": "gönderilerini",
    "g" + FF + "nderi": "gönderi",
    "g" + FF + "nderi:": "gönderi:",
    "g" + FF + "nderin": "gönderin",
    "g" + FF + "nden": "günden",
    "g" + FF + "nl" + FF + "k": "günlük",
    "g" + FF + "re": "göre",
    "g" + FF + "re,": "göre,",
    "g" + FF + "rsel:": "görsel:",
    "g" + FF + "rseli": "görseli",
    "g" + FF + "zden": "gözden",
    "g" + FF + "ster.**": "göster.**",
    "g" + FF + "ster.": "göster.",
    "do" + FF + "ru": "doğru",
    "Do" + FF + "ru": "Doğru",
    "Do" + FF + "rulama": "Doğrulama",
    "do" + FF + "al": "doğal",
    "t" + FF + "m": "tüm",
    "T" + FF + "m": "Tüm",
    "t" + FF + "r,": "tür,",
    "t" + FF + "ketimini": "tüketimini",
    ## Kullanıcı variations
    "Kullan" + FF + "c" + FF: "Kullanıcı",
    "Kullan" + FF + "c" + FF + "ya": "Kullanıcıya",
    "Kullan" + FF + "c" + FF + "n" + FF + "n": "Kullanıcının",
    "**Kullan" + FF + "c" + FF + "ya": "**Kullanıcıya",
    "**Kullan" + FF + "c" + FF: "**Kullanıcı",
    "kullan" + FF + "c" + FF: "kullanıcı",
    "kullan" + FF + "c" + FF + "lar": "kullanıcılar",
    ## yapılacak variations
    "yap" + FF + "lacak.": "yapılacak.",
    "yap" + FF + "lacaklar": "yapılacaklar",
    "yap" + FF + "yor?": "yapıyor?",
    ## özel, üretim variations
    "" + FF + "zel": "özel",
    "" + FF + "retimi": "üretimi",
    "" + FF + "retmemi": "üretmemi",
    "" + FF + "retiliyor": "üretiliyor",
    "" + FF + "retiyorlar.": "üretiyorlar.",
    "" + FF + "retir": "üretir",
    "" + FF + "retilen": "üretilen",
    "" + FF + "retebilirsin\"": "üretebilirsin\"",
    ## aşama, tanım etc
    "a" + FF + "amas" + FF + "nda": "aşamasında",
    "tan" + FF + "m": "tanım",
    "tan" + FF + "m" + FF: "tanımı",
    "tan" + FF + "mlar" + FF: "tanımları",
    "tan" + FF + "t" + FF + "m" + FF: "tanıtımı",
    "tan" + FF + "mla**": "tanımla**",
    "dosyas" + FF + "na": "dosyasına",
    "dosyalar" + FF: "dosyaları",
    "**Dosyalar" + FF: "**Dosyaları",
    ## mekanizma, yanıt etc
    "mekanizmas" + FF + "n" + FF: "mekanizmasını",
    "yan" + FF + "t": "yanıt",
    "vermedi" + FF + "inde": "vermediğinde",
    "d" + FF + FF + FF + "yor": "düşüyor",
    "olu" + FF + "uyor": "oluşuyor",
    "olu" + FF + "ur,": "oluşur,",
    "olu" + FF + "tur": "oluştur",
    "olu" + FF + "tur,": "oluştur,",
    "olu" + FF + "tur**": "oluştur**",
    "olu" + FF + "turma,": "oluşturma,",
    ## çalış variations
    "" + FF + "al" + FF + FF + "yor": "çalışıyor",
    "" + FF + "al" + FF + "t" + FF + "r": "çalıştır",
    "" + FF + "al" + FF + "t" + FF + "r,": "çalıştır,",
    "" + FF + "al" + FF + "ma": "çalışma",
    ## arası, hafıza
    "aras" + FF: "arası",
    "haf" + FF + "za**": "hafıza**",
    "Ayn" + FF: "Aynı",
    "kullan" + FF + "m" + FF + "n" + FF: "kullanımını",
    "kullan" + FF + "m" + FF + "**": "kullanımı**",
    "kullan" + FF + "m" + FF: "kullanımı",
    "geldi" + FF + "inde": "geldiğinde",
    "" + FF + "nceki": "Önceki",
    "hat" + FF + "rl" + FF + "yor": "hatırlıyor",
    "rol" + FF: "rolü",
    "Yap" + FF + "land" + FF + "rmas" + FF: "Yapılandırması",
    ## Paylaş variations
    "\"Payla" + FF + FF + "mlar\"": "\"Paylaşımlar\"",
    "'Payla" + FF + FF + "mlar'": "'Paylaşımlar'",
    "\"Payla" + FF + FF + "mlar": "\"Paylaşımlar",
    "Payla" + FF + FF + "ld" + FF: "Paylaşıldı",
    "\"Payla" + FF + FF + "ld" + FF + "\"": "\"Paylaşıldı\"",
    "payla" + FF + FF + "r": "paylaşır",
    ## is, iste, isleri etc
    "" + FF + FF + "i": "İşi",
    "" + FF + "ok": "çok",
    "i" + FF: "iş",
    "i" + FF + "e": "işe",
    "i" + FF + "areti": "işareti",
    "i" + FF + "lem": "işlem",
    "**Ge" + FF + "mi" + FF + "i": "**Geçmişi",
    "ayn" + FF: "aynı",
    "" + FF + "eyi": "şeyi",
    "**Ba" + FF + "lam" + FF: "**Bağlamı",
    "" + FF + "r" + FF + "n": "ürün",
    "" + FF + "r" + FF + "n" + FF + ",": "ürünü,",
    "" + FF + "r" + FF + "n" + FF + "\"": "ürünü\"",
    "G" + FF + "nderi": "Gönderi",
    "G" + FF + "rsel": "Görsel",
    "G" + FF + "rsel:": "Görsel:",
    "G" + FF + "rseli": "Görseli",
    "G" + FF + "nderin": "Gönderin",
    "oldu" + FF + "unda": "olduğunda",
    "d" + FF + "zenli": "düzenli",
    "y" + FF + "nlendir.**": "yönlendir.**",
    "**T" + FF + "rk" + FF + "e": "**Türkçe",
    "T" + FF + "rk" + FF + "e.": "Türkçe.",
    "T" + FF + "rk" + FF + "e,": "Türkçe,",
    "konu" + FF + ".**": "konuş.**",
    "ileti" + FF + "im": "iletişim",
    "format" + FF: "formatı",
    "E" + FF + "itim": "Eğitim",
    "" + FF + FF + "te": "İşte",
    "ad" + FF + "mda...": "adımda...",
    "kan" + FF + "t": "kanıt",
    "M" + FF + FF + "terimiz": "Müşterimiz",
    "kazand" + FF + "...": "kazandı...",
    "#ba" + FF + "ar" + FF: "#başarı",
    "#m" + FF + FF + "teri": "#müşteri",
    "Kullan" + FF + "m:": "Kullanım:",
    "" + FF + "nizlemesi": "önizlemesi",
    "tasar" + FF + "m": "tasarım",
    "kullan" + FF + "laca" + FF + FF: "kullanılacağı",
    "kararla" + FF + "t" + FF + "r" + FF + "lacakt" + FF + "r.": "kararlaştırılacaktır.",
    "Se" + FF + "im": "Seçim",
    "uyumlulu" + FF + "u,": "uyumluluğu,",
    "kolayl" + FF + FF + FF + ".": "kolaylığı.",
    "Yukar" + FF + "daki": "Yukarıdaki",
    "" + FF + "rnekleri": "örnekleri",
    "ama" + FF + "l" + FF + "d" + FF + "r,": "amaçlıdır,",
    "se" + FF + "ilen": "seçilen",
    "g" + FF + "ncellenecektir.": "güncellenecektir.",
    ## dokümantasyon
    "dok" + FF + "mantasyon": "dokümantasyon",
    "dok" + FF + "mantasyonu": "dokümantasyonu",
    "Dok" + FF + "mantasyon": "Dokümantasyon",
    ## geç
    "ge" + FF + "ir)": "geçir)",
    "ge" + FF + "mi" + FF: "geçmiş",
    "ge" + FF + "mi" + FF + "i": "geçmişi",
    "Ge" + FF + "ersiz": "Geçersiz",
    ## diğer, bulduğun
    "di" + FF + "er": "diğer",
    "buldu" + FF + "un": "bulduğun",
    "repolar" + FF + "n" + FF: "repolarını",
    ## alın, şimdi
    "al" + FF + "nd" + FF + "ktan": "alındıktan",
    "al" + FF + "n" + FF + "nca": "alınınca",
    "" + FF + "imdilik": "şimdilik",
    ## Güncelleme
    "G" + FF + "ncellemesi:": "Güncellemesi:",
    "tamamland" + FF + ".": "tamamlandı.",
    "alt" + FF + "nda": "altında",
    "Kald" + FF + "r" + FF + "lan": "Kaldırılan",
    "de" + FF + "i" + FF + "tirildi):": "değiştirildi):",
    "de" + FF + "il": "değil",
    "de" + FF + "ilse": "değilse",
    "de" + FF + "il?": "değil?",
    "de" + FF + "il,": "değil,",
    ## hazır
    "haz" + FF + "r": "hazır",
    "haz" + FF + "r.": "hazır.",
    "haz" + FF + "rlayal" + FF + "m\"": "hazırlayalım\"",
    "Haz" + FF + "r!": "Hazır!",
    ## Tutarlı
    "tutarl" + FF: "tutarlı",
    "**Tutarl" + FF + "l" + FF + "k": "**Tutarlılık",
    "farkl" + FF: "farklı",
    ## konuş variations  
    "konu" + FF + "uyor.": "konuşuyor.",
    "Konu" + FF + "arak": "Konuşarak",
    ## Ayrı
    "Ayr" + FF: "Ayrı",
    "ayr" + FF: "ayrı",
    "atmas" + FF + "na": "atmasına",
    "Ak" + FF + FF: "Akış",
    ## iç
    "i" + FF + "inde": "içinde",
    "i" + FF + "indir.": "içindir.",
    "i" + FF + "erik": "içerik",
    "" + FF + FF + "erik": "içerik",  # same but no preceding char
    "i" + FF + "eri" + FF + "i": "içeriği",
    "i" + FF + "birli" + FF + "i\"": "işbirliği\"",
    ## Bugün
    "\"Bug" + FF + "nk" + FF: "\"Bugünkü",
    "\"Bug" + FF + "n": "\"Bugün",
    ## eğitim
    "e" + FF + "itim": "eğitim",
    ## Şu
    "\"" + FF + "u": "\"Şu",
    "" + FF + "u": "Şu",
    ## nokta, özellik
    "noktam" + FF + "z:": "noktamız:",
    "" + FF + "zelli" + FF + "inin": "özelliğinin",
    "lansman" + FF + ".": "lansmanı.",
    ## çağrı, arayüz
    "" + FF + "a" + FF + "r" + FF + "s" + FF: "çağrısı",
    "aray" + FF + "z" + FF + "nden": "arayüzünden",
    "aray" + FF + "z.": "arayüz.",
    ## Bileşen
    "Bile" + FF + "denler": "Bileşenler",
    "Bile" + FF + "den": "Bileşen",
    "A" + FF + FF + "klama": "Açıklama",
    "ak" + FF + FF + FF: "akışı",
    "y" + FF + "neten": "yöneten",
    "y" + FF + "netimi,": "yönetimi,",
    "agent'" + FF: "agent'ı",
    "yaz" + FF + "l" + FF + "r.": "yazılır.",
    "k" + FF + "k": "kök",
    "al" + FF + "r": "alır",
    "al" + FF + "r,": "alır,",
    "indirebildi" + FF + "i": "indirebildiği",
    "dolmas" + FF + "n).": "dolmasın).",
    "davran" + FF + FF: "davranış",
    "kurallar" + FF: "kuralları",
    "eksik/hatal" + FF: "eksik/hatalı",
    "" + FF + FF + "kan": "çıkan",
    "d" + FF + "zelt": "düzelt",
    "b" + FF + "y" + FF + "k": "büyük",
    "ba" + FF + FF + "ml" + FF + "l" + FF + "klar" + FF + "n" + FF: "bağımlılıklarını",
    "y" + FF + "kle**": "yükle**",
    "" + FF + "l" + FF + "**": "ölç**",
    "Onaylan" + FF + "nca": "Onaylanınca",
    ## misc
    "mant" + FF + "kl" + FF: "mantıklı",
    "" + FF + FF + "kt" + FF + "s" + FF: "çıktısı",
    "" + FF + FF + "kt" + FF + "lar": "çıktılar",
    "" + FF + FF + "kt" + FF + "da": "çıktıda",
    "" + FF + FF + "kt" + FF + "lar" + FF + "n" + FF: "çıktılarını",
    "" + FF + FF + "kt" + FF + "s" + FF + "ndan": "çıktısından",
    "m" + FF + FF + "teriye": "müşteriye",
    "" + FF + "nerileri**": "önerileri**",
    "" + FF + "neriyor": "öneriyor",
    "s" + FF + "ylemeden": "söylemeden",
    "kullanaca" + FF + FF + "n" + FF: "kullanacağını",
    "bo" + FF: "boş",
    "durumlar" + FF + "n" + FF: "durumlarını",
    "zarif" + FF + "e": "zarifçe",
    "sald" + FF + "r" + FF + "s" + FF: "saldırısı",
    "d" + FF + "n" + FF + FF + FF + "m" + FF + "**": "dönüşümü**",
    "mesaj" + FF: "mesajı",
    "s" + FF + "r" + FF + "yor?": "sürüyor?",
    "y" + FF + "zeysel": "yüzeysel",
    ## row 7 misc  
    "Deste" + FF + "i": "Desteği",
    "" + FF + "u": "Şu",
    "\\\"" + FF + "u": "\"Şu",
    "\\\"Payla" + FF + FF + "mlar": "\"Paylaşımlar",
}

# Apply word mapping - sort by length descending
for old, new in sorted(word_map.items(), key=lambda x: -len(x[0])):
    text = text.replace(old, new)

remaining = text.count(FF)
fixed2 = total_before - text.count(FF) - fixed
print(f"After word mapping: {remaining} FFFD")

# ====== PHASE 3: Handle remaining standalone FFFD ======
# Only replace FFFD that are NOT part of any word (not adjacent to alphanum/quote/underscore)
# These are: em dashes, emojis, box chars
# We do it per-character position check
def is_word_char(c):
    return c.isalnum() or c in "'\"_"

result = []
i = 0
standalone_replaced = 0
while i < len(text):
    if text[i] == FF:
        # Check context
        prev_char = text[i-1] if i > 0 else '\n'
        next_char = text[i+1] if i < len(text)-1 else '\n'
        # FF is "in word" if adjacent to word char
        if is_word_char(prev_char) or is_word_char(next_char):
            # Still in word context - this means our map missed it
            result.append(FF)
        else:
            # Standalone - replace with em dash
            result.append('—')
            standalone_replaced += 1
    else:
        result.append(text[i])
    i += 1

text = ''.join(result)
print(f"Standalone FFFD → em dash: {standalone_replaced}")

# ====== FINAL VERIFY ======
remaining = text.count(FF)
print(f"\nFINAL FFFD count: {remaining}")

# Write
data = text.encode('utf-8')
if remaining == 0:
    with open('docs/superpowers/plans/2026-05-27-personalautonomy-plan.md', 'wb') as f:
        f.write(data)
    print("✅ Written to original file!")
    print(f"File size: {len(data)} bytes")
else:
    print(f"❌ Still have {remaining} FFFD remaining - need more mappings")
    # Write debug info
    with open('tmp/remaining_fffd.txt', 'w', encoding='utf-8') as out:
        for lineno, line in enumerate(text.split('\n'), 1):
            if FF in line:
                out.write(f"L{lineno}: {line[:200]}\n")
    print("Debug info written to tmp/remaining_fffd.txt")
