import pyttsx3

tts = pyttsx3.init()
tts.setProperty('rate', 170)

tts.say("안녕하세요 Text To Speech 테스트입니다.")
tts.runAndWait()