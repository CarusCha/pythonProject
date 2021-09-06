from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import os
from .lib import naverCrawling as nc


path = os.path.dirname(os.path.realpath(__file__))

def getMusicList():
    numList = getMusicNumList()
    musicDictList = []
    driver = webdriver.Chrome(path + '/chromedriver')
    driver.implicitly_wait(3)
    url = "https://www.musicow.com/song/"

    for i, num in enumerate(numList):
        print(i)
        pageUrl = url + num
        driver.get(pageUrl)
        soup = nc.BeautifulSoup(driver.page_source, 'html.parser')
        title = soup.find("strong", {"class": "title"}).text
        artist = soup.find("em", {"class": "artist"}).text

        blueList = soup.find_all("ul", {"class": "blue"})
        if len(blueList) > 0:
            priceInfo = blueList[-1]
            priceList = priceInfo.find_all("span", {"class": ""})
            perList = priceInfo.find_all("span", {"class": "per"})
            unitList = priceInfo.find_all("span", {"class": "unit"})
            price = priceList[-1].text if len(priceList) > 0 else "0"
            per = perList[-1].text if len(perList) > 0 else "0"
            unit = unitList[-1].text if len(unitList) > 0 else "0"

            dict = {'title': f'{artist} / {title}', 'price': price, 'per': per, 'unit': unit}
            musicDictList.append(dict)


    filteredMusicDictList = sorted(musicDictList, key=lambda x: float(x['per'].replace("%", "")) , reverse=True)
    for musicDict in filteredMusicDictList:
        print(f'{musicDict["title"]} - price: {musicDict["price"]} | per: {musicDict["per"]} | unit: {musicDict["unit"]}')

    return musicDictList



def getMusicNumList():
    numList = []
    url = "https://www.musicow.com/auctions?tab=market&keyword=&sortorder=&page="
    page = 1
    while True:
        pageUrl = url + str(page)
        obj = nc.getHtmlObj(pageUrl)
        aList = obj.find_all('a')
        list = []
        for a in aList:
            if 'song' in a.get('href'):
                num = a.get('href').split("/")[-1]
                list.append(num)

        if len(list) == 0:
            break

        numList.extend(list)
        print(page)
        page += 1

    print(len(numList))
    print(numList)



    return numList



# def getMusic():
#     driver = webdriver.Chrome(path + '/chromedriver')
#     driver.get('https://www.musicow.com/song/48')
#     html = driver.page_source
#
#     soup = BeautifulSoup(html, 'html.parser')
#     title = soup.find("strong", {"class":"title"})
#     artist = soup.find("em", {"class": "artist"})
#
#     blueList = soup.find_all("ul", {"class": "blue"})
#     priceInfo = blueList[-1]
#     price = priceInfo.find_all("span", {"class":""})[-1].text
#     per = priceInfo.find_all("span", {"class":"per"})[-1].text
#     unit = priceInfo.find_all("span", {"class":"unit"})[-1].text
#
#     print(f'[{artist} / {title}] price: {price} | per: {per} | unit: {unit}')
