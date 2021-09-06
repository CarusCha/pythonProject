#-*- coding:utf-8 -*-
from NaverCrawling.lib import naverCrawling as nc
from NaverCrawling import naverStockInfo
from functools import reduce
from ..db import dbManager as db

def getSectorList():
    sectorDictList = []
    table = nc.getHtmlObj("https://finance.naver.com/sise/sise_group.nhn?type=upjong").find("table",{"class":"type_1"})
    trList = table.find_all("tr")
    sectorHtmlList = list(filter(lambda x: x.find("td") != None and x.find("td").find("a") != None, trList))

    for sectorHtml in sectorHtmlList:
        tdList = sectorHtml.find_all("td")

        sectorDict = {}
        titleHtml = tdList[0].find("a")
        sectorDict["symbol"] = titleHtml.get('href').split("=")[-1]
        sectorDict["name"] = titleHtml.text
        sectorDict["comparedPreviousDate"] = tdList[1].text.replace("\n", "").replace("\t", "")
        sectorDict["all"] = tdList[2].text
        sectorDict["increase"] = tdList[3].text
        sectorDict["steadiness"] = tdList[4].textr
        sectorDict["decrease"] = tdList[5].text

        sectorDictList.append(sectorDict)

    # print(sectorDictList)
    return sectorDictList



def getSectorStockList(upjongNumber):
    sectorStockDictList = []
    table = nc.getHtmlObj("https://finance.naver.com/sise/sise_group_detail.nhn?type=upjong&no=" + upjongNumber)
    trList = table.find_all("td", {"class": "name"}, "a")
    # test = list(map(lambda x: x.text, trList))
    mappedList = list(map(lambda x: {"marketType": ("0" if "*" not in x.text else "1"),
                                     "symbol": x.find("a").get('href').split("=")[-1],
                                     "name": x.find("a").text}, trList))

    print(len(mappedList))
    print(mappedList)


def getSectorStockListWithInfo(upjongNumber, date):
    table = nc.getHtmlObj("https://finance.naver.com/sise/sise_group_detail.nhn?type=upjong&no=" + upjongNumber)
    trList = table.find_all("td", {"class": "name"}, "a")
    # mappedList = list(map(lambda x: {"marketType": ("0" if "*" not in x.text else "1"),
    #                                  "symbol": x.find("a").get('href').split("=")[-1],
    #                                  "name": x.find("a").text}, trList))
    symbolList = list(map(lambda x: x.find("a").get('href').split("=")[-1], trList))

    stockInfoList = naverStockInfo.getStockInfoListFromDB(date)
    filteredList = list(filter(lambda x: x["symbol"] in symbolList, stockInfoList))
    return filteredList


    # filteredList = list(filter(lambda x: x["ROE"] > 0, filteredList)) # ROE filter
    # filteredList = list(filter(lambda x: x["PER"] > 0, filteredList)) # PER filter
    # filteredList = sorted(filteredList, key=lambda x: x['PER'], reverse=False) # PER Sort
    #
    #
    # for stock in filteredList:
    #     print(stock)

def getSectorPERList():
    date = nc.getTodayStr()
    sectorList = getSectorList()

    stockPERDictList = []
    stockPERDictList_Minus = []
    for i, sector in enumerate(sectorList):
        print(f'{i+1}/{len(sectorList)}')
        stockList = getSectorStockListWithInfo(sector["symbol"], date)
        perList = list(map(lambda x: 0 if x.get("PER", None) is None else x["PER"], stockList))
        filteredList = list(filter(lambda x: (x > 0 and x < 200), perList))
        if len(filteredList) > 0:
            averPER = reduce(lambda x, y: x + y, filteredList) / len(filteredList)
            stockPERDict = {"name": sector["name"], "averPER": round(averPER, 2)}
            print(stockPERDict)
            stockPERDictList.append(stockPERDict)
        else:
            filteredList = list(filter(lambda x: (x > -200 and x < 200), perList))
            averPER = reduce(lambda x, y: x + y, filteredList) / len(filteredList)
            stockPERDict = {"name": sector["name"], "averPER": round(averPER, 2)}
            print(stockPERDict)
            stockPERDictList_Minus.append(stockPERDict)

    sortedList = sorted(stockPERDictList, key=lambda x: x['averPER'], reverse=False)  # PER Sort
    sortedList += sorted(stockPERDictList_Minus, key=lambda x: x['averPER'], reverse=True)  # PER Sort

    print("")
    for per in sortedList:
        print(per)


def saveSectorList():
    date = nc.getTodayStr()
    sectorList = getSectorList()
    # sectorDictList = []
    sectorDict = {}
    for i, sector in enumerate(sectorList):
        print(f'{i+1}/{len(sectorList)}')
        stockList = getSectorStockListWithInfo(sector["symbol"], date)
        # sectorDict = {"symbol": sector["symbol"], "stock": db.json.dumps(stockList, ensure_ascii=False)}
        # sectorDict = db.json.dumps({"symbol": sector["symbol"], "stock": stockList}, ensure_ascii=False)
        # sectorDictList.append(sectorDict)
        sectorDict[sector["symbol"]] = db.json.dumps(stockList, ensure_ascii=False)


    con = db.getConnection("naverSectorList.db")
    df = db.DataFrame(sectorDict, index=['stock'])
    df.to_sql(f'stock_{date}', con, if_exists='replace', index_label='stock')
    test = db.pd.read_sql(f'SELECT * FROM stock_{date}', con, index_col='stock')
    print(test)


def getSectorListFromDB(date):
    con = db.getConnection("naverSectorList.db")
    stockData = db.pd.read_sql(f'SELECT * FROM stock_{date}', con, index_col='stock').T.to_dict()
    # print(list(filter(lambda x: x["symbol"] == "217", stockData)))
    # stockDataList = db.json.loads(stockData)
    return stockData['stock']


def getSectorPERListFromDB():
    date = nc.getTodayStr()
    sectorList = getSectorList()

    stockPERDictList = []
    stockPERDictList_Minus = []
    sectorDictList = getSectorListFromDB(date)

    for i, sector in enumerate(sectorList):
        print(f'{i+1}/{len(sectorList)}')
        stockList = db.json.loads(sectorDictList[sector["symbol"]])
        # stockList = list(map(lambda x: x['stock'], stockList))
        # print(type(stockList))
        perList = list(map(lambda x: 0 if x.get("PER", None) is None else x["PER"], stockList))
        filteredList = list(filter(lambda x: (x > 0 and x < 200), perList))
        if len(filteredList) > 0:
            averPER = reduce(lambda x, y: x + y, filteredList) / len(filteredList)
            stockPERDict = {"name": sector["name"], "averPER": round(averPER, 2)}
            # print(stockPERDict)
            stockPERDictList.append(stockPERDict)
        else:
            filteredList = list(filter(lambda x: (x > -200 and x < 200), perList))
            averPER = reduce(lambda x, y: x + y, filteredList) / len(filteredList)
            stockPERDict = {"name": sector["name"], "averPER": round(averPER, 2)}
            # print(stockPERDict)
            stockPERDictList_Minus.append(stockPERDict)

    sortedList = sorted(stockPERDictList, key=lambda x: x['averPER'], reverse=False)  # PER Sort
    sortedList += sorted(stockPERDictList_Minus, key=lambda x: x['averPER'], reverse=True)  # PER Sort

    print("")
    for per in sortedList:
        print(per)



def getSectorLeaderListFromDB():
    date = nc.getTodayStr()
    sectorList = getSectorList()

    stockLeaderDictList = []
    sectorDictList = getSectorListFromDB(date)

    for i, sector in enumerate(sectorList):
        # print(f'{i+1}/{len(sectorList)}')
        stockList = db.json.loads(sectorDictList[sector["symbol"]])
        leader = list(sorted(stockList, key=lambda x: (0 if x.get('시가총액') is None else x.get('시가총액')), reverse=True))[0]
        print(leader)
        stockPERDict = {"name": leader["name"], "sector": sector["name"], "PER": 0 if leader.get("PER", None) is None else leader["PER"]}
        stockLeaderDictList.append(stockPERDict)


    sortedList = sorted(stockLeaderDictList, key=lambda x: x['PER'], reverse=False)  # PER Sort

    for leader in sortedList:
        print(leader)