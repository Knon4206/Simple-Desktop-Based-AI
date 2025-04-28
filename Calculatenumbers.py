import wolframalpha
import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    print(f": {audio}")
    engine.say(audio)
    engine.runAndWait()

def WolfRamAlpha(query):
    apikey = "LR33QE-LUP5Q99YK4"  # Replace with your own WolframAlpha API key
    requester = wolframalpha.Client(apikey)
    try:
        requested = requester.query(query)
        answer = next(requested.results).text
        return answer
    except:
        speak("The value is not answerable")
        return None

def Calc(query):
    query = query.lower()
    query = query.replace("multiply", "*")
    query = query.replace("plus", "+")
    query = query.replace("minus", "-")
    query = query.replace("divide", "/")

    try:
        result = WolfRamAlpha(query)
        if result:
            speak(f"The result is {result}")
    except:
        speak("The value is not answerable")
