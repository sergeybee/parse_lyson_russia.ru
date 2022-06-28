# https://docs.google.com/spreadsheets/d/1LIhDWTgBaLTSTrxBhywi4DN4zcdKT65naqcFaeYUjYs/edit#gid=0  - ПРИМЕР ТАБЛИЦЫ КАК ДОЛЖНО БЫТЬ
# https://www.fl.ru/projects/4906271/parsing-obyyavleniy.html?utm_source=exs&utm_medium=email&utm_campaign=freel_newsletter_с#/ - ССЫЛКА НА ТЗ

import requests
from bs4 import BeautifulSoup as BS
import csv
import time

CSV_FILE = "test.csv"

URL = 'https://lyson-russia.ru/product-category/uli/uli-iz-penopolistirola/10-ramok-dadan/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.2.615 Yowser/2.5 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


def get_html(url):
    """Получение html структуры страницы"""
    r = requests.get(url)
    return r.text


def get_product_links_current_category(html):
    """ Получает список ссылок на продукты в категории и возвращает его"""

    soup = BS(html, 'lxml')

    product_list = soup.find('ul', class_='products columns-4').find_all("li")

    links = []

    for product in product_list:
        links.append(
            product.find_next('a', class_='woocommerce-loop-product__link').get('href'))

    return links


def get_data_product(link_list):
    """ Парсит карточку товара и возвращает список данных"""
    data = []

    for link in link_list:
        html = get_html(link)

        soup = BS(html, 'lxml')

        data.append(
            {
                'title': soup.find('h1', class_="product_title").text.strip(),
                'price': soup.find('p', class_="price").find('span', class_='woocommerce-Price-amount').text.strip(),
                'made_in': soup.find('div', class_="madein").text.strip()
            }
        )

    return data


def write_to_csv(data):
    """ Запись данных в CSV файл"""

    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Цена', 'Производитель'])
        for item in data:
            writer.writerow([item['title'], item['price'], item['made_in']])


def main():
    html = get_html(URL)
    link_list = get_product_links_current_category(html)
    data = get_data_product(link_list)
    write_to_csv(data)
    print(link_list)


if __name__ == "__main__":
    main()
