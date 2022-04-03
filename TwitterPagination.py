from ast import Break
from configparser import ConfigParser
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

    def __init__(self,folder_path):
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
            7117212    |@EE
            118750085  |@bt_uk
            17872077   |@virginmedia
        """
        self.folder_path = folder_path
        self.urls = []
        self.next_token = {}
        self.params = {"expansions": "author_id,referenced_tweets.id", "tweet.fields": "id,created_at,text,author_id,lang",
                       "user.fields": "id,name,username,location", "max_results": 100,
                       "start_time": "2022-03-28T00:00:00.000Z",
                       "pagination_token": self.next_token}
        self.json_data = []
        self.json_response = {}
        # {"viuk":"20678384", "o2":"15133627", "ee":"7117212", "bt":"118750085", "virginmed":"17872077"}
        # {"jio":"1373901961","airtel":"103323813","vi":"1287644632449343488","bsnl":"2251461926"}
        # self.user_id = [20678384, 15133627, 7117212, 118750085, 17872077]
        self.user_id = [1373901961, 103323813, 1287644632449343488, 2251461926]
        self.bearer_token = os.getenv('BEARER_TOKEN')
        self.count = 0
        self.max_count = 100000
        self.total_data = []

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
            Method to get next_token and pass it to api endpoints to get more da                                                                                                           ta.
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
                    # self.write2csvfile()
                    self.join_json()
                    self.count += result_count
                    print("Total no of Tweets added(count): ", self.count)
                    print("Total Pages : ", page_no)
                    page_no += 1
                    time.sleep(2)

            # if response has no next_token
            else:
                if result_count is not None and result_count > 0:
                    # self.write2csvfile()
                    print("url Endpoint : ", url)
                    self.join_json()
                    self.count += result_count
                    print("Total no of Tweets added(count): ", self.count)
                    print("Total Pages : ", page_no)
                    page_no += 1
                    print("----------------------------------------------------------------------------")
                    time.sleep(2)
                flag = False
                self.next_token = None
            
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
            dic['tweet_id'] = str(tweet['id'])
            dic['user_id'] = str(tweet['author_id'])
            dic['created_at'] = tweet['created_at']
            dic['tweet'] = tweet['text']
            dic['username'] = user['username']
            dic['name'] = user['name']
            if 'location' in user.keys():
                dic['location'] = user['location']
            else:
                dic['location'] = ""
                
            if 'lang' in tweet.keys():
                dic['language'] = tweet['lang']
            else:
                dic['language'] = ''
            if 'referenced_tweets' in tweet.keys():
                dic['tweet_type'] = [r['type'] for r in tweet['referenced_tweets']][0]
                dic['replied_to_id'] = [str(r['id']) for r in tweet['referenced_tweets']][0]
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

        # ------------self.json_response['re-tweets'] vs self.json_response['users']----------#
        with open(os.path.join(self.folder_path,'json_files\\indiaTelecom.json'), 'r+', encoding='utf-8') as f:  
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
        [self.json_data.append(j) or j for j in tweet_list]
        [self.json_data.append(k) or k for k in reply_tweet]
        print(f'len of tweet_list: {len(tweet_list)}')
        print(f'len of reply_tweet list in api call : {len(reply_tweet)}')
        print(f'len of final list : {len(self.json_data)}')
        # return self.json_data
        
    # def save_json(self):
    #     data = self.join_json()
    #     self.total_data.append(data)

    def write2csvfile(self):
        '''
            It is used to save all the extracted data stored in json_data list to csv file.
        '''
        # data = self.join_json()
        df = pd.DataFrame(self.json_data)
        df = df.dropna(how='all')
        df.drop_duplicates(inplace=True, ignore_index=False)
        # df['created_at']=df['created_at'].astype('datetime64[ns]')

        df['get_repliedTo_tweet_link'] = df.apply(lambda x: f"https://twitter.com/i/web/status/{x['replied_to_id']}" if x['replied_to_id'] != 'Null' else 'null', axis=1)
        df['get_tweet_link'] = df.apply(lambda x: f"https://twitter.com/{x['user_id']}/status/{x['tweet_id']}", axis=1)
        start_date = df['created_at'].astype(str).min().split('T')[0].replace('-','_')
        end_date = df['created_at'].astype(str).max().split('T')[0].replace('-','_')
        df.to_csv(f"{os.path.join(self.folder_path,'csv_files')}\\India_start_{start_date}_end_{end_date}.csv", index=False)
        
        
def main():
    # file configs
    configfile_path = os.path.join(os.getcwd(),'config.ini')
    config = ConfigParser()
    config.read(configfile_path)
    folder_path = config['path']['static']

    # ? creating object to TwitterAPIData class
    apidata = TwitterAPIData(folder_path)
    apidata.create_url()
    for url in apidata.urls:
        m1 = apidata.getting_next_page(url)
        # # apidata.total_data.append(apidata.join_json())
        if m1 == 1:
            break
    apidata.write2csvfile()
    




if __name__ == "__main__":
    main()

