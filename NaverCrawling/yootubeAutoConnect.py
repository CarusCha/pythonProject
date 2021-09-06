from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os

# path = os.path.dirname(os.path.realpath(__file__))
# driver = webdriver.Chrome(path + '/chromedriver')
# driver.implicitly_wait(3)
# url = 'https://www.youtube.com/channel/UCdlJ_IHHqtzV289zeQcqNaw'
# url = 'https://www.youtube.com/watch?v=jU76P1uIoN0'
# driver.get(url)

# page = driver.page_source
# soup = BeautifulSoup(page, "html.parser")
# all_videos = soup.find_all(id='dismissable')
# liveVideo = all_videos[0]
# isLiveVideo = "live" in str(liveVideo.find('img', {'class':'style-scope yt-img-shadow'}).get('src'))
# if (isLiveVideo):

# print(soup)


import requests

def getHtmlObj(url):
    result = requests.get(url).content
    return BeautifulSoup(result, "html.parser")


newUrl = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0"
obj = getHtmlObj(newUrl)

print(obj)


