# ---------------------------------------------------------------------------------------------------------------
# Die Presse ----------------------------------------------------------------------------------------------------

import os
path = "/Users/HP/OneDrive/Documents/Python Anaconda/Twitter"
os.chdir(path)

import tweepy
import webbrowser
import time
import pandas as pd

# Approved by Twitter
consumer_key = '7CGh9EyF3tgfsiU8HsC2gPDmL'
consumer_secret = 'H4UqkqF7rWJlc5ccISV62qRnUl3s5rSChjfZHfQ2EHLWrROcAw'
callback_uri = 'oob' # https://cfe.sh/twitter/callback

auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
redirect_url = auth.get_authorization_url()
print(redirect_url)

webbrowser.open(redirect_url) # --- GET pin: 

# ---------------------------------------------------------------------------------------------------------------
# API -----------------------------------------------------------------------------------------------------------

user_pin_input = input("Put the pin:__________"); # example 2178932

auth.get_access_token(user_pin_input)
api = tweepy.API(auth)

my_timeline = api.home_timeline() # to get own time line
for status in my_timeline: # to see list of variables
    keys = vars(status).keys()
    for key in keys:
        print(key)

# search_tweets user_timeline
def extract_timeline_as_df(q):
    number_of_tweets = 1000
    name = []
    tweet = []
    date = []
    like = []
    retweet = []

    # To get tweets
    for i in tweepy.Cursor(api.search_tweets, q=q, result_type='mixed', include_entities=False, lang = "en", tweet_mode='extended').items(number_of_tweets):
                name.append(i.user.screen_name)
                tweet.append(i.full_text)
                date.append(i.created_at)
                like.append(i.favorite_count)
                retweet.append(i.retweet_count)

    # To create data frame
    df = pd.DataFrame({'name':name, 'tweet':tweet, 'date':date, 'like':like, 'retweet':retweet})

    return df

df = extract_timeline_as_df('Pandemic'); df

# To make sure we have all with Pandemic
df_check = df[df['tweet'].str.contains('Pandemic|pandemic')]; df_check

df_check.to_csv('DiePresse.csv',  index = False)

# ---------------------------------------------------------------------------------------------------------------
# Feature engineering -------------------------------------------------------------------------------------------

import pandas as pd
data = pd.read_csv('DiePresse.csv'); data

# $tweet
import re
def deEmojify(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

data['tweet'] = data['tweet'].map(lambda x: deEmojify(x)); data['tweet']

# Remove RT
data['tweet'] = data['tweet'].str[3:]

# To lower case
data['tweet'] = data['tweet'].str.lower()

# $date
data['date'] = pd.DatetimeIndex(data['date']).date
data['date'] = pd.to_datetime(data['date'])
data['date'].value_counts()

# $length
data['length'] = data['tweet'].astype(str).map(len)

data

# Save tweets
data.to_csv('Tweets.csv',  index = False)

# ---------------------------------------------------------------------------------------------------------------
# NLP -----------------------------------------------------------------------------------------------------------

# To get list of tweets
all_tweets = []
for tweet in data.tweet:
    all_tweets.append(tweet)

all_tweets

# To get list of words
all_words = list()
for line in all_tweets:    
    word = line.split()
    for w in word: 
       all_words.append(w)

all_words

# To remove punctuation
import re
all_words = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in all_words]; all_words

# To remove empty strings
all_words_clean = []
for word in all_words:
    if word != '':
        all_words_clean.append(word)

all_words_clean

# To remove stop words
import en_core_web_sm
nlp = en_core_web_sm.load()

all_words_clean_stop = []

for word in all_words_clean:
    if word not in nlp.Defaults.stop_words:
        all_words_clean_stop.append(word)

all_words_clean_stop

# Data frame for all words
df_words = pd.DataFrame(all_words_clean_stop)

df_words_count = pd.DataFrame(df_words[0].value_counts())
df_words_count = df_words_count.reset_index(level=0)
df_words_count.columns = ['word', 'count']

df_words_count

# Save words
df_words_count.to_csv('Words.csv',  index = False)

# ---------------------------------------------------------------------------------------------------------------
# Database ------------------------------------------------------------------------------------------------------

import mysql.connector
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='twitter',
                                         user='root',
                                         password='8bulwark5')

    # name
    mySql_insert_query = """INSERT INTO name (NAME) VALUES (%s)"""

    records_to_insert = list(pd.DataFrame(data['name']).itertuples(index=False, name=None))

    cursor = connection.cursor()
    cursor.executemany(mySql_insert_query, records_to_insert)
    connection.commit()
    print(cursor.rowcount, "records inserted successfully into table")

    # tweet
    mySql_insert_query = """INSERT INTO tweet (TWEET) VALUES (%s)"""

    records_to_insert = list(pd.DataFrame(data['tweet']).itertuples(index=False, name=None))

    cursor = connection.cursor()
    cursor.executemany(mySql_insert_query, records_to_insert)
    connection.commit()
    print(cursor.rowcount, "records inserted successfully into table")

    # frequency
    mySql_insert_query = """INSERT INTO frequency (WORD, COUNT) VALUES (%s, %s)"""

    records_to_insert = list(df_words_count.itertuples(index=False, name=None))

    cursor = connection.cursor()
    cursor.executemany(mySql_insert_query, records_to_insert)
    connection.commit()
    print(cursor.rowcount, "records inserted successfully into table")

    # length
    mySql_insert_query = """INSERT INTO length (LENGTH) VALUES (%s)"""

    records_to_insert = list(pd.DataFrame(data['length']).itertuples(index=False, name=None))

    cursor = connection.cursor()
    cursor.executemany(mySql_insert_query, records_to_insert)
    connection.commit()
    print(cursor.rowcount, "records inserted successfully into table")

except mysql.connector.Error as error:
    print("Failed to insert record into table {}".format(error))

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")











# table = soup.find('table',{'class': 'table table-striped table-bordered'})
from twitterscraper import query_tweets
import datetime as dt
import pandas as pd

begin_date = dt.date(2022,1,1)
end_date = dt.date(2022,3,28)

limit = 500
lang = 'english'

tweets = query_tweets('Pandemic', begindate = begin_date, enddate = end_date, limit = limit, lang = lang)
df = pd.DataFrame(t.__dict__ for t in tweets)



import tweepy
import webbrowser
import time
import pandas as pd

consumer_key = "7CGh9EyF3tgfsiU8HsC2gPDmL"
consumer_key_secret = "H4UqkqF7rWJlc5ccISV62qRnUl3s5rSChjfZHfQ2EHLWrROcAw"
access_token = "AAAAAAAAAAAAAAAAAAAAAGYEFAEAAAAAxgSsWCCjsT6HCI%2Fg%2FMvN7%2FvYF%2F4%3DXJaCx5y8hVLN6uRz0gTbCAZMyU6tc8kpsuHESs0vWTTSQ8fDNf"
access_token_secret = "1148948208787349504-QP1Q6YnfPchQ4yJ2v9FfhL1TseIQTT"

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
print("Authenticated")

api = tweepy.API(auth)

user_info = api.get_user(screen_name='elonmusk')