import google.generativeai as genai

genai.configure(api_key="AIzaSyCii06b3wkSXkLci2y7vYJdgfMAiXyl5UM")

model = genai.GenerativeModel("gemini-3-flash-preview")

chat = model.start_chat(history=[])

while True:
    user_input = input("입력: ")

    response = chat.send_message(user_input)

    print("AI:", response.text)