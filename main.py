import os
import time
import requests
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser as wb
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
setting = 0
city = "Ижевск"

opts = {
    "alias": ('антон', 'антошка', 'антончик', 'антоша', 'антун', 'антоний', 'тоня'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "stupid1": ('расскажи анектод', 'рассмеши меня', 'ты знаешь анектоды'),
        "google": ('найди', "нагугли", "что такое"),
        "pogoda": ('какая погода в', 'какая погодка в', 'сколько градусов в'),

    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]) or setting == 0:   #if voice.startswith(opts["alias"] or setting == 0):

            # обращаются к Антону
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            global sapros

            sapros = cmd
            for x in opts['cmds']:
                sapros = sapros.replace(x, "").strip()
            # распознаем и выполняем команду

            cmd = cmd.split()
            if len(cmd) > 1:
                cmd = cmd[0]
            cmd = "".join(cmd)

            cmd = recognize_cmd(cmd)

            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):

    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    gcmd = sapros.split()

    #gcmd = gcmd[1:]
    print(gcmd)
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        #музончик)
        wb.open("https://music.youtube.com/search?q=" + " ".join(gcmd))
        #os.system("C:\\Users\\User\\PycharmProjects\\Anton\\res\\mus.mp3")

    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

    elif cmd == 'google':
        wb.open("https://www.google.com/search?q=" + " ".join(gcmd))
    elif cmd == 'pogoda':

        city = gcmd[-1]
        city = morph.parse(city)[0].normal_form
        url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
        weather_data = requests.get(url).json()
        # получаем данные о температуре и о том, как она ощущается
        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])
        # выводим значения на экран
        a = 'Сейчас в городе', city, str(temperature), 'градусов по цельсию'
        b = 'Ощущается как', str(temperature_feels), 'градусов по цельсию'
        b = a, ', ', b
        speak(b)

    else:
        speak("Команда не распознана")

# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()



# forced cmd test
#speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

speak("Приветствую, я Антон")
speak("Чем я могу помочь?")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop