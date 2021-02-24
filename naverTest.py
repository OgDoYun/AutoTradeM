from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

url = "http://finance.naver.com/item/sise_day.nhn?code=068270&page=1"
with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'})) as doc:
    html = BeautifulSoup(doc, 'lxml')
    pgrr = html.find("td", class_="pgRR")
    print(pgrr.a['href'])