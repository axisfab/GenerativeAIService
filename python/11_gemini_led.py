import google.generativeai as genai
import serial

genai.configure(api_key="AIzaSyCAYtjjx4Zcj-ZBhYZWyexld8owmYP403E")

ser = serial.Serial("COM3", 115200)

model = genai.GenerativeModel(
    "gemini-3-flash-preview",
    #"gemini-3.1-flash-lite-preview",
    system_instruction="""
너는 IoT 제어 변환기다.
사용자의 명령을 반드시 아래 둘 중 하나로 변환한다:
ON
OFF
"""
)

while True:
    user_input = input("명령 입력: ")

    response = model.generate_content(user_input)
    cmd = response.text.strip()

    print("변환:", cmd)

    if cmd in ["ON", "OFF"]:
        ser.write((cmd + "\n").encode())