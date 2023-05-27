#!/usr/bin/env python3

# Loading here as otherwise these are reloaded on each call
import tweepy
import libxc
import string

## Adapted from: https://realpython.com/twitter-bot-python-tweepy
def process_tweet(Client, tweet, me):
    ## Ignore message if a reply, if already retweeted or if sent by me
    if tweet.in_reply_to_user_id is not None or \
       tweet.referenced_tweets.id is not None or \
       tweet.author_id == me.id:
        return

    # Break the tweet up in to lower case, depunctuated words
    table = str.maketrans('', '', string.punctuation)
    incoming_words = [w.translate(table) for w in tweet.full_text.casefold().split()]

    if ("retweet" or "rt") in incoming_words:
        # Retweet, since we have not retweeted it yet
        try:
            #print("Retweeting: ", tweet.full_text)
            Client.retweet(tweet_id=tweet.id)
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
        print(dir(tweet.user))
        tweet_text = "@" + Client.get_user(id=tweet.author_id) + " " + libxc.search_functional_information(incoming_words)
        try:
            #print("Replying: ", tweet_text)
            Client.create_tweet(text=tweet_text,
                                in_reply_to_tweet_id=tweet.id,
                             )
        except:
            # Error, carry on working
            pass

    return

def check_mentions(Client, since_id, startup=False, debug=False):
    new_since_id = since_id
    me = Client.get_user(username="dfbingo").id
    for tweet in tweepy.Paginator(Client.get_users_mentions(id=me, since_id=since_id, tweet_fields=list('in_reply_to_user_id', 'author_id', 'referenced_tweets.id'))).items():
        new_since_id = max(tweet.id, new_since_id)

        # Debug statement
        if debug:
            print(tweet.id, tweet.full_text)

        # On startup, just workout the most recent Tweet ID; if running, process the tweet.
        if not startup:
            process_tweet(Client, tweet, me)
    return new_since_id

