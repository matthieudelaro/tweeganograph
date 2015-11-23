# This file describs the Tweet class and provides some tests.
# It has been designed for Python 3.5. Please upgrade if you
# are using Python 2.X version.


class Tweet:
    """Holds data about a tweet. It can be used to get tweets from Tweeter,
    to store them in some kind of database (serialization of the list of
    tweets ?), to get the features of the tweet to generate the text, ..."""

    def __init__(self, author, id, content):
        self._id = id
        self._author = author
        self._content = content
        

    def inflateFeaturesFromContent(self):
        """Process the content of the tweet to compute some features."""
        self._computeHashtagsCount()
        self._computeMentionsCount()
        return self

    def inflateFeaturesFromUrl(self):
        """Request Tweeter.com to get more data about the tweet to compute
        some features."""
        extraDataFromTweeter = self._getDataFromTweeter()
        self._computeLocalization(extraDataFromTweeter)
        # self._compute...(extraDataFromTweeter)
        return self

    def __str__(self):
        return "Tweet %s by %s : %s" % (self._id, self._author, self._content)

    # simple getters/setters
    def getUrl(self):
        return "https://twitter.com/%s/status/%s" % (self._author, self._id)

    def getId(self):
        return self._id

    def getAuthor(self):
        return self._author

    def getMentionsCount(self):
        return self._mentionsCount

    def getHashtagsCount(self):
        return self._hashtagsCount

    def getContent(self):
        return self._content

    def getLocationAsGeoCode(self):
        pass  # todo

    # private methods computing features
    def _computeMentionsCount(self):
        
        #self._mentionsCount = self._content.count('@')
        return self._content.count('@')

    def _computeHashtagsCount(self):
        
        #self._hashtagsCount = self._content.count('#')
        return self._content.count('#')

    def _computeLocalization(self, extraDataFromTweeter):
        #todo
        pass

    def getFeatureVector(self):
        trsh1 = 1
        trsh2 = 3
        trsh3 = 128
        trsh4 = 16
        index = 0
        

        if (self._computeMentionsCount()>=trsh1):
            index += 1
        if (self._computeHashtagsCount()>=trsh2):
            index += 2
        if (len(self._content)>=trsh3):
            index += 4
        if (len(self._author)>=trsh4):
            index += 8
        
        #index =feat1 + 2*feat2+4*feat3+8*feat4
        return index
        #return self._featureVector


def tests():
    print("Testing Tweet")
    t = Tweet("me", 15, "I'm studying at KAIST!!!")
    print(t)

if __name__ == "__main__":
    tests()
