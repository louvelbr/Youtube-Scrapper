import scrapper
import requests
from bs4 import BeautifulSoup
import re  
import json as json  
from unidecode import unidecode
import sys, getopt

response=requests.get("https://www.youtube.com/watch?v=XbDaHt4QkIg")
soup = BeautifulSoup(response.text,"html.parser")

data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
data_json = json.loads(data) 

def test_getNbLikes():
    assert scrapper.getNbLikes(data_json) == "355 clics"

# def test_getDescriptionAndLinks(data_json):
#     description, list_link = scrapper.getDescriptionAndLinks(data_json)
#     assert list_link == [
#             "http://feeds.bbci.co.uk/news/rss.xml",
#             "https://www.youtube.com/watch?v=7QueV...",
#             "https://www.udemy.com/course/apprendr..."
#         ]