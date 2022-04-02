import json
import os
import time

import pandas as pd
from configparser import ConfigParser
import requests
from dotenv import load_dotenv

load_dotenv()


class TwitterAPIData:
    """
    A class used to Extract Twitter Mentions Data.

    Attributes
    ----------
    urls : list
        list contains the url endpoints to call the API.
    next_token : dict
        dict contains the next_token (i.e, address to next page)
    params : dict
        dict contains the fields those needs to be extracted.
    json_data : list
        the list of dict's which contains formatted extracted tweets data in required form.
    json_response : dict
        dict contains the api endpoint json response.
    user_id : list
        list contains the Twitter user id's whose data to be collected.

    bearer_token : str
        str contains authentication token

    Methods
    -------
    create_url()

        It uses user_ids to creates API endpoints and stores in urls list.

    bearer_oauth()

        Method required by bearer token authentication.

    getting_next_page()

        Method to get next_token and pass it to api endpoints to get more data.

    connect_to_endpoint()

        It calls the Api endpoints and stores the response into json_response dict.

    join_json()

        It is used to extract and join the data in required format, stores into json_data list.

    write2csvFile()
        It is used to write json data to csv.

    """

    def __init__(self):
        """
        Attributes
        ----------
        urls : list
            list contains the url endpoints to call the API.
        params : dict
            dict contains the fields those needs to be extracted.
        json_data : list
            the list of dict's which contains formatted extracted tweets data in required form.
        json_response : dict
            dict contains the api endpoint json response.
        user_id : list
            list contains the Twitter user id's whose data to be collected.

        bearer_token : str
            str contains authentication token

        """
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

        self.urls = []
        self.json_data = []
        self.json_response = {}
        self.bearer_token = os.getenv('BEARER_TOKEN')

    def create_url(self, user_ids):
        tweet_fields = "expansions=referenced_tweets.id,author_id&tweet.fields=id,author_id,created_at&user.fields=name,location,id,username"
        # https://api.twitter.com/2/users/184833230/tweets?max_results=100&
        # expansions=author_id,referenced_tweets.id&tweet.fields=id,created_at,author_id&user.fields=id,location,name,username"
        i = 0
        for user_id in user_ids:
            i += 1
            if i <= 2:
                self.urls.append(f'https://api.twitter.com/2/users/{user_id}/tweets?max_results=100&{tweet_fields}')

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2UserMentionsPython"
        return r

    def connect_to_endpoint(self, url: object) -> object:
        """
            It calls the Api endpoints and stores the response into json_response dict.
        """
        time.sleep(5)
        response = requests.request("GET", url, auth=self.bearer_oauth)
        # print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )
        self.json_response = response.json()
        # print(self.json_response)
        if response.status_code == 200:
            self.write2csvfile()

    def join_json(self):
        """
            It is used to extract and join the data in required format, stores into json_data list.
        """
        tweet_list = []
        for data in self.json_response['data']:
            dic = {}
            if '@bt_uk' in data['text'].lower() or '@ee' in data['text'].lower():
                dic['tweet_id'] = str(data['id'])
                dic['user_id'] = str(data['author_id'])
                dic['created_at'] = str(data['created_at'])
                dic['tweet'] = data['text']
                if 'referenced_tweets' in data.keys():
                    dic['tweet_type'] = [r['type'] for r in data['referenced_tweets']][0]
                    dic['replied_to_id'] = [r['id'] for r in data['referenced_tweets']][0]
                else:
                    dic['tweet_type'] = "Original_tweet"
                    dic['replied_to_id'] = "Null"
                if len(dic) != 0:
                    tweet_list.append(dic)
        [self.json_data.append(k) or k for k in tweet_list]
        return self.json_data

    def write2csvfile(self):
        data = self.join_json()
        df = pd.DataFrame(data)
        print(df)
        # df.drop_duplicates(inplace=True, ignore_index=False)
        # df['get_repliedTo_tweet_link'] = df.apply(
        #     lambda x: os.getenv('REPLIEDTWEET').format(x['replied_to_id']) if x['replied_to_id'] != 'Null' else 'null',
        #     axis=1)
        # df['get_tweet_link'] = df.apply(lambda x: os.getenv('TWEET').format(x['user_id'], x['tweet_id']), axis=1)
        df.to_csv(f"{os.getenv('SCRATCH_CSVFILES')}test2.csv", index=False)
        print("completed...............")


def main():
    file = 'H:\MyLearningProjects\PythonProjects\SentimentAnalysis\config.ini'
    config = ConfigParser()
    config.read(file)
    path = config['path']['scratch_csvfiles']
    df = pd.read_csv(os.path.join(path, 'test_data.csv'))
    user_ids = df['author_id'].astype('Int64')
    user_ids = user_ids.to_list()

    apidata = TwitterAPIData()
    apidata.create_url(user_ids)
    for url in apidata.urls:
        print(url)
        apidata.connect_to_endpoint(url)


if __name__ == "__main__":
    main()
