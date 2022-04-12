from connect import conn
import psycopg2


def create_tables():
    """ create tables in the PostgreSQL database"""
    command = (
        """
            create table IF NOT EXISTS reviews (
                tweet_id VARCHAR(255) NOT NULL, 
                author_id VARCHAR(255) NOT NULL,
                created_at TIMESTAMPTZ,
                tweet text,
                username VARCHAR(100),
                name VARCHAR(100),
                location VARCHAR(100),
                language VARCHAR(20),
                tweet_type VARCHAR(50),
                replied_to_id VARCHAR(255),
                get_repliedTo_tweet_link VARCHAR(255),
                get_tweet_link VARCHAR(255),
                clean_text text,
                prediction integer)
        """)

    try:
        #define cursor
        cur = conn.cursor()
        cur.execute(command)
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
    create_tables()