#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import re

from riv_model import Scraping_information 
# Базовый URL сайта, который содержит список городов
RIV_URL = "http://www.rivegauche.ru/shops/"

# Посылаем запрос на получение html контента старницы
riv_html_content = str(requests.get(RIV_URL).content, 'utf-8')

# Парсинг полученных данных
soup = BeautifulSoup(riv_html_content, 'html.parser')

# Находим скрипт, который содержит переменную window.initialState
# В этой переменной содержится полный список городов с URL
data = soup.find_all('table')[1].find_all('a')


# Извлекаем текст из скрипта
extract_text_from_script = data


# Быстрое удаление ненужных объйвлений переменных чтобы остался только JSON контент
# Более правильный вариант делать это с помощью регулярных выражений
result_json = '[' + str(data).replace('[',"").replace(']',"").replace('<a href="mailto:development@rivegauche.ru"><img alt="Арендуем торговые площади!" height="204" src="http://www.rivegauche.ru/sites/default/files/shops/rent.png" title="Арендуем торговые площади!" width="249"/></a>, <a href="shops/shops-on-line/">Shop-online</a>, ', "").replace('">', '", "name":"').replace('</a>', '"}').replace('<a href="/shops/cities/', '{"url":"') + ']'

# Преобразуем полученный текст в в питоновский словарь для дальнейшей работы
convert_text_to_json = json.loads(result_json)

# Извлекаем из JSON по ключу список городов
#  Создаем датафрейм и сохраняем в CSV
df = pd.DataFrame(
    data = convert_text_to_json,
    columns = [
        'url', 
        'name'
    ])

df.to_csv('riv_cities.csv', index=None)

#Создаем экземпляр класса для поиска и список адресов
data = Scraping_information()
results_addresses = []
#results_addresses.append('address')
pattern = re.compile('/span>\n.+<br/>')
i = 0
#Извлекаем из всех городов адреса. Проходим по городам
for cities in df['url']:

    #Создаем ссылку для конкретного города
    RIV_URL_city = RIV_URL + 'cities/' + str(cities)
    #Подготовка к работе со страницей города
    data.data_about_site(RIV_URL_city, 'padding')
    #Получаем страницу города
    data.get_page()
    #Парсим со страницы города адреса
    data.get_data()
	 #Склеиваем город и адрес и получаем полный адрес
    city = df['name'][i]
    i+=1
    result = pattern.findall(str(data.search_data))
    for address in result:
    	results_addresses.append(str(city) + ', ' + str(address).replace("/span>", "").replace("\n", "").replace("<br/>", "").replace("             ", ""))

#Записываем результаты в файл
result = pd.DataFrame(
    data = results_addresses, 
    columns= [ 
        'address'
    ])
result.to_csv('data.csv', index=None, encoding = 'windows-1251')

