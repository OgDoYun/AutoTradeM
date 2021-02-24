import pandas as pd
from urllib.request import urlopen
import requests
url = "https://finance.naver.com/item/sise_day.nhn?code=000020&page=1"
req = requests.get(url, headers={'User-Agent' : 'Mozilla/5.0'}).text
df = pd.DataFrame()
df = df.append(pd.read_html(req, header=0)[0])
print('df', df)