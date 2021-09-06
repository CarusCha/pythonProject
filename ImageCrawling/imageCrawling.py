import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, urlretrieve
from requests_html import HTMLSession
from selenium import webdriver
import time
import requests

path = os.path.dirname(os.path.realpath(__file__))


def generateDirectory(directoryName):
    try:
        if not (os.path.isdir(directoryName)):
            os.makedirs(os.path.join(directoryName))
    except OSError as e:
        print("Directory Error")
        return;


def getLimitImage(url, filename, directoryName):
    html = urlopen(url)
    soup = bs(html, "html.parser")
    imgList = soup.find_all("img")
    generateDirectory(directoryName)

    for i, img in enumerate(imgList):
        src = img.get("src")
        filetype = ".png" if ('png' in src) else ".jpg"
        imgUrl = src.split(f'{filetype}?')[0] + filetype
        urlretrieve(imgUrl, f"./{directoryName}/" + filename + f"_{i}{filetype}")



def getAllImage(url, filename, directoryName):

    driver = webdriver.Chrome(path + '/chromedriver')
    driver.implicitly_wait(3)
    driver.get(url)
    time.sleep(5)
    html = driver.page_source

    # html = urlopen(url)
    soup = bs(html, "html.parser")
    imgList = soup.find_all("img")
    generateDirectory(directoryName)

    for i, img in enumerate(imgList):
        src = img.get("src")
        imgUrl = None

        if ((('https' in src) == False) & (('http' in src) == False)) :
            src = img.get("data-src")
            if (src is None) == False:
                imgUrl = src
                img_data = requests.get(imgUrl).content
                with open(f"./{directoryName}/" + filename + f"_{i}" + ".png", 'wb') as handler:
                    handler.write(img_data)


        else:
            filetype = ".png" if ('png' in src) else ".jpg"
            imgUrl = src.split(f'{filetype}?')[0]
            if (filetype in imgUrl) == False:
                imgUrl = imgUrl + filetype

            print(imgUrl)
            # urlretrieve(imgUrl, f"./{directoryName}/" + filename + f"_{i}{filetype}")
            img_data = requests.get(imgUrl).content
            with open(f"./{directoryName}/" + filename + f"_{i}{filetype}", 'wb') as handler:
                handler.write(img_data)



def getNikeImage(filename, directoryName):
    generateDirectory(directoryName)
    i = 1;
    while i < 20:
        imgUrl = f'https://static.nike.com.hk/resources/product/{filename}/{filename}_BL{i}.png'
        response = requests.get(imgUrl)
        if response.status_code == 404:
            break
        img_data = response.content
        with open(f"./{directoryName}/" + filename + f"_{i}.png", 'wb') as handler:
            handler.write(img_data)

        i += 1;


def getNikeImageList(filenameList):
    for filename in filenameList:
        directoryName = f"./nike/{filename}/"
        RDirectoryName = f"./nike/R/"
        generateDirectory(directoryName)
        generateDirectory(RDirectoryName)

        i = 1;
        while i < 20:
            imgUrl = f'https://static.nike.com.hk/resources/product/{filename}/{filename}_BL{i}.png'
            response = requests.get(imgUrl)
            if response.status_code == 404:
                break
            img_data = response.content
            with open(directoryName + filename + f"_{i}.png", 'wb') as handler:
                handler.write(img_data)
            if i == 1:
                with open(RDirectoryName + filename + f"_{i}.png", 'wb') as handler:
                    handler.write(img_data)

            i += 1;


# CJ6314-006,CD3476-401,CD3476-400,CD3476-100,CD3476-003,AT3160-800,AT3160-001,DD8505-181,DA8736-101,DA8736-100,CU5691-600,CT1973-800,CT1973-004,CT1973-003,CV0978-600,CV0973-600,CV0843-600,CV8481-101,CV8481-100,CV7564-600,CW5344-100,CW3146-100,CW3146-001,CV8485-100,DC1746-103,DC1746-102,CT1983-103,CT1983-102,CT1983-101,CK6647-800,CV8821-501,CV8817-600,CV8817-001,DD8506-881,DC4467-400,DC4467-100,CJ6314-010,CJ6741-100,CJ6741-003,CT1933-500,CV8482-600,CV8482-100,CW3155-600,CZ1055-100,394053-101
# nikeList = ['CV0032-605'];
# getNikeImageList(nikeList);

# getNikeImage('CV0032-605', 'nike/CV0032-605')

getAllImage("https://smartstore.naver.com/everywherefood/products/2644248311", '세모수_어리굴젓', 'food/세모수_어리굴젓')