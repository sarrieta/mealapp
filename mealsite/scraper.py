from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from models import*
import String



    source = requests.get("https://www.opentable.com/r/kilikya-mile-end-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=5f970422-07b4-47e0-823b-bcd5829a7555&p=2&sd=2019-01-20%2019%3A00")
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
            price=price.translate({ord('£'): None})
            price=float(price)
        except:
            price=0.00



        menu = Menu_Items.objects.create("""type=type,"""item_name=name,item_price=price,item_description=desc,restaurant_name="Kilikya Mile End")
        menu.save()

    data = Restaurant.objects.only('name','opening','lat','long')
    data = serializers.serialize('json', data)
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
