#!/usr/bin/env python3

import tweepy
import libxc
import string

## Adapted from: https://realpython.com/twitter-bot-python-tweepy
def process_tweet(api, tweet, me):
    ## Ignore message if a reply, if already retweeted or if sent by me
    if tweet.in_reply_to_status_id is not None or \
       tweet.retweeted or tweet.user.id == me.id:
        return

    # Break the tweet up in to lower case, depunctuated words
    table = str.maketrans('', '', string.punctuation)
    incoming_words = [w.translate(table) for w in tweet.full_text.casefold().split()]

    if ("retweet" or "rt") in incoming_words:
        # Retweet, since we have not retweeted it yet
        try:
            #print("Retweeting: ", tweet.full_text)
            tweet.retweet()
        except:
            # Error, carry on working
            pass

    # Like post
    #if not tweet.favorited:
    #    tweet.favorite()

    # Follow user
    #if not tweet.user.following:
    #    tweet.user.follow()

    else: # Not retweeting
        # Reply to message
        tweet_text = "@" + tweet.user.screen_name + " " + libxc.search_functional_information(incoming_words)
        try:
            #print("Replying: ", tweet_text)
            api.update_status(status=tweet_text,
                              in_reply_to_status_id=tweet.id,
                             )
        except:
            # Error, carry on working
            pass

    return

def check_mentions(api, since_id, startup=False):
    new_since_id = since_id
    me = api.me()
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id, tweet_mode="extended").items():
        new_since_id = max(tweet.id, new_since_id)

        # Debug statement
        if False:
            print(tweet.id, tweet.full_text)

        # On startup, just workout the most recent Tweet ID; if running, process the tweet.
        if not startup:
            process_tweet(api, tweet, me)
    return new_since_id

# Run main

# Key import copied from https://dototot.com/reply-tweets-python-tweepy-twitter-bot/
from keys import keys

# Set up OAuth and integrate with API
auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth)

# Give an initial starting point
since_id = check_mentions(api, 1, True)

import time
while True:
    time.sleep(300)
    try:
        since_id = check_mentions(api, since_id)
    except tweepy.TweepError:
        pass
