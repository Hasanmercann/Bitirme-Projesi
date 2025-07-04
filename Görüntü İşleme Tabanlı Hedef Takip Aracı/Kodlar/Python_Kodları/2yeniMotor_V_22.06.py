import cv2
import numpy as np
import serial
import threading
import time
import sys
import os

# Seri portu başlat
try:
    port = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)
    time.sleep(5)
except serial.SerialException as e:
    print(f"Seri port hatası: {e}")
    sys.exit(1)

# IP kamerasını başlat
ip_adresi = 'http://192.168.238.10:81/stream'
cap = cv2.VideoCapture(ip_adresi)
if not cap.isOpened():
    print(f"IP kamera açılamadı: {ip_adresi}. Lütfen IP adresini kontrol edin.")
    sys.exit(1)

# Kırmızı renk için HSV aralığı
kirmizi_alt = np.array([0, 150, 100])
kirmizi_ust = np.array([10, 255, 255])
kirmizi_alt2 = np.array([170, 150, 100])
kirmizi_ust2 = np.array([180, 255, 255])

# Alan eşikleri
MIN_ALAN = 500
BUYUK_ALAN = 5000

# Hız değişkeni (0-255 arası, varsayılan 60)
hiz = 60

# İş parçacıklarının çalışmasını kontrol etmek için bir flag
dur = threading.Event()

# Seri port komutlarını gönderen fonksiyon
def seri_kontrol():
    global hiz
    while not dur.is_set():
        veri_girisi = input("Kontrol: 'a' (1), 'b' (0), 'c' (3), 'd' (4), 'q' (çık), 'h:<hiz>' (hizi ayarla): ").strip().lower()
        print(f"Giriş alındı: {veri_girisi}")
        if veri_girisi.startswith('h:'):
            try:
                hiz = int(veri_girisi.split(':')[1])
                if 0 <= hiz <= 255:
                    print(f"Hiz ayarlandı: {hiz}")
                else:
                    print("Hiz 0-255 arasinda olmali!")
                    hiz = 60
            except:
                print("Gecersiz hiz degeri!")
                hiz = 60
        elif veri_girisi == 'q':
            print("Seri kontrol sonlandırılıyor...")
            dur.set()
            try:
                port.write(f"0:{hiz}\n".encode())
                port.close()
            except:
                pass
            break
        elif veri_girisi in ['a', 'b', 'c', 'd']:
            komut = {'a': '1', 'b': '0', 'c': '3', 'd': '4'}[veri_girisi]
            port.write(f"{komut}:{hiz}\n".encode())
            print(f"Komut gönderildi: {komut} Hiz: {hiz}")
        else:
            print("Geçersiz giriş! 'a', 'b', 'c', 'd', 'q' veya 'h:<hiz>' kullanın.")

# Kamera görüntüsünü işleyen ve kırmızı nesne algılayan fonksiyon
def kamera_calistir():
    global hiz

    while not dur.is_set():
        ret, frame = cap.read()
        if not ret:
            print("IP kameradan görüntü alınamadı!")
            break

        height, width = frame.shape[:2]
        bolum_genislik = width // 3
        sol_bolum = (0, bolum_genislik)
        orta_bolum = (bolum_genislik, 2 * bolum_genislik)
        sag_bolum = (2 * bolum_genislik, width)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, kirmizi_alt, kirmizi_ust)
        mask2 = cv2.inRange(hsv, kirmizi_alt2, kirmizi_ust2)
        mask = mask1 + mask2

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=2)

        durum_metni = "Nesne tespit edilmedi"
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            alan = cv2.contourArea(max_contour)
            if alan > MIN_ALAN:
                x, y, w, h = cv2.boundingRect(max_contour)
                merkez_x = x + w // 2

                if sol_bolum[0] <= merkez_x < sol_bolum[1]:
                    durum_metni = "Sol - Komut: 4"
                    print(f"Kırmızı nesne solda algılandı, '4:{hiz}' gönderildi")
                    port.write(f"4:{hiz}\n".encode())
                elif sag_bolum[0] <= merkez_x < sag_bolum[1]:
                    durum_metni = "Sağ - Komut: 3"
                    print(f"Kırmızı nesne sağda algılandı, '3:{hiz}' gönderildi")
                    port.write(f"3:{hiz}\n".encode())
                else:
                    if alan > BUYUK_ALAN:
                        durum_metni = "Orta (Büyük) - Komut: 0"
                        print(f"Kırmızı nesne ortada ve büyük, '0:{hiz}' gönderildi")
                        port.write(f"0:{hiz}\n".encode())

                    else:
                        durum_metni = "Orta (Küçük) - Komut: 1"
                        print(f"Kırmızı nesne ortada ve küçük, '1:{hiz}' gönderildi")
                        port.write(f"1:{hiz}\n".encode())


        print(f"Durum: {durum_metni}")
        time.sleep(0.01)

    cap.release()

# İş parçacıklarını başlat
kamera_thread = threading.Thread(target=kamera_calistir)
seri_thread = threading.Thread(target=seri_kontrol)

kamera_thread.start()
seri_thread.start()

kamera_thread.join()
seri_thread.join()

try:
    port.write(f"0:{hiz}\n".encode())
    port.close()
except:
    pass

print("Program sonlanıyor...")
os._exit(0)