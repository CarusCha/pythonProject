#-*- coding:utf-8 -*-
from db import dbManager as db


def startToFind(date, name):
    con = db.getConnection("naverStockInfo.db")
    stockData = db.pd.read_sql('SELECT * FROM stockInfo', con, index_col='date').T.to_dict()
    stockDataList = db.json.loads(stockData[date]['infoJson'])
    filteredDataList = []
    keyList = ['name', '시가총액', 'PER', 'PBR', '부채총계', '유보율', '당기순이익', '보통주배당금', '자산총계', '매출액증가율', '배당률', '거래대금']
    for stockData in stockDataList:
        dataDict = {}
        for key in keyList:
            try:
                if key == '배당률':
                    dataDict[key] = round(
                        (float(stockData['보통주배당금'])) / (float(stockData['price'].replace(',', ''))) * 100, 2)
                elif key == 'name':
                    dataDict[key] = stockData[key]
                else:
                    dataDict[key] = (0 if type(stockData[key]) is str else float(stockData[key]))
            except:
                dataDict[key] = 0

        filteredDataList.append(dataDict)


    if name != None:
        filteredDataList = filter(lambda x: x['name'] == name, filteredDataList)

    else:
        filteredDataList = filter(lambda x: x['시가총액'] > 1000, filteredDataList)
        filteredDataList = filter(lambda x: (x['PER'] > 0) & (x['PER'] < 20), filteredDataList)
        filteredDataList = filter(lambda x: x['PBR'] < 1.1, filteredDataList)
        filteredDataList = filter(lambda x: x['시가총액'] < x['자산총계'], filteredDataList)
        filteredDataList = filter(lambda x: x['부채총계'] < x['자산총계'], filteredDataList)
        filteredDataList = filter(lambda x: x['부채총계'] < x['시가총액'], filteredDataList)
        filteredDataList = filter(lambda x: x['유보율'] > 1000, filteredDataList)
        filteredDataList = filter(lambda x: (x['당기순이익'] * 10) > x['시가총액'], filteredDataList)
        # filteredDataList = filter(lambda x: x['거래대금'] < 1000, filteredDataList)

        # filteredDataList = sorted(filteredDataList, key=lambda x: x['거래대금'], reverse=True)
        filteredDataList = sorted(filteredDataList, key=lambda x: x['PER'], reverse=False)



    filteredDataList = list(filteredDataList)
    print(len(filteredDataList))
    for data in filteredDataList:
        print(f'{data["name"]} | PER: {data["PER"]} | PBR: {data["PBR"]} | 자산총계: {data["자산총계"]} | 시가총액: {data["시가총액"]} '
              f'| 부채총계: {data["부채총계"]} | 유보율: {data["유보율"]} | 배당률 {data["배당률"]} | 매출액증가율: {data["매출액증가율"]} | 당기순이익: {data["당기순이익"]} | 배당금: {data["보통주배당금"]} | 거래대금: {data["거래대금"]}')



    # filteredDataList = filter(lambda x: (x['시가총액'] > 1000) &
    #                                     (0 < (-1 if type(x['PER']) is str else float(x['PER'])) < 20)
    #                                     & (0 < (-1 if type(x['PBR']) is str else float(x['PBR'])) < 1.1)
    #                                     & ((((0 if type(x['시가총액']) is str else float(x['시가총액'])) * 1.5) < ( 0 if type(x['자산총계']) is str else float(x['자산총계'])) > ( (0 if type(x['부채총계']) is str else float(x['부채총계'])) * 1)))
    #                                     & (0 < (0 if type(x['유보율']) is str else float(x['유보율'])) > 1000)
    #                                     & ((0 if type(x['부채총계']) is str else float(x['부채총계'])) < (0 if type(x['시가총액']) is str else float(x['시가총액'])))
    #                                     & (0 < (0 if type(x['당기순이익']) is str else float(x['당기순이익']) * 4.5) > ((0 if type(x['시가총액']) is str else float(x['시가총액']))))
    #                           , stockDataList)
    # sortedDataList = sorted(filteredDataList, key=lambda x: x['PBR'], reverse=True)

    # for data in sortedDataList:
    #     print(f'{data["name"]} | PER: {data["PER"]} | PBR: {data["PBR"]} | 자산총계: {data["자산총계"]} | 시가총액: {data["시가총액"]} '
    #           f'| 부채총계: {data["부채총계"]} | 유보율: {data["유보율"]} | 배당률 {data["배당률"]} | 매출액증가율: {data["매출액증가율"]} | 당기순이익: {data["당기순이익"]} | 배당금: {data["보통주배당금"]}')
    # #
    # print(len(list(sortedDataList)))







# unvaluedUnits = UnvaluedUnitsFinder()





# class UnvaluedUnitsFinder:
#     def __init__(self):
#         con = sqlite3.connect("/Users/carus/PycharmProjects/NaverFinance/NaverCrawling/db/NaverStockInfo.db")
#         sqlite3.Connection
#         stockData = pd.read_sql('SELECT * FROM stockInfo', con, index_col='date').T.to_dict()
#         self.stockDataList = json.loads(stockData['20200320']['infoJson'])
#         for stockData in self.stockDataList:
#             dividendRate = 0
#             if ( 0 if type(stockData['보통주배당금']) is str else float(stockData['보통주배당금']) ) != 0:
#                 dividendRate = round((float(stockData['보통주배당금'])) / (float(stockData['price'].replace(',', ''))) * 100, 2)
#             stockData['배당률'] = dividendRate
#
#         print(self.stockDataList[0].keys())
#         filteredDataList = filter(lambda x: (x['시가총액'] > 1000) &
#                                             (0 < (-1 if type(x['PER']) is str else float(x['PER'])) < 15)
#                                             & (0 < (-1 if type(x['PBR']) is str else float(x['PBR'])) < 1)
#                                             & (( ((0 if type(x['시가총액']) is str else float(x['시가총액'])) * 1.5) < (0 if type(x['자산총계']) is str else float(x['자산총계'])) > ((0 if type(x['부채총계']) is str else float(x['부채총계'])) * 1.5) ))
#                                             & (0 < (0 if type(x['유보율']) is str else float(x['유보율'])) > 1000)
#                                             & (0 < (0 if type(x['매출액']) is str else float(x['매출액'])) > ((0 if type(x['시가총액']) is str else float(x['시가총액']))) * 10)
#                                   , self.stockDataList)
#         sortedDataList = sorted(filteredDataList, key=lambda x: x['PBR'], reverse=True)
#         # sortedDataList = sorted(self.stockDataList, key=lambda x: x['시가총액'], reverse=True)
#
#
#         for data in sortedDataList:
#
#             print(f'{data["name"]} | PER: {data["PER"]} | PBR: {data["PBR"]} | 자산총계: {data["자산총계"]} | 시가총액: {data["시가총액"]} '
#                   f'| 부채총계: {data["부채총계"]} | 유보율: {data["유보율"]} | 배당률 {data["배당률"]} | 매출액증가율: {data["매출액증가율"]} | 매출액: {data["매출액"]}')
#
#         print(len(list(sortedDataList)))
#
#
#
#
#
# unvaluedUnits = UnvaluedUnitsFinder()






