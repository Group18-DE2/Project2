
# This script allows to crawl information and repositories from GitHub using the GitHub REST API (https://developer.github.com/v3/search/).
#
# For each query, GitHub returns a json file which is processed by this script to get information about repositories.
#
# The GitHub API limits the queries to get 100 elements per page and up to 1,000 elements in total.
# To get more than 1,000 elements, the main query should be splitted by number of days
#


#############
# Libraries #
#############
import wget
import time
import simplejson
import pycurl
import math
import csv
from io import BytesIO
import requests
from datetime import datetime, timedelta

#############
# Constants #
#############

TOKEN ="Authorization:token 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"
URL = f'https://api.github.com/search/repositories?q=created:SINCE..UNTIL&per_page=100'
OUTPUT_FOLDER = "/zips" #Folder where ZIP files will be stored
OUTPUT_CSV_FILE = "languages.csv" #Path to the CSV file generated as output

#############
# Functions #
#############
def getUrl (url):

    ''' Given a URL it returns its body '''
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(pycurl.HTTPHEADER, [TOKEN])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()

    print(body.decode('iso-8859-1'))
    return(body.decode('iso-8859-1'))


########
# MAIN #
########

#To save the number of repositories processed
since = datetime.today() - timedelta(days=30)  # Since 30 days ago
until = since + timedelta(days=1)   # Until 29 days ago 
#To save the number of repositories processed
countOfRepositories = 0

#Output CSV file which will contain information about repositories
csvfile = open(OUTPUT_CSV_FILE, 'w')
languages_count = csv.writer(csvfile, delimiter=',')

while until < datetime.today():
     for currentPage in range(1, 11):
         print("page number " + str(currentPage))
         day_url = URL.replace('SINCE', since.strftime('%Y-%m-%dT%H:%M:%SZ')).replace('UNTIL', until.strftime('%Y-%m-%dT%H:%M:%SZ'))
         url = day_url + "&page=" + str(currentPage)                                                           
         dataRead = simplejson.loads(getUrl(url))
         #Iteration over all the repositories in the current json content page
         for item in dataRead['items']:
             language = [item['language']
             if(language != None): 
                 languages_count.writerow(, 1])
             countOfRepositories = countOfRepositories + 1
     # Update dates for the next search
     since = until
     until = since + timedelta(days=1)
     time.sleep(10)

print("DONE! " + str(countOfRepositories) + " repositories have been processed.")
csvfile.close()