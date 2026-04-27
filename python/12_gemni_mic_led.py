import google.generativeai as genai
import serial
import numpy as np
import whisper

# =========================
# Serial Set
# =========================
PORT = 'COM3'
BAUD = 921600
SAMPLE_RATE = 16000
DURATION = 5
CHUNK = 512

# =========================
# Gemini Set
# =========================
genai.configure(api_key="AIzaSyCAYtjjx4Zcj-ZBhYZWyexld8owmYP403E")
model_gemini = genai.GenerativeModel(
    "gemini-3-flash-preview",
    system_instruction="""
너는 지능형 IoT 제어 시스템이다.
사용자의 명령을 반드시 아래 둘 중 하나로 변환한다:
ON
OFF
"""
)

# =========================
# 초기화
# =========================
ser = serial.Serial(PORT, BAUD, timeout=1)
model_whisper = whisper.load_model("base")
print("생성형AI IoT제어시스템 시작")
print("Start Recording..")
audio_buffer = np.zeros(int(SAMPLE_RATE * DURATION), dtype=np.float32)
idx = 0
for _ in range(int(SAMPLE_RATE / CHUNK * DURATION)):
    data = ser.read(CHUNK * 2)
    if len(data) != CHUNK * 2:
        continue
    samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
    end_idx = idx + CHUNK
    if end_idx <= len(audio_buffer):
        audio_buffer[idx:end_idx] = samples
        idx = end_idx

print("STT 변환 중...")

# =========================
# STT 변환(Whisper)
# =========================
result = model_whisper.transcribe(audio_buffer, language='ko')
text = result["text"].strip()
print("인식:", text)

# =========================
# Gemini 변환(정제필터)
# =========================
try:
    response = model_gemini.generate_content(text)
    raw_cmd = response.text.strip().upper()
    if "ON" in raw_cmd:
        cmd = "ON"
    elif "OFF" in raw_cmd:
        cmd = "OFF"
    else:
        cmd = "UNKNOWN"

except Exception as e:
    print("Gemini 오류:", e)
    cmd = "UNKNOWN"

print("변환:", cmd)

# =========================
# IoT디바이스 데이터 전송
# =========================
if cmd in ["ON", "OFF"]:
    ser.write((cmd + "\n").encode())
    print("전송:", cmd)
else:
    print("유효하지 않은 명령")

print("종료")
ser.close()