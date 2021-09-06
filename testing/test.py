#-*- coding:utf-8 -*-
import sqlite3
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm

# baseInvestmentRatio = 0.1 # 투자비율
# baseDailyTargetReturnRate = 0.02 # 일일 목표수익률

def sliceDictWithDate(dict, date, toIndex):
    newDict = {}
    keyList = list(dict.keys())
    fromIndex = keyList.index(date)
    # print(fromIndex, toIndex)
    keyList = list(dict.keys())[fromIndex:fromIndex + toIndex]
    # print(keyList)
    for key in keyList:
        newDict.update({key: dict[key]})
    return newDict

def sliceDict(dict, fromIndex, toIndex):
    newDict = {}
    keyList = list(dict.keys())
    sorted(keyList, key=lambda x:datetime.datetime.strptime(x, "%Y%m%d"))
    keyList = keyList[-(toIndex + 1 + fromIndex) : -(1 + fromIndex)]
    # keyList = list(dict.keys())[-(toIndex + 1 + fromIndex) : -(1 + fromIndex)]
    # print(-(toIndex + fromIndex))
    # print(-(toIndex + 1 + fromIndex))
    # print(-(1 + fromIndex))

    # print(len(list(dict.keys())[-(toIndex + 1 + fromIndex) : -(1 + fromIndex)]))
    # print('sliceDict', keyList)
    for key in keyList:
        newDict.update({key: dict[key]})
    return newDict


class KodexETFSimulation:

    def __init__(self):
        con = sqlite3.connect("./db/NaverStock.db")
        sqlite3.Connection
        self.dfKodex = pd.read_sql('SELECT * FROM stockDaily_122630', con, index_col='index').set_index('date').T.to_dict()
        self.dfKodexInverse = pd.read_sql('SELECT * FROM stockDaily_252670', con, index_col='index').set_index('date').T.to_dict()
        # self.kodexDict = sliceDictWithDate(dfKodex, baseDate, days)
        # self.kodexInverseDict = sliceDictWithDate(dfKodexInverse, baseDate, days)





    def setData(self, firstIndex, days, investmentRatio, dailyTargetReturnRate):
        self.kodexDict = sliceDict(self.dfKodex, firstIndex, days)
        self.kodexInverseDict = sliceDict(self.dfKodexInverse, firstIndex, days)
        self.seed = 10000000  # 자본금
        self.investmentRatio = investmentRatio # 투자비율
        self.dailyTargetReturnRate = dailyTargetReturnRate  # 일일 목표수익률

        self.seedList = []  # 자본금 증가리스트; [{'date': string, 'seed': seed, 'rate': float}]
        self.commissionRate = 0.0003  # 수수료 => 구매수수료: commissionRate / 2, 판매수수료: commissionRate / 2
        self.holdingUnitDict = {'kodex': {'quantity': 0, 'averagePrice': 0}, 'inverse': {'quantity': 0, 'averagePrice': 0}}
        self.cumulativeSell = {'income': 0, 'count': 0}  # 누적매도


    def startSimulation(self):
        keyList = sorted(self.kodexInverseDict.keys(), key=lambda x:datetime.datetime.strptime(x, "%Y%m%d"))
        print(keyList[0])
        for date in keyList:
            self.purchase('kodex', date)
            self.purchase('inverse', date)

            self.sell('kodex', date)
            self.sell('inverse', date)

            self.additionalPurchase(date)
            self.yesterdayClose = {'kodex': self.kodexDict[date]['close'], 'inverse': self.kodexInverseDict[date]['close']}

            # '자본금 증가리스트'에 현 날짜와 자본금을 저장한다.
            self.seedList.append(
                {'date': date, 'seed': f'{self.getForceToSellSeed(date)} | {self.getEstimatedSeed()}', 'rate': self.incomeRate(date)})

            # print(simulation.seedList)
            print(date)
            print(simulation.holdingUnitDict)
            print(simulation.cumulativeSell)
            print('incomeRate', self.incomeRate(date))
            print(self.seedList[-1])
            print(self.seed)







    def getEstimatedSeed(self):  # 추정자본금(보유종목의 금액을 합한)
        return self.seed + self.getHoldingUnitPrice()

    def getForceToSellSeed(self, date):
        return self.seed + self.getForceToSellHodings(date)

    # 보유 수량; {'kodex': {'quantity': int, 'averagePrice': int}, 'inverse': {'quantity': int, 'averagePrice': int}}
    def getHoldingUnitPrice(self):  # 보유종목의 금액
        k = self.holdingUnitDict['kodex']
        i = self.holdingUnitDict['inverse']
        amount = (k['quantity'] * k['averagePrice'] + i['quantity'] * i['averagePrice'])
        return amount - amount * (self.commissionRate / 2)

    def getForceToSellHodings(self, date):
        k = self.holdingUnitDict['kodex']
        i = self.holdingUnitDict['inverse']
        amount = (k['quantity'] * self.kodexDict[date]['close']) + (i['quantity'] * self.kodexInverseDict[date]['close'])
        return amount - amount * (self.commissionRate / 2)


    def incomeRate(self, date):
        return self.cumulativeSell['income'] / self.getForceToSellSeed(date) * 100


    yesterdayClose = {'kodex': 0, 'inverse': 0}
    def isDroped(self, unitName, todayClose):
        return self.yesterdayClose[unitName] > todayClose



    # '보유 수량'이 없을때 'close' 가격에 수수료를 더한 금액으로 '추정자본금'의 '투자비율'에 따른 수량만큼 매수한다.
    # 이때, '자본금'이 부족할 경우 매수하지 않는다.
    # 매수된 금액만큼 자본금에서 뺀다.
    # 매수성공 종목을 '보유 수량'에 저장한다.
    def purchase(self, unitName, date):
        holdingDict = self.holdingUnitDict[unitName]
        if holdingDict['quantity'] == 0:
            unitDict = self.kodexDict if unitName == 'kodex' else self.kodexInverseDict
            close = unitDict[date]['close']
            finalPrice = close + close * (self.commissionRate / 2)
            amountToBuy = self.getEstimatedSeed() * self.investmentRatio
            quantityToBuy = amountToBuy // finalPrice
            if quantityToBuy > 0: # 예약매수
                actualAmountToBuy = quantityToBuy * finalPrice

                # test to add money
                if self.seed < actualAmountToBuy:
                    print('test to add money', actualAmountToBuy * 1.1)
                    self.seed += actualAmountToBuy * 1.1


                if self.seed > actualAmountToBuy:
                    self.seed -= actualAmountToBuy
                    holdingDict['quantity'] = quantityToBuy
                    holdingDict['averagePrice'] = finalPrice
                    # print(self.holdingUnitDict)




    # '평단가' 대비 '일일 목표수익률'에 달성한 종목을 '수수료'를 계산한 금액으로 매도한 후 자본금에 더한다.
    # 매도완료한 종목은 '보유 수량'에서 삭제한다.
    def sell(self, unitName, date):
        holdingDict = self.holdingUnitDict[unitName]
        # print(unitName, 'quantity', holdingDict['quantity'])
        if holdingDict['quantity'] > 0:
            unitDict = self.kodexDict if unitName == 'kodex' else self.kodexInverseDict
            high = unitDict[date]['high']
            close = unitDict[date]['close']
            averagePrice = holdingDict['averagePrice']
            finalAveragePrice = averagePrice + averagePrice * (self.commissionRate / 2)
            amountToBuy = self.getEstimatedSeed() * self.investmentRatio
            quantityToBuy = amountToBuy // finalAveragePrice
            # newReturnRate = -(self.dailyTargetReturnRate * 1.7) if holdingDict['quantity'] > quantityToBuy * 2 else self.dailyTargetReturnRate
            newReturnRate = self.dailyTargetReturnRate

            # print(holdingDict['quantity'] > quantityToBuy * 2)
            # print(finalAveragePrice)
            # print(high)
            targetPrice = finalAveragePrice + finalAveragePrice * newReturnRate
            # print(targetPrice)
            # print('close', close)
            # print('finalAveragePrice', finalAveragePrice)
            if high > targetPrice:  # 예약매도
                # print(self.seed)
                # print(self.holdingUnitDict)
                # print(self.kodexInverseDict[date]['close'])
                # print(targetPrice)
                # print('판매수량', holdingDict['quantity'])
                income = (targetPrice - finalAveragePrice) * holdingDict['quantity']
                # print('매도', income)
                totalPrice = holdingDict['quantity'] * targetPrice
                self.cumulativeSell['income'] += income
                self.cumulativeSell['count'] += 1

                self.seed += totalPrice
                holdingDict['quantity'] = 0
                holdingDict['averagePrice'] = 0

            elif close > finalAveragePrice:
                income = (close - finalAveragePrice) * holdingDict['quantity']
                # print('매도', income)
                totalPrice = holdingDict['quantity'] * close
                self.cumulativeSell['income'] += income
                self.cumulativeSell['count'] += 1

                self.seed += totalPrice
                holdingDict['quantity'] = 0
                holdingDict['averagePrice'] = 0

        # else:
        #     print('no')




    # 남은 '보유 수량'이 한 종목일 경우, 해당 종목은(판매 실패) 종가가 '일일 목표수익률'이상 하락일 경우 '추정자본금'의 '투자비율'에 따른 수량만큼 추가매수 한다.
    # 이때, '자본금'이 부족할 경우 매수하지 않는다.
    def additionalPurchase(self, date):
        unitName = ''
        if (self.holdingUnitDict['kodex']['quantity'] > 0) & (self.holdingUnitDict['inverse']['quantity'] == 0):
            unitName = 'kodex'
        elif (self.holdingUnitDict['kodex']['quantity'] == 0) & (self.holdingUnitDict['inverse']['quantity'] > 0):
            unitName = 'inverse'

        if unitName != '':
            unitDict = self.kodexDict if unitName == 'kodex' else self.kodexInverseDict
            close = unitDict[date]['close']
            holdingDict = self.holdingUnitDict[unitName]
            averagePrice = holdingDict['averagePrice']
            finalAveragePrice = averagePrice + averagePrice * (self.commissionRate / 2)
            targetMinusPrice = finalAveragePrice - finalAveragePrice * self.dailyTargetReturnRate
            # isDroped = unitDict[date]['close'] > unitDict[date]['open']

            # if (close <= targetMinusPrice):
            if (close <= targetMinusPrice) & self.isDroped(unitName, unitDict[date]['close']):
                amountToBuy = self.getEstimatedSeed() * self.investmentRatio
                quantityToBuy = (amountToBuy // close) * 1.5 # 손익률 마이너스이고 주가도 떨어지고 있다면, 1.5배 추가구매
                if quantityToBuy > 0:
                    actualAmountToBuy = quantityToBuy * close

                    # test to add money
                    # if self.seed < actualAmountToBuy:
                    #     print('test to add money', actualAmountToBuy * 1.1)
                    #     self.seed += actualAmountToBuy * 1.1

                    if self.seed > actualAmountToBuy:
                        self.seed -= actualAmountToBuy
                        totalQty = holdingDict['quantity'] + quantityToBuy
                        newAveragePrice = (holdingDict['quantity'] * holdingDict['averagePrice'] + actualAmountToBuy) / totalQty
                        holdingDict['quantity'] = totalQty
                        holdingDict['averagePrice'] = newAveragePrice



    def testPeriod(self):
        resultDict = {'count': 0, 'worstIncome':999999999, 'worstPeriod': '', 'bestIncome': 0, 'bestRate': "", 'bestPeriod': '', 'averageIncome': 0, 'averageRate': 0}
        totalIncome = 0
        totalRate = 0

        i = 0
        while True:
            self.setData(i, 20) # 20일
            self.startSimulation()
            income = self.cumulativeSell['income']
            rate = income / baseSeed * 100
            totalIncome += income
            totalRate += rate
            # print(income)
            if resultDict['bestIncome'] < income:
                resultDict['bestIncome'] = income
                resultDict['bestRate'] = rate
                resultDict['bestPeriod'] = f'{list(self.kodexInverseDict.keys())[0]} - {list(self.kodexInverseDict.keys())[-1]}'
            # print(list(simulation.kodexDict.keys())[0])

            # print(resultDict['worstIncome'])
            # print(income)

            # print(resultDict['worstIncome'] > income)
            if resultDict['worstIncome'] > income:
                resultDict['worstIncome'] = income
                resultDict['worstPeriod'] = f'{list(self.kodexInverseDict.keys())[0]} - {list(self.kodexInverseDict.keys())[-1]}'

            if len(self.kodexInverseDict) < 20: # 20일
                resultDict['count'] = i
                resultDict['averageIncome'] = totalIncome / i
                resultDict['averageRate'] = totalRate / i
                return resultDict

            i += 1





simulation = KodexETFSimulation()
# list = sorted(list(simulation.dfKodexInverse.keys()), key=lambda x: datetime.datetime.strptime(x, "%Y%m%d"))
# for x in list:
#     print(x)


simulation.setData(0, 240, 0.1, 0.003)
simulation.startSimulation()

dateList = list(map(lambda x: x['date'] ,simulation.seedList))
rateList = list(map(lambda x: x['rate'] ,simulation.seedList))

plt.plot(dateList, rateList, label = 'Earning')
plt.xlabel('Date')
plt.ylabel('Earning Rate')
plt.title('KODEX 200 ETF Auto Trading For 1 year')
plt.legend()
plt.show()

#
# baseInvestmentRatio = 1
# baseDailyTargetReturnRate = 0.02
# print(simulation.testPeriod())

# bestResult = {'count': 0, 'bestIncome': 0, 'bestRate': "", 'bestPeriod': "", 'averageIncome': 0, 'averageRate': 0}
# worstResult = {'count': 0, 'bestIncome': 0, 'bestRate': "", 'bestPeriod': "", 'averageIncome': 0, 'averageRate': 0}

# for investmentRatio in np.arange(0.01, 0.1, 0.01):
#     print('investmentRatio', investmentRatio)
#     for targetReturnRate in np.arange(0.003, 0.3, 0.03):
#         print('targetReturnRate', targetReturnRate)
#
#         baseInvestmentRatio = investmentRatio
#         baseDailyTargetReturnRate = targetReturnRate
#         result = simulation.testPeriod()
#         if bestResult['averageIncome'] < result['averageIncome']:
#             print('bestIncome', bestResult['bestIncome'], result['bestIncome'])
#             print('investmentRatio', investmentRatio)
#             print('targetReturnRate', targetReturnRate)
#             bestResult = simulation.testPeriod()
#
#
# print(bestResult)

# {'count': 2452, 'bestIncome': 445716.3963932199, 'bestRate': 4.4571639639321985, 'bestPeriod': '20180213 - 20180329', 'averageIncome': 54576.68884538621, 'averageRate': 0.5457668884538622}




# solutions
# 전일 볼륨에 따른 목표수익률 변경
# 혹은.. 무조건 올팔내사를 해보기?(종가에 무조건 떨어진건 사고 오른건 팔고)


