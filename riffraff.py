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
tagger_directory = "PATH-TO-ARKNLP-DIRECTORY"
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

rappers = ["@jodyhighroller", "@LILBTHEBASEDGOD", "@FLOSSTRADAMUS", "@dasracist", "@ActionBronson", "@AndyMilonakis", "DOLLABILLGATES", "@THArealVNASTY"]

rrr_info_dirty = []
rrr_info = []
for rapper in rappers:
    rap_chat = api.search(rapper)
    rap_results = [(tweet, tweet.from_user) for tweet in rap_chat]
    for result in rap_results:
        rrr_info_dirty.append(result)

for result in rrr_info_dirty:
    if result[0].text[:4] == "RT @":
        pass
    else:
        rrr_info.append(result)

go_rr = []
try:
    userinfo = api.lookup_users(screen_names = [tweet[1] for tweet in rrr_info])
    for x in userinfo:
        print x.screen_name
        print x.followers_count
        if (x.followers_count < 6000) and (x.followers_count > 200):
            go_rr.append((x.screen_name))
        else:
		print "Skipping ", x.screen_name
except tweepy.error.TweepError or tweepy.TweepError, e:
	print "Error %s" % e

o_names = [tweet[1] for tweet in rrr_info]
rr_tweets = []
for name in o_names:
    if name in go_rr:
        rr_tweets.append(rrr_info[o_names.index(name)])
    else:
        pass

timeline_statuses = [x[0].text.replace('\n', ' ').lower() for x in rr_tweets]
statusdump = open(directory + 'rr_tweets.txt', 'wb')
for status in timeline_statuses:
	statusdump.write(status.encode('utf-8'))
	statusdump.write('\n')
statusdump.close()

status_data = [dict([('id', x[0].id), ('screen_name', x[0].from_user)]) for x in rr_tweets]

os.system(tagger_directory + 'runTagger.sh --output-format pretsv ' + directory + 'rr_tweets.txt > ' + directory + 'rr_tagged.txt')
time.sleep(5)
dectweets = open(directory + 'rr_tagged.txt', 'rb').read()
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
	print "@" + top[2] + " " + gen_tweet, top[1]
	#print tweet[1] + " " + gen_tweet, tweet[2]
except:
	print "No useful tokens"
	pass