import tweepy, os, time
from random import choice
# coding: utf-8
import urllib2, HTMLParser, re, time, twitter, random, warnings, operator
import cPickle as pickle
import nltk
from nltk.corpus import PlaintextCorpusReader, brown, stopwords

auth = tweepy.OAuthHandler("xxx", "xxx")
auth.set_access_token("xxx", "xxx")
api = tweepy.API(auth)
directory = "PATH-TO-DIRECTORY"
time.sleep(random.randint(0,300))

bandz = pickle.load(open(directory + "thug_tokens.p", "rb"))
thugtrainer = nltk.NgramModel(random.randint(2,3), bandz)

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

timeline = api.home_timeline()
timeline_notchainz = []
for status in timeline:
	if status.user.screen_name == '2chainz_bot':
		pass
	else:
		timeline_notchainz.append(status)

timeline_statuses = [x.text.replace('\n', ' ').lower() for x in timeline_notchainz]
statusdump = open(directory + 'friends_timeline.txt', 'wb')
for status in timeline_statuses:
	statusdump.write(status.encode('utf-8'))
	statusdump.write('\n')
statusdump.close()

status_data = [dict([('id', x.id), ('screen_name', x.user.screen_name)]) for x in timeline_notchainz]

os.system('PATH-TO-/arknlp/runTagger.sh --output-format pretsv PATH-TO-/friends_timeline.txt > PATH-TO-/friends_tagged.txt')
time.sleep(5)
dectweets = open(directory + 'friends_tagged.txt', 'rb').read()
dectweets = dectweets.replace('\n', '\t')
dectweets = dectweets.split('\t')
decchunks = []
for i in range(0, len(dectweets)-3, 4):
	decchunks.append([dectweets[i], dectweets[i+1], dectweets[i+2], dectweets[i+3]])
postokenpairs = [dict(zip(i[0].split(), i[1].split())) for i in decchunks]
pos_with_data = zip(postokenpairs, status_data)
print pos_with_data
#chosen = choice(pos_with_data)
keyrank = {}
for tweet in pos_with_data:
    for k, v in tweet[0].items():
        if (v != 'N') and (v != 'V') and (v != 'A') and (v != '^'):
            pass
        else:
            try:
                keyrank[(k, tweet[1]['id'], tweet[1]['screen_name'])] = (1 - (chainzkeys.index(k) / float(len(chainzkeys)))) - (1 - (brownkeys.index(k) / float(len(brownkeys))))
            except:
				try:
					keyrank[(k, tweet[1]['id'], tweet[1]['screen_name'])] = (1 - (chainzkeys.index(k) / float(len(chainzkeys))))
				except:
					pass
for k, v in keyrank.items():
    if (k[0] in stopwords):
        del keyrank[k]
try:
	top = max(keyrank.iteritems(), key=operator.itemgetter(1))[0]
	gen_tweet = " ".join(thugtrainer.generate(random.randint(5,15), [top[0]]))
	punctuation = [",", "!", ".", "'", "n't", ":", ";"]
	for punct in punctuation:
		gen_tweet = gen_tweet.replace(" " + punct, punct)
	api.update_status("@" + top[2] + " " + gen_tweet, top[1])
	print keyrank
	print top
	#print tweet[1] + " " + gen_tweet, tweet[2]
except:
	print "No useful tokens"
	pass