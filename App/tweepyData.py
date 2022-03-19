import tweepy
import os
import time

import pandas as pd

import requests
from dotenv import load_dotenv
load_dotenv()

'''
TWITTER ID |TWITTER USERNAME
20678384   |@VodafoneUK
15133627   |@O2
158368965  |@ThreeUK
361268597  |@ThreeUKSupport
7117212    |@EE
118750085  |@bt_uk
17872077   |@virginmedia
'''

# your bearer token
MY_BEARER_TOKEN = os.getenv('BEARER_TOKEN')
# create your client
client = tweepy.Client(bearer_token=MY_BEARER_TOKEN)