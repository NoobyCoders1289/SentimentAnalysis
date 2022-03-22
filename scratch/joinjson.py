import os,json
from glob import glob
import pandas as pd

path = os.path.join(r'H:\MyLearningProjects\PythonProjects\SentimentAnalysis\static\json_files\jsonfiles\\','*.json')

files = glob(path)
data_lis = []
for file in files:
    with open(file,'r+',encoding="utf-8") as f:
        dic_ = json.load(f)
        for i in dic_['data']:
            dic={}
            for j in dic_['includes']['users']:
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
                        dic['tweet_type'] = [r['type'] for r in i['referenced_tweets']][0]
                    else:
                        dic['tweet_type'] = "Original_Tweet"     
            data_lis.append(dic)
df = pd.DataFrame(data_lis)
# df.drop_duplicates(keep='first',inplace=True)
df.to_csv('sample2.csv')
print('completed..........')     
        



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