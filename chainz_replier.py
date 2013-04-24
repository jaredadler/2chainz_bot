import tweepy, os, time
# coding: utf-8
import urllib2, HTMLParser, re, time, twitter, random, warnings, operator
from BeautifulSoup import BeautifulSoup
import cPickle as pickle
import nltk
from nltk.corpus import PlaintextCorpusReader, brown

auth = tweepy.OAuthHandler("xxx", "xxx")
auth.set_access_token("xxx", "xxx")
api = tweepy.API(auth)

directory = "PATH-TO-DIRECTORY"
tagger_directory = "PATH-TO-ARKNLP-DIRECTORY"

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

mention_hist = open(directory + 'mention_hist.p', 'rb')
mention_history = pickle.load(mention_hist)
mention_hist.close()
mentions = api.mentions_timeline()
unmentioned = [i for i in mentions if i.id not in mention_history]
statusdump = open(directory + 'unmentioned_tweets.txt', 'wb')
unmentioned_statuses = ["@" + x.user.screen_name + " " + str(x.id) + " " + x.text.replace('\n', ' ').lower() for x in unmentioned]
for status in unmentioned_statuses:
	statusdump.write(status.encode('utf-8'))
	statusdump.write('\n')
statusdump.close()
for tweet in unmentioned:
	mention_history.append(int(tweet.id))
pickle.dump(mention_history, open(directory + 'mention_hist.p', 'wb'))

os.system(tagger_directory + 'runTagger.sh --output-format pretsv ' + directory +'unmentioned_tweets.txt > ' + directory + 'unmentioned_tagged.txt')
time.sleep(5)
dectweets = open(directory + 'unmentioned_tagged.txt', 'rb').read()
dectweets = dectweets.replace('\n', '\t')
dectweets = dectweets.split('\t')
decchunks = []
for i in range(0, len(dectweets)-3, 4):
	decchunks.append([dectweets[i], dectweets[i+1], dectweets[i+2], dectweets[i+3]])
postokenpairs = [[dict(zip(i[0].split(), i[1].split())), i[0].split()[0], i[0].split()[1], i[3]] for i in decchunks]
for tweet in postokenpairs:
	keyrank = {}
	for k, v in tweet[0].items():
		if (v != 'N') and (v != 'V') and (v != 'A') and (v != '^'):
			del tweet[0][k]
		else:
			try:
				keyrank[k] = (1 - (chainzkeys.index(k) / float(len(chainzkeys)))) - (1 - (brownkeys.index(k) / float(len(brownkeys))))
			except:
				try:
					keyrank[k] = (1 - (chainzkeys.index(k) / float(len(chainzkeys))))
				except:
					pass
	for k, v in keyrank.items():
		if (k in stopwords):
			del keyrank[k]
	try:
		top = max(keyrank.iteritems(), key=operator.itemgetter(1))[0]
		gen_tweet = " ".join(thugtrainer.generate(random.randint(5,15), [top]))
		punctuation = [",", "!", ".", "'", "n't", ":", ";"]
		for punct in punctuation:
			gen_tweet = gen_tweet.replace(" " + punct, punct)
		api.update_status(tweet[1] + " " + gen_tweet, tweet[2])
		print keyrank
		print top
		print tweet[1] + " " + gen_tweet, tweet[2]
	except:
		print "No useful tokens"
		pass
			
	