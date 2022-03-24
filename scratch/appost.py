import re
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

text = '@VodafoneUK I’m so happy when you are in the sun and you are keeping me safe 😂! Loving #InternationalDayOfHappiness what with being a smiler and all that it’s right up my street 😃'
with open(f'{os.getenv("STATIC_JSONFILES")}\contractions.json', 'r+') as file:
    contraction_dict = json.load(file)
# print(text.lower().split())

tokens = text.lower().replace('’', "'").split()
token_lis = []
for token in tokens:
    for key, value in contraction_dict.items():
        if token == key:
            token = contraction_dict[key]
    token_lis.append(token)
print(text)
print(' '.join(token_lis))


