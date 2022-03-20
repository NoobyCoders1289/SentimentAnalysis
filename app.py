from flask import Flask, redirect, render_template, url_for, flash


import psycopg2
conn_string = "host='localhost' dbname='blogappdb' user='postgres' password='123123123'"
conn = psycopg2.connect(conn_string)



app=Flask(__name__)
app.config['SECRET_KEY']='673b02697ceecbac65a9591ffeb47c0d'

tweets = [
    {
        "author_id":"1234345",
        "text":"hi all it is my first post",
        "created_at":"April 20, 2021",
        "username":"charan",
    },
    {
        "author_id":"1234343",
        "text":"hi all it is my second post",
        "created_at":"March 23, 2021",
        "username":"charan cherry",
    },
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',tweets=tweets)





#To run the app.py in debug Mode
if __name__=='__main__':
    app.run(debug=True)