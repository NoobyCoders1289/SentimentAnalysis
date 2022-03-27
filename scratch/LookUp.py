import requests
import os
import json
from configparser import ConfigParser
import pandas as pd

from dotenv import load_dotenv

load_dotenv()
# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url(tweet_ids):
    tweet_fields = "expansions=referenced_tweets.id,author_id&tweet.fields=id,author_id,created_at&user.fields=name,location,id,username"
    # Tweet fields are adjustable.
    # "https://api.twitter.com/2/tweets?ids={}&{}
    # expansions=referenced_tweets.id,author_id&tweet.fields=id,author_id,created_at&user.fields=name,location,id,username"
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, tweet_id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    # ids = "1506031517923000326,1505658668028776450"
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    # url = "https://api.twitter.com/2/tweets?ids={}&{}".format(ids, tweet_fields)
    # print(url)
    i = 0
    for ids in tweet_ids:
        i += 1
        if i <= 1:
            url = f'https://api.twitter.com/2/tweets?ids={ids}&{tweet_fields}'
            print(url)
            return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    file = 'H:\MyLearningProjects\PythonProjects\SentimentAnalysis\config.ini'
    config = ConfigParser()
    config.read(file)
    path = config['path']['scratch_csvfiles']
    df = pd.read_csv(os.path.join(path, 'sample2.csv'))
    tweet_ids = df['tweet_id'].to_list()
    url = create_url(tweet_ids)
    json_response = connect_to_endpoint(url)



if __name__ == "__main__":
    main()
