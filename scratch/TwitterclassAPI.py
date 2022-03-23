import json
import os
import time

import pandas as pd

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
        self.next_token = {}
        self.params = {"expansions": "author_id,referenced_tweets.id", "tweet.fields": "id,created_at,text,author_id",
                       "user.fields": "id,name,username,location", "max_results": 100,
                       "pagination_token": self.next_token}
        self.json_data = []
        self.json_response = {}
        self.user_id = [20678384, 15133627, 7117212, 118750085, 158368965, 17872077, 361268597]
        self.bearer_token = os.getenv('BEARER_TOKEN')
        self.count = 0
        self.max_count = 10000

    def create_url(self):
        """
        It uses user_ids to creates API endpoints and stores in urls list.
        """
        for user in self.user_id:
            self.urls.append(f"https://api.twitter.com/2/users/{user}/mentions")

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2UserMentionsPython"
        return r

    def getting_next_page(self, url):
        """
            Method to get next_token and pass it to api endpoints to get more data.
        """
        page_no = 1
        flag = True
        while flag:
            if self.count >= self.max_count:
                return 1
            print("----------------------------------------------------------------------------")
            print("Token: ", self.next_token)
            self.json_response = self.connect_to_endpoint(url)
            result_count = self.json_response['meta']['result_count']

            # if response has next_token
            if 'next_token' in self.json_response['meta']:
                self.next_token = self.json_response['meta']['next_token']
                print("Next_Token : ", self.next_token)

                if result_count is not None and result_count > 0 and self.next_token is not None:
                    print("url Endpoint : ", url)
                    self.write2csvfile()
                    self.count += result_count
                    print("Total # of Tweets added: ", self.count)
                    print("Total Pages : ", page_no)
                    page_no += 1
                    time.sleep(2)

            # if response has no next_token
            else:
                if result_count is not None and result_count > 0:
                    self.write2csvfile()
                    self.count += result_count
                    print("Total # of Tweets added: ", self.count)
                    print("Total Pages : ", page_no)
                    page_no += 1
                    print("----------------------------------------------------------------------------")
                    time.sleep(2)
                flag = False
                self.next_token = None
                return
            time.sleep(2)

    def connect_to_endpoint(self, url):
        """
            It calls the Api endpoints and stores the response into json_response dict.
        """
        self.params['pagination_token'] = self.next_token
        print(self.params)
        response = requests.request("GET", url, auth=self.bearer_oauth, params=self.params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )
        # self.json_response = response.json()
        return response.json()

    def join_json(self):
        """
            It is used to extract and join the data in required format, stores into json_data list.
        """

        def getDataframe(dic, tweet, user):
            dic['tweet_id'] = tweet['id']
            dic['user_id'] = tweet['author_id']
            dic['created_at'] = tweet['created_at']
            dic['tweet'] = tweet['text']
            dic['username'] = user['username']
            dic['name'] = user['name']
            if 'location' in user.keys():
                dic['location'] = user['location']
            else:
                dic['location'] = ""
            if 'referenced_tweets' in tweet.keys():
                dic['tweet_type'] = [r['type'] for r in tweet['referenced_tweets']][0]
                dic['replied_to_id'] = [r['id'] for r in tweet['referenced_tweets']][0]
            else:
                dic['tweet_type'] = "Original_tweet"
                dic['replied_to_id'] = "Null"

            return dic

        tweet_list = []
        for data in self.json_response['data']:
            tweet_dic = {}
            for user in self.json_response['includes']['users']:
                if data['author_id'] == user['id']:
                    tweet_dic = getDataframe(tweet_dic, data, user)
            tweet_list.append(tweet_dic)
        print(f'len of tweet_list: {len(tweet_list)}')

        # ------------self.json_response['tweets'] vs self.json_response['users']----------#
        with open(os.getenv('COMAPANY_DATA'), 'r+', encoding='utf-8') as f:  # type: ignore
            telecom_ids = json.load(f)
        reply_tweet = []
        for tweet in self.json_response['includes']['tweets']:
            reply_dic = {}
            for user in self.json_response['includes']['users']:
                if user['id'] == tweet['author_id']:
                    reply_dic = getDataframe(reply_dic, tweet, user)

                elif tweet['author_id'] in telecom_ids.keys():
                    # ids = {'20678384':'Vodafone','7117212':'EE','118750085':'BT'}
                    reply_dic = getDataframe(reply_dic, tweet, telecom_ids[tweet['author_id']])
            reply_tweet.append(reply_dic)
        # ------------------------------------------------------------------------------------
        print(f'len of reply_tweet list in api call : {len(reply_tweet)}')
        [self.json_data.append(j) or j for j in tweet_list]
        [self.json_data.append(k) or k for k in reply_tweet]
        print(f'len of final list : {len(self.json_data)}')
        return self.json_data

    def write2csvfile(self):
        data = self.join_json()
        df = pd.DataFrame.from_records(data)
        df.drop_duplicates(inplace=True, ignore_index=False)
        df.to_csv(f"{os.getenv('STATIC_CSVFILES')}referedTweetsData2.csv", index=False)


def main():
    apidata = TwitterAPIData()
    apidata.create_url()
    for url in apidata.urls:
        m1 = apidata.getting_next_page(url)
        if m1 == 1:
            break

    '''
        dumping the extracted data to json file
    '''
    # with open(r"DataExtraction\\tweetsReview.json", 'w') as file:
    #     json.dump(apidata.json_data, file)


if __name__ == "__main__":
    main()
# 'start_22_03_23T05_21_end_2022_03_14_T18_49'