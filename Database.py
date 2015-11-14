# This file describs the databases classes and provides some tests.
# It has been designed for Python 3.X. Please upgrade if you
# are using Python 2.X version.

import unittest
from Tweet import Tweet


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
    dimensionOfFeatureVector = 3
    defaultQuantityOfTweetsPerFeatureVector = 10

    def __init__(self):
        self._dimensionOfFeatureVector = MockDatabase.defaultQuantityOfTweetsPerFeatureVector
        self._tweets = [[]
                        for featureVector
                        in range(2**MockDatabase.dimensionOfFeatureVector)]

        for featureVector in range(len(self._tweets)):
            self._tweets[featureVector] = [Tweet("pseudo%s_%s" % (featureVector, x), "id%s_%s" % (featureVector, x), "Hello content %s_%s" % (featureVector, x)) for x in range(MockDatabase.defaultQuantityOfTweetsPerFeatureVector)]
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


class TweetsDatabase(AbstractDatabase):
    #  todo Stuart
    #  todo? : methods to load tweets from file, ...
    pass


class TestMockDatabase(unittest.TestCase):
    def setUp(self):
        self.db = MockDatabase()

    def test_counters(self):
        for featureVector in range(2**MockDatabase.dimensionOfFeatureVector):
            for i in range(MockDatabase.defaultQuantityOfTweetsPerFeatureVector):
                self.assertIsInstance(self.db.getTweetWithFeatureVector(featureVector),
                                      Tweet)
            self.assertIsNone(self.db.getTweetWithFeatureVector(featureVector))

        self.db.resetTweetUsageCounters()
        for featureVector in range(2**MockDatabase.dimensionOfFeatureVector):
            for i in range(MockDatabase.defaultQuantityOfTweetsPerFeatureVector):
                self.assertIsInstance(self.db.getTweetWithFeatureVector(featureVector),
                                      Tweet)
            self.assertIsNone(self.db.getTweetWithFeatureVector(featureVector))


if __name__ == '__main__':
    unittest.main()
