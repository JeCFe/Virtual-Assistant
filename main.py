import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia
import playsound
from pydub import AudioSegment
from pydub.playback import play

warnings.filterwarnings('ignore')



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




def miniResponse(data):
    print(data)
    myobject = gTTS(text = data, lang ='en', slow=False)
    myobject.save('assistant_response.mp3')
    playsound.playsound('assistant_response.mp3', True)



def wakeCommand(data):
    wake_phrases = ['ok mini', 'hey mini']
    data = data.lower()
    for item in wake_phrases:
        if item in data:
            return True
    return False

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






print(getDate())
miniResponse(getDate())


