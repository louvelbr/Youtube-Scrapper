import scrapper
import requests
from bs4 import BeautifulSoup
import re  
import json as json  
import validators

response=requests.get("https://www.youtube.com/watch?v=XbDaHt4QkIg")
soup = BeautifulSoup(response.text,"html.parser")

data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
data_json = json.loads(data) 

def test_getNbLikes():
    assert scrapper.getNbLikes(data_json) == "355 clics"

def test_getTitle():
    assert scrapper.getTitle(soup) == "Apprendre le Web Scrapping avec Python et BeautifulSoup"

def test_getVideoMaker():
    assert scrapper.getVideoMaker(soup) == "FORMASYS"

def test_getId():
    assert scrapper.getId(soup) == "XbDaHt4QkIg"

def test_description():
    descritption, links = scrapper.getDescriptionAndLinks(data_json)
    assert isinstance(descritption, str)

def test_links():
    descritption, links = scrapper.getDescriptionAndLinks(data_json)
    assert all([validators.url(link) for link in links])

def test_is_extract_video_informations_not_null():
    assert scrapper.extract_video_informations("https://www.youtube.com/watch?v=XbDaHt4QkIg") != ''

def test_readFile():
    assert scrapper.readFile('input.json') != ''
