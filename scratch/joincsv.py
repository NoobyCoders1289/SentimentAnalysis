import pandas as pd
import glob
import os

path = r"H:\MyLearningProjects\PythonProjects\SentimentAnalysis\static\csv_files\\"
files = os.path.join(path, "TweetsData*.csv")
join_files = glob.glob(files)
# print(join_files)
print("Resultant CSV after joining all CSV files at a particular location...")

# joining files with concat and read_csv
df = pd.concat(map(pd.read_csv, join_files), ignore_index=True)
print("Before drop_duplicates")
# print(df.shape)
# df.drop_duplicates(keep='first', inplace=True)
# print(df.duplicated().sum())
# print("After drop_duplicates")
print(df.shape)
df.to_csv(os.path.join(path, 'TwitterData123.csv'))
print('completed')
