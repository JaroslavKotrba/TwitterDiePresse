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

id = 'BBCWorld'
q = "Pandemic"
since="2022-01-01", 
until="2022-03-28"

# search_tweets user_timeline

def extract_timeline_as_df(id):
    number_of_tweets = 10
    name = []
    author = []
    tweet = []
    date = []
    like = []
    retweet = []

    for i in tweepy.Cursor(api.user_timeline, id=id, q='Pandemic', since="2022-01-01", until="2022-03-28", tweet_mode='extended').items(number_of_tweets):
                name.append(i.user.screen_name)
                author.append(i.author.screen_name,)
                tweet.append(i.full_text)
                date.append(i.created_at)
                like.append(i.favorite_count)
                retweet.append(i.retweet_count)

    df = pd.DataFrame({'name':name, 'author':name, 'tweet':tweet, 'date':date, 'like':like, 'retweet':retweet})
    return df

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

