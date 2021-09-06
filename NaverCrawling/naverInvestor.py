#-*- coding:utf-8 -*-
from .lib import naverCrawling as nc
from .db import dbManager as db



kospi = "01"
kosdaq = "02"
futures = "03"



def getInvestorDailyInfo(date, marketType):
    infoDict = {}
    url = f'https://finance.naver.com/sise/investorDealTrendDay.nhn?bizdate={date}&sosok={marketType}&page='
    obj = nc.getHtmlObj(url)

    page = 1
    maxPage = int(obj.find("td",{"class","pgRR"}).find("a").get("href").split("=")[-1])

    thObjList = obj.find_all("th")
    columnList = list(map(lambda x: x.text, filter(lambda x: x.has_attr("colspan") == False, thObjList)))
    # 기타법인 뒤로 보내기
    lastColunm = columnList[4]
    del columnList[4]
    columnList.append(lastColunm)
    for column in columnList:
        infoDict[column] = []

    while page <= maxPage:
        print(f'{marketType}: {page}/{maxPage}')
        pageUrl = f'{url}{page}'
        obj = nc.getHtmlObj(pageUrl)

        trList = list(filter(lambda x: x.find("td",{"class","date2"}) != None, obj.find_all("tr")))
        for tr in trList:
            tdList = tr.find_all("td")
            for column, td in zip(columnList, tdList):
                infoDict[column].append(td.text)

        page += 1

    # print(infoDict)
    return infoDict




def saveAllDailyInvestorInfo():
    con = db.getConnection("naverInvestorDailyInfo.db")
    marketList = [kospi, kosdaq, futures]

    date = nc.getTodayStr()
    for market in marketList:
        investorDailyInfo = getInvestorDailyInfo(date, market)
        newInvestorDailyDict = {'infoJson': db.json.dumps(investorDailyInfo, ensure_ascii=False)}
        df = db.DataFrame(newInvestorDailyDict, index=[date])
        df.to_sql(f'investorDailyInfo_{market}', con, if_exists='append', index_label='date')











def getInvestorInfo(date, marketType):
    infoDict = {}
    url = f'https://finance.naver.com/sise/investorDealTrendTime.nhn?bizdate={date}&sosok={marketType}&page='
    obj = nc.getHtmlObj(url)

    page = 1
    maxPage = int(obj.find("td",{"class","pgRR"}).find("a").get("href").split("=")[-1])

    thObjList = obj.find_all("th")
    columnList = list(map(lambda x: x.text, filter(lambda x: x.has_attr("colspan") == False, thObjList)))
    # 기타법인 뒤로 보내기
    lastColunm = columnList[4]
    del columnList[4]
    columnList.append(lastColunm)
    for column in columnList:
        infoDict[column] = []

    while page <= maxPage:
        print(f'{marketType}: {page}/{maxPage}')
        pageUrl = f'{url}{page}'
        obj = nc.getHtmlObj(pageUrl)

        trList = list(filter(lambda x: x.find("td",{"class","date2"}) != None, obj.find_all("tr")))
        for tr in trList:
            tdList = tr.find_all("td")
            for column, td in zip(columnList, tdList):
                infoDict[column].append(td.text)

        page += 1

    return infoDict



def saveAllInvestorInfo():
    con = db.getConnection("naverInvestorInfo.db")
    marketList = [kospi, kosdaq, futures]

    date = nc.getTodayStr()
    for market in marketList:
        investorInfo = getInvestorInfo(date, market)
        newInvestorDict = {'infoJson': db.json.dumps(investorInfo, ensure_ascii=False)}
        df = db.DataFrame(newInvestorDict, index=[date])
        df.to_sql(f'investorInfo_{market}', con, if_exists='append', index_label='date')

    # for date in range(20200317, 20200321):
    #     for market in marketList:
    #         investorInfo = getInvestorInfo(date, market)
    #         newInvestorDict = {'infoJson': db.json.dumps(investorInfo, ensure_ascii=False)}
    #         df = db.DataFrame(newInvestorDict, index=[date])
    #         df.to_sql(f'investorInfo_{market}', con, if_exists='append', index_label='date')


def getLatestInvestorInfo(marketType):
    infoDict = {}
    url = f'https://finance.naver.com/sise/investorDealTrendTime.nhn?bizdate={nc.getTodayStr()}&sosok={marketType}&page='
    obj = nc.getHtmlObj(url)

    thObjList = obj.find_all("th")
    columnList = list(map(lambda x: x.text, filter(lambda x: x.has_attr("colspan") == False, thObjList)))
    # 기타법인 뒤로 보내기
    lastColunm = columnList[4]
    del columnList[4]
    columnList.append(lastColunm)
    for column in columnList:
        infoDict[column] = []

    trList = list(filter(lambda x: x.find("td", {"class", "date2"}) != None, obj.find_all("tr")))
    tr = trList[0]
    tdList = tr.find_all("td")
    for column, td in zip(columnList, tdList):
         infoDict[column] = td.text



    print(infoDict)
    return infoDict


def startRealtime():
    while True:
        getLatestInvestorInfo(kospi)
        nc.time.sleep(60)
