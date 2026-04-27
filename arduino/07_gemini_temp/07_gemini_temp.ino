#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_SHTC3.h>
#include <Adafruit_NeoPixel.h>

#define SDA_PIN 10
#define SCL_PIN 9

#define LED_PIN 1
#define NUMPIXELS 1

Adafruit_SHTC3 shtc3;
Adafruit_NeoPixel pixels(NUMPIXELS, LED_PIN, NEO_GRB + NEO_KHZ800);

String cmd = "";

void setup() {
  Serial.begin(115200);

  Wire.begin(SDA_PIN, SCL_PIN);
  shtc3.begin();

  pixels.begin();
  pixels.clear();
  pixels.show();
}

void loop() {

  // =========================
  // 시리얼 명령 처리
  // =========================
  if (Serial.available()) {
    cmd = Serial.readStringUntil('\n');
    cmd.trim();

    // 온도 요청
    if (cmd == "TEMP") {
      sensors_event_t h, t;
      shtc3.getEvent(&h, &t);
      Serial.print("TEMP:");
      Serial.println(t.temperature);
    }

    // LED 파랑 (더움)
    else if (cmd == "BLUE") {
      pixels.setPixelColor(0, pixels.Color(0, 0, 150));
      pixels.show();
      Serial.println("BLUE LED ON");
    }
    // LED 빨강 (추움)
    else if (cmd == "RED") {
      pixels.setPixelColor(0, pixels.Color(150, 0, 0));
      pixels.show();
      Serial.println("RED LED ON");
    }

    // LED OFF
    else if (cmd == "OFF") {
      pixels.clear();
      pixels.show();
    }
  }

}