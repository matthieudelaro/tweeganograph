# This file describs the databases classes and provides some tests.
# It has been designed for Python 3.X. Please upgrade if you
# are using Python 2.X version.

import Tweet


class AbstractDatabase:
    def getTweets():
        """Returns Tweets as ... we have to figure out what is best.."""
        pass

    def getTweetWithFeatureVector(featureVector):
        """Returns a Tweet that has the given featureVector,
        or None in case no such Tweet exists."""
        pass


class MockDatabase(AbstractDatabase):
    def getTweets():
        return []  # todo Matthieu

    def getTweetWithFeatureVector(featureVector):
        pass  # todo Matthieu

    def tests(self):
        pass  # todo Matthieu


class TweetsDatabase(AbstractDatabase):
    #  todo Stuart
    #  todo? : def loadFromFile()
    pass


if __name__ == "__main__":
    db = MockDatabase()
    db.tests()
