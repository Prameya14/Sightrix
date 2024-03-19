# Required Imports

import sys
import webbrowser
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import os
import random
import socket
import requests
import wikipedia
import pywhatkit as kit
import json
import smtplib
import subprocess
import pyjokes
import pyautogui
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import PyPDF2
from bs4 import BeautifulSoup
import psutil
import speedtest
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Frontend.gui import Ui_Sightrix
import cv2
import openai

# Fetching Data from JSON File

with open("data.json", "r") as c:
    data = json.load(c)
    contacts = data["contacts"]
    employees = data["employees"]
    music_folder = data["music_folder"]

# Initialization of pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
print(voices)
engine.setProperty("voice", voices[1].id)


# Function 1: Convert Text to Speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Function 2: To Wish User according to Time
def wish_me():
    hours = datetime.now().strftime("%H")
    if hours >= "00" and not "12" <= hours:
        greet = "Good Morning"
    elif hours >= "12" and not "16" <= hours:
        greet = "Good Afternoon"
    else:
        greet = "Good Evening"
    speak(f"{greet} Sir, I am Sightrix! How can I help you?")


# Function 3: To send E-Mail
def send_email(to, subject, body):
    content = body
    email_user = "prameyamohanty14@gmail.com"
    email_password = "wdzgvgjckxincrpq"
    email_send = to

    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = email_send
    msg["Subject"] = subject

    body = content
    msg.attach(MIMEText(body, "plain"))

    text = msg.as_string()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email_user, email_password)

    server.sendmail(email_user, email_send, text)
    server.quit()


# Function 4: To send meeting link to employees
def send_meeting_link(to, subject, body):
    content = body + "\nOnline Meeting Link: https://meet.google.com/vzk-defd-kzk"
    email_user = "prameyamohanty14@gmail.com"
    email_password = "wdzgvgjckxincrpq"
    email_send = to

    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = email_send
    msg["Subject"] = subject

    body = content
    msg.attach(MIMEText(body, "plain"))

    text = msg.as_string()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email_user, email_password)

    server.sendmail(email_user, email_send, text)
    server.quit()


# Function 5: To fetch top headlines
def headlines():
    url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=20f5f34c8e934ffa9bbcc66833b48e52"
    data = requests.get(url).json()
    articles = data["articles"][0:11]
    return articles


# Function 6: To read a PDF File
def read_pdf(file):
    pdf = PyPDF2.PdfFileReader(file)
    pages = pdf.numPages
    for i in range(0, pages):
        speak(pdf.getPage(i).extractText())


# Function 7: To Start Google Meet Meeting by Muting Mic and Stopping Video automatically!
def start_meeting(meet_link):
    webbrowser.open(meet_link)
    time.sleep(4)
    pyautogui.moveTo(760, 730)
    time.sleep(2)
    pyautogui.click()
    time.sleep(2)
    pyautogui.moveTo(1300, 550)
    time.sleep(2)
    pyautogui.click()


# MainThread Class for Starting Sightrix and Executing Tasks
class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("Trainer/trainer.yml")
        cascadePath = "Classifier/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)
        id = 2
        names = ["", "Prameya"]
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640)
        cam.set(4, 480)
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)
        while True:
            ret, img = cam.read()
            converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                converted_image,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )
            for x, y, w, h in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                id, accuracy = recognizer.predict(converted_image[y : y + h, x : x + w])
                if accuracy < 100:
                    print(id)
                    id = names[id - 1]
                    accuracy = "  {0}%".format(round(100 - accuracy))
                    pyautogui.press("esc")
                    speak("Verification Successful!")
                    speak("Welcome Back Sir!")
                    condition = True
                    while condition:
                        permission = self.take_command()
                        if "wake up" in permission:
                            self.task_execution()
                        elif "exit" in permission:
                            speak("Thanks for using me sir!")
                            exit()
                else:
                    id = "unknown"
                    accuracy = "  {0}%".format(round(100 - accuracy))
                    speak("Sorry, Verification Failed!")
            k = cv2.waitKey(0) & 0xFF
            if k == 27:
                break

        print("Thanks for using this program, have a good day.")
        cam.release()
        cv2.destroyAllWindows()

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, phrase_time_limit=5)
        try:
            print("Recognising...")
            text = r.recognize_google(audio, language="en-in")
            print(f"User Said: {text}")
        except:
            return ""
        return text

    def task_execution(self):
        wish_me()
        while True:
            self.query = self.take_command().lower()
            if "open notepad" in self.query:
                speak("Opening Notepad...")
                os.startfile("C:\\Windows\\System32\\notepad.exe")

            elif "close notepad" in self.query:
                speak("Closing Notepad...")
                os.system("taskkill /f /im notepad.exe")

            elif "open terminal" in self.query:
                speak("Opening Command Prompt Terminal...")
                os.startfile("C:\\Windows\\System32\\cmd.exe")

            elif "close terminal" in self.query:
                speak("Closing Command Prompt Terminal...")
                os.system("taskkill /f /im cmd.exe")

            elif "open file explorer" in self.query:
                speak("Opening File Explorer...")
                subprocess.Popen("explorer")

            elif "close file explorer" in self.query:
                speak("Closing File Explorer...")
                os.system("taskkill /f /im explorer.exe")

            elif "play music" in self.query:
                try:
                    speak("Trying to Play Music...")
                    songs = os.listdir(music_folder)
                    song_num = random.randint(0, len(songs) - 1)
                    os.startfile(os.path.join(music_folder, songs[song_num]))
                except Exception as e:
                    speak(
                        f"Sorry! I am unable to play music. An error occurred that is {e}"
                    )

            elif "ip address" in self.query:
                try:
                    speak("Trying to Fetch your IP Address...")
                    net_ip = socket.gethostbyname(socket.gethostname())
                    sys_ip = requests.get("https://api.ipify.org/").text
                    print(
                        f"Your Network IP Address is {net_ip} and your System IP Address is {sys_ip}"
                    )
                    speak(
                        f"Your Network IP Address is {net_ip} and your System IP Address is {sys_ip}"
                    )
                except Exception as e:
                    speak(
                        f"Sorry! I am unable to fetch your IP Address. The error is {e}"
                    )

            elif "wikipedia" in self.query:
                try:
                    keyword = self.query.replace("wikipedia", "")
                    speak("Searching Wikipedia...")
                    result = wikipedia.summary(keyword, sentences=3)
                    print(result)
                    speak(result)
                except Exception as e:
                    speak(
                        f"An error occurred while tring to fetch from wikipedia. The error is {e}"
                    )

            elif "open youtube" in self.query:
                speak("Opening Youtube...")
                webbrowser.open("https://www.youtube.com")

            elif "open facebook" in self.query:
                speak("Opening Facebook...")
                webbrowser.open("https://www.facebook.com")

            elif "open stack overflow" in self.query:
                speak("Opening Stack Overflow...")
                webbrowser.open("https://stackoverflow.com")

            elif "search google" in self.query:
                speak("Please tell what do you want to search in google?")
                search = self.take_command()
                webbrowser.open(f"https://www.google.com/search?q={search}")

            elif "sleep" in self.query:
                speak(
                    "OK Sir! I am going to sleep now! You can wake me up at any time!"
                )
                break

            elif "song on youtube" in self.query:
                speak("Please tell me the song name")
                songname = self.take_command()
                kit.playonyt(songname)

            elif "send email" in self.query:
                speak("What should I say in the E-Mail?")
                content = self.take_command()
                speak("What should I write in the subject of the E-Mail?")
                subject = self.take_command()
                speak("To whom should I send the email?")
                contact = self.take_command().lower()
                if contact in contacts:
                    try:
                        send_email(contacts[contact], subject, content)
                        speak("E-Mail has been sent successfully!")
                    except Exception as error:
                        speak(f"An error occurred which is {error}!")

            elif "tell me a joke" in self.query:
                speak("Here is a joke for you sir!")
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)

            elif "shut down" in self.query:
                speak("Shutting Down your system...")
                os.system("shutdown /s /t 5")

            elif "restart" in self.query:
                speak("Restarting your system...")
                os.system("shutdown /r /t 5")

            elif "sleep" in self.query:
                speak("Going to sleep sir...")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif "switch the window" in self.query:
                speak("Switching the window...")
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "headlines" in self.query:
                speak("Today's top 10 headlines are...")
                news_headlines = headlines()
                for article in news_headlines:
                    print(article["title"])
                    speak(article["title"])

            elif "start meeting" in self.query:
                speak("Sending Invitations to Employees!")
                for employee in employees.keys():
                    try:
                        send_meeting_link(
                            employees[employee],
                            "Meeting Invitation",
                            "Please join the Online Meeting!",
                        )
                    except Exception as error:
                        speak(f"An error occurred which is {error}!")
                speak("Starting meeting...")
                start_meeting("https://meet.google.com/faw-itnv-nob")

            elif "location" in self.query:
                speak("Please wait sir! I am checking your location...")
                try:
                    ip = requests.get("https://api.ipify.org/").text
                    url = f"https://get.geojs.io/v1/ip/geo/{ip}.json"
                    geo_data = requests.get(url).json()
                    speak(
                        f"Sir, I am not sure but I think you are in {geo_data['city']} of {geo_data['region']}!"
                    )
                except:
                    speak(
                        "Sorry sir! I am unable to find our current location due to network issues!"
                    )

            elif "read pdf" in self.query:
                speak("Sir, please enter the path of your pdf file...")
                filepath = input("Enter: ")
                if not filepath.endswith(".pdf"):
                    speak("Sorry sir this is not a pdf file!")
                else:
                    read_pdf(filepath)

            elif "file visibility" in self.query:
                speak("Please enter the path of the folder...")
                folder_path = input("Enter: ")
                speak(
                    "Sir you want to hide files in this folder or show files in this folder?"
                )
                choice = self.take_command()
                if "hide" in choice:
                    os.chdir(folder_path)
                    os.system("attrib +h /s /d")
                    speak("All files in this folder are now hidden!")
                elif "show" in choice:
                    os.chdir(folder_path)
                    os.system("attrib -h /s /d")
                    speak("All files in this folder are now visible!")

            elif "weather report" in self.query:
                speak("Please tell me your city name...")
                city = self.take_command()
                url = f"https://www.google.com/search?q=temperature%20in%20{city}"
                response = requests.get(url).text
                temp = (
                    BeautifulSoup(response, "html.parser")
                    .find("div", class_="BNeawe")
                    .text
                )
                speak(f"Current Temperature in {city} is {temp}!")

            elif "battery percentage" in self.query:
                speak("Please wait sir! I am checking your battery percentage...")
                percent = psutil.sensors_battery().percent
                speak(f"Sir your system has {percent}% battery!")

            elif "internet speed" in self.query:
                speak("Please wait sir! I am checking your internet speed...")
                tester = speedtest.Speedtest()
                download = int(int(tester.download()) / 1000000)
                upload = int(int(tester.upload()) / 1000000)
                speak(
                    f"Sir you have {download} Mbps download speed and {upload} Mbps upload speed!"
                )

            elif "volume up" in self.query:
                speak("Increasing your Volume...")
                pyautogui.press("volumeup")

            elif "volume down" in self.query:
                speak("Decreasing your Volume...")
                pyautogui.press("volumedown")

            elif "mute" in self.query:
                speak("Muting your speaker...")
                pyautogui.press("volumemute")

            elif "folder content" in self.query:
                content = os.listdir()
                speak("This folder contains the following files...")
                for file in content:
                    speak(file)

            elif "gpt chat" in self.query:
                speak(
                    "GPT Chat Mode has been enabled. Please tell what do you want to ask to GPT?"
                )
                prompt = self.take_command()
                try:
                    openai.api_key = (
                        "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"
                    )
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-0301",
                        messages=[{"role": "user", "content": prompt}],
                    )
                    speak(
                        f'Here is the response from GPT:\n{response["choices"][0]["message"]["content"]}'
                    )
                except Exception as e:
                    speak(
                        f"An error occurred while trying to fetch response from GPT that is {e}"
                    )

            elif "gpt edit" in self.query:
                speak(
                    "GPT Edit Mode has been enabled. Please instruct GPT on what has to be edited."
                )
                instruction = self.take_command()
                speak("Tell the input text that you want to edit.")
                prompt = self.take_command()
                try:
                    openai.api_key = (
                        "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"
                    )
                    response = openai.Edit.create(
                        model="text-davinci-edit-001",
                        input=prompt,
                        instruction=instruction,
                        temperature=0.7,
                        top_p=1,
                    )
                    speak(
                        f'Here is the response from GPT:\n{response["choices"][0]["text"]}'
                    )
                except Exception as e:
                    speak(
                        f"An error occurred while trying to fetch response from GPT that is {e}"
                    )

            else:
                speak("Sorry sir, I did not get you! Please tell me something else!")


start_execution = MainThread()

# Main Class for controlling GUI


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Sightrix()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.start_task)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.showMaximized()
        self.setWindowIcon(QtGui.QIcon("Images/icon.png"))

    def start_task(self):
        self.ui.movie = QtGui.QMovie("Images/new-bg.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)
        start_execution.start()

    def show_time(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString("hh:mm:ss")
        self.ui.textBrowser.setStyleSheet(
            "background: transparent;\n"
            "border: none;\n"
            "color: green;\n"
            "font-size: 50px;\n"
            "font-family: Imprint MT Shadow;\n"
            "margin-top:0px;\n"
            "margin-bottom:0px;\n"
            "margin-left:0px;\n"
            "margin-right:0px;\n"
            "-qt-block-indent:0;\n"
            "text-indent:0px;"
        )
        self.ui.textBrowser.setText(label_time)


app = QApplication(sys.argv)
sightrix = Main()
sightrix.show()
exit(app.exec_())
