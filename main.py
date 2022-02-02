import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia
import playsound
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
from pyttsx3 import voice

warnings.filterwarnings('ignore')
#Set up the text to speech voice
voiceEngine = pyttsx3.init()
voices = voiceEngine.getProperty('voices')
voiceEngine.setProperty('voice', voices[0].id)

def listenToAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Talk")
        audio = r.listen(source)
    data = ''
    try:
        data = r.recognize_google(audio)
        print("You said " + data)
    except sr.UnknownValueError:
        print("Oops didn't quite catch that")
    except sr.RequestError as e:
        print("Request results from google recognition error: " + e)
    return data




def speechResponse(data):
    print("here")
    print(data)
    voiceEngine.say(data)
    voiceEngine.runAndWait()


#this will listen for wake word then will return what was said after the wake word
def wakeCommand(data):
    wake_phrases = ['omega','hey omega']
    data = data.lower()
    command = ""
    iterator = 0

    for item in wake_phrases:
        if item in data:
            offset = len(item)
            for i in range(iterator + offset, len(data)):
                command = command + data[i]

            return command.lstrip(' ')
        iterator +=1
    command = ""
    return command


def getDate():
    now = datetime.datetime.now()
    dateToday = datetime.datetime.today()
    weekday = calendar.day_name[dateToday.weekday()]
    month = now.month
    day = now.day
    year = now.year

    monthData = ['January', 'February', 'March', 'April', 'may', 'June', 'July',
                 'August', 'September', 'October', 'November', 'December']

    amendedNumber = ""
    day = str(day)
    if(day == '1' or day == '21' or day == '31'):
        amendedNumber = day + "st"
    elif(day == '2' or day == '22'):
        amendedNumber = day + "nd"
    elif(day == '3' or day == '23'):
        amendedNumber = day + "rd"
    else:
        amendedNumber = day + "th"

    return "Today is  " + str(weekday)+" "+ str(amendedNumber) + " of " + str(monthData[month - 1] )+ " " + str(year)

def greeting(data):
    input = ['hello', 'hi']
    output = ['hello', 'hi']
    for word in data.split():
        if word.lower() in input:
            return random.choice(output)
    return ""


def pullName(data):
    wordArray = data.split()
    name = ""
    for i in range(0, len(wordArray)):
        if i + 3 <= len(wordArray):
            if (wordArray[i].lower() == 'who' and wordArray[i+1].lower() == 'is'):
                for j in range(i+2, len(wordArray)):
                    name = name + wordArray[j] + " "
            elif(wordArray[i] == "who's"):
                for j in range(i+1, len(wordArray)):
                    name = name + wordArray[j] + " "
        return name


def manageCommandOption(data):
    command = data.split()

    if (command[0] == 'who' and command[1] == 'is') or command[0] == "who's":
        wikiResponse = ""
        name = pullName(data).title()
        name = ''.join(name.split())
        print(name)
        wikiInfo = wikipedia.summary(name, sentences = 2)
        speechResponse(wikiInfo)



while (True):
    data = listenToAudio()
    response = ''
    command = wakeCommand(data)
    if(command != "" ): #We know there has been a command given
        manageCommandOption(command)






