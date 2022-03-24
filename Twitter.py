#TWITTER
#Twitter_API_with_Tweepy

#API key:             SbyT7jGEzl3mgU9QgQM2SAgtM
#API secret key:      ugNbaECnHhZ71Icp3OD2ZFRv3f7QANTygB8mI1JzBaRtH3nHSd

#Access token:        1148948208787349504-uKWz1DiqOQjh0epKRG5mZGBDzGVdUX
#Access token secret: Tt1LEClcakjiYMCnx7TWU4VUSdf8RDGBKoOCW4hcoHuVY

from itertools import count
import tweepy
import webbrowser
import time
import pandas as pd

# NEW (not yet approved by Twitter)
#consumer_key = 'SbyT7jGEzl3mgU9QgQM2SAgtM'
#consumer_secret = 'ugNbaECnHhZ71Icp3OD2ZFRv3f7QANTygB8mI1JzBaRtH3nHSd'

# OLD (approved by Twitter)
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

# new_status = api.update_status("Hello world, hope you are good learning with @joincfe :)")
# dir(new_status)
# new_status.destroy()

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

user = api.get_user(screen_name="DiePressecom")
timeline = user.timeline(count=200)
df = extract_timeline_as_df(timeline); df

