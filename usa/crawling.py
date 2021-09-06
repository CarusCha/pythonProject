import requests
from bs4 import BeautifulSoup


def getHtmlObj(url):
    result = requests.get(url).content
    return BeautifulSoup(result, "html.parser")
