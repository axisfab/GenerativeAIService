#include <Arduino.h>
#include <driver/i2s.h>

#define I2S_WS   6
#define I2S_SCK  7
#define I2S_SD   8
#define I2S_PORT I2S_NUM_0

#define SAMPLE_RATE 16000
#define BUFFER_LEN  256

int32_t i2s_buffer[BUFFER_LEN];
int16_t pcm_buffer[BUFFER_LEN];

void setup() {
  Serial.begin(921600);  

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

void loop() {
  size_t bytes_read;

  i2s_read(I2S_PORT, i2s_buffer, sizeof(i2s_buffer), &bytes_read, portMAX_DELAY);

  int samples = bytes_read / sizeof(int32_t);

  // 32bit → 16bit 변환 (Whisper 입력용)
  // pcm(Pulse Code Modulation) 1개의 샘플>16bit로 표현, -32768 ~ 0 ~ +32767
  for (int i = 0; i < samples; i++) {
    pcm_buffer[i] = i2s_buffer[i] >> 14;
  }

  // 바이너리 그대로 전송
  Serial.write((uint8_t*)pcm_buffer, samples * sizeof(int16_t));
}