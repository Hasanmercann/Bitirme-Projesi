  TR/EN

ESP32-CAM Yüz Tanıma Projesi
Bu proje, AI Thinker ESP32-CAM modülünden alınan video akışını kullanarak gerçek zamanlı yüz tanıma işlemini gerçekleştirir. Python ve OpenCV kullanılarak geliştirilmiştir. Kod, ESP32-CAM'in IP adresinden video akışını alır ve Haar Cascade sınıflandırıcıları ile hem önden hem de profilden yüzleri algılar. Algılanan yüzler çerçeve içine alınır ve en büyük yüzün merkezi işaretlenir.
Gereksinimler

Python 3.x: Bilgisayarınıza Python'un yüklü olması gerekir.
Kütüphaneler:
OpenCV: pip install opencv-python
NumPy: pip install numpy


ESP32-CAM Modülü: IP video akışı sağlayan bir AI Thinker ESP32-CAM modülü.
Ağ Bağlantısı: ESP32-CAM ile aynı Wi-Fi ağına bağlı bir bilgisayar.

Kurulum

Python'u bilgisayarınıza yükleyin (https://www.python.org/downloads/).
Gerekli kütüphaneleri yükleyin:pip install opencv-python numpy


ESP32-CAM modülünüzün IP adresini öğrenin (örneğin, http://10.240.36.25/stream). Bu adres, kodda ip_adresi değişkenine yazılmalıdır.
face_detection.py dosyasını çalıştırılabilir bir dizine kaydedin.

Kullanım

ESP32-CAM modülünüzün açık olduğundan ve video akışının çalıştığından emin olun.
face_detection.py dosyasındaki ip_adresi değişkenini, ESP32-CAM'inizin IP adresiyle güncelleyin:ip_adresi = 'http://SIZIN_IP_ADRESINIZ/stream'


Kodu çalıştırın:python face_detection.py


Kod, video akışını alacak ve algılanan yüzleri çerçeve içine alarak en büyük yüzün merkezini kırmızı bir nokta ile işaretleyecektir.
Çıkmak için klavyeden q tuşuna basın.

Önemli Notlar

ESP32-CAM'in aynı Wi-Fi ağına bağlı olduğundan emin olun.
IP adresi doğru değilse veya modül çalışmıyorsa, kod hata verecektir. IP adresini ve bağlantıyı kontrol edin.
Haar Cascade sınıflandırıcıları, OpenCV'nin varsayılan dosyalarıdır (haarcascade_frontalface_default.xml ve haarcascade_profileface.xml). Bunların doğru yüklendiğinden emin olun.
Video akışı için düşük çözünürlük (320x240) kullanılmıştır, ancak bu değeri kodda değiştirebilirsiniz.


ESP32-CAM Face Detection Project
This project performs real-time face detection using the video stream from an AI Thinker ESP32-CAM module. It is developed using Python and OpenCV. The code retrieves the video stream from the ESP32-CAM's IP address and uses Haar Cascade classifiers to detect both frontal and profile faces. Detected faces are outlined with rectangles, and the center of the largest face is marked.
Requirements

Python 3.x: Python must be installed on your computer.
Libraries:
OpenCV: pip install opencv-python
NumPy: pip install numpy


ESP32-CAM Module: An AI Thinker ESP32-CAM module providing an IP video stream.
Network Connection: A computer connected to the same Wi-Fi network as the ESP32-CAM.

Setup

Install Python on your computer (https://www.python.org/downloads/).
Install the required libraries:pip install opencv-python numpy


Obtain the IP address of your ESP32-CAM (e.g., http://10.240.36.25/stream). Update the ip_adresi variable in the code with this address.
Save the face_detection.py file to a working directory.

Usage

Ensure your ESP32-CAM module is powered on and the video stream is active.
Update the ip_adresi variable in face_detection.py with your ESP32-CAM's IP address:ip_adresi = 'http://YOUR_IP_ADDRESS/stream'


Run the code:python face_detection.py


The code will retrieve the video stream, outline detected faces, and mark the center of the largest face with a red dot.
Press the q key to exit.

Important Notes

Ensure the ESP32-CAM is connected to the same Wi-Fi network as your computer.
If the IP address is incorrect or the module is not running, the code will throw an error. Verify the IP address and connection.
The Haar Cascade classifiers (haarcascade_frontalface_default.xml and haarcascade_profileface.xml) are included with OpenCV. Ensure they are loaded correctly.
The video stream uses a low resolution (320x240) by default, but you can modify this value in the code.
