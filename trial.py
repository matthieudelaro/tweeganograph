import tweepy
import csv

consumer_key = 'wsjOTj954n9aLO7KKrKVvX0ah'
consumer_secret = 'Dk4JzqEQDhfiKpUMmlOjDQvIXX4hpHBDaf2GwLmxZWWHPVklcg'
access_token = '3475513752-OcILSytFVDPoYOK0sXaaFQPxob5VqpCkeXPxLCw'
access_token_secret = 'y38aiyE0VD4Rr9D8ZL5l7sIAr1CyipoqsRkM1CRts3jO0'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
print(api.me().name)
user = api.get_user('obama') # any name of twitter account
print('--------------------------')
print('User Object')
print(user.id, user.name, user.friends_count, user.location,user.screen_name)
print (user)
print('--------------------------')
print('--------------------------')
print('Status Object')
mytimeline = api.user_timeline('xbox')
# for tweet in mytimeline:
    # print(tweet)
    # print (tweet.id, tweet.text)
print ('--------------------------')

#print (tweet.mentions)
srch = api.get_status(667523538945863681)
#print (srch.entities)

#srch =tweepy.Cursor( api.search,q ='#xbox', lang = 'en').items(2500)

csvFile = open('xbox5.csv', 'a')
# Use csv Writer
csvWriter = csv.writer(csvFile)
#x = 0
#    s = i.text
#    n = i.user.screen_name
#    csvWriter.writerow(['**'+str(i.id), str(n.encode('UTF-8')), str(s.encode('UTF-8')), s.count('@'), s.count('#'), len(s)])
#    x+=1

#x = 0
#for i in srch:
    #s = i.text
    #n = i.user.name
    #csvWriter.writerow(['**'+str(i.id),n.encode('utf-8'),s.encode('utf-8'),s.count('@'),s.count('#'),len(s)])
    #x+=1

#srch =tweepy.Cursor( api.search,q ='#iPhone', lang = 'en').items(180)
#for i in srch:
    #s = i.text
    #n = i.user.name
    #csvWriter.writerow(['**'+str(i.id),n.encode('utf-8'),s.encode('utf-8'),s.count('@'),s.count('#'),len(s)])
    #x+=1

#srch =tweepy.Cursor( api.search,q ='#Xperia', lang = 'en').items(180)
#for i in srch:
    #s = i.text
    #n = i.user.name
    #csvWriter.writerow(['**'+str(i.id),n.encode('utf-8'),s.encode('utf-8'),s.count('@'),s.count('#'),len(s)])
    #x+=1

#srch =tweepy.Cursor( api.search,q ='#Windows Surface', lang = 'en').items(180)
#for i in srch:
    #s = i.text
    #n = i.user.name
    #csvWriter.writerow(['**'+str(i.id),n.encode('utf-8'),s.encode('utf-8'),s.count('@'),s.count('#'),len(s)])
    #x+=1

#srch =tweepy.Cursor( api.search,q ='#Nvidia', lang = 'en').items(180)
#for i in srch:
    #s = i.text
    #n = i.user.name
    #csvWriter.writerow(['**'+str(i.id),n.encode('utf-8'),s.encode('utf-8'),s.count('@'),s.count('#'),len(s)])
    #x+=1

#srch =tweepy.Cursor( api.search,q ='#Samsung', lang = 'en').items(100)
#for i in srch:
    #s = i.text
    #n = i.user.name
    #csvWriter.writerow(['**'+str(i.id),n.encode('utf-8'),s.encode('utf-8'),s.count('@'),s.count('#'),len(s)])
    #x+=1
#srch =tweepy.Cursor( api.search,q ='#Sony', lang = 'en').items(100)
#for i in srch:
    #s = i.text
    #n = i.user.name
    #csvWriter.writerow(['**'+str(i.id),n.encode('utf-8'),s.encode('utf-8'),s.count('@'),s.count('#'),len(s)])
    #x+=1

#csvFile.close()
#print (x)

#srch =tweepy.Cursor( api.search,q ='#iPhone', lang = 'en').items(180)
#
#print(srch)
#
#x =0
#
#for s in srch:
#    x+=1
#    print(s.text)
#print(x)
