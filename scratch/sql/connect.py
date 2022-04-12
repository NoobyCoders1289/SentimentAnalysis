import datetime
import psycopg2
import os

from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('host'),
    database=os.getenv('database'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    )



