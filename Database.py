# This file describs the databases classes and provides some tests.
# It has been designed for Python 3.5. Please upgrade if you
# are using Python 2.X version.

import unittest
from Tweet import Tweet
import tweepy
import csv


class AbstractDatabase:
    def getTweets(self):
        """Returns Tweets as ... we have to figure out what is best.."""
        pass

    def getTweetWithFeatureVector(self, featureVector):
        """Returns a Tweet that has the given featureVector,
        or None in case no such Tweet exists, or if all existing tweets
        with this feature vector have already been used."""
        pass

    def getDimensionOfFeatureVector(self):
        """Returns the dimension of the feature vectors used for the tweets
        in the database."""
        pass

    def resetTweetUsageCounters(self):
        """Reset counters about which kind of tweets have been used."""
        pass


class MockDatabase(AbstractDatabase):
    defaultDimensionOfFeatureVector = 3
    defaultQuantityOfTweetsPerFeatureVector = 50

    def __init__(self):
        self._dimensionOfFeatureVector = MockDatabase.defaultDimensionOfFeatureVector
        self._tweets = [[]
                        for featureVector
                        in range(2**self._dimensionOfFeatureVector)]

        for featureVector in range(len(self._tweets)):
            self._tweets[featureVector] = [Tweet("pseudo%s_%s" % (featureVector, x), "id%s_%s" % (featureVector, x), "Hello content %s_%s" % (featureVector, x)) for x in range(MockDatabase.defaultQuantityOfTweetsPerFeatureVector)]

            # featureVectorByteArray = bytearray(Math.ceil(self._dimensionOfFeatureVector / 8))
            # featureVectorBitOver = BitOver(featureVectorByteArray)
            # featureVectorBitOver.writeInt(0, featureVector)
            for tweet in self._tweets[featureVector]:
                # tweet._featureVector = featureVectorBitOver
                tweet._featureVector = featureVector
        self.resetTweetUsageCounters()

    def resetTweetUsageCounters(self):
        self._tweetUsageCounters = [0 for featureVector in range(len(self._tweets))]

    def getTweets(self):
        return self._tweets

    def getTweetWithFeatureVector(self, featureVector):
        if self._tweets[featureVector]:
            if len(self._tweets[featureVector]) > self._tweetUsageCounters[featureVector]:
                tweet = self._tweets[featureVector][self._tweetUsageCounters[featureVector]]
                self._tweetUsageCounters[featureVector] += 1
                return tweet
        return None

    def getDimensionOfFeatureVector(self):
        return self._dimensionOfFeatureVector


class TweetDatabase(AbstractDatabase):
    defaultDimensionOfFeatureVector = 4
    defaultQuantityOfTweetsPerFeatureVector = 50

    def __init__(self):
        self._dimensionOfFeatureVector = TweetDatabase.defaultDimensionOfFeatureVector
        self._tweets = [[]
                        for featureVector
                        in range(2**self._dimensionOfFeatureVector)]
        self.loadTweets()

        #for featureVector in range(len(self._tweets)):
        #    self._tweets[featureVector] = [Tweet("pseudo%s_%s" % (featureVector, x), "id%s_%s" % (featureVector, x), "Hello content %s_%s" % (featureVector, x)) for x in range(MockDatabase.defaultQuantityOfTweetsPerFeatureVector)]

            # featureVectorByteArray = bytearray(Math.ceil(self._dimensionOfFeatureVector / 8))
            # featureVectorBitOver = BitOver(featureVectorByteArray)
            # featureVectorBitOver.writeInt(0, featureVector)
        #    for tweet in self._tweets[featureVector]:
                # tweet._featureVector = featureVectorBitOver
        #        tweet._featureVector = featureVector
        self.resetTweetUsageCounters()

    def resetTweetUsageCounters(self):
        self._tweetUsageCounters = [0 for featureVector in range(len(self._tweets))]

    def getTweets(self):
        return self._tweets

    def getTweetWithFeatureVector(self, featureVector):
        if self._tweets[featureVector]:
            if len(self._tweets[featureVector]) > self._tweetUsageCounters[featureVector]:
                tweet = self._tweets[featureVector][self._tweetUsageCounters[featureVector]]
                self._tweetUsageCounters[featureVector] += 1
                return tweet
        return None

    def getDimensionOfFeatureVector(self):
        return self._dimensionOfFeatureVector

    def loadTweets(self):
            """Returns Tweets as ... we have to figure out what is best.."""
            #Returns nested list of the tweets with the features as the index
            #Index is calculated as hexadecimal value of the 4 features.
            #The feature order is [length of Author name, length of tweet,
            # number of hashtags, number of mentions] where a 1 or 0 is set
            # based on a comparison to some predefined thresholds (trsh1-4)
            #returns features to be used in later methods.
            trsh1 = 1
            trsh2 = 3
            trsh3 = 128
            trsh4 = 16
            #features = []
            #self.tweets
            #for f in range(16):
            #    features.append([])

            csvFile = open('xboxData.csv')
            reader = csv.reader(csvFile)
            x = 0
            for row in reader:
                feat1 = 0
                feat2 = 0
                feat3 = 0
                feat4 = 0

                if (int(row[3])>=trsh1):
                    feat1 = 1
                if (int(row[4])>=trsh2):
                    feat2 = 1
                if (int(row[5])>=trsh3):
                    feat3 = 1
                if (int(row[6])>=trsh4):
                    feat4 = 1

                index = feat1 + 2*feat2 + 4*feat3 + 8*feat4

                tw =Tweet(row[1],row[0][2:],row[2])
                tw._featureVector = index
                self._tweets[index].append(tw)
                x+=1
                if (x>=2500):
                    return
            return
            #return features


class TweetsDatabase(AbstractDatabase):
    #  todo Stuart
    #  todo? : methods to load tweets from file, ...
    pass


class TestMockDatabase(unittest.TestCase):
    def setUp(self):
        self.db = MockDatabase()

    def test_counters(self):
        for featureVector in range(2**self.db.getDimensionOfFeatureVector()):
            for i in range(MockDatabase.defaultQuantityOfTweetsPerFeatureVector):
                self.assertIsInstance(self.db.getTweetWithFeatureVector(featureVector),
                                      Tweet)
            self.assertIsNone(self.db.getTweetWithFeatureVector(featureVector))

        self.db.resetTweetUsageCounters()
        for featureVector in range(2**self.db.getDimensionOfFeatureVector()):
            for i in range(MockDatabase.defaultQuantityOfTweetsPerFeatureVector):
                self.assertIsInstance(self.db.getTweetWithFeatureVector(featureVector),
                                      Tweet)
            self.assertIsNone(self.db.getTweetWithFeatureVector(featureVector))


class TestTweetDatabase(unittest.TestCase):
    def setUp(self):
        self.db = TweetDatabase()

    def test_counters(self):
        pass


if __name__ == '__main__':
    unittest.main()
