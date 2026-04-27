import google.generativeai as genai

genai.configure(api_key="AIzaSyCii06b3wkSXkLci2y7vYJdgfMAiXyl5UM")

model = genai.GenerativeModel(
    "gemini-3-flash-preview",
    system_instruction="""
너는 IoT 제어 JSON 생성기.
반드시 아래 JSON 구조만 사용.
{
  "device": "string",
  "action": "on | off",
  "location": "string",
  "color": "string",
  "brightness": number
}

규칙:
- JSON 외 다른 텍스트 출력 금지
- 없는 값은 null로 설정
- brightness는 0~100 숫자
""",
    generation_config={
        "response_mime_type": "application/json"
    }
)

user_input = input("입력: ")
response = model.generate_content(user_input)
print("result:", response.text)
