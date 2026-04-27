import google.generativeai as genai
import serial
from gtts import gTTS
import os
import time

genai.configure(api_key="AIzaSyCAYtjjx4Zcj-ZBhYZWyexld8owmYP403E")

ser = serial.Serial("COM3", 115200, timeout=2)

model = genai.GenerativeModel(
    "gemini-3-flash-preview",
    #"gemini-3.1-flash-lite-preview",
    system_instruction="""
너는 IoT 제어 시스템이다.
사용자의 말을 아래 JSON으로 변환한다:
덥다 → {"action":"HOT"}
춥다 → {"action":"COLD"}
다른 말 하지마.
"""
)

while True:
    text = input("입력: ")
    res = model.generate_content(text)
    cmd = res.text.strip()

    print("변환:", cmd)

    # =========================
    # HOT
    # =========================
    if "HOT" in cmd:
        ser.reset_input_buffer()
        ser.write(b"TEMP\n")
        time.sleep(1)
        ser.write(b"BLUE\n")

        response = ser.readline().decode(errors='ignore').strip()
        print("🌡 온도값:", response)

        # 온도 파싱
        if "TEMP:" in response:
            temp = response.split(",")[0].replace("TEMP:", "")
            tts_text = f"현재 온도는 {temp}도 입니다. 더우신가요? 시원하게 해드릴께요."
        else:
            tts_text = "온도 정보를 가져오지 못했습니다."

    # =========================
    # COLD
    # =========================
    elif "COLD" in cmd:
        ser.write(b"TEMP\n")
        ser.write(b"RED\n")

        response = ser.readline().decode(errors='ignore').strip()
        print("🌡 온도값:", response)

        if "TEMP:" in response:
            temp = response.split(",")[0].replace("TEMP:", "")
            tts_text = f"현재 온도는 {temp}도 입니다. 추우신가봐요. 따뜻하게 해드릴께요."
        else:
            tts_text = "온도 정보를 가져오지 못했습니다."

    else:
        tts_text = "명령을 이해하지 못했습니다."

    # =========================
    # 🔊 TTS 출력
    # =========================
    try:
        tts = gTTS(text=tts_text, lang='ko')
        file_path = "C:/temp/response.mp3"
        tts.save(file_path)

        os.system(f'start "" "{file_path}"')

    except Exception as e:
        print("TTS 오류:", e)

    print("음성:", tts_text)