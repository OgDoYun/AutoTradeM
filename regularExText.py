import re

date = "2020 year 8/30"
lst = re.split('\D+', date)
year = int(lst[0])
month = int(lst[1])
day = int(lst[2])
date=f"{year:04d}-{month:02d}-{day:02d}"
print("date : ", date)