#include <Arduino.h>
#include <driver/i2s.h>

#define I2S_WS   6
#define I2S_SCK  7
#define I2S_SD   8
#define I2S_PORT I2S_NUM_0

float dc_offset = 0;
float level = 0;

void setup() {
  Serial.begin(115200);

  i2s_config_t config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = 16000,   //음성인식표준샘플링
    .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_STAND_I2S,
    .intr_alloc_flags = 0,
    .dma_buf_count = 2,
    .dma_buf_len = 64
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

  i2s_read(I2S_PORT, &sample, sizeof(sample), &bytes_read, portMAX_DELAY);

  if (bytes_read > 0) {

    // DC Offset 제거 (기준 0 맞추기)
    dc_offset = dc_offset * 0.995 + sample * 0.005;
    float centered = sample - dc_offset;


    float amp = abs(centered);

    // 스케일 다운 (값 너무 큰거 방지)
    amp = amp / 1000.0;

    // EMA 필터 (부드럽게)
    level = level * 0.9 + amp * 0.1;

    // 5시리얼 플로터 출력 (안정된 그래프)
    Serial.print(0);
    Serial.print(" ");
    Serial.print(2000);
    Serial.print(" ");
    Serial.println((int)level);
  }
}