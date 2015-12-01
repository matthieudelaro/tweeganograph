# This file describs the Tweet class and provides some tests.
# It has been designed for Python 3.5. Please upgrade if you
# are using Python 2.X version.

import tweepy

class Tweet:
    """Holds data about a tweet. It can be used to get tweets from Tweeter,
    to store them in some kind of database (serialization of the list of
    tweets ?), to get the features of the tweet to generate the text, ..."""

    def __init__(self, author, id, content,follow,friend,parser,api):
        self._id = id
        #if (id == "670766141728419840" or id == "670766173638819840"):
        #    print (content)
        self._author = author
        self._content = content
        self._friendCount = friend
        self._followerCount = follow
        self.inflateFeaturesFromContent(parser,api)
        
    #def __init__(self,author,id,content,

    def inflateFeaturesFromContent(self,parser,api):
        """Process the content of the tweet to compute some features."""
        self._computeHashtagsCount()
        self._computeMentionsCount()
        if (parser == 1):
            self._computeFriendsFollowers(api)
        self._computeFeaturesVector()
        return self

    def inflateFeaturesFromUrl(self):
        """Request Tweeter.com to get more data about the tweet to compute
        some features."""
        extraDataFromTweeter = self._getDataFromTweeter()
        self._computeLocalization(extraDataFromTweeter)
        # self._compute...(extraDataFromTweeter)
        return self

    def __str__(self):
        return "Tweet %s by %s : %s  +++++++ %s" % (self._id, self._author, self._content,self._featureVector)

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

        self._mentionsCount = self._content.count('@')
        return
       # return self._content.count('@')

    def _computeHashtagsCount(self):

        self._hashtagsCount = self._content.count('#')
        return
        #return self._content.count('#')

    def _computeLocalization(self, extraDataFromTweeter):
        #todo
        pass
    
    def _computeFriendsFollowers(self, api):
                
        
        #s = api.get_user(self._author)
        try:
            t = api.get_status(self._id)
            s = t.user
            self._friendCount = s.friends_count
            self._followerCount = s.followers_count
        except:
            return
        return

    def _computeFeaturesVector(self):
        #trsh1 = 1  # mentions (changing)
        trsh2 = 4  # hashtags
        trsh3 = 130  # content
        trsh4 = 14  # length of author name
        trsh5 = 33 #335 # number of followers
        trsh6 = 33 #315 # number of friends
        index = 0
        

        #if (self._mentionsCount>=trsh1): #using new feature, besides mentions
        #    index += 1
        
        if (self._hashtagsCount>=trsh2):
            index += 2
        if (len(self._content)>=trsh3):
            index += 4
        if (len(self._author)>=trsh4):
            index += 8
        if(int(self._id[7]) %2 ==1): #is 7th digit odd?
            index+= 1
        if((self._followerCount//10)>=trsh5):
            index+=16
        if((self._friendCount//10)>=trsh6):
            index+=32

        self._featureVector = index

    def getFeatureVector(self):
        return self._featureVector


def tests():
    print("Testing Tweet")
    t = Tweet("me", 15, "#I'm #studying at #KAIST!!!")
    print(t.getFeatureVector())

if __name__ == "__main__":
    tests()
