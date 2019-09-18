import json
import tweepy
import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient

# Authenticate to Twitterc
consumer_key = "hogTh91MFJ2mif1xhrT00vtBg"
consumer_secret = "C2DeqzYMUD46MIGaNDACykogNH1gELamklQnOHJxFSiBBTtFWF"

access_token = "1057427356992778240-IopS39HiToAS975jU3173vT1qpiRNX"
access_secret = "dI6VeH5zmSiu9vrrEsJUFRVdmyFpuS1NAujqnteFzPbmo"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

MONGO_HOST= 'mongodb://localhost/twitterdb'

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print(f"{tweet.user.name}:{tweet.text}")

    def on_error(self, status):
        print("Error detected")

    def getData(self, data):
        try:
            client = MongoClient(MONGO_HOST)
            db = client.twitterdb
            datajson = json.loads(data)
            created_at = datajson['created_at']
            print("Tweet collected at " + str(created_at))
            db.twitter_search.insert(datajson)
        except Exception as e:
           print(e)




def readFromCSV(fileName):
    with open(fileName) as f:
        keywords = f.read().splitlines()
    return keywords

# real time streaming based on keywords
tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
keywords = readFromCSV("/Users/friedahuang/Desktop/XProject/src/tweeterenv/keywords.csv")
stream.filter(track=keywords, languages=["en"])

for i in range(len(keywords)):
    searched_result = api.search(keywords[i], count=1000)
    status = searched_result[0]
    print(status.text)

