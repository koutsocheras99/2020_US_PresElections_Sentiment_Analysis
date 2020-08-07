import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

state_cities_dataset = 'state_cities/Wyoming/trump_republicans_tweets.csv'

def creating_training_dataset():
    with open(state_cities_dataset, 'r', encoding='utf-8') as f:
        tweets = f.readlines()
        for tweet in tweets:
            hashtag_appearance = re.findall('#',tweet)
            if hashtag_appearance:
                print(tweet)

creating_training_dataset()


# this function is for future training/testing (apply sentiment analysis lstm,svm or something familiar)
def pre_processing():

    with open(state_cities_dataset, 'r', encoding='utf-8') as f:

        tweets = f.readlines()

        # initialize the tokenizer for Twitter
        # http://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.casual
        # it helps to keep the #rand_name together rather than separating it to two tokens ('#', 'rand_name')
        tokenizer = TweetTokenizer()

        for tweet in tweets:

            # lower the tweet
            tweet = tweet.lower()

            tweet = re.sub('[^#\w\s]','',tweet)

            # tokenize the tweet
            tokens = tokenizer.tokenize(tweet)

            # remove some words that dont affect the meaning using the nltk stopwords
            for token in tokens:

                # if the (tokenized) word belongs to stopwords remove it
                if token in stopwords.words('english'):

                    tokens.remove(token)
                    
                list_to_tweet = ' '.join(tokens)

            print(list_to_tweet)
            #print(tweet)
            #print(str(tokens)+'\n')
        
# pre_processing()