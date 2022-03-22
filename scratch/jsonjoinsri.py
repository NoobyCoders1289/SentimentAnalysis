import os
import json
from glob import glob
import pandas as pd


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


path = os.path.join(
    r'H:\\MyLearningProjects\\PythonProjects\\SentimentAnalysis\\scratch\\jsonfiles\\file1.json')
file_name = 'file1'
with open(path, 'r+', encoding='utf-8') as f:
    dic_ = json.load(f)

# ----------------------------------dic_['data'] vs dic_['users']-------------------------------
tweet_list = []
for data in dic_['data']:
    dic = {}
    for user in dic_['includes']['users']:
        if data['author_id'] == user['id']:
            dic = getDataframe(dic, data, user)
    tweet_list.append(dic)
print(f'len of tweet_list: {len(tweet_list)}')

#---------------------------------dic_['tweets'] vs dic_['users']-------------------------------------------#
with open(r'scratch\\companydata.json', 'r+', encoding='utf-8') as f:
    telecom_ids = json.load(f)
reply_tweet = []
for tweet in dic_['includes']['tweets']:
    dic2 = {}
    for user in dic_['includes']['users']:
        if user['id'] == tweet['author_id']:
            dic2 = getDataframe(dic2, tweet, user)

        elif tweet['author_id'] in telecom_ids.keys():
            # ids = {'20678384':'Vodafone','7117212':'EE','118750085':'BT'}
            dic2 = getDataframe(dic2, tweet, telecom_ids[tweet['author_id']] )
    reply_tweet.append(dic2)
# ------------------------------------------------------------------------------------
print(f'len of reply_tweet list in {file_name} : {len(reply_tweet)}')
dicts = []
[dicts.append(j) or j for j in tweet_list]
[dicts.append(k) or k for k in reply_tweet]
print(f'len of final list : {len(dicts)}')
df = pd.DataFrame(dicts)
df = df.dropna()
print(f'no of total records in {file_name} are {df.shape}')
x = df[df.duplicated()]
df.drop_duplicates(keep='last', inplace=True)
print(f'no of dupliactes in {file_name} are {x.shape}')
df.to_csv(f'sample23{file_name}.csv')
print(f'completed file{1}')
print('-----------------------------------------------------------------')
