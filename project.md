prd üretecek skill de dahil olmak üzere marketer için tanımlı olan skill ve agentlar bir pipeline'a oturtulması lazım. Burada mareketer olan kullanıcılar ne yapacaklarına karar vermemeli, sistem onları adım adım yönlendirmeli onlar sadece belirlenen süreç içerisinde karar mekanizması olmalıdır. Şu anda skiller birbirlerinden bağımsız. Bunlar çoklu agentlarca toparlanamlı ve adım adım agentlar birbirine context paslamalı ve kendilerine uygun olan skilleri zorunlu olarak bu agentlar kullanmalı. Bu yapıyı oturtmamız gerekiyor.

---

Coder agentına gerek yok. Onu coder olan kişi kendisi projeye özgü bir şekilde yapacak zaten. Biz şu anda marketer'a odaklanalım. Coder'ı düşünmeyeceğiz o kendi işini kendisi görecek.

---

Onboarding skilli bence de muhakkak olmalı. Sistemi detaylıca bilen ve kullanıcının kafasının karıştığı yerde kullanıcıyı yönlendirmelidir bu skill.

---


Şu anda sadece marketer'lar için süreci otonomlaştırıyoruz. Burada aklımdaki yapı şu: Orchastrater agent yazalım. Bunun altına da süreci parça parça yöneten agentlar tanımlayalım. Kullanıcı orchastrator agent ile diyaloğa geçsin orchastrator diğer agentları yönetsin. Kullanıcıya detaylı feedbackler versin kullanıcıya kararları sorsun. Kullanıcıdan akıl alsın vs vs. orchastrator'un altındaki agentlar da tanımlı skilleri kullansınlar iş yapsınlar orchastrator'a rapor versinler. Yani kullanıcı bir pazarlama şirketi patronu gibi olsun. orchastrator bu şirketin müdürü ve kullanıcıyla iletişime geçen kullanıcıdan akıl alan kişi olsun. Diğer agentlar da bu pazarlama şirketinde çalışan kişiler gibi olsun her birinin farklı görevleri olsun. orchastrator bunların çalışmasını düzenlesin pipeline'ı ayarlasın vs. 


---


Senden istediğim şey şu aslında: Kurmak istediğim yapıyı yukarıda detaylıca anlattım sana, ancak ben de pazarlama nasıl yapılır akış nasıl olmalıdır, agentlar nasıl olmalı vs bilemiyorum. Sadece @marketing-agent\skills/ dosyasındaki skilleri buldum ancak ürün pazarlama sürecinde doğru adımlar nelerdir bunu ben de bilmiyorum. Senden istediğim şey bu skilleri kullanan bir agentic mimari kurman. Marketer kullanıcı elinin altında büyülü bir sistem olduğunu hissetsin. Bu sistemler fikir bulsun geliştirsin. prd yazdırsın. coderdan aldığı mvp'yi test etsin. kapsamlı analizler yaptırsın, kapsamlı analizlere göre tekrar coder'a raporlar versin coder'a uygun istekler versin. gerektiği yerde sistem kullanıcıya desin ki benim şu bilgilere ihtiyacım var. Coder'dan bu bilgileri içeren bir rapor iste ve bu raporu bana ver desin.

---

Marketer kullanıcı opencode kullanarak kusursuz bir file yapısında bu akışı hem uygulayabilsin hem de dosyalayabilsin. Oturumlar içerisinde alınan kararlar yapılan işlemler vs her neyse yani projede yapılanlar her neyse opencode bunları unutmasın bunlar da sistemde kayıtlı olsun istiyorum.

---

Marketer kullanıcı bu yapıdan soyutlansın ve sadece işine baksın. Sistem onu yönlendirsin istiyorum.

---


Örnek bir akış vereyim sana: sistem app store'daki son 1 haftada en çok para kazandıran 10 appi bulur, kategorilere ayırır. Diyelim ki bu 10 appin 3'ü kişisel bakım app'i olsun. Bu applerin ne yaptıkları sistem tarafından analiz edilir, sonrasında sistem bu applerdeki olumsuz değerlendirmeleri okur ve insanların applerdeki memnuniyetsizliklerini analiz eder. sistem olumlu yorumları okur ve sistemdeki insanların neyden memnun olduklarını belirler. Sonrasında bu 3 appin karışımı bir fikir üretir, bu fikir hem memnun kullanıcılara hem de olumsuz yorum yazan memnuniyetsiz kullanıcıların problemlerini çözer ve yükselişte olan kişisel bakım konusunda fikir üretir. Üretilen bu fikir marketer ile sohbet edilerek tartışılarak son hale getirilir ve prd yazılır. Bu prd coder'a verilir mvp gerçekleştirilir ve marketer bu sefer pazarlama süreçlerini sistem ile yani opencode ile konuşarak gerçekleştirir. Sosyal medya kısmını opencode ile çözer. Pazarlama stratejisini opencode ile çözer vs vs. Kullanıcı insanlardan feedback toplamaya çalışır, insnaların bu konuya ilgisi var mı yok mu bunu tespit etmeye çalışır. Marketer bu sistemle beraber insnaların feedbackini de toparladıktan sonra sistemi de kullanrak coder'a verilecek olan proje detaylarını proje isterlerini belirler. Coder'a bu isterler iletilir. Coder yazılımı yapar. Bu yazılımı marketer'a verir. Marketer birmiş yazılımı yine sistemi kullanarak pazarlamaya çalışır. 

Yukarıda örnek bir akış yer almaktadır (Bu örnek akışı detaylıca @pipeline-example.md dosyasına yaz.) Bu akış gibi birçok akış planlanmalıdır ve sadece app değil her türlü yazılım fikri değerlendirilmelidir. Ürünün yazılım ürünü olması yeterlidir, eğer ihtiyaç varsa ürün içerisinde donanımsal bileşenler içeren karma bir ürün de olabilir. Dolayısıyla araştırma kısmı sadece app store'da değil forumlarda redditte vs de olmalıdır. 