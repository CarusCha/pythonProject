#-*- coding:utf-8 -*-
from .lib import naverCrawling as nc
from .db import dbManager as db


def getStockList(marketType):
    stockDictList = []
    url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=" + marketType
    page = 1

    while True:
        print(page)
        pageUrl = url + "&page=" + str(page)
        tdList = nc.getHtmlObj(pageUrl).find_all("td")

        stockList = filter(lambda x: x.find("a", {"class": "tltle"}) != None, tdList)
        mappedList = list(map(lambda x: {"symbol":x.find("a").get('href').split("=")[-1], "name":x.text}, stockList))
        if len(mappedList) == 0:
            break
        stockDictList.extend(mappedList)


        page += 1

    return stockDictList



def saveStockList(marketType):
    con = db.getConnection("naverStockList.db")
    kospiList = getStockList(marketType)
    df = db.DataFrame(kospiList)
    df.to_sql(f'stock_{marketType}', con, if_exists='replace', chunksize=5000)
    test = db.pd.read_sql(f'SELECT * FROM stock_{marketType}', con, index_col='index')
    print(test)

def saveAllStockList():
    saveStockList(nc.kospi)
    saveStockList(nc.kosdaq)
