FROM python:3.8
ADD requirements.txt /app/requirements.txt
WORKDIR /app/
RUN pip3 install -r requirements.txt
#RUN apt-get update && apt-get -y install python3-wget python3-simplejson python3-pycurl
COPY single_producer.py single_producer.py
COPY middle_layer_consumer.py middle_layer_consumer.py
COPY middle_prgm_commit.py middle_prgm_commit.py
COPY middle_test_lang.py middle_test_lang.py
COPY final_prgm_commits.py final_prgm_commits.py
COPY final_test_lang.py final_test_lang.py
COPY consumer_final.py consumer_final.py
