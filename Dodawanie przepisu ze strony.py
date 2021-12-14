from bs4 import BeautifulSoup
from requests import get

URL = 'https://www.przepisy.pl/przepis/kotlety-mielone-z-pieczarkami-i-zoltym-serem'

page = get(URL)
bs =BeautifulSoup(page.content, 'html.parser')



for offer in bs.findAll('div', class_='ingredients-list-content-container ng-star-inserted'):

    ingredients = offer.find('div', class_='ingredients-list-content-item').find('span', class_='text-bg-white').get_text()
    quantity = offer.find('p', class_='quantity').get_text()


    print(ingredients, quantity)

for description in bs.findAll('div', class_='step ng-star-inserted'):
    print(description.get_text())



