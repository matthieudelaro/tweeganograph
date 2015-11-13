# This file describs the Cipher class and provides some tests.
# It has been designed for Python 3.X. Please upgrade if you
# are using Python 2.X version.

import Tweet
from Database import *


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

        # todo Matthieu : render tweets as text
        return "list of tweets hidding the message"

    def decode(self, cipherText, key):
        """Decodes a string containing a list of tweets. Returns the decoded
        message."""
        listOfTweets = self._parseTextAsListOfTweets(cipherText, key)
        preprocessedPlainText = self._recoverDataFromTweetsList(listOfTweets, key)
        plainText = self._reversePlainTextPreprocessing(preprocessedPlainText, key)
        return plainText

    def _preprocessPlainText(self, plainText, key):
        """Applies compression algorithm, encode with AES, ...
        The process must be reversible with
        __reversePlainTextPreprocessing(plainText, key)"""
        return plainText  # todo Juyasohn

    def _reversePlainTextPreprocessing(self, preprocessedPlainText, key):
        """Reverses the process of _preprocessPlainText(plainText, key)"""
        return preprocessedPlainText  # todo Juyasohn

    def _selectTweetsListForEncoding(self, preprocessedPlainText, key,
                                     tweetsDatabase):
        """Select and returns a list of tweets that encode the given
        preprocessedPlainText. It selects Tweets among those provided
        by the given tweetsDatabase."""
        return []  # todo Matthieu

    def _parseTextAsListOfTweets(self, text):
        """Parses given text and returns a list of Tweet instances."""
        return []  # todo Matthieu

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
        ppt = "preprocessedPlainText: 101010001110101"
        print(ppt == self._recoverDataFromTweetsList(self._selectTweetsListForEncoding(ppt, key, tweetsDatabase), key))

if __name__ == "__main__":
    c = Cipher()
    c.tests()
