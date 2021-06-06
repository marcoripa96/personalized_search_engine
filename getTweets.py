import os
import sys
import tweepy as tw
import pandas as pd
import datetime
import csv
import secrets


def auth(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    return auth, api

def convertToDatetime(input):
    splitted = input.split("/")
    date = datetime.datetime(int(splitted[2]), int(splitted[1]), int(splitted[0]), 0, 0, 0)
    return date

def getTweets(username, n_tweets):
    tweets = []
    print('\nRequesting to Twitter...\n')
    for status in tw.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended').items(int(n_tweets)):
        tweets.append(status)
    print('Number of tweets: ', len(tweets))
    return tweets
    

def saveToCsv(tweets):
    hashtags = []
    full_texts = []
    for tweet in tweets:
        # hashtags
        tmp = []
        for hashtag in tweet.entities['hashtags']:
            tmp.append(hashtag['text'])
        hashtags.append(tmp)
        # check full_text for retweets
        if 'retweeted_status' in tweet._json:
            retweet_text = 'RT @' + api.get_user(tweet.retweeted_status.user.id_str).screen_name + ': ' \
                        + tweet._json['retweeted_status']['full_text']
            full_texts.append(retweet_text)
        else:
            full_texts.append(tweet.full_text)




    tweets_df = pd.DataFrame(vars(tweets[i]) for i in range(len(tweets)))

    # define attributes you want to save
    tweet_atts = [
    'created_at', 
    'favorite_count', 
    'retweet_count', 
    'source', 
    'retweeted',
    'id'
    ]
    tweets_df = tweets_df[tweet_atts]
    tweets_df['full_text'] = pd.Series(full_texts)
    tweets_df['hashtags'] = pd.Series(hashtags)
    tweets_df.to_csv('./' + username + '.csv', index=False, sep='\t')

# Twitter API keys
consumer_key= secrets.consumer_key
consumer_secret= secrets.consumer_secret
access_token= secrets.access_token
access_token_secret= secrets.access_token_secret

# Auth to Twitter API
auth, api = auth(consumer_key, consumer_secret, access_token, access_token_secret)

# Input username
username = input("Type the username: ")

# Input number of tweets
n_tweets = input("Input the number of tweets: ")

###
# username = "JoeBiden"
# n_tweets = 1000
###

# Get tweets of username in date range
tweets = getTweets(username, n_tweets)

# Save tweets to CSV
if len(tweets) > 0:
    saveToCsv(tweets)
    input("File saved in current folder, press enter to exit ;)" )
else:
    print('0 tweets found\n')
    input("Press enter to exit :(" )


