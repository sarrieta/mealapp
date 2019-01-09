from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

source = requests.get("https://www.opentable.co.uk/r/kilikya-mile-end-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowLCJjIjowfQ&corrId=72060503-4840-4474-9f73-75b758ca45ac&p=2&sd=2019-01-09+19%3A00")
soup = BeautifulSoup(source.text, 'lxml')

div = soup.find('div', class_="menu-body")
print(div )
