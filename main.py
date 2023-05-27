#!/usr/bin/env python3

def setup_Client():
    import tweepy
    # Key import copied from https://dototot.com/reply-tweets-python-tweepy-twitter-bot/
    from keys import keys
    
    # Set up tweepy Client 
    return tweepy.Client(consumer_key=keys['consumer_key'],
                         consumer_secret=keys['consumer_secret'],
                         access_token=keys['access_token'],
                         access_token_secret=keys['access_token_secret'],
                         bearer_token=keys['bearer_token'])

def main():
    #Parse incoming arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--tweet', help='', action="store_true")
    parser.add_argument('--listen', help='', action="store_true")
    parser.add_argument('--test', help='', action="store_true")
    args = parser.parse_args()

    # Set up OAuth and integrate with API
    Client = setup_Client()

    if args.tweet:
        # Write a tweet to push to our Twitter account
        import libxc
        tweet_text = libxc.get_random_functional()

        # If debugging, print the tweet. Otherwise, send to Twitter
        if args.test:
            print(tweet_text)
        else:
            Client.create_tweet(text=tweet_text)

    if args.listen:   
        # Enter an infinite loop listening to our Twitter feed 
        from listen import check_mentions

        # Give an initial starting point
        since_id = check_mentions(Client, 1, True, args.test)

        # Only enter the loop if not debugging
        if not args.test:
            import time
            while True:
                time.sleep(300)
                try:
                    since_id = check_mentions(Client, since_id)
                except tweepy.TweepError:
                    pass 

if __name__ == "__main__":
    main()
