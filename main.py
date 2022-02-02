import speech_recognition as sr
import config
import os
import geocoder
import requests
import pyowm
import datetime
import warnings
import calendar
import random
import wikipedia
import json
import pyttsx3


personalInfo = None
wakeWords = []
warnings.filterwarnings('ignore')
# Set up the text to speech voice
voiceEngine = pyttsx3.init()
voices = voiceEngine.getProperty('voices')
voiceEngine.setProperty('voice', voices[1].id)


def validateYesorNo():
    while True:
        response = listenToAudio()
        print(response)
        if response == "yes":
            print("answered yes")
            return True
        elif response == "no":
            print("answeered no")
            return False
        else:
            speechResponse("Sorry I didnt quite catch that. Please answer with yes or no ")


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

# Only returns weather in the current area
def weatherQuestion(option):
    apiKey = config.weatherappAPIKey
    geolocation = geocoder.ip('me')
    print(geolocation)
    print(geolocation.lat)
    lat = geolocation.lat
    lon = geolocation.lng
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=minutely,hourly,alerts&appid=%s&units=metric" % (
        lat, lon, apiKey)
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)
    with open('weather.json', 'w') as jsonFile:
        json.dump(data, jsonFile)

    city = geolocation.city

    if option == "current":
        temp = str(data["current"]["temp"])
        currentSpeed = str(data["current"]["wind_speed"])
        weatherType = str(data["current"]["weather"][0]["description"])
        speechResponse(
            "In " + city + " it is currently " + weatherType + " at a temperature of " + temp + " degrees and you can expect wind speeds of up to " + currentSpeed + " kilometers per hour")

    if option == "today":
        # Todays weather
        dayTemp = str(data["daily"][0]["temp"]["day"])
        nightTemp = str(data["daily"][0]["temp"]["night"])
        morningTemp = str(data["daily"][0]["temp"]["morn"])
        minTemp = str(data["daily"][0]["temp"]["min"])
        maxTemp = str(data["daily"][0]["temp"]["max"])
        dailySpeeds = str(data["daily"][0]["wind_speed"])
        dailyGusts = str(data["daily"][0]["wind_gust"])
        dailyWeatherType = str(data["daily"][0]["weather"][0]["description"])

        speechResponse("Today in " + city + " you can expect morning temperatures of "
                       + morningTemp + " degrees with day temperatures of " + dayTemp + " degrees and night temperatures of " + nightTemp + " degrees. " +
                       "Throughout the day you can expect a low of " + minTemp + " degrees and a max of " + maxTemp + " degrees. Wind speeds can be expected to reach " +
                       dailySpeeds + " kilometers per hour, with gusts reaching " + dailyGusts + " kilometers per hour. Today you can expect " + dailyWeatherType)


def whatQuestion(data):
    acceptedCommands = ['current weather', 'weather']
    commandToUse = None
    for item in acceptedCommands:
        if item in data:
            commandToUse = item
            break
    if commandToUse == None:
        speechResponse("Sorry I either didn't understand you, or I currently cannot do that task")
    print(commandToUse)

    if commandToUse == acceptedCommands[0]:
        weatherQuestion("current")
    elif commandToUse == acceptedCommands[1]:
        weatherQuestion("today")

    # what is the time
    # waht is the date
    # what is the weather
    # what is the current weather
    # what is love
    #

    response = ""
    return response


def speechResponse(data):
    print(data)
    voiceEngine.say(data)
    voiceEngine.runAndWait()


# this will listen for wake word then will return what was said after the wake word
def wakeCommand(data):
    global wakeWords
    data = data.lower()
    command = ""
    iterator = 0
    for item in wakeWords:
        if item in data:
            offset = len(item)
            for i in range(iterator + offset, len(data)):
                command = command + data[i]
            return command.lstrip(' ')
        iterator += 1
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
    if day == '1' or day == '21' or day == '31':
        amendedNumber = day + "st"
    elif day == '2' or day == '22':
        amendedNumber = day + "nd"
    elif day == '3' or day == '23':
        amendedNumber = day + "rd"
    else:
        amendedNumber = day + "th"
    return "Today is  " + str(weekday) + " " + str(amendedNumber) + " of " + str(monthData[month - 1]) + " " + str(year)


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
            if wordArray[i].lower() == 'who' and wordArray[i + 1].lower() == 'is':
                for j in range(i + 2, len(wordArray)):
                    name = name + wordArray[j] + " "
            elif wordArray[i] == "who's":
                for j in range(i + 1, len(wordArray)):
                    name = name + wordArray[j] + " "
        return name


def helpManager():
    global personalInfo
    speechResponse("How may I help you " + personalInfo.getName())
    speechResponse("Please respond with, change nickname, change assistant name, or list commands")
    correctInput = False
    while not correctInput:
        response = listenToAudio()
        if response == "change nickname":
            personalInfo.setName()
            correctInput = True
        elif response == "change assistant name":
            personalInfo.setAssistantName()
            correctInput = True
        elif response == "list commands":
            speechResponse("I can currently understand the following.")
            speechResponse("Who is named person.")
            speechResponse("What is. This can be used to find the current date and time. More to come")
            # Add future commands options here
            correctInput = True
        else:
            speechResponse("Sorry I didn't quite catch that")
    return False


def manageCommandOption(data):
    command = data.split()
    print(command)
    speakResponse = ""
    if (command[0] == 'who' and command[1] == 'is') or command[0] == "who's":
        name = pullName(data).title()
        name = ''.join(name.split())
        speakResponse = wikipedia.summary(name, sentences=2)

    elif command[0] == "what":
        speakResponse = whatQuestion(data)
    elif command[0] == 'help':
        helpManager()

    else:  # If the command wasnt understood
        speakResponse = "Sorry I didnt quite understand that"
    speechResponse(speakResponse)


class PersonalInformaion:
    name = ""
    wake_phrases = []

    def __init__(self):  # Sets up the configuration files
        try:
            with open('config_data.json', 'r') as jsonFile:
                data = json.load(jsonFile)
                self.name = data['name']
                self.wake_phrases = data['wake_phrases']
        except:
            self.setName(True)
            self.initaliseAssistantName()
            self.saveJson()
        global wakeWords
        wakeWords = self.wake_phrases
        response = "I am " + self.wake_phrases[0] + ", welcome " + self.name
        speechResponse(response)

    def setName(self, init=False):
        acceptedName = False
        speechResponse("What shall I call you?")
        while not acceptedName:
            self.name = listenToAudio()
            speechResponse("Do you want me to call you " + self.name)
            if not validateYesorNo():
                speechResponse("Sorry I must have misheard you")
                self.name = ""
            else:
                speechResponse("Okay, I'll call you " + self.name + " from now on")
                acceptedName = True
        if not init:
            self.saveJson()

    def initaliseAssistantName(self):
        keepLoop = True
        speechResponse("By default I am called Omega, do you wish to change this?")
        while keepLoop:
            acceptedYesNo = validateYesorNo()
            if acceptedYesNo:  # Start process to set custom name
                self.setAssistantName()
                keepLoop = False
            else:
                self.wake_phrases.append('omega')
                self.wake_phrases.append('ok omega')
                keepLoop = False

    def saveJson(self):
        try:
            data = {'name': self.name, 'wake_phrases': self.wake_phrases}
            with open('config_data.json', 'w') as jsonFile:
                json.dump(data, jsonFile)
        except:
            speechResponse("Sorry an error happened saving json file")

    def setAssistantName(self):
        nameAccepted = False
        while not nameAccepted:
            speechResponse("Please say which name you would like to address me as")
            response = listenToAudio()
            speechResponse("Do you want to call me " + response + "?")
            if validateYesorNo():  # Sets custom wake phrases
                self.wake_phrases.append(response)
                self.wake_phrases.append('ok ' + response)
                speechResponse(
                    "You can now activate me by using " + self.wake_phrases[0] + " and " + self.wake_phrases[1])
                global wakeWords
                wakeWords = self.wake_phrases
                nameAccepted = True
                self.saveJson()
            else:
                speechResponse("I must have misheard you")

    def getName(self):
        return self.name


def main():
    global personalInfo
    personalInfo = PersonalInformaion()

    while (True):
        data = listenToAudio()
        response = ''
        command = wakeCommand(data)
        print(command)
        if (command != ""):  # We know there has been a command given
            manageCommandOption(command)


if __name__ == "__main__":
    main()
