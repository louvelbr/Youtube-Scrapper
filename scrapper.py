#import packages
import requests
from bs4 import BeautifulSoup
import re  
import json as json  
from unidecode import unidecode
import sys, getopt


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
    

def extract_video_informations(url):  
    
    # importer le code de la page
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")

    result = {}  

    result["title"] = soup.find("meta", itemprop="name")['content']  
    result["VideoMaker"] = soup.find("span", itemprop="author").next.next['content'] 

    data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
    data_json = json.loads(data) 

    writeFile("tmp.json", data_json)

    result["likes"] = getNbLikes(data_json)

    result["description"], result["links"] = getDescriptionAndLinks(data_json)

    result["id"] = soup.find("meta", itemprop="videoId")['content'] 

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
    print ('Input file is :', inputFile)
    print ('Output file is :', outputFile)
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
   
