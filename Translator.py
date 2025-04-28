import googletrans
from googletrans import Translator
from gtts import gTTS
import pyttsx3
import os
import pygame
import time

# Initialize pyttsx3 for speaking
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


async def translategl(query, language):
    speak("Sure sir")
    print(googletrans.LANGUAGES)
    translator = Translator()

    # Translate the input text
    text_to_translate = await translator.translate(query, src="auto", dest=language)
    text = text_to_translate.text
    print("Translated Text:", text)

    try:
        # Use gTTS to convert the translated text to speech
        speakgl = gTTS(text=text, lang=language, slow=False)
        speakgl.save("voice.mp3")

        # Play the audio translation
        pygame.mixer.init()
        pygame.mixer.music.load("voice.mp3")
        pygame.mixer.music.play()
        time.sleep(5)  # Wait for the audio to finish
        os.remove("voice.mp3")  # Clean up the audio file

    except Exception as e:
        print("Unable to translate:", e)

    return text
