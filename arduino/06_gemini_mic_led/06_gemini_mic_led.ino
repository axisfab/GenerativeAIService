#include <Arduino.h>
#include <driver/i2s.h>

#define I2S_WS   6
#define I2S_SCK  7
#define I2S_SD   8
#define I2S_PORT I2S_NUM_0

#define LED_PIN 2

#define SAMPLE_RATE 16000
#define BUFFER_LEN  256

int32_t i2s_buffer[BUFFER_LEN];
int16_t pcm_buffer[BUFFER_LEN];

void setup() {
  Serial.begin(921600);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH); // OFF

  i2s_config_t config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
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
bool isRecording = true;
void loop() {

  // 먼저 명령 체크 (우선순위 높임)
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    isRecording = false;  // 녹음 잠시 중단

    if (cmd == "ON") {
      digitalWrite(LED_PIN, LOW);
      Serial.println("LED ON");
    }
    else if (cmd == "OFF") {
      digitalWrite(LED_PIN, HIGH);
      Serial.println("LED OFF");
    }

    delay(100);           // 안정화
    isRecording = true;   // 다시 녹음
  }

  // 녹음
  if (isRecording) {
    size_t bytes_read;

    i2s_read(I2S_PORT, i2s_buffer, sizeof(i2s_buffer), &bytes_read, portMAX_DELAY);

    int samples = bytes_read / sizeof(int32_t);

    for (int i = 0; i < samples; i++) {
      pcm_buffer[i] = i2s_buffer[i] >> 11;
    }

    Serial.write((uint8_t*)pcm_buffer, samples * sizeof(int16_t));
  }
}