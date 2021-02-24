from bs4 import BeautifulSoup
import requests
import pandas as pd
from matplotlib import pyplot as plt

# 맨 뒤 페이지 숫자구하기
url_ = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
url = requests.get(url_, headers={'User-Agent': 'Mozilla/5.0'}).text
html = BeautifulSoup(url, 'lxml')
pgrr = html.find('td', class_='pgRR')
s = str(pgrr.a['href']).split('=')
last_page = s[-1]

# 전체페이지 읽어오기
df = pd.DataFrame()
sise_url_ = 'https://finance.naver.com/item/sise_day.nhn?code=068270'
sise_url = requests.get(sise_url_, headers={'User-Agent': 'Mozilla/5.0'}).text

for page in range(1, int(last_page)+1):
    page_url = '{}&page={}'.format(sise_url, page)
    df = df.append(pd.read_html(page_url, header=0)[0])

# 차트출력을 위해 데이터프레임 가공하기
df = df.dropna()
df = df.iloc[0:30]
df = df.sort_values(by='날짜')

# 날짜, 종가 칼럼으로 차트 그리기
plt.title('Celltrion (close)')
plt.xticks(rotation=45)
plt.plot(df['날짜'], df['종가'], 'co-')
plt.grid(color='gray', linestyle='--')
plt.show()