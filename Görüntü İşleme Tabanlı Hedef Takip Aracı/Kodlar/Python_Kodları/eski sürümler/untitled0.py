# -*- coding: utf-8 -*-
"""
Created on Thu May 29 10:35:24 2025

@author: Hasan Mercan
"""

import cv2
import numpy as np

# Kamerayı başlat
cap = cv2.VideoCapture(0)  # Varsayılan kamera (0), gerekirse USB kamera için 1 veya 2 deneyin
if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

# Kırmızı renk için HSV aralığı
kirmizi_alt = np.array([0, 150, 100])    # Kırmızı alt sınır
kirmizi_ust = np.array([10, 255, 255])   # Kırmızı üst sınır
kirmizi_alt2 = np.array([170, 150, 100]) # Kırmızı için ikinci aralık
kirmizi_ust2 = np.array([180, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        print("Görüntü alınamadı!")
        break

    # Görüntü boyutlarını al
    height, width = frame.shape[:2]
    # Görüntüyü yatay olarak üçe böl
    bolum_genislik = width // 3
    sol_bolum = (0, bolum_genislik)
    orta_bolum = (bolum_genislik, 2 * bolum_genislik)
    sag_bolum = (2 * bolum_genislik, width)

    # Bölümleri görselleştirmek için dikey çizgiler çiz
    cv2.line(frame, (bolum_genislik, 0), (bolum_genislik, height), (255, 0, 0), 1)
    cv2.line(frame, (2 * bolum_genislik, 0), (2 * bolum_genislik, height), (255, 0, 0), 1)

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

    # Kırmızı nesneyi çerçevele ve konumunu belirle
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(max_contour) > 500:  # Minimum alan sınırı
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Yeşil çerçeve

            # Nesnenin merkezini hesapla
            merkez_x = x + w // 2

            # Nesnenin hangi bölgede olduğunu kontrol et
            if sol_bolum[0] <= merkez_x < sol_bolum[1]:
                print("Kırmızı nesne solda algılandı")
            elif sag_bolum[0] <= merkez_x < sag_bolum[1]:
                print("Kırmızı nesne sağda algılandı")
            else:
                print("Kırmızı nesne ortada algılandı")

    # Görüntüyü ve maskeyi göster
    cv2.imshow('Kamera', frame)
    cv2.imshow('Mask', mask)

    # 'q' tuşuna basıldığında çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Kamera sonlandırılıyor...")
        break

# Kamera ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()