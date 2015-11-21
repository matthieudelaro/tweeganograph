import csv
import random
from Tweet import Tweet

class TweetDatabase:
    def loadTweets():
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
        features = []
        for f in range(16):
            features.append([])
        #print(features)
        
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
            
            index = feat1 + 2*feat2+4*feat3+8*feat4
            
            #features[index].append(row)
            tw =Tweet(row[1],row[0],row[2])
            features[index].append(tw)
            x+=1
            #print(x)
            #print (row,feat4,feat3,feat2,feat1)
            if (x>=2500):
                break
        #print (x)
        #for f in features:
        #    print (len(f))
        return features

    def getTweetWithFeatureVector(feat4,feat3,feat2,feat1,features):
        """Returns a Tweet that has the given featureVector,
        or None in case no such Tweet exists, or if all existing tweets
        with this feature vector have already been used."""
        #Input is the binary representation of the feature (1s or 0s)
        # as well as the features list extracted in loadTweets
        #Selection is based on random selection within the index.
        #A new selection method can be implemented to ensure no repretition
        # however with a fairly large data pool, this is sufficient for now.
        
        index = feat1 + 2*feat2+4*feat3+8*feat4
        out = features[index]
        index = int(random.random()*len(out))
        #print()
        #print (index)
        return out[index]

    def getDimensionOfFeatureVector(self):
        """Returns the dimension of the feature vectors used for the tweets
        in the database."""
        #For now it is assumed that all features will be used, currently 4.
        #This can be changed once further features are extracted, and/or
        # dynamic feature usage is implemented.
        return 4

    def resetTweetUsageCounters(self):
        """Reset counters about which kind of tweets have been used."""
        #currently no implementation
        pass
    
##Testing statements
#out = TweetDatabase.loadTweets()
#print()
#print(len(out))
#print(TweetDatabase.getTweetWithFeatureVector(1,1,0,1,out))