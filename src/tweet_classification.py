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

print(cl.prob_classify('biden2020').prob('pos'))


'''
state_cities_dataset = 'state_cities/'

states = [f for f in os.listdir('state_cities')]

i=0

for state in states:

    with open(state_cities_dataset+state+'/biden_tweets.csv', 'r', encoding='utf-8') as f:
        
        tweets = f.readlines()

        for tweet in tweets:

            # lower the tweet
            tweet = tweet.lower()

            tweet = re.sub('[^#\w\s]','',tweet)

            if cl.prob_classify(tweet).prob('pos')>0.7 or cl.prob_classify(tweet).prob('pos')<0.3:
                # print(cl.prob_classify(tweet).prob('pos'))
                # print(tweet+str(cl.prob_classify(tweet).prob('pos')))
                i +=1

print(i)
'''