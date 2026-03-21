Bu çalışmada, yükseköğretim kurumlarının en karmaşık planlama 
problemlerinden biri olan Üniversite Ders Çizelgeleme Problemi için Yapay Zeka alt 
alanlarından biri olan Kısıt Sağlama Problemi (CSP) tekniklerine dayalı akıllı bir karar 
destek sistemi geliştirilmiştir. Ders programı hazırlama süreci; derslik kapasiteleri, 
öğretim elemanı müsaitlikleri ve çakışmasızlık gibi "katı" kısıtlar ile öğretim elemanı 
tercihleri gibi "esnek" kısıtların aynı anda yönetilmesini gerektiren, çözüm uzayının 
devasa olduğu NP-Zor (NP hard) sınıfında bir kombinatoryal optimizasyon 
problemidir. Çalışma kapsamında, Sembolik Yapay Zeka yaklaşımları temel alınarak 
problem modellenmiş ve çözüm uzayını akıllı arama algoritmaları ile tarayan bir motor 
geliştirilmiştir. Geliştirilen bu yapay zeka motoru, milyonlarca olası kombinasyon 
arasından kısıtları ihlal etmeyen optimum sonucu bulmayı hedefler. Sistemin 
kullanılabilirliğini artırmak amacıyla, veri yönetimi için SQLite tabanlı bir altyapı ve 
kullanıcı dostu bir arayüz tasarlanmıştır.

Editör:                      Visual Studio Code  
Programlama dili:   Python  
Veri tabanı:              SQLite  

Kullanılan kütüphaneler: 

• PyQt6:       Grafik kullanıcı arayüzü için  
• openpyxl:  Excel dosyası oluşturma ve formatlama için  
• pywin32:   Windows'ta Excel COM otomasyonu ile PDF dönüştürme için  
• sqlite3:       Veritabanı yönetimi için 
• json:           Veri serileştirme için  
• ortools:      Kısıt programlama ve optimizasyon motoru için 
