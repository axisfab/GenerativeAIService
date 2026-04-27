import google.generativeai as genai

genai.configure(api_key="AIzaSyCii06b3wkSXkLci2y7vYJdgfMAiXyl5UM")

model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction="너는 IoT와 AI전문가야. 항상 전문기술적내용으로 설명해줘."
)

chat = model.start_chat(history=[])

while True:
    user_input = input("입력: ")
    response = chat.send_message(user_input)
    print("AI:", response.text)