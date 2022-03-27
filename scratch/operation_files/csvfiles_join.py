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
    # fileexe = '49*.csv'
    # # path to the folder
    # folder_path = os.path.join(path, fileexe)
    #
    # # list of all files_path present in path folder
    # files_list = glob(folder_path)
    # print(join_files)
    files_list = [os.path.join(path, 'CleanedData_12_23.csv'), os.path.join(path, 'lookup.csv')]

    # Joining csv files with concat, map
    # converting all csv data to DataFrame with !read_csv
    df = pd.concat(map(pd.read_csv, files_list), ignore_index=True)

    # Removing Duplicate records
    # -----
    print("Before drop_duplicates: ", df.shape)
    print("No of duplicated rows :", df[df.duplicated(keep="first")].sum())
    df.drop_duplicates(subset=['tweet_id', 'user_id', 'created_at', 'tweet'], keep='last', inplace=True, ignore_index=True)
    # print(df[df.duplicated()].shape)
    # -----
    print("After drop_duplicates: ", df.shape)

    # writing to new single Csv file
    df.to_csv(os.path.join(path, 'CleanedData2_10_24.csv'))
    print('completed')


if __name__ == "__main__":
    # ConfigParse Parses the config file
    file = 'H:\MyLearningProjects\PythonProjects\SentimentAnalysis\config.ini'
    config = ConfigParser()
    config.read(file)
    # path = r"H:\\MyLearningProjects\\PythonProjects\\SentimentAnalysis\\static\\csv_files\\"
    path = config['path']['scratch_csvfiles']
    # print(path)
    joincsv(path)
