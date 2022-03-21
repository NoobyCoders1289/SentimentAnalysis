# Importing Modules
import pandas as pd
import neattext as nfx
import re
import json

### Hide warnings
import warnings

warnings.filterwarnings('ignore')

# -------------------------------------Replacing appost's in text with full words----------------------------------#
def appost_removal(df,appost_dict):

    def _get_contractions(appost_dict):
        """
        Parameters
        ----------
        appost_dict : object
        """
        contraction_re = re.compile('(%s)' % '|'.join(appost_dict.keys()))
        return appost_dict, contraction_re

    contractions, contractions_re = _get_contractions(appost_dict)

    def replace_contractions(text):
        text = text.lower()

        def replace(match):
            return contractions[match.group(0)]

        return contractions_re.sub(replace, text.replace("’", "'"))

    df['clean_text'] = df['tweet'].apply(replace_contractions)
    return df



def cleanTxt(text):
    text = text.lower()
    text = nfx.remove_userhandles(text)
    text = nfx.remove_emojis(text)
    text = nfx.remove_urls(text)
    text = re.sub(r'#',' ',text)
    text = re.sub(r'\n',' ',text)
    text = re.sub(r'&amp','&',text)
    text = nfx.remove_stopwords(text)
    text = nfx.remove_puncts(text)
    text = nfx.remove_special_characters(text)
    text = nfx.remove_numbers(text)
    text = nfx.remove_multiple_spaces(text)
    text = text.strip()
    

    return text


# LOADING DATA SET
def load_data():
    df = pd.read_csv('static/csv_files/TweetsData1.csv')
    df.dropna(inplace=True)
    df.isnull().sum()
    df.drop_duplicates(keep='first', inplace=True, ignore_index=False)
    print(f"duplicated count: {df.duplicated(keep='first').sum()}")
    # df.info()
    with open('static/json_files/contractions.json', 'r+') as file:
        contraction_dict = json.load(file)
    appost_removal(df,contraction_dict)
    # print("-------------------------------------------------")
    # print(df.shape)
    df['clean_text'] = df['clean_text'].apply(cleanTxt)
    # print(df[['tweet','clean_text']])
    df.to_csv('static/csv_files/CleanedData.csv')


if __name__ == '__main__':
    load_data()
