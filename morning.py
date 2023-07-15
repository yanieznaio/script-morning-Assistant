import datetime
import pandas as pd
import speech_recognition as sr
import wikipedia
import subprocess
import webbrowser
from gtts import gTTS
from gtts.tokenizer.pre_processors import abbreviations, end_of_line
from pygame import mixer
import time
from requests_html import HTMLSession
from mutagen.mp3 import MP3
import os
import datetime
import pywhatkit

now = datetime.datetime.now()
month_day_year = now.strftime("%m%d%y")

df = pd.read_csv(
    f'/home/ignite/Bureau/work/kimi/dist/headline-{month_day_year}.csv')
listener = sr.Recognizer()
wikipedia.set_lang("fr")


def mutagen_length(path):
    try:
        audio = MP3(path)
        length = audio.info.length
        return length
    except:
        return None


def gettemp():
    s = HTMLSession()

    query = 'avignon'
    url = f'https://www.google.com/search?q=temps+{query}'
    r = s.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})

    temp = r.html.find('span#wob_tm', first=True).text + " degré celsius"
    return temp


def textToSpeech(text):

    tts = gTTS(text, lang="fr", slow=False,
               pre_processor_funcs=[abbreviations, end_of_line])
    # Save the audio in a mp3 file
    tts.save('hello.mp3')
    # Play the audio
    mixer.init()
    mixer.music.load("hello.mp3")
    mixer.music.play()
    # Wait for the audio to be played
    length = mutagen_length('hello.mp3')
    time.sleep(length)


def take_command():

    with sr.Microphone() as source:
        print('écoute en cours...')
        listener.adjust_for_ambient_noise(source, duration=0.2)
        voice = listener.listen(source)
        print("je n'écoute plus")
    try:
        command = listener.recognize_google(voice, language="fr-FR")

    except:
        pass
    return command


def get_news():
    text = "J'ai trouvé des nouvelles actualité sur le site science-Avenir, dois-je vous les lires ?"
    textToSpeech(text)

    comand = take_command()
    if 'oui' in comand:
        for i in range(len(df)):
            title = df.values[i][1]
            link = df.values[i][2]

            ask = "Voullez vous consulter cette article ?"
            print(title + ". " + ask)
            textToSpeech(title + ". " + ask)

            response = take_command()
            if 'oui' in response:
                webbrowser.open_new(link)
                break
            elif 'stop' in response:
                break
            elif 'non' in response:
                textToSpeech("Très bien, article suivant. ")


def music():
    textToSpeech("Dois-je lancer votre playist du matin ?")

    response = take_command()
    if 'oui' in response:
        textToSpeech(
            "Ok, je lance youtube, passez une Bonne journée Juliette, et n'oubliez pas de sourire.")
        pywhatkit.playonyt("the score")
    elif 'non' in response:
        textToSpeech(
            "Ok, passez une Bonne journée Juliette, et n'oubliez pas de sourire.")


def good_morning():
    time = datetime.datetime.now().strftime('%H:%M')
    temperature = gettemp()
    textToSpeech(
        "Bonjour Juliette, Il est l'heure de vous réveiller, il est actuellement" + time)
    textToSpeech("La température extérieur à Avignon est de " + temperature)
    get_news()
    music()


good_morning()
