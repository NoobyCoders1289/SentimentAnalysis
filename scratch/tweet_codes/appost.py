import re
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

text = '@VodafoneUK Iβm so happy when you are in the sun and you are keeping me safe π! Loving #InternationalDayOfHappiness what with being a smiler and all that itβs right up my street π'
with open(f'{os.getenv("STATIC_JSONFILES")}\contractions.json', 'r+') as file:
    contraction_dict = json.load(file)
# print(text.lower().split())

tokens = text.lower().replace('β', "'").split()
token_lis = []
for token in tokens:
    for key, value in contraction_dict.items():
        if token == key:
            token = contraction_dict[key]
    token_lis.append(token)
print(text)
print(' '.join(token_lis))


