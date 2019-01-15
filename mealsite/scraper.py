from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from models import Menu

source = requests.get("https://www.opentable.com/r/the-widows-son-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=07f1e62d-8b95-4d05-9397-8f8d3df73291&p=2&sd=2019-01-11+19%3A00")
soup = BeautifulSoup(source.text, 'lxml')
menu_items = soup.find('div', class_="menu-items__2DRnPKGV")
"""type_items = soup.find('div', class_="menu-section-header__3nfLpHEA")"""

for menu_items in soup.find_all('div', class_="menu-item__2ZxJOnTY"):
    """type = type_items.findChildren()[0].text"""
    price = menu_items.findChildren()[0].text
    name = menu_items.findChildren()[1].text
    try:
        desc = menu_items.findChildren()[2].text
    except:
        desc =" "
    try:
        price=float(price)
    except:
        price=0.00

    menu = Menu.objects.create("""type=type,"""item_name=name,item_price=price,item_description=desc,restaurant_name="The Widow's Son")
    menu.save()
