import json

data = [{
    "text": "@JaH_HY Hey! We appreciate you reaching out. We recommend you contact @VodafoneUK via DM, they will be "
            "able to assist you with your query.",
    "referenced_tweets": [
        {
            "type": "replied_to",
            "id": "1505885719230914567"
        }
    ],
    "created_at": "2022-03-21T14:12:12.000Z",
    "author_id": "466341559",
    "id": "1505910150229602306"
},
    {
        "text": "@VodafoneUK #VodafoneTreats Getting out in the sunshine and exploring the Scottish coastline has "
                "definitely put a spring in my step I feel so much more alive! https://t.co/AXrIicYnfv",
        "referenced_tweets": [
            {
                "type": "replied_to",
                "id": "1498704627000233985"
            }
        ],
        "created_at": "2022-03-21T14:10:31.000Z",
        "author_id": "837271780003885056",
        "id": "1505909723144589314"
    }]

# for i in data:
#     type_ = str()
#     print(type_)
#     break
import pandas as pd

df = pd.read_csv(r'H:\MyLearningProjects\PythonProjects\SentimentAnalysis\static\csv_files\TweetsData4.csv')
print(df.value_counts('tweet_type'))
