# Kamera Hareketi Algılama Web Uygulaması

## Proje Hakkında

Bu proje, yüklenen bir videoda kamera hareketini algılayan ve hareket eden kareleri tespit eden bir web uygulamasıdır.  
Bilgisayarlı görme teknikleri kullanılarak, iki ardışık kare arasındaki özellik eşleştirme ve homografi dönüşümü hesaplanarak kamera hareketi tahmin edilmektedir.

## Yaklaşım ve Hareket Algılama Mantığı

- Önceki ve şimdiki kareler gri tonlamaya çevrilir.  
- ORB algoritması ile karelerden anahtar noktalar ve tanımlayıcılar çıkarılır.  
- BFMatcher kullanılarak iki kare arasındaki iyi eşleşmeler tespit edilir.  
- Bu eşleşmelerden homografi matrisi hesaplanır ve matrisin içerdiği x-y kaymaları analiz edilerek hareket olup olmadığı belirlenir.  
- Ardışık hareketli kareler gruplanarak daha anlamlı hareket segmentleri oluşturulur.

## Kullanılan Veri Kümesi

- Kullanıcı tarafından yüklenen herhangi bir video dosyası (MP4, AVI, MOV formatları desteklenir).  
- Uygulama gerçek zamanlı video işleme yapmaz, yüklenen video dosyası kare kare işlenir.

## Karşılaşılan Zorluklar ve Varsayımlar

- Homografi hesaplaması için yeterli sayıda iyi eşleşme gereklidir, düşük kaliteli veya durağan videolarda hareket algılaması zorlaşabilir.  
- Kamera hareketi ile nesne hareketi ayrımı yapılmamaktadır; tüm hareketler kamera hareketi olarak değerlendirilir.  
- Büyük videoların işlenmesi zaman alabilir ve bellek kullanımı artabilir.

## Uygulamanın Yerel Olarak Çalıştırılması

1. Gerekli paketleri yükleyin:
pip install streamlit opencv-python-headless numpy

2. Proje dosyasını indirin veya klonlayın.

3. Uygulamayı başlatın:

streamlit run app.py

4. Tarayıcıda açılan arayüzden video dosyanızı yükleyin ve parametreleri ayarlayın.

## Canlı Uygulama

Canlı uygulamaya şu bağlantıdan ulaşabilirsiniz:  
**[Uygulama Linki]** https://ugvizrag4barktquqbueka.streamlit.app/

## Örnek Giriş ve Çıkış

- **Giriş:** Kullanıcı tarafından yüklenen video dosyası.  
- **Çıkış:** Hareket algılanan karelerin listesi ve bu karelerin görselleri.

