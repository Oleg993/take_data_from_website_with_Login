import requests
from requests import Session
from bs4 import BeautifulSoup as bs
from time import sleep

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

work = Session()

work.get("https://quotes.toscrape.com/", headers=headers)

response = work.get("https://quotes.toscrape.com/login",  headers=headers)

soup = bs(response.text, 'lxml')
# забираем токен, так как он всегда разный (защита от ботов)
token = soup.find('form').find('input').get('value')
# создаем словарь с данными для входа
data_for_logIN = {"csrf_token": token, 'username': 'login', 'password': 'password'}
# запрос для регистрации с поддержкой перенаправления на главную страницу(allow...)
registr_page = work.post("https://quotes.toscrape.com/login", headers=headers, data=data_for_logIN, allow_redirects=True)

# запускаем бесконечный цикл, так как не знаем сколько страниц(прерываем когда нет кнопки вперед)
# на каждой странице проходим по каждой карточке с цитатой, собираем инфу
# возвращаем данные через yoeld, чтобы не копить все в списках, для ускорения работы
# после возврата данных перезапускаем цикл заново, пока есть кнопка вперет
def get_info():
    page = 1
    while True:
        url = f"https://quotes.toscrape.com/page/{page}/"
        resp = work.get(url, headers=headers).text
        page_soup = bs(resp, 'lxml')
        data = page_soup.findAll('div', class_='quote')
        sleep(3)
        for card in data:
            quote = card.find('span').text
            author = card.find('small').text
            link = card.findAll('span')[-1].findAll('a')[-1].get('href')
            yield author, quote, link

        if not page_soup.find('li', class_='next'):
            break
        page += 1

