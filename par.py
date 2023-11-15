# импортируем модули
from bs4 import BeautifulSoup
import requests
import random
requests.max_redirects = 77
def parsglav():
   st_accept = "text/html"  # говорим веб-серверу,
   # что хотим получить html
   # имитируем подключение через браузер Mozilla на macOS
   st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
   # формируем хеш заголовков
   headers = {
      "Accept": st_accept,
      "User-Agent": st_useragent
   }
   url = 'https://povar.ru/recipes/'
   response = requests.get(url)
   bs = BeautifulSoup(response.text,"lxml")
   temp = bs.find_all('a', href=True)
   url = 'https://povar.ru/' + temp[random.randint(0, 99)]['href']
   response = requests.get(url)
   bs = BeautifulSoup(response.text,"lxml")
   temp = bs.find('span', 'duration')


   return temp.text
def ppp():
   st_accept = "text/html"  # говорим веб-серверу,
   # что хотим получить html
   # имитируем подключение через браузер Mozilla на macOS
   st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
   # формируем хеш заголовков
   headers = {
      "Accept": st_accept,
      "User-Agent": st_useragent
   }
   url = 'https://povar.ru/recipes/'
   response = requests.get(url)
   bs = BeautifulSoup(response.text, "lxml")
   temp = bs.find_all('a', href=True)
   url = 'https://povar.ru/' + temp[random.randint(0, 99)]['href']
   response = requests.get(url)
   bs = BeautifulSoup(response.text, "lxml")
   tempp = bs.find('h1', 'detailed fn')
   return tempp.text
def parsvtor():
   st_accept = "text/html"  # говорим веб-серверу,
   # что хотим получить html
   # имитируем подключение через браузер Mozilla на macOS
   st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
   # формируем хеш заголовков
   headers = {
      "Accept": st_accept,
      "User-Agent": st_useragent
   }
   url = 'https://povar.ru/recipes/'
   response = requests.get(url)
   bs = BeautifulSoup(response.text, "lxml")
   temp = bs.find_all('a', href=True)
   url = 'https://povar.ru/' + temp[random.randint(0, 99)]['href']
   response = requests.get(url)
   bs = BeautifulSoup(response.text, "lxml")
   temp = bs.find_all('span', 'name')
   temp2 = bs.find_all('span', 'value')
   temp3 = bs.find_all('span', 'u-unit-name')
   for i, j, g in zip(temp, temp2, temp3):
      print(f"{i.text} {j.text} {g.text}")
   return zip(temp, temp2, temp3)
def parsstep():
   st_accept = "text/html"  # говорим веб-серверу,
   # что хотим получить html
   # имитируем подключение через браузер Mozilla на macOS
   st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
   # формируем хеш заголовков
   headers = {
      "Accept": st_accept,
      "User-Agent": st_useragent
   }
   url = 'https://povar.ru/recipes/'
   response = requests.get(url)
   bs = BeautifulSoup(response.text, "lxml")
   temp = bs.find_all('a', href=True)
   url = 'https://povar.ru/' + temp[random.randint(0, 99)]['href']
   response = requests.get(url)
   bs = BeautifulSoup(response.text, "lxml")
   temp4 = bs.find_all('div', 'detailed_step_description_big')
   return temp4