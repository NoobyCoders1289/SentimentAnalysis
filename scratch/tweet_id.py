import glob
import pickle
import pandas as pd
from configparser import ConfigParser
import os
import numpy as np

file = 'H:\MyLearningProjects\PythonProjects\SentimentAnalysis\config.ini'
config = ConfigParser()
config.read(file)
path = config['path']['scratch_csvfiles']
files_list = glob.glob(os.path.join(path, 'no_refered_type/*.csv'))
files_list2 = glob.glob(os.path.join(path, 'nolink/*.csv'))
files_list3 = glob.glob(os.path.join(path, 'link/*.csv'))
print(len(files_list))
print(len(files_list2))
print(len(files_list3))
print('----------------------')
# df = pd.concat(map(pd.read_csv, files_list), ignore_index=True)

tweet_lis = []
for i in files_list2:
    df = pd.read_csv(i)
    df
    print(df.shape)
    for j in df['tweet_id'].to_list():
        if j not in tweet_lis:
            tweet_lis.append(str(j))

df2 = pd.concat(map(pd.read_csv, files_list2), ignore_index=True)
tweet_ids = df2['tweet_id'].unique().tolist()

# df3 = pd.concat(map(pd.read_csv, files_list3), ignore_index=True)
# tweets_ids = df3['tweet_id'].unique().tolist()

print(len(tweet_ids))
print(tweet_lis)
# print(len(tweets_ids))

# final_lis = tweet_lis + tweet_ids + tweets_ids
#
# print(len(list(set(final_lis))))
# # final_lis = list(set(final_lis))
# print(final_lis[:20])
#
# print('----------------')
# # print(len(list(set(final_lis))))
# # print(tweet_ids[10280:])

# n = 100
# final.csv = [tweet_ids[i * n:(i + 1) * n] for i in range((len(tweet_ids) + n - 1) // n)]
# i = 0
# tweet_lis = []
# for tweet_id in final.csv:
#     sent = ''
#     for idss in tweet_id:
#         sent += str(idss) + ","
#     tweet_lis.append(sent)
# print(len(tweet_lis))
# for i in tweet_lis:
#     print(i[:-1])
#     break


# with open('tweet_ids', 'wb') as fp:
#     pickle.dump(final_lis, fp)


# with open('tweet_ids', 'rb') as fp:
#     itemlist = pickle.load(fp)
#
# print(len(itemlist))
# print(itemlist[:20])
