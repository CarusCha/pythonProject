#-*- coding:utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import sqlite3
import pandas as pd
from pandas import DataFrame
import json

# kospi = "0"
# kosdaq = "1"
# con = sqlite3.connect(f"./db/NaverStockData.db")


# def getTodayStr():
#     today = datetime.datetime.today()
#     overDay = today.weekday() - 4
#     if overDay > 0:
#         today += datetime.timedelta(days=-overDay)
#
#     return today.strftime("%Y%m%d")



# def selectOption(url, optionList):
#
#     try:
#         driver = webdriver.Chrome('../NaverCrawling/chromedriver')
#         driver.implicitly_wait(3)
#         driver.get(url)
#
#         html = driver.page_source
#         soup = BeautifulSoup(html, 'html.parser')
#         selectedList = soup.find_all("td", {"class": "choice"})
#         for selected in selectedList:
#             id = selected.find("input").get("id")
#             driver.find_element_by_id(id).click()
#         for option in optionList:
#             driver.find_element_by_id("option" + option).click()
#         driver.execute_script("javascript:fieldSubmit()")
#
#         return BeautifulSoup(driver.page_source, 'html.parser')
#
#     except:
#         print("error")
#         pass

#
# def getHtmlObj(url):
#     result = requests.get(url).content
#     return BeautifulSoup(result, "html.parser")





# def getStockList(marketType):
#     stockDictList = []
#     url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=" + marketType
#     page = 1
#
#     while True:
#         print(page)
#         pageUrl = url + "&page=" + str(page)
#         tdList = getHtmlObj(pageUrl).find_all("td")
#
#         stockList = filter(lambda x: x.find("a", {"class": "tltle"}) != None, tdList)
#         mappedList = list(map(lambda x: {"symbol":x.find("a").get('href').split("=")[-1], "name":x.text}, stockList))
#         if len(mappedList) == 0:
#             break
#         stockDictList.extend(mappedList)
#
#
#         page += 1
#
#     return stockDictList



# def getSectorList():
#     sectorDictList = []
#     table = getHtmlObj("https://finance.naver.com/sise/sise_group.nhn?type=upjong").find("table",{"class":"type_1"})
#     trList = table.find_all("tr")
#     sectorHtmlList = list(filter(lambda x: x.find("td") != None and x.find("td").find("a") != None, trList))
#
#     for sectorHtml in sectorHtmlList:
#         tdList = sectorHtml.find_all("td")
#
#         sectorDict = {}
#         titleHtml = tdList[0].find("a")
#         sectorDict["symbol"] = titleHtml.get('href').split("=")[-1]
#         sectorDict["name"] = titleHtml.text
#         sectorDict["comparedPreviousDate"] = tdList[1].text.replace("\n", "").replace("\t", "")
#         sectorDict["all"] = tdList[2].text
#         sectorDict["increase"] = tdList[3].text
#         sectorDict["steadiness"] = tdList[4].textr
#         sectorDict["decrease"] = tdList[5].text
#
#         sectorDictList.append(sectorDict)
#
#     return sectorDictList



# def getSectorDetails(sectorCode, selectOptionList):
#     url = "https://finance.naver.com/sise/sise_group_detail.nhn?type=upjong&no=" + sectorCode
#     te = selectOption(url, selectOptionList)
#     selectedList = te.find_all("td", {"class": "choice"})
#     print(selectedList)



# class NFStockOption:
#     def __init__(self, name, id, isSelected):
#         self.name = name
#         self.id = id
#         # self.isSelected = False
#         self.isSelected = isSelected


# def getOptionList(soup):
#     optionList = []
#     tdList = soup.find("table",{"class":"item_list"}).find_all("td")
#     tdList = filter(lambda x: x.find("input") != None, tdList)
#     for td in tdList:
#         name = td.text.replace(" ", "")
#         id = td.find("input").get("id")
#         isSelected = td.find("input").get("checked") != None
#         optionList.append(NFStockOption(name, id, isSelected))
#
#     return optionList


# def getStockDataList(marketType):
#     stockDictList = {}
#
#     driver = webdriver.Chrome('./chromedriver')
#     driver.implicitly_wait(3)
#     url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=" + marketType
#
#     page = 1
#     maxSelectionCount = 6
#     basicOptionCount = 6
#     maxPage = int(getHtmlObj(url).find("td",{"class":"pgRR"}).find("a").get('href').split("=")[-1])
#
#     while True:
#         if page > 1:
#             break
#
#         print(page)
#         pageUrl = url + "&page=" + str(page)
#
#         driver.get(pageUrl)
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         optionList = getOptionList(soup)
#
#         # Set Basic Option Values
#         stockList = soup.find_all("tr", {"onmouseover": "mouseOver(this)"})
#         for stock in stockList:
#             tdList = stock.find_all("td")
#             symbol = stock.find("a", {"class": "tltle"}).get('href').split("=")[-1]
#             stockDictList[symbol] = {}
#             stockDictList[symbol]["marketType"] = marketType # 시장타입
#             stockDictList[symbol]["date"] = datetime.date.today().strftime("%Y%m%d") # 날짜
#             stockDictList[symbol]["name"] = tdList[1].text.replace("\n", "").replace("\t", "") # 종목명
#             stockDictList[symbol]["price"] = tdList[2].text.replace("\n", "").replace("\t", "")  # 현재가
#             stockDictList[symbol]["priceDifference"] = tdList[3].text.replace("\n", "").replace("\t", "")  # 전일비
#             stockDictList[symbol]["fluctuationRate"] = tdList[4].text.replace("\n", "").replace("\t", "")  # 등락률
#             stockDictList[symbol]["parValue"] = tdList[5].text.replace("\n", "").replace("\t", "")  # 액면가
#
#         # Set Selected Option Values
#         while 1:
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             selectedOptionList = soup.find_all("td", {"class": "choice"})
#
#             # 추가
#             stockList = soup.find_all("tr", {"onmouseover": "mouseOver(this)"})
#             for stock in stockList:
#                 symbol = stock.find("a", {"class": "tltle"}).get('href').split("=")[-1]
#                 optionNameList = soup.find("thead").find_all("th")[basicOptionCount:-1]
#                 tdList = stock.find_all("td")[basicOptionCount:-1]
#                 for (name, option) in zip(optionNameList, tdList):
#                     stockDictList[symbol][name.text] = option.text.replace("\n", "").replace("\t", "")
#
#
#             notSelectedOptionList = list(filter(lambda x: x.isSelected != True, optionList))
#             if len(notSelectedOptionList) == 0:
#                 break
#
#             # 선택 해제
#             for selectedOption in selectedOptionList:
#                 id = selectedOption.find("input").get("id")
#                 driver.find_element_by_id(id).click()
#
#             # 선택
#             for i, notAddedOption in enumerate(notSelectedOptionList):
#                 id = notAddedOption.id
#                 driver.find_element_by_id(id).click()
#                 notAddedOption.isSelected = True
#                 if i == maxSelectionCount - 1:
#                     break
#
#             driver.execute_script("javascript:fieldSubmit()")
#
#         page += 1
#
#
#
#     return stockDictList



# def getStockDataList(marketType):
#     stockDictList = []
#
#     driver = webdriver.Chrome('NaverCrawling/chromedriver')
#     driver.implicitly_wait(3)
#     url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=" + marketType
#
#     page = 1
#     maxSelectionCount = 6
#     basicOptionCount = 6
#     maxPage = int(getHtmlObj(url).find("td",{"class":"pgRR"}).find("a").get('href').split("=")[-1])
#
#     while True:
#         if page > maxPage:
#             break
#
#         print(page)
#         pageUrl = url + "&page=" + str(page)
#
#         driver.get(pageUrl)
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         optionList = getOptionList(soup)
#
#         # Set Basic Option Values
#         stockList = soup.find_all("tr", {"onmouseover": "mouseOver(this)"})
#         for i, stock in enumerate(stockList):
#             stockDict = {}
#             tdList = stock.find_all("td")
#             symbol = stock.find("a", {"class": "tltle"}).get('href').split("=")[-1]
#             # stockDict["date"] = getTodayStr() # 날짜
#             stockDict["marketType"] = marketType # 시장타입
#             stockDict["symbol"] = symbol
#             stockDict["name"] = tdList[1].text.replace("\n", "").replace("\t", "") # 종목명
#             stockDict["price"] = tdList[2].text.replace("\n", "").replace("\t", "")  # 현재가
#             stockDict["priceDifference"] = tdList[3].text.replace("\n", "").replace("\t", "")  # 전일비
#             stockDict["fluctuationRate"] = tdList[4].text.replace("\n", "").replace("\t", "")  # 등락률
#             stockDict["parValue"] = tdList[5].text.replace("\n", "").replace("\t", "")  # 액면가
#             stockDictList.append(stockDict)
#         # Set Selected Option Values
#         while 1:
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             selectedOptionList = soup.find_all("td", {"class": "choice"})
#
#             # 추가
#             stockList = soup.find_all("tr", {"onmouseover": "mouseOver(this)"})
#             for i, stock in enumerate(stockList):
#                 symbol = stock.find("a", {"class": "tltle"}).get('href').split("=")[-1]
#                 optionNameList = soup.find("thead").find_all("th")[basicOptionCount:-1]
#                 tdList = stock.find_all("td")[basicOptionCount:-1]
#                 for (name, option) in zip(optionNameList, tdList):
#                     value = option.text.replace("\n", "").replace("\t", "")
#                     try:
#                         floatVal = float(value.replace(',', ''))
#                         value = floatVal
#                     except:
#                         print("error")
#
#
#                     list(filter(lambda x: x["symbol"] == symbol, stockDictList))[0][name.text] = value
#
#
#
#             notSelectedOptionList = list(filter(lambda x: x.isSelected != True, optionList))
#             if len(notSelectedOptionList) == 0:
#                 break
#
#             # 선택 해제
#             for selectedOption in selectedOptionList:
#                 id = selectedOption.find("input").get("id")
#                 driver.find_element_by_id(id).click()
#
#             # 선택
#             for i, notAddedOption in enumerate(notSelectedOptionList):
#                 id = notAddedOption.id
#                 driver.find_element_by_id(id).click()
#                 notAddedOption.isSelected = True
#                 if i == maxSelectionCount - 1:
#                     break
#
#             driver.execute_script("javascript:fieldSubmit()")
#
#
#         page += 1
#
#     # print(stockDictList)
#     driver.close()
#     return stockDictList


# def saveStcokDataList():
#
#     enableToAddTable = False
#     try:
#         if ((getTodayStr() in pd.read_sql(f'SELECT * FROM stockData', con, index_col='date')[
#             'dataJson'].keys()) == False):
#             enableToAddTable = True
#
#         else:
#             print('Already exist')
#
#     except:
#         print('new')
#         enableToAddTable = True
#
#
#     if enableToAddTable:
#         kospiStockList = getStockDataList("0")
#         time.sleep(3)
#         kosdaqStockList = getStockDataList("1")
#         stockList = kospiStockList + kosdaqStockList
#         dumpsStockList = json.dumps(stockList, ensure_ascii=False)
#
#         newDict = {}
#         newDict['dataJson'] = dumpsStockList
#         df = DataFrame(newDict, index=[getTodayStr()])
#         df.to_sql(f'stockData', con, if_exists='append', index_label='date')
#         test = pd.read_sql(f'SELECT * FROM stockData', con, index_col='date')
#         print(test)





def getStockDailyList(symbol):
    obj = getHtmlObj(f'https://fchart.stock.naver.com/sise.nhn?symbol={symbol}&timeframe=day&count=5000&requestType=0')
    itemList = obj.find_all("item")

    stockDailyDictList = []
    for item in itemList:
        stockDailyDict = {}
        dataList = item.get("data").split("|")
        stockDailyDict["date"] = dataList[0]
        stockDailyDict["open"] = int(dataList[1])
        stockDailyDict["high"] = int(dataList[2])
        stockDailyDict["low"] = int(dataList[3])
        stockDailyDict["close"] = int(dataList[4])
        stockDailyDict["volume"] = int(dataList[5])
        stockDailyDictList.append(stockDailyDict)


    print(len(itemList))
    print(len(stockDailyDictList))
    print(stockDailyDictList)
    return stockDailyDictList



# def saveStockDaily(symbol):
#     stockDailyList = getStockDailyList(symbol)
#     df = DataFrame(stockDailyList)
#     df.to_sql(f'stockDaily_{symbol}', con, if_exists='replace', chunksize=5000)
#     test = pd.read_sql(f'SELECT * FROM stockDaily_{symbol}', con, index_col='index')
#     print(test)


# def saveStockList(marketType):
#     kospiList = getStockList(marketType)
#     df = DataFrame(kospiList)
#     df.to_sql(f'stock_{marketType}', con, if_exists='replace', chunksize=5000)


# saveStockList(kospi)

# kospiList = pd.read_sql('SELECT * FROM stock_0', con, index_col='index')['symbol']
# for i, kospi in enumerate(kospiList):
#     print(str(i)+"/"+str(len(kospiList)))
#     saveStockDaily(kospi)

# print(getStockList(kospi))
# saveStockDaily("005930")
#






