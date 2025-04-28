import pyttsx3
import wolframalpha

Assistant = pyttsx3.init('sapi5')
voices = Assistant.getProperty('voices')
Assistant.setProperty('voice', voices[0].id)
Assistant.setProperty('rate', 200)

def Speak(audio):
    print(f": {audio}")
    Assistant.say(audio)
    Assistant.runAndWait()

def Wolfram(query):
    api_key = "LR33QE-LUP5Q99YK4"  # Make sure this key is valid
    requester = wolframalpha.Client(api_key)
    try:
        requested = requester.query(query)
        answer = next(requested.results).text
        return answer
    except Exception:
        return None

def calc(query):
    query = query.lower().replace("era", "")
    query = query.replace("plus", "+").replace("minus", "-")
    query = query.replace("divide", "/").replace("multiply", "*")

    result = Wolfram(query)
    if result:
        Speak(f"The answer is: {result}")
    else:
        Speak("Sorry sir, the query is not answerable.")
