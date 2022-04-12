from connect import conn
import psycopg2
import json
import pandas as pd


def insert_data(tweets_list):
    """ insert a new data into the tweets table """
    sql = """INSERT INTO tweets(tweet_id,
                                author_id,
                                created_at,
                                tweet,
                                username,
                                name,
                                location,
                                language,
                                tweet_type,
                                replied_to_id,
                                get_repliedTo_tweet_link,
                                get_tweet_link,
                                clean_text,
                                prediction)
     VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    
    try:
        #define cursor
        cur = conn.cursor()
        # insert table (single)
        cur.executemany(sql,tweets_list)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    df = pd.read_csv(r'sqlfiles\\sqlpython\\combined1345.csv')
    records = df.to_records(index=False)
    result = list(records)
    insert_data(result)

