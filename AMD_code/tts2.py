import pyttsx3

engine = pyttsx3.init("espeak")
engine.setProperty('rate', 125)

def speak(text):
    engine.say(text)
    engine.runAndWait()

speak("Menu")
speak("Pill Information")
speak("Time")
