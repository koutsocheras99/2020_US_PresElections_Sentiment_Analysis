import tweepy
from tweepy import TweepError
import pandas as pd
import os
import time
import re

state_cities_dataset = 'state_cities/'

# Authenticate to Twitter
auth = tweepy.OAuthHandler('VKNbSwqdncRIXmDPE5oZNOy9y', 'kZUYFCnXHrk7IBTZpMgRE9xRRSTdIKsBC9nIRZTbe8wNO3ltaW')
auth.set_access_token('1240790148213866497-7er0ZIdeeAkDzUBpiTcDTrZbPA5mGR', 'go1sdeNPojrqTQwxZsVHHO2cQpSYKaZuKDCoLt90zF2Q1')

# initialize the the tweepy object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

no_retweets = '-filter:retweets'

# check for format = list (example [trump,biden,republican,democrats]) and iterate(?) or simultaneously all values
search_keyword = 'trump' + no_retweets

# removing @(mentions) and links + transposing multiline tweets to one-line + removing whitespace left&right
def pre_filter(string):

    clear_mentions_links = re.sub('@\S*|http\S+', '', string)

    final_clear = re.sub('\n', ' ', clear_mentions_links).strip()

    return final_clear


def search_tweets(tweets_number, coordinates):

    # http://docs.tweepy.org/en/v3.9.0/api.html#help-methods
    get_tweets = tweepy.Cursor(api.search,
                            q=search_keyword, 
                            lang='en', 
                            count=100,
                            tweet_mode='extended',
                            result_type='recent',
                            geocode=coordinates).items(tweets_number)

    tweets_list = [pre_filter(tweet.full_text) for tweet in get_tweets]

    # add newline after each element list for future operations ..  writing the tweets in the csv files 
    newline_tweets_list = '\n'.join(tweets_list)
        
    return newline_tweets_list
    

def iterate_states():

    total_number_of_tweets = 0

    states = [f for f in os.listdir('state_cities')]

    for state in states:

        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html check the purpose of header=None
        cities_csv_file = pd.read_csv(state_cities_dataset+state+'/'+state+'.csv', header=None)

        number_of_cities_per_state = len(cities_csv_file)
        # print(number_of_cities_per_state)

        #iterate through the cities
        for _, row in cities_csv_file.iterrows():
            
            # population column
            # print(row[1])
            
            population_factor = min(20, row[1]*5e-5)
            cities_per_state_factor = max(7, 40/number_of_cities_per_state)

            # radius of search will depend on how much cities dense is the state and the population of each cities 
            # .2f for only 2 decimal numbers
            radius = f'{(population_factor + cities_per_state_factor):.2f}'
            # print(str(radius)+ ' ' + row[0]+' '+state)
            
            # number of tweets per city is correlated with pop/cities_dense but the city pop is more important
            number_of_tweets = int((population_factor)*30 + (cities_per_state_factor)*15)
        
            try:

                tweets = search_tweets(tweets_number=int(number_of_tweets), coordinates=f'{row[2]},{row[3]},{radius}km')
                
                # utf-8 encoding to suuport(?) emoticons .. else replace encoding parameter with errors='ignore'
                with open(state_cities_dataset+state+'/trump_republicans_tweets.csv', 'a', encoding='utf-8') as f:
                    f.write(str(tweets))


            # the reason for the try/except is the explicit close of the connection from the host(twitter) due to the long program duration
            # http://docs.tweepy.org/en/latest/api.html#tweepy-error-exceptions
            except TweepError as e:
                print(e)
                time.sleep(900)
                continue
            
            total_number_of_tweets+=number_of_tweets

        print(f'Finished writing with state: {state}!')
        
    print(total_number_of_tweets)

    
# iterate_states() 
