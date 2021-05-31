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
from pulsar.schema import *
import pulsar
from collections import defaultdict

#############
# Functions #
#############
TOKEN ="Authorization:token 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"

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

class ProgramContent(Record):
    lang = String()
    url = String()

class TestLanguage(Record):
    lang = String()
    count = Integer()
##Consumer
#client = pulsar.Client('pulsar://localhost:6650')
client = pulsar.Client('pulsar://pulsar:6650')

consumer = client.subscribe('Program_Content',subscription_name='ProgramContentCount', schema=AvroSchema(ProgramContent))

language_test_count = client.create_producer(topic='Language_test_count', schema=AvroSchema(TestLanguage))

program_count = {}
programs = defaultdict(list)
test_langs = {}
waitMsg = True
while waitMsg:
    try:
        msg = consumer.receive(50000)
        ex = msg.value()
        programs[ex.lang].append(ex.url)
        consumer.acknowledge(msg)
    except:
        waitMsg = False
        consumer.negative_acknowledge(msg)

for key, value in programs.items():
    for val in value:
        dataRead = simplejson.loads(getUrl(val))

        boolTest = False

        for item in dataRead:

            if(item.get('name') != None):
                name =item.get('name')
                # print(name)
                name = name.lower()
                if ("test" in name or "suite" in name):
                    booltest = True
                elif ("." in name or 'license' == name):
                    continue
                else:
                    # print(item['_links'])
                    self = item['_links']['self']
                    prevname = ""
                    time.sleep(10)
                    contents = simplejson.loads(getUrl(self))
                    for content in contents:
                        if(content.type() == str):
                            print(content)
                            continue
                        if( content.get('name') != None) :
                            prj_name = content.get('name')
                            prj_name = prj_name.lower()
                            if ("test" in prj_name or "suite" in prj_name):
                                booltest = True
                                break
                            elif ("." in prj_name or 'license' == prj_name):
                                continue
            if(boolTest):
                test_langs[key] = test_langs.get(key, 0) + 1
            time.sleep(10)

for key, value in test_langs.items():
    language_test_count.send(TestLanguage(lang=key, count=value))

client.close()