import json
import os

import pandas as pd

import requests
from dotenv import load_dotenv

load_dotenv()


class TwitterAPIData:
    '''
    A class used to Extract Twitter Mentions Data.

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
        list contains the twitter user id's whose data to be collected. 
    
    bearer_token : str
        str contains authentication token

    Methods
    -------
    create_url() 

        It uses user_ids to creates API endpoints and stores in urls list.
    
    bearer_oauth()

        Method required by bearer token authentication.
    
    connect_to_endpoint() 

        It calls the Api endpoints and stores the response into json_response dict.
    
    join_json()

        It is used to extract and join the data in required format, stores into json_data list.

    write2csvFile()
        It is used to write json data to csv.

    '''

    def __init__(self):
        '''
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
            list contains the twitter user id's whose data to be collected. 
        
        bearer_token : str
            str contains authentication token
        '''
        '''
            TWITTER ID |TWITTER USERNAME
            20678384   |@VodafoneUK
            15133627   |@O2
            158368965  |@ThreeUK
            361268597  |@ThreeUKSupport
            7117212    |@EE
            118750085  |@bt_uk
            17872077   |@virginmedia

        '''

        self.urls = []
        self.params = {"expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id", "tweet.fields": "id,created_at,text,author_id",
                       "user.fields": "id,name,username,location", "max_results": 100,
                       "start_time": "2021-03-02T17:00:00Z"}
        self.json_data = []
        self.json_response = {}
        self.user_id = [20678384, 15133627, 7117212, 118750085]
        self.bearer_token = os.getenv('BEARER_TOKEN')

    def create_url(self):
        '''
        It uses user_ids to creates API endpoints and stores in urls list.
        '''
        for user in self.user_id:
            self.urls.append(f"https://api.twitter.com/2/users/{user}/mentions")

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2UserMentionsPython"
        return r

    def connect_to_endpoint(self, url):
        '''
            It calls the Api endpoints and stores the response into json_response dict.
        '''
        response = requests.request("GET", url, auth=self.bearer_oauth, params=self.params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )
        self.json_response = response.json()

    def join_json(self):
        '''
            It is used to extract and join the data in required format, stores into json_data list.
        '''
        print(json.dumps(self.json_response))
        # print('-----------------------------------------------')
        # for i in self.json_response['data']:
        #     dic = {}
        #     for j in self.json_response['includes']['users']:
        #         if i['author_id'] == j['id']:
        #             dic['tweet_id'] = i['id']
        #             dic['user_id'] = i['author_id']
        #             dic['created_at'] = i['created_at']
        #             dic['tweet'] = i['text']
        #             dic['username'] = j['username']
        #             dic['name'] = j['name']
        #             if 'location' in j.keys():
        #                 dic['location'] = j['location']
        #             else:
        #                 dic['location'] = ""
        #             if 'referenced_tweets' in i.keys():
        #                 dic['tweet_type'] = [j['type'] for j in i['referenced_tweets']][0]
        #             else:
        #                 dic['tweet_type'] = "Original_Tweet"
        #     self.json_data.append(dic)
        # return self.json_data

    def write2csvFile(self):
        data = self.join_json()
        df = pd.DataFrame.from_records(data)
        df.drop_duplicates(inplace=True, ignore_index=False)
        df.to_csv(r"TweetsDatasample.csv", index=False)


def main():
    apiData = TwitterAPIData()
    apiData.create_url()
    for url in apiData.urls:
        apiData.connect_to_endpoint(url)
        apiData.join_json()
        break

    '''
        dumping the extracted data to json file
    '''
    # with open(r"DataExtraction\\tweetsReview.json", 'w') as file:
    #     json.dump(apiData.json_data, file)

    # apiData.write2csvFile()


if __name__ == "__main__":
    main()
