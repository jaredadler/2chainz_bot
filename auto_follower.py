import tweepy, os, time, random
import cPickle as pickle
from random import choice

auth = tweepy.OAuthHandler("xxx", "xxx")
auth.set_access_token("xxx", "xxx")
api = tweepy.API(auth)

time.sleep(random.randint(0,300))
me = api.me()
if ((float(me.followers_count) / me.friends_count) < 2):
	pass
else:
	followers = api.followers_ids('2chainz_bot')
	friends = api.friends_ids('2chainz_bot')
	r = choice(followers)
	if r in friends:
		pass
	else:
		print "following", r
		api.create_friendship(r)