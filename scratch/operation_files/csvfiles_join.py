from glob import glob
import os

import pandas as pd

from configparser import ConfigParser


def joincsv(path):
    """
        Function to join 2 or more csv files to single file
        parameters
        ["TweetsData*.csv", 'CleanedDatav*.csv', '49*.csv']
    """
    
    # !--------------------------path to the folder-----------------------------
    # folder_path = os.path.join(path, 'csv_files\\*.csv')
    # list of all files_path present in path folder
    # files_list = glob(folder_path)
    # print(files_list)

    # ! ---------------- giving path of files directly---------------------------
    files_list = [os.path.join(path, 'start_28_03_end_03_04.csv')]

    # ? Joining csv files with concat, map
    # ? converting all csv data to DataFrame with read_csv
    df = pd.concat(map(pd.read_csv, files_list), ignore_index=True)
    try:
        df.drop(columns='Unnamed: 0',axis =1)
    except:
        pass
    # df.info()
    print(df.describe())

    # !Removing Duplicate records
    print("Before drop_duplicates: ", df.shape)

    df.drop_duplicates(subset=['tweet_id', 'user_id', 'created_at', 'tweet'], keep='last', inplace=True, ignore_index=True)
    print("After drop_duplicates: ", df.shape)

    # # writing to new single Csv file
    start_date = '28_03'
    end_date = '03_04'
    df.to_csv(os.path.join(path, f'{start_date}_{end_date}.csv'),index=False)
    print('completed')


if __name__ == "__main__":
    # ConfigParse Parses the config file
    file = r'H:\\MyLearningProjects\\PythonProjects\\SentimentAnalysis\\config.ini'
    config = ConfigParser()
    config.read(file)
    path = config['path']['scratch_csvfiles']
    # print(path)
    joincsv(path)
