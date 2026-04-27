#include <Arduino.h>
#include <driver/i2s.h>

// I2S 핀 설정
#define I2S_WS   6
#define I2S_SCK  7
#define I2S_SD   8
#define I2S_PORT I2S_NUM_0

#define LED_PIN 2

void setup() {
  Serial.begin(921600);
  pinMode(LED_PIN, OUTPUT);

  // I2S 설정
  i2s_config_t config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = 16000,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_STAND_I2S,
    .intr_alloc_flags = 0,
    .dma_buf_count = 4,
    .dma_buf_len = 128
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };

  i2s_driver_install(I2S_PORT, &config, 0, NULL);
  i2s_set_pin(I2S_PORT, &pin_config);
}

void loop() {
  int32_t sample;
  size_t bytes_read;

  // 음성 데이터 읽기
  i2s_read(I2S_PORT, &sample, sizeof(sample), &bytes_read, portMAX_DELAY);

  if (bytes_read > 0) {
    // 32bit → 16bit 변환
    int16_t pcm16 = sample >> 14;
    Serial.write((uint8_t*)&pcm16, sizeof(pcm16));
  }

  // =========================
  // PC → ESP32 명령 수신
  // =========================
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');

    if (cmd == "ON") {
      digitalWrite(LED_PIN, LOW);
    }
    else if (cmd == "OFF") {
      digitalWrite(LED_PIN, HIGH);
    }
  }
}