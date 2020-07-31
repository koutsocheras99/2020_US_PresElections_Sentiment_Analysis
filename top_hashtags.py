import tweepy
import re
import os
from datetime import datetime, timedelta
import time

hashtag_directory = 'hashtag_directory/'

def create_hashtag_directory_files():

    if not os.path.exists(hashtag_directory):
        try:
            # creating dataset folder
            os.mkdir(hashtag_directory)
            with open(hashtag_directory+'Historical_Hashtags.txt', 'w'): pass
            with open(hashtag_directory+'T-minus_3Months.csv', 'w'): pass
            with open(hashtag_directory+'T-minus_1Month.csv', 'w'): pass
            with open(hashtag_directory+'T-minus_1Week.csv', 'w'): pass
        except OSError:
            print('Error creating dataset directory!')

create_hashtag_directory_files()

# Authenticate to Twitter
auth = tweepy.OAuthHandler('VKNbSwqdncRIXmDPE5oZNOy9y', 'kZUYFCnXHrk7IBTZpMgRE9xRRSTdIKsBC9nIRZTbe8wNO3ltaW')
auth.set_access_token('1240790148213866497-7er0ZIdeeAkDzUBpiTcDTrZbPA5mGR', 'go1sdeNPojrqTQwxZsVHHO2cQpSYKaZuKDCoLt90zF2Q1')

# initialize the the tweepy object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def collect_hashtags():

    # WOEID for US
    woeid = 23424977

    # https://developer.twitter.com/en/docs/trends/trends-for-location/api-reference/get-trends-place
    trends = api.trends_place(woeid)

    # every time it collects the 50 most trending topics around the USA
    for element in trends:
        for trend in element['trends']:
            hashtag_trend = re.findall('^#', trend['name'])

            # if the trend is a hashtag and the tweet volume field is not none (check the above get-trends related link)
            if hashtag_trend and trend['tweet_volume'] != None:

                #print(trend['name']+','+str(trend['tweet_volume']))
                
                #writing it to the right file for future processing
                with open(hashtag_directory+'T-minus_3Months.csv', "a") as f:
                    f.write(trend['name']+','+str(trend['tweet_volume'])+'\n')

'''
# run for certain hours
max_limit = datetime.now() + timedelta(hours=24)

while max_limit > datetime.now():

    collect_hashtags()

    # every 1 hour collect the trending hashtags
    time.sleep(60*60)

# note: could also use schedule module (https://schedule.readthedocs.io/en/stable/api.html) to specify the exact date (3month-1month-1week)
'''

def filtering_hierarchy_collected_hashtags():
    # append them to a dictionary form(?), sort them by tweet volume (remove duplicates) and focus the election related
    pass