import google.generativeai as genai

genai.configure(api_key="AIzaSyCii06b3wkSXkLci2y7vYJdgfMAiXyl5UM")

for m in genai.list_models():
    print(m.name)