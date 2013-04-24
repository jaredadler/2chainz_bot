#!/home2/pilotski/python/bin/python python
# coding: utf-8
import urllib2, HTMLParser, re, time, twitter, random, warnings
import cPickle as pickle
import nltk
#set api keys for the 2 chainz account
api = twitter.Api(consumer_key='xxx',
consumer_secret='xxx',
access_token_key='xxx',
access_token_secret='xxx')
#load tokens of 2 chainz lyrics
chainz = pickle.load(open("PATH-TO-/thug_tokens.p", "rb"))
chainztrainer = nltk.NgramModel(3, chainz)
#randomize the tweet time
time.sleep(random.randint(0,300))
#randomly generate tweet
tweet = " ".join(chainztrainer.generate(random.randint(5,15)))
punctuation = [",", "!", ".", "'", "n't", ":", ";"]
for punct in punctuation:
	tweet = tweet.replace(" " + punct, punct)
api.PostUpdate(tweet)
print "Tweeted: ", tweet
