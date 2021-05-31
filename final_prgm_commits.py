import pulsar
import time
import pandas as pd
import operator
from pulsar.schema import *
import matplotlib.pyplot as plt

class ProgramCommitCount(Record):
    name = String()
    count = Integer()

#client = pulsar.Client('pulsar://localhost:6650')
client = pulsar.Client('pulsar://pulsar:6650')
# Subscribe to a topic and subscription
consumer = client.subscribe(topic='Program_Commit_count', subscription_name='program_commit_count', schema=AvroSchema(ProgramCommitCount))

prgm_dict = {}
waitingForMsg = True

while waitingForMsg:
    try:
        msg = consumer.receive(50000)
        ex = msg.value()
        prgm_dict[ex.name] = prgm_dict.get(ex.name, 0) + ex.count
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