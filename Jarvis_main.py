# JARVIS - Fully Integrated Version with Commands and UI Inputs
# Requirements: pip install pyqt5 pyttsx3 SpeechRecognition pygame requests bs4 plyer speedtest-cli
import datetime
import os
import sys
import webbrowser

import plyer
import pyttsx3
import requests
import speech_recognition as sr
import speedtest
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QInputDialog, \
    QSizePolicy, QSpacerItem
from bs4 import BeautifulSoup
from plyer import notification
from pygame import mixer

import Cal

engine = pyttsx3.init()

class JarvisUI(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("NovaDex Login")
        self.showFullScreen()  # Fullscreen mode
        self.setStyleSheet("background-color: black;")
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Pre-login Animation
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)

        self.logo_movie = QMovie("logo.gif")  # Pre-login animation
        self.logo_movie.setScaledSize(self.size() * 0.8)
        self.gif_label.setMovie(self.logo_movie)
        self.logo_movie.start()

        self.layout.addWidget(self.gif_label)

        self.layout.addItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.input_field = QLineEdit(self)
        self.input_field.setEchoMode(QLineEdit.Password)
        self.input_field.setMaximumWidth(300)
        self.input_field.setAlignment(Qt.AlignCenter)
        self.input_field.setStyleSheet(
            "color: white; font-size: 16px; background-color: #222; border: 1px solid white; padding: 5px;")
        self.layout.addWidget(self.input_field, alignment=Qt.AlignCenter)

        self.layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.button = QPushButton("Login", self)
        self.button.setStyleSheet("font-size: 14px; padding: 6px; background-color: white; color: black;")
        self.button.setFixedSize(150, 40)
        self.layout.addWidget(self.button, alignment=Qt.AlignCenter)

        self.layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))


        self.speech_label = QLabel("", self)
        self.speech_label.setStyleSheet("color: white; font-size: 18px;")
        self.speech_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.speech_label)

        # Initially hide input and button until Startup2.mp3 finishes
        self.input_field.setVisible(False)
        self.button.setVisible(False)


        self.button.clicked.connect(self.check_password)


        self.setLayout(self.layout)

        self.engine = pyttsx3.init("sapi5")
        self.engine.setProperty("voice", self.engine.getProperty("voices")[0].id)
        self.engine.setProperty("rate", 170)

        # Set up the layout
        self.layout = QVBoxLayout(self)

        # Add a label to display instructions
        self.label = QLabel("Please enter the number of tasks:", self)
        self.label.setStyleSheet("color: white;")
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # Add a button to trigger the input dialog
        self.input_button = QPushButton("Enter Tasks", self)
        self.input_button.clicked.connect(self.show_input_dialog)
        self.layout.addWidget(self.input_button, alignment=Qt.AlignCenter)

        # Set the window to full screen
        self.showFullScreen()


    def show_input_dialog(self):

        # Show the input dialog and get the user's response
        user_input = self.get_user_input("Enter number of tasks")
        if user_input is not None:
            try:
                # Attempt to convert the input to an integer
                no_tasks = int(user_input)
                self.label.setText(f"Number of tasks: {no_tasks}")
            except ValueError:
                self.label.setText("Invalid input. Please enter a valid number.")
        else:
            self.label.setText("No input received.")

    def get_user_input(self, prompt):
        # Ensure that QApplication is running
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        # Show the input dialog with self as the parent
        text, ok = QInputDialog.getText(self, "Input Required", prompt)

        # Check if user pressed OK and entered non-empty text
        if ok and text.strip():
            return text.strip()

        # Return None if cancelled or empty
        return None

    def start_audio(self):
        mixer.init()
        mixer.music.load("Startup2.mp3")  # First animation music
        mixer.music.play()

        # Wait for the music to finish
        QTimer.singleShot(5000, self.show_login_widgets)  # Adjust the time accordingly for music length




  

    def show_login_widgets(self):
        self.input_field.setVisible(True)  # Make input field visible
        self.button.setVisible(True)  # Make login button visible


    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.speech_label.setText("Listening...")
            r.pause_threshold = 1
            r.energy_threshold = 300
            audio = r.listen(source, 0, 4)
        try:
            self.speech_label.setText("Understanding...")
            query = r.recognize_google(audio, language='en-in')
            self.speech_label.setText(f"You said: {query}")
        except:
            self.speech_label.setText("Say that again...")
            return "None"
        return query

    def check_password(self):
        with open("password.txt", "r") as pw_file:
            pw = pw_file.read()
        if self.input_field.text() == pw:
            self.start_jarvis()
        else:
            self.speech_label.setText("Incorrect password. Try again.")

    def start_jarvis(self):
        self.input_field.hide()
        self.button.hide()

        # Switch to post-login animation
        self.logo_movie.stop()
        self.movie = QMovie("ani.gif")  # <-- replace with your post-login animation
        self.movie.setScaledSize(self.size() * 0.8)
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        self.setWindowTitle("NovaDex AI Assistant")
        self.speak("Welcome Sir, please say wake up to activate me.")
        self.listen_for_wake()

    def listen_for_wake(self):
        import threading
        def run():
            while True:
                query = self.take_command().lower()
                if "wake up" in query:
                    from GreetMe import greetMe
                    greetMe()
                    self.main_loop()
                    break

                if "exit" in query:
                    pyttsx3.speak("Going to sleep, sir")
                    self.close()

        threading.Thread(target=run, daemon=True).start()

    def main_loop(self):
        def run():
            global pyautogui
            while True:
                query = self.take_command().lower()
                if "go to sleep" in query:
                    self.speak("Okay sir, I am going to sleep. Say 'wake up' when you need me.")
                    self.listen_for_wake()
                    break  # Stop the main loop, shift to wake-up listener

                elif "change password" in query:
                    self.speak("What's the new password")
                    new_pw = self.get_user_input("Enter new password")
                    with open("password.txt", "w") as f:
                        f.write(new_pw)
                    self.speak("Done sir")
                    continue

                elif "calculate" in query or "calculation" in query:
                    Cal.calc(query)

                elif "schedule my day" in query:
                    self.speak("Do you want to clear old tasks?")
                    response = self.take_command().lower()

                    if "yes" in response:
                        open("tasks.txt", "w").close()

                    user_input = self.get_user_input("Enter number of tasks")
                    if user_input is not None:
                        try:
                            no_tasks = int(user_input)
                            with open("tasks.txt", "a") as file:
                                for i in range(no_tasks):
                                    task = self.get_user_input(f"Enter task {i + 1}")
                                    if task:
                                        file.write(f"{i + 1}. {task}\n")
                                        self.speak(f"Task {i + 1} added.")
                                    else:
                                        self.speak("No task entered. Skipping.")
                        except ValueError:
                            self.speak("Invalid number entered.")
                    else:
                        self.speak("No input received for number of tasks.")

                elif "show my schedule" in query:
                    try:
                        with open("tasks.txt", "r") as file:
                            content = file.read().strip()

                        if content:
                            # Compact content to fit notification limit (approx 250 chars)
                            formatted = content.replace("\n", " \n ")
                            if len(formatted) > 250:
                                formatted = formatted[:247] + "..."

                            plyer.notification.notify(
                                title="📅 My Schedule",
                                message=formatted,
                                timeout=15
                            )

                            mixer.init()
                            mixer.music.load("notification.mp3")
                            mixer.music.play()

                            self.speak("Here is your schedule.")
                        else:
                            self.speak("Your schedule is empty.")
                    except FileNotFoundError:
                        self.speak("Schedule file not found.")

                elif "internet speed" in query:
                    self.speak("Just wait for a moment, checking your internet speed.")
                    wifi = speedtest.Speedtest()
                    download = wifi.download() / 1048576  # Convert from bits to megabits
                    upload = wifi.upload() / 1048576
                    f"Download Speed: {download:.2f} Mbps\nUpload Speed: {upload:.2f} Mbps"
                    self.speak(f"Download speed is {download:.2f} Mbps")
                    self.speak(f"Upload speed is {upload:.2f} Mbps")

                elif "ipl score" in query:
                    try:
                        url = "https://www.cricbuzz.com/"
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                        }
                        page = requests.get(url, headers=headers)
                        soup = BeautifulSoup(page.text, "html.parser")

                        # Try to locate match containers safely
                        match_containers = soup.find_all("div", class_="cb-mtch-lst cb-col cb-col-100 cb-tms-itm")
                        if match_containers:
                            first_match = match_containers[0]
                            team_names = first_match.find_all("div", class_="cb-hmscg-tm-nm")
                            team_scores = first_match.find_all("div", class_="cb-hmscg-tm-scr")

                            team1 = team_names[0].text.strip() if len(team_names) > 0 else "Team 1"
                            team2 = team_names[1].text.strip() if len(team_names) > 1 else "Team 2"
                            score1 = team_scores[0].text.strip() if len(team_scores) > 0 else "N/A"
                            score2 = team_scores[1].text.strip() if len(team_scores) > 1 else "N/A"

                            message = f"{team1}: {score1}\n{team2}: {score2}"
                        else:
                            message = "Could not find any live match information."

                        notification.notify(title="IPL SCORE", message=message, timeout=15)
                        self.speak("Here is the current IPL score")
                    except Exception as e:
                        self.speak("Sorry, I couldn't fetch the IPL score.")
                        print("IPL Error:", e)

                elif "open" in query:
                    query = query.replace("open", "").strip()
                    try:
                        import pyautogui
                        pyautogui.press("super")
                    except Exception as e:
                        print(f"Could not simulate key press: {e}")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")

                elif "start typing" in query:
                    self.speak("Starting voice typing. Say 'stop typing' to end.")

                    import pyautogui
                    import speech_recognition as sr

                    r = sr.Recognizer()
                    while True:
                        with sr.Microphone() as source:
                            self.speech_label.setText("Listening for text...")
                            r.pause_threshold = 1
                            audio = r.listen(source, phrase_time_limit=5)
                        try:
                            typed_text = r.recognize_google(audio, language="en-in").lower()
                            self.speech_label.setText(f"You said: {typed_text}")

                            if "stop typing" in typed_text:
                                self.speak("Voice typing stopped.")
                                break
                            pyautogui.write(typed_text + " ", interval=0.05)
                        except:
                            self.speech_label.setText("Didn't catch that. Say again.")


                elif "close" in query:
                    import pyautogui
                    self.speak("Closing the current tab")
                    pyautogui.hotkey("ctrl", "w")



                elif "translate" in query:
                    from Translator import translategl
                    import asyncio

                    self.speak("What sentence do you want to translate?")
                    to_translate = self.get_user_input("Enter the sentence you want to translate:").lower()

                    self.speak("Enter the language code (like 'en' for English, 'fr' for French, etc.)")
                    to_lang = self.get_user_input("Enter target language code (e.g., 'en', 'fr', 'hi'):")

                    to_translate = to_translate.replace("jarvis", "").replace("translate", "").strip()

                    async def run_translation():
                        try:
                            translated_text = await translategl(to_translate, to_lang)

                            popup = JarvisUI.TranslationPopup(translated_text)
                            popup.exec_()
                        except:
                            print()
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            loop.create_task(run_translation())
                        else:
                            loop.run_until_complete(run_translation())
                    except RuntimeError:
                        try:
                            asyncio.run(run_translation())
                            continue
                        except:
                            continue

                elif "hello" in query or "hii" in query:
                    pyttsx3.speak("Hello sir, how are you ?")
                elif "i am fine" in query:
                    pyttsx3.speak("that's great, sir")
                elif "how are you" in query or "how r u" in query:
                    pyttsx3.speak("Perfect, sir")
                elif "thank you" in query or "thank u" in query:
                    pyttsx3.speak("you are welcome, sir")

                elif "play songs" in query:
                    self.speak("Please enter the song name, Sir.")

                    from PyQt5.QtWidgets import QInputDialog, QApplication

                    # Make sure there is a QApplication instance
                    app = QApplication.instance()
                    if app is None:
                        app = QApplication([])  # Only create if not already created

                    # Now show the input dialog
                    song_name, ok = QInputDialog.getText(self, "Song Request", "Enter the song name:")

                    if ok and song_name.strip():
                        song_name = song_name.strip()
                        self.speak(f"Searching for {song_name} on YouTube!")

                        web = "https://www.youtube.com/results?search_query=" + song_name.replace(' ', '+')
                        webbrowser.open(web)

                        try:
                            import pywhatkit
                            pywhatkit.playonyt(song_name)
                            self.speak("Playing now, Sir!")
                        except Exception as e:
                            print("Error playing song directly:", e)
                            self.speak("Opened search results, Sir. Please select the song manually.")
                    else:
                        self.speak("No song name entered, Sir.")


                elif "pause" in query or "pause song" in query:
                    pyautogui.press("k")
                    pyttsx3.speak("video paused")
                elif "play" in query or "play song" in query:
                    pyautogui.press("k")
                    pyttsx3.speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    pyttsx3.speak("video muted")

                elif "volume up" in query:
                    from keyboard import volumeup
                    pyttsx3.speak("Turning volume up,sir")
                    volumeup()

                elif "volume down" in query:
                    from keyboard import volumedown
                    pyttsx3.speak("Turning volume down, sir")
                    volumedown()

                elif "screenshot" in query:
                    im = pyautogui.screenshot()
                    im.save("screenshot.png")
                    self.speak("Screenshot taken")

                elif "click my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(5)
                    pyautogui.press("enter")

                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")
                    self.speak(f"Sir, the time is {strTime}")

                elif "finally sleep" in query:
                    self.speak("Going to sleep, sir")
                    self.close()

                elif "shutdown system" in query:
                    pyttsx3.speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                        os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                        break


                elif "tell me a joke" in query:
                    import  pyjokes
                    joke = pyjokes.get_joke()
                    # Store the current speaking rate
                    original_rate = engine.getProperty('rate')
                    # Set a slower speaking rate
                    engine.setProperty('rate', 130)  # You can adjust this value (default is ~200)
                    self.speak(joke)
                    # Restore the original speaking rate
                    engine.setProperty('rate', original_rate)

                elif "search" in query:
                    self.speak("What should I search for?")
                    search_query = self.take_command().lower()

                    if search_query != "none" and search_query.strip() != "":
                        self.speak(f"Searching for {search_query} on the web.")
                        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                        webbrowser.open(search_url)
                    else:
                        self.speak("I did not catch what you want to search.")



        import threading
        threading.Thread(target=run, daemon=True).start()


def test_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    ping = st.results.ping

    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")
    print(f"Ping: {ping:.2f} ms")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisUI()
    window.show()
    # Start the audio and make login widgets visible after the audio finishes
    window.start_audio()
    
    test_speed()
    sys.exit(app.exec_())