from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import  time
import csv
import itertools
import datetime
from dateutil.relativedelta import relativedelta

def size_of_month(current_date):
    first_day_of_month = datetime.datetime(current_date.year, current_date.month, 1)

    # Get the first day of the next month
    if current_date.month == 12:
        next_month_first_day = datetime.datetime(current_date.year + 1, 1, 1)
    else:
        next_month_first_day = datetime.datetime(current_date.year, current_date.month + 1, 1)

    # Calculate the size of the current month
    return (next_month_first_day - first_day_of_month).days
def list_stripper(data):
    return list(word for sublist in data for word in sublist.split())


start_date = datetime.datetime(2000, 1, 1) # YYYY, MM, DD
end_date = datetime.datetime(2024, 6, 19)  # YYYY, MM, DD

f = open("Weatherdata.csv", "a", newline='')
writer = csv.writer(f)

# Iterate over months
current_date = start_date
while current_date <= end_date:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options)
    l=[]
    while not l:
        l = []
        URL = "https://www.wunderground.com/history/monthly/in/new-delhi/VIDP/date/"
        URL += current_date.strftime("%Y-%m")
        driver.get(URL)
        time.sleep(10)
        html = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html,'lxml')
        count=0
        for i in soup.select('table.days.ng-star-inserted'): #note to self CSS allows spaces but html needs . in place of " "
                for j in i.select('tr.ng-star-inserted'):
                    if count!=0:
                        l.append(j.get_text())
                    else:
                        count = 1
    x=0
    l1=[]
    t=(len(l)+1)//7
    while x<len(l):
        l1.append(l[x:x+t-1]) # arithmetic to calculate amt of data
        x+=t

    # print(f"{l}\n{l1}") used to print ur data
    Date=list_stripper(l1[0])
    Temp=list_stripper(l1[1])
    Dew=list_stripper(l1[2])
    humidity=list_stripper(l1[3])
    Wind=list_stripper(l1[4])
    pressure=list_stripper(l1[5])
    precip=list_stripper(l1[6])

    Max_temp=Temp[0::3]
    Avg_temp=Temp[1::3]
    Min_temp=Temp[2::3]

    Max_Dew=Dew[0::3]
    Avg_Dew=Dew[1::3]
    Min_Dew=Dew[2::3]

    Max_humidity=humidity[0::3]
    Avg_humidity=humidity[1::3]
    Min_humidity=humidity[2::3]

    Max_wind=Wind[0::3]
    Avg_wind=Wind[1::3]
    Min_wind=Wind[2::3]

    Max_pressure=pressure[0::3]
    Avg_pressure=pressure[1::3]
    Min_pressure=pressure[2::3]

    for i in range(min(len(Date),len(Max_temp),len(Avg_temp),len(Min_temp),len(Max_Dew),len(Avg_Dew),len(Min_Dew),len(Max_humidity),len(Avg_humidity),len(Min_humidity),len(Max_wind),len(Avg_wind),len(Min_wind),len(Max_pressure),len(Avg_pressure),len(Min_pressure),len(precip))):
        writer.writerow([current_date.strftime("%Y%m")+str(Date[i]),Max_temp[i],Avg_temp[i],Min_temp[i],Max_Dew[i],Avg_Dew[i],Min_Dew[i],Max_humidity[i],Avg_humidity[i],Min_humidity[i],Max_wind[i],Avg_wind[i],Min_wind[i],Max_pressure[i],Avg_pressure[i],Min_pressure[i],precip[i]])
    current_date += relativedelta(months=1)
    print(f"{URL} is done.")  # if program crashes u know where to start from next.

f.close()