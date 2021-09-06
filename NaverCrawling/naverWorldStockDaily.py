from .lib import naverCrawling as nc
from .db import dbManager as db
from selenium import webdriver
import os
import csv

path = os.path.dirname(os.path.realpath(__file__))

con = db.getConnection("naverWorldStockDaily.db")


china = 'SHS@000001'
dow = 'DJI@DJI'
nasdaq = 'NAS@IXIC'
snp = 'SPI@SPX'

def getWorldStockDaily(symbol):
    stockDictList = []
    url = 'https://finance.naver.com/world/sise.nhn?symbol=' + symbol

    driver = webdriver.Chrome(path + '/chromedriver')
    driver.implicitly_wait(3)
    driver.get(url)
    isFirstPage = True

    while True:
        soup = nc.BeautifulSoup(driver.page_source, 'html.parser')
        dayPaging = soup.find("div", {"class", "paging"})
        pagingList = dayPaging.find_all("a")

        for paging in pagingList:
            id = paging.get("id")
            className = paging.get("class")[0] if paging.get("class") != None else None
            if (id != None):
                if isFirstPage:
                    isFirstPage = False
                    stockDictList += generateStockDict(driver)

                    # pageSoup = nc.BeautifulSoup(driver.page_source, 'html.parser')
                    # dayTable = pageSoup.find("table", {"id": "dayTable"})
                    # trList = dayTable.find("tbody").find_all("tr")
                    # for tr in trList:
                    #     stockDict = {}
                    #     tdList = tr.find_all("td")
                    #     stockDict['date'] = tdList[0].text
                    #     stockDict['close'] = tdList[1].text
                    #     stockDict['rate'] = tdList[2].text
                    #     stockDict['open'] = tdList[3].text
                    #     stockDict['high'] = tdList[4].text
                    #     stockDict['low'] = tdList[5].text
                    #     stockDictList.append(stockDict)
                    #     print(stockDict)


                if className != "on":
                    driver.find_element_by_id(id).click()
                    nc.time.sleep(1)
                    stockDictList += generateStockDict(driver)

                    # pageSoup = nc.BeautifulSoup(driver.page_source, 'html.parser')
                    # dayTable = pageSoup.find("table", {"id": "dayTable"})
                    # trList = dayTable.find("tbody").find_all("tr")
                    # for tr in trList:
                    #     stockDict = {}
                    #     tdList = tr.find_all("td")
                    #     stockDict['date'] = tdList[0].text
                    #     stockDict['close'] = tdList[1].text
                    #     stockDict['rate'] = tdList[2].text
                    #     stockDict['open'] = tdList[3].text
                    #     stockDict['high'] = tdList[4].text
                    #     stockDict['low'] = tdList[5].text
                    #     stockDictList.append(stockDict)
                    #     print(stockDict)


            elif (className != None):
                if className == "next":
                    driver.find_element_by_class_name(className).click()
                    nc.time.sleep(1)
                    stockDictList += generateStockDict(driver)

                    # pageSoup = nc.BeautifulSoup(driver.page_source, 'html.parser')
                    # dayTable = pageSoup.find("table", {"id": "dayTable"})
                    # trList = dayTable.find("tbody").find_all("tr")
                    # for tr in trList:
                    #     stockDict = {}
                    #     tdList = tr.find_all("td")
                    #     stockDict['date'] = tdList[0].text
                    #     stockDict['close'] = tdList[1].text
                    #     stockDict['rate'] = tdList[2].text
                    #     stockDict['open'] = tdList[3].text
                    #     stockDict['high'] = tdList[4].text
                    #     stockDict['low'] = tdList[5].text
                    #     stockDictList.append(stockDict)
                    #     print(stockDict)



        if dayPaging.find("a", {"class","next"}) == None:
            break

    return stockDictList




def generateStockDict(googleDriver):
    stockDictList = []
    pageSoup = nc.BeautifulSoup(googleDriver.page_source, 'html.parser')
    dayTable = pageSoup.find("table", {"id": "dayTable"})
    trList = dayTable.find("tbody").find_all("tr")
    for tr in trList:
        stockDict = {}
        tdList = tr.find_all("td")
        stockDict['date'] = tdList[0].text.replace(".", "")
        stockDict['close'] = tdList[1].text
        trClass = tr.get("class")
        if trClass == None:
            stockDict['rate'] = tdList[2].text
        elif trClass[0] == "point_dn":
            stockDict['rate'] = f'-{tdList[2].text}'
        elif trClass[0] == "point_up":
            stockDict['rate'] = f'+{tdList[2].text}'


        stockDict['open'] = tdList[3].text
        stockDict['high'] = tdList[4].text
        stockDict['low'] = tdList[5].text
        stockDictList.append(stockDict)

    return stockDictList



    # soup = nc.getHtmlObj(url)
    # dayTable = soup.find("table",{"id":"dayTable"})
    # trList = dayTable.find("tbody").find_all("tr")
    # for tr in trList:
    #     stockDict = {}
    #     tdList = tr.find_all("td")
    #     stockDict['date'] = tdList[0].text
    #     stockDict['close'] = tdList[1].text
    #     stockDict['rate'] = tdList[2].text
    #     stockDict['open'] = tdList[3].text
    #     stockDict['high'] = tdList[4].text
    #     stockDict['low'] = tdList[5].text
    #     stockDictList.append(stockDict)
    #
    #
    # print(stockDictList)


    # dayPaging = soup.find("div",{"class","paging"})
    # pagingList = dayPaging.find_all("a")
    # for paging in pagingList:
    #     print(paging)
    #     id = paging.get("id")
    #     className = paging.get("class")




def saveStockWorldDaily(symbol):
    stockWorldDailyList = getWorldStockDaily(symbol)
    df = db.DataFrame(stockWorldDailyList)
    newSymbol = f'{symbol}'.split('@')[0]
    df.to_sql(f'stockWorldDaily_{newSymbol}', con, if_exists='replace', chunksize=5000)
    test = db.pd.read_sql(f'SELECT * FROM stockWorldDaily_{newSymbol}', con, index_col='index')
    print(test)


def loadStockWorldDaily(symbol):
    newSymbol = f'{symbol}'.split('@')[0]
    stockWorldDailyList = db.pd.read_sql(f'SELECT * FROM stockWorldDaily_{newSymbol}', con, index_col='index')
    dict = stockWorldDailyList.T.to_dict()
    print(dict)
    return dict
    # for i in range(0, len(dict)):
    #     date = dict[i]['date']
    #     count = 0
    #     for j in range(0, len(dict)):
    #         if date == dict[j]['date']:
    #             count += 1
    #     if count > 1:
    #         print(date)
    #         print(count)


    # print(keys)


def loadCSV():
    dict = {}
    keyList = []
    f = open(path + '/kospiFutures.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for i,line in enumerate(rdr):
        if i == 0:
            keyList = line
        else:
            dataDict = {}
            for j, key in enumerate(keyList):
                data = line[j]
                if j == 0:
                    data = data.replace('/','')
                dataDict[key] = data

            dict[i-1] = dataDict

    f.close()

    print(dict)
    return dict