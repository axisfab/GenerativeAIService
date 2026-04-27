import serial
import numpy as np
import whisper
import soundfile as sf
import os
from gtts import gTTS

# =========================
# 설정
# =========================
PORT = 'COM3'
BAUD = 921600
SAMPLE_RATE = 16000
DURATION = 5

os.makedirs("C:/temp", exist_ok=True)

# =========================
# 초기화
# =========================
ser = serial.Serial(PORT, BAUD, timeout=1)
model = whisper.load_model("base")

print("🎤 Start Recording...")

# =========================
# 음성 수집
# =========================
audio_data = []

for _ in range(int(SAMPLE_RATE / 512 * DURATION)):
    data = ser.read(512 * 2)
    samples = np.frombuffer(data, dtype=np.int16)
    audio_data.extend(samples)

audio_np = np.array(audio_data).astype(np.float32) / 32768.0


sf.write("C:/temp/record.wav", audio_np, SAMPLE_RATE)

print("🧠 Processing Whisper...")

# =========================
# 2️⃣ STT
# =========================
result = model.transcribe(audio_np, language='ko')
text = result["text"]

print("📝 result:", text)

# =========================
# 3️⃣ 명령 처리
# =========================
response = ""

if "켜" in text:
    print("LED ON")
    ser.write(b'ON\n')
    response = "램프가 켜졌습니다"

elif "꺼" in text:
    print("LED OFF")
    ser.write(b'OFF\n')
    response = "램프가 꺼졌습니다."

elif "온도" in text:
    response = "현재 온도는 25도 입니다"

else:
    response = "명령을 이해하지 못했습니다"

# =========================
# 4️⃣ TTS
# =========================
tts = gTTS(text=response, lang='ko')
tts_path = "C:/temp/response.mp3"
tts.save(tts_path)

os.system(tts_path)

print("🔊 response:", response)