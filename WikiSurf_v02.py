######################################################################################
#       Tutorial 2 Belen's scrapWiki & other small Functions trimmed and changed !!  #
######################################################################################
from bs4 import BeautifulSoup
import requests
import re
import operator
import json
from tabulate import tabulate
import sys
from stop_words import get_stop_words
import random
import numpy as np
import urllib
import csv

scrappedSites = []

#saving 
def saveScrappedData(rows_to_save):
    with open("output.csv", "a",newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows_to_save)

def clearScrappedDataFile():
    f = open("output.csv", "w+")
    f.close()
        
#get the words
def getWordList(url):
    word_list = []
    #raw data
    source_code = requests.get(url)
    #convert to text
    plain_text = source_code.text
    #lxml format
    soup = BeautifulSoup(plain_text, 'lxml')

    #find the words in paragraph tag
    for text in soup.findAll('p'):
        if text.text is None:
            continue
        #content
        content = text.text
        #lowercase and split into an array
        words = content.lower().split()

        #for each word
        for word in words:
            #remove non-chars
            cleaned_word = clean_word(word)
            #if there is still something there
            if len(cleaned_word) > 0:
                #add it to our word list
                word_list.append(cleaned_word)

    return word_list


#clean word with regex
def clean_word(word):
    cleaned_word = re.sub('[^A-Za-z]+', '', word)
    return cleaned_word


def createFrquencyTable(word_list):
    #word count
    never_count = 0
    word_count = {}
    for word in word_list:
        #index is the word
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count


#remove stop words
def remove_stop_words(frequency_list):
    stop_words = get_stop_words('en')

    temp_list = []
    for key, value in frequency_list:
        if key not in stop_words:
            temp_list.append([key, value])

    return temp_list


##############################################################################################################
def scrapWiki(search_word, search_modeFlag, target_word, printing):
    #access wiki API. json format. query it for data. search tyep. shows list of possibilities
    wikipedia_api_link = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
    wikipedia_link = "https://en.wikipedia.org/wiki/"
    percentage_value_targeted = 0;
    nextWord = search_word
    
    #if the search word is too small, throw error
    if (len(search_word) < 2):
        print("Enter valid string")
        return None, search_word

    #get the search word
    string_query = search_word

    #to remove stop words or not
    if (len(search_modeFlag) > 2):
        search_mode = True
    else:
        search_mode = False

    #create our URL
    url = wikipedia_api_link + string_query
    
    #try-except block. simple way to deal with exceptions
    #great for HTTP requests
    try:
        #use requests to retrieve raw data from wiki API URL we
        #just constructed
        response = requests.get(url)

        #format that data as a JSON dictionary
        data = json.loads(response.content.decode("utf-8"))

        #page title, first option
        #show this in web browser
        if data['query']['search'][1]['title'] == string_query:
            wikipedia_page_tag = data['query']['search'][1]['title']
        else:
            wikipedia_page_tag = data['query']['search'][0]['title']

        #get actual wiki page based on retrieved title
        url = wikipedia_link + string_query
        print("##################################")
        print("Scrapped URL " + url)
        
        #get list of words from that page
        page_word_list = getWordList(url)
            
        #create table of word counts, dictionary
        page_word_count = createFrquencyTable(page_word_list)
        #sort the table by the frequency count
        sorted_word_frequency_list = sorted(
            page_word_count.items(), key=operator.itemgetter(1), reverse=True)
        #remove stop words if the user specified
        if (search_mode):
            sorted_word_frequency_list = remove_stop_words(
                sorted_word_frequency_list)

        #sum the total words to calculate frequencies
        total_words_sum = 0
        
        for key, value in sorted_word_frequency_list:
            total_words_sum = total_words_sum + value
 
        #create our final list which contains words, frequency (word count), percentage
        final_list = []
        j=0
        for key, value in sorted_word_frequency_list:
            percentage_value = float(value * 100) / total_words_sum
            final_list.append([key, value, round(percentage_value, 4)])
            if key == target_word:
                percentage_value_targeted = percentage_value
                j+=1
        nextWord = key
        scrappedSites.append([time.ctime(),url,str(percentage_value_targeted), str(j)])
        print(scrappedSites)
        saveScrappedData(scrappedSites)
        print('targeted word FREQ:  ' + str(percentage_value_targeted), "\tTimes that it appeared: ",j)
        print("##################################")
	
        
    #throw an exception in case it breaks
    except requests.exceptions.Timeout:
        print("The server didn't respond. This word has no page.")
        return None, search_word
    return percentage_value_targeted
 ###############################################################################################################       









##########################################################################
#    NIKOOOOOOOOOOOOOOOOOOOOOOOOOS's  crawler with gaaaaaaaaaap          #
#    using Belen's scrapppppppppppperrrrrrrrrrrrrrrr                     #
##########################################################################






##########################################################################
#    MEDITERRANEAN WIKIPEDIA SURFER                                      #
#    SURFING THE NET !!!!!                                               #
##########################################################################



from urllib.request import urlopen
import time

#set prefered population and sample size
population=1000
sample=100


GAP = population/sample
GAPcounter=GAP #it reduces on each jump, until you reach a correct article. then it is reset to GAP +/- a coefficient from -1 to 1 (or -1 to 2 if we want it to have the tedency to raise)
#First page (seed):
NextLink="/wiki/Screen_Actors_Guild_Award_for_Outstanding_Performance_by_a_Cast_in_a_Motion_Picture"


#clear 
allLinks=[]
clearScrappedDataFile()


#and lets go!!
i=0
sum=scrapWiki(NextLink[6:], "Yes", "human", True)  #keep a sum of the frequencies :)
while (i<population):
    html = urlopen("http://en.wikipedia.org/"+NextLink)
    bsObj = BeautifulSoup(html, "html.parser")
    currentList=[]
    # save all links that start with /wiki/ and after that do not contain any colons 
    for link in bsObj.find("div", {"id":"bodyContent"}).findAll( "a", href=re.compile("^(/wiki/)((?!:).)*$") ):
        
       # if 'href' in link.attrs:
        currentLink=str(link.attrs['href'])
        if currentLink not in currentList:
            allLinks.append(currentLink)
            
        currentList.append(currentLink)
       
    # choose the next jump
    NextList=[]
    falseWhenNextListIsNotEmpty=True
    
    linkFreqInAllLinks=1
    while (falseWhenNextListIsNotEmpty):
        
        for link in currentList :
            
            if allLinks.count(link)==linkFreqInAllLinks:
                #print("link:",link,"\n freq",allLinks.count(link))
                NextList.append(link)
                falseWhenNextListIsNotEmpty=False
        
        linkFreqInAllLinks+=1 # if the for loop above finished and didnt find freq=1 in the allLinks list, raise the accepted freq

    NextLink=random.choice(NextList)
    print("jumped this:",NextLink)

    GAPcounter-=1
    i+=1
    print("\t#No of article:",i,"#\t",GAPcounter," more until the next Freq", "#\t#freq level of NextList links in AllList:",linkFreqInAllLinks-1)
    print("\t#All links parsed::",len(allLinks),"#\t")

    if (GAPcounter==0):
        sum+=scrapWiki(NextLink[6:], "Yes", "human", True)
        GAPcounter=GAP+random.randint(-1,1)
        


    
    
            

