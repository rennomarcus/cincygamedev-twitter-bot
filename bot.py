from credentials import consumer_key, consumer_secret, access_token, \
        access_token_secret
from constants import DB_NAME, HASH_TAGS, MIN_FAVS, MIN_RETWEETS
from pymongo import DESCENDING as DSC
from db import DbManager
import tweepy
import random
import time


# Access and authorize our Twitter credentials from credentials.py
class Bot():
    def __init__(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.db = DbManager(DB_NAME)
        random.seed(time.time())

    # make search based on our favorite hash tags
    def queryTags(self, hash_tags=HASH_TAGS):
        for tag in hash_tags:
            for tweet in tweepy.Cursor(self.api.search, q=tag).items(5):
                self.saveTweet(tweet)

    # save tweets
    def saveTweet(self, tweet):
        # check first if tweet is not in our DB
        if self.db.getTweet(tweet.id):
            return
        self.db.saveTweet("tweets", tweet)

    # create analysis of latests tweets
    def createAnalysis(self):
        pass

    def getGoodTweets(self):
        # for now we are just getting the  latest three tweets we stored
        return self.db.find("tweets", {
                "$or": [
                    {"retweet_count": {"$gte": MIN_RETWEETS}},
                    {"favorite_count": {"$gte": MIN_FAVS}}
                ]
            }).sort("created_at", DSC).limit(3)

    # retweet based on analysis
    def retweet(self):
        print("Retweeting...")
        for tweet in self.getGoodTweets():
            # first we checked if we already retweeted it
            if self.db.getMyTweet(tweet["status_id"]):
                continue
            self.db.saveTweet("my_tweets", tweet, False)
            # sleep for random time before tweeting
            time.sleep(random.randrange(0, 60))
            self.api.retweet(tweet["status_id"])
            print("Retweeted {0}".format(tweet["status_id"]))
