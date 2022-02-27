FROM python:3.8

RUN apt-get update
RUN apt-get install -y mecab libmecab-dev mecab-ipadic-utf8
#RUN git clone https://github.com/neologd/mecab-ipadic-neologd.git
#WORKDIR /mecab-ipadic-neologd
#RUN bin/install-mecab-ipadic-neologd

RUN pip install tweepy mecab-python3==0.996.5 markovify schedule



COPY . /app

WORKDIR /app

CMD ["python3","tweet.py"]