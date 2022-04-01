import os
import json
from glob import glob
import pandas as pd




# path = os.path.join(r'H:\\MyLearningProjects\\PythonProjects\\SentimentAnalysis\\static\\scratch\\jsonfiles\\','*.json')
# files = glob(path)
# file_no = 1
# for file in files:
#     file_name = file.replace('\\','/').split('/')[-1].split('.')[0]
#     print(f'file no: {file_no}')
#     with open(file,'r+',encoding='utf-8') as f:
#         dic_ = json.load(f)
#     lis_data = []
#     for i in dic_['data']:
#         dic={}
#         for j in dic_['includes']['users']:
#             if i['author_id'] == j['id']:
#                 dic['tweet_id'] = i['id']
#                 dic['user_id'] = i['author_id']
#                 dic['created_at'] = i['created_at']
#                 dic['tweet'] = i['text']
#                 dic['username'] = j['username']
#                 dic['name'] = j['name']
#                 if 'location' in j.keys():
#                     dic['location'] = j['location']
#                 else:
#                     dic['location'] = ""
#                 if 'referenced_tweets' in i.keys():
#                     dic['tweet_type'] = [r['type'] for r in i['referenced_tweets']][0]
#                     dic['replied_to_id'] = [r['id'] for r in i['referenced_tweets']][0]
#                 else:
#                     dic['tweet_type'] = "Original_tweet"
#                     dic['replied_to_id'] = "Null"
#         lis_data.append(dic)
#     print(f'len of lis_data: {len(lis_data)}')
#     #----------------------------------------------------------------------------#
#     d = []
#     for k in dic_['includes']['tweets']:
#         ids = {'20678384':'Vodafone','7117212':'EE','118750085':'BT'}
#         dic2={}
#         for j in dic_['includes']['users']:
#             if j['id'] == k['author_id']:
#                 dic2['tweet_id'] = k['id']
#                 dic2['user_id'] = k['author_id']
#                 dic2['created_at'] = k['created_at']
#                 dic2['tweet'] = k['text']
#                 dic2['username'] = j['username']
#                 dic2['name'] = j['name']
#                 if 'location' in j.keys():
#                     dic2['location'] = j['location']
#                 else:
#                     dic2['location'] = ""
#                 if 'referenced_tweets' in k.keys():
#                     dic2['tweet_type'] = [r['type'] for r in k['referenced_tweets']][0]
#                     dic2['replied_to_id'] = [r['id'] for r in k['referenced_tweets']][0]
#                 else:
#                     dic2['tweet_type'] = "Original_tweet"
#                     dic2['replied_to_id'] = "Null"


#             else: #k['author_id'] == '20678384':
#                 # ids = {'20678384':'Vodafone','7117212':'EE','118750085':'BT'}
#                 for x,y in ids.items():
#                     if k['author_id'] == x:
#                         dic2['tweet_id'] = k['id']
#                         dic2['user_id'] = k['author_id']
#                         dic2['created_at'] = k['created_at']
#                         dic2['tweet'] = k['text']
#                         dic2['username'] = y
#                         dic2['name'] = y
#                         dic2['location'] = "UK"
#                         if 'referenced_tweets' in k.keys():
#                             dic2['tweet_type'] = [r['type'] for r in k['referenced_tweets']][0]
#                             dic2['replied_to_id'] = [r['id'] for r in k['referenced_tweets']][0]
#                         else:
#                             dic2['tweet_type'] = "Original_tweet"
#                             dic2['replied_to_id'] = "Null"
#         d.append(dic2)
#     #------------------------------------------------------------------------------------
#     print(f'len of d list in {file_name} : {len(d)}')
#     dicts = []
#     [dicts.append(j) or j for j in lis_data]
#     [dicts.append(k) or k for k in d]
#     print(f'len of final.csv list : {len(dicts)}')
#     df = pd.DataFrame(dicts)
#     df = df.dropna()
#     print(f'no of total records in {file_name} are {df.shape}')
#     x = df[df.duplicated()]
#     df.drop_duplicates(keep='last',inplace=True)
#     print(f'no of dupliactes in {file_name} are {x.shape}')
#     df.to_csv(f'csv_files//sample{file_name}.csv')
#     print(f'completed file{file_no}')
#     file_no+=1
#     print('-----------------------------------------------------------------')


# # create csv file
# files = glob(path)
# for file in files:
#     with open(file,'r+',encoding="utf-8") as f:
#         dic = json.load(f)
#         normalized_data = pd.json_normalize(dic['data'])
#         normalized_users = pd.json_normalize(dic['includes']['users']).set_index('id')
#         normalized_tweets = pd.json_normalize(dic['includes']['tweets']).set_index('id')

#         normalized_users.rename({'id': 'author_id'}, inplace = True, axis = 1)
#         normalized_data.rename({'id': 'tweet_id'}, inplace = True, axis = 1)
#         normalized_tweets.rename({'id': 'tweet_id'}, inplace = True, axis = 1)

#         normalized = normalized_data.join(normalized_users, on = 'author_id', how = 'outer', rsuffix = '_user')
#         normalized = normalized.join(normalized_tweets, on = 'author_id', how = 'outer', rsuffix = '_twitter')
#         normalized.to_csv('sample.csv')
#         break
