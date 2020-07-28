import tweepy
import pandas as pd
import os

state_cities_dataset = 'state_cities/'

# Authenticate to Twitter
auth = tweepy.OAuthHandler('VKNbSwqdncRIXmDPE5oZNOy9y', 'kZUYFCnXHrk7IBTZpMgRE9xRRSTdIKsBC9nIRZTbe8wNO3ltaW')
auth.set_access_token('1240790148213866497-7er0ZIdeeAkDzUBpiTcDTrZbPA5mGR', 'go1sdeNPojrqTQwxZsVHHO2cQpSYKaZuKDCoLt90zF2Q1')

# initialize the the tweepy object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

no_retweets = '-filter:retweets'

# check for format = list (example [trump,biden,republican,democrats]) and iterate(?) or simultaneously all values
search_keyword = 'trump' + no_retweets

def search_tweets(tweets_number, coordinates):

    # http://docs.tweepy.org/en/v3.9.0/api.html#help-methods
    get_tweets = tweepy.Cursor(api.search,
                            q=search_keyword, 
                            lang='en', 
                            result_type='recent',
                            geocode=coordinates).items(tweets_number)

    tweets_list = [tweet.text for tweet in get_tweets]

    # add newline after each element list for future operations -> writing the tweets in the csv files 
    newline_tweets_list = '\n'.join(tweets_list)
        
    return newline_tweets_list
    

def iterate_states():

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
            
            tweets = search_tweets(tweets_number=10, coordinates=f'{row[2]},{row[3]},20km')

            # utf-8 encoding to suuport(?) emoticons 
            # with open(state_cities_dataset+'/'+state+'/tweets.csv', 'a', encoding='utf-8') as f:
            #    f.write(str(tweets))
        
        # find an equation for the radius based on city population and cities in the state

# iterate_states() 

