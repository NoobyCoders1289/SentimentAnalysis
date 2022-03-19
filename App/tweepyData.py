import tweepy
import os
import time

import pandas as pd

import requests
from dotenv import load_dotenv
load_dotenv()

"""
TWITTER ID |TWITTER USERNAME
20678384   |@VodafoneUK
15133627   |@O2
158368965  |@ThreeUK
361268597  |@ThreeUKSupport
7117212    |@EE
118750085  |@bt_uk
17872077   |@virginmedia
"""

# your bearer token
MY_BEARER_TOKEN = os.getenv("BEARER_TOKEN")
# create your client
client = tweepy.Client(bearer_token=MY_BEARER_TOKEN)

# # query to search for tweets
# query = "@O2 lang:en -is:reply -is:retweet"
# # your start and end time for fetching tweets
# # start_time = "2021-12-10T00:00:00Z"
# # end_time = "2021-12-14T00:00:00Z"
# # get tweets from the API
# tweets = client.search_recent_tweets(query=query,
#                                      tweet_fields=[
#                                          "created_at", "text", "source"],
#                                      user_fields=[
#                                          "name", "username", "location"],
#                                      max_results=10,
#                                      expansions="author_id"
#                                      )
# # first tweet
# first_tweet = tweets  # type: ignore
# # print(dict(first_tweet))

# # import the pandas library
# import pandas as pd
# # create a list of records
# tweet_info_ls = []
# # iterate over each tweet and corresponding user details
# for tweet, user in zip(tweets.data, tweets.includes["users"]): #type: ignore
#     tweet_info = {
#         "created_at": tweet.created_at,
#         "text": tweet.text,
#         "source": tweet.source,
#         "name": user.name,
#         "username": user.username,
#         "location": user.location,
#         "verified": user.verified,
#         "description": user.description
#     }
#     tweet_info_ls.append(tweet_info)
# # create dataframe from the extracted records
# tweets_df = pd.DataFrame(tweet_info_ls)
# # display the dataframe
# # print(tweets_df.head())
# # print(tweets_df.to_json(orient='records'))
# # tweets_df.to_csv('tweepydata.csv')



for tweet in tweepy.Paginator(client.get_users_mentions, "20678384",max_results=100).flatten(limit=5):
    print(tweet.id)