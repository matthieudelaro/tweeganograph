# This file describs the Cipher class and provides some tests.
# It has been designed for Python 3.X. Please upgrade if you
# are using Python 2.X version.

import Tweet
from Database import *
from BitIterator import *


class Cipher:

    def encode(self, plainText, key, topicOfTweets, tweetsDatabase):
        """Returns a string containing a list of tweets encoding the plaintext.
        First it pre-processes the plaintext with compression algorithm and AES
        encryption (this is the usage of the key). Then it selects tweets that
        can convey the pre-processed plaintext, and renders them as text,
        which is returned. Given tweetDatabase contains all the Tweets that
        the cipher can use to encode the given plainText."""
        preprocessedPlainText = self._preprocessPlainText(plainText, key)
        listOfTweets = self._selectTweetsListForEncoding(preprocessedPlainText,
                                                         tweetsDatabase)

        output = ""
        for tweet in listOfTweets:
            output += "%s\n%s\n\n" % (tweet.content, tweet.getUrl())
        return output

    def decode(self, cipherText, key):
        """Decodes a string containing a list of tweets. Returns the decoded
        message."""
        listOfTweets = self._parseTextAsListOfTweets(cipherText, key)
        preprocessedPlainText = self._recoverDataFromTweetsList(listOfTweets, key)
        plainText = self._reversePlainTextPreprocessing(preprocessedPlainText, key)
        return plainText

    def _preprocessPlainText(self, plainText, key):
        """Applies compression algorithm, encode with AES, ... and returns
        bytes. The process must be reversible with
        __reversePlainTextPreprocessing(plainText, key)."""
        # examples about bytes and bytearray: http://www.dotnetperls.com/bytes
        # some crypto module that seems nice: https://pypi.python.org/pypi/pycrypto
        return bytearray(plainText)  # todo Juyasohn.
        # warning : take care of encoding issues (UTF-8, Latin1, ...)

    def _reversePlainTextPreprocessing(self, preprocessedPlainText, key):
        """Reverses the process of _preprocessPlainText(plainText, key) by
        returning a string from the given bytes preprocessedPlainText."""
        return preprocessedPlainText  # todo Juyasohn
        # warning : take care of encoding issues (UTF-8, Latin1, ...)

    def _selectTweetsListForEncoding(self, preprocessedPlainText, key,
                                     tweetsDatabase):
        """Select and returns a list of tweets that encode the given
        preprocessedPlainText. It selects Tweets among those provided
        by the given tweetsDatabase."""
        db = tweetsDatabase
        dim = db.getDimensionOfFeatureVector()
        ppt = BitOver(preprocessedPlainText)
        output = []
        # for it in range(start=0, stop=len(ppt), step=dim):
        it = 0
        finished = False
        while not finished:
            itEnd = it + dim
            featureVector = ppt.getAsInt(slice(it, itEnd))
            quantityOfExtraBits = 0
            # print("it:%d itEnd:%d => %s (%s)" % (it, itEnd, ppt[it:itEnd], featureVector))

            if itEnd < len(ppt):
                it += dim
            else:
                quantityOfExtraBits = itEnd - len(ppt)
                # output.append(db.getTweetWithFeatureVector(ppt.getAsInt(slice(it, itEnd))))
                # print("last:%s" % str(output[-1]))
                finished = True

            tweet = db.getTweetWithFeatureVector(featureVector)
            if not tweet: raise BufferError("Could not find proper tweet for feature %s" % featureVector)
            output.append(tweet)
            if finished:
                tweetEOF = db.getTweetWithFeatureVector(quantityOfExtraBits)
                if not tweetEOF: raise BufferError("Could not find proper tweet for feature %s" % featureVector)
                # print("last feature vector: %s" % ppt[it:itEnd])
                # print("quantityOfExtraBits: %s" % quantityOfExtraBits)
                output.append(tweetEOF)
        # print("len(ppt):%d" % len(ppt))
        return output

    def _parseTextAsListOfTweets(self, text):
        """Parses given text and returns a list of Tweet instances."""
        return []  # todo Stuart

    def _recoverDataFromTweetsList(self, listOfTweets, key):
        """Interprets the given list of Tweets. Returns the data hidden in the
        Tweets. It reverses the process of
        _selectTweetsListForEncoding(preprocessedPlainText, key)"""
        return []  # todo Matthieu

    def tests(self):
        print("Testing Cipher (tests below should all return True):")
        pt = "plainText : Hello World!"
        key = "password"
        print(pt == self._reversePlainTextPreprocessing(self._preprocessPlainText(pt, key), key))

        tweetsDatabase = MockDatabase()
        ppt = bytearray("preprocessedPlainText: 101010001110101")
        print(ppt == self._recoverDataFromTweetsList(self._selectTweetsListForEncoding(ppt, key, tweetsDatabase), key))

if __name__ == "__main__":
    c = Cipher()
    c.tests()
