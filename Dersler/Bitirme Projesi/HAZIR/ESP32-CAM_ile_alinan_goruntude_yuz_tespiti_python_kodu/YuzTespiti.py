import cv2
import sys

# ESP32-CAM video stream
ip_adresi = 'http://10.240.36.25/stream'  # ESP32-CAM IP address
cap = cv2.VideoCapture(ip_adresi)
if not cap.isOpened():
    print(f"IP kamera açılamadı: {ip_adresi}. Lütfen IP adresini, portu veya protokolü kontrol edin.")
    sys.exit(1)

# Yüz algılama için Haar Cascade sınıflandırıcıları
face_frontal_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
if face_frontal_cascade.empty() or face_profile_cascade.empty():
    print("Hata: Haar Cascade sınıflandırıcısı yüklenemedi.")
    cap.release()
    sys.exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Görüntü alınamadı")
        break

    # Resize frame to 320x240 and flip vertically
    frame = cv2.resize(frame, (320, 240))
    frame = cv2.flip(frame, 0)  # 0: vertical, 1: horizontal, -1: both

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect frontal faces
    frontal_faces = face_frontal_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Detect profile faces
    profile_faces = face_profile_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Combine all detected faces
    all_faces = list(frontal_faces) + list(profile_faces)
    
    # Process detected faces
    if all_faces:
        # Assign labels to faces and find the largest one
        largest_area = 0
        largest_face = None
        for i, (x, y, w, h) in enumerate(all_faces):
            # Draw rectangle and label for each face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Yuz {i+1}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            # Calculate area to find the largest face
            area = w * h
            if area > largest_area:
                largest_area = area
                largest_face = (x, y, w, h)
        
        # Track the largest face
        if largest_face:
            x, y, w, h = largest_face
            center_x = x + w // 2
            center_y = y + h // 2
            
            # Draw center point for the tracked face
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    # Display frame
    cv2.imshow('Frame', frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()