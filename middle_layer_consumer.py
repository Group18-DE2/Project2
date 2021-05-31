import pulsar
import pandas as pd
from pulsar.schema import *

class LanguageCount(Record):
    lang = String()
    count = Integer()
# Create a pulsar client by supplying ip address and port
#client = pulsar.Client('pulsar://localhost:6650')
client = pulsar.Client('pulsar://pulsar:6650')
consumer = client.subscribe('Top_lang',subscription_name='LanguageCount', schema=AvroSchema(LanguageCount))

# Create a producer on the topic that consumer can subscribe to
producer = client.create_producer(topic='Languages_1', schema=AvroSchema(LanguageCount))
languages = []
lang_dict = {}
waitingForMsg = True
while waitingForMsg:
    try:
        msg = consumer.receive(50000)
        ex = msg.value()
        languages.append(ex.lang)
        consumer.acknowledge(msg)
    except:
        waitingForMsg = False
        consumer.negative_acknowledge(msg)

for key in languages:
    lang_dict[key] = lang_dict.get(key, 0) + 1

# Send a message to consume len is the length of the input array - Result is the Result og the query which can be aggregated to the consumer
for key, val in lang_dict.items():
    producer.send(LanguageCount(lang=key, count=val))

# Destroy pulsar client
client.close()
