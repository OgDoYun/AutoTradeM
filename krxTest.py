import requests
import pandas as pd


url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
req = requests.get(url, headers={'User-Agent' : 'Mozilla/5.0'}).text
krx = pd.read_html(req, header=0)[0]
krx = krx[['종목코드', '회사명']]
krx = krx.rename(columns={'종목코드':'code', '회사명':'company'})
krx.code = krx.code.map('{:06d}'.format)
print(krx)