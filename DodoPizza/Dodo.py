#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

from dodo_old import Scraping_information 
# Базовый URL сайта, который содержит список городов
DODO_URL = "https://dodopizza.ru/"

# Посылаем запрос на получение html контента старницы
dodo_html_content = str(requests.get(DODO_URL).content, 'utf-8')

# Парсинг полученных данных
soup = BeautifulSoup(dodo_html_content, 'html.parser')

# Находим скрипт, который содержит переменную window.initialState
# В этой переменной содержится полный список городов с URL
data = soup.find_all('script')[1]
#print(data)
#data = BeautifulSoup(data, 'html.parser')
#print(data.get_text())
#for child in data.children:
#    print(child)
#print(data)
# Извлекаем текст из скрипта
extract_text_from_script = data
#extract_text_from_script = data.get_text()
#extract = data.getAttribute('innerText')
#print(extract_text_from_script)

# Быстрое удаление ненужных объйвлений переменных чтобы остался только JSON контент
# Более правильный вариант делать это с помощью регулярных выражений
result_json = str(data).replace("window.initialState = ", "").replace(';window.settings = {"clientAnalyticsHost":"https://eventstream.dodopizza.com/"};', "").replace("<script>", "").replace("</script>", "")

# Преобразуем полученный текст в в питоновский словарь для дальнейшей работы
convert_text_to_json = json.loads(result_json)

# Извлекаем из JSON по ключу список городов
#  Создаем датафрейм и сохраняем в CSV
df = pd.DataFrame(
    data = convert_text_to_json['corePageData']['localities'], 
    columns= [
        'id', 
        'name', 
        'translitAlias', 
        'url', 
        'deliveryZoneMapUrl', 
        'timeZoneOffsetInSeconds', 
        'menuSpecializationType'
    ])

df.to_csv('dod_cities.csv', index=None)

#Создаем экземпляр класса для поиска и список адресов
data = Scraping_information()
results_addresses = []
#results_addresses.append('address')
i=1
#Извлекаем из всех городов адреса. Проходим по городам
for cities in df['url']:
    if(i>5):
        break
    #Создаем ссылку для конкретного города
    DODO_URL_city = DODO_URL + str(cities) + '/contacts'
    #Подготовка к работе со страницей города
    data.data_about_site(DODO_URL_city, 'contacts-pizzerias__item_address')
    #Получаем страницу города
    data.get_page()
    #Парсим со страницы города адреса
    data.get_data()
    city = str(data.city).replace('<a class="header__about-slogan-text header__about-slogan-text_locality header__about-slogan-text_link" data-testid="header__about-slogan-text_link" href="#">', "").replace('</a>','').replace('[',"").replace(']',"")
    for address in data.search_data:
        results_addresses.append(str(city)+', '+str(address).replace('<span class="contacts-pizzerias__item contacts-pizzerias__item_address">', "").replace('</span>', ""))
    i+=1
#Записываем результаты в файл
result = pd.DataFrame(
    data = results_addresses, 
    columns= [ 
        'address'
    ])
result.to_csv('data.csv', index=None, encoding = 'windows-1251')

















