# Data-Engineering2-Group18
#The data flow that should be running from single_producer.py towards different middle layers,
#where each middle layer connects to their final consumer. Things should be running parallely
#to different instances so that you get fast results.
#single_producer.py sends messages to middle_layer_1.py middle_layer_2.py middle_layer_3.py middle_layer_4.py
#and middle_layer_1.py sends to consumer_1.py middle_layer_2.py sends to consumer_2.py etc.


#For question 1
#single_producer sends to middle_layer_consumer to the final_consumer
#For question 2
#single_producer sends to middle_prgm_commit to the final_prgm_consumer
#For question 3
#single_producer sends to middle_test_lang to the final_test_lang
#For question 4 we did not have time to establish the flow properly but the
#planned implementation can be seen in the diagram in the report
