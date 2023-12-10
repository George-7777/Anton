import wikipedia
import os
import PySimpleGUI as sg
import time
from ai import responce
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import webbrowser as wb
from threading import Thread
import pymorphy2
import requests
import random
import winsound
import config
import par
wikipedia.set_lang("ru")
morph = pymorphy2.MorphAnalyzer()
setting = 0
city = "Ижевск"
muz = ["1.mp3", "2.mp3", "3.mp3"]
ball = ["да", "нет", "не знаю", "спроси позже", "скорее всего", "врятли"]
scazki = ["colobok.mp3", "gusi.mp3", "lyagushka.mp3", "masha.mp3", "medvedi.mp3", "repka.mp3", "terem.mp3"]
cmds = ""
opts = config.command()
boltun_mod = False

# функции

# запуск
def start():
    def speak(what):
        print(what)
        speak_engine.say(what)
        speak_engine.runAndWait()
        speak_engine.stop()
        text_elem = window['-text-']
        # выводим в него текст с новым числом
        text_elem.update("Результат: {}".format(what))
    def remind(local_time=1):

        local_time = local_time * 60
        # Ждём нужное количество секунд, программа в это время ничего не делает
        time.sleep(local_time)
        # Показываем текст напоминания
        speak("АААААААААААААААААААААААААААААААААААААААААААААААААА. ТАймер вышел из под контроля")

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

                # for x in opts['tbr']:
                # cmd = cmd.replace(x, "").strip() принят отказ в Антон V0.4
                global sapros
                global cmds
                cmds = cmd
                sapros = cmd
                for i in opts['cmds']:

                    for x in opts['cmds'][i]:
                        print(x)
                        sapros = sapros.replace(x, "").strip()
                # распознаем и выполняем команду

                cmd = recognize_cmd(cmd)

                execute_cmd(cmd['cmd'])
        except sr.RequestError:
            callback(r, r.listen(m, 5, 5))
            print("[log] Неизвестная ошибка, проверьте интернет!")
        except sr.UnknownValueError:

            callback(r, r.listen(m, 5, 5))
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
        global boltun_mod
        global cmds
        # gcmd = gcmd[1:]
        print(gcmd)
        if boltun_mod:
            texx = responce(cmds)
            speak(texx)
        else:
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

                city = gcmd[0]
                city = morph.parse(city)[0].normal_form
                url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
                weather_data = requests.get(url).json()

                # получаем данные о температуре и о том, как она ощущается
                temperature = round(weather_data['main']['temp'])
                temperature_feels = round(weather_data['main']['feels_like'])
                # выводим значения на экран
                a = 'Сейчас в городе' + city + str(temperature) + 'градусов по цельсию'
                b = 'Ощущается как' + str(temperature_feels) + 'градусов по цельсию'
                b = a + ', ' + b

                speak(b.replace("-", " минус"))
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
            elif cmd == 'listt':
                speak('''
                Также я могу:
                Включить ваш любимый (или не очень) сайт.
                поиграть в магический шар,
                запомнить ваше имя,
                посчитать на калькуляторе,
                подбросить монету,
                и поставить таймер
                ''')
            elif cmd == 'what':
                speak(wikipedia.summary(" ".join(gcmd), sentences=2))
            elif cmd == 'rad':
                wb.open("http://europaplus.hostingradio.ru:8014/ep-top256.mp3")
                #playsound("http://europaplus.hostingradio.ru:8014/ep-top256.mp3")
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
                speak("Магический шар вас слушает")
                winsound.PlaySound("mag.mp3", winsound.SND_ALIAS)
                time.sleep(3)
                speak(f"Звёзды говорят {random.choice(ball)}")
            elif cmd == 'name':
                speak(f"Приятно познакомится {gcmd}!")
                f = open("name.txt", "w", encoding="utf-8")
                f.write(str(gcmd[0]))
                f.close()
            elif cmd == 'calc':
                # for i in cal:
                # sapros = sapros.replace(i, cal[i]).strip()
                gcmd = " ".join(gcmd)
                gcmd = gcmd.replace("х", "*").strip()
                gcmd = gcmd.replace("в степени", "**").strip()
                print(gcmd)
                speak(str(int(eval(gcmd))))
            elif cmd == 'mon':
                speak(random.choice(['орёл', 'решка']))
            elif cmd == 'timer':

                local_time = int(gcmd[0])
                # Создаём новый поток
                th = Thread(target=remind, args=())
                # И запускаем его
                th.start()
            elif cmd == "recepts":
                st_accept = "text/html"  # говорим веб-серверу,
                # что хотим получить html
                # имитируем подключение через браузер Mozilla на macOS
                st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
                # формируем хеш заголовков
                headers = {
                    "Accept": st_accept,
                    "User-Agent": st_useragent
                }
                speak("Могу посоветовать")
                speak(par.ppp())
                speak("Время готовки")
                speak(par.parsglav())
                speak("Ингредиенты")
                for i, j, g in par.parsvtor():
                    speak(f"{i.text} {j.text} {g.text}")
                speak("Шаги приготовления")
                for i in par.parsstep():
                    speak(i.text)
            elif cmd == 'boltun':
                boltun_mod = True
                f = random.randint(0, 2)
                if f == 0:
                    speak("Хорошо. Я люблю поговорить с хорошим человеком")
                elif f == 1:
                    speak("Хорошо")
                elif f == 2:
                    speak("Давай. О чём поговорим")
            elif cmd == "zadolbal":
                speak("ОК")
                boltun_mod = False
            else:
                speak("Команда не распознана. Если вы хотели поболтать, скажите давай поговорим")
        print("hello")
        callback(r, r.listen(m, 5, 5))
    r = sr.Recognizer()
    m = sr.Microphone(device_index=1)

    with m as source:
        r.adjust_for_ambient_noise(source)

    speak_engine = pyttsx3.init()

    # forced cmd test
    # speak("Мой разработчик не научил меня анекдотам ... Ха ха ха")
    f = open("name.txt", "r", encoding='utf-8')
    if os.stat("name.txt").st_size > 0:
        name = f.readline()
        print(f)
        speak(f"Приветствую {name}")
        speak("Чем я могу помочь?")
    else:
        speak("Приветствую, я Антон")
        speak("Чем я могу помочь?")
    f.close()
    #r.listen_in_background(m, callback)
    with m:
        callback(r, r.listen(m, 5, 5))
    #aud = r.listen(m)
    #callback(aud)
def update():
    # получаем новое случайное число
    r = random.randint(1,100)
    # получаем доступ к текстовому элементу


# что будет внутри окна
# первым описываем кнопку и сразу указываем размер шрифта
layout = [[sg.Text('', size=(25, 5), key='-text-', font='Helvetica 10')],
    [sg.Button('Спросить',enable_events=True, key='-FUNCTION-', font='Helvetica 32')]
        # затем делаем текст
        ]

# рисуем окно
window = sg.Window('Антон alpha v.1', layout, size=(500,700))

# запускаем основной бесконечный цикл
while True:
    # получаем события, произошедшие в окне
    event, values = window.read()
    # если нажали на крестик
    if event in (sg.WIN_CLOSED, 'Exit'):
        # выходим из цикла
        break
    # если нажали на кнопку
    if event == '-FUNCTION-':
        # запускаем связанную функцию
        start()

# закрываем окно и освобождаем используемые ресурсы
window.close()


