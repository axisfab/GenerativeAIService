#pip install google-generativeai


import google.generativeai as genai

genai.configure(api_key="AIzaSyCii06b3wkSXkLci2y7vYJdgfMAiXyl5UM")

model = genai.GenerativeModel("gemini-3-flash-preview")

while True:
    user_input = input("입력: ")

    response = model.generate_content(user_input)

    print("AI:", response.text)
    print("API TOKEN:", response.usage_metadata)