import pulsar
import time
import pandas as pd
import pulsar
import pandas as pd
import operator
from pulsar.schema import *
import matplotlib.pyplot as plt

class LanguageCount(Record):
    lang = String()
    count = Integer()
    
# Create a pulsar client by supplying ip address and port
#client = pulsar.Client('pulsar://localhost:6650')
client = pulsar.Client('pulsar://pulsar:6650')

# Subscribe to a topic and subscription
consumer = client.subscribe(topic='Languages_1', subscription_name='Question_1', schema=AvroSchema(LanguageCount))

lang_dict = {}
waitingForMsg = True
while waitingForMsg:
    try:
        msg = consumer.receive(50000)
        ex = msg.value()
        lang_dict[ex.lang] = lang_dict.get(ex.lang, 0) + ex.count
        consumer.acknowledge(msg)
    except:
        waitingForMsg = False
        consumer.negative_acknowledge(msg)

sorted_d = dict(sorted(prgm_dict.items(), key=operator.itemgetter(1), reverse = True)[:10])
print(sorted_d)
names = list(sorted_d.keys())
values = list(sorted_d.values())

plt.bar(range(len(sorted_d)), values, tick_label=names)
plt.show()

# Destroy pulsar client
client.close()
