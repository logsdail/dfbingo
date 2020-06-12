#!/usr/bin/env python3

import tweepy
import libxc
# Key import copied from https://dototot.com/reply-tweets-python-tweepy-twitter-bot/
from keys import keys

# Set up OAuth and integrate with API
auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth)

# Write a tweet to push to our Twitter account
tweet_text = libxc.get_random_functional()

debug = True
if debug:
    print(tweet_text)
else:
    api.update_status(status=tweet_text)

