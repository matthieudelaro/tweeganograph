import tweepy
consumer_key = 'wsjOTj954n9aLO7KKrKVvX0ah'
consumer_secret = 'Dk4JzqEQDhfiKpUMmlOjDQvIXX4hpHBDaf2GwLmxZWWHPVklcg'
access_token = '3475513752-OcILSytFVDPoYOK0sXaaFQPxob5VqpCkeXPxLCw'
access_token_secret = 'y38aiyE0VD4Rr9D8ZL5l7sIAr1CyipoqsRkM1CRts3jO0'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
print(api.me().name)
user = api.get_user('gsct') # any name of twitter account
print('--------------------------')
print('User Object')
print(user.id, user.name, user.friends_count, user.location)
print('--------------------------')
print('--------------------------')
print('Status Object')
mytimeline = api.user_timeline('gsct')
for tweet in mytimeline:
    print (tweet.id, tweet.text)
print ('--------------------------')

srch = api.search('sony')
print (srch)