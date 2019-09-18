from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient

def readFromCSV(fileName):
    with open(fileName) as f:
        keywords = f.read().splitlines()
    return keywords

WORDS = readFromCSV("/Users/friedahuang/Desktop/XProject/src/tweeterenv/keywords.csv")
MONGO_HOST= 'mongodb://localhost/twitterdb' 

CONSUMER_KEY = "hogTh91MFJ2mif1xhrT00vtBg"
CONSUMER_SECRET = "C2DeqzYMUD46MIGaNDACykogNH1gELamklQnOHJxFSiBBTtFWF"
ACCESS_TOKEN = "1057427356992778240-IopS39HiToAS975jU3173vT1qpiRNX"
ACCESS_TOKEN_SECRET = "dI6VeH5zmSiu9vrrEsJUFRVdmyFpuS1NAujqnteFzPbmo"

class StreamListener(tweepy.StreamListener):    
 
    def on_connect(self):
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        try:
            client = MongoClient(MONGO_HOST)
            db = client.twitterdb
            datajson = json.loads(data)
            
            created_at = datajson['created_at']
            print("Tweet collected at " + str(created_at))
            db.twitter_search.insert(datajson)
        except Exception as e:
           print(e)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)

