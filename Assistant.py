import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
import smtplib

engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak('Good Morning!')
    elif hour>=12 and hour<18:
        speak('Good Afternoon!')
    else:
        speak('Good Evening!')
    speak('I am Jarvis. How may I help you?')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=2) as source:
        """ dev = sr.Microphone.list_microphone_names()
        print(dev) """
        print('Listening...')
        r.energy_threshold = 650.44
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    text_file = open("pass.txt", "r")
    data = text_file.read()
    text_file.close()
    speak('Enter password of your email')
    pwd = input("Enter Password: ")
    if pwd == data:
        server.login('yuvrajsigh1402@gmail.com', data)
    server.sendmail('yuvrajsigh1402@gmail.com', to, content)
    server.close()

if __name__ == '__main__':
    wishMe()
    while True: #if 1 for listening one time
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)
            speak('According to Wikipedia')
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open('youtube.com')
        
        elif 'open google' in query:
            webbrowser.open('google.com')

        elif 'open stackoverflow' in query:
            webbrowser.open('stackoverflow.com')

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f'The time is {strTime}')
        
        elif 'play music' in query:
            lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

            spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
            results = spotify.artist_top_tracks(lz_uri)

            for track in results['tracks'][:10]:
                print('track    : ' + track['name'])
                print('audio    : ' + track['preview_url'])
                print('cover art: ' + track['album']['images'][0]['url'])
                print()
            """ scope = "user-library-read"

            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
            spicetify API invoke?

            results = sp.current_user_saved_tracks()
            for idx, item in enumerate(results['items']):
                track = item['track']
                print(idx, track['artists'][0]['name'], " – ", track['name']) """
        
        elif 'open code' in query:
            codePath = "C:\\Users\\Yuvraj Singh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        
        elif 'change voice' in query:
            engine.setProperty('voice', voice[1].id)
            
        elif 'emial to yuvraj' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "yuvrajyourEmail@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Email not sent")