#-*- coding:utf-8 -*-
import sqlite3
import pandas as pd
import datetime
from datetime import timedelta
import math
import matplotlib.pyplot as plt



# def sliceDict(dict, fromIndex, toIndex):
#     newDict = {}
#     keyList = list(dict.keys())
#     sorted(keyList, key=lambda x:datetime.datetime.strptime(x, "%Y%m%d"))
#     keyList = keyList[-(toIndex + 1 + fromIndex) : -(1 + fromIndex)]
#     for key in keyList:
#         newDict.update({key: dict[key]})
#     return newDict

def sliceDict(dict, startDate, days):
    newDict = {}
    keyList = list(dict.keys())
    sorted(keyList, key=lambda x:datetime.datetime.strptime(x, "%Y%m%d"))
    firstIndex = None
    i = 0
    while i < 20:
        if startDate in keyList:
            firstIndex = keyList.index(startDate)
            break
        else:
            nextDay = (datetime.datetime.strptime(startDate, "%Y%m%d") + timedelta(days=1)).strftime("%Y%m%d")
            startDate = nextDay

        i += 1

    if firstIndex == None:
        return

    keyList = keyList[firstIndex:firstIndex + days]
    for key in keyList:
        newDict.update({key: dict[key]})
    return newDict

class SamsungSimulation:
    def __init__(self):
        con = sqlite3.connect("./db/NaverStock.db")
        sqlite3.Connection
        self.dfSamsung = pd.read_sql('SELECT * FROM stockDaily_005930', con, index_col='index').set_index(
            'date').T.to_dict()


    yesterdayClose = 0
    def isDroped(self, todayClose):
        return self.yesterdayClose > todayClose

    # def setData(self, firstIndex, days):
    #     self.samsungDict = sliceDict(self.dfSamsung, firstIndex, days)
    #     # self.seed = 10000000  # 자본금
    #     # self.investmentRatio = investmentRatio # 투자비율
    #     # self.dailyTargetReturnRate = dailyTargetReturnRate  # 일일 목표수익률
    #     self.commissionRate = 0.0003  # 수수료 => 구매수수료: commissionRate / 2, 판매수수료: commissionRate / 2
    #     self.holdingDict = {'quantity': 0, 'averagePrice': 0}

    def setData(self, startDate, days):
        self.samsungDict = sliceDict(self.dfSamsung, startDate, days)
        # self.seed = 10000000  # 자본금
        # self.investmentRatio = investmentRatio # 투자비율
        # self.dailyTargetReturnRate = dailyTargetReturnRate  # 일일 목표수익률
        self.commissionRate = 0.0003  # 수수료 => 구매수수료: commissionRate / 2, 판매수수료: commissionRate / 2
        self.holdingDict = {'quantity': 0, 'averagePrice': 0, 'incomeRate': 0, 'breakEvenDays': []}



    def getLowestPrice(self):
        lowestPriceDict = {'date': '', 'price': 0}
        for i, key in enumerate(self.samsungDict.keys()):
            samsung = self.samsungDict[key]
            if i == 0:
                lowestPriceDict['price'] = samsung['close']
                lowestPriceDict['date'] = key
            if (lowestPriceDict['price'] > samsung['close']):
                lowestPriceDict['price'] = samsung['close']
                lowestPriceDict['date'] = key

        return lowestPriceDict

    def getHighestPrice(self):
        highestPriceDict = {'date': '', 'price': 0}
        for key in self.samsungDict.keys():
            samsung = self.samsungDict[key]
            if (highestPriceDict['price'] < samsung['close']):
                highestPriceDict['price'] = samsung['close']
                highestPriceDict['date'] = key

        return highestPriceDict



    def dailyPurchase(self):
        keyList = sorted(self.samsungDict.keys(), key=lambda x:datetime.datetime.strptime(x, "%Y%m%d"))
        breakEvenDays = 0
        for i, date in enumerate(keyList):
            print(date)
            samsung = self.samsungDict[date]
            self.purchase(samsung)
            # self.purchaseProportionally(samsung)

            breakEvenDays += 1
            if samsung['close'] > self.holdingDict['averagePrice']:
                self.holdingDict['breakEvenDays'].append(breakEvenDays)

            if len(keyList) - 1 == i:
                if (samsung['close'] - self.holdingDict['averagePrice'] > 0) & (self.holdingDict['averagePrice'] > 0):
                    self.holdingDict['incomeRate'] = (samsung['close'] - self.holdingDict['averagePrice']) / self.holdingDict['averagePrice'] * 100


            self.yesterdayClose = self.samsungDict[date]['close']



    def purchase(self, samsung):
        close = samsung['close']
        # print(close)
        print(samsung)
        if self.isDroped(close):
            finalPrice = close + close * (self.commissionRate / 2)
            quantityToBuy = 1
            actualPriceToBuy = quantityToBuy * finalPrice
            totalQty = self.holdingDict['quantity'] + quantityToBuy
            newAveragePrice = (self.holdingDict['quantity'] * self.holdingDict['averagePrice'] + actualPriceToBuy) / totalQty
            self.holdingDict['quantity'] = totalQty
            self.holdingDict['averagePrice'] = newAveragePrice

        # finalPrice = close + close * (self.commissionRate / 2)
        # quantityToBuy = 1
        # actualPriceToBuy = quantityToBuy * finalPrice
        # totalQty = self.holdingDict['quantity'] + quantityToBuy
        # newAveragePrice = (self.holdingDict['quantity'] * self.holdingDict[
        #     'averagePrice'] + actualPriceToBuy) / totalQty
        # self.holdingDict['quantity'] = totalQty
        # self.holdingDict['averagePrice'] = newAveragePrice

    def purchaseProportionally(self, samsung):
        close = samsung['close']
        if self.yesterdayClose == 0:
            self.yesterdayClose = samsung['close']
        rate = 100 - (self.yesterdayClose / close * 100)
        # print(rate)
        # print(self.yesterdayClose)
        # print(samsung)
        # if (rate < 0):
        finalPrice = close + close * (self.commissionRate / 2)
        quantityToBuy = 1 if (rate < 0 or rate == 0) else (math.ceil(abs(rate)))
        actualPriceToBuy = quantityToBuy * finalPrice
        totalQty = self.holdingDict['quantity'] + quantityToBuy
        newAveragePrice = (self.holdingDict['quantity'] * self.holdingDict[
            'averagePrice'] + actualPriceToBuy) / totalQty
        self.holdingDict['quantity'] = totalQty
        self.holdingDict['averagePrice'] = newAveragePrice






simulation = SamsungSimulation()


# 이전 최고점에서 사서 다음 최고점(20200123)에서 팜
# 최대 물린기간: 약 8개월
# 총 투자기간 약 28개월
# 총 투자금액: 떨어졌을때만 매수(1,500만원), 매일 매수(2,600만원)
# 수익률: 떨어졌을때만 매수(약 29%(약 440만원)), 매일 매수(약 27.8%(약 723만원))
# simulation.setData("20171101", 547) # 약 56,000원
# simulation.dailyPurchase()
# print(simulation.holdingDict)

# 이전 최저점에서 사서 다음 최고점(20200123)에서 팜
# 최대 물린기간: 약 한달
# 총 투자기간 약 13개월
# 총 투자금액: 떨어졌을때만 매수(656만원), 매일 매수(1,232만원)
# 수익률: 떨어졌을때만 매수(약 30%(약 197만원)), 매일 매수(약 28.2%(약 347만원))
# simulation.setData("20190104", 260) # 37,450원
# simulation.dailyPurchase()
# print(simulation.holdingDict)


# 이전 최고점에서 사서 다음 최고점(20200123)에서 팜
# 최대 물린기간: 약 8개월
# 총 투자기간 약 28개월
# 총 투자금액: 떨어졌을때만 매수(1,500만원), 매일 매수(3,325만원)
# 수익률: 떨어졌을때만 매수(약 29%(약 440만원)), 매일 매수(약 27.8%(약 724만원))
simulation.setData("20171101", 300)
simulation.dailyPurchase()
print(simulation.holdingDict)



# print(simulation.getHighestPrice())
# print(simulation.getLowestPrice())

# 20171101
# 20170811


