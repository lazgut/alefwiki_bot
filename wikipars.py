import requests
from bs4 import BeautifulSoup as BS


def get_cities() -> dict:
    page = requests.get("https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B8%D0%B5_%D0%BD%D0%B0%D1%81%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B5_%D0%BF%D1%83%D0%BD%D0%BA%D1%82%D1%8B_%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B9_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D0%B8")
    soup = BS(page.text, 'lxml')

    list_city = {}
    for city in soup.find_all('tr')[1:75]:
        city_count = city.find_all('td')[4].get('data-sort-value')
        row_data = city.find_all('td')[1]
        row = {i.get('title'): [city_count, i.get('href')] for i in row_data}
        list_city.update(row)
    return list_city
