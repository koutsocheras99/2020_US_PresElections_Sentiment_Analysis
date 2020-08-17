import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

train_test_dataset = 'training_dataset.csv'

# this function is for future training/testing (apply sentiment analysis lstm,svm or something familiar)
def train():

    with open(train_test_dataset, 'r', encoding='utf-8') as f:

        tweets = f.readlines()

        # initialize the tokenizer for Twitter
        # http://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.casual
        # it helps to keep the #rand_name together rather than separating it to two tokens ('#', 'rand_name')
        tokenizer = TweetTokenizer()

        for tweet in tweets:

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
        
# train()