#-*- coding:utf-8 -*-
from .lib import naverCrawling as nc
from .db import dbManager as db

con = db.getConnection("naverStockDaily.db")


def getPreDateStock(dateStr, stockDict):
    today = nc.datetime.datetime.strptime(dateStr, "%Y%m%d")
    for dict in stockDict:
        stockDateStr = stockDict[dict]['date']
        stockDate = nc.datetime.datetime.strptime(stockDateStr, "%Y%m%d")
        if stockDate < today:
            return stockDict[dict]


def getUpRate(stockDict):
    open = stockDict['open']
    high = stockDict['high']
    if type(open) == str:
        open = float(open.replace(',', ''))
    if type(high) == str:
        high = float(high.replace(',', ''))

    upRate = ((high - open) / high * 100)

    return upRate

def getDownRate(stockDict):
    open = stockDict['open']
    low = stockDict['low']
    if type(open) == str:
        open = float(open.replace(',', ''))
    if type(low) == str:
        low = float(low.replace(',', ''))

    upRate = ((low - open) / low * 100)

    return upRate


def getLargerGap(stockDict):
    open = stockDict['open']
    high = stockDict['high']
    low = stockDict['low']
    if type(open) == str:
        open = float(open.replace(',', ''))
    if type(high) == str:
        high = float(high.replace(',', ''))
    if type(low) == str:
        low = float(low.replace(',', ''))

    if (high - open) > (open - low):
        return 'high'
    elif (high - open) < (open - low):
        return 'low'
    else:
        return 'same'





def getStockDailyList(symbol):
    obj = nc.getHtmlObj(f'https://fchart.stock.naver.com/sise.nhn?symbol={symbol}&timeframe=day&count=5000&requestType=0')
    itemList = obj.find_all("item")
    stockDailyDictList = []
    for item in itemList:
        stockDailyDict = {}
        dataList = item.get("data").split("|")
        stockDailyDict["date"] = dataList[0]
        stockDailyDict["open"] = float(dataList[1])
        stockDailyDict["high"] = float(dataList[2])
        stockDailyDict["low"] = float(dataList[3])
        stockDailyDict["close"] = float(dataList[4])
        stockDailyDict["volume"] = float(dataList[5])
        stockDailyDictList.append(stockDailyDict)


    print(len(itemList))
    print(len(stockDailyDictList))
    print(stockDailyDictList)
    return stockDailyDictList


def saveStockDaily(symbol):
    stockDailyList = getStockDailyList(symbol)
    df = db.DataFrame(stockDailyList)
    df.to_sql(f'stockDaily_{symbol}', con, if_exists='replace', chunksize=5000)
    test = db.pd.read_sql(f'SELECT * FROM stockDaily_{symbol}', con, index_col='index')
    print(test)


def saveAllStockDaily():
    stockListCon = db.getConnection("naverStockList.db")
    kospiList = db.pd.read_sql('SELECT * FROM stock_0', stockListCon, index_col='index')['symbol']
    kosdaqList = db.pd.read_sql('SELECT * FROM stock_1', stockListCon, index_col='index')['symbol']


    for i, kospi in enumerate(kospiList):
        print("kospi: " + str(i) + "/" + str(len(kospiList)))
        saveStockDaily(con, kospi)

    for i, kosdaq in enumerate(kosdaqList):
        print("kosdaq: " + str(i) + "/" + str(len(kosdaqList)))
        saveStockDaily(con, kosdaq)





# 상승장 및 하락장 상승 및 하락 확률 테스트
def testSimulation(worldStockDict):
    # stockList = getStockDailyList("122630") # 레버리지
    stockList = getStockDailyList("252670") # 선물 인버스
    # stockList = getStockDailyList("233740") # 코스닥 레버리지
    # stockList = getStockDailyList("069500") # kodex 200

    stockList = stockList[-800:]

    seed = 1000000

    totalVolume = 0

    yesterdayPrice = 0
    yesterdayStatus = ""
    allCount = len(stockList)
    allUp = 0
    up_up = 0
    up_down = 0

    allDown = 0
    down_up = 0
    down_down = 0

    allNone = 0
    none_up = 0
    none_down = 0

    maxUp = 0
    minUp = 100
    averageUp = 0

    targetRate = 0.5
    countOfLessTarget = 0
    countZero = 0
    countOfLoss = 0

    upFluctuation = 0
    uf_up = 0
    uf_down = 0

    downFluctuation = 0
    df_up = 0
    df_down = 0


    isZero = 0
    pointOneToHalf = 0
    zeroToPointOne = 0
    halfToOne = 0
    moreThanOne = 0

    relativeCount = 0
    relativeAllCount = 0

    for stock in stockList:
        status = "변동없음"
        date = stock['date']
        open = stock["open"]
        high = stock["high"]
        low = stock["low"]
        close = stock["close"]
        volume = stock["volume"]




        fluctuation = 0
        try:
            fluctuation = 100 - (yesterdayPrice / open * 100)
        except:
            pass

        totalVolume += volume

        # y = x + x * z/100
        # z = (y - x) / x * 100
        print('\n')
        worldStock = getPreDateStock(date, worldStockDict)
        print(f'worldStock: {worldStock}')
        worldStockUpRate = getUpRate(worldStock)
        print(f'worldStock uprate: {worldStockUpRate}')
        worldStockDownRate = getDownRate(worldStock)
        print(f'worldStock downrate: {worldStockDownRate}')
        worldStockLargetGap = getLargerGap(worldStock)
        print(f'worldStock LargerGap: {worldStockLargetGap}')

        worldHigh = float(worldStock['high'].replace(',',''))
        worldLow = float(worldStock['low'].replace(',',''))








        upRate = 0
        try:
            upRate = ((high - open) / high * 100)
            # upRate = ((high - yesterdayPrice) / high * 100)
            if upRate > maxUp:
                maxUp = upRate

            if (high - open != 0) & (upRate < minUp):
                minUp = upRate

            averageUp += upRate
            if upRate < targetRate:
                countOfLessTarget += 1
            if upRate == 0:
                countZero += 1

        except:
            pass

        downRate = 0
        try:
            downRate = ((low - open) / low * 100)
        except:
            pass

        # if -(worldStockUpRate * 2) - targetRate > fluctuation:
        #     print(f"check: {-(worldStockUpRate * 2)}, {fluctuation}, {targetRate}")
        #     relativeAllCount += 1
        #     if upRate > targetRate:
        #         relativeCount += 1
        #     if upRate < targetRate:
        #         loss = ((close - open) / close * 100)
        #         if loss < 0:
        #             countOfLoss += 1
        #         print(f'fail: {countOfLoss}. {loss}')
        #
        # elif -(worldStockDownRate * 2) + targetRate > fluctuation:
        #     print(f"check: {-(worldStockUpRate * 2)}, {fluctuation}, {targetRate}")
        #     relativeAllCount += 1
        #     if upRate > targetRate:
        #         relativeCount += 1
        #     if upRate < targetRate:
        #         loss = ((close - open) / close * 100)
        #         if loss < 0:
        #             countOfLoss += 1
        #         print(f'fail: {countOfLoss}. {loss}')


        # if worldStockUpRate > (targetRate / 2):
        #     relativeAllCount += 1
        #     if upRate > targetRate:
        #         relativeCount += 1

        relativeAllCount += 1
        if upRate > targetRate:
              relativeCount += 1



        # if upRate < targetRate:
        #     loss = ((close - open) / close * 100)
        #     if loss < 0:
        #         countOfLoss += 1
        #     print(f'fail: {countOfLoss}. {loss}')


        # buyCount = int(seed / open)


        # if worldHigh - worldLow > 100:
        # relativeAllCount += 1
        #
        # if worldStockLargetGap == 'low':
        #     buyAmount = open * buyCount
        #     seed -= buyAmount
        #     rate = ((close - open) / close * 100) if upRate < targetRate else targetRate
        #     returnsPerOne = open + (open / 100 * (rate))
        #     totalReturns = buyCount * returnsPerOne
        #     print(returnsPerOne)
        #     seed += totalReturns
        #     print(seed)
        #
        #     if upRate > targetRate:
        #         relativeCount += 1
        #
        #
        #
        #     else:
        #         loss = ((close - open) / close * 100)
        #         if abs(loss) > 0:
        #             countOfLoss += 1
        #         print(f'fail: {countOfLoss}. {loss}')


            # if worldStockLargetGap == 'low':
            #     if downRate < -targetRate:
            #         relativeCount += 1
            #
            #         buyAmount = open * buyCount
            #         seed -= buyAmount
            #         rate = ((close - open) / close * 100) if downRate > -targetRate else -targetRate
            #         returnsPerOne = open + (open / 100 * rate)
            #         totalReturns = buyCount * returnsPerOne
            #         print(returnsPerOne)
            #         seed += totalReturns
            #         print(seed)
            #
            #     else:
            #         loss = ((close - open) / close * 100)
            #         if abs(loss) > 0:
            #             countOfLoss += 1
            #         print(f'fail: {countOfLoss}. {loss}')








        rateStatus = ""
        if (upRate > 0) & (upRate <= 0.1):
            zeroToPointOne += 1
            rateStatus = "zeroToPointOne"
        elif (upRate > 0.1) & (upRate <= 0.5):
            pointOneToHalf += 1
            rateStatus = "pointOneToHalf"

        elif (upRate > 0.5) & (upRate <= 1):
            halfToOne += 1
            rateStatus = "halfToOne"

        elif upRate > 1:
            moreThanOne += 1
            rateStatus = "moreThanOne"

        else:
            isZero += 1
            rateStatus = "isZero"


        print(rateStatus)



        print(f'date_: {date}, upRate: {upRate}, downRate: {downRate}')
        if fluctuation > 0:
            if fluctuation >= 4:
                status = f"{fluctuation}% 큰폭상승출발"
                upFluctuation += 1
                if high > open:
                    uf_up += 1
                if low < open:
                    uf_down += 1

                if (high > open) == False:
                    print("high fail")

                if (low < open) == False:
                    print("low fail")




            else:
                status = f"{fluctuation}% 상승출발"
                allUp += 1
                if high > open:
                    up_up += 1
                if low < open:
                    up_down += 1


        elif fluctuation < 0:
            if fluctuation < -3:
                status = f"{fluctuation}% 큰폭하락출발"
                downFluctuation += 1
                if high > open:
                    df_up += 1
                if low < open:
                    df_down += 1

                if (high > open) == False:
                    print("high fail")

                if (low < open) == False:
                    print("low fail")


            else:
                status = f"{fluctuation}% 하락출발"
                allDown += 1
                if high > open:
                    down_up += 1
                if low < open:
                    down_down += 1




        else:
            allNone += 1
            if high > open:
                none_up += 1
            if low < open:
                none_down += 1



        print(f'{date}: {status}')
        print(f'yesterday: {yesterdayPrice}, open: {open}, high: {high}, low: {low}, close: {close}, volume: {volume}')
        print(f'yesterday Info: {yesterdayStatus}')
        yesterdayPrice = stock["close"]
        yesterdayStatus = status + f' {100 - (open / close * 100)}' + f' volume: {volume}'


        # buyCount = int(seed / open)
        # if high > open:
        #     buyAmount = open * buyCount
        #     seed -= buyAmount
        #     rate = ((close - open) / close * 100) if upRate < targetRate else targetRate
        #     returnsPerOne = open + (open / 100 * rate)
        #     totalReturns = buyCount * returnsPerOne
        #     print(returnsPerOne)
        #     seed += totalReturns
        #     print(seed)






    print('\n')
    print("Kodex 레버리지 테스트")
    print(f'total days: {allCount}')
    print(f'상승시작장: {allUp}({round(allUp/allCount*100)}%), 하락시작장: {allDown}({round(allDown/allCount*100)}%), 변동없는장: {allNone}({round(allNone/allCount*100)}%)')
    print(f'큰폭 상승출발일때 중간에 더 상승할 확률: {uf_up}/{upFluctuation}({round(uf_up / upFluctuation * 100)}%)')
    print(f'큰폭 상승출발일때 중간에 하락할 확률: {uf_down}/{upFluctuation}({round(uf_down / upFluctuation * 100)}%)')
    print(f'상승출발일때 중간에 더 상승할 확률: {up_up}/{allUp}({round(up_up / allUp * 100)}%)')
    print(f'상승출발일때 중간에 하락할 확률: {up_down}/{allUp}({round(up_down / allUp * 100)}%)')
    print(f'큰폭 하락출발일때 중간에 상승할 확률: {df_up}/{downFluctuation}({round(df_up / downFluctuation * 100)}%)')
    print(f'큰폭 하락출발일때 중간에 더 하락할 확률: {df_down}/{downFluctuation}({round(df_down / downFluctuation * 100)}%)')
    print(f'하락출발일때 중간에 상승할 확률: {down_up}/{allDown}({round(down_up / allDown * 100)}%)')
    print(f'하락출발일때 중간에 더 하락할 확률: {down_down}/{allDown}({round(down_down / allDown * 100)}%)')
    print(f'변동없을때 중간에 상승할 확률: {none_up}/{allNone}({round(none_up / allNone * 100)}%)')
    print(f'변동없을때 중간에 하락할 확률: {none_down}/{allNone}({round(none_down / allNone * 100)}%)')
    print(f'최대상승률:{maxUp}')
    print(f'최소상승률:{minUp}')
    print(f'평균상승률:{averageUp/allCount}')
    print(f'{countOfLessTarget}/{allCount}({round(100-countOfLessTarget/allCount*100)}%)')
    print(f'{countZero}/{allCount}')
    # print(f'volume average: {totalVolume/allCount}')

    # print(f'zeroToPointOne: {zeroToPointOne}, pointOneToHalf: {pointOneToHalf}, halfToOne: {halfToOne}, moreThanOne: {moreThanOne}, isZero: {isZero}')
    print(f'relativeCount: {relativeCount}/{relativeAllCount}({round(relativeCount/relativeAllCount*100)}%) - {allCount}')
