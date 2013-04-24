# -*- coding: utf-8 -*-
import tweepy
import re
import nltk
from nltk.corpus import PlaintextCorpusReader, brown
import cPickle as pickle
import operator
import random
auth = tweepy.OAuthHandler("xxx", "xxx")
auth.set_access_token("xxx", "xxx")
api = tweepy.API(auth)

directory = "PATH-TO-DIRECTORY"

bandz = pickle.load(open(directory + "thug_tokens.p", "rb"))
thugtrainer = nltk.NgramModel(3, bandz)

corpus_root = directory + "/songs"
chainzcorpus = PlaintextCorpusReader(corpus_root, '.*')

chainzwords = nltk.probability.FreqDist()
for sent in chainzcorpus.sents():
	for word in sent:
		chainzwords.inc(word.lower())
chainzkeys = chainzwords.keys()

brownwords = nltk.probability.FreqDist()
for sent in brown.sents():
	for word in sent:
		brownwords.inc(word.lower())
brownkeys = brownwords.keys()

stopwords = nltk.corpus.stopwords.words('english')

trends_US = api.trends_place(23424977)

trendlist = []
for trend in trends_US[0]['trends']:
    trendlist.append(trend['name'])

trendwords = []
for trend in trendlist:
    if trend.startswith('#'):
        if len(re.findall('[A-Z][^A-Z]*', trend)) > 1:
            trendwords.append((re.findall('[A-Z][^A-Z]*', trend), trend))
        else:
            pass
    else:
        pass

keyrank = {}
for trend in trendwords:
    for word in trend[0]:
		if len(word) < 2:
			pass
		else:
			try:
				keyrank[(word.lower(), trend[1])] = (1 - (chainzkeys.index(word.lower()) / float(len(chainzkeys)))) - (1 - (brownkeys.index(word.lower()) / float(len(brownkeys))))
			except:
				try:
					keyrank[(word, trend[1])] = (1 - (chainzkeys.index(word.lower()) / float(len(chainzkeys))))
				except:
					pass

for k, v in keyrank.items():
    if (k[0] in stopwords):
        del keyrank[k]

top = max(keyrank.iteritems(), key=operator.itemgetter(1))[0]


top = max(keyrank.iteritems(), key=operator.itemgetter(1))[0]
gen_tweet = " ".join(thugtrainer.generate(random.randint(5,15), [top[0]]))
punctuation = [",", "!", ".", "'", "n't", ":", ";"]
for punct in punctuation:
    gen_tweet = gen_tweet.replace(" " + punct, punct)
api.update_status(top[1] + " " + gen_tweet)
print top[1] + " " + gen_tweet
print keyrank
print top
#print "@" + top[2] + " " + gen_tweet, top[1]
#except:
#    print "No useful tokens"
#    pass