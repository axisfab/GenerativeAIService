import google.generativeai as genai

genai.configure(api_key="AIzaSyCii06b3wkSXkLci2y7vYJdgfMAiXyl5UM")

model = genai.GenerativeModel(
    "gemini-3-flash-preview",
    generation_config={
        "response_mime_type": "application/json"
    }
)
response = model.generate_content("거실의 조명을 초록색으로 50%밝기로 켜줘")

print(response.text)