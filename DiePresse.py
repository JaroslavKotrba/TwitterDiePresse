from nbformat import read
import tweepy
import webbrowser
import time
import pandas as pd

# Aapproved by Twitter
consumer_key = '7CGh9EyF3tgfsiU8HsC2gPDmL'
consumer_secret = 'H4UqkqF7rWJlc5ccISV62qRnUl3s5rSChjfZHfQ2EHLWrROcAw'

callback_uri = 'oob' # https://cfe.sh/twitter/callback

auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
redirect_url = auth.get_authorization_url()
print(redirect_url)

webbrowser.open(redirect_url) # --- GET pin: 

user_pin_input = input("What's the pin value?"); # 2178932

auth.get_access_token(user_pin_input)

print(auth.access_token, auth.access_token_secret)

api = tweepy.API(auth)

# For my timeline
my_timeline = api.home_timeline() # to get own time line
for status in my_timeline:
    # print(status.text) # to see tweets as timeline
    # print(status.user.screen_name) # to see authors of these tweets as timeline
    keys = vars(status).keys() # to see variables
    for key in keys:
        print(key)

# For other timelines
def extract_timeline_as_df(timeline_list):
    columns = set()
    allowed_types = [str, int]
    tweets_data = []
    for status in timeline_list:
        status_dict = dict(vars(status))
        keys = status_dict.keys()
        single_tweet_data = {"user":status.user.screen_name, "author":status.author.screen_name, "created_at":status.created_at}
        for k in keys:
            try:
                v_type = type(status_dict[k])
            except:
                v_type = None
            if v_type != None:
                if v_type in allowed_types:
                    single_tweet_data[k] = status_dict[k]
                    columns.add(k)
        tweets_data.append(single_tweet_data)

    header_cols = list(columns)
    header_cols.append("user")
    header_cols.append("author")
    header_cols.append("created_at")
    df = pd.DataFrame(tweets_data, columns=header_cols)
    return df

user = api.get_user(screen_name="BBCWorld")
timeline = user.timeline(count=200)
df = extract_timeline_as_df(timeline); df










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
    number_of_tweets = 500
    name = []
    tweet = []
    date = []
    like = []
    retweet = []

    for i in tweepy.Cursor(api.search_tweets, q=q, result_type='mixed', include_entities=False, lang = "en", tweet_mode='extended').items(number_of_tweets):
                name.append(i.user.screen_name)
                tweet.append(i.full_text)
                date.append(i.created_at)
                like.append(i.favorite_count)
                retweet.append(i.retweet_count)

    df = pd.DataFrame({'name':name, 'tweet':tweet, 'date':date, 'like':like, 'retweet':retweet})
    return df

df = extract_timeline_as_df('Pandemic'); df

df.to_csv('Twitter.csv',  index = False)

import pandas as pd
data = pd.read_csv('Twitter.csv'); data

# $date
data['date'] = pd.DatetimeIndex(data['date']).date
data['date'] = pd.to_datetime(data['date'])
data['date'].value_counts()

# TWEETS
# $length
data['length'] = data['tweet'].astype(str).map(len)
data

# $words
# Remove RT
data['tweet'] = data['tweet'].str[3:]

# To lower case
data['tweet'] = data['tweet'].str.lower()

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

df_words[0].value_counts().head(20)











BBC = extract_timeline_as_df('BBCWorld'); BBC
CNN = extract_timeline_as_df('cnnbrk'); CNN
NT = extract_timeline_as_df('nytimes'); NT

data = pd.concat([BBC, CNN, NT]); data

# $date
data['date'] = data['date'].astype(str)
data['date'] = pd.DatetimeIndex(data['date']).date
data['date'] = pd.to_datetime(data['date'])
data

import pandas as pd
writer = pd.ExcelWriter("/Users/HP/OneDrive/Documents/Python Anaconda/Twitter/Data_World.xlsx", engine='xlsxwriter') #CHANGE
data.to_excel(writer, sheet_name='data', index=False)
writer.save()







import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import re  
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

from twitterscraper import query_tweets
from twitterscraper.query import query_tweets_from_user
import datetime as dt 
import pandas as pd 









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

