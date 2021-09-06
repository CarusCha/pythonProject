import re
import requests
import json
from lxml import etree
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import math
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


ticker = input("Enter Ticker: ")
expectedGrowth = input("Enter Annual Expected Growth Over the Next Decade(e.g. 15%): ")
marginOfSafety = input("Enter Margin of Safety(e.g. 50%): ")
if expectedGrowth == '':
    expectedGrowth = '15%'
if marginOfSafety == '':
    marginOfSafety = '50%'

def getSoup(url, xPATH):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome('/Users/chajonghun/PycharmProjects/pythonProject/NaverCrawling/chromedriver')
    driver.maximize_window()
    driver.implicitly_wait(20)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    element_present = EC.presence_of_element_located((By.XPATH, xPATH))
    WebDriverWait(driver, 5).until(element_present)

    driver.close()
    return soup




# STEP 1: Get EPS TTM
def getEPSTTM():
    print("getEPSTTM...")
    ##################################################
    ### Get EPS TTM
    soup = getSoup(f'https://www.wsj.com/market-data/quotes/{ticker}', '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/ul/li[2]/div/span')
    objList = soup.find_all("li",{"class","WSJTheme--cr_data_row--2h_M996h"})
    filteredList = list(filter(lambda x: "EPS" in x.getText(), objList))
    if len(filteredList) == 0:
        return None

    epsObj = filteredList[0].find("span",{"class":"WSJTheme--data_data--3CZkJ3RI"})
    epsStr = float(epsObj.getText().replace('$','').replace(',', ''))
    return epsStr


# STEP 2: Get Growth Rate
def growthRate(current, initial, age):
    print("growthRate...")
    x = math.log(age, 2) # log2(8) = 3
    # (age) square root of (current/initial) - 1 is (growth)
    # ** 0.5 == 2 squared
    growth = ((current/initial) ** (0.5**x)) - 1
    return growth


def getBookValueGrowthRate():
    print("getBookValueGrowthRate...")
    ##################################################
    ### Get Full Key Ratios Data Url
    # soup = getSoup(f'https://www.morningstar.com/stocks/xnas/{ticker}/quote', '//*[@id="__layout"]/div/div[2]/div[3]/main/div[2]/div/div/div[1]/sal-components/section/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div[1]/a')
    # objList = soup.find_all('a',{'class','mds-link ng-binding'})
    # filteredList = list(filter(lambda x: x.get('href') != None, objList))
    # if len(filteredList) == 0:
    #     return None


    ##################################################
    ### Get Book Value Per Share List
    # href = filteredList[0].get('href')
    # soup = getSoup('https:' + href, '//*[@id="i8"]')
    soup = getSoup(f'http://financials.morningstar.com/ratios/r.html?t={ticker}', '//*[@id="financials"]/table')
    financialTable = soup.find('table',{'class','r_table1 text2'}).find('tbody')

    objList = []
    for tr in financialTable.find_all('tr'):
        if tr.find('th',{'class','row_lbl'}) != None:
            objList.append(tr)

    filteredList = []
    for obj in objList:
        if "Book Value Per Share" in obj.getText():
            filteredList.append(obj)

    # objList = list(filter(lambda x: x.find('th',{'class','row_lbl'}) != None, soup.find_all('tr')))
    # filteredList = list(filter(lambda x: "Book Value Per Share" in x.getText(), objList))
    if len(filteredList) == 0:
        return None
    bookValueList = filteredList[0].find_all('td')

    filteredBookValueList = []
    for bookVal in bookValueList:
        if re.match(r'^-?\d+(?:\.\d+)$', bookVal.getText()) != None:
            filteredBookValueList.append(bookVal)

    # filteredBookValueList = list(filter(lambda x: re.match(r'^-?\d+(?:\.\d+)$', x.getText()) != None, bookValueList))
    if len(filteredBookValueList) < 3:
        return None



    current = float(filteredBookValueList[-2].getText())
    initial = float(filteredBookValueList[0].getText())
    age = len(filteredBookValueList) - 2

    ##################################################
    ### Get Growth Rate From Book Value Per Share List
    rate = growthRate(current, initial, age)
    return rate




def getTotalEquityGrowthRate():
    print("getTotalEquityGrowthRate...")
    ##################################################
    ### Get Total Equity List
    soup = getSoup(f'https://www.wsj.com/market-data/quotes/{ticker}/financials/annual/balance-sheet', '//*[@id="cr_cashflow"]/div[3]/div[2]/table/tbody/tr[55]/td[1]')
    tableList = soup.find_all('table',{'class','cr_dataTable'})

    objList = []
    for table in tableList:
        if 'Total Equity' in table.getText():
            trList = table.find('tbody').find_all('tr')
            for tr in trList:
                if 'Total Equity' in tr.getText():
                    objList = tr.find_all('td',{'class',''})

    filteredList = []
    for obj in objList:
        numberStr = obj.getText().replace(',', '')
        if (numberStr.isnumeric()):
            filteredList.append(float(numberStr))

    if len(filteredList) < 2:
        return None

    current = filteredList[0]
    initial = filteredList[-1]
    age = len(filteredList) - 1

    ##################################################
    ### Get Growth Rate From Total Equity List
    rate = growthRate(current, initial, age)
    return rate



def getFinalGrowthRate():
    print("getFinalGrowthRate...")
    ##################################################
    ### Get Growth Rate From Yahoo
    soup = getSoup(f'https://finance.yahoo.com/quote/FB/analysis?p={ticker}', '//*[@id="Col1-0-AnalystLeafPage-Proxy"]/section/table[6]/tbody/tr[5]/td[2]')
    trList = soup.find_all('tr',{'class','BdT Bdc($seperatorColor)'})

    for tr in trList:
        if 'Next 5 Years' in tr.getText():
            tdList = tr.find_all('td')
            for td in tdList:
                numberStr = td.getText().replace('%','')
                # if (numberStr.isnumeric()):
                if re.match(r'^-?\d+(?:\.\d+)$', numberStr) != None:
                    return float(numberStr)


def getLowestGrowthRate():
    print("getLowestGrowthRate...")
    bookValueGR = getBookValueGrowthRate()
    totalEquityGR = getTotalEquityGrowthRate()
    finalGR = getFinalGrowthRate()
    return min(bookValueGR, totalEquityGR, finalGR)



def getFuturePERatio(lowestGrowthRate):
    print("getFuturePERatio...")

    # soup = getSoup(f'https://www.bing.com/search?q={ticker}+stock', '//*[@id="tab_2"]/div[2]/div/div/div/p')
    # buttonList = soup.find_all('a', {'class','rb_btnLink'})
    # url = ''
    # for button in buttonList:
    #     if button.find('span').find('input', {'value', 'Analysis'}) != None:
    #         print(button['href'])


    # driver = webdriver.Chrome('/Users/chajonghun/PycharmProjects/pythonProject/NaverCrawling/chromedriver')
    # driver.maximize_window()
    # driver.implicitly_wait(20)
    # driver.get('https://www.msn.com/en-us/money/')
    # element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="searchBox"]/input'))
    # WebDriverWait(driver, 5).until(element_present)
    #
    # element = driver.find_element_by_class_name('autoSuggest_commonv2-DS-EntryPoint1-1')
    # element.send_keys('FB')
    # driver.implicitly_wait(10)
    # element.send_keys(Keys.RETURN)
    #
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[5]/div/div/div[1]/div/div[2]/div[2]/div/div/a[3]'))
    # WebDriverWait(driver, 5).until(element_present)

    print("https://www.msn.com/en-us/money/ -> Search stocks -> Analysis -> PRICE RATIOS")
    per5YearsHigh = input("Enter P/E Ratio 5-Year High: ")
    per5YearsLow = input("Enter P/E Ratio 5-Year Low: ")
    average = (float(per5YearsHigh) + float(per5YearsLow)) / 2
    doubleGR = lowestGrowthRate * 200

    return min(average, doubleGR)



def getTenYearsEPS(EPSTTM, grothRate):
    print("getTenYearsEPS...")
    tenYearsEPS = EPSTTM*pow(1+grothRate,10)
    print(tenYearsEPS)
    return tenYearsEPS



def calculate():
    EPSTTM = getEPSTTM()
    print(f'EPS TTM: {EPSTTM}')
    growthRate = getLowestGrowthRate()
    print(f'Lowest Growth Rate: {growthRate}')
    futurePER = getFuturePERatio(growthRate)
    print(f'Future PE Ratio: {futurePER}')
    tenYearsEPS = getTenYearsEPS(EPSTTM, growthRate)
    print(f'10 Years EPS: {tenYearsEPS}')
    sharePriceTenYears = futurePER * tenYearsEPS
    print(f'Future Stock Value: {sharePriceTenYears}')

    eg = float(expectedGrowth.replace('%', '')) / 100
    mos = float(marginOfSafety.replace('%', '')) / 100
    stockValue = sharePriceTenYears / (pow(1+eg,10)) * mos

    print(f'Current Implied Price: {stockValue}')
    return stockValue


calculate()