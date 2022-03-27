import pandas as pd
from configparser import ConfigParser
import os

file = 'H:\MyLearningProjects\PythonProjects\SentimentAnalysis\config.ini'
config = ConfigParser()
config.read(file)
path = config['path']['scratch_csvfiles']
df = pd.read_csv(os.path.join(path, 'CleanedData2_10_24.csv'))
print(df.shape)

tweet_ids = df['tweet_id'].to_list()
print(tweet_ids[10280:])

# n = 100
# final = [tweet_ids[i * n:(i + 1) * n] for i in range((len(tweet_ids) + n - 1) // n)]
# i = 0
# tweet_lis = []
# for tweet_id in final:
#     sent = ''
#     for idss in tweet_id:
#         sent += str(idss) + ","
#     tweet_lis.append(sent)
# print(len(tweet_lis))
# for i in tweet_lis:
#     print(i[:-1])
#     break

