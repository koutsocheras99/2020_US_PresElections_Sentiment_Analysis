import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics import accuracy_score
import collections

class Classifier():

    def __init__(self):
        self.train_set, self.test_set = self.load_data()
        self.counts, self.test_counts = self.vectorize()
        self.multinomial_classifier = self.multinomial_model()
        self.bernoulli_classifier = self.bernoulli_model()

    # get training dataset and split training and testing
    def load_data(self):
        df = pd.read_csv('training_dataset.csv')
        train_set, test_set = train_test_split(df, test_size=0.2)
        return train_set, test_set

    # check for specifications https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html
    def multinomial_model(self):
        classifier = MultinomialNB()
        # targets = the second column of the training set aka the sentiment of each tweet
        targets = self.train_set['polarity']
        # training the model with the features(self.counts) and the labels(targets)
        classifier.fit(self.counts, targets)
        return classifier

    # check for specifications https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.BernoulliNB.html
    def bernoulli_model(self):
        # comments and guidelines are same as above (multinomial)
        classifier = BernoulliNB()
        targets = self.train_set['polarity']
        classifier.fit(self.counts, targets)
        return classifier

    # convert data to tf-idf features
    def vectorize(self):
        # check here for parameters details 
        # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
        # might need some more parameter adjustments-twists
        vectorizer = TfidfVectorizer(min_df=5,
                                 max_df = 0.7,
                                 ngram_range = (1,2),
                                 stop_words='english')
        counts = vectorizer.fit_transform(self.train_set['tweet'])
        test_counts = vectorizer.transform(self.test_set['tweet'])
        self._vectorizer = vectorizer
        return counts, test_counts

    def preprocess(self):
        # pairne ta tweet apo ta state kai katharize ta!
        pass

    # predict whether input is pro trump or pro biden with several ways
    def predict(self, input):
        input_text = input
        input_vectorizer = TfidfVectorizer(min_df=5,
                                 max_df = 0.7,
                                 ngram_range = (1,2))                               
        input_counts = self._vectorizer.transform(input_text)

        multinomial_predictions = self.multinomial_classifier.predict(input_counts)
        bernoulli_predictions = self.bernoulli_classifier.predict(input_counts)

        return multinomial_predictions, bernoulli_predictions

    # using accuracy score display score ON TESTING DATA
    def accuracy(self):
        test_counts,test_set = self.test_counts, self.test_set

        multinomial_predictions = self.multinomial_classifier.predict(test_counts)
        bernoulli_predictions = self.bernoulli_classifier.predict(test_counts)

        # check docs for accuracy_score https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html
        print('The accuracy score for multinomial bayes classifier is {:.2%}'.format(accuracy_score(test_set['polarity'], multinomial_predictions)))
        print('The accuracy score for bernoulli bayes classifier is {:.2%}'.format(accuracy_score(test_set['polarity'], bernoulli_predictions)))


model = Classifier()

new_data = ['joe biden has dignity','biden stands a chance in hell', 'trump is the worst', 'trunp is the best']

# random forest 92% sto test dataset alla se nea dokimastika data ta phgaine xalia, to idio me svc

multionomial_res, bernoulli = model.predict(new_data)
print(multionomial_res)
print(bernoulli)

# gia to posa einai uper trump/biden
# print(collections.Counter(multionomial_res))

model.accuracy()
