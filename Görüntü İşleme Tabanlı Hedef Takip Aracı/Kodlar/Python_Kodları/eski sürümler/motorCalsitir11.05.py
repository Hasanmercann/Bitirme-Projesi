import cv2
import numpy as np
import serial
import threading
import time
import sys

# Seri portu başlat
try:
    port = serial.Serial('COM8', 9600, timeout=1)  # COM11 yerine doğru portu yazın
    time.sleep(2)  # Arduino'nun bağlanması için bekle
except serial.SerialException as e:
    print(f"Seri port hatası: {e}")
    sys.exit(1)

# Kamerayı başlat
cap = cv2.VideoCapture(0)  # Varsayılan kamera (0), gerekirse değiştirin
if not cap.isOpened():
    print("Kamera açılamadı!")
    sys.exit(1)

# Kırmızı renk için daha sıkı HSV aralığı (çok kırmızı olanlar için)
kirmizi_alt = np.array([0, 150, 100])    # Kırmızı alt sınır (daha yüksek doygunluk ve değer)
kirmizi_ust = np.array([10, 255, 255])   # Kırmızı üst sınır
kirmizi_alt2 = np.array([170, 150, 100]) # Kırmızı için ikinci aralık
kirmizi_ust2 = np.array([180, 255, 255])

# Seri port komutlarını gönderen fonksiyon
def seri_kontrol():
    while True:
        veri_girisi = input("Kontrol: 'a' (1), 'b' (0), 'c' (3), 'd' (4), 'q' (çık): ").strip().lower()
        print(f"Giriş alındı: {veri_girisi}")  # Girişi kontrol et
        if veri_girisi == 'a':
            port.write(b'1')
            print("Komut gönderildi: 1 (a)")
        elif veri_girisi == 'b':
            port.write(b'0')
            print("Komut gönderildi: 0 (b)")
        elif veri_girisi == 'c':
            port.write(b'3')
            print("Komut gönderildi: 3 (c)")
        elif veri_girisi == 'd':
            port.write(b'4')
            print("Komut gönderildi: 4 (d)")
        elif veri_girisi == 'q':
            print("Seri kontrol sonlandırılıyor...")
            break
        else:
            print("Geçersiz giriş! 'a', 'b', 'c', 'd' veya 'q' kullanın.")

# Kamera görüntüsünü işleyen ve kırmızı nesne algılayan fonksiyon
def kamera_calistir():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Görüntü alınamadı!")
            break

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

        # Konturları bul
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Kırmızı nesneyi çerçevele ve komut gönder
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(max_contour) > 500:  # Minimum alan sınırı
                x, y, w, h = cv2.boundingRect(max_contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Nesneyi yeşil kare ile çerçevele
                print("Kırmızı nesne algılandı, 'c' komutu gönderildi")
                port.write(b'3')  # Kırmızı nesne algılandığında 'c' komutunu gönder

        # Görüntüyü göster
        cv2.imshow('Kamera', frame)
        cv2.imshow('Mask', mask)

        # 'q' tuşuna basıldığında çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            port.write(b'0')
            cap.release()   
            cv2.destroyAllWindows()
            port.close()
            break

# İş parçacıklarını başlat
kamera_thread = threading.Thread(target=kamera_calistir)
seri_thread = threading.Thread(target=seri_kontrol)

kamera_thread.start()
seri_thread.start()

kamera_thread.join()
seri_thread.join()

# Temizlik
cap.release()
cv2.destroyAllWindows()
port.close()