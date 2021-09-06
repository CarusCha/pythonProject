#-*- coding:utf-8 -*-
from selenium import webdriver
from .lib import naverCrawling as nc
from .db import dbManager as db
import os

path = os.path.dirname(os.path.realpath(__file__))

class NFStockOption:
    def __init__(self, name, id, isSelected):
        self.name = name
        self.id = id
        self.isSelected = isSelected


def getOptionList(soup):
    optionList = []
    tdList = soup.find("table",{"class":"item_list"}).find_all("td")
    tdList = filter(lambda x: x.find("input") != None, tdList)
    for td in tdList:
        name = td.text.replace(" ", "")
        id = td.find("input").get("id")
        isSelected = td.find("input").get("checked") != None
        optionList.append(NFStockOption(name, id, isSelected))

    return optionList



def getStockInfoList(marketType):
    stockDictList = []
    driver = webdriver.Chrome(path + '/chromedriver')
    driver.implicitly_wait(3)
    url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=" + marketType

    page = 1
    maxSelectionCount = 6
    basicOptionCount = 6
    maxPage = int(nc.getHtmlObj(url).find("td",{"class":"pgRR"}).find("a").get('href').split("=")[-1])

    while True:
        if page > maxPage:
            break

        print(page)
        pageUrl = url + "&page=" + str(page)

        driver.get(pageUrl)
        soup = nc.BeautifulSoup(driver.page_source, 'html.parser')
        optionList = getOptionList(soup)

        # Set Basic Option Values
        stockList = soup.find_all("tr", {"onmouseover": "mouseOver(this)"})
        for i, stock in enumerate(stockList):
            stockDict = {}
            tdList = stock.find_all("td")
            symbol = stock.find("a", {"class": "tltle"}).get('href').split("=")[-1]
            # stockDict["date"] = getTodayStr() # 날짜
            stockDict["marketType"] = marketType # 시장타입
            stockDict["symbol"] = symbol
            stockDict["name"] = tdList[1].text.replace("\n", "").replace("\t", "") # 종목명
            stockDict["price"] = tdList[2].text.replace("\n", "").replace("\t", "")  # 현재가
            stockDict["priceDifference"] = tdList[3].text.replace("\n", "").replace("\t", "")  # 전일비
            stockDict["fluctuationRate"] = tdList[4].text.replace("\n", "").replace("\t", "")  # 등락률
            stockDict["parValue"] = tdList[5].text.replace("\n", "").replace("\t", "")  # 액면가
            stockDictList.append(stockDict)
        # Set Selected Option Values
        while 1:
            soup = nc.BeautifulSoup(driver.page_source, 'html.parser')
            selectedOptionList = soup.find_all("td", {"class": "choice"})

            # 추가
            stockList = soup.find_all("tr", {"onmouseover": "mouseOver(this)"})
            for i, stock in enumerate(stockList):
                symbol = stock.find("a", {"class": "tltle"}).get('href').split("=")[-1]
                optionNameList = soup.find("thead").find_all("th")[basicOptionCount:-1]
                tdList = stock.find_all("td")[basicOptionCount:-1]
                for (name, option) in zip(optionNameList, tdList):
                    value = option.text.replace("\n", "").replace("\t", "")
                    try:
                        floatVal = float(value.replace(',', ''))
                        value = floatVal
                        
                        list(filter(lambda x: x["symbol"] == symbol, stockDictList))[0][name.text] = value
                    except:
                        pass





            notSelectedOptionList = list(filter(lambda x: x.isSelected != True, optionList))
            if len(notSelectedOptionList) == 0:
                break

            # 선택 해제
            for selectedOption in selectedOptionList:
                id = selectedOption.find("input").get("id")
                driver.find_element_by_id(id).click()

            # 선택
            for i, notAddedOption in enumerate(notSelectedOptionList):
                id = notAddedOption.id
                driver.find_element_by_id(id).click()
                notAddedOption.isSelected = True
                if i == maxSelectionCount - 1:
                    break

            driver.execute_script("javascript:fieldSubmit()")


        page += 1

    # print(stockDictList)
    driver.close()
    return stockDictList


import ast

def getStockInfoFromDB(symbol, date):
    con = db.getConnection("naverStockInfo.db")
    stockData = db.pd.read_sql('SELECT * FROM stockInfo', con, index_col='date').T.to_dict()
    stockDataList = db.json.loads(stockData[date]['infoJson'])
    info = list(filter(lambda x: x['symbol'] == symbol, stockDataList))[0]
    print(info)
    return info

def getStockInfoListFromDB(date):
    con = db.getConnection("naverStockInfo.db")
    stockData = db.pd.read_sql('SELECT * FROM stockInfo', con, index_col='date').T.to_dict()
    stockDataList = db.json.loads(stockData[date]['infoJson'])
    # print(stockDataList)
    return stockDataList


def saveStcokInfoList():
    con = db.getConnection("naverStockInfo.db")
    enableToAddTable = False
    try:
        if ((nc.getTodayStr() in db.pd.read_sql(f'SELECT * FROM stockInfo', con, index_col='date')[
            'infoJson'].keys()) == False):
            enableToAddTable = True

        else:
            print('Already exist')

    except:
        print('new')
        enableToAddTable = True


    if enableToAddTable:
        kospiStockList = getStockInfoList(nc.kospi)
        nc.time.sleep(3)
        kosdaqStockList = getStockInfoList(nc.kosdaq)
        stockList = kospiStockList + kosdaqStockList
        # stockList = kospiStockList
        dumpsStockList = db.json.dumps(stockList, ensure_ascii=False)

        newDict = {}
        newDict['infoJson'] = dumpsStockList
        df = db.DataFrame(newDict, index=[nc.getTodayStr()])
        df.to_sql(f'stockInfo', con, if_exists='append', index_label='date')
        test = db.pd.read_sql(f'SELECT * FROM stockInfo', con, index_col='date')
        print(test)


