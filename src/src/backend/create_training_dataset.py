from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import ast
import re
import os

# create a Naive Bayes Classifier using some keywords
keywords = []

with open('classification_keywords_less.txt', 'r') as f:
    content = f.read().splitlines()
    
    for element in content:  

        keywords.append(element)

keywords = (', '.join(keywords))

keywords = ast.literal_eval(keywords)   

cl = NaiveBayesClassifier(keywords)

# print(cl.prob_classify('biden2020').prob('pos'))


state_cities_dataset = 'state_cities/'

states = [f for f in os.listdir('state_cities')]

i=0

for state in states:
    
    # need to be run twice, 1 for trump 1 for biden
    with open(state_cities_dataset+state+'/trump_tweets.csv', 'r', encoding='utf-8') as f1,\
        open('training_dataset.csv', 'a', encoding='utf-8') as f2:
        
        f2.write('tweet,polarity\n')

        tweets = f1.readlines()

        for tweet in tweets:

            # lower the tweet
            tweet = tweet.lower().strip()

            tweet = re.sub('[^#\w\s]','',tweet)

            polarity = cl.prob_classify(tweet).prob('pos')

            # if clearly in favor of trump or biden
            if polarity>0.7 or polarity<0.3:
                
                # label = 1 if in favor of trump - 0 if in favor of biden
                label = (1 if polarity>0.7 else 0)

                # if hashtags remain in the training/testing dataset they(the hashtags) will interfere to the accuracy so remove them
                no_hashtags_tweet = re.sub('#[\w]*',' ',tweet).strip()

                # print(no_hashtags_tweet+str(polarity))
                i+=1

                f2.write(no_hashtags_tweet+', '+str(label)+'\n')
