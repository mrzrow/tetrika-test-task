import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from string import ascii_uppercase

result = defaultdict(int)
base_url = 'https://ru.wikipedia.org'
url = f'{base_url}/wiki/Категория:Животные_по_алфавиту'

run = True
while run:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # div с сылками и таблицей
    pages = (
        soup.find('div', id='mw-content-text', class_='mw-body-content')
        .find('div', id='mw-pages')
    )

    # ссылка на следующую страницу
    next_page = pages.find_all('a')[-1]['href']

    # div'ы с таблицей и ее заголовком
    groups = (
        pages.find_all('div', class_='mw-category mw-category-columns')[-1]
        .find_all('div', class_='mw-category-group')
    )
    # так как на одной странице может быть несколько таблиц, идем по всем 
    for group in groups:
        letter = group.find('h3').text
        # если начались латинские буквы, то останавливаемся
        if letter in ascii_uppercase:
            run = False
            break
        rows = group.find_all('li')
        result[letter] += len(rows)

    # формируем url следующей страницы 
    url = f'{base_url}{next_page}'

with open('beasts.csv', 'w') as file:
    for k, v in result.items():
        file.write(f'{k},{v}\n')
