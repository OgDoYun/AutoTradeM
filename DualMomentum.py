import pandas as pd
import pymysql
from datetime import datetime
from datetime import timedelta
from dyson import Analyzer

class DualMomentum:
    def __init__(self):
        """생성자: KRX 종목코드(codes)를 구히기 위한 MarketDB 객체 생성"""
        self.mk = Analyzer.MarketDB()

    def get_rltv_momentum(self, start_date, end_date, stock_count):
        """
        특정 기간 동안 수익률이 제일 높았던 stock_count 개의 종목들 (상대 모멘텀)
            - start_date : 상대 모멘텀을 구할 시작일자 ('2020-01-01')
            - end_date : 상대 모멘텀을 구할 종료일자 ('2020-12-31')
            - stock_count : 상대 모멘텀을 구할 종목수
        """
        connection = pymysql.connect(host='localhost', user='root', password='thread8820!!', db='dyson', charset='utf8')
        cursor = connection.cursor()

        sql = f"select max(date) from daily_price where date <= '{start_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if (result[0] is None):
            print("start_date : {} -> returned None".format(sql))
            return
        start_date = result[0].strftime('%Y-%m-%d')

        sql = f"select max(date) from daily_price where date <= '{end_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if (result[0] is None):
            print("end_date : {} -> returned None".format(sql))
            return
        end_date = result[0].strftime('%Y-%m-%d')

        rows = []
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']
        for _, code in enumerate(self.mk.codes):
            sql = f"select close from daily_price "\
                f"where code='{code}' and date='{start_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if (result is None):
                continue
            old_price = int(result[0])
            sql = f"select close from daily_price "\
                f"where code='{code}' and date='{end_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if (result is None):
                continue
            new_price = int(result[0])
            returns = (new_price / old_price - 1) * 100
            rows.append([code, self.mk.codes[code], old_price, new_price, returns])

        df = pd.DataFrame(rows, columns=columns)
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)
        df = df.head(stock_count)
        df.index = pd.Index(range(stock_count))

        connection.close()
        print(df)
        print(f"\nRelative momentum ({start_date} ~ {end_date}) : "\
            f"{df['returns'].mean():.2f}% \n")
        return df

    def get_abs_momentum(self, rltv_momentum, start_date, end_date):
        """
        특정 기간 동안 상대 모멘텀에 투자했을 때의 수익률(절대 모멘텀)
            - rltv_momentum : get_rltv_momentum() 함수의 리턴값 (상대 모멘텀)
            - start_date : 절대 모멘텀을 구할 시작일자 ('2020-01-01')
            - end_date : 절대 모멘텀을 구할 종료일자 ('2020-12-31')
        """
        stockList = list(rltv_momentum['code'])

        connection = pymysql.connect(host='localhost', user='root', password='thread8820!!', db='dyson', charset='utf8')
        cursor = connection.cursor()

        sql = f"select max(date) from daily_price where date <= '{start_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if (result[0] is None):
            print("start_date : {} -> returned None".format(sql))
            return
        start_date = result[0].strftime('%Y-%m-%d')

        sql = f"select max(date) from daily_price where date <= '{end_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if (result[0] is None):
            print("end_date : {} -> returned None".format(sql))
            return
        end_date = result[0].strftime('%Y-%m-%d')

        rows = []
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']
        for _, code in enumerate(stockList):
            sql = f"select close from daily_price "\
                f"where code='{code}' and date='{start_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if (result is None):
                continue
            old_price = int(result[0])

            sql = f"select close from daily_price "\
                f"where code='{code}' and date='{end_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if (result is None):
                continue
            new_price = int(result[0])

            returns = (new_price / old_price - 1) * 100
            rows.append([code, self.mk.codes[code], old_price, new_price, returns])

        df = pd.DataFrame(rows, columns=columns)
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)

        connection.close()
        print(df)
        print(f"\nAbsolute momentum ({start_date} ~ {end_date}) : "\
            f"{df['returns'].mean():.2f}%")
        return




