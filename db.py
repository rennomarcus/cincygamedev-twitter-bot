from pymongo import MongoClient
from credentials import mongouri


class DbManager():
    def __init__(self, dbName):
        self.client = MongoClient(mongouri)
        self.db = self.client[dbName]

    def insert(self, collection, document):
        self.db[collection].insert_one(document)
        return self

    def find(self, collection, query={}):
        return self.db[collection].find(query)

    def delete(self, collection, id):
        self.db[collection].delete_one({"_id": id})
        return self

    def saveTweet(self, collection, tweet, deserialize=True):
        if deserialize:
            td = TwitterData(tweet)
            self.insert(collection, td.deserialize())
        else:
            self.insert(collection, tweet)

    def getTweets(self):
        return self.find("tweets")

    def getTweet(self, id):
        return self.db["tweets"].find_one({"status_id": id})

    def getMyTweet(self, id):
        return self.db["my_tweets"].find_one({"status_id": id})


class TwitterData():
    def __init__(self, tweet=None):
        self.tweet = tweet

    def deserialize(self):
        if not self.tweet:
            return {}
        tw = self.tweet
        return {
            "status_id": tw.id,
            "text": tw.text,
            "user": tw.user._json,
            "tweet_created_at": tw.created_at,
            "retweet_count": tw.retweet_count,
            "favorite_count": tw.favorite_count
        }

    def __str__(self):
        return self.tweet
