// L298N Motor Sürücü Pin Tanımlamaları (Arduino Mega için)
const int ENA = 6;    // Motor A ve B hız kontrol pini (PWM, Mega'da PWM destekli)
const int IN1 = 2;    // Motor A yön kontrol pini 1 (Sol motor)
const int IN2 = 3;    // Motor A yön kontrol pini 2 (Sol motor)
const int IN3 = 4;    // Motor B yön kontrol pini 1 (Sağ motor)
const int IN4 = 5;    // Motor B yön kontrol pini 2 (Sağ motor)

void setup() {
  // Pinleri çıkış olarak ayarla
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Seri haberleşmeyi başlat (9600 baud)
  Serial.begin(9600);
  Serial.println("Komutlar: 1=Ileri, 2=Geri, 3=Sag, 4=Sol (Hiz: 0-255)");

  // Başlangıçta motorları durdur
  motorStop();
}

void loop() {
  // Seri porttan veri gelirse oku
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n'); // Gelen tüm satırı oku
    input.trim(); // Boşlukları ve yeni satırları temizle

    // Komut ve hızı ayır (örneğin, "1:100" formatında)
    int separatorIndex = input.indexOf(':');
    if (separatorIndex != -1) {
      String commandStr = input.substring(0, separatorIndex);
      String speedStr = input.substring(separatorIndex + 1);
      char command = commandStr.charAt(0); // İlk karakter komut
      int speed = speedStr.toInt(); // Kalan kısım hız (0-255 arası)

      // Hızı 0-255 aralığında kontrol et
      if (speed < 0 || speed > 255) {
        speed = 60; // Geçersizse varsayılan 60
      }

      // Komutlara göre motor kontrolü
      if (command == '1') {
        motorForward(speed);
        Serial.println("Motorlar ileri hareket ediyor, Hiz: " + String(speed));
      }
      else if (command == '2') {
        motorBackward(speed);
        Serial.println("Motorlar geri hareket ediyor, Hiz: " + String(speed));
      }
      else if (command == '3') {
        motorRight(speed);
        Serial.println("Motorlar sağa dönüyor, Hiz: " + String(speed));
      }
      else if (command == '4') {
        motorLeft(speed);
        Serial.println("Motorlar sola dönüyor, Hiz: " + String(speed));
      }
      else {
        motorStop();
        Serial.println("Gecersiz komut! 1, 2, 3 veya 4 girin");
      }
    }
  }
}

// Motorları ileri hareket ettiren fonksiyon
void motorForward(int speed) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, speed);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, speed);
}

// Motorları geri hareket ettiren fonksiyon
void motorBackward(int speed) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, speed);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, speed);
}

// Motorları sağa döndüren fonksiyon
void motorRight(int speed) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, speed);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, speed);
}

// Motorları sola döndüren fonksiyon
void motorLeft(int speed) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, speed);

  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, speed);
}

// Motorları durduran fonksiyon
void motorStop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
}