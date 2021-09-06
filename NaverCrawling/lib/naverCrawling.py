import requests
from bs4 import BeautifulSoup
import datetime
import time

kospi = "0"
kosdaq = "1"

def getHtmlObj(url):
    result = requests.get(url).content
    return BeautifulSoup(result, "html.parser")


def getTodayStr():
    today = datetime.datetime.today()
    overDay = today.weekday() - 4
    if overDay > 0:
        today += datetime.timedelta(days=-overDay)

    # return '20200504'
    return today.strftime("%Y%m%d")

