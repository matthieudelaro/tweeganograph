# This file describs the Cipher class and provides some tests.
# It has been designed for Python 3.5. Please upgrade if you
# are using Python 2.X version.

import unittest
import math
from Tweet import Tweet
from Database import MockDatabase
from BitIterator import BitOver


class Cipher:

    def encode(self, plainText, key, topicOfTweets, tweetsDatabase):
        """Returns a string containing a list of tweets encoding the plaintext.
        First it pre-processes the plaintext with compression algorithm and AES
        encryption (this is the usage of the key). Then it selects tweets that
        can convey the pre-processed plaintext, and renders them as text,
        which is returned. Given tweetDatabase contains all the Tweets that
        the cipher can use to encode the given plainText."""
        preprocessedPlainText = self._preprocessPlainText(plainText, key)
        listOfTweets, listOfBitsPerTweet = self._selectTweetsListForEncoding(preprocessedPlainText,
                                                         tweetsDatabase)

        output = self._generateHeader(topicOfTweets)
        for tweet in listOfTweets:
            output += "\n%s\n%s\n" % (tweet.getContent(), tweet.getUrl())
        return output

    def decode(self, cipherText, key):
        """Decodes a string containing a list of tweets. Returns the decoded
        message."""
        listOfTweets, listOfBitsPerTweet = self._parseTextAsListOfTweets(cipherText)
        preprocessedPlainText = self._recoverDataFromTweetsList(listOfTweets, listOfBitsPerTweet)
        plainText = self._reversePlainTextPreprocessing(preprocessedPlainText, key)
        return plainText

    def _generateHeader(self, topicOfTweets):
        return """Dear customer,
            Click on this link to get a PROMO CODE and earn an Xbox One : http://virus.hack.ch.
            Here is what people say about this great article :

            """

    def _preprocessPlainText(self, plainText, key):
        """Applies compression algorithm, encode with AES, ... and returns
        bytes. The process must be reversible with
        __reversePlainTextPreprocessing(plainText, key)."""
        # examples about bytes and bytearray: http://www.dotnetperls.com/bytes
        # some crypto module that seems nice: https://pypi.python.org/pypi/pycrypto
        return bytearray(plainText, 'UTF-8')  # todo Juyasohn.
        # warning : take care of encoding issues (UTF-8, Latin1, ...)

    def _reversePlainTextPreprocessing(self, preprocessedPlainText, key):
        """Reverses the process of _preprocessPlainText(plainText, key) by
        returning a string from the given bytes preprocessedPlainText."""
        return preprocessedPlainText.decode("UTF-8")  # todo Juyasohn
        # warning : take care of encoding issues (UTF-8, Latin1, ...)

    def _selectTweetsListForEncoding(self, preprocessedPlainText,
                                     tweetsDatabase):
        """Select and returns a list of tweets that encode the given
        preprocessedPlainText, and a list of containing the quantity
        of bits encoded in each tweet. It selects Tweets among those provided
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
        return (output, [dim for i in range(len(output))])

    def _parseTextAsListOfTweets(self, text):
        """Parses given text and returns a list of Tweet instances,
        as well as a list of quantity of bits encoded in each tweet."""
        trsh1 = 1
        trsh2 = 3
        trsh3 = 128
        trsh4 = 16
        tweets = []
        bits = []
        
        lines = text.split('\n')

        flag = 0
        userId = ""
        tweetId = ""
        content = ""
        start = "https://twitter.com/"
        end = "/status/"
        
        
        for line in lines[5:]:
            #print (line)
            if flag ==0:
                content = line
            if flag ==1:
                userId = line[line.index(start)+len(start):line.index(end)]
                tweetId = line[line.rindex("/")+1:]
            flag+= 1
            if flag ==3:
                flag = 0
                tweets.append(Tweet(userId,tweetId,content))
                bits.append(4)
        
        return (tweets,bits)  # todo Stuart

    def _recoverDataFromTweetsList(self, listOfTweets, listOfBitsPerTweet):
        """Interprets the given list of Tweets. Returns the data hidden in the
        Tweets. It reverses the process of
        _selectTweetsListForEncoding(preprocessedPlainText)"""
        tweetQuantity = len(listOfTweets)
        if tweetQuantity != len(listOfBitsPerTweet):
            raise ValueError("Both lists should have the same length")
        totalBitQuantity = 0
        for quantity in listOfBitsPerTweet:
            totalBitQuantity += quantity
        # print(totalBitQuantity - listOfTweets[-1].getFeatureVector())
        # print((totalBitQuantity - listOfTweets[-1].getFeatureVector()) / 8)
        # print(math.ceil((totalBitQuantity - listOfTweets[-1].getFeatureVector()) / 8))
        outputData = bytearray([0] * math.ceil(
            (totalBitQuantity
             - listOfTweets[-1].getFeatureVector()  # the last tweet tells us how much bits from the last but one bit are to be removed
             - listOfBitsPerTweet[-1]) / 8))  # the last tweet does not carry any data
        # print(len(outputData))
        output = BitOver(outputData)
        outputIterator = 0

        lastButTwoData = bytearray([0] * math.ceil(listOfBitsPerTweet[-2] / 8))
        lastButTwo = BitOver(lastButTwoData)
        lastButTwoDimension = 0
        for tweetIndex, (tweet, dimension) in enumerate(zip(listOfTweets, listOfBitsPerTweet)):
            if tweetIndex == tweetQuantity - 1:  # if last tweet
                bitsToDelete = tweet.getFeatureVector()
                # bitsToDelete = output.getAsInt(slice(outputIterator,
                                                     # outputIterator+dimension))
                # print("bitsToDelete: %d" % bitsToDelete)
                # output[outputIterator:outputIterator+bitsToDelete] = []
                output[outputIterator:outputIterator+dimension-bitsToDelete] = featureVector
            else:
                featureVector = tweet.getFeatureVector()
                if tweetIndex == tweetQuantity - 2:  # if last but one tweet
                    lastButTwo[0:dimension] = featureVector
                    lastButTwoDimension = dimension
                else:
                    # print("%d: %d bits in tweet %s" % (tweetIndex, dimension, tweet))
                    # output.writeInt(outputIterator, featureVector, dimension)
                    output[outputIterator:outputIterator+dimension] = featureVector
                    outputIterator += dimension

        return outputData


class TestCipher(unittest.TestCase):
    def setUp(self):
        self.cipher = Cipher()
        self.pt = "plainText : Hello World!"
        self.key = "password"
        self.ppt = bytearray("preprocessedPlainText: 101010001110101", "UTF-8")

    def test_preprocessing(self):
        self.assertEqual(self.pt,
                         self.cipher._reversePlainTextPreprocessing
                         (self.cipher._preprocessPlainText(self.pt, self.key),
                          self.key))

    def test_selectTweetsListForEncoding(self):
        tweetsDatabase = MockDatabase()
        listOfTweets, listOfBitsPerTweet = self.cipher._selectTweetsListForEncoding(self.ppt, tweetsDatabase)
        recoveredData = self.cipher._recoverDataFromTweetsList(listOfTweets, listOfBitsPerTweet)
        self.assertListEqual(BitOver(self.ppt)[:], BitOver(recoveredData)[:])
        self.assertListEqual(BitOver(self.ppt)[-8:], BitOver(recoveredData)[-8:])
        self.assertEqual(self.ppt, recoveredData)

    def test_encodeAndDecode(self):
        pass  # todo

    def test__parseTextAsListOfTweets(self):
        pass  # todo

if __name__ == '__main__':
    unittest.main()
