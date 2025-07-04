import cv2
import numpy as np
import serial
import threading
import time
import sys
import os

# Seri portu başlat
try:
    port = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)  # Orange Pi için seri port
    time.sleep(5)  # Arduino'nun bağlanması için bekle
except serial.SerialException as e:
    print(f"Seri port hatası: {e}")
    sys.exit(1)

# IP kamerasını başlat
ip_adresi = 'http://192.168.1.19:81/stream'  # HTTP akış URL'si
cap = cv2.VideoCapture(ip_adresi)  # IP kamerası için URL
if not cap.isOpened():
    print(f"IP kamera açılamadı: {ip_adresi}. Lütfen IP adresini, portu veya protokolü kontrol edin.")
    sys.exit(1)

# Kırmızı renk için HSV aralığı
kirmizi_alt = np.array([0, 150, 100])    # Kırmızı alt sınır
kirmizi_ust = np.array([10, 255, 255])   # Kırmızı üst sınır
kirmizi_alt2 = np.array([170, 150, 100]) # Kırmızı için ikinci aralık
kirmizi_ust2 = np.array([180, 255, 255])

# Alan eşikleri
MIN_ALAN = 500      # Nesnenin algılanması için minimum alan
BUYUK_ALAN = 5000   # Nesnenin "yeteri kadar büyük" sayılması için eşik

# İş parçacıklarının çalışmasını kontrol etmek için bir flag
dur = threading.Event()

# Kamera görüntüsünü işleyen ve kırmızı nesne algılayan fonksiyon
def kamera_calistir():
    son_b_komut_zamani = time.time()  # Son 'b' komutunun gönderilme zamanını tut
    b_komut_araligi = 3  # 3 saniyelik aralık

    while not dur.is_set():
        ret, frame = cap.read()
        if not ret:
            print("IP kameradan görüntü alınamadı! Bağlantıyı veya URL'yi kontrol edin.")
            break

        # Görüntü boyutlarını al
        height, width = frame.shape[:2]
        # Görüntüyü dikey olarak üçe böl
        bolum_genislik = width // 3
        sol_bolum = (0, bolum_genislik)
        sag_bolum = (2 * bolum_genislik, width)

        # Görüntüyü HSV renk uzayına çevir
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Kırmızı renk için maske oluştur
        mask1 = cv2.inRange(hsv, kirmizi_alt, kirmizi_ust)
        mask2 = cv2.inRange(hsv, kirmizi_alt2, kirmizi_ust2)
        mask = mask1 + mask2

        # Gürültüyü azaltmak için morfolojik işlemler
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=2)

        # Durum metni için başlangıç değeri
        durum_metni = "Nesne tespit edilmedi"

        # Konturları bul
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Kırmızı nesneyi çerçevele ve konumuna göre komut gönder
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            alan = cv2.contourArea(max_contour)
            if alan > MIN_ALAN:  # Minimum alan sınırı
                x, y, w, h = cv2.boundingRect(max_contour)
                merkez_x = x + w // 2

                # Nesnenin hangi bölgede olduğunu kontrol et
                if sol_bolum[0] <= merkez_x < sol_bolum[1]:
                    durum_metni = "Sol - Komut: d (4)"
                    print("Kırmızı nesne solda algılandı, 'd' komutu gönderildi")
                    port.write(b'4')  # Solda: d komutu
                elif sag_bolum[0] <= merkez_x < sag_bolum[1]:
                    durum_metni = "Sağ - Komut: c (3)"
                    print("Kırmızı nesne sağda algılandı, 'c' komutu gönderildi")
                    port.write(b'3')  # Sağda: c komutu
                else:
                    # Orta bölgede: Nesne boyutuna göre komut seç
                    if alan > BUYUK_ALAN:
                        durum_metni = "Orta (Büyük) - Komut: b (0)"
                        print("Kırmızı nesne ortada ve yeteri kadar büyük, 'b' komutu gönderildi")
                        port.write(b'0')  # Orta ve büyük: b komutu
                        son_b_komut_zamani = time.time()  # Zamanlayıcıyı sıfırla
                    else:
                        durum_metni = "Orta (Küçük) - Komut: a (1)"
                        print("Kırmızı nesne ortada ama yeteri kadar büyük değil, 'a' komutu gönderildi")
                        port.write(b'1')  # Orta ve küçük: a komutu
            else:
                # Küçük konturlar için 'b' komutu gönder
                if time.time() - son_b_komut_zamani >= b_komut_araligi:
                    durum_metni = "Küçük kontur - Komut: b (0)"
                    print("Küçük kontur algılandı, 'b' komutu gönderildi")
                    port.write(b'0')
                    son_b_komut_zamani = time.time()
        else:
            # Kontur yoksa her 3 saniyede bir 'b' komutu gönder
            if time.time() - son_b_komut_zamani >= b_komut_araligi:
                durum_metni = "Nesne yok - Komut: b (0)"
                print("Kırmızı nesne tespit edilmedi, 'b' komutu gönderildi")
                port.write(b'0')
                son_b_komut_zamani = time.time()

        # Durum metnini konsola yazdır
        print(f"Durum: {durum_metni}")

        # Döngüde çok hızlı çalışmayı önlemek için küçük bir gecikme
        time.sleep(0.01)  # 10 ms gecikme

    # Kamera ve kaynakları temizle
    cap.release()

# Ana program
try:
    # Kamera iş parçacığını başlat
    kamera_thread = threading.Thread(target=kamera_calistir)
    kamera_thread.start()

    # İş parçacığının tamamlanmasını bekle
    kamera_thread.join()

except KeyboardInterrupt:
    print("Klavye kesmesi alındı, program sonlandırılıyor...")
    dur.set()

# Temizlik
try:
    port.write(b'0')  # Son bir komut gönder
    port.close()
except:
    pass

# Programı tamamen sonlandır
print("Program sonlanıyor...")
os._exit(0)  # Ctrl+C gibi anında sonlandır