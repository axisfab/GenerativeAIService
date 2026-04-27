import google.generativeai as genai
import serial

genai.configure(api_key="AIzaSyCAYtjjx4Zcj-ZBhYZWyexld8owmYP403E")

ser = serial.Serial("COM3", 115200, timeout=2)

model = genai.GenerativeModel(
    "gemini-3-flash-preview",
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
        ser.write(b"TEMP\n")
        ser.write(b"BLUE\n")

        # IoT 디바이스 응답 읽기(온도값)
        response = ser.readline().decode().strip()
        print("현재 온도값:", response)

    # =========================
    # COLD
    # =========================
    elif "COLD" in cmd:
        ser.write(b"TEMP\n")
        ser.write(b"RED\n")

        # IoT 디바이스 응답 읽기(온도값)
        response = ser.readline().decode().strip()
        print("온도값:", response)