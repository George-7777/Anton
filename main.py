import wikipedia
import os
import time
import requests
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser as wb
import pymorphy2
import random
wikipedia.set_lang("ru")
morph = pymorphy2.MorphAnalyzer()
setting = 0
city = "Ижевск"
muz = ["1.mp3", "2.mp3", "3.mp3"]
ball = ["да", "нет", "не знаю", "спроси позже", "скорее всего", "врятли"]
scazki = ["colobok.mp3", "gusi.mp3", "lyagushka.mp3", "masha.mp3", "medvedi.mp3", "repka.mp3", "terem.mp3"]

opts = {
    "alias": ('антон', 'антошка', 'антончик', 'антоша', 'антун', 'антоний', 'тоня'),
    # "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси', 'что ты', 'что'), принят отказ в Антон V 0.4
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "stupid1": ('расскажи анектод', 'рассмеши меня', 'ты знаешь анектоды'),
        "google": ('найди', "нагугли"),
        "pogoda": ('какая погода в', 'какая погодка в', 'сколько градусов в'),
        "what": ('что такое', 'что значит'),
        "list": ('что ты можешь', 'что ты умеешь'),
        "scazki": ('расскажи сказку', 'включи сказку', 'хочу сказку'),
        "youtube": ('включи ютуб', 'открой ютуб'),
        "gog": ('включи гугл', 'открой гугл', 'включи google', 'открой google'),
        "ya": ('включи яндекс', 'открой яндекс'),
        "uchi": ('включи учи ру', 'открой учи ру', 'включи uchi.ru', 'открой uchi.ru', 'uchi.ru'),
        "figna": ('включи skysmart', 'открой skysmart', 'включи скайсмарт', 'открой скайсмарт'),
        "magic": ('магический шар', 'шар', 'магический шар скажи', 'шар скажи', 'шарик', 'шарик скажи')
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognize, audio):
    print("работаем-работаем")
    try:
        voice = recognize.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]) or setting == 0:  # if voice.startswith(opts["alias"] or setting == 0):

            # обращаются к Антону
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            #for x in opts['tbr']:
                #cmd = cmd.replace(x, "").strip() принят отказ в Антон V0.4
            global sapros

            sapros = cmd
            for x in opts['cmds']:
                sapros = sapros.replace(x, "").strip()
            # распознаем и выполняем команду



            cmd = recognize_cmd(cmd)

            execute_cmd(cmd['cmd'])
    except sr.RequestError:
        print("[log] Неизвестная ошибка, проверьте интернет!")
    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except Exception as e:
        print(e)



def recognize_cmd(cmd):
    print(cmd)
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

    # gcmd = gcmd[1:]
    print(gcmd)
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        # музончик)
        os.system(random.choice(muz))
        # os.system("C:\\Users\\User\\PycharmProjects\\Anton\\res\\mus.mp3")

    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

    elif cmd == 'google':
        wb.open("https://www.google.com/search?q=" + " ".join(gcmd))
    elif cmd == 'pogoda':

        city = gcmd[-1]
        city = morph.parse(city)[0].normal_form
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
        weather_data = requests.get(url).json()
        # получаем данные о температуре и о том, как она ощущается
        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])
        # выводим значения на экран
        a = 'Сейчас в городе', city, str(temperature), 'градусов по цельсию'
        b = 'Ощущается как', str(temperature_feels), 'градусов по цельсию'
        b = a, ', ', b
        speak(b)
    elif cmd == 'list':
        speak('''
        Я могу:
        Сказать который час,
        рассказать анектод,
        включить музыку,
        рассказать сказку,
        поиграть в магический шар,
        сказать какая погода в вашем городе,
        и ответить на ваш вопрос!
        ''')
    elif cmd == 'what':
        speak(wikipedia.summary(" ".join(gcmd[1:]), sentences=3))
    elif cmd == 'scazki':

        os.system(f"сказки\\{random.choice(scazki)}")
    elif cmd == 'youtube':
        wb.open("https://www.youtube.com/")
    elif cmd == 'gog':
        wb.open("https://www.google.ru/")
    elif cmd == 'figna':
        wb.open("https://skysmart.ru/")
    elif cmd == 'ya':
        wb.open("https://ya.ru/")
    elif cmd == 'uchi':
        wb.open("https://uchi.ru/")
    elif cmd == 'magic':
        speak(random.choice(ball))
    else:
        speak("Команда не распознана")

# запуск

r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# forced cmd test
# speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")

speak("Приветствую, я Антон")
speak("Чем я могу помочь?")
stop_listening = r.listen_in_background(m, callback)

#aud = r.listen(m)
#callback(aud)

while True: time.sleep(0.1)  # infinity loop
