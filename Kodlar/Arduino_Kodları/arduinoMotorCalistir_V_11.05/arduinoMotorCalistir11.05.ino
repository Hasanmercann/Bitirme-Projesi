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
  Serial.println("1: Ileri, 2: Geri, 3: Sag, 4: Sol");

  // Başlangıçta motorları durdur
  motorStop();
}

void loop() {
  // Seri porttan veri gelirse oku
  if (Serial.available() > 0) {
    char command = Serial.read(); // Gelen komutu oku
    // Yeni satır veya taşıma karakterlerini temizle
    if (command == '\n' || command == '\r') {
      return;
    }

    // Komutlara göre motor kontrolü
    if (command == '1') {
      motorForward(100); // 200 PWM hızında ileri
      Serial.println("Motorlar ileri hareket ediyor");
    }
    else if (command == '2') {
      motorBackward(100); // 200 PWM hızında geri
      Serial.println("Motorlar geri hareket ediyor");
    }
    else if (command == '3') {
      motorRight(100); // 200 PWM hızında sağa dönüş
      Serial.println("Motorlar sağa dönüyor");
    }
    else if (command == '4') {
      motorLeft(100); // 200 PWM hızında sola dönüş
      Serial.println("Motorlar sola dönüyor");
    }
    else {
      motorStop(); // Geçersiz komutsa motorları durdur
      Serial.println("Gecersiz komut! 1, 2, 3 veya 4 girin");
    }
  }
}

// Motorları ileri hareket ettiren fonksiyon
void motorForward(int speed) {
  // Motor A (Sol motor)
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, speed);

  // Motor B (Sağ motor)
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, speed);
}

// Motorları geri hareket ettiren fonksiyon
void motorBackward(int speed) {
  // Motor A (Sol motor)
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, speed);

  // Motor B (Sağ motor)
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, speed);
}

// Motorları sağa döndüren fonksiyon
void motorRight(int speed) {
  // Motor A (Sol motor) ileri
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, speed);

  // Motor B (Sağ motor) geri
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, speed);
}

// Motorları sola döndüren fonksiyon
void motorLeft(int speed) {
  // Motor A (Sol motor) geri
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(ENA, speed);

  // Motor B (Sağ motor) ileri
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, speed);
}

// Motorları durduran fonksiyon
void motorStop() {
  // Motor A (Sol motor)
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 0);

  // Motor B (Sağ motor)
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
}