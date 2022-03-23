from glob import glob
import os

import pandas as pd

from configparser import ConfigParser




def joincsv(path):
    """
        Function to join 2 or more csv files to single file
        parameters
        
    """
    # path to the folder 
    folder_path = os.path.join(path, "TweetsData*.csv")

    # list of all files_path present in path folder
    files_list = glob(folder_path)
    # print(join_files)

    # Joining csv files with concat, map
    # converting all csv data to DataFrame with !read_csv
    df = pd.concat(map(pd.read_csv, files_list), ignore_index=True)
    
    #Removing Duplicate records
   #----- 
    print("Before drop_duplicates")
    print(df.shape)
    df.drop_duplicates(keep='first', inplace=True)
    print(df[df.duplicated()].shape)
   #-----
    print("After drop_duplicates")
    print(df.shape)
    
    # writing to new single Csv file
    df.to_csv(os.path.join(path, 'TwitterData123.csv'))
    print('completed')


if __name__ == "__main__":
    # ConfigParse Parses the config file
    file = 'config.ini'
    config = ConfigParser()
    config.read(file)
    # path = r"H:\\MyLearningProjects\\PythonProjects\\SentimentAnalysis\\static\\csv_files\\"
    path = config['path']['static_csvfiles']
    # print(path)
    joincsv(path)
   