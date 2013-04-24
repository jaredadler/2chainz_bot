# coding: utf-8
import urllib2, HTMLParser, re, time, twitter, random, warnings
#from eautifulSoup import BeautifulSoup
import cPickle as pickle
import nltk
"""
thuglyrics = []
allthug = ['http://www.rapgenius.com/2-chainz-im-different-lyrics',
	'http://www.rapgenius.com/2-chainz-birthday-song-lyrics',
	'http://www.rapgenius.com/2-chainz-no-lie-lyrics',
	'http://www.rapgenius.com/Juicy-j-bandz-a-make-her-dance-remix-lyrics',
	'http://www.rapgenius.com/2-chainz-2-chainz-sway-in-the-morning-freestyle-lyrics',
	'http://www.rapgenius.com/2-chainz-addicted-to-rubberbands-lyrics',
	'http://www.rapgenius.com/Juicy-j-bandz-a-make-her-dance-remix-lyrics',
	'http://www.rapgenius.com/2-chainz-birthday-song-lyrics',
	'http://www.rapgenius.com/2-chainz-boo-lyrics',
	'http://www.rapgenius.com/2-chainz-call-tiesha-lyrics',
	'http://www.rapgenius.com/2-chainz-cant-do-it-like-me-lyrics',
	'http://www.rapgenius.com/Curren-y-capitol-lyrics',
	'http://www.rapgenius.com/2-chainz-countdown-lyrics',
	'http://www.rapgenius.com/2-chainz-crack-lyrics',
	'http://www.rapgenius.com/2-chainz-dirty-dark-lyrics',
	'http://www.rapgenius.com/2-chainz-dope-peddler-lyrics',
	'http://www.rapgenius.com/Kirko-bangz-drank-in-my-cup-remix-lyrics',
	'http://www.rapgenius.com/2-chainz-extremely-blessed-lyrics',
	'http://www.rapgenius.com/2-chainz-feeling-you-lyrics',
	'http://www.rapgenius.com/Asap-rocky-fuckin-problems-lyrics',
	'http://www.rapgenius.com/2-chainz-fuk-da-roof-lyrics',
	'http://www.rapgenius.com/2-chainz-gasolean-lyrics',
	'http://www.rapgenius.com/Gucci-mane-get-it-back-lyrics',
	'http://www.rapgenius.com/2-chainz-get-it-in-lyrics',
	'http://www.rapgenius.com/2-chainz-ghetto-dreams-lyrics',
	'http://www.rapgenius.com/Wale-globetrotter-lyrics',
	'http://www.rapgenius.com/2-chainz-good-morning-lyrics',
	'http://www.rapgenius.com/2-chainz-got-one-lyrics',
	'http://www.rapgenius.com/Waka-flocka-flame-hood-rich-lyrics',
	'http://www.rapgenius.com/2-pistols-i-dont-care-lyrics',
	'http://www.rapgenius.com/2-chainz-i-feel-good-lyrics',
	'http://www.rapgenius.com/2-chainz-i-got-it-lyrics',
	'http://www.rapgenius.com/2-chainz-i-luv-dem-strippers-lyrics',
	'http://www.rapgenius.com/2-chainz-in-town-lyrics',
	'http://www.rapgenius.com/Wiz-khalifa-its-nothin-lyrics',
	'http://www.rapgenius.com/2-chainz-ko-lyrics',
	'http://www.rapgenius.com/2-chainz-letter-to-da-rap-game-lyrics',
	'http://www.rapgenius.com/Roscoe-dash-like-diz-lyrics',
	'http://www.rapgenius.com/2-chainz-like-me-lyrics',
	'http://www.rapgenius.com/French-montana-marble-floors-lyrics',
	'http://www.rapgenius.com/Ti-loud-mouth-lyrics',
	'http://www.rapgenius.com/2-chainz-money-machine-lyrics',
	'http://www.rapgenius.com/Big-krit-money-on-the-floor-lyrics',
	'http://www.rapgenius.com/2-chainz-murder-lyrics',
	'http://www.rapgenius.com/Gucci-mane-okay-with-me-lyrics',
	'http://www.rapgenius.com/Bob-perfect-symmetry-lyrics',
	'http://www.rapgenius.com/2-chainz-pimp-c-back-lyrics',
	'http://www.rapgenius.com/Lil-wayne-rich-as-fuck-lyrics',
	'http://www.rapgenius.com/2-chainz-riot-lyrics',
	'http://www.rapgenius.com/Rick-ross-spend-it-remix-lyrics',
	'http://www.rapgenius.com/2-chainz-stop-me-now-lyrics',
	'http://www.rapgenius.com/Meek-mill-str8-like-dat-lyrics',
	'http://www.rapgenius.com/2-chainz-stunt-lyrics',
	'http://www.rapgenius.com/E-40-they-point-lyrics',
	'http://www.rapgenius.com/2-chainz-think-about-it-lyrics',
	'http://www.rapgenius.com/2-chainz-too-easy-lyrics',
	'http://www.rapgenius.com/2-chainz-turnt-up-freestyle-lyrics',
	'http://www.rapgenius.com/2-chainz-twilight-zone-lyrics',
	'http://www.rapgenius.com/2-chainz-undastatement-lyrics',
	'http://www.rapgenius.com/2-chainz-up-in-smoke-lyrics',
	'http://www.rapgenius.com/2-chainz-vi-agra-lyrics',
	'http://www.rapgenius.com/2-chainz-wut-we-doin-lyrics',
	'http://www.rapgenius.com/David-banner-yao-ming-lyrics',
	'http://www.rapgenius.com/2-chainz-yuck-lyrics',
	'http://www.rapgenius.com/Juicy-j-zip-and-a-double-cup-remix-lyrics',
	'http://www.rapgenius.com/2-chainz-all-i-do-is-me-lyrics']
for song in allthug:
	print "Loading...", song
	try:
		response = urllib2.urlopen(song)
		soup = BeautifulSoup(response)
		lyrics = soup.find('div', attrs={'class': 'lyrics '})
		lyricsreg = re.sub('<[^<]+?>', '', str(lyrics))
		lyricsreg = lyricsreg.split('\n')
		for line in lyricsreg:
			thuglyrics.append(line)
		time.sleep(5)
	except urllib2.HTTPError:
		print "Error loading song"
		pass

tokenized = [nltk.word_tokenize(t) for t in thuglyrics]
"""
bandz = pickle.load(open("thug_tokens.p", "rb"))
thugtrainer = nltk.NgramModel(3, bandz)

api = twitter.Api(consumer_key='xxx',
consumer_secret='xxx',
access_token_key='xxx',
access_token_secret='xxx')

while True:
	tweet = " ".join(thugtrainer.generate(random.randint(5,15)))
	punctuation = [",", "!", ".", "'", "n't", ":", ";"]
	for punct in punctuation:
		tweet = tweet.replace(" " + punct, punct)
	api.PostUpdate(tweet)
	print "Tweeted: ", tweet
	sleeptime = random.randint(2500,5000)
	print "Sleeping for " + str(sleeptime) + " seconds."
	time.sleep(sleeptime)
