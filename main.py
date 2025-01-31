import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from pygame import mixer
from io import BytesIO
import os
import openai

# configure openai
openai.api_key = 'user api key'

messages_array = [
    {'role':'system','content':'You are my voice assistant named Aadhi'}
]

# capture voice
def listen():
    read = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening......')
        read.pause_threshold = 1
        audio = read.listen(source)
    try:
        print('Recognizing.....')
        query = read.recognize_google(audio,language ='en-in')
        print(f'user has said {query} ')
        messages_array.append({'role':'user','content':query})
        respond(audio)

    except Exception as e:
        print('Say that again please..',e)


 # respond to the new conversation item
def respond(audio):
    print('Responding....')
    res = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = messages_array
    )
    res_message = res.choices[0].message
    messages_array.append(res_message)

    speak(res_message.content)

# speak out the audio response   
def speak(text):
    speech = gTTS(text=text,lang='en',slow=False)
    speech.save('captured_voice.mp3')
    playsound('captured_voice.mp3')

    os.remove('captured_voice.mp3')
    listen()

query = listen()


     

