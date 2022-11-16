#import packages
import requests
from bs4 import BeautifulSoup
import re  
import json as json  
from unidecode import unidecode
import sys, getopt

import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

nbComments = 10

def getComments(url):
    acc = 0
    comments = []
    with Chrome() as driver:
        wait = WebDriverWait(driver,10)
        driver.get(url)

        for item in range(3): #by increasing the highest range you can get more content
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(3)

        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
            if acc < nbComments:
                comments.append(comment.text)
                acc += 1
            else:
                break
    return comments


dict = {}

def readFile(inputFile):
    # Opening JSON file
    f = open(inputFile)
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    return data

def writeFile(outputFile, dict):
    # Write the initial json object (list of dicts)
    with open(outputFile, mode='w',encoding='utf8') as f:
        json.dump(dict, f, ensure_ascii=False)

def getNbLikes(data_json):
    videoPrimaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']  

     # number of likes  
    likes_label = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']# "No likes" or "###,### likes"  

    likes_str = likes_label.split(' ')[0].replace(',','')  

    return '0' if likes_str == 'No' else unidecode(likes_str)

def getDescriptionAndLinks(data_json):
    dict_tmp = data_json['contents']["twoColumnWatchNextResults"]["results"]["results"]["contents"][1]["videoSecondaryInfoRenderer"]["description"]["runs"]

    res = ''
    list_link = []
    for i in range(len(dict_tmp)):

        if 'text' in dict_tmp[i].keys():

            res += dict_tmp[i]['text']
            
            if "http" in dict_tmp[i]['text']:
                list_link.append(dict_tmp[i]['text'])
    return res, list_link
    
def getDataFromVideo(url):
    # import code from page
    response=requests.get(url)
    return BeautifulSoup(response.text,"html.parser")

def getTitle(soup):
    return soup.find("meta", itemprop="name")['content'] 

def getVideoMaker(soup):
    return soup.find("span", itemprop="author").next.next['content'] 

def getId(soup):
    return soup.find("meta", itemprop="videoId")['content'] 

def extract_video_informations(url):  
    
    soup = getDataFromVideo(url)

    result = {}  

    result["title"] =  getTitle(soup)
    result["videoMaker"] = getVideoMaker(soup)

    data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
    data_json = json.loads(data) 

    result["likes"] = getNbLikes(data_json)

    result["description"], result["links"] = getDescriptionAndLinks(data_json)

    result["id"] = getId(soup)
    result["comments"] = getComments(url)

    return(result)




def readArguments(argv):
    inputFile = ''
    outputFile = ''
    try:
        options, args = getopt.getopt(argv,"hi:o:",["input=","output="])
    except getopt.GetoptError:
        print ('scrapper.py --input <inputfile> --output <outputfile>')
        sys.exit(2)
    for opt, arg in options:
        if opt == '-h':
            print ('scrapper.py --input <inputfile> --output <outputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputFile = arg
        elif opt in ("-o", "--output"):
            outputFile = arg
    return inputFile, outputFile

if __name__ == "__main__":
    inputFile, outputFile =  readArguments(sys.argv[1:])

    data = readFile(inputFile)

    # Iterating through the json
    # list
    for id in data['videos_id']:
        dict_result = extract_video_informations("https://www.youtube.com/watch?v="+id)
        dict[id] = dict_result

    writeFile(outputFile, dict)
   
