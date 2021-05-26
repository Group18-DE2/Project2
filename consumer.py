import pulsar
#import _pulsar
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://localhost:6650')
# Subscribe to a topic and subscription
consumer = client.subscribe('Top_languages', subscription_name='TopLanguages2.1')
#consumer = client.subscribe('Top_updated_projects', subscription_name='TopLanguages2.2')
#consumer = client.subscribe('Top_unit_test', subscription_name='TopLanguages2.3')
#consumer = client.subscribe('Top_ci_cd', subscription_name='TopLanguages2.4')
# Display message received from producer

while True:
        msg = consumer.receive()
except:
        consumer.negative_acknowledge(msg)

msg = msg.data()

languages = set(msg)
top=[]
#Create language-Count list
for i in languages:
        res=msg.count(i)
        top.append((i,res))
top= pd.DataFrame(data=top,columns=('Languages','Counts')).sort_values(by=['Counts'],ascending=False)
print(top[:10])
# Destroy pulsar client
client.close()
