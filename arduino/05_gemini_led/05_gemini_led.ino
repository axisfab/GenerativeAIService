#define LED_PIN 2  

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  digitalWrite(LED_PIN, HIGH);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "ON") {
      digitalWrite(LED_PIN, LOW);   // ON
      Serial.println("LED ON");
    }
    else if (cmd == "OFF") {
      digitalWrite(LED_PIN, HIGH);  // OFF
      Serial.println("LED OFF");
    }
    else {
      Serial.println("INVALID");
    }
  }
}