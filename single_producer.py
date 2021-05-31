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
import pulsar
from pulsar.schema import *
from collections import defaultdict

#############
# Constants #
#############

TOKEN ="Authorization:token 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"
URL = f'https://api.github.com/search/repositories?q=created:SINCE..UNTIL&per_page=100'

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

    return(body.decode('iso-8859-1'))


########
# MAIN #
########


#To save the number of repositories processed
since = datetime.today() - timedelta(days=2)  # Since 5 days ago
until = since + timedelta(days=1)   # Until 4 days ago
#To save the number of repositories processed
countOfRepositories = 0

languages = []
commits = {}
content = defaultdict(list)

while until < datetime.today():
    for currentPage in range(1, 2):
        print("page number " + str(currentPage))
        day_url = URL.replace('SINCE', since.strftime('%Y-%m-%dT%H:%M:%SZ')).replace('UNTIL', until.strftime('%Y-%m-%dT%H:%M:%SZ'))
        url = day_url + "&page=" + str(currentPage)
        print("url" + url)
        dataRead = simplejson.loads(getUrl(url))
        #Iteration over all the repositories in the current json content page
        for item in dataRead['items']:
            language = item['language']
            if(language != None):
                languages.append(language)
            countOfRepositories = countOfRepositories + 1
            repo_name = item['name']
            commit_url = item['commits_url']
            content_data = item['contents_url']
            if(repo_name != None and commit_url != None):
                commits[repo_name] = commit_url[:-6]
            if(language != None and repo_name != None and content_data != None):
                content[language].append(content_data[:-8])
     # Update dates for the next search
    since = until
    until = since + timedelta(days=1)
    time.sleep(10)

print("DONE! " + str(countOfRepositories) + " repositories have been processed.")

class LanguageCount(Record):
    lang = String()
    count = Integer()

class ProgramCommit(Record):
    name = String()
    url = String()

class ProgramContent(Record):
    lang = String()
    url = String()

#client = pulsar.Client('pulsar://localhost:6650')
client = pulsar.Client('pulsar://pulsar:6650')
producer = client.create_producer(topic='Top_lang', schema=AvroSchema(LanguageCount))

producer_commit = client.create_producer(topic='Program_Commit', schema=AvroSchema(ProgramCommit))

producer_content = client.create_producer(topic='Program_Content', schema=AvroSchema(ProgramContent))

for lang in languages:
    producer.send(LanguageCount(lang=lang, count=1))

for key, val in commits.items():
    producer_commit.send(ProgramCommit(name=key, url=val))

for key, val in content.items():
    for v in val:
        producer_content.send(ProgramContent(lang=key, url=v))

# When the crawler is finished the client can be stoped
client.close()