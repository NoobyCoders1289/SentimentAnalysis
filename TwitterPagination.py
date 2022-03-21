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
                       "start_time": "2021-03-02T17:00:00Z", "pagination_token": self.next_token}
        self.json_data = []
        self.json_response = {}
        self.user_id = [20678384, 15133627, 7117212, 118750085]
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
        for i in self.json_response['data']:
            dic = {}
            for j in self.json_response['includes']['users']:
                if i['author_id'] == j['id']:
                    dic['tweet_id'] = i['id']
                    dic['user_id'] = i['author_id']
                    dic['created_at'] = i['created_at']
                    dic['tweet'] = i['text']
                    dic['username'] = j['username']
                    dic['name'] = j['name']
                    if 'location' in j.keys():
                        dic['location'] = j['location']
                    else:
                        dic['location'] = ""
                    if 'referenced_tweets' in i.keys():
                        dic['tweet_type'] = [j['type'] for j in i['referenced_tweets']][0]
                    else:
                        dic['tweet_type'] = "Original_Tweet"
            self.json_data.append(dic)
        return self.json_data

    def write2csvfile(self):
        data = self.join_json()
        df = pd.DataFrame.from_records(data)
        df.drop_duplicates(inplace=True, ignore_index=False)
        df.to_csv(r"static\\csv_files\\TweetsData4.csv", index=False)


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
