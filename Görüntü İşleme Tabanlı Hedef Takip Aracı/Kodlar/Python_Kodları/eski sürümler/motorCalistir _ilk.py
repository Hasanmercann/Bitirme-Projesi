import cv2
import serial
import threading
import time
import sys

# Seri portu başlat
try:
    port = serial.Serial('COM11', 9600, timeout=1)  # COM11 yerine doğru portu yazın
    time.sleep(2)  # Arduino'nun bağlanması için bekle
except serial.SerialException as e:
    print(f"Seri port hatası: {e}")
    sys.exit(1)

# Kamerayı başlat
cap = cv2.VideoCapture(0)  # Varsayılan kamera (0), gerekirse değiştirin
if not cap.isOpened():
    print("Kamera açılamadı!")
    sys.exit(1)

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

# Kamera görüntüsünü işleyen ana döngü
def kamera_calistir():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Görüntü alınamadı!")
            break
        cv2.imshow('Kamera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
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