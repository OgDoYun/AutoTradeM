import pymysql

connection = pymysql.connect(host='127.0.0.1', port=3306, db='dyson', user='root', passwd='thread8820!!', autocommit=True)
cursor = connection.cursor()
cursor.execute("SELECT VERSION();")
result = cursor.fetchone()

print("MariaDB version : {}".format(result))

connection.close()