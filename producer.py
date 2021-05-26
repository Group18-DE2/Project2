import pulsar
# Create a pulsar client by supplying ip address and port
client = pulsar.Client('pulsar://localhost:6650')

# Create a producer on the topic that consumer can subscribe to
producer = client.create_producer('TopLanguages2.1')

# Send a message to consume len is the length of the input array - Result is the Result og the query which can be aggre>for i in range(len):
    producer.send((Result).encode('utf-8'))

# Destroy pulsar client
client.close()
