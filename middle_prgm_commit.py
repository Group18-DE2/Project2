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

#############
# Functions #
#############

def getUrl (url):

    ''' Given a URL it returns its body '''
    buffer = BytesIO()

    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()

    return(body.decode('iso-8859-1'))

########
# MAIN #
########

class ProgramCommit(Record):
    name = String()
    url = String()

class ProgramCommitCount(Record):
    name = String()
    count = Integer()
##Consumer
#client = pulsar.Client('pulsar://localhost:6650')
client = pulsar.Client('pulsar://pulsar:6650')

consumer = client.subscribe('Program_Commit',subscription_name='Question_2', schema=AvroSchema(ProgramCommit))

producer_commit_count = client.create_producer(topic='Program_Commit_count', schema=AvroSchema(ProgramCommitCount))

program_count = {}
question2dict = {}
waitMsg = True
while waitMsg:
    try:
        msg = consumer.receive(50000)
        ex = msg.value()
        question2dict[ex.name] =  ex.url
        consumer.acknowledge(msg)
    except:
        waitMsg = False
        consumer.negative_acknowledge(msg)

for key, value in question2dict.items():
    dataRead = simplejson.loads(getUrl(value))

    program_count[key] = program_count.get(key, 0) + len(dataRead)

for key, value in program_count.items():
    producer_commit_count.send(ProgramCommitCount(name=key, count=value))

client.close()