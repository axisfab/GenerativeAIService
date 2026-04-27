import serial
import numpy as np
import whisper
import soundfile as sf
import os
import sys

os.makedirs("C:/temp", exist_ok=True)

ser = serial.Serial('COM3', 921600, timeout=1)
model = whisper.load_model("base")

SAMPLE_RATE = 16000
DURATION = 5  # recording time

print("Start Recording...")

audio_data = []

for _ in range(int(SAMPLE_RATE / 512 * DURATION)):
    data = ser.read(512 * 2)  # int16 = 2바이트
    samples = np.frombuffer(data, dtype=np.int16)
    audio_data.extend(samples)

audio_np = np.array(audio_data).astype(np.float32) / 32768.0

# wav 파일 저장 (선택)
sf.write("C:/temp/record.wav", audio_np, SAMPLE_RATE)

print("Processing Whisper...")

result = model.transcribe(audio_np, language='ko')

print("result:", result["text"])

sys.exit()